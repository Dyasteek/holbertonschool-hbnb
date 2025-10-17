from .base_model import BaseModel

class Location(BaseModel):
    def __init__(self, address, city, country):
        super().__init__()
        self.address = address
        self.city = city
        self.country = country
        self.places = []

    def add_place(self, place):
        """Add a place to this location"""
        if place not in self.places:
            self.places.append(place)

    def to_dict(self):
        """Convert the instance to a dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            'address': self.address,
            'city': self.city,
            'country': self.country
        })
        return base_dict
