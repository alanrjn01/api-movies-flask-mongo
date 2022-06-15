from flask import jsonify, render_template,request,Response,Blueprint
from bson import json_util
from bson.objectid import ObjectId
import pymongo
characters = Blueprint('characters', __name__)
import app 
#rutas characters

#método POST: crea un personaje
@characters.route('/characters', methods=['POST'])
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
    if name and (movies or series):
        app.mongo.db.characters.insert_one({
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
        return app.page_not_found("")


#método PUT: reemplaza por completo los atributos de un personaje
@characters.route('/characters/<id>', methods=['PUT'])
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
        app.mongo.db.characters.update_one({"_id":ObjectId(id)},{"$set":{
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
        return app.page_not_found("")


#método DELETE: elimina un personaje
@characters.route('/characters/<id>', methods=['DELETE'])
def delete_character(id):
    #.recibo por url la id del personaje a eliminar y realizo la petición en la db
    app.mongo.db.characters.delete_one({'_id':ObjectId(id)})
    response = jsonify({
        'message':'Character ' + id + ' was deleted succesfully'
    })
    return response


#método GET: obtiene todos los personajes
@characters.route('/characters', methods=['GET'])
def show_characters():
    #.almaceno en 'characters' la petición de obtener todos los personajes
    #.almaceno en 'response' los personajes formateados en json
    #.retorno una instancia de la clase Response con la variable
    #'response' y el mimetype de application/json
    characters = app.mongo.db.characters.find({},{"name":1,"image":1,"_id":0}).sort("name",pymongo.ASCENDING)
    return render_template('characters.html', data = characters)

#método GET: obtiene todos los datos de un personaje en particular
@characters.route('/characters/<id>', methods=['GET'])
def show_character_detail(id):
    character = app.mongo.db.characters.find_one_or_404({"_id":ObjectId(id)},{"_id":0})
    response = json_util.dumps(character)
    return Response(response,mimetype="application/json")

#método GET: filtra los personajes por la pelicula indicada
@characters.route('/characters/search/<string:movie>', methods=['GET'])
def show_filtered_characters_by_name(movie):
    movie = app.mongo.db.characters.find({"movies":movie},{"_id":0})
    response = json_util.dumps(movie)
    return Response(response,mimetype="application/json")

#método GET: filtra los personajes por la edad
@characters.route('/characters/search/<int:age>', methods=['GET'])
def show_filtered_characters_by_age(age):
    print(type(age))
    character = app.mongo.db.characters.find({"age":age},{"_id":0})
    response = json_util.dumps(character)
    return Response(response,mimetype="application/json")

