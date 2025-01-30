import jwt
import os
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import db, app
from api.jwt_authorize import token_required
import google.generativeai as genai
from dotenv import load_dotenv
from model.gemini import AIMessage

# Define Flask Blueprint and API
gemini_api = Blueprint('gemini_api', __name__, url_prefix='/api')
api = Api(gemini_api)

# Load environment variables
load_dotenv()

# Configure the Google Generative AI client
genai.configure(api_key=os.getenv("API_KEY"))

# Define model configuration
generation_config = {
    "temperature": 1.0,
    "top_p": 1,
    "top_k": 50,
    "max_output_tokens": 1000,
    "response_mime_type": "text/plain",
}
# Define system instruction for the chatbot
system_instruction = (
    "You are an AI expert specializing in camping advice. You have the knowledge of park rangers and survival specialists. "
    "You are knowledgeable about camping in national parks, especially in tundras, deserts, valleys, mountains, and forests. "
    "You provide expert guidance on the best camping gear and brands, strategies for sourcing food in the wild, essential survival skills, and practical tips and tricks for a safe and enjoyable outdoor experience. "
    "Maintain a friendly and supportive tone suitable for campers of all levels. "
    "Inform the users about the best camping brands and cheaper alternatives. "
    "Your responses are short, concise, and easy to understand. "
    "You DO NOT give responses longer than 4 sentences."
)
# Create the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=system_instruction,
)

class Chatbot(Resource):
    MAX_HISTORY = 50  # Maximum history length

    def __init__(self):
        self.history = []
        self.chat_session = model.start_chat(history=self.history)  # Persistent session

    def generate_ai_response(self, user_input):
        """Generates a response from the Google Generative AI model."""
        try:
            response = self.chat_session.send_message(user_input)
            return response.text.rstrip("\n")
        except Exception as e:
            print(f"Error generating AI response: {str(e)}")
            return "Sorry, I couldn't process that."

    def update_history(self, role: str, message: str):
        """Update the conversation history and save messages to the database."""
        if len(self.history) >= self.MAX_HISTORY:
            self.history.pop(0)  # Maintain a maximum history length
        self.history.append({"role": role, "parts": [message]})

        ai_message = AIMessage(
            message=message,
            author=role,
            category="response" if role == "assistant" else "user"
        )
        ai_message.create()
        return ai_message.id  # Return the ID of the created message

    def post(self):
        """Handles POST requests to send a message and get a response."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON"}), 400

            user_input = data.get("user_input")
            if not user_input:
                return jsonify({"error": "User input is required"}), 400

            # Save the user's message to the database and get its ID
            user_message = AIMessage(message=user_input, author="user", category="user_message")
            db.session.add(user_message)
            db.session.commit()
            user_message_id = user_message.id  # Get the auto-generated ID

            # Generate AI response using Google Generative AI
            response_text = self.generate_ai_response(user_input)

            # Save the AI's response to the database and get its ID
            ai_message = AIMessage(message=response_text, author="assistant", category="ai_response")
            db.session.add(ai_message)
            db.session.commit()
            ai_message_id = ai_message.id  # Get the auto-generated ID

            return jsonify({
                "user_message_id": user_message_id,  # ID of the user's message
                "ai_message_id": ai_message_id,  # ID of the AI's response
                "user_input": user_input,
                "model_response": response_text
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def put(self):
        """Handles PUT requests to update an existing message by ID."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON"}), 400

            message_id = data.get("id")
            new_message = data.get("user_input")

            if not message_id or not new_message:
                return jsonify({"error": "Message ID and new message content are required"}), 400

            # Find the message by ID
            message = AIMessage.query.get(message_id)
            if not message:
                return jsonify({"error": "Message not found"}), 404

            # Update the message content
            message.message = new_message
            db.session.commit()

            return jsonify({"message": "Message updated successfully"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def delete(self):
        """Handles DELETE requests to delete a message by ID."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON"}), 400

            message_id = data.get("id")
            if not message_id:
                return jsonify({"error": "Message ID is required"}), 400

            # Find the message by ID
            message = AIMessage.query.get(message_id)
            if not message:
                return jsonify({"error": "Message not found"}), 404

            # Delete the message
            db.session.delete(message)
            db.session.commit()

            return '', 204  # Return a 204 No Content to indicate successful deletion
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Add Chatbot resource to the API
api.add_resource(Chatbot, '/chatbot')