import jwt
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from __init__ import db
from api.jwt_authorize import token_required
from model.checklist import ChecklistItem  


# Blueprint for Checklist API
checklist_api = Blueprint('checklist_api', __name__, url_prefix='/api')
api = Api(checklist_api)


class ChecklistAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Add a new item to the checklist."""
            current_user = g.current_user
            data = request.get_json()


            if not data or 'item_name' not in data:
                return {"message": "Item name is required"}, 400


            new_item = ChecklistItem(user_id=current_user.id, item_name=data['item_name'])
            db.session.add(new_item)
            db.session.commit()


            return new_item.read(), 201



        @token_required()
        def get(self):
            """Retrieve all checklist items for the user."""
            current_user = g.current_user
            items = ChecklistItem.query.filter_by(user_id=current_user.id).all()
            return [item.read() for item in items], 200



        @token_required()
        def delete(self):
            """Remove an item from the checklist."""
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


    # Register the resource with API
    api.add_resource(_CRUD, '/checklist')