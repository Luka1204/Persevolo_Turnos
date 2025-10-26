from PersevoloORM import Model 

class Atenciones(Model):
    _fields = ['nro_atencion', 'hora_desde', 'hora_hasta', 'dia', 'nro_servicio', 'cantidad']
    _filename = 'atenciones.csv'