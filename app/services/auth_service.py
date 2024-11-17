from app.models import User, db
from werkzeug.exceptions import BadRequest
from flask_jwt_extended import create_access_token
from flask import jsonify


def register_user(username, password, first_name, last_name, birth_date):

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        raise BadRequest("Username already exists")

    new_user = User(username, password, first_name, last_name, birth_date)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return {"message": "User registered successfully"}, 201


def login_user(username, password):
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):  
        token = create_access_token(str(user.id))
        return {"access_token": token}, 200

    return {"message": "Invalid username or password"}, 401
