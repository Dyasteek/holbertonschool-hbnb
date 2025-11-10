from flask_restx import Namespace, Resource, fields
from ...services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Request models
review_create_model = api.model('ReviewCreate', {
    'title': fields.String(required=True, description='Title of the review'),
    'text': fields.String(required=True, description='Text content of the review'),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5'),
    'place_id': fields.String(required=True, description='ID of the place being reviewed')
})

review_update_model = api.model('ReviewUpdate', {
    'title': fields.String(required=False, description='Title of the review'),
    'text': fields.String(required=False, description='Text content of the review'),
    'rating': fields.Integer(required=False, description='Rating from 1 to 5')
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

    @api.expect(review_create_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Create a new review"""
        review_data = api.payload

        current_user_id = get_jwt_identity()
        user = facade.get_user(current_user_id)
        if not user:
            return {'error': 'User not found'}, 404

        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 400

        if place.owner and place.owner.id == current_user_id:
            return {'error': 'No puedes revisar tu propio lugar'}, 400

        existing_reviews = [
            review for review in facade.get_all_reviews()
            if review.place and review.place.id == place.id
            and review.user and review.user.id == current_user_id
        ]
        if existing_reviews:
            return {'error': 'Ya has reseñado este lugar'}, 400

        if not (1 <= review_data['rating'] <= 5):
            return {'error': 'Rating must be between 1 and 5'}, 400

        review_obj_data = {
            'title': review_data['title'],
            'text': review_data['text'],
            'rating': review_data['rating'],
            'place': place,
            'user': user
        }

        new_review = facade.create_review(review_obj_data)
        place.add_review(new_review)
        user.reviews.append(new_review)

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

    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review successfully updated')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized')
    @jwt_required()
    def put(self, review_id):
        """Update review details"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        current_user_id = get_jwt_identity()
        if not review.user or review.user.id != current_user_id:
            return {'error': 'Acción no autorizada'}, 403

        review_data = api.payload or {}

        update_fields = {}
        allowed_fields = ['title', 'text', 'rating']
        for field in allowed_fields:
            if field in review_data:
                update_fields[field] = review_data[field]

        if 'rating' in update_fields and not (1 <= update_fields['rating'] <= 5):
            return {'error': 'Rating must be between 1 and 5'}, 400

        if not update_fields:
            return {'error': 'No se proporcionaron datos para actualizar'}, 400

        facade.update_review(review_id, update_fields)
        return {'message': 'Review updated successfully'}, 200

    @api.response(200, 'Review successfully deleted')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        current_user_id = get_jwt_identity()
        if not review.user or review.user.id != current_user_id:
            return {'error': 'Acción no autorizada'}, 403

        if review.user and review in review.user.reviews:
            review.user.reviews.remove(review)
        if review.place and review in review.place.reviews:
            review.place.reviews.remove(review)

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200