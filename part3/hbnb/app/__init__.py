from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config as config_map, Config as BaseConfig

bcrypt = Bcrypt()
jwt = JWTManager()
cors = CORS()
db = SQLAlchemy()

def create_app(config: str | type[BaseConfig] | BaseConfig | None = None) -> Flask:
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # Configuration
    if isinstance(config, str):
        cfg_class = config_map.get(config, config_map.get('default'))
        app.config.from_object(cfg_class)
    elif isinstance(config, type) and issubclass(config, BaseConfig):
        app.config.from_object(config)
    elif isinstance(config, BaseConfig):
        app.config.from_object(config)
    else:
        app.config.from_object(config_map.get('default'))

    # configuration key JWT
    app.config["JWT_SECRET_KEY"] = app.config["SECRET_KEY"]

    # Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    #CORS config
    cors.init_app(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    with app.app_context():
        from .models import user, place, review, amenity
        from .models.place_amenity import place_amenity
        db.create_all()

    @app.route('/health')
    def health():
        return 'maicol yeston'

    from .services.facade import HBnBFacade
    from .api.v1.users import api as users_ns
    from .api.v1.amenities import api as amenities_ns
    from .api.v1.places import api as places_ns
    from .api.v1.reviews import api as reviews_ns
    from .api.v1.locations import api as locations_ns
    from .api.v1.auth import api as auth_ns

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(locations_ns, path='/api/v1/locations')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    app.facade = HBnBFacade()

    return app
