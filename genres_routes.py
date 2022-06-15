from flask import jsonify,request,Response,Blueprint
from bson import json_util
from bson.objectid import ObjectId
genres = Blueprint('genres', __name__)
import app

#método POST: crea una pelicula
@genres.route('/genres', methods=['POST'])
def create_genre():
    name = request.json['name']
    movies = request.json['movies']
    series = request.json['series']
    image = request.json['image']
    if name and (movies or series):
        app.mongo.db.genres.insert_one({
            "name":name,
            "movies":movies,
            "series":series,
            "image":image
        })
        response=jsonify({"Message":"Genre "+name+" created sucessfully"})
        return response
    else:
        return app.page_not_found("")


#método PUT: reemplaza por completo los atributos de un genero
@genres.route('/genres/<id>', methods=['PUT'])
def update_genre(id):
    name = request.json['name']
    movies = request.json['movies']
    series = request.json['series']
    image = request.json['image']
    if name and (movies or series):
        app.mongo.db.genres.update_one({"_id":ObjectId(id)},{"$set":{
            "name":name,
            "movies":movies,
            "series":series,
            "image":image
        }})
        response=jsonify({"Message":"Genre "+name+" updated sucessfully"})
        return response
    else:
        return app.page_not_found("")


#método DELETE: elimina un genero
@genres.route('/genres/<id>', methods=['DELETE'])
def delete_genre(id):
    app.mongo.db.genres.delete_one({'id':ObjectId(id)})
    response = jsonify({
        'message':'Genre with id: ' + id + ' was deleted succesfully'
    })
    return response


#método GET: obtiene todos los generos
@genres.route('/genres', methods=['GET'])
def show_genres():
    genres = app.mongo.db.genres.find()
    response = json_util.dumps(genres)
    return Response(response,mimetype='application/json')

