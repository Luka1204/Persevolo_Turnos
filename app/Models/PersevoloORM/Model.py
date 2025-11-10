import csv
import json
import os
from abc import ABC
from datetime import datetime
from .FileHandler import FileHandler
from .Validators import Validator


class Model(ABC, FileHandler):
    _filename = None
    _fields = []

    def __init__(self, **kwargs):
        """Constructor genérico que inicializa todos los campos definidos en _fields

        Para campos complejos (listas/dicts) se aceptan objetos Python en kwargs.
        """
        self._validator = Validator()  # Crear validador PRIMERO
        for field in self._fields:
            default = self._get_default_value(field)
            setattr(self, field, kwargs.get(field, default))

    def __str__(self):
        class_name = self.__class__.__name__
        attributes = []
        for field in self._fields:
            value = getattr(self, field, None)
            if value is not None and value != "":
                attributes.append(f"{field}={value}")
        attributes_str = ", ".join(attributes)
        return f"{class_name}({attributes_str})"

    def __repr__(self):
        _fields_ = ', '.join(f"{field}={getattr(self, field)!r}" for field in self._fields)
        return f"{self.__class__.__name__}({_fields_})"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return all(getattr(self, _field_) == getattr(other, _field_) for _field_ in self._fields)

    def __hash__(self):
        return hash(tuple(getattr(self, _field_) for _field_ in self._fields))

    @classmethod
    def all(cls):
        instancias = []
        nom_archivo = cls.get_filename()
        path = 'DB/' + nom_archivo
        if not os.path.exists(path):
            return instancias

        with open(path, mode='r', newline='', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo, skipinitialspace=True)
            for row in reader:
                data = {}
                for field in cls.get_fields():
                    raw = row.get(field, '')
                    if raw is None:
                        data[field] = ''
                        continue
                    raw = raw.strip()
                    if raw.startswith('{') or raw.startswith('['):
                        try:
                            data[field] = json.loads(raw)
                            continue
                        except Exception:
                            pass
                    data[field] = raw
                instancias.append(cls(**data))
        return instancias

    def validate(self):
        """
        Recorre los campos definidos en _fields y valida con los validadores disponibles.
        Devuelve True si pasa, o un dict {campo: mensaje} con errores.
        """
        print("Estoy acá literalmente - Validando instancia")
        errors = {}
        
        for field in self._fields:
            if hasattr(self, field):
                value = getattr(self, field)
        
        for field in getattr(self, "_fields", []):
            if field == 'id':
                continue
            if hasattr(self, field):
                val = getattr(self, field)
                
                # Usar el método mejorado del validador
                error_msg = self._validator.validate_field(field, val)
                
                if error_msg:
                    errors[field] = error_msg
        
        return True if not errors else errors

    def _get_default_value(self, field):
        if field == 'id':
            return None
        elif field == 'estado':
            return 'pendiente'
        elif field == 'atenciones':
            return []
        else:
            return ""

    def to_dict(self):
        """Valores Python list/dict sin serializar. Útil para convert_to_json."""
        return {field: getattr(self, field) for field in self._fields}

    def to_csv_dict(self):
        """Valores preparados para CSV: listas/dicts -> JSON strings."""
        csv_dict = {}
        for field in self._fields:
            val = getattr(self, field)
            if isinstance(val, (dict, list)):
                try:
                    csv_dict[field] = json.dumps(val, ensure_ascii=False)
                except Exception:
                    csv_dict[field] = str(val)
            elif val is None:
                csv_dict[field] = ''
            else:
                csv_dict[field] = val
        return csv_dict
    
    def save(self):
        """
        Antes de persistir, validar. Si hay errores devuelve (False, errores).
        En caso contrario sigue con el flujo normal de guardado.
        """
        valid = self.validate()
        
        if valid is not True:
            print(f"Errores de validación:")
            for key,value in valid.items():
                print(f"Campo:{key}, {value}")
            return False
        
        # Generar ID si no existe
        if not hasattr(self, 'id') or not self.id:
            self.id = self.generar_id_unico()
            
        nom_archivo = self.get_filename()
        path = 'DB/' + nom_archivo
        archivo_bool = os.path.isfile(path)
        
        try:
            with open(path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.get_fields())
                if not archivo_bool:
                    writer.writeheader()
                writer.writerow(self.to_csv_dict())
                file.flush()
                os.fsync(file.fileno())
                print(f"Se guardó la instancia de {self.__class__.__name__} en {nom_archivo}")
                self.convert_to_json(f"{nom_archivo.rsplit('.',1)[0]}.json")
                return True, "Guardado exitoso"
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False, f"Error al guardar: {e}"

    @classmethod
    def find_by(cls, **kwargs):
        res = []
        for model in cls.all():
            if all(getattr(model, key) == value for key, value in kwargs.items()):
                res.append(model)
        return res

    @classmethod
    def find_one_by(cls, **kwargs):
        for model in cls.all():
            if all(getattr(model, key) == value for key, value in kwargs.items()):
                return model
        return None

    @classmethod
    def delete_by(cls, **kwargs):
        instancias = cls.all()
        instancias_conservar = [instancia for instancia in instancias if not all(getattr(instancia, key) == value for key, value in kwargs.items())]
        cls.save_all(instancias_conservar)
        print(f"Se eliminaron las instancias de {cls.__name__} que coinciden con {kwargs}")
        return len(instancias) - len(instancias_conservar)

    @classmethod
    def count(cls):
        return len(cls.all())

    @classmethod
    def exists(cls, **kwargs):
        return any(all(getattr(instancia, key) == value for key, value in kwargs.items()) for instancia in cls.all())

    @classmethod
    def get_fields(cls):
        return cls._fields

    @classmethod
    def where(cls, **kwargs):
        instancias = cls.all()
        resultados = []
        for instancia in instancias:
            if all(getattr(instancia, key) == value for key, value in kwargs.items() if value is not None and value != ""):
                resultados.append(instancia)
        return resultados

    @classmethod
    def generar_id_unico(cls):
        objetos = cls.all()
        ids = []
        for obj in objetos:
            if hasattr(obj, 'id') and obj.id:
                try:
                    ids.append(int(obj.id))
                except (ValueError, TypeError):
                    continue
        return str(max(ids) + 1) if ids else "1"

    def update(self):
        if not hasattr(self, 'id') or not self.id:
            raise ValueError("La instancia debe tener un ID para actualizarse.")
        valid = self.validate()
        
        if valid is not True:
            print(f"Errores de validación:")
            for key,value in valid.items():
                print(f"Campo:{key}, {value}")
            return False
        
        self.__class__.update_csv(self, **self.to_dict())

    def delete(self):
        if not hasattr(self, 'id') or not self.id:
            raise ValueError("La instancia debe tener un ID para eliminarse.")
        deleted_count = self.__class__.delete_by(id=self.id)
        return deleted_count

    def delete_all(self):
        deleted_count = self.delete_by()
        return deleted_count