from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import app
from __init__ import db

# Define a Blueprint for the analytics API
analytics_blueprint = Blueprint('analytics', __name__, url_prefix='/api')
api = Api(analytics_blueprint)

app.register_blueprint(analytics_blueprint)

class AnalyticsAPI:
    class _CRUD(Resource):
        def post(self):
            """
            Create a new analytics entry.
            """
            data = request.get_json()

            # Validate input
            required_fields = ['park_id', 'user_id', 'stars', 'review_text']
            if not all(field in data for field in required_fields):
                return {'message': 'Missing required fields'}, 400

            # Create and save a new analytics entry
            try:
                analytics = Analytics(
                    park_id=data['park_id'],
                    user_id=data['user_id'],
                    stars=data['stars'],
                    review_text=data['review_text']
                )
                analytics.create()
                return jsonify(analytics.read()), 201
            except Exception as e:
                return {'message': f'An error occurred: {str(e)}'}, 500

        def get(self):
            """
            Retrieve analytics filtered by park_id.
            """
            park_id = request.args.get('park_id')

            if not park_id:
                return {'message': 'park_id parameter is required'}, 400

            try:
                analytics_list = Analytics.query.filter_by(park_id=park_id).all()
                if not analytics_list:
                    return {'message': 'No analytics found for the given park_id'}, 404

                return jsonify([entry.read() for entry in analytics_list]), 200
            except Exception as e:
                return {'message': f'An error occurred: {str(e)}'}, 500

    class _BULK_CRUD(Resource):
        def post(self):
            """
            Bulk create analytics entries.
            """
            data_list = request.get_json()

            if not isinstance(data_list, list):
                return {'message': 'Expected a list of analytics data'}, 400

            results = {'success': 0, 'errors': []}

            for data in data_list:
                try:
                    # Validate input
                    required_fields = ['park_id', 'user_id', 'stars', 'review_text']
                    if not all(field in data for field in required_fields):
                        raise ValueError('Missing required fields')

                    # Create and save analytics entry
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

    class _SUMMARY(Resource):
        def get(self):
            """
            Retrieve overall analytics summary data (reviews, stars) for all parks.
            """
            try:
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
    api.add_resource(_CRUD, '/analytics')
    api.add_resource(_BULK_CRUD, '/analytics/bulk')
    api.add_resource(_SUMMARY, '/analytics/summary')
