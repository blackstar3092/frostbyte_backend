import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.camping_post import camping
from model.channel import Channel


"""
This Blueprint object is used to define APIs for the Post model.
- Blueprint is used to modularize application files.
- This Blueprint is registered to the Flask app in main.py.
"""
camping_api = Blueprint('camping_api', __name__, url_prefix='/api')

"""
The Api object is connected to the Blueprint object to define the API endpoints.
- The API object is used to add resources to the API.
- The objects added are mapped to code that contains the actions for the API.
- For more information, refer to the API docs: https://flask-restful.readthedocs.io/en/latest/api.html
"""
api = Api(camping_api)

class CampingAPI:
    """
    Define the API CRUD endpoints for the Post model.
    There are four operations that correspond to common HTTP methods:
    - post: create a new post
    - get: read posts
    - put: update a post
    - delete: delete a post
    """
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

    class _USER(Resource):
        @token_required()
        def get(self):
            """
            Retrieve all posts by the current user.
            """
            # Obtain the current user
            current_user = g.current_user
            # Find all the posts by the current user
            campingPosts = camping.query.filter(camping._user_id == current_user.id).all()
            # Prepare a JSON list of all the posts, using list comprehension
            json_ready = [campingPost.read() for campingPost in campingPosts]
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)

    class _BULK_CRUD(Resource):
        def Post(self):
            """
            Handle bulk post creation by sending POST requests to the single post endpoint.
            """
            campingPosts = request.get_json()

            if not isinstance(campingPosts, list):
                return {'message': 'Expected a list of post data'}, 400

            results = {'errors': [], 'success_count': 0, 'error_count': 0}

            with current_app.test_client() as client:
                for campingPost in campingPosts:
                    # Simulate a POST request to the single post creation endpoint
                    response = client.post('/api/campingPost', json=campingPost)

                    if response.status_code == 200:
                        results['success_count'] += 1
                    else:
                        results['errors'].append(response.get_json())
                        results['error_count'] += 1

            # Return the results of the bulk creation process
            return jsonify(results)
        
        def get(self):
            """
            Retrieve all posts.
            """
            # Find all the posts
            campingPosts = camping.query.all()
            # Prepare a JSON list of all the posts, using list comprehension
            json_ready = []
            for campingPost in campingPosts:
                campingPost_data = campingPost.read()
                json_ready.append(campingPost_data)
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)

    class _FILTER(Resource):
        @token_required()
        def campingPost(self):
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

    """
    Map the _CRUD, _USER, _BULK_CRUD, and _FILTER classes to the API endpoints for /post, /post/user, /posts, and /posts/filter.
    - The API resource class inherits from flask_restful.Resource.
    - The _CRUD class defines the HTTP methods for the API.
    - The _USER class defines the endpoints for retrieving posts by the current user.
    - The _BULK_CRUD class defines the bulk operations for the API.
    - The _FILTER class defines the endpoints for filtering posts by channel ID and user ID.
    """
    api.add_resource(_CRUD, '/campingPost')
    api.add_resource(_USER, '/campingPost/user')
    api.add_resource(_BULK_CRUD, '/campingPosts')
    api.add_resource(_FILTER, '/campingPosts/filter')