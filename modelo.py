from conexion import db,app

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_evento = db.Column(db.String(20), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    # Agrega campos adicionales según tus necesidades
    campo_adicional_1 = db.Column(db.String(50))
    campo_adicional_2 = db.Column(db.String(50))

    def __init__(self, tipo_evento, descripcion, fecha, estado, campo_adicional_1=None, campo_adicional_2=None):
        self.tipo_evento = tipo_evento
        self.descripcion = descripcion
        self.fecha = fecha
        self.estado = estado
        self.campo_adicional_1 = campo_adicional_1
        self.campo_adicional_2 = campo_adicional_2

    def __repr__(self):
        return f"Evento(id={self.id}, tipo_evento={self.tipo_evento}, fecha={self.fecha}, estado={self.estado})"
    
    
    

