import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.channel import Channel
from model.group import Group
from model.user import User
import google.generativeai as genai

# create a blueprint for gemini API
gemini_api = Blueprint('gemini_api', __name__, url_prefix='/api/id')
# Create an Api object and associate it with the Blueprint
api = Api(gemini_api)

#gemini integration
genai.configure(api_key="AIzaSyAkwGL0VcgW-zJb2XG0lDvKtW7PvhhB5S8")
model = genai.GenerativeModel('gemini-pro')
@app.route('/api/ai/help', methods=['POST'])
def ai_homework_help():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "No question provided."}), 400
    try:
        response = model.generate_content(f"You are an AI expert specializing in family-friendly camping advice. Your responses are short, concise, and easy to understand. You are knowledgeable about camping in national parks, especially in tundras, deserts, valleys, mountains, and forests. You provide expert guidance on the best camping gear and brands, strategies for sourcing food in the wild, essential survival skills, and practical tips and tricks for a safe and enjoyable outdoor experience. Maintain a friendly and supportive tone suitable for families and beginners\nHere is your prompt: {question}")
        return jsonify({"response": response.text}), 200
    except Exception as e:
        print("error!")
        print(e)
        return jsonify({"error": str(e)}), 500
    
class ChannelAPI:
    """
    Define the API CRUD endpoints for the Channel model.
    There are four operations that correspond to common HTTP methods:
    - post: create a new channel
    - get: read channels
    - put: update a channel
    - delete: delete a channel
    """
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create a new channel.
            """
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            
            # Validate the presence of required keys
            if not data:
                return {'message': 'No input data provided'}, 400
            if 'name' not in data:
                return {'message': 'Channel name is required'}, 400
            if 'group_id' not in data:
                return {'message': 'Group ID is required'}, 400
            if 'attributes' not in data:
                data['attributes'] = {}
                
            # Create a new channel object using the data from the request
            channel = Channel(data['name'], data['group_id'], data.get('attributes', {}))
            # Save the channel object using the Object Relational Mapper (ORM) method defined in the model
            channel.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(channel.read())

        @token_required()
        def get(self):
            """
            Retrieve a single channel by ID.
            """
            # Obtain and validate the request data sent by the RESTful client API
            data = request.get_json()
            if data is None:
                return {'message': 'Channel data not found'}, 400
            if 'id' not in data:
                return {'message': 'Channel ID not found'}, 400
            # Find the channel to read
            channel = Channel.query.get(data['id'])
            if channel is None:
                return {'message': 'Channel not found'}, 404
            # Convert Python object to JSON format 
            json_ready = channel.read()
            # Return a JSON restful response to the client
            return jsonify(json_ready)

        @token_required()
        def put(self):
            """
            Update a channel.
            """
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Find the channel to update
            channel = Channel.query.get(data['id'])
            if channel is None:
                return {'message': 'Channel not found'}, 404
            # Update the channel object using the data from the request
            channel._name = data['name']
            channel._group_id = data['group_id']
            channel._attributes = data.get('attributes', {})
            # Save the channel object using the Object Relational Mapper (ORM) method defined in the model
            channel.update()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(channel.read())

        @token_required()
        def delete(self):
            """
            Delete a channel.
            """
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Find the channel to delete
            channel = Channel.query.get(data['id'])
            if channel is None:
                return {'message': 'Channel not found'}, 404
            # Delete the channel object using the Object Relational Mapper (ORM) method defined in the model
            channel.delete()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify({'message': 'Channel deleted'})

    class _BULK_CRUD(Resource):
        def post(self):
            """
            Handle bulk channel creation by sending POST requests to the single channel endpoint.
            """
            channels = request.get_json()

            if not isinstance(channels, list):
                return {'message': 'Expected a list of channel data'}, 400

            results = {'errors': [], 'success_count': 0, 'error_count': 0}

            with current_app.test_client() as client:
                for channel in channels:
                    # Simulate a POST request to the single channel creation endpoint
                    response = client.post('/api/gemini', json=channel)
                    if response.status_code == 200:
                        results['success_count'] += 1
                    else:
                        results['errors'].append(response.get_json())
                        results['error_count'] += 1

            # Return the results of the bulk creation process
            return jsonify(results)
        
        def get(self):
            """
            Retrieve all channels.
            """
            # Find all the channels
            channels = Channel.query.all()
            # Prepare a JSON list of all the channels, using list comprehension
            json_ready = []
            for channel in channels:
                channel_data = channel.read()
                json_ready.append(channel_data)
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)
    class _BULK_FILTER(Resource):
        @token_required()
        def post(self):
            """
            Retrieve all channels under a group by group name.
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
            
            # Find all channels under the group
            channels = Channel.query.filter_by(_group_id=group.id).all()
            # Prepare a JSON list of all the channels, using list comprehension
            json_ready = [channel.read() for channel in channels]
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)

    class _FILTER(Resource):
        @token_required()
        def post(self):
            """
            Retrieve a single channel by group name and channel name.
            """
            # Obtain and validate the request data sent by the RESTful client API
            data = request.get_json()
            if data is None:
                return {'message': 'Group and Channel data not found'}, 400
            if 'group_name' not in data:
                return {'message': 'Group name not found'}, 400
            if 'channel_name' not in data:
                return {'message': 'Channel name not found'}, 400
            
            # Find the group by name
            group = Group.query.filter_by(_name=data['group_name']).first()
            if group is None:
                return {'message': 'Group not found'}, 404
            
            # Find the channel by group ID and channel name
            channel = Channel.query.filter_by(_group_id=group.id, _name=data['channel_name']).first()
            if channel is None:
                return {'message': 'Channel not found'}, 404
            
            # Convert Python object to JSON format 
            json_ready = channel.read()
            # Return a JSON restful response to the client
            return jsonify(json_ready)


    """
    Map the _CRUD, _BULK_CRUD, _BULK_FILTER, and _FILTER classes to the API endpoints for /channel, /channels, /channels/filter, and /channel/filter.
    - The API resource class inherits from flask_restful.Resource.
    - The _CRUD class defines the HTTP methods for the API.
    - The _BULK_CRUD class defines the bulk operations for the API.
    - The _BULK_FILTER class defines the endpoints for filtering channels by group name.
    - The _FILTER class defines the endpoints for filtering a specific channel by group name and channel name.
    """
    api.add_resource(_CRUD, '/gemini')
    api.add_resource(_BULK_CRUD, '/gemini_bulk')
    api.add_resource(_BULK_FILTER, '/gemini_bulk/filter')
    api.add_resource(_FILTER, '/gemini/filter')