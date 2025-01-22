from flask import Flask, Blueprint, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from datetime import datetime
from api.jwt_authorize import token_required

# Initialize Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'  # Example SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Blueprint for the Quiz API
points_api = Blueprint('points_api', __name__, url_prefix='/api')
api = Api(points_api)

# User model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    quiz_scores = db.relationship('QuizScore', back_populates='user')

# QuizScore model
class QuizScore(db.Model):
    __tablename__ = 'quiz_scores'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    park = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates='quiz_scores')

    def create(self):
        db.session.add(self)
        db.session.commit()

    def read(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "points": self.points,
            "park": self.park,
            "timestamp": self.timestamp.isoformat()
        }

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# Utility function to assign park

def assign_park(points):
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

# API Resources
class PointsAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            current_user = g.current_user
            data = request.get_json()

            if not data or 'points' not in data:
                return {'message': 'Points are required'}, 400

            points = data['points']
            park = assign_park(points)

            existing_score = QuizScore.query.filter_by(user_id=current_user.id).first()
            if existing_score:
                existing_score.points = points
                existing_score.park = park
                existing_score.update()
                return jsonify(existing_score.read())

            new_score = QuizScore(user_id=current_user.id, points=points, park=park)
            new_score.create()
            return jsonify(new_score.read())

        @token_required()
        def get(self):
            current_user = g.current_user
            score = QuizScore.query.filter_by(user_id=current_user.id).first()
            if not score:
                return {'message': 'Quiz result not found'}, 404

            return jsonify(score.read())

        @token_required()
        def delete(self):
            current_user = g.current_user
            score = QuizScore.query.filter_by(user_id=current_user.id).first()
            if not score:
                return {'message': 'Quiz result not found'}, 404

            score.delete()
            return {'message': 'Quiz result deleted successfully.'}, 200

    class _ALL_SCORES(Resource):
        @token_required()
        def get(self):
            scores = QuizScore.query.all()
            results = [score.read() for score in scores]
            return jsonify(results)

# Register API endpoints
api.add_resource(PointsAPI._CRUD, '/quiz')
api.add_resource(PointsAPI._ALL_SCORES, '/quizzes')

# Register Blueprint
app.register_blueprint(points_api)

if __name__ == '__main__':
    # Initialize the database
    with app.app_context():
        db.create_all()

    app.run(debug=True, host="0.0.0.0", port=8887)
