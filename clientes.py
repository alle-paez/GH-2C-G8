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
    if flag:
        if dni ==-1:
            flag=True

    while flag==False:
        dni = validar_entero("Ingrese el Dni del cliente nuevamente: (-1 para finalizar la carga:)")
        flag=verificar_formato(dni)
           
    while dni != -1: 
        try: 
            with open(archivo, 'r', encoding="UTF-8") as data:
                clientes = json.load(data)
            
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
            flag_tel=es_telefono(telefono)
            while not flag_tel:
                telefono = validar_entero("Ingrese el telefono del cliente: ")
                flag_tel=es_telefono(telefono)

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
            
            print(f"Se ha ahregado al cliente {nuevo_cliente["nombre"]} {nuevo_cliente["apellido"]} de dni {nuevo_cliente["dni"]}.")

        except (FileNotFoundError, OSError) as error:
            print(f"Error! {error}")

            dni = validar_entero("Ingrese el Dni del cliente: (-1 para finalizar la carga): ")
            flag=verificar_formato(dni)
            while not flag:
                dni = validar_entero("Ingrese el Dni del cliente nuevamente: (-1 para finalizar la carga:)")
                flag=verificar_formato(dni)

#MODIFICAR CLIENTES-------------------------------------------------------------------------------------------------------

def modificar_clientes(archivo="tabla_clientes.json"):
    print_clt(archivo)
    dni = validar_entero("\nIngrese DNI del cliente a modificar (-1 para salir): ")
    while dni != "-1":
        if re.match(r"^\d{8}$", dni):
            dni = int(dni)
            pos = ubicar(m, dni)
            if pos != -1:
                fila = m[pos]
                print("Cliente encontrado:")
                print_clt([fila])

                nuevo_nombre   = input(f"Nuevo nombre ({fila[1]}): ").strip()
                if nuevo_nombre != "":
                    while not es_texto(nuevo_nombre):
                        nuevo_nombre = input("Nombre inválido. Reingrese: ").strip()
                    fila[1] = nuevo_nombre.title()

                nuevo_apellido = input(f"Nuevo apellido ({fila[2]}): ").strip()
                if nuevo_apellido != "":
                    while not es_texto(nuevo_apellido):
                        nuevo_apellido = input("Apellido inválido. Reingrese: ").strip()
                    fila[2] = nuevo_apellido.title()

                nuevo_tel = input(f"Nuevo teléfono ({fila[3]}): ").strip()
                if nuevo_tel != "":
                    while not es_telefono(nuevo_tel):
                        nuevo_tel = input("Teléfono inválido. Reingrese (####-####): ").strip()
                    fila[3] = nuevo_tel

                nuevo_mail = input(f"Nuevo mail ({fila[4]}): ").strip()
                if nuevo_mail != "":
                    while not es_mail(nuevo_mail):
                        nuevo_mail = input("Mail inválido (solo @gmail.com). Reingrese: ").strip()
                    fila[4] = nuevo_mail

                m[pos] = fila
                print("Cliente modificado con éxito.")
                print_clt([fila])
            else:
                print("No existe cliente con ese DNI.")
        else:
            print("DNI inválido.")

        dni = input("\nIngrese DNI del cliente a modificar (-1 para salir): ").strip()
    

#VALIDACIONES DE FORMATO--------------------------------------------------------------------------------------------------
es_texto=lambda x: re.search(r'^[a-zA-Z ]+$', x)is not None
es_telefono= lambda x: re.search(r'\d{4}-\d{4}$', x) is not None
es_mail= lambda x: re.search(r'\w*@gmail\.com$', x) is not None

#IMPRESIÓN DE CLIENTES----------------------------------------------------------------------------------------------------
def print_clt(archivo):
    try:
        with open(archivo, 'r', encoding="UTF-8") as data:
            clientes = json.load(data)
        print("Tabla clientes -------------------------------------")
        print(f"{"Dni":<10}{"Nombre":<10}{"Apellido":<10}{"Teléfono":<10}{"Mail":<10}")
        for cli in clientes:
            print(f"{cli["dni"]:<10}{cli["nombre"]:<10}{cli["apellido"]:<10}{cli["telefono"]:<10}{cli["mail"]:<10}")
    except (FileNotFoundError, OSError) as error:
        print(f"Error! {error}")



#ELIMINAR CLIENTES-----------------------------------------------------------------------------------------------------------
def borrar_clientes(clt,clt_borr):
    item=input("Ingrese el dni del cliente que quiera eliminar: ".strip())
    formato=verificar_formato(item)

    flag=1

    while flag ==1:
        flag=0
        pos=ubicar(clt, int(item.strip()))
        if pos!=-1 and formato:
            clt_borr.append(clt[pos])
            del clt[pos]
            print(f'El cliente {item} ha sido eliminado con éxito')
            flag=int(input("Si desea eliminar otro cliente ingrese 1, si no, ingrese 0: ").strip())
            while flag !=1 and flag !=0:
                flag=int(input("Si desea eliminar otro cliente ingrese 1, si no, ingrese 0: ").strip())

        else:
            while pos==-1:
                print(f'no se encontró el cliente {item}')
                item=input("Ingrese el dni de cliente nuevamente: ")
                formato=verificar_formato(item)
                if formato:
                    pos=ubicar(clt, int(item.strip()))
                    if pos!=-1:
                        clt_borr.append(clt[pos])
                        del clt[pos]
                        print(f'El cliente {item} ha sido eliminado con éxito')
                        flag=int(input("Si desea eliminar otro cliente ingrese 1, si no, ingrese 0: "))
                        while flag !=1 and flag !=0:
                            flag=int(input("Si desea eliminar otro cliente ingrese 1, si no, ingrese 0: ").strip())
    ordenar_clt(m_clientes)
    ordenar_clt(clientes_borrados)

#DESHACER BORRAR DE UN CLIENTE--------------------------------------------------------------------------------------------------
def deshacer_borrar_clt(clt, clt_borr):
    item=input("Ingrese el dni del cliente que quiera recuperar: ")
    formato=verificar_formato(item)

    flag=1

    while flag ==1:
        flag=0
        pos=ubicar(clt_borr, int(item.strip()))
        if pos!=-1 and formato:
            clt.append(clt_borr[pos])
            del clt_borr[pos]
            print(f'El cliente {item} ha sido recuperado con éxito')
            flag=int(input("Si desea recuperar otro cliente ingrese 1, si no, ingrese 0: "))
            while flag !=1 and flag !=0:
                flag=int(input("Si desea recuperar otro cliente ingrese 1, si no, ingrese 0: ").strip())

        else:
            while pos==-1:
                print(f'no se encontró el cliente {item}')
                item=input("Ingrese el dni de cliente nuevamente: ")
                formato=verificar_formato(item.strip())
                if formato:
                    pos=ubicar(clt_borr, int(item.strip()))
                    if pos!=-1:
                        clt.append(clt_borr[pos])
                        del clt_borr[pos]
                        print(f'El cliente {item} ha sido recuperado con éxito')
                        flag=int(input("Si desea recuperar otro cliente ingrese 1, si no, ingrese 0: ").strip())
                        while flag !=1 and flag !=0:
                            flag=int(input("Si desea recuperar otro cliente ingrese 1, si no, ingrese 0: ").strip())
    ordenar_clt(m_clientes)
    ordenar_clt(clientes_borrados)

#ORDENAR POR NOMBRE-----------------------------------------------------------------------------------------------------------
def ordenar_clt(clt):
    clt.sort(key=lambda x: x[1])
    return clt

