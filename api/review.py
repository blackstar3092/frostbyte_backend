import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.review import review
from model.channel import Channel

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

class reviewAPI:
    """
    Define the API CRUD endpoints for the review model.
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
            # Obtain the current user from the token required setting in the global context
            current_user = g.current_user
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()

            # Validate the presence of required keys
            if not data:
                return {'message': 'No input data provided'}, 400
            if 'title' not in data:
                return {'message': 'review title is required'}, 400
            if 'comment' not in data:
                return {'message': 'review comment is required'}, 400
            if 'channel_id' not in data:
                return {'message': 'Channel ID is required'}, 400
            if 'content' not in data:
                data['content'] = {}

            # Create a new review object using the data from the request
            review = review(data['title'], data['comment'], current_user.id, data['channel_id'], data['content'])
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
                return {'message': 'review data not found'}, 400
            if 'id' not in data:
                return {'message': 'review ID not found'}, 400
            # Find the review to read
            review = review.query.get(data['id'])
            if review is None:
                return {'message': 'review not found'}, 404
            # Convert Python object to JSON format 
            json_ready = review.read()
            # Return a JSON restful response to the client
            return jsonify(json_ready)

        @token_required()
        def put(self):
            """
            Update a review.
            """
            # Obtain the current user
            current_user = g.current_user
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
            # Obtain the current user
            current_user = g.current_user
            # Obtain the request data
            data = request.get_json()
            # Find the current review from the database table(s)
            review = review.query.get(data['id'])
            if review is None:
                return {'message': 'review not found'}, 404
            # Delete the review using the ORM method defined in the model
            review.delete()
            # Return response
            return jsonify({"message": "review deleted"})

    class _USER(Resource):
        @token_required()
        def get(self):
            """
            Retrieve all reviews by the current user.
            """
            # Obtain the current user
            current_user = g.current_user
            # Find all the reviews by the current user
            reviews = review.query.filter(review._user_id == current_user.id).all()
            # Prepare a JSON list of all the reviews, using list comprehension
            json_ready = [review.read() for review in reviews]
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)

    class _BULK_CRUD(Resource):
        def review(self):
            """
            Handle bulk review creation by sending POST requests to the single review endpoint.
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
            Retrieve all reviews by channel ID and user ID.
            """
            # Obtain and validate the request data sent by the RESTful client API
            data = request.get_json()
            if data is None:
                return {'message': 'Channel and User data not found'}, 400
            if 'channel_id' not in data:
                return {'message': 'Channel ID not found'}, 400
            
            # Find all reviews by channel ID and user ID
            reviews = review.query.filter_by(_channel_id=data['channel_id']).all()
            # Prepare a JSON list of all the reviews, using list comprehension
            json_ready = [review.read() for review in reviews]
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)

    """
    Map the _CRUD, _USER, _BULK_CRUD, and _FILTER classes to the API endpoints for /review, /review/user, /reviews, and /reviews/filter.
    - The API resource class inherits from flask_restful.Resource.
    - The _CRUD class defines the HTTP methods for the API.
    - The _USER class defines the endpoints for retrieving reviews by the current user.
    - The _BULK_CRUD class defines the bulk operations for the API.
    - The _FILTER class defines the endpoints for filtering reviews by channel ID and user ID.
    """
    api.add_resource(_CRUD, '/review')
    api.add_resource(_USER, '/review/user')
    api.add_resource(_BULK_CRUD, '/reviews')
    api.add_resource(_FILTER, '/reviews/filter')