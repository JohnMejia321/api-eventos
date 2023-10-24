from flask import Flask, request, jsonify
from conexion import db,app  # Importa 'db' desde 'conexion.py'
from modelo import Evento  # Importa el modelo Evento
from sqlalchemy.exc import NoSuchTableError


# Lista de eventos de ejemplo (simulación de base de datos)
events = []

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

@app.route('/events/<int:event_id>', methods=['GET'])
def get_event_by_id(event_id):
    event = next((event for event in events if event['id'] == event_id), None)
    if event:
        return jsonify(event), 200
    return "Evento no encontrado", 404

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

        return f'Evento agregado con ID: {nuevo_evento.id}', 201
    except Exception as e:
        return f'Error al agregar el evento: {str(e)}', 500

@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event = next((event for event in events if event['id'] == event_id), None)
    if not event:
        return "Evento no encontrado", 404
    data = request.get_json()
    event['tipo_evento'] = data.get('tipo_evento')
    event['descripcion'] = data.get('descripcion')
    event['fecha'] = data.get('fecha')
    event['estado'] = data.get('estado')
    return jsonify(event), 200

@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = next((event for event in events if event['id'] == event_id), None)
    if not event:
        return "Evento no encontrado", 404
    events.remove(event)
    return "", 204

if __name__ == '__main__':
    app.run(debug=True)
