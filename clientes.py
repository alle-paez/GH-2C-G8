from listas_codeadas import *
import re
from habitaciones import ubicar
from validaciones import *
import json

def leer_clientes(archivo="tabla_cliente.json", modo="r"):
    try:
        contenido = open(archivo, modo, encoding="UTF-8")
        clientes = json.load(contenido)
        return clientes
    except:
        print("Error, no se pudo acceder a la base de datos")
    finally:
        try:
            archivo.close()
        except:
            print("Error al cerrar el archivo")
        
#AGREGAR CLIENTES--------------------------------------------------------------------------------

def llenar_clientes(archivo="tabla_clientes.json"):
    dni = validar_entero("Ingrese el Dni del cliente: (-1 para finalizar la carga): ")
    flag=verificar_formato(dni)
    if dni ==-1:
        flag=True

    while flag==False:
        dni = validar_entero("Ingrese el Dni del cliente nuevamente: (-1 para finalizar la carga:)")
        flag=verificar_formato(dni)
        if dni == -1:
            flag = True
           
    while dni != -1: 
        try: 
            with open(archivo, 'r', encoding="UTF-8") as data:
                clientes = json.load(data)
            
            dnis_existentes = [cli["dni"] for cli in clientes]

            if dni in dnis_existentes and flag:
                existe = True
                while existe:
                    print("El dni ingresado ya existe, por favor, ingrese otro.")
                    dni = validar_entero("Ingrese el dni del cliente nuevamente (-1 para finalizar): ")
                    if dni == -1:
                        existe = False
                    else:
                        flag = verificar_formato(dni)
                        if flag and dni not in dnis_existentes:
                            existe = False

            if dni != -1:

                nombre = esta_vacio("Ingrese el nombre del cliente: ")
                flag_name=es_texto(nombre)
                while not flag_name:
                    nombre = esta_vacio("Ingrese el nombre del cliente nuevamente: ")
                    flag_name=es_texto(nombre)

                apellido = esta_vacio("Ingrese el apellido del cliente: ")
                flag_sur=es_texto(apellido)
                while not flag_sur:
                    apellido = esta_vacio("Ingrese el apellido del cliente: ")
                    flag_sur=es_texto(apellido)

                telefono = validar_entero("Ingrese el telefono del cliente: ")
                flag_tel=es_telefono(str(telefono))
                while not flag_tel:
                    telefono = validar_entero("Ingrese el telefono del cliente: ")
                    flag_tel=es_telefono(str(telefono))

                mail = esta_vacio("Ingrese el e-mail del cliente: ")
                flag_mail=es_mail(mail)
                while not flag_mail:
                    mail = esta_vacio("Ingrese el e-mail del cliente: ")
                    flag_mail=es_mail(mail) 

                nuevo_cliente ={
                    "dni":dni,
                    "nombre":nombre,
                    "apellido":apellido,
                    "telefono":telefono,
                    "mail":mail
                    }
                
                clientes.append(nuevo_cliente)
                with open(archivo, 'w', encoding="UTF-8") as data:
                    json.dump(clientes, data, ensure_ascii=False, indent=4)
                
                print(f"Se ha agregado al cliente {nuevo_cliente["nombre"]} {nuevo_cliente["apellido"]} de dni {nuevo_cliente["dni"]}.")
                
                dni = validar_entero("Ingrese el Dni del cliente: (-1 para finalizar la carga): ")
                flag=verificar_formato(dni)
                while not flag:
                    dni = validar_entero("Formato incorrecto, ingrese el Dni del cliente nuevamente: (-1 para finalizar la carga:)")
                    flag=verificar_formato(dni)
                    if dni == -1:
                        flag = True

        except (FileNotFoundError, OSError) as error:
            print(f"Error! {error}")

            

#MODIFICAR CLIENTES-------------------------------------------------------------------------------------------------------
def abrir_archivo(archivo):
    try:
        with open(archivo, 'r', encoding="UTF-8") as data:
            tabla = json.load(data)
        return tabla
    except (FileNotFoundError, OSError) as error:
        print(f"Error! No se pudo abrir el archivo. {error}")
    except Exception as e:
        print(f"Error! {e}")

def escribir_archivo(archivo,tabla,mensaje="Dump generado con exito"):
    try:
        with open(archivo, 'w', encoding="UTF-8") as data:
            json.dump(tabla,data,ensure_ascii=False, indent=4)
        print(mensaje)
    except (FileNotFoundError, OSError) as error:
        print(f"Error! No se pudo abrir el archivo. {error}")
    except Exception as e:
        print(f"Error! {e}")
    

