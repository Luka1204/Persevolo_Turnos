from app.Models.Cliente import Cliente


def crear_cliente():
# Crear una instancia de Cliente
    cliente = Cliente(nombre="Juan", apellido="Pérez", dni="12345678", email="juan.perez@example.com", telefono="555-1234")
    print("Cliente creado:")
    print(cliente.to_dict())    
    cliente.save()
    cliente.save()
    print("Cliente guardado en CSV.") 
    cliente.convert_to_json("clientes.json")
    print(cliente.to_dict())

def main():
    crear_cliente()


if __name__ == "__main__":
    main()