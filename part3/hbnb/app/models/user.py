from .base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = None
        if password is not None:
            self.set_password(password)
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    def set_password(self, password):
        from .. import bcrypt
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        if not self.password_hash:
            return False
        from .. import bcrypt
        return bcrypt.check_password_hash(self.password_hash, password)

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
