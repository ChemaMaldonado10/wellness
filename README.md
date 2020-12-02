PRUEBA TÉCNICA - BACKEND - WELLNESS.

Se ha desarrollado una API en el microframework Flask para la base de datos se ha usado MariaDB (se puede instalar siguiendo los pasos de este enlace: https://www.digitalocean.com/community/tutorials/how-to-install-mariadb-on-ubuntu-20-04-es) 

Como parte obligatoria de esta prueba se ha implementado:

-> La importación desde un fichero CSV (report.csv) de la información hacia una base de datos (MariaDB).
    Se ha implementado en el propio servidor un endpoint ("/import_csv") para la automatización de:
        - Creación de la base de datos.
        - Creación de la tabla utilizada.
        - Inserción de valores desde el CSV.

    De este apartado se detalla que:
        - El csv contenía algunos espacios en blanco y se ha reemplazado por el valor 0.000.
        - El formato de fecha está establecido como VARCHAR(20) para una mayor agilidad en la prueba 
            pero se podría establecer como DATETIME o TIMESTAMP.

-> Respecto a la exposición de datos de la API:
    Se han creado dos endpoints "generales":
        - "/data_example":
            Con este endpoint obtendríamos los últimos datos almacenados asociados al último día en que se obtuvieron.
            (Esta parte haría referencia a la sección superior de la imagen proporcionada.)
        - "/graph_example":
            Con este endpoint obtendríamos todo el histórico de datos relacionados con una variable en concreto para la creación de gráficas.
            En este caso usamos la energía.
            (Esta parte haría referencia a la sección inferior de la imagen proporcionada.)


Como parte opcional de esta prueba se ha implementado:

-> Sistema de Auth mediante el uso de JWT (Json Web Tokens) que genera un token por usuario si las credenciales han sido correctas.
    Para ello se ha creado un endpoint "/login" que usa el método POST para recibir email y contraseña y en base a estos generar el token.

-> Sistema de caché bajo la ruta "/cache_example" que mediante un decorador @cache.cached(timeout) establece un tiempo de caché para la función
    que especifiquemos desde la ruta seleccionada.

-> No se han implementado test unitarios. 
    Sería interesante realizar algún test de conexión con base de datos ya que ésta es la acción que más se repite.


(Se adjuntan imágenes de los resultados obtenidos de cada uno de los endpoints en la carpeta img.)








