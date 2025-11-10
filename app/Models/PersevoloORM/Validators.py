import re
from datetime import datetime

class Validator:
    def __init__(self):
        # mapeo campo -> método validador ligado
        self.FIELD_VALIDATORS = {
            'nombre': self.validate_nombre,
            'apellido': self.validate_apellido,
            'dni': self.validate_dni,
            'email': self.validate_email,
            'telefono': self.validate_telefono,
            'cuil': self.validate_cuil,
            'hora_desde': self.validate_hora_desde,
            'hora_hasta': self.validate_hora_hasta,
            'duracion': self.validate_duracion,
            'precio': self.validate_precio,
            'atencines':self.validate_atenciones
        }

    def _is_non_empty_string(self, v):
        result = isinstance(v, str) and v.strip() != ''
        return result

    def validate_field(self, field_name, value):
        """Valida un campo por nombre si existe un validador específico"""
        validator = self.FIELD_VALIDATORS.get(field_name)
        if validator:
            result = validator(value)
            return result
        return None  # No hay validador para este campo

    def validate_atenciones(self, val):
        return len(val) > 0
    def validate_nombre(self, value):
        if not self._is_non_empty_string(value):
            return "El nombre no puede estar vacío"
        if len(value.strip()) < 2:
            return "El nombre es demasiado corto"
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s\-]+$', value.strip()):
            return "El nombre contiene caracteres inválidos"
        return None

    def validate_apellido(self, value):
        if not self._is_non_empty_string(value):
            return "El apellido no puede estar vacío"
        if len(value.strip()) < 2:
            return "El apellido es demasiado corto"
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s\-]+$', value.strip()):
            return "El apellido contiene caracteres inválidos"
        return None

    def validate_dni(self, value):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return "DNI requerido"
        s = str(value).strip()
        if not s.isdigit():
            return "DNI debe contener solo dígitos"
        if not (7 <= len(s) <= 9):
            return "DNI debe tener entre 7 y 9 dígitos"
        return None

    def validate_email(self, value):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return "Email requerido"
        s = value.strip()
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', s):
            return "Email inválido"
        return None

    def validate_telefono(self, value):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return "Teléfono requerido"
        s = str(value).strip()
        digits = re.sub(r'\D', '', s)
        if len(digits) < 6:
            return "Teléfono inválido (menos de 6 dígitos)"
        if not re.match(r'^[0-9\+\-\s\(\)]+$', s):
            return "Teléfono contiene caracteres inválidos"
        return None

    def validate_cuil(self, value):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return "CUIL requerido"
        s = re.sub(r'\D', '', str(value))
        if len(s) != 11:
            return "CUIL debe tener 11 dígitos"
        if not s.isdigit():
            return "CUIL inválido"
        return None

    def _parse_time(self, value):
        if isinstance(value, str):
            for fmt in ("%H:%M", "%H:%M:%S"):
                try:
                    return datetime.strptime(value.strip(), fmt).time()
                except Exception:
                    continue
        return None

    def validate_hora_desde(self, value):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return "hora_desde requerida"
        if self._parse_time(value) is None:
            return "Formato de hora_desde inválido (HH:MM o HH:MM:SS)"
        return None

    def validate_hora_hasta(self, value):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return "hora_hasta requerida"
        if self._parse_time(value) is None:
            return "Formato de hora_hasta inválido (HH:MM o HH:MM:SS)"
        return None

    def validate_duracion(self, value):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return "Duración requerida"
        try:
            v = int(value)
            if v <= 0:
                return "Duración debe ser entero positivo"
        except Exception:
            return "Duración inválida (debe ser entero)"
        return None

    def validate_precio(self, value):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return "Precio requerido"
        try:
            v = float(value)
            if v < 0:
                return "Precio no puede ser negativo"
        except Exception:
            return "Precio inválido (debe ser numérico)"
        return None

# para compatibilidad si se importa a nivel de módulo
default_validator = Validator()
FIELD_VALIDATORS = default_validator.FIELD_VALIDATORS