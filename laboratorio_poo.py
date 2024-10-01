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

import mysql.connector
from mysql.connector import Error
from decouple import config
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
    def __init__(self):
        self.host = config('DB_HOST')
        self.database= config('DB_NAME')
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')
        self.port = config('DB_PORT')

    def connect(self):
        '''Establecer una conexion con la base de datos'''
        try:
            connection = mysql.connector.connect(
                host = self.host,
                database = self.database,
                user = self.user,
                password= self.password,
                port= self.port
            )
            if connection.is_connected():
                return connection
              
        except Error as e:
            print(f'Error al conectar la base de datos: {e}')
            return None

    def crear_producto(self, producto):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    #Verificamos si existe
                    cursor.execute('SELECT idproducto FROM producto WHERE idproducto = %s',(producto.idproducto,))
                    if cursor.fetchone():
                        print(f'Error: Ya existe el producto con ese ID.')
                        return
                    #Inserto el producto dependiendo si es electronico o alimenticio
                    if isinstance(producto, ProductoElectronico):
                        query ='''
                        INSERT INTO producto (nombre, precio, cantidad, idproducto, marca)
                        VALUES(%s, %s, %s, %s, %s)                     
                        '''
                        cursor.execute(query,(producto.nombre, producto.precio, 
                                              producto.cantidad, producto.idproducto, producto.marca))
                        
                        query = '''
                        INSERT INTO productoelectronico(idproducto, garantia)
                        VALUES(%s, %s)
                        '''
                        cursor.execute(query,(producto.idproducto, producto.garantia))

                    elif isinstance(producto, ProductoAlimenticio):
                        query ='''
                        INSERT INTO producto (nombre, precio, cantidad, idproducto, marca)
                        VALUES(%s, %s, %s, %s, %s)                     
                        '''
                        cursor.execute(query,(producto.nombre, producto.precio, 
                                              producto.cantidad, producto.idproducto, producto.marca))
                        query = '''
                        INSERT INTO productoalimenticio(idproducto, vencimiento)
                        VALUES(%s, %s)
                        '''
                        cursor.execute(query,(producto.idproducto, producto.vencimiento))
                    connection.commit()
                    print(f'Producto con nombre: {producto.nombre} y Id: {producto.idproducto} fue creado correctamente.')

        except Exception as error:
            print(f'Error inesperado al crear el producto: {error}')

    def leer_producto(self, idproducto):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM producto WHERE idproducto = %s', (idproducto,))
                    producto_data = cursor.fetchone()

                    if producto_data:
                        cursor.execute('SELECT garantia FROM productoelectronico WHERE idproducto = %s', (idproducto,))
                        garantia = cursor.fetchone()
                        if garantia:
                            producto_data['garantia'] = garantia['garantia']
                            producto = ProductoElectronico(**producto_data)
                        else:
                            cursor.execute('SELECT vencimiento FROM productoalimenticio WHERE idproducto = %s', (idproducto,))
                            vencimiento = cursor.fetchone()
                            if vencimiento:
                                producto_data['vencimiento'] = vencimiento['vencimiento']
                                producto = ProductoAlimenticio(**producto_data)
                            else:
                                producto = Producto(**producto_data)
                        print(f'Producto encontrado: {producto}')
                    else:
                        print(f'No se encontró el producto con ID: {idproducto}.')
                    

        except Error as e:
            print(f"Error al leer el producto deseado: {e}")
        finally:
            if connection.is_connected():
                connection.close()

    def actualizar_producto(self,idproducto , nuevo_precio):
        '''Actualizar precio del producto'''
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    #Verificar si existe un producto con el id a buscar
                    cursor.execute('SELECT * FROM producto WHERE idproducto = %s',(idproducto,))
                    if not cursor.fetchone():
                        print(f"No se encontro producto con el ID:{idproducto}.")
                        return
                
                    #Actualizar precio
                    cursor.execute('UPDATE producto SET precio = %s WHERE idproducto = %s',(nuevo_precio, idproducto))
                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f'El precio del producto se actualizo y es: {nuevo_precio} con ID:{idproducto}')
                    else:
                        print(f'El producto con ID:{idproducto} no fue encontrado.')
        except Exception as e:
            print(f"Error al actualizar el producto: {e}")
        finally:
            if connection.is_connected():
                connection.close()

    def eliminar_producto(self,idproducto ):

        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    #Verificar si existe un producto con el id a buscar
                    cursor.execute('SELECT * FROM producto WHERE idproducto = %s',(idproducto,))
                    if not cursor.fetchone():
                        print(f"No se encontro producto con el ID:{idproducto}.")
                        return
                
                    #Eliminar el producto
                    cursor.execute('DELETE FROM productoelectronico WHERE idproducto = %s',(idproducto,))
                    cursor.execute('DELETE FROM productoalimenticio WHERE idproducto = %s',(idproducto,))
                    cursor.execute('DELETE FROM producto WHERE idproducto = %s',(idproducto,))
                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f'El producto con ID:{idproducto} fue eliminado correctamente')
                    else:
                        print(f'No se encontro el producto con ID: {idproducto}')          

        except Exception as e:
            print(f"Error al eliminar el producto: {e}")
        finally:
            if connection.is_connected():
                connection.close()
            
    def leer_todos_los_productos(self):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM producto')
                    productos_data = cursor.fetchall()
                    
                    producto2 = []

                    for producto_data in productos_data:
                        idproducto = producto_data['idproducto']

                        cursor.execute('SELECT garantia FROM productoelectronico WHERE idproducto = %s', (idproducto,))
                        garantia = cursor.fetchone()

                        if garantia:
                            producto_data['garantia'] = garantia['garantia']
                            productos = ProductoElectronico(**producto_data)
                        else:
                            cursor.execute('SELECT vencimiento FROM productoalimenticio WHERE idproducto = %s', (idproducto,))
                            vencimiento = cursor.fetchone()
                            producto_data['vencimiento'] = vencimiento['vencimiento']
                            productos = ProductoAlimenticio(**producto_data)

                        producto2.append(productos)       

        except Exception as e:
            print(f"Error mostrar los productos: {e}")
        else:
            return producto2
        finally:
            if connection.is_connected():
                connection.close()