import jwt
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.post import Post
from model.likes import Likes

# Define the Blueprint for the Likes API
likes_api = Blueprint('likes_api', __name__, url_prefix='/api')

# Connect the Api object to the Blueprint
api = Api(likes_api)

class LikesAPI:
    """
    Define the API CRUD endpoints for the Likes model.
    There are operations for upvoting, downvoting, and retrieving likess for a post.
    """

    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create or update a likes (uplikes or downlikes) for a post.
            """
            # Get current user from the token
            current_user = g.current_user
            # Get the request data
            data = request.get_json()

            # Validate required fields
            if not data or 'post_id' not in data or 'rating' not in data:
                return {'message': 'Post ID and rating are required'}, 400
            if not (1 <=data['rating'] <=5):
                return {'message':'Rating must be between 1 and 5'}, 400
            # Check if the likes already exists for the user on the post
            existing_likes = Likes.query.filter_by(_post_id=data['post_id'], _user_id=current_user.id).first()
            if existing_likes:
                # Update the existing likes type
                existing_likes._likes_type = data ['likes_type']
                existing_likes.create()  # This will commit the update
                return jsonify(existing_likes.read())

            # Create a new likes object
            likes = Likes(data['likes_type'], current_user.id, data['post_id'])
            # Save the likes using the ORM method
            likes.create()
            # Return the saved likes in JSON format
            return jsonify(likes.read())

        @token_required()
        def delete(self):
            """
            Remove a likes by a user on a specific post.
            """
            # Get current user from the token
            current_user = g.current_user
            # Get the request data
            data = request.get_json()

            # Validate required fields
            if not data or 'post_id' not in data:
                return {'message': 'Post ID is required'}, 400

            # Find the likes by user and post
            likes = Likes.query.filter_by(_post_id=data['post_id'], _user_id=current_user.id).first()
            if likes is None:
                return {'message': 'Likes not found'}, 404

            # Delete the likes
            likes.delete()
            return jsonify({"message": "Likes removed"})

    class _POST_LIKES(Resource):
        def get(self):
            """
            Retrieve all likess for a specific post, including counts of uplikess and downlikes.
            """
            # Attempt to get post_id from query parameters first
            post_id = request.args.get('post_id')
            
            # If not found in query params, try to parse from JSON body
            if not post_id:
                try:
                    data = request.get_json()
                    post_id = data.get('post_id') if data else None
                except:
                    return {'message': 'Post ID is required either as a query parameter or in the JSON body'}, 400

            if not post_id:
                return {'message': 'Post ID is required'}, 400

            # Get all likess for the post
            likes = Likes.query.filter_by(_post_id=post_id).all()
            uplikes = [likes.read() for likes in likes if likes._likes_type == 'uplikes']
            downlikes = [likes.read() for likes in likes if likes._likes_type == 'downlikes']

            result = {
                "post_id": post_id,
                "uplikes_count": len(uplikes),
                "downlikes_count": len(downlikes),
                "uplikes": uplikes,
                "downlikes": downlikes
            }
            return jsonify(result)

    """
    Map the _CRUD and _POST_LIKES classes to the API endpoints for /likes and /likes/post.
    - The _CRUD class defines the HTTP methods for voting (post and delete).
    - The _POST_LIKES class defines the endpoint for retrieving all likess for a specific post.
    """
    api.add_resource(_CRUD, '/likes')
    api.add_resource(_POST_LIKES, '/likes/post')
