from flask import Response, request
from flask_restful import Resource
from models import LikePost, db
import json
from views import can_view_post
import flask_jwt_extended

class PostLikesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def post(self):

        body = request.get_json()
        print(body)
        # create a new "like_post" based on the data posted in the body 
        if not body.get('post_id'):
            return Response(json.dumps({'error': 'post id required'}), mimetype="application/json", status=400)
        try:
            id=int(body.get('post_id'))
        except:
            return Response(json.dumps({'error': 'invalid post id format'}), mimetype="application/json", status=400)

        if not can_view_post(body.get('post_id'), self.current_user):
            return Response(json.dumps({'error': 'Cannot like post'}), mimetype="application/json", status=404)


        like = LikePost(
            post_id=body.get('post_id'),
            user_id=self.current_user.id
        )
        try:
            db.session.add(like)
            db.session.commit()
        except:
            return Response(json.dumps({'error': 'Could not like'}), mimetype="application/json", status=400)

        return Response(json.dumps(like.to_dict()), mimetype="application/json", status=201)

class PostLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def delete(self, id):
        try:
            id = int(id)
        except:
            return Response(json.dumps({'error': 'Bad id format'}), status=404)

        try:
            like=LikePost.query.get(id)
        except:
            return Response(json.dumps({'error': 'Bad id format'}), status=404)
        if like is None:
            return Response(json.dumps({"message": "Like not found"}), mimetype="application/json", status=404)
        if like.user_id != self.current_user.id:
            return Response(json.dumps({"message": "No access allowed"}), mimetype="application/json", status=404)
        LikePost.query.filter_by(id=id).delete()
        db.session.commit()
        return Response(json.dumps(None), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        PostLikesListEndpoint, 
        '/api/posts/likes', 
        '/api/posts/likes/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )

    api.add_resource(
        PostLikesDetailEndpoint, 
        '/api/posts/likes/<int:id>', 
        '/api/posts/likes/<int:id>/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
