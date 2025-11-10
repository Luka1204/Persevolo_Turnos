from app.Models.PersevoloORM.Request.Request import Request
from app.Models.Atencion import Atencion
from app.Models.Dia import Dia
from app.Models.Servicio import Servicio

from app.Http.Controllers.ServiciosController import ServiciosController
from app.Http.Controllers.DiasController import DiasController


from datetime import time


class AtencionController:
    def __init__(self):
        self._servicios_controller = ServiciosController()
        self._dias_controller = DiasController()
        
    
    def get_atenciones(self):
        return Atencion.all()

    def guardar_atencion(self, request:Request):
        # Atenciones no dependen del profesional; se definen por servicio/día/hora
        (request.require('hora_desde','hora_hasta','dia','id_servicio','cantidad'))

        if(request.has_errors()):
            return False, request.errors

        try:
            data = request.data
            atenciones = Atencion.all()

            if (any((a.hora_desde == data['hora_desde'] and a.hora_hasta == data['hora_hasta'] and a.id_servicio == data['id_servicio']) for a in atenciones)):
                return False, {"error":"Esta atención ya existe!"}

            atencion = Atencion(hora_desde=data["hora_desde"],hora_hasta=data["hora_hasta"],dia=data["dia"],id_servicio=data["id_servicio"],cantidad=data["cantidad"])

            return atencion.save()
        except Exception as e:
            return False, {"error": f"Error al registrar la atención: {str(e)}"}
    def solicitar_guardar_atencion(self):
        
        try:
            
            dias = self._dias_controller.get_dias()
            servicios = self._servicios_controller.get_servicios()
            
            if(len(servicios) == 0):
                print("No hay servicios, cargados! Para registrar atenciones debe cargar servicios!")
                return False
            
            format_code_3 = "%H:%M"
            hora_desde = time.fromisoformat(input("Ingrese la hora desde donde comienza la atención con el siguiente formato (HH:MM:SS): "))
            hora_hasta =  time.fromisoformat(input("Ingrese la hora hasta donde finaliza la atención con el siguiente formato (HH:MM:SS): "))

            print(hora_desde,hora_hasta)
            print("Seleccione el día de la atencion: ")
            for dia in dias:
                print(dia.id,")"," ",dia.nombre)
            
            opc_dia = int(input("Ingrese una opción: "))
            
            dia = dias[opc_dia-1]
            
            
            
            for servicio in servicios:
                print(servicio.id,")"," ",servicio.nombre)
                
            opc_servicio = int(input("Ingrese una opción: "))
            
            servicio = servicios[opc_servicio-1]
            print(servicio)
            print(dia)

            cantidad = int(input("Ingrese la cantidad de atenciones requeridas: "))
            
            request = Request({
                'hora_desde':hora_desde,
                'hora_hasta':hora_hasta,
                'dia':dia.nombre,
                'id_servicio':servicio.id,
                'cantidad':cantidad
            })
            
            success =  self.guardar_atencion(request)
            
            if (success):
                print("Atencion registrada!")    
        except Exception as e:
            print(str(e))
            return False, {"error": f"Error al registrar la atención: {str(e)}"}
        
    def modificar_atencion(self, request: Request):
        (request.require('atencion'))
        
        if(request.has_errors()):
            return False
        
        atencion = request.get('atencion') if isinstance(request.get('atencion'), Atencion) else None
        try:
            # Buscar cliente
            if not hasattr(atencion,'id'):
                return False
            
            if not atencion:
                return False
            
            return atencion.update()
            
            
        except Exception as e:
            return False, {"error": f"Error al actualizar atención: {str(e)}"}
        pass
        
    def solicitar_modificar_atencion(self):
        atencion = self.buscar_atencion()
        dias = self._dias_controller.get_dias()
        servicios = self._servicios_controller.get_servicios()
                
        if not atencion:
            return False
        
        print("Atención: ",atencion)
        
        hora_desde = input("Nueva hora desde (dejar vacío para no cambiar): ")
        hora_hasta = input("Nueva hora hasta (dejar vacío para no cambiar): ")
        
        
        print("Seleccione el nuevo día para la atención (Dejar vacío para no cambiar)")
        
        for dia in dias:
            print(dia.id,")"," ",dia.nombre)
            
        opc_dia = input("Ingrese una opción: ")
        
        print("Seleccione el nuevo servicio para la tención (Dejar vacío para no cambiar)")
        
        for servicio in servicios:
            print(servicio.id,")"," ",servicio.nombre)
            
        opc_servicio = input("Ingrese una opción: ")

        cantidad = input("Ingrese la nueva cantidad de la atención (Dejar vacío para no cambiar): ")

        atencion.hora_desde = hora_desde if hora_desde != '' else atencion.hora_desde
        atencion.hora_hasta = hora_hasta if hora_hasta != '' else atencion.hora_hasta
        atencion.dia = dias[int(opc_dia)-1].nombre if opc_dia != '' else atencion.dia
        atencion.id_servicio = servicios[int(opc_servicio)-1].id if opc_servicio != '' else atencion.id_servicio 
        atencion.cantidad = cantidad if cantidad != '' else atencion.cantidad
         

        print("Atención: ",atencion)
        
        request = Request({'atencion':atencion})
        
        success = self.modificar_atencion(request)
        
        if success:
            print("Atención actualizada!")
    
    def buscar_atencion(self):
        dias = self._dias_controller.get_dias()
        servicios = self._servicios_controller.get_servicios()
        
        if(len(servicios) == 0):
            print("No hay servicios, cargados! Para buscar atenciones debe cargar servicios!")
            return False
        
        hora_desde_s = input("Ingrese la hora desde donde comienza la atención con el siguiente formato (HH:MM:SS): ")
        hora_hasta_s = input("Ingrese la hora hasta donde finaliza la atención con el siguiente formato (HH:MM:SS): ")

        print("Seleccione el día de la atencion: ")
        for dia in dias:
            print(dia.id,")"," ",dia.nombre)
        
        opc_dia = int(input("Ingrese una opción: "))
        
        dia_s = dias[opc_dia-1]
        
        
        
        for servicio in servicios:
            print(servicio.id,")"," ",servicio.nombre)
            
        opc_servicio = int(input("Ingrese una opción: "))
        
        servicio_s = servicios[opc_servicio-1]
        
        atencion = Atencion.where(hora_desde=hora_desde_s,hora_hasta=hora_hasta_s,dia=dia_s.nombre,id_servicio=servicio_s.id)
        if not atencion:
            return False, {"error":"No sé encontró la atención"}
        
        return atencion[0]
    
    def solicitar_eliminar_atencion(self):
        print("Elija una opción: ")
        print("1.) Eliminar atencion por parámetros")
        print("2.) Eliminar TODAS las atenciones")
        
        opc = input("Ingrese una opción: ")
        if opc == '1':
            atencion = self.buscar_atencion()
            
            if not atencion:
                return False
            
            return atencion.delete()
        elif opc == '2':
            delete = input("¿Está seguro que desea eliminar TODAS las atenciones? (S/N): ")
            
            if delete.upper() == 'S':
                return Atencion.delete_all(Atencion)
            else:
                return False
        else:
            print("Opción incorrecta")
            return False