# Здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки).
# Сюда импортируются сервисы из пакета service.

from flask import request
from flask_restx import Resource, Namespace

from container import movie_dao
from dao.model.movies import MovieSchema


movies_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route('/')
class MoviesView(Resource):

    def get(self):
        data = movie_dao.get_all()
        result = movies_schema.dump(data)
        return result, 200

    def post(self):
        request_data = request.json
        new_movie = movie_dao.create(request_data)
        result = movie_schema.dump(new_movie)
        return result, 201


@movies_ns.route('/<int:mov_id>')
class MovieView(Resource):

    def get(self, mov_id: int):
        data = movie_dao.get_one(mov_id)
        result = movie_schema.dump(data)
        return result, 200

    def put(self, mov_id: int):
        request_data = request.json
        result_data = movie_dao.update(mov_id, request_data)
        result = movie_schema.dump(result_data)
        return result, 200

    def patch(self, mov_id: int):
        request_data = request.json
        result_data = movie_dao.update_partial(mov_id, request_data)
        result = movie_schema.dump(result_data)
        return result, 200

    def delete(self, mov_id: int):
        movie_dao.delete(mov_id)
        return f"Data ID: {mov_id} was deleted successfully.", 200