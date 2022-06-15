from flask_restx import Resource, Namespace
from flask import request, abort
from models import User, UserSchema
from setup_db import db
from utils import get_hash

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        rs = db.session.query(User).all()
        res = UserSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        req_json = request.json
        username = req_json.get("username", None)
        password = req_json.get("password", None)
        if None in [username, password]:
            abort(400)

        req_json["password"] = get_hash(password)

        user_ = UserSchema().load(req_json)
        new_user = User(**user_)
        with db.session.begin():
            db.session.add(new_user)
        return "", 201



@user_ns.route('/<int:user_id>')
class UserView(Resource):
    def get(self, user_id):
        r = db.session.query(User).get(user_id)
        sm_d = UserSchema().dump(r)
        return sm_d, 200

    def put(self, user_id):
        user_selected = db.session.query(User).filter(User.id == user_id)
        user_first = user_selected.first()

        if user_first is None:
            return "", 404

        req_json = request.json

        if "password" in req_json:
            req_json["password"] = get_hash(req_json["password"])

        user_selected.update(req_json)
        db.session.commit()
        return "", 204

    def delete(self, user_id):
        user_selected = db.session.query(User).filter(User.id == user_id)
        user_first = user_selected.first()

        if user_first is None:
            return "", 404

        rows_deleted = user_selected.delete()
        if rows_deleted != 1:
            return "", 400

        db.session.commit()
        return "", 204