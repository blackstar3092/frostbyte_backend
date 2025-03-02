import jwt
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from __init__ import app, db
from api.jwt_authorize import token_required

# Blueprint for Checklist API
checklist_api = Blueprint('checklist_api', __name__, url_prefix='/api')
api = Api(checklist_api)

# Camping Checklist Model
class ChecklistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    is_checked = db.Column(db.Boolean, default=False)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def read(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "item_name": self.item_name,
            "is_checked": self.is_checked
        }

class ChecklistAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Add a new item to the checklist"""
            current_user = g.current_user
            data = request.get_json()

            if not data or 'item_name' not in data:
                return {"message": "Item name is required"}, 400

            new_item = ChecklistItem(user_id=current_user.id, item_name=data['item_name'])
            new_item.create()

            return jsonify(new_item.read())

        @token_required()
        def get(self):
            """Retrieve all checklist items for the user"""
            current_user = g.current_user
            items = ChecklistItem.query.filter_by(user_id=current_user.id).all()
            return jsonify([item.read() for item in items])

        @token_required()
        def delete(self):
            """Remove an item from the checklist"""
            current_user = g.current_user
            data = request.get_json()

            if not data or 'id' not in data:
                return {"message": "Item ID is required"}, 400

            item = ChecklistItem.query.filter_by(id=data['id'], user_id=current_user.id).first()
            if not item:
                return {"message": "Item not found"}, 404

            db.session.delete(item)
            db.session.commit()

            return {"message": "Item removed"}, 200

    api.add_resource(_CRUD, '/checklist')

