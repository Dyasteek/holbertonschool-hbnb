from flask import Flask
from app.services.facade import HBnBFacade


def create_app() -> Flask:
    app = Flask(__name__)

    # Simple facade available to the app
    app.facade = HBnBFacade()

    # Basic health route (placeholder)
    @app.route('/health')
    def health():
        return 'maicol yeston'

    return app
