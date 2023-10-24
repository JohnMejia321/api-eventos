from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista de eventos de ejemplo (simulación de base de datos)
events = []

@app.route('/events', methods=['GET'])
def list_events():
    return jsonify(events), 200

@app.route('/events/<int:event_id>', methods=['GET'])
def get_event_by_id(event_id):
    event = next((event for event in events if event['id'] == event_id), None)
    if event:
        return jsonify(event), 200
    return "Evento no encontrado", 404

@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    event = {
        'id': len(events) + 1,
        'tipo_evento': data.get('tipo_evento'),
        'descripcion': data.get('descripcion'),
        'fecha': data.get('fecha'),
        'estado': data.get('estado'),
    }
    events.append(event)
    return jsonify(event), 201

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
