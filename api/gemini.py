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
gemini_api = Blueprint('gemini_api', __name__, url_prefix='/api')
# Create an Api object and associate it with the Blueprint
api = Api(gemini_api)
      
# Configure the API key (ensure the API_KEY environment variable is set)
genai.configure(api_key="AIzaSyAkwGL0VcgW-zJb2XG0lDvKtW7PvhhB5S8")
# Create the model with the configuration
generation_config = {
    "temperature": 1.0,
    "top_p": 1,
    "top_k": 50,
    "max_output_tokens": 10000,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "You are an AI expert specializing in family-friendly camping advice. You have the knowledge of park rangers and survival specialists."
        "You are knowledgeable about camping in national parks, especially in tundras, deserts, valleys, mountains, and forests." 
        "You provide expert guidance on the best camping gear and brands, strategies for sourcing food in the wild, essential survival skills, and practical tips and tricks for a safe and enjoyable outdoor experience."
        "Maintain a friendly and supportive tone suitable for families and beginners"
        "Your responses are short, concise, and easy to understand."
        "You use diction that high school students can understand."
        "You DO NOT give responses longer than 4 sentences."
    ),
)
class _Chatbot(Resource):
    def __init__(self):
        self.history = []
    def post(self):
        from flask import request, jsonify
        data = request.get_json()
        user_input = data.get("user_input")
        if not user_input:
            return jsonify({"error": "User input is required"}), 400
        try:
            # Start the chat session
            chat_session = model.start_chat(history=self.history)
            # Get the response from the model
            response = chat_session.send_message(user_input)
            # Extract the model response and remove trailing newline characters
            model_response = response.text.rstrip("\n")
            # Update the conversation history
            self.history.append({"role": "user", "parts": [user_input]})
            self.history.append({"role": "assistant", "parts": [model_response]})
            return jsonify({
                "user_input": user_input,
                "model_response": model_response,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
# Add the resource to the API
api.add_resource(_Chatbot, '/gemini')
chatbot_api_instance = _Chatbot()