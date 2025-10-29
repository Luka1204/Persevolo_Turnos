import csv
import json
import os
from abc import ABC, abstractmethod
from datetime import datetime
from .FileHandler import FileHandler

class Model(ABC,FileHandler):

    _filename = None
    _fields = []

    def __init__(self, **kwargs):
        """Constructor genérico que inicializa todos los campos definidos en _fields"""
        for field in self._fields:
            # Si no se proporciona el campo, usar valor por defecto
            setattr(self, field, kwargs.get(field, ""))
    
    def __str__(self):
        """Representación genérica del objeto"""
        class_name = self.__class__.__name__
        attributes = []
        
        for field in self._fields:
            value = getattr(self, field, None)
            if value is not None:
                attributes.append(f"{field}={value}")
        
        attributes_str = ", ".join(attributes)
        return f"{class_name}({attributes_str})"
    
    def __repr__(self): #Representación en cadena de la instancia del modelo
        _fields_ = ', '.join(f"{field}={getattr(self, field)!r}" for field in self._fields)
        return f"{self.__class__.__name__}({_fields_})"
    
    def __eq__(self, other): #Comparar dos instancias del modelo
        if not isinstance(other, self.__class__):
            return False
        return all(getattr(self, _field_) == getattr(other, _field_) for _field_ in self._fields)
    
    def __hash__(self): #Generar un hash para la instancia del modelo
        return hash(tuple(getattr(self, _field_) for _field_ in self._fields))
    
    def _get_default_value(self, field):
        """Obtener valor por defecto según el tipo de campo"""
        if field == 'id':
            return None
        elif field == 'estado':
            return 'pendiente'
        else:
            return ""
    
    
    def to_dict(self): #Convertir la instancia del modelo a un diccionario
        return {field:getattr(self,field) for field in self._fields}
    
    
    def save(self): #Guardar la instancia del modelo en el archivo CSV
        self.id = self.generar_id_unico(self.__class__.all())
        nom_archivo = self.get_filename()
        archivo_bool = os.path.isfile(nom_archivo)
        with open(nom_archivo, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.get_fields())
            if not archivo_bool:
                writer.writeheader()
            writer.writerow(self.to_dict())
            file.flush()
            os.fsync(file.fileno())
            print(f"Se guardó la instancia de {self.__class__.__name__} en {nom_archivo}")


    @classmethod
    def find_by(cls, **kwargs): #Buscar instancias del modelo que coincidan con los criterios dados
        res = []
        for model in cls.all():
            if all(getattr(model, key) == value for key, value in kwargs.items()):
                res.append(model)
        return res
    
    @classmethod
    def find_one_by(cls, **kwargs): #Buscar una única instancia del modelo que coincida con los criterios dados
        for model in cls.all():
            if all(getattr(model, key) == value for key, value in kwargs.items()):
                return model
        return None
    
    @classmethod
    def delete_by(cls, **kwargs): #Eliminar instancias del modelo que coincidan con los criterios dados
        instancias = cls.all()
        instancias_conservar = [instancia for instancia in instancias if not all(getattr(instancia, key) == value for key, value in kwargs.items())]
        cls.save_all(instancias_conservar)
        print(f"Se eliminaron las instancias de {cls.__name__} que coinciden con {kwargs}")
        return len(instancias) - len(instancias_conservar)

    @classmethod
    def count(cls): #Contar el número de instancias del modelo en el archivo CSV
        return len(cls.all())
    
    @classmethod
    def exists(cls, **kwargs): #Verificar si existe una instancia del modelo que coincida con los criterios dados
        return any(all(getattr(instancia, key) == value for key, value in kwargs.items()) for instancia in cls.all())
    
    @classmethod
    def get_fields(cls): #Obtener los campos del modelo
        return cls._fields
    
    @classmethod   
    def generar_id_unico(self, objetos):
        """Generar un ID único para un nuevo objeto"""
        if not objetos:
            return "1"
        
        # Usar el método find de la clase base
        ids = []
        for obj in objetos:
            if hasattr(obj, 'id') and obj.id:
                try:
                    ids.append(int(obj.id))
                except (ValueError, TypeError):
                    continue
        
        return str(max(ids) + 1) if ids else "1"
    

