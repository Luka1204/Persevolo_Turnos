from app.Models.PersevoloORM.Request.Request import Request
from app.Models.Profesional import Profesional
class ProfesionalController:
    def registrar_profesional(self, request: Request):
        """
        Registrar nuevo profesional

        Args:
            request: Objeto Request con datos del profesional

        Returns:
            Tuple (success, data_or_error)
        """
        # Validaciones
        (request.require('nombre', 'apellido', 'dni','cuil','atenciones')
           .validate_string('nombre', min_length=2, max_length=100)
           .validate_string('apellido', min_length=2, max_length=100)
           .validate_string('dni', min_length=2, max_length=100)
           .validate_string('cuil', min_length=2, max_length=100))
        
        if request.has_errors():
            return False, request.errors

        data = request.data
        """ request.clean()
        data = request.validated_data """
        try:
            # Verificar que no exista un profesional con el mismo nombre y apellido
            profesionales = Profesional.all()
            existe = any((p.nombre == data['nombre'] and p.apellido == data['apellido']) or (p.dni == data['dni']) or (p.cuil == data['cuil']) for p in profesionales)
            if existe:
                return False, {"error": "Ya existe un profesional con ese nombre y apellido"}

            # Crear nuevo profesional
            nuevo_profesional = Profesional(
                nombre=data['nombre'],
                apellido=data['apellido'],
                dni=data['dni'],
                cuil=data['cuil'],
                atenciones=data['atenciones']
            )

            profesionales.append(nuevo_profesional)
            Profesional.save_all(profesionales)

            return True, nuevo_profesional

        except Exception as e:
            return False, {"error": f"Error al registrar profesional: {str(e)}"}