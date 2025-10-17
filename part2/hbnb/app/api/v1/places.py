from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Place model
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'price': fields.Integer(required=True, description='Price of the place'),
    'max_guest': fields.Integer(required=True, description='Maximum number of guests'),
    'location_id': fields.String(required=True, description='ID of the location'),
    'owner_id': fields.String(required=True, description='ID of the owner')
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

    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place"""
        place_data = api.payload
        
        # Get location and owner objects
        location = facade.get_location(place_data['location_id'])
        owner = facade.get_user(place_data['owner_id'])
        
        if not location:
            return {'error': 'Location not found'}, 400
        if not owner:
            return {'error': 'Owner not found'}, 400
        
        # Create place with objects
        place_obj_data = {
            'title': place_data['title'],
            'description': place_data['description'],
            'price': place_data['price'],
            'max_guest': place_data['max_guest'],
            'location': location,
            'owner': owner
        }
        
        new_place = facade.create_place(place_obj_data)
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

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place successfully updated')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """Update place details"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        place_data = api.payload
        facade.update_place(place_id, place_data)
        return {'message': 'Place updated successfully'}, 200

    @api.response(200, 'Place successfully deleted')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200