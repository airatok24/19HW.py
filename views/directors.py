from flask_restx import Resource, Namespace
from flask import request
from models import Director, DirectorSchema
from setup_db import db
from utils import auth_required, admin_required

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = db.session.query(Director).all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        new_data = request.json

        director_ = DirectorSchema().load(new_data)
        new_director = Director(**director_)
        with db.session.begin():
            db.session.add(new_director)

        return "", 201



@director_ns.route('/<int:did>')
class DirectorView(Resource):
    @auth_required
    def get(self, did):
        r = db.session.query(Director).get(did)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, did):
        director_selected = db.session.query(Director).filter(Director.id == did)
        director_first = director_selected.first()

        if director_first is None:
            return "", 404

        new_data = request.json
        director_selected.update(new_data)
        db.session.commit()

        return "", 204

    @admin_required
    def delete(self, did):
        director_selected = db.session.query(Director).filter(Director.id == did)
        director_first = director_selected.first()

        if director_first is None:
            return "", 404

        rows_deleted = director_selected.delete()
        if rows_deleted != 1:
            return "", 400

        db.session.commit()
        return "", 204