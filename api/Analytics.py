import jwt
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from api.Analytics import Analytics
from model.user import User
from model.storereview import storereview
from __init__ import db
from flask import Blueprint
from flask_restful import Api, Resource


analytics_blueprint = Blueprint('analytics', __name__, url_prefix='/api')
api = Api(analytics_blueprint)


app.register_blueprint(analytics_blueprint)



class AnalyticsAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create a new analytics entry with validation.
            """
            try:
                current_user = g.current_user  # Provided by token_required
                data = request.get_json()

                
                required_fields = ['park_id', 'user_id', 'stars', 'review_text']
                if not all(field in data for field in required_fields):
                    return {'message': 'Missing required fields'}, 400

                if not isinstance(data['stars'], int) or not (1 <= data['stars'] <= 5):
                    return {'message': 'Stars must be an integer between 1 and 5'}, 400

                if not isinstance(data['review_text'], str) or not data['review_text'].strip():
                    return {'message': 'review_text must be a non-empty string'}, 400

                # Create the analytics entry
                analytics = Analytics(
                    park_id=data['park_id'],
                    user_id=data['user_id'],
                    stars=data['stars'],
                    review_text=data['review_text'],
                    moderator_id=current_user.id
                )
                analytics.create()
                return jsonify(analytics.read()), 201
            except Exception as e:
                return {'message': f'An error occurred: {str(e)}'}, 500

        @token_required()
        def get(self):
            """
            Retrieve analytics filtered by park_id.
            """
            try:
                park_id = request.args.get('park_id')
                if not park_id:
                    return {'message': 'park_id parameter is required'}, 400
                
                analytics_list = Analytics.query.filter_by(park_id=park_id).all()
                if not analytics_list:
                    return {'message': 'No analytics found for the given park_id'}, 404
                
                return jsonify([entry.read() for entry in analytics_list]), 200
            except Exception as e:
                return {'message': f'An error occurred: {str(e)}'}, 500

    class _BULK_CRUD(Resource):
        @token_required()
        def post(self):
            """
            Bulk create analytics with validation.
            """
            try:
                data_list = request.get_json()
                if not isinstance(data_list, list):
                    return {'message': 'Expected a list of analytics data'}, 400

                results = {'success': 0, 'errors': []}

                for data in data_list:
                    try:
                        # Validation checks
                        required_fields = ['park_id', 'user_id', 'stars', 'review_text']
                        if not all(field in data for field in required_fields):
                            raise ValueError('Missing required fields')

                        if not isinstance(data['stars'], int) or not (1 <= data['stars'] <= 5):
                            raise ValueError('Stars must be an integer between 1 and 5')

                        if not isinstance(data['review_text'], str) or not data['review_text'].strip():
                            raise ValueError('review_text must be a non-empty string')

                        # Create and save
                        analytics = Analytics(
                            park_id=data['park_id'],
                            user_id=data['user_id'],
                            stars=data['stars'],
                            review_text=data['review_text']
                        )
                        analytics.create()
                        results['success'] += 1
                    except Exception as e:
                        results['errors'].append({'data': data, 'error': str(e)})

                return jsonify(results), 207
            except Exception as e:
                return {'message': f'An error occurred: {str(e)}'}, 500

    class _ANALYTICS(Resource):
        @token_required()
        def get(self):
            """
            Retrieve overall analytics summary data (reviews, stars) for all parks.
            """
            try:
                # Aggregate analytics data
                analytics_summary = (
                    db.session.query(
                        Analytics.park_id,
                        db.func.avg(Analytics.stars).label('stars'),
                        db.func.count(Analytics.id).label('total_reviews')
                    )
                    .group_by(Analytics.park_id)
                    .all()
                )

                if not analytics_summary:
                    return {'message': 'No analytics data available'}, 404

                # Format and return the response
                return jsonify([
                    {
                        "park_id": entry.park_id,
                        "stars": round(entry.stars, 1),
                        "total_reviews": entry.total_reviews
                    }
                    for entry in analytics_summary
                ]), 200
            except Exception as e:
                return {'message': f'An error occurred: {str(e)}'}, 500


# Add resources to the API
api.add_resource(AnalyticsAPI._CRUD, '/Analytics')
api.add_resource(AnalyticsAPI._BULK_CRUD, '/Analytics/bulk')
api.add_resource(AnalyticsAPI._ANALYTICS, '/Analytics/summary')



