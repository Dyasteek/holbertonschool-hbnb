from ...models.user import User
from ...persistence.sqlalchemy_repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)
    
    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

