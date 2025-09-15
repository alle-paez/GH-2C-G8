from listas_codeadas import *
from reservas import *
import re
from habitaciones import ubicar
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


def modificar_clientes(m):
    print_clientes(m)
    dni = input("\nIngrese DNI del cliente a modificar (-1 para salir): ").strip()

    while dni != "-1":
        if re.match(r"^\d{8}$", dni):
            dni = int(dni)
            pos = ubicar(m, dni)
            if pos != -1:
                fila = m[pos]
                print("Cliente encontrado:")
                print_clientes([fila])

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
                print_clientes([fila])
            else:
                print("No existe cliente con ese DNI.")
        else:
            print("DNI inválido.")

        dni = input("\nIngrese DNI del cliente a modificar (-1 para salir): ").strip()
    

def mostrar_opciones_mod_2():
    print(f"¿Que elemento/s de la reserva desea modificar?:\n \
(El id, dni del cliente y el total de la reserva no son posibles de modificar.) \n \
Fechas de entrada y salida: 1 \n \
Número de habitación: 2 \n \
Cantidad de pasajeros: 3")

#existe_cliente()
#buscar_cliente()
es_texto=lambda x: re.search(r'^[a-zA-Z ]+$', x)is not None
es_telefono= lambda x: re.search(r'\d{4}-\d{4}$', x) is not None
es_mail= lambda x: re.search(r'\w*@gmail\.com$', x) is not None

def print_clt(matriz):
    print("")
    print("---------------------------------------------------------------------------------")
    print("DNI       |Nombre       |Apellido       |Teléfono        |Mail                  ")
    print("---------------------------------------------------------------------------------")
    for valor in matriz:
        fila = valor
        dni, nombre, apellido, telefono, mail= fila

        print(str(dni).ljust(9), "|",
            str(nombre).ljust(11), "|",
            str(apellido).ljust(13), "|",
            str(telefono).ljust(14), "|",
            str(mail).ljust(14))

"""    clientes = [
    [30555999, "Juan", "Pérez", "1123456789", "juan.perez@email.com"],
    [28444888, "María", "Gómez", "1167894321", "maria.gomez@email.com"],
    [33222111, "Lucas", "Martínez", "1134567890", "lucas.martinez@email.com"],
    [29888777, "Sofía", "López", "1145678901", "sofia.lopez@email.com"],
    [31222333, "Martín", "Díaz", "1178901234", "martin.diaz@email.com"]
]"""