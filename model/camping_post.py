from flask_sqlalchemy import SQLAlchemy
from sqlite3 import IntegrityError
from sqlalchemy import Text, JSON
from sqlalchemy.exc import IntegrityError
from __init__ import app, db
from model.frostbyte import Frostbyte
from model.channel import Channel
from sqlalchemy.orm import relationship

class campingPost(db.Model):
    __tablename__ = 'campingPost'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('frostbytes.id'), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)

    def __init__(self, title, comment, user_id=None, channel_id=None):
        self.title = title
        self.comment = comment
        self.user_id = user_id
        self.channel_id = channel_id


    def create(self):
        db.session.add(self)
        db.session.commit()
        
    def read(self):
        user = Frostbyte.query.get(self.user_id)
        channel = Channel.query.get(self.channel_id)
        data = {
            "id": self.id,
            "title": self.title,
            "comment": self.comment,
            "user_id": user.id if user else None,
            "channel_id": channel.id if channel else None
        }
        return data

    def update(self, inputs):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

def initCampingPosts():
    from model.camping_post import campingPost
    with app.app_context():
        """Create database and tables"""
        db.create_all()

        """Tester data for camping posts"""
        post1 = campingPost(title="Desert Adventure", comment="Surprisingly enjoyed camping in the desert", user_id=1, channel_id=8)
        post2 = campingPost(title="Beach Camping", comment="highly reccomend", user_id=2, channel_id=7)
        posts = [post1, post2]

    for post in posts:
        try:
            post.create()
            print("Created camping post: {post.title}")
        except IntegrityError:
            """Fails with bad or duplicate data"""
            db.session.rollback()
            print("Error creating camping post: {post.title}")
