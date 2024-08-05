"""""""""
Desafío 1: Sistema de Gestión de Productos
Objetivo: Desarrollar un sistema para manejar productos en un inventario.

Requisitos:

*Crear una clase base Producto con atributos como nombre, precio, cantidad en stock, etc.
*Definir al menos 2 clases derivadas para diferentes categorías de productos 
(por ejemplo, ProductoElectronico, ProductoAlimenticio) con atributos y métodos específicos.
*Implementar operaciones CRUD para gestionar productos del inventario.
*Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
*Persistir los datos en archivo JSON.
"""""""""
import json

class Producto:
    def __init__(self, nombre, precio, cantidad, idproducto, marca):
        self.__nombre = nombre
        self.__precio = self.validar_precio(precio)
        self.__cantidad = self.validar_cantidad(cantidad)
        self.__idproducto = self.validar_idproducto(idproducto)
        self.__marca = marca

    @property
    def nombre(self):
        return self.__nombre.capitalize()
    
    @property
    def precio(self):
        return self.__precio
    
    @property
    def cantidad(self):
        return self.__cantidad
    
    @property
    def idproducto(self):
        return self.__idproducto
    
    @property
    def marca(self):
        return self.__marca.capitalize()
    

    @precio.setter
    def precio(self, nuevo_precio):
        self.__precio =self.validar_precio(nuevo_precio)
    def validar_precio(self, precio):
        try:
            precio_num = float(precio)
            if precio_num < 0:
                raise ValueError("El precio debe ser positivo")
            return precio_num
        except ValueError:
            raise ValueError("El precio debe ser un numero valido")
         
    @idproducto.setter
    def idproducto(self, nuevo_idproducto):
        self.__idproducto =self.validar_idproducto(nuevo_idproducto)
    
    def validar_idproducto(self, idproducto):
        try:
            idproducto_num = int(idproducto)
            if idproducto_num < 0:
                raise ValueError("El id del producto debe ser positivo.")
            return idproducto_num
        except ValueError:
            raise ValueError("El id del producto debe ser un numero entero valido.")
    
    @cantidad.setter
    def cantidad(self, nueva_cantidad):
        self.__cantidad =self.validar_cantidad(nueva_cantidad)
    
    def validar_cantidad(self, cantidad):
        try:
            cantidad_num = int(cantidad)
            if cantidad_num < 0:
                raise ValueError("El cantidad de los productos debe ser 0 o positivo.")
            return cantidad_num
        except ValueError:
            raise ValueError("La cantidad productos debe ser un numero entero valido.")
        

    def to_dict(self):
        return{
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "idproducto": self.idproducto,
            "marca": self.marca
        }
    def __str__ (self):
        return f"{self.nombre} {self.precio}"

class ProductoElectronico(Producto):
    def __init__(self, nombre, precio, cantidad, idproducto, marca, garantia):
        super().__init__(nombre, precio, cantidad, idproducto, marca)
        self.__garantia = self.validar_garantia(garantia)
    
    @property
    def garantia(self):
        return self.__garantia
    
    @garantia.setter
    def garantia(self, nueva_garantia):
        self.__garantia =self.validar_garantia(nueva_garantia)
    
    def validar_garantia(self, garantia):
        try:
            garantia_num = int(garantia)
            if garantia_num < 6:
                raise ValueError("La garantia minima para un producto electronico es de 6 meses.")
            return garantia_num
        except ValueError:
            raise ValueError("La garantia debe ser un numero entero valido y mayor a 6 meses.")
    
    def to_dict(self):
        data = super().to_dict()
        data["garantia"] =self.garantia
        return data
    
    def __str__(self):
        return f"{super().__str__()} - La garantia en meses es:{self.garantia}"

class ProductoAlimenticio(Producto):
    def __init__(self, nombre, precio, cantidad, idproducto, marca, vencimiento):
        super().__init__(nombre, precio, cantidad, idproducto, marca)
        self.__vencimiento = self.validar_vencimiento(vencimiento)

    @property
    def vencimiento(self):
        return self.__vencimiento
    
    @vencimiento.setter
    def vencimiento(self, nuevo_vencimiento):
        self.__vencimiento = self.validar_vencimiento(nuevo_vencimiento)
    
    def validar_vencimiento(self, vencimiento):
        try:
            vencimiento_num = int(vencimiento)
            if vencimiento_num < 2:
                raise ValueError("El vencimiento minimo para un producto alimenticio de la panaderia es de 3 dias.")
            return vencimiento_num
        except ValueError:
            raise ValueError("El vencimiento debe ser un numero entero valido y mayor a 2 dias.")
    
    def to_dict(self):
        data = super().to_dict()
        data["vencimiento"] =self.vencimiento
        return data
    
    def __str__(self):
        return f"{super().__str__()} - El vencimiento del producto alimenticio en dias es:{self.vencimiento}"
    
class GestionProducto:
    def __init__(self, archivo):
        self.archivo = archivo

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al leer datos del archivo: {error}')
        else:
            return datos

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')

    def crear_producto(self, producto):
        try:
            datos = self.leer_datos()
            idproducto = producto.idproducto
            if not str(idproducto) in datos.keys():
                datos[idproducto] = producto.to_dict()
                self.guardar_datos(datos)
                print(f'El Guardado de datos del producto fue exitoso.')
            else:
                print(f'Producto con el Id ingresado ({idproducto}) ya existe, intentelo nuevamente.')
        except Exception as error:
            print(f'Error inesperado al crear el producto: {error}')

    def leer_producto(self, idproducto):
        try:
            datos = self.leer_datos()
            if idproducto in datos:
                producto_data = datos[idproducto]
                if "garantia" in producto_data:
                    producto = ProductoElectronico(**producto_data)
                    print(f"Producto encontrado con IdProducto {idproducto} es:")
                    print(f"{producto_data}")
                else:
                    producto = ProductoAlimenticio(**producto_data)
                    print(f"Producto encontrado con IdProducto {idproducto} es:")
                    print(f"{producto_data}")
            else:
                 print(f"Producto no encontrado con IdProducto {idproducto}")

        except Exception as e: 
            print(f"Error no al leer el producto deseado: {e}")



    def actualizar_producto(self,idproducto , nuevo_precio):
        try:
            datos = self.leer_datos()
            if str(idproducto) in datos.keys():
                datos[idproducto]["precio"] = nuevo_precio
                self.guardar_datos(datos)
                print(f"El precio del producto con ID ({idproducto}) se actualizo correctamente.")
            else:
                print(f"No existe el producto con ID ({idproducto}).")
        except Exception as e:
            print(f"Error al actualizar el producto: {e}")


    def eliminar_producto(self,idproducto ):
        try:
            datos = self.leer_datos()
            if str(idproducto) in datos.keys():
                del datos[idproducto]
                self.guardar_datos(datos)
                print(f"El producto con ID ({idproducto}) se elimino.")
            else:
                print(f"No existe el producto con ID ({idproducto}).")
        except Exception as e:
            print(f"Error al eliminar el producto: {e}")
        