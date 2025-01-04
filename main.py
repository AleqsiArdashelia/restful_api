from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, marshal_with, abort

import os
from dotenv import load_dotenv
from datetime import datetime
from werkzeug.security import generate_password_hash

from utils import user_table_dict, get_user_args


load_dotenv()
db_uri = os.getenv("SQLALCHEMY_DATABASE_URI")
user_args = get_user_args()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
api = Api(app)


class DatabaseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def validate_user_data(username, email, password):
    if DatabaseModel.query.filter_by(username=username).first():
        abort(400, message="username already exists")

    if DatabaseModel.query.filter_by(email=email).first():
        abort(400, message="this email already exists")
    elif "@" not in email:
        abort(400, message="email format is not valid")

    if len(password) < 8:
        abort(400, message="password must contain at least 8 characters")


class AllUsers(Resource):
    @marshal_with(user_table_dict)
    def get(self):
        users = DatabaseModel.query.all()
        return users

    @marshal_with(user_table_dict)
    def post(self):
        args = user_args.parse_args()

        username = args["username"].lower()
        email = args["email"].lower()
        password = args["password"]

        validate_user_data(username, email, password)

        user = DatabaseModel(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        users = DatabaseModel.query.all()
        return users, 201

api.add_resource(AllUsers, '/')


class IndividualUser(Resource):
    @marshal_with(user_table_dict)
    def get(self, id):
        user = DatabaseModel.query.filter_by(id=id).first()

        if not user:
            abort(404, message="user does not exist")
        return user

    @marshal_with(user_table_dict)
    def patch(self, id):
        args = user_args.parse_args()
        user = DatabaseModel.query.filter_by(id=id).first()

        if not user:
            abort(404, message="user does not exist")

        username = args["username"].lower()
        email = args["email"].lower()
        password = args["password"]

        validate_user_data(username, email, password)

        user.username = username
        user.email = email
        user.password = generate_password_hash(password)

        db.session.commit()
        return user

    @marshal_with(user_table_dict)
    def delete(self, id):
        user = DatabaseModel.query.filter_by(id=id).first()

        if not user:
            abort(404, message="user does not exist")

        db.session.delete(user)
        db.session.commit()
        users = DatabaseModel.query.all()
        return users

api.add_resource(IndividualUser, '/user_info/<int:id>')


if __name__ == '__main__':
    app.run(debug=False)
