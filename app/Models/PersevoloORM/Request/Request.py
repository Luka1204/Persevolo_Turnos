from typing import List, Dict, Any, Optional
from ..FileHandler import FileHandler

class Request:
    """
    Modelo Request para operaciones de consulta y manipulación de datos
    Proporciona una interfaz fluid  a para trabajar con los modelos
    """
    
    def __init__(self, model_class: type):
        """
        Inicializar Request para una clase de modelo específica
        
        Args:
            model_class: Clase del modelo (ej: Cliente, Turno, etc.)
        """
        self.model_class = model_class
        self._filters = {}
        self._limit = None
        self._offset = 0
        self._order_by = None
        self._ascending = True
    
    def filter(self, **filters) -> 'Request':
        """
        Aplicar filtros a la consulta
        
        Args:
            **filters: Pares campo=valor para filtrar
            
        Returns:
            Self para method chaining
        """
        self._filters.update(filters)
        return self
    
    def limit(self, limit: int) -> 'Request':
        """
        Limitar número de resultados
        
        Args:
            limit: Número máximo de resultados
            
        Returns:
            Self para method chaining
        """
        self._limit = limit
        return self
    
    def offset(self, offset: int) -> 'Request':
        """
        Saltar un número de resultados (para paginación)
        
        Args:
            offset: Número de resultados 
            
        Returns:
            Self para method chaining
        """
        self._offset = offset
        return self
    
    def order_by(self, field: str, ascending: bool = True) -> 'Request':
        """
        Ordenar resultados por campo
        
        Args:
            field: Campo por el cual ordenar
            ascending: True para orden ascendente, False para descendente
            
        Returns:
            Self para method chaining
        """
        self._order_by = field
        self._ascending = ascending
        return self
    
    def all(self) -> List[FileHandler]:
        """
        Obtener todos los objetos que coincidan con los filtros
        
        Returns:
            Lista de objetos del modelo
        """
        objects = self.model_class.load_all()
        
        # Aplicar filtros
        if self._filters:
            objects = self._apply_filters(objects)
        
        # Aplicar ordenamiento
        if self._order_by:
            objects = self._apply_ordering(objects)
        
        # Aplicar paginación
        if self._offset > 0:
            objects = objects[self._offset:]
        
        if self._limit:
            objects = objects[:self._limit]
        
        return objects
    
    def first(self) -> Optional[FileHandler]:
        """
        Obtener el primer objeto que coincida con los filtros
        
        Returns:
            Primer objeto o None si no hay resultados
        """
        results = self.limit(1).all()
        return results[0] if results else None
    
    def count(self) -> int:
        """
        Contar número de objetos que coinciden con los filtros
        
        Returns:
            Número de objetos
        """
        objects = self.model_class.load_all()
        if self._filters:
            objects = self._apply_filters(objects)
        return len(objects)
    
    def get(self, object_id: str) -> Optional[FileHandler]:
        """
        Obtener un objeto por su ID
        
        Args:
            object_id: ID del objeto a buscar
            
        Returns:
            Objeto encontrado o None
        """
        return self.model_class.find_by_id(self.model_class.load_all(), object_id)
    
    def create(self, **data) -> FileHandler:
        """
        Crear un nuevo objeto
        
        Args:
            **data: Datos para el nuevo objeto
            
        Returns:
            Nuevo objeto creado
        """
        # Generar ID automáticamente si no se proporciona
        if 'id' not in data or not data['id']:
            existing_objects = self.model_class.all()
            new_id = self._generate_new_id(existing_objects)
            data['id'] = new_id
        
        new_object = self.model_class(**data)
        objects = self.model_class.load_all()
        objects.append(new_object)
        self.model_class.save_all(objects)
        
        return new_object
    
    def update(self, object_id: str, **data) -> Optional[FileHandler]:
        """
        Actualizar un objeto existente
        
        Args:
            object_id: ID del objeto a actualizar
            **data: Datos a actualizar
            
        Returns:
            Objeto actualizado o None si no se encontró
        """
        objects = self.model_class.load_all()
        target_object = None
        target_index = -1
        
        for i, obj in enumerate(objects):
            if str(obj.id) == str(object_id):
                target_object = obj
                target_index = i
                break
        
        if target_object is None:
            return None
        
        # Actualizar atributos
        for key, value in data.items():
            if hasattr(target_object, key):
                setattr(target_object, key, value)
        
        objects[target_index] = target_object
        self.model_class.save_all(objects)
        
        return target_object
    
    def delete(self, object_id: str) -> bool:
        """
        Eliminar un objeto
        
        Args:
            object_id: ID del objeto a eliminar
            
        Returns:
            True si se eliminó, False si no se encontró
        """
        objects = self.model_class.load_all()
        initial_count = len(objects)
        
        objects = [obj for obj in objects if str(obj.id) != str(object_id)]
        
        if len(objects) < initial_count:
            self.model_class.save_all(objects)
            return True
        return False
    
    def _apply_filters(self, objects: List[FileHandler]) -> List[FileHandler]:
        """Aplicar filtros a la lista de objetos"""
        filtered = objects.copy()
        
        for field, value in self._filters.items():
            if hasattr(objects[0], field):
                filtered = [obj for obj in filtered if getattr(obj, field) == value]
        
        return filtered
    
    def _apply_ordering(self, objects: List[FileHandler]) -> List[FileHandler]:
        """Aplicar ordenamiento a la lista de objetos"""
        if not objects or not hasattr(objects[0], self._order_by):
            return objects
        
        try:
            sorted_objects = sorted(
                objects, 
                key=lambda x: getattr(x, self._order_by),
                reverse=not self._ascending
            )
            return sorted_objects
        except (TypeError, AttributeError):
            # Si hay error en el ordenamiento, devolver sin ordenar
            return objects
    
    def _generate_new_id(self, objects: List[FileHandler]) -> str:
        """Generar un nuevo ID único"""
        if not objects:
            return "1"
        
        numeric_ids = []
        for obj in objects:
            try:
                if hasattr(obj, 'id') and obj.id:
                    numeric_ids.append(int(obj.id))
            except (ValueError, TypeError):
                continue
        
        return str(max(numeric_ids) + 1) if numeric_ids else "1"
    
    def exists(self, **filters) -> bool:
        """
        Verificar si existe al menos un objeto que coincida con los filtros
        
        Args:
            **filters: Filtros a aplicar
            
        Returns:
            True si existe al menos un objeto, False en caso contrario
        """
        return self.filter(**filters).count() > 0
    
    def bulk_create(self, data_list: List[Dict[str, Any]]) -> List[FileHandler]:
        """
        Crear múltiples objetos de una vez
        
        Args:
            data_list: Lista de diccionarios con datos para crear objetos
            
        Returns:
            Lista de objetos creados
        """
        objects = self.model_class.load_all()
        new_objects = []
        
        for data in data_list:
            if 'id' not in data or not data['id']:
                new_id = self._generate_new_id(objects + new_objects)
                data['id'] = new_id
            
            new_object = self.model_class(**data)
            new_objects.append(new_object)
        
        all_objects = objects + new_objects
        self.model_class.save_all(all_objects)
        
        return new_objects
    
    def bulk_update(self, updates: Dict[str, Dict[str, Any]]) -> int:
        """
        Actualizar múltiples objetos de una vez
        
        Args:
            updates: Diccionario con {object_id: {campo: nuevo_valor}}
            
        Returns:
            Número de objetos actualizados
        """
        objects = self.model_class.load_all()
        updated_count = 0
        
        for i, obj in enumerate(objects):
            obj_id = str(obj.id)
            if obj_id in updates:
                for field, value in updates[obj_id].items():
                    if hasattr(obj, field):
                        setattr(obj, field, value)
                        updated_count += 1
                objects[i] = obj
        
        if updated_count > 0:
            self.model_class.save_all(objects)
        
        return updated_count