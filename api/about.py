# api/about.py
from flask import Blueprint, jsonify
from model.about import AboutModel

# Create a Blueprint for the API
about_api = Blueprint('about_api', __name__)

# Initialize the InfoModel
about_model = AboutModel()

@about_api.route('/api/data', methods=['GET'])
def get_data():
    data = about_model.get_all()
    return jsonify(data)