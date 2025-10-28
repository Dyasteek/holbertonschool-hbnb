V1.6 (Current)
- Complete REST API implementation:
  - All CRUD endpoints for Users, Places, Reviews, Amenities, Locations
  - Full validation and error handling

- API Endpoints:
  - Users: GET, POST, PUT, DELETE /api/v1/users/
  - Places: GET, POST, PUT, DELETE /api/v1/places/
  - Reviews: GET, POST, PUT, DELETE /api/v1/reviews/
  - Amenities: GET, POST, PUT, DELETE /api/v1/amenities/
  - Locations: GET, POST, PUT, DELETE /api/v1/locations/

- Updated project structure:
  - hbnb/app/models/ -> Python classes (models)
  - hbnb/app/persistence/repository.py -> simple in-memory storage
  - hbnb/app/services/facade.py -> business logic layer
  - hbnb/app/api/v1/ -> REST API endpoints
  - hbnb/app/__init__.py -> Flask app factory
  - hbnb/run.py -> Flask app runner
  - hbnb/.venv/ -> virtual environment

- Notes
  - Complete REST API with all CRUD operations
  - Data persistence during app session
  - Relationship validation (place-location, review-user, etc.)

V1.5
- Flask app working:
  - Basic Flask app with health endpoint (/health)
  - HBnBFacade service layer for business logic

- Updated project structure:
  - hbnb/app/models/ -> Python classes (models)
  - hbnb/app/persistence/repository.py -> simple in-memory storage
  - hbnb/app/services/facade.py -> business logic layer
  - hbnb/app/__init__.py -> Flask app factory
  - hbnb/run.py -> Flask app runner
  - hbnb/.venv/ -> virtual environment

- Notes for V1.5:
  - Virtual environment properly configured
  - All imports and dependencies resolved


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

How to run (with venv)
1. Go to project folder: part2/hbnb
2. Create venv: python -m venv .venv
3. Activate venv (PowerShell): .\.venv\Scripts\Activate.ps1
4. Install deps: pip install -r .\requirements.txt
5. Run Flask app: python .\run.py
6. Test: curl http://127.0.0.1:5000/healt

Notes
- No database, no ORM, no migrations
- Complete REST API with all CRUD operations
- Swagger documentation at /api/v1/
- Data persists during app session (in-memory)
