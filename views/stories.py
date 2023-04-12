from flask import Response
from flask_restful import Resource
from models import Story, Following
from views import get_authorized_user_ids
import json

class StoriesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # get stories created by one of these users:
        following = Following.query.filter_by(user_id=self.current_user.id).all()
        #building list of friends usernames
        friend_ids=[]
        for rec in following:
            friend_ids.append(rec.following_id)
        friend_ids.append(self.current_user.id)
            
        stories = Story.query.filter(Story.user_id.in_(friend_ids))
            
        return Response(json.dumps([story.to_dict() for story in stories]), mimetype="application/json", status=200)
    
        # print(get_authorized_user_ids(self.current_user))
        # return Response(json.dumps([]), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        StoriesListEndpoint, 
        '/api/stories', 
        '/api/stories/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
