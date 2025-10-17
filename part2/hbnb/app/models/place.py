from .base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, max_guest, location, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.max_guest = max_guest
        self.location = location
        self.owner = owner
        self.amenities = []
        self.reviews = []

    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_review(self, review):
        """Add a review to the place"""
        if review not in self.reviews:
            self.reviews.append(review)

    def get_amenities(self):
        """Get all amenities of the place"""
        return self.amenities

    def get_reviews(self):
        """Get all reviews of the place"""
        return self.reviews

    def to_dict(self):
        """Convert the instance to a dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'max_guest': self.max_guest,
            'location_id': self.location.id if self.location else None,
            'owner_id': self.owner.id if self.owner else None
        })
        return base_dict