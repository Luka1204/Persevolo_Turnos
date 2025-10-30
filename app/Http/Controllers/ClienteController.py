from app.Models.PersevoloORM.Request.Request import Request
from app.Models.Cliente import Cliente

class ClienteController:
    def guardar_cliente(self, request: Request):
        """
        Registrar nuevo cliente con validación
        
        Args:
            request: Objeto Request con datos del cliente
            
        Returns:
            Tuple (success, data_or_error)
        """
        # Validar datos requeridos
        request.require('nombre','dni', 'telefono', 'email')
        
        # Validaciones específicas
        (request.validate_min_length('nombre', 2)
           .validate_max_length('nombre', 100)
           .validate_phone('telefono')
           .validate_email('email')
           .validate_min_length('telefono', 8))
        
        if request.has_errors():
            return False, request.errors
        
        # Limpiar y preparar datos
        request.clean()
        data = request.validated_data
        
        try:
            # Verificar que no exista cliente con mismo email
            clientes_existentes = Cliente.all()
            for cliente in clientes_existentes:
                if cliente.email == data['email'] or cliente.dni == data.get('dni', None):
                    return False, {"email": "Ya existe un cliente con este email"}
            
            # Crear nuevo cliente
            nuevo_cliente = Cliente(
                nombre=data['nombre'],
                apellido=data['apellido'],
                dni=data['dni'],
                telefono=data['telefono'],
                email=data['email'],     
            )
            
            # Guardar
            nuevo_cliente.save()
            
            return True, nuevo_cliente
            
        except Exception as e:
            return False, {"error": f"Error al registrar cliente: {str(e)}"}
    
    def actualizar_cliente(self, request: Request):

        request.require('cliente')
        if request.has_errors():
            return False, request.errors
        
        cliente = request.get('cliente') if isinstance(request.get('cliente'), Cliente) else None
        try:
            # Buscar cliente
            if not hasattr(cliente,'id'):
                return False, {"error": "ID de cliente inválido"}
            
            if not cliente:
                return False, {"error": "Cliente no encontrado"}
            
            cliente.update()
            return True, Cliente.all()
            
        except Exception as e:
            return False, {"error": f"Error al actualizar cliente: {str(e)}"}
    
    def buscar_cliente(self, request: Request):
        """
        Buscar cliente con filtros
        
        Args:
            request: Objeto Request con criterios de búsqueda
            
        Returns:
            Tuple (success, data_or_error)
        """
        try:
            clientes = Cliente.all()
            resultados = []
            
            # Aplicar filtros si están presentes
            filtros = {}

            if request.get('nombre'):
                filtros['nombre'] = request.get('nombre')
            if request.get('email'):
                filtros['email'] = request.get('email')
            if request.get('telefono'):
                filtros['telefono'] = request.get('telefono')
            if request.get('apellido'):
                filtros['apellido'] = request.get('apellido')
            if request.get('dni'):
                filtros['dni'] = request.get('dni')

            for cliente in clientes:
                coincide = True
                for campo, valor in filtros.items():
                    if valor.lower() not in getattr(cliente, campo, '').lower():
                        coincide = False
                        break
                if coincide:
                    resultados.append(cliente)
            
            return True, resultados
            
        except Exception as e:
            return False, {"error": f"Error al buscar clientes: {str(e)}"}
        
    def registrar_cliente(self):
        print("\n--- REGISTRAR CLIENTE ---")
        
        # Recoger datos del usuario
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        dni = input("DNI: ")
        email = input("Email: ")
        telefono = input("Teléfono: ")
        
        
        # Crear Request
        request = Request({
            'nombre': nombre,
            'apellido':apellido,
            'dni':dni,
            'email': email,
            'telefono': telefono
        })
        
        # Llamar al controlador
        success, result = self.guardar_cliente(request)
        
        if success:
            print(f"Cliente registrado: {result}")
        else:
            print("Errores:")
            for campo, error in result.items():
                print(f"   - {campo}: {error}")
    
    def solicitar_turno(self):
        print("\n--- SOLICITAR TURNO ---")
        
        # Recoger datos
        cliente_id = input("ID del cliente: ")
        profesional_id = input("ID del profesional: ")
        fecha = input("Fecha (YYYY-MM-DD): ")
        hora = input("Hora (HH:MM): ")
        servicio = input("Servicio: ")
        
        # Crear Request
        request = Request({
            'cliente_id': cliente_id,
            'profesional_id': profesional_id,
            'fecha': fecha,
            'hora': hora,
            'servicio': servicio
        })
        
        # Llamar al controlador
        success, result = self.turno_controller.solicitar_turno(request)
        
        if success:
            print(f"Turno solicitado: {result}")
        else:
            print("Errores:")
            for campo, error in result.items():
                print(f"   - {campo}: {error}")

    def solicitar_buscar_cliente(self):
        print("\n--- BUSCAR CLIENTE ---")
        
        nombre = input("Nombre (opcional): ")
        apellido = input("Apellido (opcional): ")
        dni = input("DNI (opcional): ")

        email = input("Email (opcional): ")
        telefono = input("Teléfono (opcional): ")
        
        request = Request({
            'nombre': nombre,
            'apellido':apellido,
            'dni':dni,
            'email': email,
            'telefono': telefono
        })
        
        success, result = self.buscar_cliente(request)
        
        if success:
            if result:
                print("Clientes encontrados:")
                for cliente in result:
                    print(f"  - {cliente}")
            else:
                print("No se encontraron clientes")
        else:
            print(f"Error: {result}")
    
    def cancelar_turno(self):
        print("\n--- CANCELAR TURNO ---")
        
        turno_id = input("ID del turno a cancelar: ")
        
        request = Request({'turno_id': turno_id})
        success, result = self.turno_controller.cancelar_turno(request)
        
        if success:
            print(f"Turno cancelado: {result}")
        else:
            print(f"Error: {result}")
        
    def eliminar_cliente(self):
        cliente_dni = input("DNI del cliente a eliminar: ")
        cliente = None
        cliente = Cliente.where(Cliente,dni=cliente_dni)

        if not cliente:
            print("Cliente no encontrado")
            return False
        
        cliente = cliente[0]
        print("Cliente: ",cliente)

        confirmacion = input(f"¿Está seguro que desea eliminar al cliente {cliente.nombre} {cliente.apellido}? (s/n): ")
        if confirmacion.lower() != 's':
            print("Eliminación cancelada")
            return False

        try:
            cliente.delete()
            print("Cliente eliminado exitosamente")
            return True
        except Exception as e:
            print(f"Error al eliminar cliente: {str(e)}")
            return False

    def solicitar_eliminar_cliente(self):
        print("\n--- ELIMINAR CLIENTE ---")
        print("1.)Eliminar por DNI")
        print("2.)Eliminar todos los clientes")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            self.eliminar_cliente()
        elif opcion == "2":
            print("Advertencia: Esta acción eliminará todos los clientes. ¿Desea continuar? (s/n)")
            confirmar = input().lower()
            if confirmar == 's': 
                Cliente.delete_all()
            
            print("Se eliminaron todos los clientes")
        
        
    def solicitar_actualizar_cliente(self):
        print("\n--- ACTUALIZAR CLIENTE ---")
        cliente_dni = input("DNI del cliente a actualizar: ")
        cliente = None
        cliente = Cliente.where(Cliente,dni=cliente_dni)
        print("Cliente: ",cliente)

        if not cliente:
            print("Cliente no encontrado")
            return False
        
        cliente = cliente[0]
        print("Cliente: ",cliente)

        nombre = input("Nuevo nombre (dejar vacío para no cambiar): ")
        telefono = input("Nuevo teléfono (dejar vacío para no cambiar): ")
        email = input("Nuevo email (dejar vacío para no cambiar): ")

        cliente.nombre = nombre if nombre != '' else cliente.nombre
        cliente.telefono = telefono if telefono != '' else cliente.telefono
        cliente.email = email if email != '' else cliente.email 

        print("Cliente: ",cliente)
        request = Request({
            'cliente': cliente,
        })
        
        success, result = self.actualizar_cliente(request)
        
        if success:
            print(f"Cliente actualizado: {result}")
        else:
            print("Errores:")
            for campo, error in result.items():
                print(f"   - {campo}: {error}")