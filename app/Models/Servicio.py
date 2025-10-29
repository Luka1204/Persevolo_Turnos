from .PersevoloORM import Model

class Servicio(Model):
    _fields = ['nro_servicio', 'nombre', 'duracion', 'precio']
    _filename = 'servicios.csv'