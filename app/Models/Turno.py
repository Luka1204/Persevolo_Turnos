from .PersevoloORM import Model

class Turno(Model):
    _fields = ['nro_turno', 'fecha', 'hora', 'nro_cliente', 'dia', 'nro_profesional','nro_cliente']
    _filename = 'turnos.csv'