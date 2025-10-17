from app.persistence.repository import Repository
from app.models.user import User
from app.models.place import Place
from app.models.review import Rewiew
from app.models.amenity import Amenity
from app.models.location import Location

class HBnBFacade:
    def __init__(self):
        self.user_repo = Repository()
        self.place_repo = Repository()
        self.review_repo = Repository()
        self.amenity_repo = Repository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.User_repo.create(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass
