import os
import platform
from laboratorio_poo import(
    ProductoElectronico,
    ProductoAlimenticio,
    GestionProducto
)
def limpiar_pantalla():
    "Limpiar la pantalla segun el sistema operativo"
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def mostrar_menu():
    print("==================================================================")
    print("|                      Menú de Gestión de Productos               |")
    print("==================================================================")
    print("| 1) Agregar el producto Electrónico                              |")
    print("| 2) Agregar el producto Alimenticio                              |")
    print("| 3) Buscar el producto por su Id de producto                     |")
    print("| 4) Actualizar el producto                                       |")
    print("| 5) Eliminar el producto por su Id                               |")
    print("| 6) Mostrar los productos en el inventario                       |")
    print("| 7) Salir                                                        |")
    print("==================================================================")

def agregar_producto(gestion, tipo_producto):
    try:
        nombre = input("Ingrese el Nombre del producto: ")
        precio = float(input("Ingrese el Precio del producto: "))
        cantidad = int(input("Ingrese el Cantidad del producto: "))
        idproducto = input("Ingrese el Id del producto(Enteros): ")
        marca = input("Ingrese la Marca del producto: ")
        if tipo_producto == "1":
            garantia = int(input("Ingrese la Garantia del producto(Mayor a 6 meses): "))
            producto = ProductoElectronico(nombre, precio, cantidad, idproducto, marca, garantia)
        elif tipo_producto == "2":
            vencimiento = int(input("Ingrese el vencimiento del producto(Mayor a 2 dias): "))
            producto = ProductoAlimenticio(nombre, precio, cantidad, idproducto, marca, vencimiento)
        else:
            print("Opcion invalida")
            return
        gestion.crear_producto(producto)    
        input("Presione enter para continuar..")

    except ValueError as e:
        print(f"A ocurrido un error: {e}")
    except Exception as e:
        print(f"Ocurrio un error no esperado.")


def buscar_producto_por_id(gestion):
    idproducto = input("Ingrese el id del producto: ")
    gestion.leer_producto(idproducto)
    input("Presione enter para continuar..")
    

def actualizar_precio_producto(gestion):
    idproducto = input("Ingrese el id del producto para actualizar su precio: ")
    precio = float(input("Ingrese el precio del producto: "))
    gestion.actualizar_producto(idproducto, precio)
    input("Presione enter para continuar..")

def eliminar_producto_por_id(gestion):
        idproducto = input("Ingrese el id del producto para eliminarlo: ")
        gestion.eliminar_producto(idproducto)
        input("Presione enter para continuar..")


def mostrar_todos_los_productos(gestion):
    print("========== Listado completo de los productos en stock ==========")
    for producto in gestion.leer_datos().values():
        if "garantia" in producto:
            print(f"Nombre:{producto['nombre']} - Precio:{producto['precio']} - Cantidad:{producto['cantidad']} - IdProducto:{producto['idproducto']} - Marca:{producto['marca']} - Garantia:{producto['garantia']}.")
        else:
            print(f"Nombre:{producto['nombre']} - Precio:{producto['precio']} - Cantidad:{producto['cantidad']} - IdProducto:{producto['idproducto']}  - Marca:{producto['marca']}  - Vencimiento:{producto['vencimiento']}.")
    print("================================================================")
    input("Presione enter para continuar..")
           


if __name__ == "__main__":

    archivo_productos = "productos_db.json"
    gestion = GestionProducto(archivo_productos)
    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input("Que opcion del menu desea:")
        if opcion == "1" or opcion == "2":
            agregar_producto(gestion, opcion)
        elif opcion == "3":
            buscar_producto_por_id(gestion)
        elif opcion == "4":
            actualizar_precio_producto(gestion)
        elif opcion == "5":
            eliminar_producto_por_id(gestion)
        elif opcion == "6":
            mostrar_todos_los_productos(gestion)
        elif opcion == "7":
            print("Saliendo del programa...")
            break

        else:
            print("Opcion ingresada no valida. Por favor, ingrese de (1-7).")
        
