from flask import Flask, request, jsonify, Blueprint
from flask_restful import Api, Resource
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Blueprint for API routes
points_api = Blueprint('points_api', __name__, url_prefix='/api')

# Attach Flask-RESTful API to the Blueprint
api = Api(points_api)

# In-memory storage for quiz data (to be replaced with a database in production)
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
        Endpoint to submit quiz points.
        """
        def post(self):
            # Parse JSON data from request
            data = request.get_json()

            # Validate data presence and required fields
            if not data:
                return jsonify({"message": "Request body cannot be empty."}), 400
            if 'user_id' not in data or 'points' not in data:
                return jsonify({"message": "'user_id' and 'points' are required fields."}), 400

            # Extract user_id and points
            user_id = data.get('user_id')
            points = data.get('points')

            # Validate data types
            if not isinstance(user_id, int) or not isinstance(points, int):
                return jsonify({"message": "'user_id' and 'points' must be integers."}), 400

            # Store data and assign park
            user_points[user_id] = {
                "points": points,
                "park": assign_park(points),
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            return jsonify({
                "message": "Points successfully submitted.",
                "user_id": user_id,
                "points": points,
                "park": user_points[user_id]["park"]
            }), 201

    class GetPoints(Resource):
        """
        Endpoint to retrieve a user's points and park assignment.
        """
        def get(self, user_id):
            try:
                user_id = int(user_id)  # Validate user_id as integer
            except ValueError:
                return jsonify({"message": "'user_id' must be an integer."}), 400

            if user_id not in user_points:
                return jsonify({"message": f"No data found for user_id {user_id}."}), 404

            user_data = user_points[user_id]
            return jsonify({
                "user_id": user_id,
                "points": user_data["points"],
                "park": user_data["park"],
                "timestamp": user_data["timestamp"]
            })

    class GetAllPoints(Resource):
        """
        Endpoint to retrieve all users' points and park assignments.
        """
        def get(self):
            if not user_points:
                return jsonify({"message": "No data available."}), 404

            return jsonify(user_points)

    class DeletePoints(Resource):
        """
        Endpoint to delete a user's quiz data.
        """
        def delete(self, user_id):
            try:
                user_id = int(user_id)  # Validate user_id as integer
            except ValueError:
                return jsonify({"message": "'user_id' must be an integer."}), 400

            if user_id not in user_points:
                return jsonify({"message": f"No data found for user_id {user_id}."}), 404

            del user_points[user_id]
            return jsonify({"message": f"Data for user_id {user_id} successfully deleted."}), 200

# Add resources to API
api.add_resource(PointsAPI.SubmitPoints, '/points/submit')
api.add_resource(PointsAPI.GetPoints, '/points/<user_id>')
api.add_resource(PointsAPI.GetAllPoints, '/points/all')
api.add_resource(PointsAPI.DeletePoints, '/points/<user_id>')

# Register the Blueprint with the app
app.register_blueprint(points_api)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, host="0.0.0.0", port=5000)
