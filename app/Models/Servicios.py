from .PersevoloORM import Model

class Servicios(Model):
    _fields = ['nro_servicio', 'nombre', 'duracion', 'precio']
    _filename = 'servicios.csv'