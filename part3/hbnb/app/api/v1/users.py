from flask_restx import Namespace, Resource, fields
from ...services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

user_create_model = api.model('UserCreate', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user')
})

@api.route('/')
class UserList(Resource):
    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        return [{'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email} for user in users], 200

    @api.expect(user_create_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload or {}

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email}, 201

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email}, 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized')
    @jwt_required()
    def put(self, user_id):
        """Update user details"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        current_user_id = get_jwt_identity()
        if user_id != current_user_id:
            return {'error': 'Acción no autorizada'}, 403

        user_data = api.payload or {}

        if 'email' in user_data or 'password' in user_data:
            return {'error': 'No puede modificar su correo electrónico o contraseña'}, 400

        update_fields = {}
        for field in ['first_name', 'last_name']:
            if field in user_data:
                update_fields[field] = user_data[field]

        if not update_fields:
            return {'error': 'No se proporcionaron datos para actualizar'}, 400

        facade.update_user(user_id, update_fields)
        return {'message': 'User updated successfully'}, 200

    @api.response(200, 'User successfully deleted')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        facade.delete_user(user_id)
        return {'message': 'User deleted successfully'}, 200