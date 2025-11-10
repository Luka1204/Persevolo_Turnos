# Manual Técnico - Sistema de Gestión de Turnos Persevolo

## 1. Arquitectura del Sistema

El sistema está desarrollado en Python y sigue una arquitectura MVC (Modelo-Vista-Controlador) con las siguientes capas:

### 1.1 Estructura de Directorios

```
app/
├── Http/
│   └── Controllers/       # Controladores de la aplicación
├── Models/               # Modelos de datos
│   └── PersevoloORM/     # ORM personalizado
└── resources/
    └── views/            # Vistas de la aplicación
DB/                      # Almacenamiento de datos en CSV/JSON
```

### 1.2 Componentes Principales

#### Models (app/Models/)
- `Cliente.py`: Modelo para gestión de clientes
- `Profesional.py`: Modelo para gestión de profesionales
- `Turno.py`: Modelo para gestión de turnos
- `Atencion.py`: Modelo para gestión de atenciones
- `Servicio.py`: Modelo para gestión de servicios
- `Dia.py`: Modelo para gestión de días y horarios

#### Controllers (app/Http/Controllers/)
- `ClienteController.py`: Control de operaciones de clientes
- `ProfesionalController.py`: Control de operaciones de profesionales
- `TurnoController.py`: Control de operaciones de turnos
- `AtencionController.py`: Control de operaciones de atenciones
- `ServiciosController.py`: Control de operaciones de servicios
- `DiasController.py`: Control de operaciones de días

#### Views (app/resources/views/)
- `MenuView.py`: Interfaz de usuario en consola

## 2. Base de Datos

El sistema utiliza un sistema de almacenamiento basado en archivos CSV/JSON ubicado en el directorio `DB/`. Cada entidad tiene su propio archivo de almacenamiento:

- `clientes.csv/json`
- `profesionales.csv/json`
- `turnos.csv/json`
- `atenciones.csv/json`
- `servicios.csv/json`
- `dias.csv/json`

## 3. Funcionalidades Principales

### 3.1 Gestión de Clientes
- Registro de nuevos clientes
- Búsqueda de clientes
- Actualización de datos de clientes
- Eliminación de clientes

### 3.2 Gestión de Profesionales
- Registro de profesionales
- Búsqueda de profesionales
- Actualización de datos de profesionales
- Eliminación de profesionales
- Búsqueda de turnos por profesional

### 3.3 Gestión de Turnos
- Solicitud de turnos
- Cancelación de turnos
- Consulta de turnos
- Generación masiva de turnos (función administrativa)

### 3.4 Gestión de Atenciones
- Registro de atenciones
- Búsqueda de atenciones
- Edición de atenciones
- Eliminación de atenciones

### 3.5 Gestión de Servicios
- Registro de servicios
- Actualización de servicios
- Eliminación de servicios

## 4. Flujo de Datos

1. El usuario interactúa con el sistema a través de `MenuView`
2. Los controladores procesan las solicitudes y aplican la lógica de negocio
3. Los modelos gestionan el acceso y manipulación de datos
4. El ORM personalizado (PersevoloORM) maneja la persistencia de datos

## 5. Sistema de ORM Personalizado

El sistema incluye un ORM personalizado (PersevoloORM) que proporciona:
- Manejo de archivos CSV/JSON
- Validación de datos
- Operaciones CRUD básicas
- Gestión de modelos de datos

## 6. Consideraciones Técnicas

### 6.1 Requisitos del Sistema
- Python 3.x
- Sistema de archivos con permisos de lectura/escritura

### 6.2 Mantenimiento
- Los archivos CSV/JSON deben ser respaldados periódicamente
- Se recomienda mantener un registro de las operaciones realizadas
- Es importante validar la integridad de los datos periódicamente

## 7. Seguridad

- Los datos sensibles deben ser manejados con precaución
- Se recomienda implementar un sistema de respaldo regular
- El acceso a los archivos de la base de datos debe estar restringido

## 8. Extensibilidad

El sistema está diseñado para ser extensible:
- Nuevos módulos pueden ser agregados siguiendo la estructura MVC
- El ORM personalizado permite agregar nuevos modelos fácilmente
- La interfaz de usuario puede ser modificada o reemplazada sin afectar la lógica de negocio