from datetime import datetime
from flask import Flask, jsonify,request,Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import pymongo

#iniciando flask 1
app = Flask(__name__)

#conexión a base de datos:
app.config['MONGO_URI'] = 'mongodb://localhost:27017/disneydb'
mongo = PyMongo(app)

#rutas characters

#método POST: crea un personaje
@app.route('/characters', methods=['POST'])
def create_character():
    #.almaceno en variables los datos recibidos a través de request.json
    #.compruebo que existan los datos name,movie,series
    #.hago un insert en la base de datos de mongo en la colección characters
    #. creo una response con texto a retornar -> retorno la response
    #. en caso de que no existan los atributos del if se devuelve un mensaje de error
    name = request.json['name']
    age = request.json['age']
    weight = request.json['weight']
    desc = request.json['desc']
    movies = request.json['movies']
    series = request.json['series']
    image = request.json['image']
    if name and movies and series:
        mongo.db.characters.insert_one({
            "name":name,
            "age":age,
            "weight":weight,
            "desc":desc,
            "movies":movies,
            "series":series,
            "image":image
        })
        response=jsonify({"Message":"Character "+name+" created sucessfully"})
        return response
    else:
        return page_not_found("")


#método PUT: reemplaza por completo los atributos de un personaje
@app.route('/characters/<id>', methods=['PUT'])
def update_character(id):
    #.la ruta posee una variable id que indicará el id del personaje
    #a cambiar, y por parámetro se recibe este id
    #.se almacena todos los datos ingresados y luego se realiza
    #la peticion muy parecida al post, solo que usando el metodo update_one
    #en los parametros indicamos la id del personaje y luego los datos a cambiar
    name = request.json['name']
    age = request.json['age']
    weight = request.json['weight']
    desc = request.json['desc']
    movies = request.json['movies']
    series = request.json['series']
    image = request.json['image']
    if name and movies and series:
        mongo.db.characters.update_one({"_id":ObjectId(id)},{"$set":{
            "name":name,
            "age":age,
            "weight":weight,
            "desc":desc,
            "movies":movies,
            "series":series,
            "image":image
        }})
        response=jsonify({"Message":"Character with id "+id+" updated sucessfully"})
        return response
    else:
        return page_not_found("")


#método DELETE: elimina un personaje
@app.route('/characters/<id>', methods=['DELETE'])
def delete_character(id):
    #.recibo por url la id del personaje a eliminar y realizo la petición en la db
    mongo.db.characters.delete_one({'id':ObjectId(id)})
    response = jsonify({
        'message':'Character ' + id + ' was deleted succesfully'
    })
    return response


#método GET: obtiene todos los personajes
@app.route('/characters', methods=['GET'])
def show_characters():
    #.almaceno en 'characters' la petición de obtener todos los personajes
    #.almaceno en 'response' los personajes formateados en json
    #.retorno una instancia de la clase Response con la variable
    #'response' y el mimetype de application/json
    characters = mongo.db.characters.find({},{"name":1,"image":1,"_id":0}).sort("name",pymongo.ASCENDING)
    response = json_util.dumps(characters)
    return Response(response,mimetype='application/json')

#método GET: obtiene todos los datos de un personaje en particular
@app.route('/characters/<id>', methods=['GET'])
def show_character_detail(id):
    character = mongo.db.characters.find_one_or_404({"_id":ObjectId(id)},{"_id":0})
    response = json_util.dumps(character)
    return Response(response,mimetype="application/json")

#método GET: filtra los personajes por la pelicula indicada
@app.route('/characters/search/<string:movie>', methods=['GET'])
def show_filtered_characters_by_name(movie):
    movie = mongo.db.characters.find({"movies":movie},{"_id":0})
    response = json_util.dumps(movie)
    return Response(response,mimetype="application/json")

#método GET: filtra los personajes por la edad
@app.route('/characters/search/<int:age>', methods=['GET'])
def show_filtered_characters_by_age(age):
    print(type(age))
    character = mongo.db.characters.find({"age":age},{"_id":0})
    response = json_util.dumps(character)
    return Response(response,mimetype="application/json")


#rutas movies

