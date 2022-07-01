import uuid

from app.api.utils.two_one_one.constants import Constants


class Credentials:
    token = None
    url = None
    business_details = None
    party_id = None
    country_code = None

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'token': self.token,
            'url': self.url,
            'business_details': {'name': 'GIREVE OCPI tester'},
            'party_id': self.party_id,
            'country_code': self.country_code
        }

    def __init__(self, country_code, party_id, role):
        self.token = uuid.uuid4().__str__()
        if role == Constants.EMSP_CONSTANT:
            self.url = Constants.SERVER_URL + Constants.TO_EMSP_VERSIONS_ENDPOINT_CONSTANT
        elif role == Constants.CPO_CONSTANT:
            self.url = Constants.SERVER_URL + Constants.TO_CPO_VERSIONS_ENDPOINT_CONSTANT
        self.party_id = party_id
        self.country_code = country_code
