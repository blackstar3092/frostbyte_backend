import jwt
from flask import Blueprint, request, jsonify, current_app, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.rating import Rating  
from model.post import Post 

# Blueprint for Post API
star_api = Blueprint('star_api', __name__, url_prefix='/api')
api = Api(star_api)

class StarAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Create a new post."""
            current_user = g.current_user
            data = request.get_json()

            if not data or 'title' not in data or 'comment' not in data or 'channel_id' not in data:
                return {'message': 'Missing required fields'}, 400

            post = Rating(data['title'], data['comment'], current_user.id, data['channel_id'], data.get('content', {}))
            post.create()
            return jsonify(post.read())

        @token_required()
        def get(self):
            """Retrieve a single post by ID."""
            data = request.get_json()
            if not data or 'id' not in data:
                return {'message': 'Post ID not found'}, 400

            post = Rating.query.get(data['id'])
            if not post:
                return {'message': 'Post not found'}, 404

            return jsonify(post.read())

    class _RATING(Resource):
        @token_required()
        def post(self):
            """Store a star rating."""
            current_user = g.current_user
            data = request.get_json()

            if not data or 'stars' not in data or 'post_id' not in data:
                return {'message': 'Missing required fields (stars, post_id)'}, 400

            stars = data['stars']
            if not isinstance(stars, int) or stars < 1 or stars > 5:
                return {'message': 'Invalid star rating. Must be an integer between 1 and 5.'}, 400

            post = Rating.query.get(data['post_id'])
            if not post:
                return {'message': 'Post not found'}, 404

            rating = Rating(stars=stars, user_id=current_user.id, post_id=post.id)
            rating.create()

            return {'message': 'Rating submitted successfully'}, 201

        @token_required()
        def get(self):
            """Retrieve all ratings for a post."""
            data = request.get_json()

            if not data or 'post_id' not in data:
                return {'message': 'Post ID is required'}, 400

            post = Rating.query.get(data['post_id'])
            if not post:
                return {'message': 'Post not found'}, 404
            
            ratings = Rating.query.filter_by(post_id=post.id).all()
            json_ready = [rating.read() for rating in ratings]

            return jsonify({
                "ratings": json_ready
            })

    # Map resources to endpoints
    api.add_resource(_CRUD, '/post')  # Handles post creation and retrieval
    api.add_resource(_RATING, '/rating')  # Handles ratings

