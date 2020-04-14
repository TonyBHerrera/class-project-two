from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
import os

app = Flask(__name__)
CORS(app)
heroku = Heroku(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Profile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer, primary_key = True)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    user_description = db.Column(db.String(150), nullable=False)

    def __init__(self, password, email, user_description):
        self.password = password
        self.email = email
        self.user_description = user_description

class ProfileSchema(ma.Schema):
    class Meta:
        fields = ('id', 'password', 'email', 'user_description')

profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)

@app.route("/", methods=["GET"])
def home():
    return "<h1> Class Project </h1>"

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
    password = request.json['password']
    email = request.json['email']
    user_description = request.json['user_description']

    new_profile = Profile(password, email, user_description)

    db.session.add(new_profile)
    db.session.commit()

    profile = Profile.query.get(new_profile.id)
    return profile_schema.jsonify(profile)

@app.route("/profile/<id>", methods=["PATCH"])
def update_description(id):
    profile = Profile.query.get(id)

    new_description = request.json['user_description']

   profile.user_description = new_description

    db.session.commit()
    return profile_schema.jsonify(profile)

@app.route('/profile/<id>')
def delete_todo(id):
    record = Profile.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify('Deleted.')

if __name__ == "__main__":
    app.debug = True
    app.run()
