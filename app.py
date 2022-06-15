from flask import Flask
from flask_pymongo import PyMongo


#iniciando flask 1
app = Flask(__name__)

#conexión a base de datos:
app.config['MONGO_URI'] = 'mongodb://localhost:27017/disneydb'
mongo = PyMongo(app)

#error handler
@app.errorhandler(404)
def page_not_found(error):
    return error, 404

#registrando los blueprints
import characters_routes
import movies_routes
import genres_routes
app.register_blueprint(characters_routes.characters)
app.register_blueprint(movies_routes.movies)
app.register_blueprint(genres_routes.genres)

#flask 2
if __name__ == "__main__":
    app.run(debug=True)

