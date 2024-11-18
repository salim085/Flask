from app.models import Property
from werkzeug.exceptions import BadRequest

class PropertyService:
    @staticmethod
    def get_properties_by_city(city):
        properties = Property.query.filter_by(city=city.lower() ).all()
        return properties


    @staticmethod
    def get_properties_with_filters(filters):

        query = Property.query

        # Appliquer les filtres dynamiquement
        for key, value in filters.items():
            if hasattr(Property, key):  
                query = query.filter(getattr(Property, key) == value)
            else:
                 raise BadRequest(f"attribute {key} doesn't exist")   
        
        
        properties = query.all()
        
        
        return [
            {
                "id": property.id,
                "name": property.name,
                "description": property.description,
                "type": property.type,
                "city": property.city,
                "owner_id": property.owner_id,
            }
            for property in properties
        ]