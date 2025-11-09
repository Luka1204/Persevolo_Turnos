from app.Models.PersevoloORM.Request.Request import Request
from app.Models.Profesional import Profesional
from app.Http.Controllers.AtencionController import AtencionController
class ProfesionalController:

    def __init__(self):
        self._atencion_controller = AtencionController


    def solicitar_guardar_profesional(self):
        atenciones = self._atencion_controller.get_atenciones()
        nombre = input('Ingrese nombre del profesional: ')
        apellido = input('Ingrese apellido del profesional: ')
        dni = input('Ingrese DNI del profesional: ')
        cuil = input('Ingrese CUIL del profesional ')
        atenciones_seleccionadas = []
        if atenciones:
            print('Atenciones disponibles:')
            for idx, a in enumerate(atenciones, start=1):
                print(f"{idx}) id = {a.id} servicio = {a.id_servicio} dia={a.dia} {a.hora_desde}-{a.hora_hasta}")
        
            select = input('Ingrese números de atenciones para asociar (coma-separados) o dejar vacío: ')
            
            if select.strip() != '':
                try:
                    indices = [int(x.strip()) for x in select.split(',') if x.strip()]
                    for i in indices:
                        if 1 <= i < len(atenciones)-1:
                            a = atenciones[i]
                            print(a)
                            atenciones_seleccionadas.append(a)
                except Exception:
                    print('Selección inválida; no se asociarán atenciones.')