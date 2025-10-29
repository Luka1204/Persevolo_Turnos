from PersevoloORM import Model 

class Atencion(Model):
    _fields = ['nro_atencion', 'hora_desde', 'hora_hasta', 'dia', 'nro_servicio', 'cantidad']
    _filename = 'atenciones.csv'

    def __str__(self):
        """Representación personalizada para Atencion"""
        return f"Atencion {self.nro_atencion}: {self.hora_desde} ({self.hora_hasta}) {self.nro_servicio}"