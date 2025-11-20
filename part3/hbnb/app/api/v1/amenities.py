from flask_restx import Namespace, Resource, fields
from ...services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.response(200, 'Amenities retrieved successfully')
    def get(self):
        """Get all amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': amenity.id, 
                'name': amenity.name} for amenity in amenities], 200

    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Create a new amenity"""
        amenity_data = api.payload or {}
        new_amenity = facade.create_amenity(amenity_data)
        return {'id': new_amenity.id, 
                'name': new_amenity.name}, 201
                
@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id,  
                'name': amenity.name}, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity successfully updated')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def put(self, amenity_id):
        """Update amenity details"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        amenity_data = api.payload
        facade.update_amenity(amenity_id, amenity_data)
        return {'message': 'Amenity updated successfully'}, 200

    @api.response(200, 'Amenity successfully deleted')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def delete(self, amenity_id):
        """Delete an amenity"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        facade.delete_amenity(amenity_id)
        return {'message': 'Amenity deleted successfully'}, 200