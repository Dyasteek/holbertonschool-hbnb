from flask_restx import Namespace, Resource, fields
from ...services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Request models
place_create_model = api.model('PlaceCreate', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place')
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(required=False, description='Title of the place'),
    'description': fields.String(required=False, description='Description of the place'),
    'price': fields.Float(required=False, description='Price per night'),
    'latitude': fields.Float(required=False, description='Latitude of the place'),
    'longitude': fields.Float(required=False, description='Longitude of the place')
})

@api.route('/')
class PlaceList(Resource):
    @api.response(200, 'Places retrieved successfully')
    def get(self):
        """Get all places"""
        places = facade.get_all_places()
        return [{'id': place.id, 
                'title': place.title, 
                'description': place.description, 
                'price': place.price, 
                'latitude': place.latitude, 
                'longitude': place.longitude,
                'user_id': place.user_id} for place in places], 200

    @api.expect(place_create_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Create a new place"""
        place_data = api.payload or {}
        current_user_id = get_jwt_identity()

        required_fields = ['title', 'description', 'price', 'latitude', 'longitude']
        missing_fields = [field for field in required_fields if field not in place_data]
        if missing_fields:
            return {'error': 'Datos incompletos'}, 400

        user = facade.get_user(current_user_id)
        if not user:
            return {'error': 'User not found'}, 404

        place_obj_data = {
            'title': place_data['title'],
            'description': place_data['description'],
            'price': place_data['price'],
            'latitude': place_data['latitude'],
            'longitude': place_data['longitude'],
            'user_id': current_user_id
        }

        new_place = facade.create_place(place_obj_data)

        return {'id': new_place.id, 
                'title': new_place.title, 
                'description': new_place.description, 
                'price': new_place.price, 
                'latitude': new_place.latitude, 
                'longitude': new_place.longitude,
                'user_id': new_place.user_id}, 201

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {'id': place.id, 
                'title': place.title, 
                'description': place.description, 
                'price': place.price, 
                'latitude': place.latitude, 
                'longitude': place.longitude,
                'user_id': place.user_id}, 200

    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place successfully updated')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized')
    @jwt_required()
    def put(self, place_id):
        """Update place details"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        current_user_id = get_jwt_identity()
        if place.user_id != current_user_id:
            return {'error': 'Acción no autorizada'}, 403

        place_data = api.payload or {}

        update_fields = {}
        allowed_fields = ['title', 'description', 'price', 'latitude', 'longitude']
        for field in allowed_fields:
            if field in place_data:
                update_fields[field] = place_data[field]

        if not update_fields:
            return {'error': 'No se proporcionaron datos para actualizar'}, 400

        facade.update_place(place_id, update_fields)

        return {'message': 'Place updated successfully'}, 200

    @api.response(200, 'Place successfully deleted')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        current_user_id = get_jwt_identity()
        if place.user_id != current_user_id:
            return {'error': 'Acción no autorizada'}, 403

        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200