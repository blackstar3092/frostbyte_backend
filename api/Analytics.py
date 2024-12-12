import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.analytics import Analytics
from model.user import User
from model.section import Section

"""
This Blueprint object is used to define APIs for the Analytics model.
- Blueprint is used to modularize application files.
- This Blueprint is registered to the Flask app in main.py.
"""
analytics_api = Blueprint('analytics_api', __name__, url_prefix='/api')

"""
The Api object is connected to the Blueprint object to define the API endpoints.
- The API object is used to add resources to the API.
- The objects added are mapped to code that contains the actions for the API.
- For more information, refer to the API docs: https://flask-restful.readthedocs.io/en/latest/api.html
"""
api = Api(analytics_api)

class AnalyticsAPI:
    """
    Define the API CRUD endpoints for the Analytics model.
    There are four operations that correspond to common HTTP methods:
    - post: create a new analytics
    - get: read analytics
    - put: update a analytics
    - delete: delete a analytics
    """
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create a new analytics.
            """
            # Obtain the current user from the token required setting in the global context
            current_user = g.current_user
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Create a new analytics object using the data from the request
            analytics = Analytics(data['park_id'], data['user_id'], data['stars'], data['review_text'], data.get('moderator_id', current_user.id))
            # Save the analytics object using the Object Relational Mapper (ORM) method defined in the model
            analytics.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(analytics.read())

        @token_required()
        def get(self):
            """
            Retrieve a single analytics by ID.
            """
            # Obtain and validate the request data sent by the RESTful client API
            data = request.get_json()
            if data is None:
                return {'message': 'Analytics data not found'}, 400
            if 'id' not in data:
                return {'message': 'Analytics ID not found'}, 400
            # Find the analytics to read
            analytics = Analytics.query.get(data['id'])
            if analytics is None:
                return {'message': 'Analytics not found'}, 404
            # Convert Python object to JSON format 
            json_ready = analytics.read()
            # Return a JSON restful response to the client
            return jsonify(json_ready)

        @token_required()
        def put(self):
            """
            Update a analytics.
            """
            # Obtain the current user from the token required setting in the global context
            current_user = g.current_user
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Find the analytics to update
            analytics = Analytics.query.get(data['id'])
            if analytics is None:
                return {'message': 'Analytics not found'}, 404
            # Update the analytics object using the data from the request
            analytics._park_id = data['park_id']
            analytics._user_id = data['user_id']
            analytics._stars = data['stars']
            analytics._review_text = data['review_text']
            analytics._moderator_id = data.get('moderator_id', current_user.id)
            # Save the analytics object using the Object Relational Mapper (ORM) method defined in the model
            analytics.update()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(analytics.read())

        @token_required()
        def delete(self):
            """
            Delete a analytics.
            """
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Find the analytics to delete
            analytics = Analytics.query.get(data['id'])
            if analytics is None:
                return {'message': 'Analytics not found'}, 404
            # Delete the analytics object using the Object Relational Mapper (ORM) method defined in the model
            analytics.delete()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify({'message': 'Analytics deleted'})

    class _BULK_CRUD(Resource):
        def post(self):
            """
            Handle bulk analytics creation by sending POST requests to the single analytics endpoint.
            """
            analytics = request.get_json()

            if not isinstance(analytics, list):
                return {'message': 'Expected a list of analytics data'}, 400

            results = {'errors': [], 'success_count': 0, 'error_count': 0}

            with current_app.test_client() as client:
                for analytics in analytics:
                    # Simulate a POST request to the single analytics creation endpoint
                    response = client.post('/api/analytics', json=analytics)

                    if response.status_code == 200:
                        results['success_count'] += 1
                    else:
                        results['errors'].append(response.get_json())
                        results['error_count'] += 1

            # Return the results of the bulk creation process
            return jsonify(results)
        
        def get(self):
            """
            Retrieve all analytics.
            """
            # Find all the analytics
            analytics = Analytics.query.all()
            # Prepare a JSON list of all the analytics, using list comprehension
            json_ready = []
            for analytics in analytics:
                analytics_data = analytics.read()
                json_ready.append(analytics_data)
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)

    class _MODERATOR(Resource):
        @token_required()
        def post(self):
            """
            Add a moderator to a analytics.
            """
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Find the analytics to update
            analytics = Analytics.query.get(data['analytics_id'])
            if analytics is None:
                return {'message': 'Analytics not found'}, 404
            # Find the user to add as a moderator
            user = User.query.get(data['user_id'])
            if user is None:
                return {'message': 'User not found'}, 404
            # Add the user as a moderator
            analytics.moderators.append(user)
            # Save the analytics object using the Object Relational Mapper (ORM) method defined in the model
            analytics.update()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(analytics.read())

        @token_required()
        def delete(self):
            """
            Remove a moderator from a analytics.
            """
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Find the analytics to update
            analytics = Analytics.query.get(data['analytics_id'])
            if analytics is None:
                return {'message': 'Analytics not found'}, 404
            # Find the user to remove as a moderator
            user = User.query.get(data['user_id'])
            if user is None:
                return {'message': 'User not found'}, 404
            # Remove the user as a moderator
            analytics.moderators.remove(user)
            # Save the analytics object using the Object Relational Mapper (ORM) method defined in the model
            analytics.update()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(analytics.read())

    class _BULK_FILTER(Resource):
        @token_required()
        def post(self):
            """
            Retrieve all analytics under a section by section park_id.
            """
            # Obtain and validate the request data sent by the RESTful client API
            data = request.get_json()
            if data is None:
                return {'message': 'Section data not found'}, 400
            if 'section_name' not in data:
                return {'message': 'Section name not found'}, 400
            
            # Find the section by name
            section = Section.query.filter_by(_name=data['section_name']).first()
            if section is None:
                return {'message': 'Section not found'}, 404
            
            # Find all analytics under the section
            analytics = Analytics.query.filter_by(_user_id=section.id).all()
            # Prepare a JSON list of all the analytics, using list comprehension
            json_ready = [analytics.read() for analytics in analytics]
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)

    class _FILTER(Resource):
        @token_required()
        def post(self):
            """
            Retrieve a single analytics by analytics name.
            """
            # Obtain and validate the request data sent by the RESTful client API
            data = request.get_json()
            if data is None:
                return {'message': 'Analytics data not found'}, 400
            if 'analytics_name' not in data:
                return {'message': 'Analytics name not found'}, 400
            
            # Find the analytics by name
            analytics = Analytics.query.filter_by(_name=data['analytics_name']).first()
            if analytics is None:
                return {'message': 'Analytics not found'}, 404
            
            # Convert Python object to JSON format 
            json_ready = analytics.read()
            # Return a JSON restful response to the client
            return jsonify(json_ready)

    """
    Map the _CRUD, _BULK_CRUD, _BULK_FILTER, and _FILTER classes to the API endpoints for /analytics, /analytics, /analytics/filter, and /analytics/filter.
    - The API resource class inherits from flask_restful.Resource.
    - The _CRUD class defines the HTTP methods for the API.
    - The _BULK_CRUD class defines the bulk operations for the API.
    - The _BULK_FILTER class defines the endpoints for filtering analytics by section name.
    - The _FILTER class defines the endpoints for filtering a specific analytics by analytics name.
    """
    api.add_resource(_CRUD, '/analytics')
    api.add_resource(_BULK_CRUD, '/analytics')
    api.add_resource(_BULK_FILTER, '/analytics/filter')
    api.add_resource(_FILTER, '/analytics/filter')