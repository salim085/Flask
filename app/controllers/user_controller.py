import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService
from werkzeug.exceptions import BadRequest, NotFound

# Définition du blueprint
user_bp = Blueprint('user', __name__)

@user_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    
    user_id = get_jwt_identity()  
    user = UserService.get_user_by_id(user_id)
    if not user:
        raise NotFound("Utilisateur introuvable")
    
    return jsonify({
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "birth_date": user.birth_date.strftime('%Y-%m-%d')
    }), 200

@user_bp.route('/user', methods=['PUT'])
@jwt_required()
def update_user():
    
    user_id = get_jwt_identity()  
    data = request.get_json()

    if not data:
        raise BadRequest("Aucune donnée à mettre à jour.")

    user = UserService.get_user_by_id(user_id)
    if not user:
        raise NotFound("Utilisateur introuvable")

    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'birth_date' in data:
        try:
            user.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
        except ValueError:
            raise BadRequest("Le format de la date de naissance est incorrect. Utilisez AAAA-MM-JJ.")

    
    updated_user = UserService.save_user(user)

    return jsonify({
        "message": "Informations mises à jour avec succès.",
        "user": {
            "username": updated_user.username,
            "first_name": updated_user.first_name,
            "last_name": updated_user.last_name,
            "birth_date": updated_user.birth_date.strftime('%Y-%m-%d')
        }
    }), 200
