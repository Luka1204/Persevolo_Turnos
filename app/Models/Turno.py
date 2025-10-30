from .PersevoloORM.Model import Model

class Turno(Model):
    _fields = ['id', 'fecha', 'hora', 'id_cliente', 'dia', 'id_profesional', 'id_cliente']
    _filename = 'turnos.csv'

""" class RegistrarTurno():
    def __init__(self):
        self.turnos == []

    def reserva_turno(self,nro_cliente,fecha,hora,nro_turno,dia,nro_profesional):
        for turno in self.turnos:
            if turno.fecha == fecha and turno.hora == hora:
                print('Reservado')
        

    def mostrar_turno(self): """
                