import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.likes import Likes
from model.group import Group
from model.user import User

"""
This Blueprint object is used to define APIs for the Likes model.
- Blueprint is used to modularize application files.
- This Blueprint is registered to the Flask app in main.py.
"""
likes_api = Blueprint('likes_api', __name__, url_prefix='/api')

"""
The Api object is connected to the Blueprint object to define the API endpoints.
- The API object is used to add resources to the API.
- The objects added are mapped to code that contains the actions for the API.
- For more information, refer to the API docs: https://flask-restful.readthedocs.io/en/latest/api.html
"""
api = Api(likes_api)

class LikesAPI:
    """
    Define the API CRUD endpoints for the Likes model.
    There are four operations that correspond to common HTTP methods:
    - post: create a new likes
    - get: read likess
    - put: update a likes
    - delete: delete a likes
    """
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create a new like.
            """
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            
            # Validate the presence of required keys
            if not data:
                return {'message': 'No input data provided'}, 400
            if 'name' not in data:
                return {'message': 'Likes name is required'}, 400
            if 'group_id' not in data:
                return {'message': 'Group ID is required'}, 400
            if 'attributes' not in data:
                data['attributes'] = {}
                
            # Create a new likes object using the data from the request
            likes = Likes(data['name'], data['group_id'], data.get('attributes', {}))
            # Save the likes object using the Object Relational Mapper (ORM) method defined in the model
            likes.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(likes.read())

        @token_required()
        def get(self):
            """
            Retrieve a single likes by ID.
            """
            # Obtain and validate the request data sent by the RESTful client API
            data = request.get_json()
            if data is None:
                return {'message': 'Likes data not found'}, 400
            if 'id' not in data:
                return {'message': 'Likes ID not found'}, 400
            # Find the likes to read
            likes = Likes.query.get(data['id'])
            if likes is None:
                return {'message': 'Likes not found'}, 404
            # Convert Python object to JSON format 
            json_ready = likes.read()
            # Return a JSON restful response to the client
            return jsonify(json_ready)

        @token_required()
        def put(self):
            """
            Update a like.
            """
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Find the likes to update
            likes = Likes.query.get(data['id'])
            if likes is None:
                return {'message': 'Likes not found'}, 404
            # Update the likes object using the data from the request
            likes._name = data['name']
            likes._group_id = data['group_id']
            likes._attributes = data.get('attributes', {})
            # Save the likes object using the Object Relational Mapper (ORM) method defined in the model
            likes.update()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(likes.read())

        @token_required()
        def delete(self):
            """
            Delete a like.
            """
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Find the likes to delete
            likes = Likes.query.get(data['id'])
            if likes is None:
                return {'message': 'Likes not found'}, 404
            # Delete the likes object using the Object Relational Mapper (ORM) method defined in the model
            likes.delete()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify({'message': 'Likes deleted'})

    class _BULK_CRUD(Resource):
        def post(self):
            """
            Handle bulk likes creation by sending POST requests to the single likes endpoint.
            """
            likes = request.get_json()

            if not isinstance(likes, list):
                return {'message': 'Expected a list of likes data'}, 400

            results = {'errors': [], 'success_count': 0, 'error_count': 0}

            with current_app.test_client() as client:
                for likes in likes:
                    # Simulate a POST request to the single likes creation endpoint
                    response = client.post('/api/likes', json=likes)

                    if response.status_code == 200:
                        results['success_count'] += 1
                    else:
                        results['errors'].append(response.get_json())
                        results['error_count'] += 1

            # Return the results of the bulk creation process
            return jsonify(results)
        
        def get(self):
            """
            Retrieve all likess.
            """
            # Find all the likes
            likes = Likes.query.all()
            # Prepare a JSON list of all the likess, using list comprehension
            json_ready = []
            for likes in likes:
                likes_data = likes.read()
                json_ready.append(likes_data)
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)

    class _BULK_FILTER(Resource):
        @token_required()
        def post(self):
            """
            Retrieve all likess under a group by group name.
            """
            # Obtain and validate the request data sent by the RESTful client API
            data = request.get_json()
            if data is None:
                return {'message': 'Group data not found'}, 400
            if 'group_name' not in data:
                return {'message': 'Group name not found'}, 400
            
            # Find the group by name
            group = Group.query.filter_by(_name=data['group_name']).first()
            if group is None:
                return {'message': 'Group not found'}, 404
            
            # Find all likess under the group
            likes = Likes.query.filter_by(_group_id=group.id).all()
            # Prepare a JSON list of all the likess, using list comprehension
            json_ready = [likes.read() for likes in likes]
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)

    class _FILTER(Resource):
        @token_required()
        def post(self):
            """
            Retrieve a single likes by group name and likes name.
            """
            # Obtain and validate the request data sent by the RESTful client API
            data = request.get_json()
            if data is None:
                return {'message': 'Group and Likes data not found'}, 400
            if 'group_name' not in data:
                return {'message': 'Group name not found'}, 400
            if 'likes_name' not in data:
                return {'message': 'Likes name not found'}, 400
            
            # Find the group by name
            group = Group.query.filter_by(_name=data['group_name']).first()
            if group is None:
                return {'message': 'Group not found'}, 404
            
            # Find the likes by group ID and likes name
            likes = Likes.query.filter_by(_group_id=group.id, _name=data['likes_name']).first()
            if likes is None:
                return {'message': 'Likes not found'}, 404
            
            # Convert Python object to JSON format 
            json_ready = likes.read()
            # Return a JSON restful response to the client
            return jsonify(json_ready)

    """
    Map the _CRUD, _BULK_CRUD, _BULK_FILTER, and _FILTER classes to the API endpoints for /likes, /likess, /likess/filter, and /likes/filter.
    - The API resource class inherits from flask_restful.Resource.
    - The _CRUD class defines the HTTP methods for the API.
    - The _BULK_CRUD class defines the bulk operations for the API.
    - The _BULK_FILTER class defines the endpoints for filtering likess by group name.
    - The _FILTER class defines the endpoints for filtering a specific likes by group name and likes name.
    """
    api.add_resource(_CRUD, '/likes')
    api.add_resource(_BULK_CRUD, '/likes')
    api.add_resource(_BULK_FILTER, '/likes/filter')
    api.add_resource(_FILTER, '/likes/filter')