# Manual de Usuario - Sistema de Gestión de Turnos Persevolo

## Índice
1. Introducción
2. Inicio del Sistema
3. Menú Principal
4. Gestión de Clientes
5. Gestión de Turnos
6. Gestión de Profesionales
7. Gestión de Atenciones
8. Gestión de Servicios
9. Administración
10. Solución de Problemas Comunes

## 1. Introducción

Bienvenido al Sistema de Gestión de Turnos Persevolo. Este sistema le permite gestionar de manera eficiente los turnos, clientes, profesionales y servicios de su negocio.

## 2. Inicio del Sistema

Para iniciar el sistema:
1. Abra una terminal o línea de comandos
2. Navegue hasta la carpeta del sistema
3. Ejecute el comando: `python main.py`

## 3. Menú Principal

Al iniciar el sistema, verá el siguiente menú:
```
=== SISTEMA DE TURNOS ===
1. Clientes
2. Turnos
3. Profesionales
4. Atenciones
5. Servicios
6. ADMIN
7. Salir
```

Seleccione una opción ingresando el número correspondiente y presione Enter.

## 4. Gestión de Clientes

### Menú Clientes
```
=== MENÚ CLIENTES ===
1. Registrar cliente
2. Buscar cliente
3. Actualizar cliente
4. Eliminar cliente
5. Volver al menú principal
```

### 4.1 Registrar un Nuevo Cliente
1. Seleccione opción 1
2. Ingrese los datos solicitados del cliente
3. Confirme el registro

### 4.2 Buscar un Cliente
1. Seleccione opción 2
2. Ingrese el DNI del cliente
3. El sistema mostrará los datos del cliente si existe

### 4.3 Actualizar Datos de Cliente
1. Seleccione opción 3
2. Ingrese el DNI del cliente
3. Ingrese los nuevos datos

### 4.4 Eliminar Cliente
1. Seleccione opción 4
2. Ingrese el DNI del cliente a eliminar
3. Confirme la eliminación

## 5. Gestión de Turnos

### Menú Turnos
```
=== MENÚ TURNOS ===
1. Solicitar turno
2. Cancelar turno
3. Consultar turno
4. Volver al menú principal
```

### 5.1 Solicitar un Turno
1. Seleccione opción 1
2. Siga los pasos para seleccionar:
   - Profesional
   - Fecha
   - Horario disponible
3. Confirme la reserva

### 5.2 Cancelar un Turno
1. Seleccione opción 2
2. Ingrese el ID del turno
3. Confirme la cancelación

### 5.3 Consultar un Turno
1. Seleccione opción 3
2. Ingrese el ID del turno o los criterios de búsqueda
3. El sistema mostrará los detalles del turno

## 6. Gestión de Profesionales

### Menú Profesionales
```
=== MENÚ PROFESIONALES ===
1. Registrar profesional
2. Buscar profesional
3. Actualizar profesional
4. Eliminar profesional
5. Búsqueda de Turnos por Profesional
6. Volver al menú principal
```

### 6.1 Registrar Profesional
1. Seleccione opción 1
2. Ingrese los datos del profesional
3. Confirme el registro

### 6.2 Buscar Profesional
1. Seleccione opción 2
2. Ingrese el DNI del profesional
3. Visualice los datos

### 6.3 Actualizar Datos de Profesional
1. Seleccione opción 3
2. Ingrese el DNI del profesional
3. Modifique los datos necesarios

### 6.4 Eliminar Profesional
1. Seleccione opción 4
2. Ingrese el DNI del profesional
3. Confirme la eliminación

### 6.5 Buscar Turnos por Profesional
1. Seleccione opción 5
2. Ingrese el DNI del profesional
3. Visualice los turnos asignados

## 7. Gestión de Atenciones

### Menú Atenciones
```
=== MENÚ ATENCIONES ===
1. Registrar atenciones
2. Buscar atenciones
3. Editar atención
4. Eliminar atención
5. Volver al menú principal
```

### 7.1 Registrar Atención
1. Seleccione opción 1
2. Ingrese los datos de la atención
3. Confirme el registro

### 7.2 Buscar Atenciones
1. Seleccione opción 2
2. Ingrese los criterios de búsqueda
3. Visualice los resultados

## 8. Gestión de Servicios

### Menú Servicios
```
=== MENÚ SERVICIOS ===
1. Registrar servicio
2. Actualizar servicio
3. Eliminar servicio
4. Volver al menú principal
```

### 8.1 Registrar Servicio
1. Seleccione opción 1
2. Ingrese los datos del servicio
3. Confirme el registro

### 8.2 Actualizar Servicio
1. Seleccione opción 2
2. Seleccione el servicio a modificar
3. Ingrese los nuevos datos

## 9. Administración

### Menú Administración
```
=== MENÚ ADMINISTRACIÓN ===
1. Generación de turnos
2. Volver al menú principal
```

### 9.1 Generación Masiva de Turnos
1. Seleccione opción 1
2. Ingrese la fecha para generar turnos
3. El sistema generará automáticamente los turnos disponibles

## 10. Solución de Problemas Comunes

### 10.1 No se puede registrar un turno
- Verifique que el profesional esté disponible en ese horario
- Confirme que la fecha seleccionada sea válida
- Asegúrese de que el cliente esté registrado en el sistema

### 10.2 Error al buscar cliente/profesional
- Verifique que el DNI ingresado sea correcto
- Confirme que la persona esté registrada en el sistema

### 10.3 No se pueden generar turnos
- Verifique que la fecha sea futura
- Confirme que haya profesionales disponibles
- Asegúrese de que los servicios estén correctamente configurados

### 10.4 Consejos Generales
- Siempre guarde los IDs de turnos para futuras referencias
- Mantenga actualizada la información de clientes y profesionales
- Realice las cancelaciones con suficiente anticipación
- En caso de error persistente, contacte al soporte técnico