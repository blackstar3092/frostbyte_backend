import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from api.Analytics import Analytics
from model.user import User
from model.section import Section

analytics_api = Blueprint('analytics_api', __name__, url_prefix='/api')
api = Api(analytics_api)

class AnalyticsAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create a new analytics entry with validation.
            """
            current_user = g.current_user
            data = request.get_json()

            # Validation for required fields
            if not all(k in data for k in ('park_id', 'user_id', 'stars', 'review_text')):
                return {'message': 'Missing required fields'}, 400

            # Type checking and validations
            if not isinstance(data['stars'], int) or not (1 <= data['stars'] <= 5):
                return {'message': 'Stars must be an integer between 1 and 5'}, 400
            if not isinstance(data['review_text'], str) or not data['review_text'].strip():
                return {'message': 'review_text must be a non-empty string'}, 400

            # Create new analytics entry
            analytics = Analytics(
                park_id=data['park_id'],
                user_id=data['user_id'],
                stars=data['stars'],
                review_text=data['review_text'],
                moderator_id=current_user.id
            )
            analytics.create()
            return jsonify(analytics.read())

        @token_required()
        def get(self):
            """
            Retrieve analytics filtered by park_id.
            """
            park_id = request.args.get('park_id')
            if not park_id:
                return {'message': 'park_id parameter is required'}, 400
            
            analytics_list = Analytics.query.filter_by(park_id=park_id).all()
            return jsonify([entry.read() for entry in analytics_list])

    class _BULK_CRUD(Resource):
        @token_required()
        def post(self):
            """
            Bulk create analytics with validation.
            """
            data_list = request.get_json()
            if not isinstance(data_list, list):
                return {'message': 'Expected a list of analytics data'}, 400

            results = {'success': 0, 'errors': []}

            for data in data_list:
                try:
                    # Validation checks
                    if not all(k in data for k in ('park_id', 'user_id', 'stars', 'review_text')):
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
                except ValueError as e:
                    results['errors'].append({'data': data, 'error': str(e)})
            
            return jsonify(results)

    class _ANALYTICS(Resource):
        @token_required()
        def get(self):
            """
            Retrieve overall analytics data (reviews, stars) for all parks.
            """
            analytics = Analytics.query.all()
            return jsonify([entry.read() for entry in analytics])

api.add_resource(AnalyticsAPI._CRUD, '/analytics')
api.add_resource(AnalyticsAPI._BULK_CRUD, '/analytics/bulk')
api.add_resource(AnalyticsAPI._ANALYTICS, '/analytics/summary')

