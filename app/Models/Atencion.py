from .PersevoloORM.Model import Model

class Atencion(Model):
    _fields = ['id', 'hora_desde', 'hora_hasta', 'dia', 'id_servicio', 'cantidad']
    _filename = 'atenciones.csv'