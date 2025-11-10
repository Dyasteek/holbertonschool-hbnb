from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload or {}

        email = credentials.get('email')
        password = credentials.get('password')
        if not email or not password:
            return {'error': 'Datos inválidos'}, 400

        user = facade.get_user_by_email(email)

        if not user or not user.check_password(password):
            return {'error': 'Credenciales inválidas'}, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )
        
        return {'access_token': access_token}, 200
