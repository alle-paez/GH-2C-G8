import re
import json
from validaciones import *

def leer_habitaciones(archivo):
    try:
        with open(archivo, "r", encoding="UTF-8") as contenido:
            habitaciones = json.load(contenido)
            return habitaciones
    except Exception as e:
        print(f"Error, no se pudo acceder a la base de datos: {e}")

#IMPRIMIR HABITACIONES----------------------------------------------------------------------------------------------
def print_habitaciones(archivo):
    try: 
        with open(archivo, 'r', encoding="UTF-8") as data:
            habitaciones = json.load(data)
            print(f"\nLista de las Habitaciones ----------------------------")
            print(f'{"Número":<10}{"Precio":<10}{"Tipo":<10}{"Capacidad":<10}{"Estado":<10}')

            for hab in habitaciones:
                print(f"{hab["hab"]:<10}{hab["precio"]:<10}{hab["tipo"]:<15}{hab["capacidad"]:<5}{hab["estado"]:<10}")
    
    except (FileNotFoundError, OSError) as error:
        print(f"Error! {error}")

def opciones_ver_habitaciones():
    print(f"Seleccione un filtro: \n\
        1 - Ver todas \n\
        2 - Buscar por número \n\
        3 - Filtrar por tipo \n\
        4 - Filtrar por precio \n\
        5 - Filtrar por estado\n")
    
def busquedas_habitaciones(archivo="GH-2C-G8/tabla_habitaciones.json"):
    opciones_ver_habitaciones()
    while True:
        op = validar_entero("Ingrese una opción del 1 al 5. (-1 para salir): ")
        if op == -1:
            break
        elif op not in (1,2,3,4,5):
            distinto = True
            while distinto: 
                print("El numero ingresado no es una opción. Por favor, ingrese uno valido.")
                opciones_ver_habitaciones()
                op = validar_entero("Ingrese una opción válida. (1-5): ")
                if (op in (1,2,3,4,5)) or op == -1:
                    distinto = False
                else:
                    distinto = True

        if op == -1 and not distinto:
            break
        
        try:
            with open(archivo, 'r', encoding="UTF-8") as data:
                habitaciones = json.load(data)
            nros_hab = [habi["hab"] for habi in habitaciones]
            
            if op == 1:
                print_habitaciones(archivo)
            
            elif op == 2:
                room = validar_entero("Ingrese el numero de habitación que desea filtrar: ")
                if room in nros_hab:
                    indice = nros_hab.index(room)
                    print("------------------------------------")
                    print(f'{"Número":<10}{"Precio":<10}{"Tipo":<10}{"Capacidad":<10}{"Estado":<10}')
                    print(f"{habitaciones[indice]["hab"]:<10}{habitaciones[indice]["precio"]:<10}{habitaciones[indice]["tipo"]:<15}{habitaciones[indice]["capacidad"]:<5}{habitaciones[indice]["estado"]:<10}")
                else:
                    print("La habitación ingresada no existe.")
            elif op == 3:
                tipo = leer_tipo()
                filtrado = []
                for hab in habitaciones:
                    if hab["tipo"] == tipo:
                        filtrado.append(hab)
                print()
                print(f'{"Número":<10}{"Precio":<10}{"Tipo":<10}{"Capacidad":<10}{"Estado":<10}')
                for hab in filtrado:
                    print(f"{hab["hab"]:<10}{hab["precio"]:<10}{hab["tipo"]:<15}{hab["capacidad"]:<5}{hab["estado"]:<10}")
        
        except (FileNotFoundError, OSError) as error:
            print(f"Error! {error}")

                
                
                    

                
            

                
                


            





#ORDENAR POR ÍNDICE: NÚMERO DE HABITACIÓN------------------------------------------------------------------------------------
def ordenar_hab(hab):
    hab.sort(key=lambda x: int(x[0]))
    return hab

