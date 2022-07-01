from app.api.utils.two_one_one.constants import Constants


class Versions:
    version = None
    url = None

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'version': self.version,
            'url': self.url
        }

    def __init__(self, version, role):
        if version == Constants.TWO_DOT_ONE_DOT_ONE_CONSTANT:
            self.version = Constants.TWO_DOT_ONE_DOT_ONE_CONSTANT
            if role == Constants.EMSP_CONSTANT:
                self.url = Constants.SERVER_URL + Constants.TO_EMSP_VERSIONS_DETAILS_211_ENDPOINT_CONSTANT
            elif role == Constants.CPO_CONSTANT:
                self.url = Constants.SERVER_URL + Constants.TO_CPO_VERSIONS_DETAILS_211_ENDPOINT_CONSTANT


class VersionsDetails:
    version = None
    endpoints = None

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'version': self.version,
            'endpoints': [i.serialize for i in self.endpoints if self.endpoints is not None]
        }

    def __init__(self, version, role):
        if version == Constants.TWO_DOT_ONE_DOT_ONE_CONSTANT:
            self.version = Constants.TWO_DOT_ONE_DOT_ONE_CONSTANT
            if role == Constants.EMSP_CONSTANT:
                self.endpoints = [Endpoint(identifier=Endpoint.CDRS_MODULE_ID, url=Constants.SERVER_URL + Constants.TO_EMSP_CDRS_211_ENDPOINT_CONSTANT),
                                  Endpoint(identifier=Endpoint.COMMANDS_MODULE_ID, url=Constants.SERVER_URL + Constants.TO_EMSP_COMMANDS_211_ENDPOINT_CONSTANT),
                                  Endpoint(identifier=Endpoint.CREDENTIALS_MODULE_ID, url=Constants.SERVER_URL + Constants.TO_EMSP_CREDENTIALS_211_ENDPOINT_CONSTANT),
                                  Endpoint(identifier=Endpoint.LOCATIONS_MODULE_ID, url=Constants.SERVER_URL + Constants.TO_EMSP_LOCATIONS_211_ENDPOINT_CONSTANT),
                                  Endpoint(identifier=Endpoint.SESSIONS_MODULE_ID, url=Constants.SERVER_URL + Constants.TO_EMSP_SESSIONS_211_ENDPOINT_CONSTANT),
                                  Endpoint(identifier=Endpoint.TARIFFS_MODULE_ID, url=Constants.SERVER_URL + Constants.TO_EMSP_TARIFFS_211_ENDPOINT_CONSTANT),
                                  Endpoint(identifier=Endpoint.TOKENS_MODULE_ID, url=Constants.SERVER_URL + Constants.TO_EMSP_TOKENS_211_ENDPOINT_CONSTANT)]
            elif role == Constants.CPO_CONSTANT:
                self.endpoints = [Endpoint(identifier=Endpoint.CDRS_MODULE_ID,
                                           url=Constants.SERVER_URL + Constants.TO_CPO_CDRS_211_ENDPOINT_CONSTANT),
                                  Endpoint(identifier=Endpoint.COMMANDS_MODULE_ID,
                                           url=Constants.SERVER_URL + Constants.TO_CPO_COMMANDS_211_ENDPOINT_CONSTANT),
                                  Endpoint(identifier=Endpoint.CREDENTIALS_MODULE_ID,
                                           url=Constants.SERVER_URL + Constants.TO_CPO_CREDENTIALS_211_ENDPOINT_CONSTANT),
                                  Endpoint(identifier=Endpoint.LOCATIONS_MODULE_ID,
                                           url=Constants.SERVER_URL + Constants.TO_CPO_LOCATIONS_211_ENDPOINT_CONSTANT),
                                  Endpoint(identifier=Endpoint.SESSIONS_MODULE_ID,
                                           url=Constants.SERVER_URL + Constants.TO_CPO_SESSIONS_211_ENDPOINT_CONSTANT),
                                  Endpoint(identifier=Endpoint.TARIFFS_MODULE_ID,
                                           url=Constants.SERVER_URL + Constants.TO_CPO_TARIFFS_211_ENDPOINT_CONSTANT),
                                  Endpoint(identifier=Endpoint.TOKENS_MODULE_ID,
                                           url=Constants.SERVER_URL + Constants.TO_CPO_TOKENS_211_ENDPOINT_CONSTANT)]


class Endpoint:
    CDRS_MODULE_ID = "cdrs"
    COMMANDS_MODULE_ID = "commands"
    CREDENTIALS_MODULE_ID = "credentials"
    LOCATIONS_MODULE_ID = "locations"
    SESSIONS_MODULE_ID = "sessions"
    TARIFFS_MODULE_ID = "tariffs"
    TOKENS_MODULE_ID = "tokens"
    identifier = None
    url = None

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'identifier': self.identifier,
            'url': self.url
        }

    def __init__(self, identifier, url):
        self.identifier = identifier
        self.url = url
