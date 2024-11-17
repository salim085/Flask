from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user
from werkzeug.exceptions import BadRequest

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
   
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    first_name= data.get('first_name')
    last_name= data.get('last_name')
    birth_date=data.get('birth_date')


    if not username or not password:
        raise BadRequest("Username and password are required")

    response, status_code = register_user(username, password, first_name, last_name, birth_date )
    return jsonify(response), status_code



@auth_bp.route('/login', methods=['POST'])
def login():
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        raise BadRequest("Username and password are required")

    response, status_code = login_user(username, password)
    return jsonify(response), status_code
