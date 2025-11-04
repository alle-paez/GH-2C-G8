import re
import json
from validaciones import *
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

def llenar_habitaciones(archivo="GH-2C-G8/tabla_habitaciones.json"):
    numero = validar_entero("Número de habitación (-1 para salir): ") #Chequea enteros con excepciones. 
    while numero != -1:
        try: 
            with open(archivo, 'r', encoding="UTF-8") as data:
                habitaciones = json.load(data)
            for habi in habitaciones: 
                while habi["hab"] == numero:
                    print("La habitación ya existe. ")
                    numero = validar_entero("Número de habitación: ")


            precio = validar_entero("Precio (entero > 0): ")
            tipo_txt = leer_tipo()
            capacidad = validar_entero("Capacidad (> 0): ")
            estado_txt = leer_estado()
            
            nueva_habitacion = {
                "hab":numero,
                "Precio": precio,
                "Tipo": tipo_txt,
                "Capacidad": capacidad,
                "Estado": estado_txt
            }

            habitaciones.append(nueva_habitacion)

            with open(archivo, 'w', encoding="UTF-8") as data:
                json.dump(habitaciones, data, ensure_ascii=False, indent=4) #Ensure... Evita la codificacion del formato unicode dentro del json.
            print(f"Se ha agregado la habitacion {nueva_habitacion["hab"]} de tipo {nueva_habitacion["Tipo"]}.")
        except (FileNotFoundError, OSError) as error:
            print(f"Error! {error}")
        finally: 
            numero = validar_entero("Número de habitación (-1 para salir): ")

        """idx = ubicar(matriz, int(numero))
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
    ordenar_hab(matriz)"""

#MODIFICAR HABITACIONES----------------------------------------------------------------------------------------------
def modificar_habitacion(archivo="GH-2C-G8/tabla_habitaciones.json"):
    numero= validar_entero("Número de habitación a modificar (-1 para volver): ")

    while numero != -1:
        try: 
            with open(archivo, 'r', encoding="UTF-8") as data:
                habitaciones = json.load(data)
            
            nros_hab = [habi["hab"] for habi in habitaciones]
            if numero in nros_hab: 
                indice = nros_hab.index(numero)
            
            else:
                while numero not in nros_hab:
                    print("El número de habitación ingresado no existe. Ingrese otro.")
                    numero= validar_entero("Número de habitación a modificar: ")
                indice = nros_hab.index(numero)
                       
            op_txt = input("\n1-Precio  2-Tipo  3-Capacidad  4-Estado  5-Todos  (-1 volver)\nOpción: ").strip()
            while not (op_txt.lstrip("-").isdigit() and int(op_txt) in {1,2,3,4,5,-1}):
                print("Opción inválida.")
                op_txt = input("\n1-Precio  2-Tipo  3-Capacidad  4-Estado  5-Todos  (-1 volver)\nOpción: ").strip()
            op = int(op_txt)

            while op != -1:
                if op == 1:
                    while True:
                        try: 
                            nuevo_precio = input("Nuevo precio: ")
                            break
                        except ValueError:
                            print("Se ingreso un número invalido.")

                    habitaciones[indice]["precio"] = nuevo_precio

                    with open(archivo, 'w', encoding="UTF-8") as data:
                        json.dump(habitaciones, data, ensure_ascii=False, indent=4)
                    print("Precio actualizado.")

                elif op == 2:
                    nuevo_tipo = leer_tipo()
                    habitaciones[indice]["tipo"] = nuevo_tipo

                    with open(archivo, 'w', encoding="UTF-8") as data:
                        json.dump(habitaciones, data, ensure_ascii=False, indent=4)
                    print("Tipo actualizado.")
                            
                elif op == 3:
                    nueva_cap = validar_entero("Nueva capacidad (> 0): ")
                    habitaciones[indice]["capacidad"] = nueva_cap

                    with open(archivo, 'w', encoding="UTF-8") as data:
                        json.dump(habitaciones, data, ensure_ascii=False, indent=4)
                    print("Capacidad actualizada.")

                elif op == 4:
                    nuevo_estado = leer_estado()
                    habitaciones[indice]["estado"] = nuevo_estado
            
                    with open(archivo, 'w', encoding="UTF-8") as data:
                        json.dump(habitaciones, data, ensure_ascii=False, indent=4)
                    print("Estado actualizado.")

                elif op == 5:
                    nuevo_precio = validar_entero("Nuevo precio (> 0):")
                    nuevo_tipo = leer_tipo()
                    nueva_cap = validar_entero("Nueva capacidad (> 0): ")
                    nuevo_estado = leer_estado()

                    habitaciones[indice]["precio"] = nuevo_precio
                    habitaciones[indice]["tipo"] = nuevo_tipo
                    habitaciones[indice]["capacidad"] = nueva_cap
                    habitaciones[indice]["estado"] = nuevo_estado

                    with open(archivo, 'w', encoding="UTF-8") as data:
                        json.dump(habitaciones, data, ensure_ascii=False, indent=4)
                    print("Todos los campos actualizados.")

                op_txt = input("\n1-Precio  2-Tipo  3-Capacidad  4-Estado  5-Todos  (-1 volver)\nOpción: ").strip()
                while not (op_txt.lstrip("-").isdigit() and int(op_txt) in {1,2,3,4,5,-1}):
                    print("Opción inválida.")
                    op_txt = input("\n1-Precio  2-Tipo  3-Capacidad  4-Estado  5-Todos  (-1 volver)\nOpción: ").strip()
                op = int(op_txt)

                numero = validar_entero("Número de otra habitación a modificar (-1 para volver): ")
    
        except (FileNotFoundError, OSError) as error:
            print(f"Error! {error}")
        finally: 
            numero = validar_entero("Número de habitación (-1 para salir): ")            

#LEER TIPOS Y SUS OPCIONES--------------------------------------------------------------------------------------------------------
tipos   = ["Single", "Doble", "Triple", "Suite"]
estados = ["Disponible", "Ocupada", "Mantenimiento"]

def leer_tipo():
    
    tipo = esta_vacio("Escribí el tipo de habitación (Single/Doble/Triple/Suite): ")
    valido = list(filter(lambda x: x == tipo, tipos))
    while len(valido) == 0:
        tipo = input("Tipo inválido. Volvé a escribir: ").capitalize()
        valido = list(filter(lambda x: x == tipo, tipos))
    return tipo

def leer_estado():
    estado = esta_vacio("Escribí el estado (Disponible/Ocupada/Mantenimiento): ")
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