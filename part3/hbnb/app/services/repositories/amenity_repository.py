from ...models.amenity import Amenity
from ...persistence.sqlalchemy_repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)

