from os import name
from flask import Flask, views
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# Data Model
class VideoModel(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  views = db.Column(db.Integer, nullable=False)
  likes = db.Column(db.Integer, nullable=False)

  def __repr__(self):
    return '<User %r>' % self.name

#create the DB - do this once after defining models
# db.create_all() 

# args for video body - like express body parser
video_post_args = reqparse.RequestParser()
video_post_args.add_argument("name", type=str, help="Video Name is Required", required=True)
video_post_args.add_argument("views", type=str, help="Video Views is Required", required=True)
video_post_args.add_argument("likes", type=str, help="Video Likes is Required", required=True)

# same as post args except nothing is required
video_patch_args = reqparse.RequestParser()
video_patch_args.add_argument("name", type=str)
video_patch_args.add_argument("views", type=str)
video_patch_args.add_argument("likes", type=str)

# type Defs for ORM
video_resource_fields = {
  'id': fields.Integer,
  'name': fields.String,
  'views': fields.Integer,
  'likes': fields.Integer
}

class Videos(Resource):
  @marshal_with(video_resource_fields)
  def get(self):
    result = VideoModel.query.all()
    return result


class Video(Resource):
  @marshal_with(video_resource_fields)
  def get(self, video_id):
    result = VideoModel.query.get_or_404(video_id)
    return result

  @marshal_with(video_resource_fields)
  def post(self, video_id):
    args = video_post_args.parse_args()
    # check if video with that id already exists
    exists = VideoModel.query.get(video_id)
    if exists: 
      abort(409, message='Video ID Taken')
    # create new video instance
    newVideo = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
    # add to db
    db.session.add(newVideo)
    db.session.commit()
    return newVideo, 201

  @marshal_with(video_resource_fields)
  def patch(self, video_id):
    args = video_patch_args.parse_args()
    # update the model
    updated = VideoModel.query.get_or_404(video_id)
    if args.name:
      updated.name = args.name
    if args.views:
      updated.views = args.views
    if args.likes:
      updated.likes = args.likes
    # save to db
    db.session.add(updated)
    db.session.commit()
    return updated

api.add_resource(Video, '/video/<int:video_id>')
api.add_resource(Videos, '/video/all')


if __name__ == "__main__":
  print(dir(VideoModel))
  app.run(debug=True)