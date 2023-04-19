from flask import Response, request
from flask_restful import Resource
import json
from models import db, Comment, Post, Following
from views import can_view_post

def get_list_of_user_ids_in_network(user_id):
    following = Following.query.filter_by(user_id=user_id).all()
        #building list of friends usernames
    friend_ids=[rec.following_id for rec in following]
    friend_ids.append(user_id)
    return friend_ids

class CommentListEndpoint(Resource):



    def __init__(self, current_user):
        self.current_user = current_user
    
    def post(self):

        body = request.get_json()
        print(body)

        # me_and_friends_id= get_list_of_user_ids_in_network(self.current_user.id)

        # postID=body.get('post_id')

        # post=Post.query.get(postID)
        # if post.user_id not in me_and_friends_id:
        #     return Response(json.dumps({'error': 'No access'}), status=404)

        # if post is None:
        #     return Response(json.dumps({'error': 'not valid post'}), status=404)

        # if not body.get('text'):
        #     return Response(json.dumps({'error': 'text required'}), status=400)
        try:
            post_id = body.get('post_id')
            post_id = int(post_id)
        except:
            return Response(
                json.dumps({'error': 'No string for postId'}), status=400
            )
        if not body.get('text'):
            return Response(
                json.dumps({'error': 'Need text in comment'}), status=400
            )
        
        if not can_view_post(post_id, self.current_user):
            return Response(
                json.dumps({'error': 'Cannot access'}), status=404
            )
        try:
            post=Post.query.get(post_id)
        except:
            return Response(
                json.dumps({'error': 'Post not exist'}), status=404
            )
        

        new_comment = Comment(
            text=body.get('text'),
            user_id=self.current_user.id, # must be a valid user_id or will throw an error
            #pub_date=body.get('pub_date'),
            post_id=body.get('post_id')
        )
        db.session.add(new_comment)    # issues the insert statement
        db.session.commit()       
        return Response(json.dumps(new_comment.to_dict()), mimetype="application/json", status=201)
        # create a new "Comment" based on the data posted in the body 
        # body = request.get_json()
        # print(body)
        # return Response(json.dumps({}), mimetype="application/json", status=201)
        
class CommentDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
  
    def delete(self, id):
        # delete "Comment" record where "id"=id
        try:
            id = int(id)
        except:
            return Response(json.dumps({'error': 'Bad id format'}), status=404)

        try:
            comment=Comment.query.get(id)
        except:
            return Response(json.dumps({'error': 'Bad id format'}), status=404)
        if not comment:
            return Response(json.dumps({"message": "Comment not found"}), mimetype="application/json", status=404)
        if comment.user_id != self.current_user.id:
            return Response(json.dumps({"message": "No access allowed"}), mimetype="application/json", status=404)
        Comment.query.filter_by(id=id).delete()
        db.session.commit()
        return Response(json.dumps(None), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        CommentListEndpoint, 
        '/api/comments', 
        '/api/comments/',
        resource_class_kwargs={'current_user': api.app.current_user}

    )
    api.add_resource(
        CommentDetailEndpoint, 
        '/api/comments/<int:id>', 
        '/api/comments/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
