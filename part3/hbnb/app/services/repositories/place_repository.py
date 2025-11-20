from ...models.place import Place
from ...persistence.sqlalchemy_repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

