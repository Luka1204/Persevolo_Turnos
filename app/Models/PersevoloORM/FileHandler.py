import csv
import json
import os

class FileHandler():
    @classmethod
    def get_filename(cls): #Obtener el nombre del archivo CSV asociado al modelo
        if cls._filename is None:
            cls._filename = f"{cls.__name__.lower()}s.csv"
        return cls._filename
    
    @classmethod 
    def convert_to_json(cls,json_nom): #Convertir todas las instancias del modelo a un archivo JSON
        objects = cls.all()
        data = [obj.to_dict() for obj in objects]
        with open(json_nom, mode='w', encoding='utf-8') as json_obj:
            json.dump(data, json_obj, indent=4)
            print(f"Se guardaron las instancias de {cls.__name__} en el archivo JSON {json_nom}")

    @classmethod
    def load_from_json(cls,json_nom): #Cargar instancias del modelo desde un archivo JSON
        if not os.path.exists(json_nom):
            print(f"El archivo JSON {json_nom} no existe.")
            return []
        
        with open(json_nom, mode='r', encoding='utf-8') as json_obj:
            data = json.load(json_obj)
            instancias = [cls.from_dict(i) for i in data]
            cls.save_all(instancias)
            return instancias
        
    @classmethod
    def from_dict(cls,data): #Crear una instancia del modelo a partir de un diccionario
        return cls(**data)
    
    @classmethod
    def all(cls): #Obtener todas las instancias del modelo desde el archivo CSV
        instancias = []
        nom_archivo = cls.get_filename()
        if not os.path.exists(nom_archivo):
            return instancias

        with open(nom_archivo, mode='r', newline='', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            for row in reader:
                data = {field: row[field] for field in cls.get_fields()}
                instancias.append(cls(**data))
        return instancias
    
    @classmethod
    def delete_all(cls): #Eliminar todas las instancias del modelo
        nom_archivo = cls.get_filename()
        if os.path.exists(nom_archivo):
            os.remove(nom_archivo)
            print(f"Se eliminaron todas las instancias de {cls.__name__} al eliminar {nom_archivo}")
        else:
            print(f"No se encontró el archivo para {cls.__name__}, nada que eliminar.")
            return 0
        return 1
    
    @classmethod
    def save_all(cls,objects): #Guardar todas las instancias del modelo en el archivo
        nom_archivo = cls.get_filename()
        with open(nom_archivo, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=cls.get_fields())
            writer.writeheader()
            for obj in objects:
                writer.writerow(obj.to_dict())
            writer.flush()
            os.fsync(file.fileno())
        print(f"Se guardaron todas las instancias de {cls.__name__} en {nom_archivo}")