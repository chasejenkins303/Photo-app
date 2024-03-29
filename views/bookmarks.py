from flask import Response, request
from flask_restful import Resource
from models import Bookmark, db
import json
from views import can_view_post
import flask_jwt_extended

class BookmarksListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        bookmarks = Bookmark.query.filter_by(user_id=self.current_user.id).all()
        return Response(json.dumps([bookmark.to_dict() for bookmark in bookmarks]), mimetype="application/json", status=200)

    @flask_jwt_extended.jwt_required()
    def post(self):
        # create a new "bookmark" based on the data posted in the body 
        body = request.get_json()
        print(body)

        try:
            if not body.get('post_id'):
                return Response(json.dumps({'error': 'post id required'}), status=400)
            if not can_view_post(body.get('post_id'), self.current_user):
                return Response(json.dumps({'error': 'permission denied'}), status=404)
        except:
            return Response(json.dumps({'error': 'post id wrong format'}), status=400)

        bookmark = Bookmark(
            post_id=body.get('post_id'),
            user_id=self.current_user.id
        )

        try:
            db.session.add(bookmark)    # issues the insert statement
            db.session.commit()   
        except:
            return Response(json.dumps({'error': 'Cannot post'}), status=400)  

        return Response(json.dumps(bookmark.to_dict()), mimetype="application/json", status=201)

class BookmarkDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def delete(self, id):
        try:
            id = int(id)
        except:
            return Response(json.dumps({'error': 'Bad id format'}), status=404)

        try:
            bookmark=Bookmark.query.get(id)
        except:
            return Response(json.dumps({'error': 'Bad id format'}), status=404)
        if bookmark is None:
            return Response(json.dumps({"message": "Bookmark not found"}), mimetype="application/json", status=404)
        if bookmark.user_id != self.current_user.id:
            return Response(json.dumps({"message": "No access allowed"}), mimetype="application/json", status=404)
        Bookmark.query.filter_by(id=id).delete()
        db.session.commit()
        return Response(json.dumps(None), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        BookmarksListEndpoint, 
        '/api/bookmarks', 
        '/api/bookmarks/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )

    api.add_resource(
        BookmarkDetailEndpoint, 
        '/api/bookmarks/<int:id>', 
        '/api/bookmarks/<int:id>',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
