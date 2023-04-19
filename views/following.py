from flask import Response, request
from flask_restful import Resource
from models import Following, User, db
import json
from views import can_view_post

def get_path():
    return request.host_url + 'api/posts/'

class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
       following = Following.query.filter_by(user_id=self.current_user.id).all()
       return Response(json.dumps([follows.to_dict_following() for follows in following]), mimetype="application/json", status=200)

    def post(self):

        body = request.get_json()
        #print(body)
        try:
            if body.get('user_id') is None:
                return Response(json.dumps({'error': 'user id required'}), mimetype="application/json", status=400)
        except:
            return Response(json.dumps({'error': 'user id required'}), mimetype="application/json", status=400)

        try:
            id=int(body.get('user_id'))
        except:
            return Response(json.dumps({'error': 'invalid user id format'}), mimetype="application/json", status=400)
        try:
            user = User.query.get(body.get('user_id'))
            if not user:
                return Response(json.dumps({'error': 'Could not get user'}), mimetype="application/json", status=404)

        except:
            return Response(json.dumps({'error': 'Could not get user'}), mimetype="application/json", status=404)
        following = Following(
            user_id=self.current_user.id,
            following_id=body.get('user_id')
        )
        try:
            db.session.add(following)
            db.session.commit()
        except:
            return Response(json.dumps({'error': 'Already following'}), mimetype="application/json", status=400)

        return Response(json.dumps(following.to_dict_following()), mimetype="application/json", status=201)


class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        try:
            id = int(id)
        except:
            return Response(json.dumps({'error': 'Bad id format'}), status=404)

        try:
            following=Following.query.get(id)
        except:
            return Response(json.dumps({'error': 'Bad id format'}), status=404)
        if following is None:
            return Response(json.dumps({"message": "Following not found"}), mimetype="application/json", status=404)
        if following.user_id != self.current_user.id:
            return Response(json.dumps({"message": "No access allowed"}), mimetype="application/json", status=404)
        Following.query.filter_by(id=id).delete()
        db.session.commit()
        return Response(json.dumps(None), mimetype="application/json", status=200)




def initialize_routes(api):
    api.add_resource(
        FollowingListEndpoint, 
        '/api/following', 
        '/api/following/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<int:id>', 
        '/api/following/<int:id>/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
