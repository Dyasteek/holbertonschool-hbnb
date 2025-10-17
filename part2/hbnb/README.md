HBNB

V1.0
- Basic data models:
  - BaseModel: id, created_at, updated_at, save(), update(), delete(), to_dict()
  - User: first_name, last_name, email, password_hash, is_admin
  - Place: title, description, price, max_guest, location, owner, amenities, reviews
  - Location: address, city, country
  - Amenity: name, description
  - Review: title, text, rating, place, user

- In-memory repository:
  - Store, get, list, update and delete objects in a dict

- Project structure (in parts):
  - hbnb/app/models/ -> Python classes (models)
  - hbnb/app/persistence/repository.py -> simple in-memory storage
  - hbnb/run.py -> (to be used later to run)


Notes
- No database, no ORM, no migrations
- Next update: build Flask endpoints using these models
