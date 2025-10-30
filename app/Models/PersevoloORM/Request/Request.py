from typing import Any, Dict, List, Optional
from datetime import datetime

class Request():
    """
    Modelo Request para recibir y validar datos de entrada del usuario
    Actúa como DTO (Data Transfer Object) entre la vista y el controlador
    """
    
    def __init__(self, data: Dict[str, Any] = None):
        """
        Inicializar Request con datos
        
        Args:
            data: Diccionario con datos de la solicitud
        """
        self._data = data or {}
        self._errors = {}
        self._validated_data = {}
    
    @property
    def data(self) -> Dict[str, Any]:
        """Obtener datos originales"""
        return self._data.copy()
    
    @property
    def validated_data(self) -> Dict[str, Any]:
        """Obtener datos validados"""
        return self._validated_data.copy()
    
    @property
    def errors(self) -> Dict[str, str]:
        """Obtener errores de validación"""
        return self._errors.copy()
    
    def has_errors(self) -> bool:
        """Verificar si hay errores de validación"""
        return len(self._errors) > 0
    
    def is_valid(self) -> bool:
        """Verificar si la request es válida"""
        return len(self._errors) == 0
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtener valor por clave
        
        Args:
            key: Clave a buscar
            default: Valor por defecto si no existe
            
        Returns:
            Valor de la clave o default
        """
        return self._data.get(key, default)
    
    def get_str(self, key: str, default: str = "") -> str:
        """Obtener valor como string"""
        value = self.get(key, default)
        return str(value) if value is not None else default
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Obtener valor como integer"""
        try:
            value = self.get(key, default)
            return int(value) if value is not None else default
        except (ValueError, TypeError):
            return default
    
    def get_float(self, key: str, default: float = 0.0) -> float:
        """Obtener valor como float"""
        try:
            value = self.get(key, default)
            return float(value) if value is not None else default
        except (ValueError, TypeError):
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Obtener valor como boolean"""
        value = self.get(key, default)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'si', 'sí')
        return bool(value)
    
    def get_list(self, key: str, default: List = None) -> List:
        """Obtener valor como lista"""
        if default is None:
            default = []
        value = self.get(key, default)
        return value if isinstance(value, list) else default
    
    def get_dict(self, key: str, default: Dict = None) -> Dict:
        """Obtener valor como diccionario"""
        if default is None:
            default = {}
        value = self.get(key, default)
        return value if isinstance(value, dict) else default
    
    def require(self, *fields: str) -> 'Request':
        """
        Validar que los campos requeridos estén presentes
        
        Args:
            *fields: Campos requeridos
            
        Returns:
            Self para method chaining
        """
        for field in fields:
            if field not in self._data or self._data[field] in (None, ""):
                self._add_error(field, f"El campo '{field}' es requerido")
        return self
    
    def validate_email(self, field: str) -> 'Request':
        """
        Validar que un campo sea un email válido
        
        Args:
            field: Campo a validar
            
        Returns:
            Self para method chaining
        """
        value = self.get(field)
        if value and '@' not in str(value):
            self._add_error(field, f"El campo '{field}' debe ser un email válido")
        return self
    
    def validate_min_length(self, field: str, min_length: int) -> 'Request':
        """
        Validar longitud mínima de un campo string
        
        Args:
            field: Campo a validar
            min_length: Longitud mínima requerida
            
        Returns:
            Self para method chaining
        """
        value = self.get_str(field)
        if value and len(value) < min_length:
            self._add_error(field, f"El campo '{field}' debe tener al menos {min_length} caracteres")
        return self
    
    def validate_max_length(self, field: str, max_length: int) -> 'Request':
        """
        Validar longitud máxima de un campo string
        
        Args:
            field: Campo a validar
            max_length: Longitud máxima permitida
            
        Returns:
            Self para method chaining
        """
        value = self.get_str(field)
        if value and len(value) > max_length:
            self._add_error(field, f"El campo '{field}' no puede tener más de {max_length} caracteres")
        return self
    
    def validate_numeric(self, field: str) -> 'Request':
        """
        Validar que un campo sea numérico
        
        Args:
            field: Campo a validar
            
        Returns:
            Self para method chaining
        """
        value = self.get(field)
        if value and not str(value).replace('.', '').isdigit():
            self._add_error(field, f"El campo '{field}' debe ser numérico")
        return self
    
    def validate_phone(self, field: str) -> 'Request':
        """
        Validar que un campo sea un teléfono válido
        
        Args:
            field: Campo a validar
            
        Returns:
            Self para method chaining
        """
        value = self.get_str(field)
        if value and not value.replace(' ', '').replace('-', '').isdigit():
            self._add_error(field, f"El campo '{field}' debe ser un teléfono válido")
        return self
    
    def validate_date(self, field: str, format: str = "%Y-%m-%d") -> 'Request':
        """
        Validar que un campo sea una fecha válida
        
        Args:
            field: Campo a validar
            format: Formato de fecha esperado
            
        Returns:
            Self para method chaining
        """
        value = self.get_str(field)
        if value:
            try:
                datetime.strptime(value, format)
            except ValueError:
                self._add_error(field, f"El campo '{field}' debe ser una fecha válida en formato {format}")
        return self
    
    def validate_time(self, field: str, format: str = "%H:%M") -> 'Request':
        """
        Validar que un campo sea una hora válida
        
        Args:
            field: Campo a validar
            format: Formato de hora esperado
            
        Returns:
            Self para method chaining
        """
        value = self.get_str(field)
        if value:
            try:
                datetime.strptime(value, format)
            except ValueError:
                self._add_error(field, f"El campo '{field}' debe ser una hora válida en formato {format}")
        return self
    
    def validate_custom(self, field: str, validator: callable, message: str = None) -> 'Request':
        """
        Validación personalizada
        
        Args:
            field: Campo a validar
            validator: Función de validación que retorna bool
            message: Mensaje de error personalizado
            
        Returns:
            Self para method chaining
        """
        value = self.get(field)
        if value and not validator(value):
            error_msg = message or f"El campo '{field}' no es válido"
            self._add_error(field, error_msg)
        return self
    
    """ def add_data(self, **kwargs) -> 'Request':
        Agregar datos adicionales a la request
        
        Args:
            **kwargs: Datos a agregar
            
        Returns:
            Self para method chaining

        self._data.update(kwargs)
        return self """
    
    def clean(self) -> 'Request':
        """
        Limpiar y preparar datos validados
        
        Returns:
            Self para method chaining
        """
        if self.is_valid():
            self._validated_data = self._data.copy()
        return self
    
    def _add_error(self, field: str, message: str):
        """Agregar error de validación"""
        self._errors[field] = message
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario (solo datos válidos)"""
        return self.validated_data if self.is_valid() else self.data
    
    def __str__(self) -> str:
        return f"Request(data={self._data}, errors={self._errors}, valid={self.is_valid()})"
    
    def __getitem__(self, key: str) -> Any:
        return self.get(key)
    
    def __contains__(self, key: str) -> bool:
        return key in self._data