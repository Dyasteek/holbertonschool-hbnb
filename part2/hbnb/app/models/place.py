from .base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        if not title or len(title) > 100:
            raise ValueError("El título es obligatorio y no puede superar los 100 caracteres")
        if price <= 0:
            raise ValueError("El precio debe ser un valor positivo")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("La latitud debe estar entre -90 y 90")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("La longitud debe estar entre -180 y 180")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner  # instancia de User
        self.reviews = []   # lista de Review
        self.amenities = [] # lista de Amenity

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)
