from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.exceptions import BadRequest
from app.services.property_service import PropertyService

property_bp = Blueprint('property', __name__)

#Solution plus intuitive adapté à RST
@property_bp.route('/properties/city/<city_name>', methods=['GET'])
@jwt_required()
def get_properties_by_city(city_name):
    properties = PropertyService.get_properties_by_city(city_name)
    return jsonify([property.to_dict() for property in properties]), 200


#Solution fléxible et évolutive
@property_bp.route('/properties', methods=['GET'])
@jwt_required()
def get_filtered_properties():

    filters = request.args.to_dict()
    

    city = filters.get('city')
    if not city:
        raise BadRequest("Le paramètre 'city' est obligatoire.")


    properties = PropertyService.get_properties_with_filters(filters)
    
    return jsonify(properties), 200


@property_bp.route('/properties', methods=['PUT'])
@jwt_required()
def update_property():

    user_id = get_jwt_identity()
    data = request.get_json()
    adress = data.get('adress')



    if not adress:
        return jsonify({'message': "vous devez saisir une adresse"}), 400


    updated_property= PropertyService.update_property(user_id, data)

    if not updated_property :
        return jsonify({
            'message': 'propriété introuvable ou pas accessible',
        }), 400

    return jsonify({
        'message': 'Propriétés mises à jour avec succès.',
        'updated_properties': updated_property.to_dict() 
    }), 200
