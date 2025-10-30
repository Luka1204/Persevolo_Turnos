from .PersevoloORM.Model import Model

class Profesional(Model):
    _fields = ['id', 'nombre', 'apellido', 'dni', 'cuil', 'atenciones']
    _filename = 'profesionales.csv'