import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g 
from flask_restful import Api, Resource 
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model import review
from model import channel


from __init__ import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    content = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    park_id = db.Column(db.Integer, db.ForeignKey('parks.id'), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)

    park = db.relationship('park', backref=db.backref('reviews', lazy=True))
    channel = db.relationship('Channel', backref=db.backref('reviews', lazy=True))

    def __init__(self, title, comment, park_id, channel_id, content=None):
        self.title = title
        self.comment = comment
        self.park_id = park_id
        self.channel_id = channel_id
        self.content = content or {}

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def read(self):
        return {
            'id': self.id,
            'title': self.title,
            'comment': self.comment,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'park_id': self.park_id,
            'channel_id': self.channel_id
        }

"""
This Blueprint object is used to define APIs for the review model.
- Blueprint is used to modularize application files.
- This Blueprint is registered to the Flask app in main.py.
"""
review_api = Blueprint('review_api', __name__, url_prefix='/api')

"""
The Api object is connected to the Blueprint object to define the API endpoints.
- The API object is used to add resources to the API.
- The objects added are mapped to code that contains the actions for the API.
- For more information, refer to the API docs: https://flask-restful.readthedocs.io/en/latest/api.html
"""
api = Api(review_api)

class REVIEWAPI:
    """
    Define the API CRUD endpoints for the Review model.
    There are four operations that correspond to common HTTP methods:
    - review: create a new review
    - get: read reviews
    - put: update a review
    - delete: delete a review
    """
    class _CRUD(Resource):
        @token_required()
        def review(self):
            """
            Create a new review.
            """
            # Obtain the current park from the token required setting in the global context
            current_park = g.current_park
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()

            # Validate the presence of required keys
            if not data:
                return {'message': 'No input data provided'}, 400
            if 'title' not in data:
                return {'message': 'Review title is required'}, 400
            if 'comment' not in data:
                return {'message': 'Review comment is required'}, 400
            if 'channel_id' not in data:
                return {'message': 'Channel ID is required'}, 400
            if 'content' not in data:
                data['content'] = {}

            # Create a new review object using the data from the request
            review =Review(data['title'], data['comment'], current_park.id, data['channel_id'], data['content'])
            # Save the review object using the Object Relational Mapper (ORM) method defined in the model
            review.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(review.read())

        @token_required()
        def get(self):
            """
            Retrieve a single review by ID.
            """
            # Obtain and validate the request data sent by the RESTful client API
            data = request.get_json()
            if data is None:
                return {'message': 'Review data not found'}, 400
            if 'id' not in data:
                return {'message': 'Review ID not found'}, 400
            # Find the review to read
            review = review.query.get(data['id'])
            if review is None:
                return {'message': 'Review not found'}, 404
            # Convert Python object to JSON format 
            json_ready = review.read()
            # Return a JSON restful response to the client
            return jsonify(json_ready)

        @token_required()
        def put(self):
            """
            Update a review.
            """
            # Obtain the current park
            current_park = g.current_park
            # Obtain the request data
            data = request.get_json()
            # Find the current review from the database table(s)
            review = review.query.get(data['id'])
            if review is None:
                return {'message': 'review not found'}, 404
            # Update the review
            review._title = data['title']
            review._content = data['content']
            review._channel_id = data['channel_id']
            # Save the review
            review.update()
            # Return response
            return jsonify(review.read())

        @token_required()
        def delete(self):
            """
            Delete a review.
            """
            # Obtain the current park
            current_park = g.current_park
            # Obtain the request data
            data = request.get_json()
            # Find the current review from the database table(s)
            review = review.query.get(data['id'])
            if review is None:
                return {'message': 'Review not found'}, 404
            # Delete the review using the ORM method defined in the model
            review.delete()
            # Return response
            return jsonify({"message": "Review deleted"})

    class _park(Resource):
        @token_required()
        def get(self):
            """
            Retrieve all reviews by the current park.
            """
            # Obtain the current park
            current_park = g.current_park
            # Find all the reviews by the current park
            reviews = review.query.filter(Review._park_id == current_park.id).all()
            # Prepare a JSON list of all the reviews, using list comprehension
            json_ready = [review.read() for review in reviews]
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)

    class _BULK_CRUD(Resource):
        def review(self):
            """
            Handle bulk review creation by sending REVIEW requests to the single review endpoint.
            """
            reviews = request.get_json()

            if not isinstance(reviews, list):
                return {'message': 'Expected a list of review data'}, 400

            results = {'errors': [], 'success_count': 0, 'error_count': 0}

            with current_app.test_client() as client:
                for review in reviews:
                    # Simulate a review request to the single review creation endpoint
                    response = client.review('/api/review', json=review)

                    if response.status_code == 200:
                        results['success_count'] += 1
                    else:
                        results['errors'].append(response.get_json())
                        results['error_count'] += 1

            # Return the results of the bulk creation process
            return jsonify(results)
        
        def get(self):
            """
            Retrieve all reviews.
            """
            # Find all the reviews
            reviews = review.query.all()
            # Prepare a JSON list of all the reviews, using list comprehension
            json_ready = []
            for review in reviews:
                review_data = review.read()
                json_ready.append(review_data)
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)

    class _FILTER(Resource):
        @token_required()
        def review(self):
            """
            Retrieve all reviews by channel ID and park ID.
            """
            # Obtain and validate the request data sent by the RESTful client API
            data = request.get_json()
            if data is None:
                return {'message': 'Channel and park data not found'}, 400
            if 'channel_id' not in data:
                return {'message': 'Channel ID not found'}, 400
            
            # Find all reviews by channel ID and park ID
            reviews = review.query.filter_by(_channel_id=data['channel_id']).all()
            # Prepare a JSON list of all the reviews, using list comprehension
            json_ready = [review.read() for review in reviews]
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)

    """
    Map the _CRUD, _park, _BULK_CRUD, and _FILTER classes to the API endpoints for /review, /review/park, /reviews, and /reviews/filter.
    - The API resource class inherits from flask_restful.Resource.
    - The _CRUD class defines the HTTP methods for the API.
    - The _park class defines the endpoints for retrieving reviews by the current park.
    - The _BULK_CRUD class defines the bulk operations for the API.
    - The _FILTER class defines the endpoints for filtering reviews by channel ID and park ID.
    """
    api.add_resource(_CRUD, '/review')
    api.add_resource(_park, '/review/park')
    api.add_resource(_BULK_CRUD, '/reviews')
    api.add_resource(_FILTER, '/reviews/filter')