#ELIMINAR HABITACIONES------------------------------------------------------------------------------------------------------
def eliminar_hab(archivo1="GH-2C-G8/tabla_habitaciones.json", archivo2="habitaciones_borradas.json"):
    while True:
        print_habitaciones(archivo1)
        item=validar_entero("Ingrese el número de habitación que quiera eliminar: (-1 para salir.)")
        if item == -1:
            break

        try: 
            with open(archivo1, 'r', encoding="UTF-8") as data:
                habitaciones = json.load(data)
            
            nros_hab = [habi["hab"] for habi in habitaciones]
            if item in nros_hab: 
                indice = nros_hab.index(item)
                eliminado = habitaciones.pop(indice)
                with open(archivo1, 'w', encoding="UTF-8") as data:
                    json.dump(habitaciones, data, ensure_ascii=False, indent=4)
                    print(f"La habitación {item} de tipo {eliminado["tipo"]} ha sido eliminada con exito.")
                
                with open(archivo2,'r',encoding="UTF-8") as borrados:
                    hab_borradas = json.load(borrados)

                hab_borradas.append(eliminado)
                with open(archivo2, 'w', encoding="UTF-8") as borrados:
                    json.dump(hab_borradas, borrados, ensure_ascii=False, indent=4)


            else:
                s = True
                while item not in nros_hab and s:
                    n_ingreso = input("El número de habitación ingresado no existe. ¿Desea ingresar otro? s/n: ")
                    if n_ingreso.isdigit():
                        raise TypeError("No se permiten enteros. ")
                    if not n_ingreso:
                        raise ValueError("Debe ingresar algo.")
                    if n_ingreso.lower == "s":
                        s = True
                        item=validar_entero("Ingrese el número de habitación que quiera eliminar: ")
                        if item in nros_hab: 
                            indice = nros_hab.index(item)
                            eliminado = habitaciones.pop(indice)
                            with open(archivo1, 'w', encoding="UTF-8") as data:
                                json.dump(habitaciones, data, ensure_ascii=False, indent=4)
                                print(f"La habitación {item} de tipo {eliminado["tipo"]} ha sido eliminada con exito.")

                            with open(archivo2,'r',encoding="UTF-8") as borrados:
                                hab_borradas = json.load(borrados)

                            hab_borradas.append(eliminado)
                            with open(archivo2, 'w', encoding="UTF-8") as borrados:
                                json.dump(hab_borradas, borrados, ensure_ascii=False, indent=4)
                    else:
                        s = False

        except (FileNotFoundError, OSError) as error:
            print(f"Error! {error}")
            
"""while flag ==1:
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
            item=int(input("Ingrese el número de habitación que quiera eliminar: ").strip())"""

#DESHACER BORRAR DE UNA HABITACIÓN--------------------------------------------------------------------------------------------------
def deshacer_borrar(archivo1="GH-2C-G8/tabla_habitaciones.json", archivo2="habitaciones_borradas.json"):
    print_habitaciones(archivo2)
    item=validar_entero("Ingrese el número de habitación que quiera recuperar: ")
    flag=1

    while flag ==1:
        flag=0
        habitaciones_borradas = leer_habitaciones(archivo2)
        habitaciones = leer_habitaciones(archivo1)
        nros_hab = [habi["hab"] for habi in habitaciones_borradas]
        if item in nros_hab:
            indice = nros_hab.index(item)
            habitaciones.append(habitaciones_borradas.pop(indice))
            try:
                with open(archivo1, 'w', encoding="UTF-8") as data:
                    json.dump(habitaciones, data, ensure_ascii=False, indent=4)

                with open(archivo2, 'w',encoding = "UTF-8") as borrados:
                    json.dump(habitaciones_borradas, borrados, ensure_ascii=False, indent=4)

                print(f"La habitación {item} ha sido recuperada con exito.")
                flag=validar_entero("Si desea recuperar otra habitación ingrese 1, si no, ingrese 0: ")
                        
            except (FileNotFoundError, OSError) as error:
                print(f"Error! {error}")
        
        else:
            print(f"No se encontro la habitación {item}. ")
            item=validar_entero("Ingrese el número de habitación nuevamente: ")
            flag == 1

        if flag == 1:
            item = validar_entero("Ingrese el numero de habitación que quiera recuperar. ")
        

            
"""pos=ubicar(hab_borradas, item)
        if pos!=-1:
            hab.append(hab_borradas[pos])
            del (hab_borradas[pos])
            print(f'La habitación {item} ha sido recuperada con éxito')
            flag=int(input("Si desea recuperar otra habitación ingrese 1, si no, ingrese 0: ").strip())
        else:
            print(f'no se encontró la habitación {item}')
            item=int(input("Ingrese el número de habitación nuevamente: ").strip())
            
        if flag==1:
            item=int(input("Ingrese el número de habitación que quiera recuperar: ").strip())"""

#VALIDACIÓN DE NÚMEROS-------------------------------------------------------------------------------------------------------------
#es_entero = lambda x: re.search(r'^-?[0-9]+$', x) is not None

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
                "precio": precio,
                "tipo": tipo_txt,
                "capacidad": capacidad,
                "estado": estado_txt
            }

            habitaciones.append(nueva_habitacion)

            with open(archivo, 'w', encoding="UTF-8") as data:
                json.dump(habitaciones, data, ensure_ascii=False, indent=4) #Ensure... Evita la codificacion del formato unicode dentro del json.
            print(f"Se ha agregado la habitacion {nueva_habitacion["hab"]} de tipo {nueva_habitacion["tipo"]}.")
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