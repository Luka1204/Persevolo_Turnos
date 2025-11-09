from app.Models.PersevoloORM.Request.Request import Request
from app.Http.Controllers.ClienteController import ClienteController
from app.Http.Controllers.TurnoController import TurnoController
from app.Http.Controllers.ProfesionalController import ProfesionalController
from app.Http.Controllers.AtencionController import AtencionController
from app.Http.Controllers.ServiciosController import ServiciosController
from app.Http.Controllers.LiquidacionController import LiquidacionController



class MenuView:
    def __init__(self):
        self.cliente_controller = ClienteController()
        self.turno_controller = TurnoController()
        self.atencion_controller = AtencionController()
        self.professional_controller = ProfesionalController()
        self.liquidacion_controller = LiquidacionController()
        self.servicios_controller = ServiciosController()
            
    def mostrar_menu_principal(self):
        while True:
            print("\n=== SISTEMA DE TURNOS ===")
            print("1. Clientes")
            print("2. Turnos")
            print("3. Profesionales")
            print("4. Atenciones")
            print("5. Servicios")
            print("6. ADMIN")
            print("7. Salir")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.menu_clientes()    
            elif opcion == "2":
                self.menu_turnos()
            elif opcion == "3":
                self.menu_profesionales()
            elif opcion == "4":
                self.menu_atenciones()
            elif opcion == "5":
                self.menu_servicios()
            elif opcion == "6":
                self.menu_administracion()
            elif opcion == "7":
                break
            else:
                print("Opción inválida")
    
    def menu_servicios(self):
        print("=== MENÚ SERVICIOS ===")
        print("1.) Registrar servicio")
        print("2.) Actualizar servicio")
        print("3.) Eliminar servicio")
        print("4.) Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            self.servicios_controller.solicitar_guardar_servicio()
        elif opcion == "2":
            self.servicios_controller.solicitar_modificar_servicio()
        elif opcion == "3":
            self.servicios_controller.solicitar_eliminar_servicio()
        elif opcion == "4":
            return
        else:
            print("Opción inválida")

    def menu_clientes(self):
        print("=== MENÚ CLIENTES ===")
        print("1.) Registrar cliente")
        print("2.) Buscar cliente")
        print("3.) Actualizar cliente")
        print("4.) Eliminar cliente")
        print("5.) Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            self.cliente_controller.registrar_cliente()
        elif opcion == "2":
            self.cliente_controller.solicitar_buscar_cliente()
        elif opcion == "3":
            self.cliente_controller.solicitar_actualizar_cliente()
        elif opcion == "4":
            self.cliente_controller.solicitar_eliminar_cliente()
        elif opcion == "5":
            return
        else:
            print("Opción inválida")

    def menu_atenciones(self):
        print("=== MENÚ ATENCIONES ===")
        print("1.) Registrar atenciones")
        print("2.) Buscar atenciones")
        print("3.) Editar atencion")
        print("4.) Eliminar atencion")
        print("5.) Volver al menú principal")
    
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            self.atencion_controller.solicitar_guardar_atencion()
        elif opcion == "2":
            self.atencion_controller.buscar_atencion()
        elif opcion == "3":
            self.atencion_controller.solicitar_modificar_atencion()
        elif opcion == "4":
            self.atencion_controller.solicitar_eliminar_atencion()
        elif opcion == "5":
            return
        else:
            print("Opción inválida")

    def menu_administracion(self):
        print("=== MENÚ ADMINISTRACIÓN ===")
        print("1.) Generación de turnos")
        print("2.) Liquidación del día por fecha")
        print("3.) Liquidación del día actual")
        print("4.) Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            self.menu_profesionales()
        elif opcion == "2":
            self.menu_turnos()
        elif opcion == "3":
            return
        else:
            print("Opción inválida")

    def menu_profesionales(self):
        print("=== MENÚ PROFESIONALES ===")
        print("1.) Registrar profesional")
        print("2.) Buscar profesional")
        print("3.) Actualizar profesional")
        print("4.) Eliminar profesional")
        print("5.) Búsqueda de Turnos por Profesional")
        print("6.) Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            self.professional_controller.solicitar_registro_profesional()
        elif opcion == "2":
            self.professional_controller.solicitar_buscar_profesional()
        elif opcion == "3":
            self.professional_controller.actualizar_profesional()
        elif opcion == "4":
            dni = input('Ingrese DNI del profesional: ')
            self.professional_controller.eliminar_profesional(dni)
        elif opcion == "5":
            self.professional_controller.buscar_turnos_por_profesional()
        elif opcion == "6": 
            return
        else:
            print("Opción inválida")
    
    def menu_turnos(self):
        print("=== MENÚ TURNOS ===")
        print("1.) Solicitar turno")
        print("2.) Cancelar turno")
        print("3.) Consultar turno")
        print("4.) Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            self.turno_controller.solicitar_turno()
        elif opcion == "2":
            self.turno_controller.cancelar_turno()
        elif opcion == "3":
            self.turno_controller.consultar_turno()
        elif opcion == "4":
            return
        else:
            print("Opción inválida")