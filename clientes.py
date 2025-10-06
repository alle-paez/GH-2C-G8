from listas_codeadas import *
from reservas import *
import re
from habitaciones import ubicar

#AGREGAR CLIENTES--------------------------------------------------------------------------------

def llenar_clientes(m):
    dni = input("Ingrese el Dni del cliente: (-1 para finalizar la carga): ")
    flag=verificar_formato(dni)

    if flag:
        if int(dni)==-1:
            flag=True

    while flag==False:
        dni = input("Ingrese el Dni del cliente nuevamente: (-1 para finalizar la carga:)")
        flag=verificar_formato(dni)

            
    while int(dni) != -1: 
        nombre = input("Ingrese el nombre del cliente: ")
        flag_name=es_texto(nombre)
        while not flag_name:
            nombre = input("Ingrese el nombre del cliente nuevamente: ")
            flag_name=es_texto(nombre)

        apellido = input("Ingrese el apellido del cliente: ")
        flag_sur=es_texto(apellido)
        while not flag_sur:
            apellido = input("Ingrese el apellido del cliente: ")
            flag_sur=es_texto(apellido)

        telefono = input("Ingrese el telefono del cliente: ")
        flag_tel=es_telefono(telefono)
        while not flag_tel:
            telefono = input("Ingrese el telefono del cliente: ")
            flag_tel=es_telefono(telefono)

        mail = input("Ingrese el e-mail del cliente: ")
        flag_mail=es_mail(mail)
        while not flag_mail:
            mail = input("Ingrese el e-mail del cliente: ")
            flag_mail=es_mail(mail) 

        m.append([dni,nombre,apellido,telefono,mail])

        dni = input("Ingrese el Dni del cliente: (-1 para finalizar la carga:)")
        flag=verificar_formato(dni)
        while not flag:
            dni = input("Ingrese el Dni del cliente nuevamente: (-1 para finalizar la carga:)")
            flag=verificar_formato(dni)
    ordenar_clt(clientes)

#MODIFICAR CLIENTES-------------------------------------------------------------------------------------------------------
def modificar_clientes():
    pass

def modificar_clientes(m):
    print_clt(m)
    dni = input("\nIngrese DNI del cliente a modificar (-1 para salir): ").strip()

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
def print_clt(matriz):
    print("")
    print("---------------------------------------------------------------------------------")
    print("DNI       |Nombre       |Apellido       |Teléfono     |Mail                      ")
    print("---------------------------------------------------------------------------------")
    for valor in matriz:
        fila = valor
        dni, nombre, apellido, telefono, mail= fila

        print(str(dni).ljust(9), "|",
            str(nombre).ljust(11), "|",
            str(apellido).ljust(13), "|",
            str(telefono).ljust(14), "|",
            str(mail).ljust(14))

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
    ordenar_clt(clientes)
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
    ordenar_clt(clientes)
    ordenar_clt(clientes_borrados)

#ORDENAR POR NOMBRE-----------------------------------------------------------------------------------------------------------
def ordenar_clt(clt):
    clt.sort(key=lambda x: x[1])
    return clt
