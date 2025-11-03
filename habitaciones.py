from listas_codeadas import *
import re
import json

def leer_habitaciones(archivo="tabla_habitaciones.json"):
    try:
        contenido = open(archivo, "r", encoding="UTF-8")
        habitaciones = json.load(contenido)
        return habitaciones
    except:
        print("Error, no se pudo acceder a la base de datos")
    finally:
        try:
            archivo.close()
        except:
            print("Error al cerrar el archivo")

#IMPRIMIR HABITACIONES----------------------------------------------------------------------------------------------
def print_habitaciones(matriz):
    print("Número    |Precio    |Tipo      |Capacidad |Estado    |")
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(f'{matriz[i][j]} '.ljust(10), end="")
        print()
    return matriz

#ORDENAR POR ÍNDICE: NÚMERO DE HABITACIÓN------------------------------------------------------------------------------------
def ordenar_hab(hab):
    hab.sort(key=lambda x: int(x[0]))
    return hab

#ELIMINAR HABITACIONES------------------------------------------------------------------------------------------------------
def eliminar_hab(hab, hab_borradas):
    item=int(input("Ingrese el número de habitación que quiera eliminar: ").strip())
    flag=1

    while flag ==1:
        flag=0
        pos=ubicar(hab, item)
        if pos!=-1:
            hab_borradas.append(hab[pos])
            del hab[pos]
            print(f'La habitación {item} ha sido eliminada con éxito')
            flag=int(input("Si desea eliminar otra habitación ingrese 1, si no, ingrese 0: ").strip())
            while flag !=1 and flag !=0:
                flag=int(input("Si desea eliminar otra habitación ingrese 1, si no, ingrese 0: ").strip())

        else:
            print(f'no se encontró la habitación {item}')
            item=int(input("Ingrese el número de habitación nuevamente: ").strip())
        

        if flag==1:
            item=int(input("Ingrese el número de habitación que quiera eliminar: ").strip())

#DESHACER BORRAR DE UNA HABITACIÓN--------------------------------------------------------------------------------------------------
def deshacer_borrar(hab, hab_borradas):

    item=int(input("Ingrese el número de habitación que quiera recuperar: ").strip())
    flag=1

    while flag ==1:
        flag=0
        pos=ubicar(hab_borradas, item)
        if pos!=-1:
            hab.append(hab_borradas[pos])
            del (hab_borradas[pos])
            print(f'La habitación {item} ha sido recuperada con éxito')
            flag=int(input("Si desea recuperar otra habitación ingrese 1, si no, ingrese 0: ").strip())
        else:
            print(f'no se encontró la habitación {item}')
            item=int(input("Ingrese el número de habitación nuevamente: ").strip())
            
        if flag==1:
            item=int(input("Ingrese el número de habitación que quiera recuperar: ").strip())

#VALIDACIÓN DE NÚMEROS-------------------------------------------------------------------------------------------------------------
es_entero = lambda x: re.search(r'^-?[0-9]+$', x) is not None

#LLENAR HABITACIONES-----------------------------------------------------------------------------------------------------------------
def llenar_habitaciones(matriz):
    numero = pedir_opcion("Número de habitación (-1 para salir): ") #Chequea enteros con excepciones. 
    #checkeo que no exista ya
    while numero != -1:
        idx = ubicar(matriz, int(numero))
        while idx != -1:
            print("Esta habitación ya existe.")
            while flag==False or idx!=-1:
                numero = input("Número de habitación (-1 para salir): ")
                flag=es_entero(numero)
                idx = ubicar(matriz, int(numero))

        if int(numero) != -1 and idx == -1 and flag:
            precio = input("Precio (entero > 0): ")
            es_entero(precio)

            tipo_txt = leer_tipo()
            capacidad = input("Capacidad (> 0): ")

            estado_txt = leer_estado()

            matriz.append([numero, precio, tipo_txt, capacidad, estado_txt])
            print("Habitación agregada.")

            numero = input("Número de habitación (-1 para salir): ")
            idx = ubicar(matriz, int(numero))
            flag=es_entero(numero)
    ordenar_hab(matriz)

