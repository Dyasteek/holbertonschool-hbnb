from flask_restx import Namespace, Resource, fields
from ...services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Request models
place_create_model = api.model('PlaceCreate', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'price': fields.Integer(required=True, description='Price of the place'),
    'max_guest': fields.Integer(required=True, description='Maximum number of guests'),
    'location_id': fields.String(required=True, description='ID of the location')
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(required=False, description='Title of the place'),
    'description': fields.String(required=False, description='Description of the place'),
    'price': fields.Integer(required=False, description='Price of the place'),
    'max_guest': fields.Integer(required=False, description='Maximum number of guests'),
    'location_id': fields.String(required=False, description='ID of the location')
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
                'max_guest': place.max_guest, 
                'location_id': place.location.id if place.location else None, 
                'owner_id': place.owner.id if place.owner else None} for place in places], 200

    @api.expect(place_create_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Create a new place"""
        place_data = api.payload
        current_user_id = get_jwt_identity()

        owner = facade.get_user(current_user_id)
        if not owner:
            return {'error': 'User not found'}, 404

        location = facade.get_location(place_data['location_id'])
        if not location:
            return {'error': 'Location not found'}, 400

        place_obj_data = {
            'title': place_data['title'],
            'description': place_data['description'],
            'price': place_data['price'],
            'max_guest': place_data['max_guest'],
            'location': location,
            'owner': owner
        }

        new_place = facade.create_place(place_obj_data)
        owner.add_place(new_place)
        location.add_place(new_place)

        return {'id': new_place.id, 
                'title': new_place.title, 
                'description': new_place.description, 
                'price': new_place.price, 
                'max_guest': new_place.max_guest, 
                'location_id': new_place.location.id, 
                'owner_id': new_place.owner.id}, 201

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
                'max_guest': place.max_guest, 
                'location_id': place.location.id if place.location else None, 
                'owner_id': place.owner.id if place.owner else None}, 200

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
        if not place.owner or place.owner.id != current_user_id:
            return {'error': 'Acción no autorizada'}, 403

        place_data = api.payload or {}

        update_fields = {}
        allowed_fields = ['title', 'description', 'price', 'max_guest']
        for field in allowed_fields:
            if field in place_data:
                update_fields[field] = place_data[field]

        new_location = None
        if 'location_id' in place_data:
            new_location = facade.get_location(place_data['location_id'])
            if not new_location:
                return {'error': 'Location not found'}, 400
            update_fields['location'] = new_location

        if not update_fields:
            return {'error': 'No se proporcionaron datos para actualizar'}, 400

        if new_location and place.location and place in place.location.places:
            place.location.places.remove(place)

        facade.update_place(place_id, update_fields)

        if new_location:
            new_location.add_place(place)

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
        if not place.owner or place.owner.id != current_user_id:
            return {'error': 'Acción no autorizada'}, 403

        if place.owner and place in place.owner.places:
            place.owner.places.remove(place)
        if place.location and place in place.location.places:
            place.location.places.remove(place)

        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200