import random

from app.api.utils.two_one_one.helper import Helper


class Connector:
    CONNECTOR_STANDARDS = ['CHADEMO', 'DOMESTIC_A', 'DOMESTIC_B', 'DOMESTIC_C', 'DOMESTIC_D', 'DOMESTIC_E', 'DOMESTIC_F', 'DOMESTIC_G', 'DOMESTIC_H', 'DOMESTIC_I', 'DOMESTIC_J', 'DOMESTIC_K', 'DOMESTIC_L', 'IEC_60309_2_single_16', 'IEC_60309_2_three_16', 'IEC_60309_2_three_32', 'IEC_60309_2_three_64', 'IEC_62196_T1', 'IEC_62196_T1_COMBO', 'IEC_62196_T2', 'IEC_62196_T2_COMBO', 'IEC_62196_T3A', 'IEC_62196_T3C', 'TESLA_R', 'TESLA_S']
    CONNECTOR_FORMATS = ['SOCKET', 'CABLE']
    CONNECTOR_POWER_TYPES = ['AC_1_PHASE', 'AC_3_PHASE', 'DC']
    id = None
    standard = None
    format = None
    power_type = None
    voltage = None
    amperage = None
    last_updated = None

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'standard': self.standard,
            'format': self.format,
            'power_type': self.power_type,
            'voltage': self.voltage,
            'amperage': self.amperage,
            'last_updated': self.last_updated
        }

    def __init__(self, conn_id):
        self.id = str(conn_id)
        self.standard = random.choice(self.CONNECTOR_STANDARDS)
        self.format = random.choice(self.CONNECTOR_FORMATS)
        self.power_type = random.choice(self.CONNECTOR_POWER_TYPES)
        self.voltage = random.randint(230, 1000)
        self.amperage = random.randint(16, 32)
        self.last_updated = Helper.get_current_timestamp()
