from . import db
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Modèle Utilisateur
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    properties = db.relationship('Property', backref='owner', lazy=True)

    def __init__(self, username, password, first_name, last_name, birth_date):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.username = username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Modèle Propriété 
class Property(db.Model):
    adress = db.Column(db.String(100), nullable=False, primary_key=True)
    description = db.Column(db.String(500))
    type = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)

    # Relation one-to-many avec Room
    rooms = db.relationship('Room', backref='property', lazy=True)
    
    # ForeignKey vers User
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, description, property_type, city, owner_id):
        self.adress = name
        self.description = description
        self.type = property_type
        self.city = city
        self.owner_id = owner_id

    def to_dict(self):
        return {
            'adress': self.adress,
            'description': self.description,
            'type': self.type,
            'city': self.city,
            'rooms': [ room.to_dict() for room in self.rooms]
        }

# Modèle Pièce 
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Integer)  
    property_adress= db.Column(db.String(100), db.ForeignKey('property.adress'), nullable=True)
    name=db.Column(db.String(100), nullable=True)
    def __init__(self, name, area, property_adress):
        self.name = name
        self.area = area
        self.property_adress =property_adress

    def to_dict(self):
        return {
            'id': self.id,
            'area': self.area,
            'name': self.name
        }

