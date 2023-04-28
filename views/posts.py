from flask import Response, request
from flask_restful import Resource
from models import Post, Following, db
from views import get_authorized_user_ids
import flask_jwt_extended
#import access_utils

import json

def get_path():
    return request.host_url + 'api/posts/'

def get_list_of_user_ids_in_network(user_id):
    following = Following.query.filter_by(user_id=user_id).all()
        #building list of friends usernames
    friend_ids=[rec.following_id for rec in following]
    friend_ids.append(user_id)
    return friend_ids

class PostListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user

    @flask_jwt_extended.jwt_required()
    def get(self):
        try:
            limit = request.args.get('limit') or 20
            limit = int(limit)
        except:
            return Response(
                json.dumps({'error': 'No string for limit'}), status=400
            )
        if limit >50:
            return Response(
                json.dumps({'error': 'Bad data. Limit cannot exceed 20'}), status=400
            )
        # get posts created by one of these users:
        #Get all ids of people that they are following

        following = Following.query.filter_by(user_id=self.current_user.id).all()
        #building list of friends usernames
        friend_ids=[]
        for rec in following:
            friend_ids.append(rec.following_id)
        friend_ids.append(self.current_user.id)
            
        posts = Post.query.filter(Post.user_id.in_(friend_ids)).limit(limit)
            
        return Response(json.dumps([post.to_dict() for post in posts]), mimetype="application/json", status=200)
    
    @flask_jwt_extended.jwt_required()
    def post(self):
        # create a new post based on the data posted in the body
        # request.getjson holds the data the user just sent. Stored as dictionary 
        body = request.get_json()
        print(body)

        if not body.get('image_url'):
            return Response(json.dumps({'error': 'image required'}), status=400)
        new_post = Post(
            image_url=body.get('image_url'),
            user_id=self.current_user.id, # must be a valid user_id or will throw an error
            caption=body.get('caption'),
            alt_text=body.get('alt_text')
        )
        db.session.add(new_post)    # issues the insert statement
        db.session.commit()       
        return Response(json.dumps(new_post.to_dict()), mimetype="application/json", status=201)
        
class PostDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
        
    @flask_jwt_extended.jwt_required()
    def patch(self, id):
        # update post based on the data posted in the body 
        post=Post.query.get(id)

        me_and_friends_id= get_list_of_user_ids_in_network(self.current_user.id)
       # posts_allowed = Post.query.filter('user_id' == self.current_user.id).limit(limit)

        body = request.get_json()

        if post is None or post.user_id not in me_and_friends_id:
            return Response(json.dumps({'error': 'Bad id'}), status=404)
        # if body.get('user_id')!=self.current_user.id:
        #     return Response(
        #         json.dumps({'error': 'Bad id.'}), status=404
        #     )
        else:
            if body.get('image_url'):
                post.image_url=body.get('image_url')
            if body.get('caption'):
                post.caption=body.get('caption')
            if body.get('alt_text'):
                post.alt_text=body.get('alt_text')


            db.session.commit()
            print(body)       
            return Response(json.dumps(post.to_dict()), mimetype="application/json", status=200)

    #@access_utils.can_modify_or_404
    @flask_jwt_extended.jwt_required()
    def delete(self, id):
        try:
            id = int(id)
        except:
            return Response(json.dumps({'error': 'Bad id format'}), status=404)

        try:
            post=Post.query.get(id)
        except:
            return Response(json.dumps({'error': 'Bad id format'}), status=404)
        if post is None:
            return Response(json.dumps({"message": "Post not found"}), mimetype="application/json", status=404)
        if post.user_id != self.current_user.id:
            return Response(json.dumps({"message": "No access allowed"}), mimetype="application/json", status=404)
        Post.query.filter_by(id=id).delete()
        db.session.commit()
        return Response(json.dumps(None), mimetype="application/json", status=200)

    @flask_jwt_extended.jwt_required()
    def get(self, id):


        me_and_friends_id= get_list_of_user_ids_in_network(self.current_user.id)

        post=Post.query.get(id)
        # if post.user_id not in me_and_friends_id:
        #     return Response(json.dumps({'error': 'No access'}), status=404)

        if post is None or post.user_id not in me_and_friends_id:
            return Response(json.dumps({'error': 'Post ' + str(id) +' does not exist'}), status=404)
        else:
            return Response(json.dumps(post.to_dict()), mimetype="application/json", status=200)

def initialize_routes(api):
    api.add_resource(
        PostListEndpoint, 
        '/api/posts', '/api/posts/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
    api.add_resource(
        PostDetailEndpoint, 
        '/api/posts/<int:id>', '/api/posts/<int:id>/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )