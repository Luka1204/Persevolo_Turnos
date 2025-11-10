from .PersevoloORM.Model import Model


class Turno(Model):
    # Ahora Turno está asociado a una Atencion (que contiene el servicio).
    # Campos: id, fecha, hora, cliente_id (puede estar vacío si está disponible),
    # profesional_id, atencion_id, estado
    _fields = ['id', 'fecha', 'hora', 'cliente_id', 'profesional_id', 'atencion_id', 'estado']
    _filename = 'turnos.csv'

    # Si en el futuro se desea añadir lógica específica para Turno, puede añadirse aquí
                