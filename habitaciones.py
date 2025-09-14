from listas_codeadas import *
from auxiliar_habitaciones import *

def print_habitaciones(matriz):
    print("Número    |Precio    |Tipo      |Capacidad |Estado    |")
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(f'{matriz[i][j]} '.center(10," "), end="")
        print()
    return matriz



#ORDENAR POR ÍNDICE: NÚMERO DE HABITACIÓN
def ordenar_hab(hab):
    hab.sort(key=lambda x: x[0])
    return hab

def eliminar_hab(hab, hab_borradas):
    item=int(input("Ingrese el número de habitación que quiera eliminar: "))
    flag=1

    while flag ==1:
        flag=0
        pos=ubicar(hab, item)
        if pos!=-1:
            hab_borradas.append(hab[pos])
            hab.delete(hab[pos])
            print(f'La habitación {item} ha sido eliminada con éxito')
            flag=int(input("Si desea eliminar otra habitación ingrese 1, si no, ingrese 0: "))
        else:
            print(f'no se encontró la habitación {item}')
            item=int(input("Ingrese el número de habitación nuevamente: "))

        if flag==1:
            item=int(input("Ingrese el número de habitación que quiera eliminar: "))

#DESHACER BORRAR DE UNA HABITACIÓN
def deshacer_borrar(hab, hab_borradas):

    item=int(input("Ingrese el número de habitación que quiera recuperar: "))
    flag=1

    while flag ==1:
        flag=0
        pos=ubicar(hab_borradas, item)
        if pos!=-1:
            hab.append(hab_borradas[pos])
            hab_borradas.delete(hab_borradas[pos])
            print(f'La habitación {item} ha sido recuperada con éxito')
            flag=int(input("Si desea recuperar otra habitación ingrese 1, si no, ingrese 0: "))
        else:
            print(f'no se encontró la habitación {item}')
            item=int(input("Ingrese el número de habitación nuevamente: "))
            
        if flag==1:
            item=int(input("Ingrese el número de habitación que quiera recuperar: "))