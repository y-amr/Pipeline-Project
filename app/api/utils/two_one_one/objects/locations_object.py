import random

from app.api.utils.two_one_one.helper import Helper
from app.api.utils.two_one_one.objects.evse_object import EVSE


class Locations:
    LOCATION_TYPES = ['ON_STREET', 'PARKING_GARAGE', 'UNDERGROUND_GARAGE', 'PARKING_LOT', 'OTHER', 'UNKNOWN']
    id = None
    type = None
    address = None
    city = None
    postal_code = None
    country = None
    coordinates = None
    evses = None
    last_updated = None

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'type': self.type,
            'address': self.address,
            'city': self.city,
            'postal_code': self.postal_code,
            'country': self.country,
            'coordinates': self.coordinates,
            'evses': [i.serialize for i in self.evses if self.evses is not None],
            'last_updated': self.last_updated
        }

    def __init__(self, location_id, country_code, party_id, last_updated=Helper.get_current_timestamp()):
        self.id = str(location_id)
        self.type = random.choice(self.LOCATION_TYPES)
        self.address = "address of Location " + str(location_id)
        self.city = "city of Location " + str(location_id)
        self.postal_code = "75001"
        self.country = "FRA"
        self.coordinates = {"latitude": "48.804399", "longitude": "2.17151"}
        self.evses = [EVSE(str(location_id) + str(i), country_code, party_id) for i in range(1, random.randint(2, 5))]
        self.last_updated = last_updated
