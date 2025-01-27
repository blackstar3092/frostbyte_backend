from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import app
from __init__ import db
from model.analytics import Analytics

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
            required_fields = ['channel_id', 'user_id', 'stars']
            if not all(field in data for field in required_fields):
                return {'message': 'Missing required fields'}, 400

            # Create and save a new analytics entry
            try:
                analytics = Analytics(
                    channel_id=data['channel_id'],
                    user_id=data['user_id'],
                    stars=data['stars']
                )
                analytics.create()
                return analytics.read(), 201
            except Exception as e:
                return {'message': f'An error occurred: {str(e)}'}, 500

        def get(self):
            """
            Retrieve analytics filtered by channel_id.
            """
            channel_id = request.args.get('channel_id')

            if not channel_id:
                return {'message': 'channel_id parameter is required'}, 400

            try:
                analytics_list = Analytics.query.filter_by(channel_id=channel_id).all()
                if not analytics_list:
                    return {'message': 'No analytics found for the given channel_id'}, 404

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
                    required_fields = ['channel_id', 'user_id', 'stars']
                    if not all(field in data for field in required_fields):
                        raise ValueError('Missing required fields')

                    # Create and save analytics entry
                    analytics = Analytics(
                        channel_id=data['channel_id'],
                        user_id=data['user_id'],
                        stars=data['stars'],
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
                        Analytics.channel_id,
                        db.func.avg(Analytics.stars).label('stars'),
                        db.func.count(Analytics.id).label('total_reviews')
                    )
                    .group_by(Analytics.channel_id)
                    .all()
                )

                if not analytics_summary:
                    return {'message': 'No analytics data available'}, 404

                return jsonify([
                    {
                        "channel_id": entry.channel_id,
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
