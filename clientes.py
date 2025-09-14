from listas_codeadas import *
from reservas import *
import re

def llenar_clientes(m):
    dni = input("Ingrese el Dni del cliente: (-1 para finalizar la carga:)")
    flag=verificar_formato(dni)
    if int(dni)==-1:
        flag=True
    while not flag:
        dni = input("Ingrese el Dni del cliente nuevamente: (-1 para finalizar la carga:)")
        flag=verificar_formato(dni)
        
    if dni==-1:    
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


def print_clientes(m):
    print("Dni	Nombre	Apellido	Teléfono	Mail")
    for i in range(len(m)):
        for j in range(len(m[i])):
            print(f'{m[i][j]}'.center(10," "), end = "")
        print()

def modificar_clientes():
    pass


#existe_cliente()
#buscar_cliente()
es_texto=lambda x: re.search(r'^[a-zA-Z ]+$', x)is not None
es_telefono= lambda x: re.search(r'\d{4}-\d{4}$', x) is not None
es_mail= lambda x: re.search(r'\w*@gmail\.com$', x) is not None