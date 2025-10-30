from app.Models.PersevoloORM.Request.Request import Request
from app.Models.Turno import Turno
from app.Models.Cliente import Cliente
from app.Models.Profesional import Profesional

class TurnoController:
    def solicitar_turno(self, request: Request):
        """
        Solicitar nuevo turno
        
        Args:
            request: Objeto Request con datos del turno
            
        Returns:
            Tuple (success, data_or_error)
        """
        # Validaciones
        (request.require('cliente_id', 'profesional_id', 'fecha', 'hora', 'servicio')
           .validate_date('fecha')
           .validate_time('hora'))
        
        if request.has_errors():
            return False, request.errors
        
        request.clean()
        data = request.validated_data
        
        try:
            # Verificar que el cliente existe
            clientes = Cliente.all()
            cliente_existe = any(c.id == data['cliente_id'] for c in clientes)
            if not cliente_existe:
                return False, {"cliente_id": "Cliente no encontrado"}
            
            # Verificar que el profesional existe
            profesionales = Profesional.all()
            profesional_existe = any(p.id == data['profesional_id'] for p in profesionales)
            if not profesional_existe:
                return False, {"profesional_id": "Profesional no encontrado"}
            
            # Verificar que no haya turno en el mismo horario
            turnos = Turno.all()
            for turno in turnos:
                if (turno.profesional_id == data['profesional_id'] and
                    turno.fecha == data['fecha'] and
                    turno.hora == data['hora'] and
                    turno.estado != 'cancelado'):
                    return False, {"error": "Ya existe un turno en ese horario para este profesional"}
            
            # Crear nuevo turno
            nuevo_id = str(len(turnos) + 1)
            nuevo_turno = Turno(
                id=nuevo_id,
                cliente_id=data['cliente_id'],
                profesional_id=data['profesional_id'],
                fecha=data['fecha'],
                hora=data['hora'],
                servicio=data['servicio'],
                estado='pendiente'
            )
            
            turnos.append(nuevo_turno)
            Turno.save_all(turnos)
            
            return True, nuevo_turno
            
        except Exception as e:
            return False, {"error": f"Error al solicitar turno: {str(e)}"}
    
    def cancelar_turno(self, request: Request):
        """
        Cancelar turno
        
        Args:
            request: Objeto Request con ID del turno
            
        Returns:
            Tuple (success, data_or_error)
        """
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