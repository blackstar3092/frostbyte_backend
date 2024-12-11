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
    

class GeminiAPI:
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
            if 'content' not in data:
                data['content'] = {}

            # Create a new post object using the data from the request
            post = Post(data['title'], data['comment'], current_user.id, data['channel_id'], data['content'])
            # Save the post object using the Object Relational Mapper (ORM) method defined in the model
            post.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(post.read())

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
            post = Post.query.get(data['id'])
            if post is None:
                return {'message': 'Post not found'}, 404
            # Convert Python object to JSON format 
            json_ready = post.read()
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
            post = Post.query.get(data['id'])
            if post is None:
                return {'message': 'Post not found'}, 404
            # Update the post
            post._title = data['title']
            post._content = data['content']
            post._channel_id = data['channel_id']
            # Save the post
            post.update()
            # Return response
            return jsonify(post.read())

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
            post = Post.query.get(data['id'])
            if post is None:
                return {'message': 'Post not found'}, 404
            # Delete the post using the ORM method defined in the model
            post.delete()
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
            posts = Post.query.filter(Post._user_id == current_user.id).all()
            # Prepare a JSON list of all the posts, using list comprehension
            json_ready = [post.read() for post in posts]
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)

    class _BULK_CRUD(Resource):
        def post(self):
            """
            Handle bulk post creation by sending POST requests to the single post endpoint.
            """
            posts = request.get_json()

            if not isinstance(posts, list):
                return {'message': 'Expected a list of post data'}, 400

            results = {'errors': [], 'success_count': 0, 'error_count': 0}

            with current_app.test_client() as client:
                for post in posts:
                    # Simulate a POST request to the single post creation endpoint
                    response = client.post('/api/post', json=post)

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
            posts = Post.query.all()
            # Prepare a JSON list of all the posts, using list comprehension
            json_ready = []
            for post in posts:
                post_data = post.read()
                json_ready.append(post_data)
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)

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
            posts = Post.query.filter_by(_channel_id=data['channel_id']).all()
            # Prepare a JSON list of all the posts, using list comprehension
            json_ready = [post.read() for post in posts]
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
    api.add_resource(_CRUD, '/post')
    api.add_resource(_USER, '/post/user')
    api.add_resource(_BULK_CRUD, '/posts')
    api.add_resource(_FILTER, '/posts/filter')