from flask import Response, request
from flask_restful import Resource
from models import Following
import json
import flask_jwt_extended

def get_path():
    return request.host_url + 'api/followers/'

class FollowerListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        following = Following.query.filter_by(following_id=self.current_user.id).all()
        return Response(json.dumps([follows.to_dict_follower() for follows in following]), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        FollowerListEndpoint, 
        '/api/followers', 
        '/api/followers/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
