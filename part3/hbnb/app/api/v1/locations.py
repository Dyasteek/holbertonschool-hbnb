from flask_restx import Namespace, Resource, fields
from ...services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('locations', description='Location operations')

location_model = api.model('Location', {
    'address': fields.String(required=True, description='Address of the location'),
    'city': fields.String(required=True, description='City of the location'),
    'country': fields.String(required=True, description='Country of the location')
})

@api.route('/')
class LocationList(Resource):
    @api.response(200, 'Locations retrieved successfully')
    def get(self):
        """Get all locations"""
        locations = facade.get_all_locations()
        return [{'id': location.id, 
                'address': location.address, 
                'city': location.city, 
                'country': location.country} for location in locations], 200

    @api.expect(location_model, validate=True)
    @api.response(201, 'Location successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new location"""
        location_data = api.payload
        new_location = facade.create_location(location_data)
        return {'id': new_location.id, 
                'address': new_location.address, 
                'city': new_location.city, 
                'country': new_location.country}, 201

@api.route('/<location_id>')
class LocationResource(Resource):
    @api.response(200, 'Location details retrieved successfully')
    @api.response(404, 'Location not found')
    def get(self, location_id):
        """Get location details by ID"""
        location = facade.get_location(location_id)
        if not location:
            return {'error': 'Location not found'}, 404
        return {'id': location.id, 
                'address': location.address, 
                'city': location.city, 
                'country': location.country}, 200

    @api.expect(location_model, validate=True)
    @api.response(200, 'Location successfully updated')
    @api.response(404, 'Location not found')
    def put(self, location_id):
        """Update location details"""
        location = facade.get_location(location_id)
        if not location:
            return {'error': 'Location not found'}, 404
        
        location_data = api.payload
        facade.update_location(location_id, location_data)
        return {'message': 'Location updated successfully'}, 200

    @api.response(200, 'Location successfully deleted')
    @api.response(404, 'Location not found')
    def delete(self, location_id):
        """Delete a location"""
        location = facade.get_location(location_id)
        if not location:
            return {'error': 'Location not found'}, 404
        
        facade.delete_location(location_id)
        return {'message': 'Location deleted successfully'}, 200
