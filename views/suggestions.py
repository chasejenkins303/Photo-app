from flask import Response, request
from flask_restful import Resource
from models import User, Following
from views import get_authorized_user_ids
import json

class SuggestionsListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # suggestions should be any user with an ID that's not in this list:
        # print(get_authorized_user_ids(self.current_user))
        not_following = Following.query.filter(~Following.user_id.in_([self.current_user.id]))#=self.current_user.id).all()
        #building list of friends usernames
        friend_ids=[]
        for rec in not_following:
            friend_ids.append(rec.following_id)
        friend_ids.append(self.current_user.id)
            
        suggestions = User.query.filter(User.id.in_(friend_ids)).limit(7)
            
        return Response(json.dumps([sug.to_dict() for sug in suggestions]), mimetype="application/json", status=200)
    
        #return Response(json.dumps([]), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        SuggestionsListEndpoint, 
        '/api/suggestions', 
        '/api/suggestions/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
