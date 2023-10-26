from flask import Flask, request, jsonify
from conexion import db,app  # Importa 'db' desde 'conexion.py'
from modelo import Evento  # Importa el modelo Evento
from sqlalchemy.exc import NoSuchTableError
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy import text
from flask_swagger_ui import get_swaggerui_blueprint
import psycopg2


db_uri = "postgresql://postgres:fredy555@localhost/eventos"



SWAGGER_URL = '/api/docs'  # La URL donde se servirá la documentación Swagger
API_URL = '/static/swagger.json'  # La URL de la especificación Swagger JSON

# Crea una instancia de SwaggerUI y especifica las rutas
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # La URL de Swagger UI
    API_URL,
    config={  # Configuración de Swagger UI
        'app_name': "Mi API"  
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)





db_params = {
    'dbname': 'eventos',     # Nombre de la base de datos
    'user': 'postgres',      # Usuario de PostgreSQL
    'password': 'fredy555',  # Contraseña
    'host': 'localhost',     # Host donde se encuentra la base de datos
    'port': '5432'           # Puerto de PostgreSQL
}

# Establecer la conexión a la base de datos
db_connection = psycopg2.connect(**db_params)

# Crear la tabla "evento" si no existe
with db_connection.cursor() as cursor:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evento (
            id SERIAL PRIMARY KEY,
            tipo_evento VARCHAR(50),
            descripcion TEXT,
            fecha DATE,
            estado VARCHAR(20),
            campo_adicional_1 VARCHAR(50),
            campo_adicional_2 VARCHAR(50)
        )
    ''')

# Agregar registros por defecto si la tabla está vacía
with db_connection.cursor() as cursor:
    cursor.execute('SELECT COUNT(*) FROM evento')
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute('''
            INSERT INTO evento (tipo_evento, descripcion, fecha, estado, campo_adicional_1, campo_adicional_2) VALUES
            ('Evento tipo 1', 'Descripción 1', '2023-10-24', 'Revisado', 'Campo 1 Valor', 'Campo 2 Valor'),
            ('Evento tipo 2', 'Descripción 2', '2023-10-25', 'Pendiente', 'Campo 1 Valor', 'Campo 2 Valor'),
            ('Evento tipo 3', 'Descripción 3', '2023-10-26', 'Revisado', 'Campo 1 Valor', 'Campo 2 Valor')
        ''')
    db_connection.commit()




def load_initial_records(engine):
    with engine.connect() as connection:
        # Verifica si ya hay registros en la tabla "evento"
        query = text("SELECT COUNT(*) FROM evento")
        count = connection.execute(query).scalar()

        if count == 0:
            # Si no hay registros, carga los datos iniciales desde el archivo SQL
            with open("data.sql") as sql_file:
                sql_statements = sql_file.read()
                connection.execute(text(sql_statements))
            print("Registros iniciales insertados en la base de datos.")
        else:
            print("La base de datos ya contiene registros, no se insertaron registros iniciales.")



# Llama a la función con la URL de tu base de datos


engine = create_engine(db_uri)
load_initial_records(engine)



# Define una ruta para crear la tabla y algunos registros automáticamente
@app.route('/crear_tabla_y_registros', methods=['GET'])
def crear_tabla_y_registros():
    try:
        # Intenta acceder a la tabla, esto lanzará una excepción si la tabla no existe
        db.session.query(Evento).first()
        tabla_existe = True
    except NoSuchTableError:
        tabla_existe = False

    if not tabla_existe:
        # Si la tabla no existe, crea la tabla
        with app.app_context():
            db.create_all()

            # Agrega algunos eventos de ejemplo a la tabla
            eventos_ejemplo = [
                Evento(tipo_evento='Evento tipo 1', descripcion='Descripción 1', fecha='2023-10-24', estado='Revisado'),
                Evento(tipo_evento='Evento tipo 2', descripcion='Descripción 2', fecha='2023-10-25', estado='Pendiente'),
                Evento(tipo_evento='Evento tipo 3', descripcion='Descripción 3', fecha='2023-10-26', estado='Revisado'),
            ]

            for evento in eventos_ejemplo:
                db.session.add(evento)

            db.session.commit()
            return 'Tabla y registros creados automáticamente.'
    else:
        return "La tabla ya existe en la base de datos."


# Función para verificar la conexión a la base de datos
def verificar_conexion_db():
    try:
        with db.engine.connect():
            return True
    except Exception as e:
        return str(e)
    
    


# Ruta para verificar la conexión a la base de datos
@app.route('/verificar_conexion_db')
def verificar_conexion():
    resultado = verificar_conexion_db()
    if resultado is True:
        return 'Conexión exitosa a la base de datos PostgreSQL.'
    else:
        return f'Error de conexión a la base de datos: {resultado}'
    
    

# Crea las tablas si no existen
with app.app_context():
    db.create_all()


# ...

# Ruta para obtener todos los eventos desde la base de datos
@app.route('/events', methods=['GET'])
def get_events():
    try:
        # Consulta la base de datos para obtener todos los eventos
        eventos = db.session.query(Evento).all()

        # Convierte los objetos Evento en un formato JSON para la respuesta
        eventos_json = [
            {
                'id': evento.id,
                'tipo_evento': evento.tipo_evento,
                'descripcion': evento.descripcion,
                'fecha': evento.fecha.isoformat(),  # Convierte la fecha a formato ISO
                'estado': evento.estado,
                # Agrega campos adicionales según tus necesidades
                'campo_adicional_1': evento.campo_adicional_1,
                'campo_adicional_2': evento.campo_adicional_2,
            }
            for evento in eventos
        ]

        return jsonify(eventos_json), 200
    except Exception as e:
        return f'Error al obtener eventos desde la base de datos: {str(e)}', 500



# Ruta para agregar un evento a la base de datos
@app.route('/events', methods=['POST'])
def create_event():
    try:
        data = request.get_json()
        nuevo_evento = Evento(
            tipo_evento=data.get('tipo_evento'),
            descripcion=data.get('descripcion'),
            fecha=data.get('fecha'),
            estado=data.get('estado'),
            campo_adicional_1=data.get('campo_adicional_1'),
            campo_adicional_2=data.get('campo_adicional_2')
        )

        db.session.add(nuevo_evento)
        db.session.commit()

        respuesta = {'mensaje': f'Evento agregado con ID: {nuevo_evento.id}'}
        return jsonify(respuesta), 201
    except Exception as e:
        respuesta = {'mensaje': f'Error al agregar el evento: {str(e)}'}
        return jsonify(respuesta), 500
    
    
# Ruta para obtener un evento por su ID
@app.route('/events/<int:event_id>', methods=['GET'])
def get_event_by_id(event_id):
    try:
        evento = db.session.query(Evento).get(event_id)

        if evento:
            evento_json = {
                'id': evento.id,
                'tipo_evento': evento.tipo_evento,
                'descripcion': evento.descripcion,
                'fecha': evento.fecha.isoformat(),
                'estado': evento.estado,
                'campo_adicional_1': evento.campo_adicional_1,
                'campo_adicional_2': evento.campo_adicional_2
            }
            return jsonify(evento_json), 200
        else:
            return jsonify({'mensaje': 'Evento no encontrado'}), 404
    except Exception as e:
        return jsonify({'mensaje': f'Error al obtener el evento: {str(e)}'}), 500


# Ruta para editar un evento por su ID
@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    try:
        data = request.get_json()
        evento = db.session.query(Evento).get(event_id)

        if not evento:
            return jsonify({'mensaje': 'Evento no encontrado'}), 404

        evento.tipo_evento = data.get('tipo_evento')
        evento.descripcion = data.get('descripcion')
        evento.fecha = data.get('fecha')
        evento.estado = data.get('estado')
        evento.campo_adicional_1 = data.get('campo_adicional_1')
        evento.campo_adicional_2 = data.get('campo_adicional_2')

        db.session.commit()

        respuesta = {'mensaje': 'Evento actualizado exitosamente'}
        return jsonify(respuesta), 200
    except Exception as e:
        respuesta = {'mensaje': f'Error al editar el evento: {str(e)}'}
        return jsonify(respuesta), 500

# Ruta para eliminar un evento por su ID
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    try:
        evento = db.session.query(Evento).get(event_id)

        if not evento:
            return jsonify({'mensaje': 'Evento no encontrado'}), 404

        db.session.delete(evento)
        db.session.commit()

        respuesta = {'mensaje': 'Evento eliminado exitosamente'}
        return jsonify(respuesta), 204  # 204 significa "No Content" para indicar que la eliminación fue exitosa
    except Exception as e:
        respuesta = {'mensaje': f'Error al eliminar el evento: {str(e)}'}
        return jsonify(respuesta), 500

if __name__ == '__main__':
    app.run(debug=True)
