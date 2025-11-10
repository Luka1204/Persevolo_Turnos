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
        """Buscar cliente y reservar un turno disponible."""
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
        except (IndexError, ValueError):
            print("Selección inválida.")
            return False, {"error": "Selección inválida"}

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
        except (IndexError, ValueError):
            print("Selección inválida.")
            return False, {"error": "Selección inválida"}

        return self.reservar_turno(turno.id, cliente.id)

    def cancelar_turno(self):
        """Cancela un turno mostrando los turnos reservados del cliente."""
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
        except (IndexError, ValueError):
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
        except (IndexError, ValueError):
            print("Selección inválida.")
            return False, {"error": "Selección inválida"}

        turno.estado = 'cancelado'
        Turno.save_all(Turno.all())
        print("Turno cancelado correctamente.")
        return True, turno

    def consultar_turno(self):
        """Consulta un turno mostrando los turnos del cliente."""
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
        except (IndexError, ValueError):
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
        except (IndexError, ValueError):
            print("Selección inválida.")
            return False, {"error": "Selección inválida"}

        print(f"Turno seleccionado: Fecha: {turno.fecha} | Día: {dia_nombre} | Hora: {turno.hora} | Profesional: {profesional.nombre if profesional else turno.profesional_id} | Servicio: {servicio.nombre if servicio else '-'} | Estado: {turno.estado}")
        return True, turno

    def generar_turnos_para_profesional(self, profesional_id: str, fecha_str: str):
        """Genera turnos para las atenciones aplicables en una fecha."""
        try:
            print("Iniciando generación de turnos...")
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            dias_map = {0: 'LUNES', 1: 'MARTES', 2: 'MIERCOLES', 3: 'JUEVES', 4: 'VIERNES', 5: 'SABADO', 6: 'DOMINGO'}
            dia_nombre = dias_map[fecha.weekday()]
            print(f"Fecha: {fecha}, Día: {dia_nombre}")

            atenciones = [a for a in Atencion.all() if getattr(a, 'dia', '').upper() == dia_nombre]
            if not atenciones:
                print("No hay atenciones configuradas para la fecha dada.")
                return False, {"error": "No hay atenciones configuradas para la fecha dada"}

            creados = []

            for a in atenciones:
                servicio = Servicio.find_one_by(id=a.id_servicio)
                if not servicio:
                    print(f"Servicio no encontrado para atención ID: {a.id}")
                    continue

                # ...existing code...
                hora_desde = datetime.strptime(a.hora_desde, "%H:%M:%S").time()  # Ajustar a HH:MM:SS si es necesario
                hora_hasta = datetime.strptime(a.hora_hasta, "%H:%M:%S").time()  # Ajustar a HH:MM:SS si es necesario
                dur = int(servicio.duracion)

                profesionales = [p for p in Profesional.all() if str(p.id) == str(profesional_id)]
                if not profesionales:
                    print(f"No se encontraron profesionales para ID: {profesional_id}")
                    continue

                for prof in profesionales:
                    cursor = datetime.combine(fecha, hora_desde)
                    end_at = datetime.combine(fecha, hora_hasta)
                    print(f"Generando turnos desde {cursor} hasta {end_at}")

                    while cursor + timedelta(minutes=dur) <= end_at:
                        slot_hora = cursor.time().strftime("%H:%M")
                        print(f"Verificando slot: {slot_hora}")
                        if not Turno.exists(profesional_id=str(prof.id), fecha=fecha_str, hora=slot_hora):
                            nuevo = Turno(cliente_id='', profesional_id=str(prof.id), fecha=fecha_str, hora=slot_hora, atencion_id=str(a.id), estado='disponible')
                            nuevo.save()
                            creados.append(nuevo)
                            print(f"Turno creado: {nuevo}")
                        cursor += timedelta(minutes=dur)

            return True, creados
        except Exception as e:
            print(f"Error al generar turnos: {str(e)}")
            return False, {"error": f"Error al generar turnos: {str(e)}"}

    def generar_turnos_masivos(self, fecha_str: str):
        """Genera turnos masivos para todos los profesionales."""
        resultados = []
        for prof in Profesional.all():
            ok, data = self.generar_turnos_para_profesional(str(prof.id), fecha_str)
            resultados.append((prof.id, ok, data))
        return True, resultados

    def solicitar_generar_turnos_masivos(self):
        """Solicita la fecha para generar turnos masivos."""
        fecha = input('Fecha (YYYY-MM-DD) para generar turnos masivos: ')
        return self.generar_turnos_masivos(fecha)

    def reservar_turno(self, turno_id: str, cliente_id: str):
        """Reserva un turno existente."""
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
            return False, {"error": "Turno no encontrado"}
        except Exception as e:
            return False, {"error": f"Error al solicitar turno: {str(e)}"}

    def cancelar_turno(self, request: Request):
        """Cancela un turno."""
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