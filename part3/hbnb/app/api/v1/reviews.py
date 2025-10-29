from flask_restx import Namespace, Resource, fields
from ...services import facade

api = Namespace('reviews', description='Review operations')

# Review model
review_model = api.model('Review', {
    'title': fields.String(required=True, description='Title of the review'),
    'text': fields.String(required=True, description='Text content of the review'),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5'),
    'place_id': fields.String(required=True, description='ID of the place being reviewed'),
    'user_id': fields.String(required=True, description='ID of the user writing the review')
})

@api.route('/')
class ReviewList(Resource):
    @api.response(200, 'Reviews retrieved successfully')
    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return [{'id': review.id, 
                'title': review.title, 
                'text': review.text, 
                'rating': review.rating, 
                'place_id': review.place.id if review.place else None, 
                'user_id': review.user.id if review.user else None} for review in reviews], 200

    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new review"""
        review_data = api.payload
        
        # Get place and user objects
        place = facade.get_place(review_data['place_id'])
        user = facade.get_user(review_data['user_id'])
        
        if not place:
            return {'error': 'Place not found'}, 400
        if not user:
            return {'error': 'User not found'}, 400
        
        # Create review with objects
        review_obj_data = {
            'title': review_data['title'],
            'text': review_data['text'],
            'rating': review_data['rating'],
            'place': place,
            'user': user
        }
        
        new_review = facade.create_review(review_obj_data)
        return {'id': new_review.id, 
                'title': new_review.title, 
                'text': new_review.text, 
                'rating': new_review.rating, 
                'place_id': new_review.place.id if new_review.place else None, 
                'user_id': new_review.user.id if new_review.user else None}, 201

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {'id': review.id, 
                'title': review.title, 
                'text': review.text, 
                'rating': review.rating, 
                'place_id': review.place.id if review.place else None, 
                'user_id': review.user.id if review.user else None}, 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review successfully updated')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update review details"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        review_data = api.payload
        facade.update_review(review_id, review_data)
        return {'message': 'Review updated successfully'}, 200

    @api.response(200, 'Review successfully deleted')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200