import random

from app.api.utils.two_one_one.constants import Constants
from app.api.utils.two_one_one.helper import Helper
from app.api.utils.two_one_one.objects.connector_object import Connector


class EVSE:
    EVSE_STATUS = ['AVAILABLE', 'BLOCKED', 'CHARGING', 'INOPERATIVE', 'OUTOFORDER', 'PLANNED', 'REMOVED', 'RESERVED', 'UNKNOWN']
    uid = None
    evse_id = None
    status = None
    connectors = None
    last_updated = None

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'uid': self.uid,
            'evse_id': self.evse_id,
            'status': self.status,
            'connectors': [i.serialize for i in self.connectors if self.connectors is not None],
            'last_updated': self.last_updated
        }

    def __init__(self, evse_uid, country_code, party_id):
        self.uid = str(evse_uid)
        self.evse_id = country_code + Constants.STAR_CONSTANT + party_id + Constants.STAR_CONSTANT + 'E' + str(evse_uid)
        self.status = random.choice(self.EVSE_STATUS)
        self.voltage = random.randint(230, 1000)
        self.connectors = [Connector(j) for j in range(1, random.randint(2, 5))]
        self.last_updated = Helper.get_current_timestamp()
