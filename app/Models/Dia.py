from .PersevoloORM.Model import Model

class Dia(Model):
    _fields = ['id', 'nombre']
    _filename = 'dias.csv'