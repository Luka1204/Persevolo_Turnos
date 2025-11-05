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
        """(request.require('nombre', 'apellido', 'dni','cuil')
           .validate_string('nombre', min_length=2, max_length=100)
           .validate_string('apellido', min_length=2, max_length=100)
           .validate_string('dni', min_length=2, max_length=100)
           .validate_string('cuil', min_length=2, max_length=100))
        """
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
                cuil=data['cuil']
            )

            #profesionales.append(nuevo_profesional)
            #Profesional.save_all(profesionales)
            nuevo_profesional.save()

            return True, nuevo_profesional
            #modificar profesional
        except Exception as e:
            return False, {"error": f"Error al registrar profesional: {str(e)}"}
        
    def eliminar_profesional(self, dni_p):
        profesional = Profesional.where(Profesional, dni=dni_p)[0]
        a = profesional.delete()
        print(a)

    def solicitar_registro_profesional(self):
        nombre = input('Ingrese nombre del profesional: ')
        apellido = input('Ingrese apellido del profesional: ')
        dni = input('Ingrese DNI del profesional: ')
        cuil = input('Ingrese CUIL del profesional ')

        s = Request({
            "nombre":nombre,
            "apellido":apellido,
            "dni": dni,
            "cuil":cuil
        })
        return self.registrar_profesional(s)