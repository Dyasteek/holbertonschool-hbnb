import os
from hbnb.app import create_app
from hbnb.config import config as config_map

flask_config_name = os.getenv('FLASK_CONFIG', 'default')
app = create_app(flask_config_name)

if __name__ == '__main__':
    app.run(debug=app.config.get('DEBUG', False))
