import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
import google.generativeai as genai

# create a blueprint for gemini API
gemini_api = Blueprint('gemini_api', __name__, url_prefix='/api')
# Create an Api object and associate it with the Blueprint
api = Api(gemini_api)
      
# Configure the API key (ensure the API_KEY environment variable is set)
genai.configure(api_key="AIzaSyBOwK_K_HCD4lKh3ASmfuNhag_Vi0GwA_c")
# Create the model with the configuration
generation_config = {
    #controls the randomness of the model
    "temperature": 1.0,
    "top_p": 1,
    "top_k": 50,
    "max_output_tokens": 1000,
    "response_mime_type": "text/plain",
}
# Create the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # Define the system instructions
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
# Define the chatbot resource
class Chatbot(Resource):

    # Initialize the chatbot
    def __init__(self):
        # Initialize the conversation history
        self.history: list[dict[str, list[str]]] = []
        # Start the chat session
        self.chat_session = model.start_chat(history=self.history)  # Persistent session

    # Define the maximum history length
    MAX_HISTORY = 50  
    # Update the conversation history
    def update_history(self, role: str, message: str):
        # check if the history is full
        if len(self.history) >= self.MAX_HISTORY:
            # Remove the oldest entry
            self.history.pop(0)  
        #updates the conversation history by adding another entry
        self.history.append({"role": role, "parts": [message]})

    # Handle the POST request
    def post(self):
        try:
            # Check if the user input is provided
            data = request.get_json()
            user_input = data.get("user_input")
            if not user_input:
                # Return an error if the user input is missing
                return jsonify({"error": "User input is required"}), 400

            # Get the response from the model
            response = self.chat_session.send_message(user_input)
            model_response = response.text.rstrip("\n")

            # Update the conversation history
            self.update_history("user", user_input)
            self.update_history("assistant", model_response)

            # Return the response
            return jsonify({
                # 
                "user_input": user_input,
                # 
                "model_response": model_response,
            })
        # Handle exceptions
        except Exception as e:
            import traceback
            print(f"Error occurred: {str(e)}")
            traceback.print_exc()  # Log the full traceback
            return jsonify({"error": str(e)}), 500
        
# Add the resource to the API
api.add_resource(Chatbot, '/gemini')
chatbot_api_instance = Chatbot()