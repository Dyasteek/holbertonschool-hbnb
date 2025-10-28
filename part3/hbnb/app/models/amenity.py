from .base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, description=""):
        super().__init__()
        self.name = name
        self.description = description
        self.places = []

    def add_place(self, place):
        """Add a place that has this amenity"""
        if place not in self.places:
            self.places.append(place)

    def to_dict(self):
        """Convert the instance to a dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            'name': self.name,
            'description': self.description
        })
        return base_dict
