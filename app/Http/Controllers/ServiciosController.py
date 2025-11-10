from app.Models.PersevoloORM.Request.Request import Request
from app.Models.Servicio import Servicio

class ServiciosController:
    def __init__(self):
        pass
    
    
    def get_servicios(self):
        return Servicio.all()
    def guardar_servicio(self, request: Request):
        
        (request.require('nombre','duracion','precio'))
        
        if(request.has_errors()):
            return False, request.errors
        
        try:
            
            data = request.data
            # Verificar que no exista un profesional con el mismo nombre y apellido
            servicios = self.get_servicios()
            existe = any((s.nombre == data['nombre'] and s.duracion == data['duracion'] and s.precio == data ['precio']) for s in servicios)
            if existe:
                return False

            # Crear nuevo profesional
            nuevo_servicio = Servicio(
                nombre=data['nombre'],
                duracion=data['duracion'],
                precio=data['precio'],
            )

            #profesionales.append(nuevo_profesional)
            #Profesional.save_all(profesionales)
            return nuevo_servicio.save()

            #modificar profesional
        except Exception as e:
            return False, {"error": f"Error al registrar servicio: {str(e)}"}

    
    def solicitar_guardar_servicio(self):
        nombre = input('Ingrese el nombre del servcio: ')
        duracion = int(input('Ingrese la duracion (min) del servcio: '))        
        precio = float(input('Ingrese el precio del servcio: '))
        
        if ((nombre == '' or duracion == '' or precio == '' ) or (duracion == 0 or precio == 0.00)):
            return False, {"error": "Hay campos incompletos, por favor intente denuevo"}        
        
        request = Request({
            'nombre': nombre.upper(),
            'duracion':duracion,
            'precio':precio
        })
        
        success = self.guardar_servicio(request)
    
        if success:
            print("Servicio registrado!")
                
    def modificar_servicio(self,request:Request):
        
        request.require('servicio')
        if request.has_errors():
            return False
        
        servicio = request.get('servicio') if isinstance(request.get('servicio'), Servicio) else None
        try:
            # Buscar cliente
            if not hasattr(servicio,'id'):
                return False
            
            if not servicio:
                return False
            
            return servicio.update()
            
        except Exception as e:
            return False, {"error": f"Error al actualizar servicio: {str(e)}"}
        
        pass
        
    def solicitar_modificar_servicio(self):
        servicio = self.buscar_servicio_by_nombre()
        
        if not servicio:
            print("Servicio no encontrado")
            return False
        
        print("Servicio: ",servicio)
        opc = input("¿Es correcto? (S/N): ")
        if ( opc.upper() == 'S'):
            
            nombre = input("Nuevo nombre (dejar vacío para no cambiar): ")
            duracion = input("Nueva duración (dejar vacío para no cambiar): ")
            precio = input("Nuevo precio (dejar vacío para no cambiar): ")

            servicio.nombre = nombre.upper() if nombre != '' else servicio.nombre.upper()
            servicio.duracion = duracion if duracion != '' and int(duracion) != 0 else servicio.duracion
            servicio.precio = precio if precio != '' and float(precio) != 0.00 else servicio.precio 
            request = Request({
                'servicio': servicio,
            })
            
            success = self.modificar_servicio(request)
            
            if success:
                print(f"Servicio actualizado!")
        elif opc.upper() == 'N':
            self.solicitar_modificar_servicio()
        else:
            print("Opción inválida")
            return False
        

    def buscar_servicio_by_nombre(self):
        nombre_s = input("Ingrese el nombre del servicio a que desea buscar: ")
        if nombre_s == '':
            print("Ingrese el nombre del servicio a buscar!")
            self.buscar_servicio_by_nombre()
            
        servicio = Servicio.where(nombre=nombre_s.upper())
        if not servicio:
            return False
        
        servicio= servicio[0]
        return servicio
    
    def solicitar_eliminar_servicio(self):
        print("Elija una opción: ")
        print("1.) Eliminar servicio por Nombre")
        print("2.) Eliminar TODOS los servicios")
        
        opcion = input("Ingrese la opción: ")
        
        if (opcion == '1'):
            servicio = self.buscar_servicio_by_nombre()
        
            if not servicio:
                print("Servicio no encontrado")
                return False
            
            print("Servicio: ",servicio)
            opc = input("¿Es correcto? (S/N): ")
            if ( opc.upper() == 'S'):
                return servicio.delete()
            elif (opc.upper() == 'N'):
                self.solicitar_eliminar_servicio()
            else:
                print("Opción incorrecta!")
                self.solicitar_eliminar_servicio()
            
        elif (opcion == '2'):
            opc = input("¿Está seguro que desea eliminar TODOS los SERVICIOS? (S/N): ")
            
            if(opc.upper() == 'S'):
                return Servicio.delete_all(Servicio)
            elif (opc.upper() == 'N'):
                self.solicitar_eliminar_servicio()
            else:
                print("Opción incorrecta")
                return False
        else:
            print("Opción incorrecta")
            return False
        
    