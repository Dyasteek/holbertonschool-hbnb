from .base_model import BaseModel
from .. import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'
    
    name = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'name': self.name
        })
        return base_dict
