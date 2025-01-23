import jwt
from flask import Blueprint, request, jsonify, current_app, g, make_response
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app, db
from api.jwt_authorize import token_required
from model.rating import Rating  
#from model.post import Post 
from model.channel import Channel
from model.frostbyte import Frostbyte

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

            channel = Rating.query.get(data['id'])
            if not channel:
                return {'message': 'channel not found'}, 404

            return jsonify(channel.read())

    class _RATING(Resource):
        @token_required()
        def post(self):
            """Handle both storing and fetching ratings."""
            current_user = g.current_user
            data = request.get_json()

            # If 'stars' is in the request body, handle storing a rating
            if 'stars' in data:
                # Validate required fields
                if not data or 'stars' not in data or 'channel_id' not in data:
                    return {'message': 'Missing required fields (stars, channel_id)'}, 400

                stars = data['stars']
                channel_id = data['channel_id']

                # Validate stars
                if not isinstance(stars, int) or stars < 1 or stars > 5:
                    return {'message': 'Invalid star rating. Must be an integer between 1 and 5.'}, 400

                # Check if the channel exists
                channel = Channel.query.get(channel_id)
                if not channel:
                    return {'message': 'Channel not found'}, 404

                # Create or update the rating
                rating = Rating.query.filter_by(user_id=current_user.id, channel_id=channel.id).first()
                if rating:
                    rating.stars = stars  # Update the stars if the rating already exists
                else:
                    rating = Rating(stars=stars, user_id=current_user.id, channel_id=channel.id)
                    db.session.add(rating)

                db.session.commit()
                return {'message': 'Rating submitted successfully', 'rating': rating.read()}, 201

            # If 'stars' is NOT in the request body, assume it's a fetch request
            elif 'user_id' in data and 'channel_id' in data:
                user_id = data.get('user_id')
                channel_id = data.get('channel_id')

                # Validate request data
                if not user_id or not channel_id:
                    return {'message': 'Missing user_id or channel_id in request body'}, 400

                # If user_id is a string (e.g., a name like "toby"), map it to its ID
                if isinstance(user_id, str):  # If user_id is passed as a name
                    print(f"Searching for user with name: {user_id}")
                    user = Frostbyte.query.filter_by(_uid=user_id).first()
                    if not user:
                        print(f"User '{user_id}' not found in the database.")
                        return {'message': f'User "{user_id}" not found'}, 404
                    user_id = user.id
                    print(f"Found user: {user.name} with ID: {user.id}")

                # Query the Rating table for the user's rating for the given channel
                rating = Rating.query.filter_by(user_id=user_id, channel_id=channel_id).first()

                if not rating:
                    return {'message': 'No rating found for the specified user and channel'}, 404

                return jsonify({'stars': rating.stars})

            # If neither case matches, return an error
            return {'message': 'Invalid request'}, 400




        @token_required()
        def get(self):
            """Retrieve all ratings for a post."""
            data = request.get_json()

            if not data or 'channel_id' not in data:
                return {'message': 'Channel ID is required'}, 400

            ratings = Rating.query.filter_by(channel_id=data['channel_id']).all()
            if not ratings:
                return {'message': 'No ratings found for this channel'}, 404

            return jsonify({
                "ratings": [rating.read() for rating in ratings]
            })
        
        @token_required()
        def delete(self):
            """Delete all ratings by a specific user."""
            data = request.get_json()
            user_id = data.get('user_id')

            # Validate user_id
            if not user_id:
                return {'message': 'Missing user_id in request body'}, 400

            # Query the User table to ensure the user exists
            user = Frostbyte.query.filter_by(_uid=user_id).first()  # Match by _uid
            if not user:
                return {'message': f'User "{user_id}" not found'}, 404

            # Delete all ratings by the user
            deleted_count = Rating.query.filter_by(user_id=user.id).delete()
            db.session.commit()

            if deleted_count == 0:
                return {'message': 'No ratings found for the specified user'}, 404

            return {'message': f'Deleted {deleted_count} rating(s) for user "{user_id}"'}, 200

        def initialize_sample_data_ratings(cls):
        # Check if ratings already exist to avoid duplicates
            if cls.query.count() > 0:
                print("Sample data already exists in the ratings table.")
                return  # Skip adding data if it already exists

            sample_ratings = [
                {"stars": 5, "user_id": 1, "channel_id": 10},
                {"stars": 4, "user_id": 2, "channel_id": 11},
                {"stars": 3, "user_id": 3, "channel_id": 12},
                {"stars": 2, "user_id": 2, "channel_id": 13},
                {"stars": 1, "user_id": 1, "channel_id": 10},
            ]
            
            for data in sample_ratings:
                rating = Rating(stars=data["stars"], user_id=data["user_id"], channel_id=data["channel_id"])
                db.session.add(rating)
            
            db.session.commit()
            print("Sample data initialized in the ratings table.")

    # Map resources to endpoints
    api.add_resource(_CRUD, '/post')  # Handles post creation and retrieval
    api.add_resource(_RATING, '/rating')  # Handles ratings

