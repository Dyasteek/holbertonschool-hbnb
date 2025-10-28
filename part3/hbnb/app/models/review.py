from .base_model import BaseModel

class Review(BaseModel):
    def __init__(self, title, text, rating, place, user):
        super().__init__()
        self.title = title
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def to_dict(self):
        """Convert the instance to a dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            'title': self.title,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place.id if self.place else None,
            'user_id': self.user.id if self.user else None
        })
        return base_dict
