from app.Models.PersevoloORM.Request.Request import Request
from app.Models.Profesional import Profesional
from app.Http.Controllers.AtencionController import AtencionController
from app.Models.Servicio import Servicio
from app.Models.Atencion import Atencion
class ProfesionalController:

    def __init__(self):
        self._atencion_controller = AtencionController


    def solicitar_guardar_profesional(self):
        nombre = input('Ingrese nombre del profesional: ')
        apellido = input('Ingrese apellido del profesional: ')
        dni = input('Ingrese DNI del profesional: ')
        cuil = input('Ingrese CUIL del profesional ')
        # Permitir asociar atenciones existentes al profesional
        atenciones = Atencion.all()
        seleccionadas = []
        if atenciones:
            print('Atenciones disponibles:')
            for idx, a in enumerate(atenciones, start=1):
                print(f"{idx}) id={a.id} servicio={Servicio.where(id=getattr(a,'id_servicio', ''))[0].nombre} dia={a.dia} {a.hora_desde}-{a.hora_hasta}")
            sel = input('Ingrese números de atenciones para asociar (coma-separados) o dejar vacío: ')
            if sel.strip() != '':
                try:
                    indices = [int(x.strip()) for x in sel.split(',') if x.strip()]
                    for i in indices:
                        if 1 <= i <= len(atenciones):
                            a = atenciones[i-1]
                            print(a)
                            seleccionadas.append(a)
                except Exception:
                    print('Selección inválida; no se asociarán atenciones.')
            else:
                a = atenciones[sel-1]
                print(a)
                seleccionadas.append(a)
