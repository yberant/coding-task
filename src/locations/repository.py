from .models import Location
from django.db.models import QuerySet
from typing import Optional

class LocationRepository:
    def get_all_locations(
        self,
        order_by: str = '-id'
    ) -> QuerySet:
        return Location.objects.order_by(order_by)
    
    def filter_location_by_name(
        self,
        city_name: str,
        country_name: str
    ) -> QuerySet:
        return Location.objects.filter(city=city_name, country=country_name)

    
    def get_location_by_id(
        self, 
        id: int
    ) -> tuple[Optional[Location], Optional[str]]:
        try:
            return Location.objects.get(id=id), None
        except Location.DoesNotExist:
            return None, f"Location with id {id} not found"
        except Exception as e:
            return None, str(e)
    
    def create_location(
        self, 
        city_name: str, 
        country_name: str, 
        latitude: float, 
        longitude: float
    ) -> tuple[Optional[Location], Optional[str]]:

        try:
            return Location.objects.create(
                city=city_name, 
                country=country_name, 
                latitude=latitude, 
                longitude=longitude
            ), None
        except IntegrityError:
            return None, f"Location: {city}, {country} with latitude: {latitude}, longitude: {longitude} already exists"
        except Exception as e:
            return None, str(e)
    
    def delete_location(
        self, 
        location: Location
    ) -> Location:
        location.delete()
        return location