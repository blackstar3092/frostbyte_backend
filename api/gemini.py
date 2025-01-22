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

# Initialize the Generative AI client
genai.api_key = os.getenv("API_KEY")


class Chatbot(Resource):

    def __init__(self):
        self.history = []

    def generate_ai_response(self, user_input):
        """Generates a response from the Google Generative AI model."""
        try:
            response = genai.chat(
                messages=[{"role": "user", "content": user_input}],
                temperature=0.7,
                max_tokens=100
            )
            return response["messages"][0]["content"]
        except Exception as e:
            print(f"Error generating AI response: {str(e)}")
            return "Sorry, I couldn't process that."

    def post(self):
        """Handles POST requests to send a message and get a response."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON"}), 400

            user_input = data.get("user_input")

            if not user_input:
                return jsonify({"error": "User input is required"}), 400

            # Generate AI response using Google Generative AI
            response_text = self.generate_ai_response(user_input)

            # Save user input and AI response to history and database
            self.update_history("user", user_input)
            self.update_history("assistant", response_text)

            return jsonify({
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

            # Return a 204 No Content to indicate successful deletion
            return '', 204
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def update_history(self, role: str, message: str):
        """Update the conversation history and save messages to the database."""
        ai_message = AIMessage(
            message=message,
            author=role,
            category="response" if role == "assistant" else "user"
        )
        ai_message.create()


# Add Chatbot resource to the API
api.add_resource(Chatbot, '/chatbot')
