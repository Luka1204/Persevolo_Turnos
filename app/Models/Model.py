import csv
import json
import os
from abc import ABC, abstractmethod
from datetime import datetime

class Model(ABC):

    _filename = None
    _fields = []

    def __init__(self, ** kwargs): #kwargs es un diccionario que va a recibir el constructor para asignar los valores del modelo
        for field in self._fields:
            setattr(self, field, kwargs.get(field))

    @classmethod
    def get_filename(cls): #Obtener el nombre del archivo CSV asociado al modelo
        if cls._filename is None:
            cls._filename = f"{cls.__name__.lower()}s.csv"
        return cls._filename
    
    @classmethod
    def get_fields(cls): #Obtener los campos del modelo
        return cls._fields
    

    def to_dict(self): #Convertir la instancia del modelo a un diccionario
        return {field:getattr(self,field) for field in self._fields}
    
    @classmethod
    def from_dict(cls,data): #Crear una instancia del modelo a partir de un diccionario
        return cls(**data)
    
    @classmethod
    def all(cls): #Obtener todas las instancias del modelo desde el archivo CSV
        instances = []
        filename = cls.get_filename()
        if not os.path.exists(filename):
            return instances
        
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                instance_data = {field: row[field] for field in cls.get_fields()}
                instances.append(cls(**instance_data))
        return instances
    
    def save(self): #Guardar la instancia del modelo en el archivo CSV
        filename = self.get_filename()
        file_exists = os.path.isfile(filename)
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.get_fields())
            if not file_exists:
                writer.writeheader()
            writer.writerow(self.to_dict())
            writer.flush()
            os.fsync(file.fileno())
            # Optionally, you can implement additional logic here, such as logging or notifying other parts of your application.
            print(f"Saved {self.__class__.__name__} instance to {filename}")       

    @classmethod
    def save_all(cls,objects): #Guardar todas las instancias del modelo en el archivo CSV
        filename = cls.get_filename()
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=cls.get_fields())
            writer.writeheader()
            for obj in objects:
                writer.writerow(obj.to_dict())
            writer.flush()
            os.fsync(file.fileno())
            print(f"Saved all {cls.__name__} instances to {filename}") 

    @classmethod
    def find_by(cls, **kwargs): #Buscar instancias del modelo que coincidan con los criterios dados
        results = []
        for instance in cls.all():
            if all(getattr(instance, key) == value for key, value in kwargs.items()):
                results.append(instance)
        return results
    
    @classmethod
    def find_one_by(cls, **kwargs): #Buscar una única instancia del modelo que coincida con los criterios dados
        for instance in cls.all():
            if all(getattr(instance, key) == value for key, value in kwargs.items()):
                return instance
        return None
    
    @classmethod
    def delete_by(cls, **kwargs): #Eliminar instancias del modelo que coincidan con los criterios dados
        instances = cls.all()
        instances_to_keep = [instance for instance in instances if not all(getattr(instance, key) == value for key, value in kwargs.items())]
        cls.save_all(instances_to_keep)
        print(f"Deleted instances of {cls.__name__} matching {kwargs}")
        return len(instances) - len(instances_to_keep)
    

    @classmethod
    def delete_all(cls): #Eliminar todas las instancias del modelo
        filename = cls.get_filename()
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Deleted all instances of {cls.__name__} by removing {filename}")
        else:
            print(f"No file found for {cls.__name__}, nothing to delete.")
            return 0
        return 1
    
    @classmethod 
    def convert_to_json(cls,json_filename): #Convertir todas las instancias del modelo a un archivo JSON
        objects = cls.all()
        data = [obj.to_dict() for obj in objects]
        with open(json_filename, mode='w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)
            print(f"Converted {cls.__name__} instances to JSON file {json_filename}")

    @classmethod
    def load_from_json(cls,json_filename): #Cargar instancias del modelo desde un archivo JSON
        if not os.path.exists(json_filename):
            print(f"JSON file {json_filename} does not exist.")
            return []
        
        with open(json_filename, mode='r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            instances = [cls.from_dict(item) for item in data]
            cls.save_all(instances)
            return instances
    

