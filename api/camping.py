import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.camping_post import camping
from model.channel import Channel


camping_api = Blueprint('camping_api', __name__, url_prefix='/api')

api = Api(camping_api)

class CampingAPI:
    
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create a new post.
            """
            # Obtain the current user from the token required setting in the global context
            current_user = g.current_user
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()

            # Validate the presence of required keys
            if not data:
                return {'message': 'No input data provided'}, 400
            if 'title' not in data:
                return {'message': 'Post title is required'}, 400
            if 'comment' not in data:
                return {'message': 'Post comment is required'}, 400
            if 'channel_id' not in data:
                return {'message': 'Channel ID is required'}, 400

            # Create a new post object using the data from the request
            campingPost = camping(data['title'], data['comment'], current_user.id, data['channel_id'])
            # Save the post object using the Object Relational Mapper (ORM) method defined in the model
            campingPost.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(campingPost.read())

        @token_required()
        def get(self):
            """
            Retrieve a single post by ID.
            """
            # Obtain and validate the request data sent by the RESTful client API
            data = request.get_json()
            if data is None:
                return {'message': 'Post data not found'}, 400
            if 'id' not in data:
                return {'message': 'Post ID not found'}, 400
            # Find the post to read
            campingPost = camping.query.get(data['id'])
            if campingPost is None:
                return {'message': 'Post not found'}, 404
            # Convert Python object to JSON format 
            json_ready = campingPost.read()
            # Return a JSON restful response to the client
            return jsonify(json_ready)

        @token_required()
        def put(self):
            """
            Update a post.
            """
            # Obtain the current user
            current_user = g.current_user
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            campingPost = camping.query.get(data['id'])
            if campingPost is None:
                return {'message': 'Post not found'}, 404
            # Update the post
            campingPost._title = data['title']
            campingPost._channel_id = data['channel_id']
            # Save the post
            campingPost.update()
            # Return response
            return jsonify(campingPost.read())

        @token_required()
        def delete(self):
            """
            Delete a post.
            """
            # Obtain the current user
            current_user = g.current_user 
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            campingPost = camping.query.get(data['id'])
            if campingPost is None:
                return {'message': 'Post not found'}, 404
            # Delete the post using the ORM method defined in the model
            campingPost.delete()
            # Return response
            return jsonify({"message": "Post deleted"})
    class _FILTER(Resource):
        @token_required()
        def post(self):
            """
            Retrieve all posts by channel ID and user ID.
            """
            # Obtain and validate the request data sent by the RESTful client API
            data = request.get_json()
            if data is None:
                return {'message': 'Channel and User data not found'}, 400
            if 'channel_id' not in data:
                return {'message': 'Channel ID not found'}, 400
            
            # Find all posts by channel ID and user ID
            campingPosts = camping.query.filter_by(_channel_id=data['channel_id']).all()
            # Prepare a JSON list of all the posts, using list comprehension
            json_ready = [campingPost.read() for campingPost in campingPosts]
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)

   
    api.add_resource(_CRUD, '/campingPost')
    api.add_resource(_FILTER, '/campingPosts/filter')