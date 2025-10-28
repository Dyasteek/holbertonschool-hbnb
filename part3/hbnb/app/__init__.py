from flask import Flask
from flask_restx import Api
from app.services.facade import HBnBFacade
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.locations import api as locations_ns
from config import config as config_map, Config as BaseConfig


def create_app(config: str | type[BaseConfig] | BaseConfig | None = None) -> Flask:
    app = Flask(__name__)

    # Apply configuration
    if isinstance(config, str):
        cfg_class = config_map.get(config, config_map.get('default'))
        app.config.from_object(cfg_class)
    elif isinstance(config, type) and issubclass(config, BaseConfig):
        app.config.from_object(config)
    elif isinstance(config, BaseConfig):
        app.config.from_object(config)
    else:
        app.config.from_object(config_map.get('default'))
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Register all namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(locations_ns, path='/api/v1/locations')

    app.facade = HBnBFacade()

    # Basic health route (placeholder)
    @app.route('/health')
    def health():
        return 'maicol yeston'

    return app
