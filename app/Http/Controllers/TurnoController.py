from app.Models.PersevoloORM.Request.Request import Request
from app.Models.Turno import Turno
from app.Models.Cliente import Cliente
from app.Models.Profesional import Profesional
from app.Models.Atencion import Atencion
from app.Models.Servicio import Servicio

from app.Http.Controllers.ClienteController import ClienteController

from datetime import datetime, timedelta


class TurnoController:
    
    def __init__(self):
        self._cliente_controller = ClienteController()
        
    def solicitar_turno(self):
        """
        Buscar cliente usando solicitar_buscar_cliente, luego mostrar turnos disponibles y reservar.
        """
        # Buscar cliente usando método multiparametro
        clientes = self._cliente_controller.solicitar_buscar_cliente()
        if not clientes:
            print("No se encontraron clientes.")
            return False, {"error": "Cliente no encontrado"}
        if isinstance(clientes, dict):
            # Si el método retorna un dict de error
            return False, clientes
        print("Seleccione un cliente:")
        for idx, c in enumerate(clientes, 1):
            print(f"{idx}. {c.nombre} {c.apellido} (ID: {c.id})")
        sel = input("Opción: ")
        try:
            cliente = clientes[int(sel)-1]
        except Exception:
            print("Selección inválida.")
            return False, {"error": "Selección inválida"}

        # Mostrar todos los turnos disponibles (sin cliente asignado)
        turnos = [t for t in Turno.all() if t.estado == 'disponible']
        if not turnos:
            print("No hay turnos disponibles.")
            return False, {"error": "No hay turnos disponibles"}

        print("Seleccione un turno disponible:")
        for idx, t in enumerate(turnos, 1):
            profesional = next((p for p in Profesional.all() if str(p.id) == str(t.profesional_id)), None)
            atencion = next((a for a in Atencion.all() if str(a.id) == str(t.atencion_id)), None)
            servicio = None
            if atencion:
                servicio = next((s for s in Servicio.all() if str(s.id) == str(atencion.id_servicio)), None)
            dia_nombre = ''
            if t.fecha:
                try:
                    fecha_dt = datetime.strptime(t.fecha, "%Y-%m-%d")
                    dias_map = {0: 'LUNES', 1: 'MARTES', 2: 'MIERCOLES', 3: 'JUEVES', 4: 'VIERNES', 5: 'SABADO', 6: 'DOMINGO'}
                    dia_nombre = dias_map[fecha_dt.weekday()]
                except Exception:
                    dia_nombre = ''
            print(f"{idx}. Fecha: {t.fecha} | Día: {dia_nombre} | Hora: {t.hora} | Profesional: {profesional.nombre if profesional else t.profesional_id} | Servicio: {servicio.nombre if servicio else '-'}")
        sel = input("Opción: ")
        try:
            turno = turnos[int(sel)-1]
        except Exception:
            print("Selección inválida.")
            return False, {"error": "Selección inválida"}

        # Reservar el turno
        return self.reservar_turno(turno.id, cliente.id)

    def cancelar_turno(self):
        """
        Cancela un turno mostrando los turnos reservados del cliente (usando solicitar_buscar_cliente).
        """
        clientes = self._cliente_controller.solicitar_buscar_cliente()
        if not clientes:
            print("No se encontraron clientes.")
            return False, {"error": "Cliente no encontrado"}
        if isinstance(clientes, dict):
            return False, clientes
        print("Seleccione un cliente:")
        for idx, c in enumerate(clientes, 1):
            print(f"{idx}. {c.nombre} {c.apellido} (ID: {c.id})")
        sel = input("Opción: ")
        try:
            cliente = clientes[int(sel)-1]
        except Exception:
            print("Selección inválida.")
            return False, {"error": "Selección inválida"}

        turnos = [t for t in Turno.all() if t.cliente_id == cliente.id and t.estado == 'reservado']
        if not turnos:
            print("No hay turnos reservados para este cliente.")
            return False, {"error": "No hay turnos reservados"}
        print("Seleccione el turno a cancelar:")
        for idx, t in enumerate(turnos, 1):
            profesional = next((p for p in Profesional.all() if str(p.id) == str(t.profesional_id)), None)
            atencion = next((a for a in Atencion.all() if str(a.id) == str(t.atencion_id)), None)
            servicio = None
            if atencion:
                servicio = next((s for s in Servicio.all() if str(s.id) == str(atencion.id_servicio)), None)
            dia_nombre = ''
            if t.fecha:
                try:
                    fecha_dt = datetime.strptime(t.fecha, "%Y-%m-%d")
                    dias_map = {0: 'LUNES', 1: 'MARTES', 2: 'MIERCOLES', 3: 'JUEVES', 4: 'VIERNES', 5: 'SABADO', 6: 'DOMINGO'}
                    dia_nombre = dias_map[fecha_dt.weekday()]
                except Exception:
                    dia_nombre = ''
            print(f"{idx}. Fecha: {t.fecha} | Día: {dia_nombre} | Hora: {t.hora} | Profesional: {profesional.nombre if profesional else t.profesional_id} | Servicio: {servicio.nombre if servicio else '-'}")
        sel = input("Opción: ")
        try:
            turno = turnos[int(sel)-1]
        except Exception:
            print("Selección inválida.")
            return False, {"error": "Selección inválida"}

        turno.estado = 'cancelado'
        Turno.save_all(Turno.all())
        print("Turno cancelado correctamente.")
        return True, turno

    def consultar_turno(self):
        """
        Consulta un turno mostrando los turnos del cliente (usando solicitar_buscar_cliente).
        """
        clientes = self._cliente_controller.solicitar_buscar_cliente()
        if not clientes:
            print("No se encontraron clientes.")
            return False, {"error": "Cliente no encontrado"}
        if isinstance(clientes, dict):
            return False, clientes
        print("Seleccione un cliente:")
        for idx, c in enumerate(clientes, 1):
            print(f"{idx}. {c.nombre} {c.apellido} (ID: {c.id})")
        sel = input("Opción: ")
        try:
            cliente = clientes[int(sel)-1]
        except Exception:
            print("Selección inválida.")
            return False, {"error": "Selección inválida"}

        turnos = [t for t in Turno.all() if t.cliente_id == cliente.id]
        if not turnos:
            print("No hay turnos para este cliente.")
            return False, {"error": "No hay turnos"}
        print("Seleccione el turno a consultar:")
        for idx, t in enumerate(turnos, 1):
            profesional = next((p for p in Profesional.all() if str(p.id) == str(t.profesional_id)), None)
            atencion = next((a for a in Atencion.all() if str(a.id) == str(t.atencion_id)), None)
            servicio = None
            if atencion:
                servicio = next((s for s in Servicio.all() if str(s.id) == str(atencion.id_servicio)), None)
            dia_nombre = ''
            if t.fecha:
                try:
                    fecha_dt = datetime.strptime(t.fecha, "%Y-%m-%d")
                    dias_map = {0: 'LUNES', 1: 'MARTES', 2: 'MIERCOLES', 3: 'JUEVES', 4: 'VIERNES', 5: 'SABADO', 6: 'DOMINGO'}
                    dia_nombre = dias_map[fecha_dt.weekday()]
                except Exception:
                    dia_nombre = ''
            print(f"{idx}. Fecha: {t.fecha} | Día: {dia_nombre} | Hora: {t.hora} | Profesional: {profesional.nombre if profesional else t.profesional_id} | Servicio: {servicio.nombre if servicio else '-'} | Estado: {t.estado}")
        sel = input("Opción: ")
        try:
            turno = turnos[int(sel)-1]
        except Exception:
            print("Selección inválida.")
            return False, {"error": "Selección inválida"}

        print(f"Turno seleccionado: Fecha: {turno.fecha} | Día: {dia_nombre} | Hora: {turno.hora} | Profesional: {profesional.nombre if profesional else turno.profesional_id} | Servicio: {servicio.nombre if servicio else '-'} | Estado: {turno.estado}")
        return True, turno

    def generar_turnos_para_profesional(self, profesional_id: str, fecha_str: str):
        """Genera turnos para las atenciones aplicables en una fecha. Si profesional_id no es vacío, limita a ese profesional."""
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            dias_map = {0: 'LUNES', 1: 'MARTES', 2: 'MIERCOLES', 3: 'JUEVES', 4: 'VIERNES', 5: 'SABADO', 6: 'DOMINGO'}
            dia_nombre = dias_map[fecha.weekday()]

            atenciones = [a for a in Atencion.all() if getattr(a, 'dia', '').upper() == dia_nombre]
            if not atenciones:
                return False, {"error": "No hay atenciones configuradas para la fecha dada"}

            creados = []

            def parse_time(t):
                if isinstance(t, str):
                    try:
                        return datetime.strptime(t, "%H:%M:%S").time()
                    except Exception:
                        return datetime.strptime(t, "%H:%M").time()
                return t

            def profesional_ofrece_atencion(prof, atencion_id):
                val = getattr(prof, 'atenciones', '')
                if isinstance(val, str):
                    items = [s.strip() for s in val.split(',') if s.strip()]
                    return str(atencion_id) in items
                if isinstance(val, list):
                    for item in val:
                        if isinstance(item, dict):
                            if str(item.get('id')) == str(atencion_id):
                                return True
                        else:
                            if str(item) == str(atencion_id):
                                return True
                return False

            for a in atenciones:
                servicio = Servicio.find_one_by(id=a.id_servicio)
                if not servicio:
                    continue

                hora_desde = parse_time(a.hora_desde)
                hora_hasta = parse_time(a.hora_hasta)
                dur = int(servicio.duracion)

                profesionales = [p for p in Profesional.all() if profesional_ofrece_atencion(p, a.id)]
                if profesional_id and profesional_id != '':
                    profesionales = [p for p in profesionales if str(p.id) == str(profesional_id)]
                if not profesionales:
                    continue

                for prof in profesionales:
                    cursor = datetime.combine(fecha, hora_desde)
                    end_at = datetime.combine(fecha, hora_hasta)
                    while cursor + timedelta(minutes=dur) <= end_at:
                        slot_hora = cursor.time().strftime("%H:%M")
                        if not Turno.exists(profesional_id=str(prof.id), fecha=fecha_str, hora=slot_hora):
                            nuevo = Turno(cliente_id='', profesional_id=str(prof.id), fecha=fecha_str, hora=slot_hora, atencion_id=str(a.id), estado='disponible')
                            nuevo.save()
                            creados.append(nuevo)
                        cursor += timedelta(minutes=dur)

            return True, creados
        except Exception as e:
            return False, {"error": f"Error al generar turnos: {str(e)}"}

    def generar_turnos_masivos(self, fecha_str: str):
        resultados = []
        for prof in Profesional.all():
            ok, data = self.generar_turnos_para_profesional(str(prof.id), fecha_str)
            resultados.append((prof.id, ok, data))
        return True, resultados

    def solicitar_generar_turnos_masivos(self):
        fecha = input('Fecha (YYYY-MM-DD) para generar turnos masivos: ')
        return self.generar_turnos_masivos(fecha)

    def reservar_turno(self, turno_id: str, cliente_id: str):
        try:
            turnos = Turno.all()
            for t in turnos:
                if str(t.id) == str(turno_id):
                    if getattr(t, 'estado', '') != 'disponible':
                        return False, {"error": "Turno no disponible para reservar"}
                    t.cliente_id = str(cliente_id)
                    t.estado = 'reservado'
                    Turno.save_all(turnos)
                    return True, t
            turnos = Turno.all()
        except Exception as e:
            return False, {"error": f"Error al solicitar turno: {str(e)}"}
    
    def cancelar_turno(self, request: Request):
        """ Cancelar turno """
        # Soporta llamada interactiva si no se pasa Request
        if request is None:
            turno_id = input("ID del turno a cancelar: ")
            request = Request({'turno_id': turno_id})

        request.require('turno_id')

        if request.has_errors():
            return False, request.errors

        turno_id = request.get_str('turno_id')
        
        try:
            turnos = Turno.all()
            for turno in turnos:
                if turno.id == turno_id:
                    turno.estado = 'cancelado'
                    Turno.save_all(turnos)
                    return True, turno
            
            return False, {"error": "Turno no encontrado"}
            
        except Exception as e:
            return False, {"error": f"Error al cancelar turno: {str(e)}"}

    def generar_turnos_para_profesional(self, profesional_id: str, fecha_str: str):
        """Genera turnos disponibles para un profesional en una fecha concreta basada en sus atenciones """
        try:
            # validar fecha
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()

            # mapear nombre del dia en español (asume Dia.nombre está en español)
            dias_map = {
                0: 'LUNES', 1: 'MARTES', 2: 'MIERCOLES', 3: 'JUEVES', 4: 'VIERNES', 5: 'SABADO', 6: 'DOMINGO'
            }
            dia_nombre = dias_map[fecha.weekday()]

            # obtener atenciones para ese dia (las atenciones son independientes)
            atenciones = [a for a in Atencion.all() if a.dia.upper() == dia_nombre]

            if not atenciones:
                return False, {"error": "No hay atenciones configuradas para la fecha dada"}

            creados = []
            # helper para parsear horas
            def parse_time(t):
                if isinstance(t, str):
                    try:
                        return datetime.strptime(t, "%H:%M:%S").time()
                    except ValueError:
                        return datetime.strptime(t, "%H:%M").time()
                return t

            # helper para verificar si un profesional ofrece una atencion
            def profesional_ofrece_atencion(prof, atencion_id):
                val = getattr(prof, 'atenciones', '')
                # Si es string (formato antiguo o vacío)
                if isinstance(val, str):
                    items = [s.strip() for s in val.split(',') if s.strip()]
                    return str(atencion_id) in items

                # Si es lista, puede contener ids o dicts con 'id'
                if isinstance(val, list):
                    for item in val:
                        if isinstance(item, dict):
                            if str(item.get('id')) == str(atencion_id):
                                return True
                        else:
                            if str(item) == str(atencion_id):
                                return True
                return False

            for a in atenciones:
                servicio = Servicio.find_one_by(id=a.id_servicio)
                if not servicio:
                    continue

                hora_desde = parse_time(a.hora_desde)
                hora_hasta = parse_time(a.hora_hasta)
                dur = int(servicio.duracion)

                # profesionales que ofrecen esta atencion
                profesionales = [p for p in Profesional.all() if profesional_ofrece_atencion(p, a.id)]
                if profesional_id and profesional_id != '':
                    profesionales = [p for p in profesionales if str(p.id) == str(profesional_id)]

                if not profesionales:
                    # si ningún profesional está asignado a la atencion, se omite
                    continue

                # generar slots para cada profesional
                for prof in profesionales:
                    cursor = datetime.combine(fecha, hora_desde)
                    end_at = datetime.combine(fecha, hora_hasta)
                    while cursor + timedelta(minutes=dur) <= end_at:
                        slot_hora = cursor.time().strftime("%H:%M")
                        # verificar no exista turno ya para ese profesional/fecha/hora
                        if not Turno.exists(profesional_id=str(prof.id), fecha=fecha_str, hora=slot_hora):
                            nuevo = Turno(cliente_id='', profesional_id=str(prof.id), fecha=fecha_str, hora=slot_hora, atencion_id=str(a.id), estado='disponible')
                            nuevo.save()
                            creados.append(nuevo)
                        cursor += timedelta(minutes=dur)

            return True, creados
        except Exception as e:
            return False, {"error": f"Error al generar turnos: {str(e)}"}


    def generar_turnos_masivos(self, fecha_str: str):
        """Genera turnos para todos los profesionales que tengan atenciones para la fecha dada."""
        resultados = []
        for prof in Profesional.all():
            ok, data = self.generar_turnos_para_profesional(str(prof.id), fecha_str)
            resultados.append((prof.id, ok, data))
        return True, resultados

    def solicitar_generar_turnos_masivos(self):
        fecha = input('Fecha (YYYY-MM-DD) para generar turnos masivos: ')
        return self.generar_turnos_masivos(fecha)

    def reservar_turno(self, turno_id: str, cliente_id: str):
        """Reservar un turno existente: asigna cliente_id y marca estado 'reservado' si estaba disponible."""
        turnos = Turno.all()
        for turno in turnos:
            if str(turno.id) == str(turno_id):
                if getattr(turno, 'estado', '') != 'disponible':
                    return False, {"error": "Turno no disponible para reservar"}
                turno.cliente_id = str(cliente_id)
                turno.estado = 'reservado'
                Turno.save_all(turnos)
                return True, turno
        return False, {"error": "Turno no encontrado"}