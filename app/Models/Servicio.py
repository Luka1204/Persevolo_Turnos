from .PersevoloORM.Model import Model

class Servicio(Model):
    _fields = ['id', 'nombre', 'duracion', 'precio']
    _filename = 'servicios.csv'