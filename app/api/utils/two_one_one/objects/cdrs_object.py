import random
import string

from app.api.utils.two_one_one.helper import Helper
from app.api.utils.two_one_one.objects.locations_object import Locations


class Cdrs:
    CDR_CURRENCY = ['DOL', 'EUR']
    CDR_AUTH_METHOD = ['AUTH_REQUEST', 'WHITELIST']
    id = None
    start_date_time = None
    stop_date_time = None
    auth_id = None
    auth_method = None
    location = None
    currency = None
    charging_periods = None
    total_cost = None
    total_energy = None
    total_time = None
    last_updated = None

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'start_date_time': self.start_date_time,
            'stop_date_time': self.stop_date_time,
            'auth_id': self.auth_id,
            'auth_method': self.auth_method,
            'location': self.location.serialize,
            'currency': self.currency,
            'charging_periods': self.charging_periods,
            'total_cost': self.total_cost,
            'total_energy': self.total_energy,
            'total_time': self.total_time,
            'last_updated': self.last_updated
        }

    def __init__(self, cdr_id, country_code, party_id):
        self.id = str(cdr_id)
        self.start_date_time = Helper.get_current_timestamp()
        self.stop_date_time = Helper.get_current_timestamp()
        self.auth_id = ''.join(random.choice(string.ascii_letters) for i in range(random.randint(5, 10)))
        self.auth_method = random.choice(self.CDR_AUTH_METHOD)
        location = Locations(location_id='111', country_code=country_code, party_id=party_id)
        # Keep one EVSE one connector
        location.evses = [location.evses[0]]
        location.evses[0].connectors = [location.evses[0].connectors[0]]
        self.location = location
        self.currency = random.choice(self.CDR_CURRENCY)
        self.total_cost = round(random.random() * random.randint(0, 100), 4)
        self.total_energy = round(random.random() * random.randint(0, 70), 4)
        self.total_time = round(random.random() * random.randint(0, 24), 4)
        self.charging_periods = [{'start_date_time': Helper.get_current_timestamp(), 'dimensions': [{'type': 'TIME', 'volume': self.total_time}]}]
        self.last_updated = Helper.get_current_timestamp()
