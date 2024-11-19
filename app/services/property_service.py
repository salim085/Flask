import copy
from app.models import Property, Room
from werkzeug.exceptions import BadRequest
from app import db

class PropertyService:
    @staticmethod
    def get_properties_by_city(city):
        properties = Property.query.filter_by(city=city.lower() ).all()
        return properties


    @staticmethod
    def get_properties_with_filters(filters):

        query = Property.query

        for key, value in filters.items():
            if hasattr(Property, key):  
                query = query.filter(getattr(Property, key) == value)
            else:
                 raise BadRequest(f"attribute {key} doesn't exist")   
        
        
        properties = query.all()
        
        
        return [
            {
                "adress": property.adress,
                "description": property.description,
                "type": property.type,
                "city": property.city
            }
            for property in properties
        ]
    
   
    @staticmethod
    def update_property(user_id, data):
        adress = data.get('adress')
        description = data.get('description')
        city = data.get('city')
        type = data.get('type')
        rooms = data.get('rooms', None) 
        property_to_update = Property.query.filter_by(adress=adress, owner_id=user_id).first()

        if not property_to_update:
            return None  
        
        property_to_update.description = description
        property_to_update.type = type
        property_to_update.city = city

        if rooms is not None:
            
            current_room_ids = {room['id'] for room in rooms if 'id' in room}
            for existing_room in property_to_update.rooms:
                if existing_room.id not in current_room_ids:
                    db.session.delete(existing_room)

            for room_data in rooms:
               
                room_id = room_data.get('id')  
                room_name = room_data.get('name')  
                room_area = room_data.get('area')  

                if room_id: 

                    room = Room.query.filter_by(id=room_id, property_adress=property_to_update.adress).first()
                    if room:
                        if room.name:
                            room.name = room_name

                        if room.area:
                            room.area = room_area
                    
                    else:  
                        raise BadRequest(f" Il n'y a aucune 'room' avec l'id {room_id}.")
                    

                else:  
                        
                    new_room = Room(name=room_name, area=room_area, property_adress=property_to_update.adress)
                    db.session.add(new_room)

        db.session.commit()
        return property_to_update
