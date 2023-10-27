# Guía para Levantar una API Flask en Ambiente Local con Base de Datos PostgreSQL

Esta guía te ayudará a configurar y ejecutar una API Flask en tu entorno local y crear una base de datos PostgreSQL llamada "eventos" con credenciales personalizadas. Asegúrate de tener Python y PostgreSQL instalados antes de comenzar.

## Paso 1: Preparación del Entorno

1. **Instalar Python:** Si no tienes Python instalado, descárgalo e instálalo desde [python.org](https://www.python.org/downloads/).

2. **Instalar PostgreSQL:** Descarga e instala PostgreSQL desde el [sitio oficial](https://www.postgresql.org/download/).

## Paso 2: Configuración de la Base de Datos

3. **Crear una Base de Datos:** Abre la consola de PostgreSQL y ejecuta los siguientes comandos para crear una base de datos llamada "eventos":

   ```sql
   CREATE DATABASE eventos;



## Paso 2: EJECUTAR LA API

1. **Descargar las dependencias:** Dentro de la raiz de la aplicacion ejecutar el comando pip install -r requirements.txt para descargar las librerias necesarias.

2. **Cambiar las credenciales de la BD:** Dentro del archivo conexion.py cambiar credenciales de acceso a la BD

3. **Ejecutar comando de ejecución:** Dentro de la raiz del proyecto ejecutar el comando flask run o python /app.py


## Paso 3: ENDPOINTS

1. **Endpoints peticiones http:**   La url cuando se ejecuta la aplicacon en local es localhost:5000 y sus distintos endpoins son:

     Obtener todos los eventos:
        URL: /events
        GET: Obtener una lista de todos los eventos en la base de datos.

    Crear un nuevo evento:
        URL: /events
        POST: Agregar un nuevo evento proporcionando datos en formato JSON.

    Obtener un evento por su ID:
        URL: /events/<event_id>
        GET: Obtener información detallada de un evento específico por su ID.

    Actualizar un evento por su ID:
        URL: /events/<event_id>
        PUT: Editar un evento existente proporcionando datos actualizados en formato JSON.

    Eliminar un evento por su ID:
        URL: /events/<event_id>
        DELETE: Eliminar un evento específico por su ID.


1. **Endpoints Swagger:** Desde el endpoint http://localhost:5000/api/docs/  se puede revisar la documentación de la api
y ejecutas las distintaciones peticiones http.


## Paso 4: DOCKERFILE

1. **Ejecutar contenedor docker:**  Con el comando dentro de la raiz del proyecto docker build -t nombre_de_la_imagen .
se crea un una imagen docker de la api, para ejecutarla con el comando docker run -p 5000:5000 nombre_de_la_imagen
Esto mapeará el puerto 5000 del contenedor al puerto 5000 de tu sistema local para que puedas acceder a tu aplicación Flask en http://localhost:5000.