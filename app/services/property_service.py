from app.models import Property

class PropertyService:
    @staticmethod
    def get_properties_by_city(city):
        properties = Property.query.filter_by(city=city.lower() ).all()
        return properties
