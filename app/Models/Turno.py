from .PersevoloORM import Model

class Turno(Model):
    _fields = ['nro_turno', 'fecha', 'hora', 'nro_cliente', 'dia', 'nro_profesional','nro_cliente']
    _filename = 'turnos.csv'

""" class RegistrarTurno():
    def __init__(self):
        self.turnos == []

    def reserva_turno(self,nro_cliente,fecha,hora,nro_turno,dia,nro_profesional):
        for turno in self.turnos:
            if turno.fecha == fecha and turno.hora == hora:
                print('Reservado')
        

    def mostrar_turno(self): """
                