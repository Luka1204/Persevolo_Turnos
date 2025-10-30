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
        (request.require('nombre', 'apellido', 'especialidad')
           .validate_string('nombre', min_length=2, max_length=100)
           .validate_string('apellido', min_length=2, max_length=100)
           .validate_string('especialidad', min_length=2, max_length=100))

        if request.has_errors():
            return False, request.errors

        request.clean()
        data = request.validated_data

        try:
            # Verificar que no exista un profesional con el mismo nombre y apellido
            profesionales = Profesional.all()
            existe = any(p.nombre == data['nombre'] and p.apellido == data['apellido'] for p in profesionales)
            if existe:
                return False, {"error": "Ya existe un profesional con ese nombre y apellido"}

            # Crear nuevo profesional
            nuevo_id = str(len(profesionales) + 1)
            nuevo_profesional = Profesional(
                id=nuevo_id,
                nombre=data['nombre'],
                apellido=data['apellido'],
                especialidad=data['especialidad']
            )

            profesionales.append(nuevo_profesional)
            Profesional.save_all(profesionales)

            return True, nuevo_profesional

        except Exception as e:
            return False, {"error": f"Error al registrar profesional: {str(e)}"}