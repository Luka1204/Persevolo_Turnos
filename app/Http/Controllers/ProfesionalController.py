from app.Models.PersevoloORM.Request.Request import Request
from app.Models.Profesional import Profesional
from app.Models.Atencion import Atencion
from app.Models.Servicio import Servicio
from app.Models.Turno import Turno

class ProfesionalController:
    
    def __init__(self):
        pass
    def registrar_profesional(self, request: Request):
        """ Registrar nuevo profesional"""
        # Validaciones básicas usando Request
        (request.require('nombre', 'apellido', 'dni', 'cuil'))

        if request.has_errors():
            return False, request.errors

        request.clean()
        data = request.validated_data
        try:
            # Verificar que no exista un profesional con el mismo nombre y apellido
            profesionales = Profesional.all()
            existe = any((p.nombre == data['nombre'] and p.apellido == data['apellido']) or (p.dni == data['dni']) or (p.cuil == data['cuil']) for p in profesionales)
            if existe:
                return False, {"error": "Ya existe un profesional con ese nombre y apellido"}

            # Crear nuevo profesional (asociar atenciones si vienen en data)
            nuevo_profesional = Profesional(
                nombre=data['nombre'],
                apellido=data['apellido'],
                dni=data['dni'],
                cuil=data['cuil'],
                atenciones=data.get('atenciones', [])
            )

            #profesionales.append(nuevo_profesional)
            #Profesional.save_all(profesionales)
            return nuevo_profesional.save()

        except Exception as e:
            return False, {"error": f"Error al registrar profesional: {str(e)}"}
        
    def eliminar_profesional(self, dni_p):
        """Eliminar profesional por DNI. Usa find_one_by para obtener la instancia y la elimina."""
        profesional = Profesional.where(dni=dni_p)
        if not profesional:
            print(f"No se encontró profesional con DNI {dni_p}")
            return 0
        profesional = profesional[0]
        # Eliminar turnos disponibles asociados al profesional
        turnos_a_eliminar = [t for t in Turno.all() if t.profesional_id== str(profesional.id) and t.estado == 'disponible']
        for turno in turnos_a_eliminar:
            turno.delete()  # Asumiendo que hay un método delete en la clase Turno

        # Ahora eliminar el profesional
        deleted = profesional.delete()
        print(f"Se eliminaron: {deleted} profesionales y {len(turnos_a_eliminar)} turnos disponibles.")
        return deleted

    def solicitar_registro_profesional(self):
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

        s = Request({
            "nombre":nombre,
            "apellido":apellido,
            "dni": dni,
            "cuil":cuil,
            "atenciones": seleccionadas
        })
        succes = self.registrar_profesional(s)
        
        if succes:
            print("Profesional registrado!")

    def solicitar_buscar_profesional(self):
        """Interfaz interactiva para buscar profesionales por nombre/apellido/dni."""
        nombre = input('Nombre (opcional): ')
        apellido = input('Apellido (opcional): ')
        dni = input('DNI (opcional): ')

        filtros = {}
        if nombre:
            filtros['nombre'] = nombre
        if apellido:
            filtros['apellido'] = apellido
        if dni:
            filtros['dni'] = dni

        resultados = Profesional.where(**filtros)
        if not resultados:
            print('No se encontraron profesionales')
            return []
        for p in resultados:
            print(p)
        return resultados

    def actualizar_profesional(self, request: Request = None):
        """Actualizar profesional; si no se recibe Request, se ejecuta modo interactivo."""
        if request is None:
            dni = input('Ingrese DNI del profesional a actualizar: ')
            encontrados = Profesional.where(dni=dni)
            if not encontrados:
                print('Profesional no encontrado')
                return False, {"error": "Profesional no encontrado"}
            prof = encontrados[0]
            nombre = input('Nuevo nombre (dejar vacío para no cambiar): ')
            apellido = input('Nuevo apellido (dejar vacío para no cambiar): ')
            cuil = input('Nuevo CUIL (dejar vacío para no cambiar): ')

            prof.nombre = nombre if nombre != '' else prof.nombre
            prof.apellido = apellido if apellido != '' else prof.apellido
            prof.cuil = cuil if cuil != '' else prof.cuil
            request = Request({'profesional': prof})

        request.require('profesional')
        if request.has_errors():
            return False

        profesional = request.get('profesional') if isinstance(request.get('profesional'), Profesional) else None
        if not profesional or not hasattr(profesional, 'id'):
            return False

        success= profesional.update()
        if success:
            print("Profesional actualizado!")
        return True

    def buscar_turnos_por_profesional(self):
        """Listar turnos de un profesional por su ID o DNI (interactivo)."""
        criterio = input('Ingrese  DNI del profesional: ')
        profesional = Profesional.find_one_by(dni=criterio)
        if not profesional:
            print('Profesional no encontrado')
            return False, {"error": "Profesional no encontrado"}

        
        turnos = [t for t in Turno.all() if getattr(t, 'profesional_id', '') == str(profesional.id)]
        if not turnos:
            print('No hay turnos para este profesional')
            return []
        for t in turnos:
            print(t)
        return turnos