def modificar_clientes(archivo="tabla_clientes.json"):
    print_clt(archivo)
    dni = validar_entero("\nIngrese DNI del cliente a modificar (-1 para salir): ")
    while dni != -1:
        if re.match(r"^\d{8}$", str(dni)):
            dni = int(dni)
            
            clientes = abrir_archivo(archivo)
            dnis_cli = [cli["dni"] for cli in clientes]

            if dni in dnis_cli:
                pos = dnis_cli.index(dni)            
            else:
                pos = -1

            if pos != -1:
                cliente = clientes[pos]
                print("Cliente encontrado:")
                print(f"{"Dni":<10}{"Nombre":<10}{"Apellido":<10}{"Teléfono":<15}{"Mail":<15}")
                print(f"{cliente["dni"]:<10}{cliente["nombre"]:<10}{cliente["apellido"]:<10}{cliente["telefono"]:<15}{cliente["mail"]:<15}")

                nuevo_nombre   = input(f"Nuevo nombre ({cliente["nombre"]})(Enter para continuar): ").strip()
                if nuevo_nombre != "":
                    while not es_texto(nuevo_nombre) and nuevo_nombre != "":
                        nuevo_nombre = input("Nombre inválido. Reingrese: ").strip()
                    if nuevo_nombre != "":
                        clientes[pos]["nombre"] = nuevo_nombre.title()


                nuevo_apellido = input(f"Nuevo apellido ({cliente["apellido"]})(Enter para continuar):").strip()
                if nuevo_apellido != "":
                    while not es_texto(nuevo_apellido) and nuevo_apellido != "":
                        nuevo_apellido = input("Apellido inválido. Reingrese: ").strip()
                    if nuevo_apellido != "":
                        clientes[pos]["apellido"] = nuevo_apellido.title()

                nuevo_tel = input(f"Nuevo teléfono ({cliente["telefono"]})(Enter para continuar): ").strip()
                if nuevo_tel != "":
                    while not es_telefono(nuevo_tel) and nuevo_tel != "":
                        nuevo_tel = input("Teléfono inválido. Reingrese (ARG: 10 dígitos): ").strip()
                    if nuevo_tel != "":
                        clientes[pos]["telefono"] = nuevo_tel

                nuevo_mail = input(f"Nuevo mail ({cliente["mail"]}): ").strip()
                if nuevo_mail != "":
                    while not es_mail(nuevo_mail) and nuevo_mail != "":
                        nuevo_mail = input("Mail inválido (solo @gmail.com). Reingrese: ").strip()
                    if nuevo_mail != "":
                        clientes[pos]["mail"] = nuevo_mail

                escribir_archivo(archivo,clientes,"Cliente modificado con éxito.")
                cliente = clientes[pos]
                print(f"{"Dni":<10}{"Nombre":<10}{"Apellido":<10}{"Teléfono":<15}{"Mail":<15}")
                print(f"{cliente["dni"]:<10}{cliente["nombre"]:<10}{cliente["apellido"]:<10}{cliente["telefono"]:<15}{cliente["mail"]:<15}")

            else:
                print("No existe cliente con ese DNI.")
        else:
            print("DNI inválido.")
        dni = validar_entero("\nIngrese DNI del cliente a modificar (-1 para salir): ")
    

#VALIDACIONES DE FORMATO--------------------------------------------------------------------------------------------------
es_texto=lambda x: re.search(r'^[a-zA-Z ]+$', x)is not None
es_telefono= lambda x: re.search(r'^\d{10}$', x) is not None
es_mail= lambda x: re.search(r'\w*@gmail\.com$', x) is not None

#IMPRESIÓN DE CLIENTES----------------------------------------------------------------------------------------------------
def print_clt(archivo):
    try:
        with open(archivo, 'r', encoding="UTF-8") as data:
            clientes = json.load(data)
        print("Tabla clientes -------------------------------------")
        print(f"{"Dni":<10}{"Nombre":<10}{"Apellido":<10}{"Teléfono":<15}{"Mail":<15}")
        for cli in clientes:
            print(f"{cli["dni"]:<10}{cli["nombre"]:<10}{cli["apellido"]:<10}{cli["telefono"]:<15}{cli["mail"]:<15}")
    except (FileNotFoundError, OSError) as error:
        print(f"Error! {error}")



#ELIMINAR CLIENTES-----------------------------------------------------------------------------------------------------------
def borrar_clientes(archivo1, archivo2, mensaje):
    print_clt(archivo1)
    dni=validar_entero(f"Ingrese el dni del cliente que quiera {mensaje}r: ")
    formato=verificar_formato(dni)
    flag=1
    while flag ==1:
        flag=0
        clientes = abrir_archivo(archivo1)
        clientes_borrados = abrir_archivo(archivo2)
        dnis_cli = [cli["dni"] for cli in clientes]
        if dni in dnis_cli:
            pos = dnis_cli.index(dni)
        else: 
            pos = -1
        
        if pos!=-1 and formato:
            eliminado = clientes.pop(pos)
            clientes_borrados.append(eliminado)
            escribir_archivo(archivo1,clientes,f'El cliente {eliminado["nombre"]} {eliminado["apellido"]} ha sido {mensaje}do con éxito. ')
            escribir_archivo(archivo2, clientes_borrados,"")
            
            flag=validar_entero(f"Si desea {mensaje}r otro cliente ingrese 1, si no, ingrese 0: ")
            while flag !=1 and flag !=0:
                flag=validar_entero(f"Si desea {mensaje}r otro cliente ingrese 1, si no, ingrese 0: ")
        else:
            while pos==-1 and dni != -1:
                print(f'no se encontró el cliente {dni}')
                dni = validar_entero("Ingrese el dni de cliente nuevamente (-1 para salir):  ")
                formato=verificar_formato(dni)
                if formato and dni != -1:
                    if dni in dnis_cli:
                        pos = dnis_cli.index(dni)
                    else:
                        pos = -1        
                    if pos!=-1:
                        eliminado = clientes.pop(pos)
                        clientes_borrados.append(eliminado)

                        escribir_archivo(archivo1,clientes,f'El cliente {eliminado["nombre"]} {eliminado["apellido"]} ha sido {mensaje}do con éxito. ')
                        escribir_archivo(archivo2, clientes_borrados,"") 

                        flag=validar_entero(f"Si desea {mensaje}r otro cliente ingrese 1, si no, ingrese 0: ")
                        while flag !=1 and flag !=0:
                            flag=validar_entero(f"Si desea {mensaje}r otro cliente ingrese 1, si no, ingrese 0: ")
                        
                        if flag == 1:
                            dni=validar_entero(f"Ingrese el dni del cliente que quiera {mensaje}r (-1 para salir): ")
                            if dni == -1:
                                flag = 0



#ORDENAR POR NOMBRE-----------------------------------------------------------------------------------------------------------
def ordenar_clt(clt):
    clt.sort(key=lambda x: x[1])
    return clt

