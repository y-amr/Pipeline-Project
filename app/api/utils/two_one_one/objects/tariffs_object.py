import random

from app.api.utils.two_one_one.helper import Helper


class PriceComponent:
    PRICE_COMPONENT_TARIFF_DIMENSION_TYPE = ['ENERGY', 'FLAT', 'PARKING_TIME', 'TIME']
    type = None
    price = None
    step_size = None

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'type': self.type,
            'price': self.price,
            'step_size': self.step_size,
        }

    def __init__(self):
        self.type = random.choice(self.PRICE_COMPONENT_TARIFF_DIMENSION_TYPE)
        self.price = round(random.random() * random.randint(0, 10), 4)
        self.step_size = random.randint(1, 1000)


class TariffElement:
    price_components = None

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'price_components': [i.serialize for i in self.price_components if self.price_components is not None],
        }

    def __init__(self):
        self.price_components = [PriceComponent() for i in range(0, random.randint(1, 5))]


class Tariffs:
    TARIFF_CURRENCY = ['DOL', 'EUR']
    id = None
    currency = None
    elements = None
    last_updated = None

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'currency': self.currency,
            'elements': [i.serialize for i in self.elements if self.elements is not None],
            'last_updated': self.last_updated
        }

    def __init__(self, tariff_id):
        self.id = str(tariff_id)
        self.currency = random.choice(self.TARIFF_CURRENCY)
        self.elements = [TariffElement() for i in range(0, random.randint(1, 5))]
        self.last_updated = Helper.get_current_timestamp()
