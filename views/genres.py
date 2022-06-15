from flask_restx import Resource, Namespace
from flask import request
from models import Genre, GenreSchema
from setup_db import db
from utils import auth_required, admin_required

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = db.session.query(Genre).all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        new_data = request.json

        genre_ = GenreSchema().load(new_data)
        new_genre = Genre(**genre_)
        with db.session.begin():
            db.session.add(new_genre)

        return "", 201


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        r = db.session.query(Genre).get(gid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, gid):
        genre_selected = db.session.query(Genre).filter(Genre.id == gid)
        genre_first = genre_selected.first()

        if genre_first is None:
            return "", 404

        new_data = request.json
        genre_selected.update(new_data)
        db.session.commit()

        return "", 204

    @admin_required
    def delete(self, gid):
        genre_selected = db.session.query(Genre).filter(Genre.id == gid)
        genre_first = genre_selected.first()

        if genre_first is None:
            return "", 404

        rows_deleted = genre_selected.delete()
        if rows_deleted != 1:
            return "", 400

        db.session.commit()
        return "", 204