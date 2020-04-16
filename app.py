from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
import os

app = Flask(__name__)
CORS(app)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Profile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), nullable=False)
    user_description = db.Column(db.String(150), nullable=False)
    user_image = db.Column(db.String(200), nullable=False)
    profile_name = db.Column(db.String(32), nullable=False)

    def __init__(self, email, user_description, user_image, profile_name):
        
        self.email = email
        self.user_description = user_description
        self.user_image = user_image
        self.profile_name = profile_name

class ProfileSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'user_description', 'user_image', 'profile_name')

profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)

@app.route("/", methods=["GET"])
def home():
    return "<h1>Class Project</h1>"

@app.route("/profiles", methods=["GET"])
def get_profiles():
    all_profiles = Profile.query.all()
    result = profiles_schema.dump(all_profiles)
    return jsonify(result)

@app.route('/profile/<id>', methods=['GET'])
def get_profile():
    profile = Profile.query.get(id)

    result = profile_schema.dump(profile)
    return jsonify(result)

#POST
@app.route("/profile", methods=["POST"])
def add_profile():
    email = request.json['email']
    user_description = request.json['user_description']
    user_image = request.json['user_image']
    profile_name = request.json['profile_name']

    new_profile = Profile(email, user_description, user_image, profile_name)

    db.session.add(new_profile)
    db.session.commit()

    profile = Profile.query.get(new_profile.id)
    return profile_schema.jsonify(profile)

@app.route("/profile/<id>", methods=["PATCH"])
def update_description(id):
    profile = Profile.query.get(id)
    
    new_description = request.json['user_description']
    new_image = request.json['user_image']
    
    profile.user_description = new_description
    profile.user_image = new_image

    db.session.commit()
    return profile_schema.jsonify(profile)

@app.route('/profile/<id>', methods=['DELETE'])
def delete_profile(id):
    record = Profile.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify('Deleted.')

if __name__ == "__main__":
    app.debug = True
    app.run()
