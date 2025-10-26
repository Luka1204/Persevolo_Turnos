from .PersevoloORM import Model
class Cliente(Model):
    _fields = ['nro_cliente', 'nombre', 'apellido', 'dni', 'email', 'telefono']
    _filename = 'clientes.csv'

    """ def __init__(self, **kwargs):
        super().__init__(**kwargs)
            writer.writeheader()
            for obj in objects:
                writer.writerow(obj.to_dict())
                writer.flush()
                os.fsync(writer.fileno())
        for field in self._fields:
            setattr(self, field, kwargs.get(field)) """

