from flask_sqlalchemy import SQLAlchemy
import logging
from sqlite3 import IntegrityError
from sqlalchemy import Text, JSON
from sqlalchemy.exc import IntegrityError
from __init__ import app, db
from model.frostbyte import Frostbyte
from model.channel import Channel
from sqlalchemy.orm import relationship

class camping(db.Model):

    __tablename__ = 'campingPosts'

    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(255), nullable=False)
    _comment = db.Column(db.String(255), nullable=False)
    _user_id = db.Column(db.Integer, db.ForeignKey('frostbytes.id', ondelete='SET NULL'), nullable=True)
    _channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False, default=1)  # Replace 1 with a valid default ID
    
    def __init__(self, title, comment, user_id=None, channel_id=None, user_name=None, channel_name=None):
        
        self._title = title
        self._comment = comment
        self._user_id = user_id
        self._channel_id = channel_id


    def __repr__(self):
        
        return f"campingPost(id={self.id}, title={self._title}, comment={self._comment}, user_id={self._user_id}, channel_id={self._channel_id})"

    def create(self):
        
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not create post with title '{self._title}' due to {str(e)}.")
            return None
        return self
        
    def read(self):
        """
        The read method retrieves the object data from the object's attributes and returns it as a dictionary.
        
        Uses:
            The Channel.query and User.query methods to retrieve the channel and user objects.
        
        Returns:
            dict: A dictionary containing the post data, including user and channel names.
        """
        user = Frostbyte.query.get(self._user_id)
        channel = Channel.query.get(self._channel_id)
        data = {
            "id": self.id,
            "title": self._title,
            "comment": self._comment,
            "user_name": user.name if user else None,
            "channel_name": channel.name if channel else None
        }
        return data
    

    '''def update(self):
        """
        Updates the post object with new data.
        
        Args:
            inputs (dict): A dictionary containing the new data for the post.
        
        Returns:
            Post: The updated post object, or None on error.
        """
        
        inputs = Post.query.get(self.id)
        
        title = inputs._title
        content = inputs._content
        channel_id = inputs._channel_id
        user_name = Frostbyte.query.get(inputs._user_id).name if inputs._user_id else None
        channel_name = Channel.query.get(inputs._channel_id).name if inputs._channel_id else None

        # If channel_name is provided, look up the corresponding channel_id
        if channel_name:
            channel = Channel.query.filter_by(_name=channel_name).first()
            if channel:
                channel_id = channel.id
                
        if user_name:
            user = Frostbyte.query.filter_by(_name=user_name).first()
            if user:
                user_id = user.id
            else:
                return None

        # Update table with new data
        if title:
            self._title = title
        if content:
            self._content = content
        if channel_id:
            self._channel_id = channel_id
        if user_id:
            self._user_id = user_id

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not update post with title '{title}' due to missing channel_id.")
            return None
        return self'''
    

    def update(self, inputs):
        """
        Updates the post object with new data.
        
        Args:
            inputs (dict): A dictionary containing the new data for the post.
        
        Returns:
            Post: The updated post object, or None on error.
        """
        if not isinstance(inputs, dict):
            return None  # Return None if inputs are invalid

        # Update fields from inputs
        for key, value in inputs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        # Commit changes to the database
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not update post due to {str(e)}.")
            return None
        return self

    
    def delete(self):
        """
        The delete method removes the object from the database and commits the transaction.
        
        Uses:
            The db ORM methods to delete and commit the transaction.
        
        Raises:
            Exception: An error occurred when deleting the object from the database.
        """    
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    ''' @staticmethod
    def restore(data):
        for post_data in data:
            _ = post_data.pop('id', None)  # Remove 'id' from post_data
            title = post_data.get("title", None)
            post = Post.query.filter_by(_title=title).first()
            if post:
                post.update(post_data)
            else:
                post = Post(**post_data)
                post.update(post_data)
                post.create()''' 
    
    ''' @staticmethod
    def restore(data):
        """
        Restores posts from the given data.
        
        Args:
            data (list): A list of dictionaries representing posts to restore.
        """
        for post_data in data:
            post_id = post_data.pop('id', None)  # Remove 'id' from post_data if present
            post = Post.query.filter_by(_title=post_data.get("title")).first()

            if post:
                post.update(post_data)  # Update existing post
            else:
                new_post = Post(**post_data)  # Create new post
                new_post.create()'''
    
    @staticmethod
    def restore(data):
        for campingPost_data in data:
            _ = campingPost_data.pop('id', None)  # Remove 'id' from post_data
            title = campingPost_data.get("title", None)
            campingPost = camping.query.filter_by(_title=title).first()
            if campingPost:
                campingPost.update(campingPost_data)
            else:
                campingPost = campingPost(**campingPost_data)
                campingPost.update(campingPost_data)
                campingPost.create()

        
def initCampingPosts():
    """
    The initPosts function creates the Post table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        Post objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """        
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        campingPosts = [
            camping(title='Cool Experience', comment='aquatic camping was new and fun', user_id=1, channel_id=7),
            camping(title='My next trip', comment='thinking of camping at the desert next', user_id=1, channel_id=8),
        ]
        
        for campingPost in campingPosts:
            try:
                campingPost.create()
                print(f"Record created: {repr(campingPost)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {campingPost._title}")