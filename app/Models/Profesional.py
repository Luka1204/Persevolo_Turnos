from .PersevoloORM import Model

class Profesional(Model):
    _fields = ['nro_profesional', 'nombre', 'apellido', 'dni', 'cuil', 'atenciones']
    _filename = 'profesionales.csv'