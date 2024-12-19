from flask import Flask, request, jsonify, Blueprint
from flask_restful import Api, Resource
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Blueprint for API routes, ensuring modularity
points_api = Blueprint('points_api', __name__, url_prefix='/api')

# Attach Flask-RESTful API to the Blueprint
api = Api(points_api)

# In-memory storage for user points and park assignments
# Note: In production, replace this with a database like PostgreSQL or MongoDB
user_points = {}

def assign_park(points):
    """
    Assign a national park based on the user's total quiz points.
    
    Args:
        points (int): Total quiz points submitted by the user.

    Returns:
        str: The name of the assigned national park.
    """
    if 70 <= points <= 130:
        return "Denali National Park"
    elif 140 <= points <= 170:
        return "Grand Canyon National Park"
    elif 180 <= points <= 220:
        return "Redwood National Park"
    elif 230 <= points <= 280:
        return "Buck Island Reef National Monument"
    else:
        return "No matching park found"

class PointsAPI:
    """
    Flask-RESTful API class for managing quiz points and park assignments.
    """

    class SubmitPoints(Resource):
        """
        Endpoint to handle point submissions.
        - Allows users to submit their quiz points along with their user ID.
        - Stores the data in in-memory storage.
        - Assigns a park based on the quiz points.
        """
        def post(self):
            # Parse incoming JSON data
            data = request.get_json()

            # Validate presence of required fields
            if not data:
                return jsonify({"message": "Request body cannot be empty."}), 400
            if 'user_id' not in data or 'points' not in data:
                return jsonify({"message": "'user_id' and 'points' are required fields."}), 400

            # Extract fields from the request
            user_id = data['user_id']
            points = data['points']

            # Validate field types
            if not isinstance(user_id, int):
                return jsonify({"message": "'user_id' must be an integer."}), 400
            if not isinstance(points, int):
                return jsonify({"message": "'points' must be an integer."}), 400

            # Store the user's points and assign a park
            user_points[user_id] = {
                "points": points,
                "park": assign_park(points),
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            # Respond with the stored data
            return jsonify({
                "message": "Points successfully submitted.",
                "user_id": user_id,
                "points": points,
                "park": user_points[user_id]["park"]
            }), 201

    class GetPoints(Resource):
        """
        Endpoint to retrieve stored quiz points and park assignment for a specific user.
        """
        def get(self, user_id):
            try:
                # Ensure user_id is an integer
                user_id = int(user_id)
            except ValueError:
                return jsonify({"message": "'user_id' must be an integer."}), 400

            # Check if the user exists in storage
            if user_id not in user_points:
                return jsonify({"message": f"No data found for user_id {user_id}."}), 404

            # Retrieve and return the user's data
            user_data = user_points[user_id]
            return jsonify({
                "user_id": user_id,
                "points": user_data["points"],
                "park": user_data["park"],
                "timestamp": user_data["timestamp"]
            })

    class GetAllPoints(Resource):
        """
        Endpoint to retrieve all users' stored quiz points and park assignments.
        """
        def get(self):
            # Check if storage is empty
            if not user_points:
                return jsonify({"message": "No data available."}), 404

            # Return all stored data
            return jsonify(user_points)

    class DeletePoints(Resource):
        """
        Endpoint to delete quiz points and park assignment for a specific user.
        """
        def delete(self, user_id):
            try:
                # Ensure user_id is an integer
                user_id = int(user_id)
            except ValueError:
                return jsonify({"message": "'user_id' must be an integer."}), 400

            # Check if the user exists in storage
            if user_id not in user_points:
                return jsonify({"message": f"No data found for user_id {user_id}."}), 404

            # Delete the user's data
            del user_points[user_id]
            return jsonify({"message": f"Data for user_id {user_id} successfully deleted."}), 200

# Add API resources to Flask-RESTful API
api.add_resource(PointsAPI.SubmitPoints, '/points/submit')
api.add_resource(PointsAPI.GetPoints, '/points/<user_id>')
api.add_resource(PointsAPI.GetAllPoints, '/points/all')
api.add_resource(PointsAPI.DeletePoints, '/points/<user_id>')

# Register the Blueprint with the Flask app
app.register_blueprint(points_api)

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
