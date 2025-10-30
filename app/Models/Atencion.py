from .PersevoloORM.Model import Model

class Atencion(Model):
    _fields = ['id', 'hora_desde', 'hora_hasta', 'dia', 'id_servicio', 'cantidad']
    _filename = 'atenciones.csv'

    def __str__(self):
        """Representación personalizada para Atencion"""
        return f"Atencion {self.id}: {self.hora_desde} ({self.hora_hasta}) {self.nro_servicio}"