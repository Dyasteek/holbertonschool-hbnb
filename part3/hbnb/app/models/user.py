from .base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password_hash, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    def add_place(self, place):
        """Add a place owned by this user"""
        if place not in self.places:
            self.places.append(place)

    def get_reviews(self):
        """Get all reviews written by this user"""
        return self.reviews

    def to_dict(self):
        """Convert the instance to a dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        return base_dict
