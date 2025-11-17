from ..persistence.repository import Repository
from .repositories.user_repository import UserRepository
from .repositories.place_repository import PlaceRepository
from .repositories.review_repository import ReviewRepository
from .repositories.amenity_repository import AmenityRepository
from ..models.user import User
from ..models.place import Place
from ..models.review import Review
from ..models.amenity import Amenity
from ..models.location import Location

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()
        self.location_repo = Repository()

    # User
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.create(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)

    def delete_user(self, user_id):
        self.user_repo.delete(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    # Place
    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.create(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def update_place(self, place_id, place_data):
        self.place_repo.update(place_id, place_data)

    def delete_place(self, place_id):
        self.place_repo.delete(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    # Review
    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.create(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def update_review(self, review_id, review_data):
        self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        self.review_repo.delete(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    # Amenity
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.create(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)

    def delete_amenity(self, amenity_id):
        self.amenity_repo.delete(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    # Location
    def create_location(self, location_data):
        location = Location(**location_data)
        self.location_repo.create(location)
        return location

    def get_location(self, location_id):
        return self.location_repo.get(location_id)

    def update_location(self, location_id, location_data):
        self.location_repo.update(location_id, location_data)

    def delete_location(self, location_id):
        self.location_repo.delete(location_id)

    def get_all_locations(self):
        return self.location_repo.get_all()
