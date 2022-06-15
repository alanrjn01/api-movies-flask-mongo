from datetime import datetime
from flask import jsonify,request,Response,Blueprint
from bson import json_util
from bson.objectid import ObjectId
import pymongo
movies = Blueprint('movies', __name__)
import app

#/método POST: crea una pelicula
@movies.route('/movies', methods=['POST'])
def create_movies():
    #creo un objeto de tipo datetime para la fecha ingresada por json (dd/mm/year)
    title = request.json['title']
    creation_date = datetime.strptime(request.json['creation_date'],"%d/%m/%Y")
    rate = request.json['rate']
    characters = request.json['characters']
    genre = request.json['genre']
    image = request.json['image']
    if title and creation_date:
        app.mongo.db.movies.insert_one({
            "title":title,
            "creation_date":creation_date,
            "rate":rate,
            "characters":characters,
            "genre":genre,
            "image":image
        })
        response=jsonify({"Message":"Movie "+title+" created sucessfully"})
        return response
    else:
        return app.page_not_found("")


#método PUT: reemplaza por completo los atributos de una pelicula
@movies.route('/movies/<id>', methods=['PUT'])
def update_movie(id):
    title = request.json['title']
    creation_date = datetime.strptime(request.json['creation_date'],"%d/%m/%Y")
    rate = request.json['rate']
    characters = request.json['characters']
    genre = request.json['genre']
    image = request.json['image']
    if title and creation_date:
        app.mongo.db.movies.update_one({"_id":ObjectId(id)},{"$set":{
            "title":title,
            "creation_date":creation_date,
            "rate":rate,
            "characters":characters,
            "genre":genre,
            "image":image
        }})
        response=jsonify({"Message":"Movie "+title+" updated sucessfully"})
        return response
    else:
        return app.page_not_found("")


#método DELETE: elimina una pelicula
@movies.route('/movies/<id>', methods=['DELETE'])
def delete_movies(id):
    app.mongo.db.movies.delete_one({'id':ObjectId(id)})
    response = jsonify({
        'message':'Movie with id: ' + id + ' was deleted succesfully'
    })
    return response


#método GET: obtiene todas las peliculas
@movies.route('/movies', methods=['GET'])
def show_movies():
    movies= app.mongo.db.movies.find({},{"title":1,"creation_date":1,"image":1})
    response = json_util.dumps(movies)
    return Response(response,mimetype='application/json')

#método GET: obtiene los datos de una pelicula por id
@movies.route('/movies/<id>', methods=['GET'])
def show_movie(id):
    movie = app.mongo.db.movies.find({"_id":ObjectId(id)})
    response = json_util.dumps(movie)
    return Response(response,mimetype='application/json')

#método GET: recibe un género y muestra todas las películas que coincidan con este
@movies.route('/movies/search/<string:genre>', methods=['GET'])
def show_movie_by_genre(genre):
    movie = app.mongo.db.movies.find({"genre":genre})
    response = json_util.dumps(movie)
    return Response(response,mimetype='application/json')


#método GET: recibe un orden (asc o desc) y los ordena por fecha en base a lo indicado
@movies.route('/movies/order/<string:order>',methods=['GET'])
def show_movies_ordered(order):
    if order:
        if order=='asc':
            moviesAsc= app.mongo.db.movies.find({},{"title":1,"creation_date":1,"image":1}).sort("creation_date",pymongo.ASCENDING)
            response = json_util.dumps(moviesAsc)
            return Response(response,mimetype='application/json')
        if order=='desc':
            moviesDesc= app.mongo.db.movies.find({},{"title":1,"creation_date":1,"image":1}).sort("creation_date",pymongo.DESCENDING)
            response = json_util.dumps(moviesDesc)
            return Response(response,mimetype='application/json')
        else:
            return app.page_not_found("")

