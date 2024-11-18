from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import BadRequest
from app.services.property_service import PropertyService

property_bp = Blueprint('property', __name__)

#Solution plus intuitive adapté à RST
@property_bp.route('/properties/city/<city_name>', methods=['GET'])
@jwt_required()
def get_properties_by_city(city_name):

    properties = PropertyService.get_properties_by_city(city_name)

    return jsonify([property.to_dict() for property in properties]), 200


