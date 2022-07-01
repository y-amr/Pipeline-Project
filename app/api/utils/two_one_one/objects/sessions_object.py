import random
import string

from app.api.utils.two_one_one.helper import Helper
from app.api.utils.two_one_one.objects.locations_object import Locations


class Sessions:
    SESSION_CURRENCY = ['DOL', 'EUR']
    SESSION_STATUS = ['ACTIVE', 'COMPLETED', 'INVALID', 'PENDING']
    SESSION_AUTH_METHOD = ['AUTH_REQUEST', 'WHITELIST']
    id = None
    start_datetime = None
    kwh = None
    auth_id = None
    auth_method = None
    location = None
    currency = None
    status = None
    last_updated = None

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'start_datetime': self.start_datetime,
            'kwh': self.kwh,
            'auth_id': self.auth_id,
            'auth_method': self.auth_method,
            'location': self.location.serialize,
            'currency': self.currency,
            'status': self.status,
            'last_updated': self.last_updated
        }

    def __init__(self, session_id, country_code, party_id):
        self.id = str(session_id)
        self.start_datetime = Helper.get_current_timestamp()
        self.kwh = round(random.random() * random.randint(0, 70), 4)
        self.auth_id = ''.join(random.choice(string.ascii_letters) for i in range(random.randint(5, 10)))
        self.auth_method = random.choice(self.SESSION_AUTH_METHOD)
        location = Locations(location_id='111', country_code=country_code, party_id=party_id)
        # Keep one EVSE one connector
        location.evses = [location.evses[0]]
        location.evses[0].connectors = [location.evses[0].connectors[0]]
        self.location = location
        self.currency = random.choice(self.SESSION_CURRENCY)
        self.status = random.choice(self.SESSION_STATUS)
        self.last_updated = Helper.get_current_timestamp()
