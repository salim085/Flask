from . import db

# Modèle utilisateur
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date)
    properties = db.relationship('Property', backref='owner', lazy=True)

# Modèle de bien immobilier
class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    property_type = db.Column(db.String(50))
    city = db.Column(db.String(50))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rooms = db.relationship('Room', backref='property', lazy=True)

# Modèle de pièce
class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    name = db.Column(db.String(50))
    size = db.Column(db.Float)
