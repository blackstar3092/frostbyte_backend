from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from model.quiz_result import QuizResult
from model.frostbyte import Frostbyte
from __init__ import app, db
from api.jwt_authorize import token_required
from datetime import datetime

# Blueprint for Quiz API
quiz_api = Blueprint('quiz_api', __name__, url_prefix='/api/quiz')
api = Api(quiz_api)

class QuizAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Submit quiz points, assign a national park, and store the results."""
            current_user = g.current_user
            data = request.get_json()

            # Validate input
            if not data or 'total_points' not in data:
                return {'message': 'Missing required field: total_points'}, 400

            # Ensure total_points is an integer
            try:
                total_points = int(data['total_points'])
            except (ValueError, TypeError):
                return {'message': 'total_points must be an integer'}, 400

            # Assign a national park based on the total points
            assigned_park = self.assign_national_park(total_points)

            # Create a new quiz result
            quiz_result = QuizResult(
                user_id=current_user.id,
                assigned_park=assigned_park
            )
            quiz_result.create()

            return jsonify({
                "message": "Quiz submitted successfully",
                "quiz_result": quiz_result.read(),
                "total_points": total_points,
                "assigned_park": assigned_park
            })

        def assign_national_park(self, total_points):
            """Assign a national park based on the total points."""
            if 70 <= total_points <= 130:
                return "Denali National Park"
            elif 140 <= total_points <= 170:
                return "Grand Canyon National Park"
            elif 180 <= total_points <= 220:
                return "Redwood National Park"
            elif 230 <= total_points <= 280:
                return "Buck Island Reef National Monument"
            else:
                return "Unknown Park"  # Fallback for unexpected scores

        @token_required()
        def get(self):
            """Retrieve a user's quiz results."""
            current_user = g.current_user
            quiz_results = QuizResult.query.filter_by(user_id=current_user.id).all()

            if not quiz_results:
                return {'message': 'No quiz results found for this user'}, 404

            return jsonify([result.read() for result in quiz_results])

        @token_required()
        def put(self):
            """Update a user's quiz results."""
            current_user = g.current_user
            data = request.get_json()

            # Validate input
            if not data or 'id' not in data:
                return {'message': 'Missing quiz result ID'}, 400

            # Find the quiz result
            quiz_result = QuizResult.query.filter_by(id=data['id'], user_id=current_user.id).first()
            if not quiz_result:
                return {'message': 'Quiz result not found'}, 404

            # Validate and update assigned_park if provided
            if 'assigned_park' in data:
                if not isinstance(data['assigned_park'], str):
                    return {'message': 'assigned_park must be a string'}, 400
                quiz_result.update(assigned_park=data['assigned_park'])

            return jsonify(quiz_result.read())

        @token_required()
        def delete(self):
            """Delete a user's quiz results."""
            current_user = g.current_user
            data = request.get_json()

            # Validate input
            if not data or 'id' not in data:
                return {'message': 'Missing quiz result ID'}, 400

            # Find the quiz result
            quiz_result = QuizResult.query.filter_by(id=data['id'], user_id=current_user.id).first()
            if not quiz_result:
                return {'message': 'Quiz result not found'}, 404

            # Delete the quiz result
            quiz_result.delete()
            return {'message': 'Quiz result deleted successfully'}, 200

# Map resources to endpoints
api.add_resource(QuizAPI._CRUD, '/')