#MODIFICAR HABITACIONES----------------------------------------------------------------------------------------------
def modificar_habitacion(matriz):
    numero= input("Número de habitación a modificar (-1 para volver): ")
    flag=es_entero(numero)

    while int(numero) != -1 and flag:

        idx = ubicar(matriz, int(numero))
        while idx == -1 and int(numero) != -1:
            print("No existe esa habitación.")
            numero = input("Número de habitación a modificar (-1 para volver): ")
            flag= es_entero(numero)

            if int(numero) != -1:
                idx = ubicar(matriz, int(numero))
            else:
                numero = input("Número de habitación a modificar (-1 para volver): ")
                flag=es_entero(numero)

        if int(numero) != -1:
            fila = matriz[idx]  # [nro, precio, tipo, capacidad, estado]
            print(f'\nActual →\
Nro: {fila[0]}\
Precio:{fila[1]}\
Tipo:{fila[2]}\
Capacidad:{fila[3]}\
Estado:{fila[4]}')\

            op_txt = input(f"\n¿Qué modificar?  1-Precio  2-Tipo  3-Capacidad  4-Estado  5-Todos  (-1 volver)\nOpción: ").strip()
            while not (op_txt.lstrip("-").isdigit() and int(op_txt) in {1,2,3,4,5,-1}):
                print("Opción inválida.")
                op_txt = input(f"\n1-Precio  2-Tipo  3-Capacidad  4-Estado  5-Todos  (-1 volver)\nOpción: ").strip()
            op = int(op_txt)

            while op != -1:
                if op == 1:
                    nuevo = input("Nuevo precio (> 0): ")
                    es_entero(nuevo)

                    matriz[idx][1] = int(nuevo)
                    print("Precio actualizado.")

                elif op == 2:
                    matriz[idx][2] = leer_tipo()
                    print("Tipo actualizado.")

                elif op == 3:
                    cap = input("Nueva capacidad (> 0): ")
                    es_entero(cap)

                    matriz[idx][3] = cap
                    print("Capacidad actualizada.")

                elif op == 4:
                    matriz[idx][4] = leer_estado()
                    print("Estado actualizado.")

                elif op == 5:
                    nuevo = input("Nuevo precio (> 0): ")
                    es_entero(nuevo)

                    t_txt = leer_tipo()
                    cap = input("Nueva capacidad (> 0): ")
                    es_entero(cap)

                    e_txt = leer_estado()

                    matriz[idx][1] = nuevo
                    matriz[idx][2] = t_txt
                    matriz[idx][3] = cap
                    matriz[idx][4] = e_txt
                    print("Todos los campos actualizados.")

                op_txt = input("\n1-Precio  2-Tipo  3-Capacidad  4-Estado  5-Todos  (-1 volver)\nOpción: ").strip()
                while not (op_txt.lstrip("-").isdigit() and int(op_txt) in {1,2,3,4,5,-1}):
                    print("Opción inválida.")
                    op_txt = input("\n1-Precio  2-Tipo  3-Capacidad  4-Estado  5-Todos  (-1 volver)\nOpción: ").strip()
                op = int(op_txt)

            numero = input("Número de otra habitación a modificar (-1 para volver): ")
            es_entero(numero)
    ordenar_hab(matriz)

#LEER TIPOS Y SUS OPCIONES--------------------------------------------------------------------------------------------------------
tipos   = ["Single", "Doble", "Triple", "Suite"]
estados = ["Disponible", "Ocupada", "Mantenimiento"]

def leer_tipo():
    tipo = input("Escribí el tipo de habitación (Single/Doble/Triple/Suite): ").capitalize()
    valido = list(filter(lambda x: x == tipo, tipos))
    while len(valido) == 0:
        tipo = input("Tipo inválido. Volvé a escribir: ").capitalize()
        valido = list(filter(lambda x: x == tipo, tipos))
    return tipo

def leer_estado():
    estado = input("Escribí el estado (Disponible/Ocupada/Mantenimiento): ").capitalize()
    valido = list(filter(lambda x: x == estado, estados))
    while len(valido) == 0:
        estado = input("Estado inválido. Volvé a escribir: ").capitalize()
        valido = list(filter(lambda x: x == estado, estados))
    return estado

#UBICAR-------------------------------------------------------------------------------------------------------------------------
def ubicar(matriz, item):
    flag = 0
    i = 0
    pos = -1
    while flag != 1:
        if matriz[i][0] == item:
            flag = 1
            pos = i
        i += 1
        if i == len(matriz):
            flag = 1
    return pos



"""def leer_numero(num,mensaje="Ingrese el número, cerrar con-1", permitir_menos1=False):
    
    #Pide un número entero validado con expresión regular.
    #Si permitir_menos1=True, se permite el valor -1 como salida.
    
    patron = r"^-?[0-9]+$"
    while not re.match(patron, num) or (not permitir_menos1 and int(num) < 1):
        print("Entrada inválida. Solo números enteros válidos.")
        num = input(mensaje).strip()
    return int(num)"""