#/método POST: crea una pelicula
@app.route('/movies', methods=['POST'])
def create_movies():
    #creo un objeto de tipo datetime para la fecha ingresada por json (dd/mm/year)
    title = request.json['title']
    creation_date = datetime.strptime(request.json['creation_date'],"%d/%m/%Y")
    rate = request.json['rate']
    characters = request.json['characters']
    genre = request.json['genre']
    image = request.json['image']
    if title and creation_date:
        mongo.db.movies.insert_one({
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
        return page_not_found("")


#método PUT: reemplaza por completo los atributos de una pelicula
@app.route('/movies/<id>', methods=['PUT'])
def update_movie(id):
    title = request.json['title']
    creation_date = datetime.strptime(request.json['creation_date'],"%d/%m/%Y")
    rate = request.json['rate']
    characters = request.json['characters']
    genre = request.json['genre']
    image = request.json['image']
    if title and creation_date:
        mongo.db.movies.update_one({"_id":ObjectId(id)},{"$set":{
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
        return page_not_found("")


#método DELETE: elimina una pelicula
@app.route('/movies/<id>', methods=['DELETE'])
def delete_movies(id):
    mongo.db.movies.delete_one({'id':ObjectId(id)})
    response = jsonify({
        'message':'Movie with id: ' + id + ' was deleted succesfully'
    })
    return response


#método GET: obtiene todas las peliculas
@app.route('/movies', methods=['GET'])
def show_movies():
    movies= mongo.db.movies.find({},{"title":1,"creation_date":1,"image":1})
    response = json_util.dumps(movies)
    return Response(response,mimetype='application/json')

#método GET: obtiene los datos de una pelicula por id
@app.route('/movies/<id>', methods=['GET'])
def show_movie(id):
    movie = mongo.db.movies.find({"_id":ObjectId(id)})
    response = json_util.dumps(movie)
    return Response(response,mimetype='application/json')

#método GET: recibe un género y muestra todas las películas que coincidan con este
@app.route('/movies/search/<string:genre>', methods=['GET'])
def show_movie_by_genre(genre):
    movie = mongo.db.movies.find({"genre":genre})
    response = json_util.dumps(movie)
    return Response(response,mimetype='application/json')


#método GET: recibe un orden (asc o desc) y los ordena por fecha en base a lo indicado
@app.route('/movies/order/<string:order>',methods=['GET'])
def show_movies_ordered(order):
    if order:
        if order=='asc':
            moviesAsc= mongo.db.movies.find({},{"title":1,"creation_date":1,"image":1}).sort("creation_date",pymongo.ASCENDING)
            response = json_util.dumps(moviesAsc)
            return Response(response,mimetype='application/json')
        if order=='desc':
            moviesDesc= mongo.db.movies.find({},{"title":1,"creation_date":1,"image":1}).sort("creation_date",pymongo.DESCENDING)
            response = json_util.dumps(moviesDesc)
            return Response(response,mimetype='application/json')
        else:
            return page_not_found


#rutas generos

#método POST: crea una pelicula
@app.route('/genres', methods=['POST'])
def create_genre():
    name = request.json['name']
    movies = request.json['movies']
    series = request.json['series']
    image = request.json['image']
    if name and (movies or series):
        mongo.db.genres.insert_one({
            "name":name,
            "movies":movies,
            "series":series,
            "image":image
        })
        response=jsonify({"Message":"Genre "+name+" created sucessfully"})
        return response
    else:
        return page_not_found("")


#método PUT: reemplaza por completo los atributos de un genero
@app.route('/genres/<id>', methods=['PUT'])
def update_genre(id):
    name = request.json['name']
    movies = request.json['movies']
    series = request.json['series']
    image = request.json['image']
    if name and (movies or series):
        mongo.db.genres.update_one({"_id":ObjectId(id)},{"$set":{
            "name":name,
            "movies":movies,
            "series":series,
            "image":image
        }})
        response=jsonify({"Message":"Genre "+name+" updated sucessfully"})
        return response
    else:
        return page_not_found("")


#método DELETE: elimina un genero
@app.route('/genres/<id>', methods=['DELETE'])
def delete_genre(id):
    mongo.db.genres.delete_one({'id':ObjectId(id)})
    response = jsonify({
        'message':'Genre with id: ' + id + ' was deleted succesfully'
    })
    return response


#método GET: obtiene todos los generos
@app.route('/genres', methods=['GET'])
def show_genres():
    genres = mongo.db.genres.find()
    response = json_util.dumps(genres)
    return Response(response,mimetype='application/json')


#error handler
@app.errorhandler(404)
def page_not_found(error):
    return error, 404

#flask 2
if __name__ == "__main__":
    app.run(debug=True)