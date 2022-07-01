import random

from app.api.utils.two_one_one.helper import Helper


class Tokens:
    TOKENS_TOKENSTYPE = ['OTHER', 'RFID']
    TOKENS_VALID = [True, False]
    TOKENS_WHITELISTTYPE = ['ALWAYS', 'ALLOWED', 'ALLOWED_OFFLINE', 'NEVER']
    uid = None
    type = None
    auth_id = None
    visual_number = None
    issuer = None
    valid = None
    whitelist = None
    language = None
    last_updated = None

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'uid': self.uid,
            'type': self.type,
            'auth_id': self.auth_id,
            'visual_number': self.visual_number,
            'issuer': self.issuer,
            'valid': self.valid,
            'whitelist': self.whitelist,
            'language': self.language,
            'last_updated': self.last_updated
        }

    def __init__(self, uid):
        self.uid = str(uid)
        self.type = random.choice(self.TOKENS_TOKENSTYPE)
        self.auth_id = str(uid)
        self.visual_number = str(uid)
        self.issuer = str(uid)
        self.valid = random.choice(self.TOKENS_VALID)
        self.whitelist = random.choice(self.TOKENS_WHITELISTTYPE)
        self.language = 'FR'
        self.last_updated = Helper.get_current_timestamp()
