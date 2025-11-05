from .PersevoloORM.Model import Model

class Profesional(Model):
    _fields = ['id', 'nombre', 'apellido', 'dni', 'cuil']
    _filename = 'profesionales.csv'