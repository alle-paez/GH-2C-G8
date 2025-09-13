from listas_codeadas import *

def print_habitaciones(matriz):
    print("Número    |Precio    |Tipo      |Capacidad |Estado    |")
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(f'{matriz[i][j]} '.center(10," "), end="")
        print()
    return matriz

#DESHACER BORRAR DE UNA HABITACIÓN
def deshacer_borrar(hab, hab_del):
    item=int(input("Ingrese el número de habitación a borrar: "))
    if item in hab_del:
        hab.append(hab_del[hab_del.index(item)])

#ORDENAR POR ÍNDICE: NÚMERO DE HABITACIÓN
def ordenar_hab(hab):
    hab.sort(key=lambda x: x[0])
    return hab

def eliminar_hab(hab, hab_borradas):
    item=int(input("Ingrese el número de habitación que quiera eliminar: "))
    pos=0
    flag=0
    if item in hab:
        for i in hab:
            pos=hab[i][0].index(item)
        #
        flag=1
    else:
        print(f'no se encontró la habitación {item}')