api creada con flask y mongodb para la base de datos.
contiene un crud(GET,POST,PUT,DELETE) para las colecciones:
* movies
* characters
* genres

# PUT y DELETE
ambas peticiones reciben un id a partir de la cual se podrá modificar o eliminar un documento
**coleccion = nombre de cualquiera de las 3 colecciones**
</coleccion/id>

# GET y POST
estas peticiones no requieren de un id
</coleccion>

### characters
</characters/id>
obtiene los datos de un personaje a través de su id
</characters/search/movie>
obtiene los personajes que participaron en la película buscada
</characters/search/age>
obtiene los personajes que coincidan con la edad especificada

### movies
</movies/id>
obtiene los datos de una pelicula a través de su id
</movies/search/<genre>
obtiene las peliculas que coincidan con el genero indicado
</movies/order/asc_or_desc>
se indica el orden deseado por el cual se quiere listar las peliculas en base a su fecha
* asc = ascendente
* desc = descendente 

