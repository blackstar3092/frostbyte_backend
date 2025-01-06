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
    "max_output_tokens": 5000,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "You are an AI expert specializing in camping advice. You have the knowledge of park rangers and survival specialists."
        "You are knowledgeable about camping in national parks, especially in tundras, deserts, valleys, mountains, and forests." 
        "You provide expert guidance on the best camping gear and brands, strategies for sourcing food in the wild, essential survival skills, and practical tips and tricks for a safe and enjoyable outdoor experience."
        "Maintain a friendly and supportive tone suitable for campers of all levels."
        "inform the users about the best camping brands and cheaper alternatives."
        "Your responses are short, concise, and easy to understand."
        "You use diction that high school students can understand."
        "You DO NOT give responses longer than 4 sentences."
    ),
)
class Chatbot(Resource):
    MAX_HISTORY = 50  # Limit conversation history

    def __init__(self):
        self.history: list[dict[str, list[str]]] = []
        self.chat_session = model.start_chat(history=self.history)  # Persistent session

    def update_history(self, role: str, message: str):
        if len(self.history) >= self.MAX_HISTORY:
            self.history.pop(0)  # Remove the oldest entry
        self.history.append({"role": role, "parts": [message]})

    def post(self):
        try:
            data = request.get_json()
            user_input = data.get("user_input")
            if not user_input:
                return jsonify({"error": "User input is required"}), 400

            # Get the response from the model
            response = self.chat_session.send_message(user_input)
            model_response = response.text.rstrip("\n")

            # Update the conversation history
            self.update_history("user", user_input)
            self.update_history("assistant", model_response)

            return jsonify({
                "user_input": user_input,
                "model_response": model_response,
            })
        except Exception as e:
            import traceback
            print(f"Error occurred: {str(e)}")
            traceback.print_exc()  # Log the full traceback
            return jsonify({"error": str(e)}), 500
        
# Add the resource to the API
api.add_resource(Chatbot, '/gemini')
chatbot_api_instance = Chatbot()