import re
import json
from validaciones import *
from mas_auxiliares import ordenar
from clientes import *

def leer_habitaciones(archivo="tabla_habitaciones.json"):
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
            habitaciones_ordenados_por_num = ordenar(habitaciones, "hab")
        print(f"\n{"Lista de las Habitaciones":->80}")
        print(f'{"Número":<15}|{"Precio":<15}|{"Tipo":<15}|{"Capacidad":<15}|{"Estado":<16}\n\
{"-"*15}|{"-"*15}|{"-"*15}|{"-"*15}|{"-"*16}')

        for hab in habitaciones_ordenados_por_num:
            print(f"{hab["hab"]:<15}|{hab["precio"]:<15}|{hab["tipo"]:<15}|{hab["capacidad"]:<15}|{hab["estado"]:<16}")
    
    except (FileNotFoundError, OSError) as error:
        print(f"Error! {error}")
    except:
        print("Error inesperado. Intente nuevamente. ")

def opciones_ver_habitaciones():
    print(f"Seleccione un filtro: \n\
    1 - Ver todas \n\
    2 - Buscar por número \n\
    3 - Filtrar por tipo \n\
    4 - Filtrar por precio \n\
    5 - Filtrar por estado\n")
    
def busquedas_habitaciones(archivo="tabla_habitaciones.json"):
    opciones_ver_habitaciones()
    op = validar_entero("Ingrese una opción del 1 al 5. (-1 para salir): ")
    while op != -1:
        while op not in (-1,1,2,3,4,5):
                print("El numero ingresado no es una opción. Por favor, ingrese uno valido. ")
                opciones_ver_habitaciones()
                op = validar_entero("Ingrese una opción válida. (1-5)(-1 para salir): ")

        try:
            with open(archivo, 'r', encoding="UTF-8") as data:
                habitaciones = json.load(data)
                habitaciones_ordenados_por_num = ordenar(habitaciones, "hab")
            nros_hab = [habi["hab"] for habi in habitaciones_ordenados_por_num]
            
            if op == 1:
                print_habitaciones(archivo)
            
            elif op == 2:
                room = validar_entero("Ingrese el numero de habitación que desea filtrar: ")
                if room in nros_hab:
                    indice = nros_hab.index(room)
                    print("-"*80)
                    print(f'{"Número":<10}{"Precio":<10}{"Tipo":<10}{"Capacidad":<10}{"Estado":<10}')
                    print(f"{habitaciones_ordenados_por_num[indice]["hab"]:<10}{habitaciones_ordenados_por_num[indice]["precio"]:<10}{habitaciones_ordenados_por_num[indice]["tipo"]:<15}{habitaciones_ordenados_por_num[indice]["capacidad"]:<5}{habitaciones_ordenados_por_num[indice]["estado"]:<10}")
                else:
                    print("La habitación ingresada no existe.")
            elif op == 3:
                tipo = leer_tipo()
                filtrado = []
                for hab in habitaciones_ordenados_por_num:
                    if hab["tipo"] == tipo:
                        filtrado.append(hab)
                print()
                print(f'{"Número":<10}{"Precio":<10}{"Tipo":<10}{"Capacidad":<10}{"Estado":<10}')
                for hab in filtrado:
                    print(f"{hab["hab"]:<10}{hab["precio"]:<10}{hab["tipo"]:<15}{hab["capacidad"]:<5}{hab["estado"]:<10}")

            elif op == 4:
                error = True
                while error:
                    precio = input("Ingrese el precio que desea buscar: ")
                    try:
                        precio = int(precio)
                        if precio < 0:
                            raise ValueError("El precio no puede ser negativo.")
                        error = False 
                    except ValueError as error:
                        print(f"Error! {error}")
                 
                modo = menor_mayor_igual()
                filtrado = []

                if modo == "Menor":
                    print(f"Habitaciones con precio por noche {modo.lower()} a {precio}: ")
                    for hab in habitaciones_ordenados_por_num:
                        if int(hab["precio"]) <= precio:
                            filtrado.append(hab)
                
                elif modo == "Mayor":
                    print(f"Habitaciones con precio por noche {modo.lower()} a {precio}: ")
                    for hab in habitaciones_ordenados_por_num:
                        if int(hab["precio"]) >= precio:
                            filtrado.append(hab)
                
                elif modo == "Igual":
                    print(f"Habitaciones con precio por noche {modo.lower()} a {precio}: ")
                    for hab in habitaciones_ordenados_por_num:
                        if int(hab["precio"]) == precio:
                            filtrado.append(hab)
                
                if len(filtrado) > 0:
                    print()
                    print(f'{"Número":<15}|{"Precio":<15}|{"Tipo":<15}|{"Capacidad":<15}|{"Estado":<16}\n\
{"-"*15}|{"-"*15}|{"-"*15}|{"-"*15}|{"-"*16}')
                    for hab in filtrado:
                        print(f"{hab["hab"]:<15}|{hab["precio"]:<15}|{hab["tipo"]:<15}|{hab["capacidad"]:<15}|{hab["estado"]:<15}")
                
                else: 
                    print("No se registran habitaciones. ")
            
            elif op == 5:
                estado = leer_estado()
                filtrado = []
                for hab in habitaciones_ordenados_por_num:
                    if hab["estado"] == estado:
                        filtrado.append(hab)
                print()
                print(f'{"Número":<15}|{"Precio":<15}|{"Tipo":<15}|{"Capacidad":<15}|{"Estado":<16}\n\
{"-"*15}|{"-"*15}|{"-"*15}|{"-"*15}|{"-"*16}')
                for hab in filtrado:
                    print(f"{hab["hab"]:<15}|{hab["precio"]:<15}|{hab["tipo"]:<15}|{hab["capacidad"]:<15}|{hab["estado"]:<15}")

            op = validar_entero("Ingrese una opción del 1 al 5. (-1 para salir): ")
        except (FileNotFoundError, OSError) as error:
            print(f"Error! {error}")
        except:
            print("Error inesperado. Intente nuevamente. ")

#ORDENAR POR ÍNDICE: NÚMERO DE HABITACIÓN------------------------------------------------------------------------------------
def ordenar_hab(hab):
    hab.sort(key=lambda x: int(x[0]))
    return hab

#ELIMINAR HABITACIONES------------------------------------------------------------------------------------------------------
def eliminar_hab(archivo1="tabla_habitaciones.json", archivo2="habitaciones_borradas.json"):
    print_habitaciones(archivo1)
    item=validar_entero("Ingrese el número de habitación que quiera eliminar: (-1 para salir.)")    
    while item !=-1:
        try: 
            with open(archivo1, 'r', encoding="UTF-8") as data:
                habitaciones = json.load(data)
                habitaciones_ordenados_por_num = ordenar(habitaciones, "hab")
            
            nros_hab = [habi["hab"] for habi in habitaciones_ordenados_por_num]
            if item in nros_hab: 
                indice = nros_hab.index(item)
                eliminado = habitaciones_ordenados_por_num.pop(indice)
                with open(archivo1, 'w', encoding="UTF-8") as data:
                    json.dump(habitaciones_ordenados_por_num, data, ensure_ascii=False, indent=4)
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

            item=validar_entero("Ingrese el número de habitación que quiera eliminar: (-1 para salir.)") 
        except (FileNotFoundError, OSError) as error:
            print(f"Error! {error}")
        except:
            print("Error inesperado. Intente nuevamente. ")
            
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
def deshacer_borrar(archivo1="tabla_habitaciones.json", archivo2="habitaciones_borradas.json"):
    print_habitaciones(archivo2)
    item=validar_entero("Ingrese el número de habitación que quiera recuperar (-1 para salir): ")
    flag=1

    if item == -1:
        flag = 0

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
                flag=validar_entero("Si desea recuperar otra habitación ingrese 1, si no, ingrese otro numero:  ")
                        
            except (FileNotFoundError, OSError) as error:
                print(f"Error! {error}")
            
            except:
                print("Error inesperado. Intente nuevamente. ")
        
        else:
            print(f"No se encontro la habitación {item}. ")
            flag == 1

        if flag == 1:
            item = validar_entero("Ingrese el numero de habitación que quiera recuperar(-1 para salir): ")
            if item == -1:
                flag = 0
        
#VALIDACIÓN DE NÚMEROS-------------------------------------------------------------------------------------------------------------
#es_entero = lambda x: re.search(r'^-?[0-9]+$', x) is not None

#LLENAR HABITACIONES-----------------------------------------------------------------------------------------------------------------

def llenar_habitaciones(archivo="tabla_habitaciones.json"):
    numero = validar_entero("Número de habitación (-1 para salir): ") #Chequea enteros con excepciones. 
    while numero != -1:
        try: 
            with open(archivo, 'r', encoding="UTF-8") as data:
                habitaciones = json.load(data)
                habitaciones_ordenados_por_num = ordenar(habitaciones, "hab")
            for habi in habitaciones_ordenados_por_num: 
                while habi["hab"] == numero:
                    print("La habitación ya existe. ")
                    numero = validar_entero("Número de habitación: ")

            tipo_txt = leer_tipo()

            err = True
            while err:
                try:
                    precio = validar_entero("Precio (entero > 0): ")
                    if precio < 0:
                        raise ValueError("No puede ser un valor negativo.")
                    err = False
                except ValueError as e:
                    print(f"Error! {e}")
            
            err = True 
            while err:
                try:
                    capacidad = validar_entero("Capacidad (> 0): ")
                    if capacidad < 0:
                        raise ValueError("No puede ser un valor negativo.")
                    if capacidad > 10:
                        raise Exception("No existen habitaciones tan grandes.")
                    err = False
                except (ValueError,Exception) as e:
                    print(f"Error! {e}")
                except:
                    print("Error inesperado. Intente nuevamente. ")

                    
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
        except:
            print("Error inesperado. Intente nuevamente. ")
        finally: 
            numero = validar_entero("Número de habitación (-1 para salir): ")


#MODIFICAR HABITACIONES----------------------------------------------------------------------------------------------

def incremento_porcentual(tabla):
    precios_hab = [tb["precio"] for tb in tabla]
    err = True
    while err:
        inc = input("Ingrese el porcentaje que quiera incrementar. (-75% a 300%(ingresar sin %)): ")
        try:
            inc = float(inc)
            if inc < -75:
                raise Exception("No se puede bajar más de un 75%.")
            elif inc > 300:
                raise Exception("No se puede aumentar más de un 300%. ")
            err = False           
        except ValueError:
            print("Se ingreso un formato incorrecto. (Ingresar sin %)")
        except Exception as er:
            print(f"Error! {er}")
        except:
            print("Error inesperado. Intente nuevamente. ")
      
    precios_inc = list(map(lambda x: x * (1 + inc / 100), precios_hab))

    for pre in precios_inc:
        precio_ent = int(pre)
        i = precios_inc.index(pre)
        tabla[i]["precio"] = precio_ent

    return tabla


def modificar_habitacion(archivo="tabla_habitaciones.json"):
    print_habitaciones(archivo)
    print(f"\nPara efectuar un incremento porcentual del precio a todas las habitaciones, ingrese 1.\n")
    numero= validar_entero("Número de habitación a modificar (-1 para volver): ")

    while numero != -1:
        try: 
            with open(archivo, 'r', encoding="UTF-8") as data:
                habitaciones = json.load(data)
            
            nros_hab = [habi["hab"] for habi in habitaciones]
            if numero in nros_hab: 
                indice = nros_hab.index(numero)

            elif numero not in nros_hab and numero !=-1 and numero != 1:
                while numero not in nros_hab and numero !=-1 and numero != 1:
                    print("El número de habitación ingresado no existe. Ingrese otro.")
                    numero = validar_entero("Número de habitación a modificar(-1 para salir): ")
            
            if numero == 1:
                incremento_porcentual(habitaciones)
                with open(archivo, 'w', encoding="UTF-8") as data:
                    json.dump(habitaciones, data, ensure_ascii=False, indent=4)
                print("Incremento porcentual terminado. ")
     
            elif numero !=-1:
                indice = nros_hab.index(numero)
            
                print("Si no desea modificar un campo, presione enter")

                while True:
                    try:
                        nuevo_id = input("Nuevo número de habitación: ").strip()

                        if nuevo_id == "":
                            nuevo_id = habitaciones[indice]["hab"]
                            break

                        nuevo_id = int(nuevo_id)

                        if nuevo_id < 0:
                            raise ValueError("El número no puede ser negativo.")

                        if nuevo_id in nros_hab:
                            raise AssertionError("El ID ya existe.")

                        habitaciones[indice]["hab"]= nuevo_id
                        break

                    except ValueError:
                        print("Se ingresó un formato inválido.")
                    except AssertionError:
                        print("Se ingresó un ID ya existente.")


                while True:
                    try:
                        nuevo_precio = input("Precio (entero > 0): ").strip()

                        if nuevo_precio == "":
                            nuevo_precio = habitaciones[indice]["precio"]
                            break

                        nuevo_precio = int(nuevo_precio)

                        if nuevo_precio <= 0:
                            raise ValueError("Debe ser mayor a 0.")

                        habitaciones[indice]["precio"] = nuevo_precio
                        break

                    except ValueError:
                        print("Se ingresó un valor inválido.")

                while True:
                    try:
                        nuevo_tipo= input("Ingrese el tipo de habitación (Single/Doble/Triple/Suite): ").strip()
                        if nuevo_tipo == "":
                            nuevo_tipo = habitaciones[indice]["tipo"]
                            break
                        assert list(filter(lambda x: x == nuevo_tipo, tipos))
                        habitaciones[indice]["tipo"] = nuevo_tipo
                        break
                    except ValueError:
                        print("Se ingreso un formato invalido.")
                    except AssertionError:
                        print("Tipo invalido, ingrese nuevamente: ")
                
                while True:
                    try:
                        nueva_cap = input("Nueva capacidad (> 0): ").strip()
                        if nueva_cap == "":
                            nueva_cap = habitaciones[indice]["capacidad"]
                            break
                        nueva_cap = int(nueva_cap)
                        if nueva_cap <= 0:
                            raise ValueError("Debe ser mayor a 0.")
                        
                        habitaciones[indice]["capacidad"] = nueva_cap
                        break
                    except ValueError:
                        print("Se ingreso un formato invalido.")                

                while True:
                    try:
                        nuevo_estado=input("Escribí el estado (Disponible/Ocupada/Mantenimiento): ").strip()
                        if nuevo_estado == "":
                            nuevo_estado = habitaciones[indice]["estado"]
                            break
                        assert list(filter(lambda x: x == nuevo_estado, estados))

                        habitaciones[indice]["estado"] = nuevo_estado
                        break
                    except ValueError:
                        print("Se ingreso un formato invalido.")      
                    except AssertionError:
                        print("Estado invalido, ingrese nuevamente: ")  
                
                # después del último while de estado
                with open(archivo, 'w', encoding="UTF-8") as data:
                    json.dump(habitaciones, data, ensure_ascii=False, indent=4)

                print("Habitación modificada con éxito.")

                habitacion = habitaciones[indice]
                print(f"{"ID":^15}|{"Precio":<15}|{"Tipo":<15}|{"Capacidad":<16}|{"Estado":<15}\n\
{'-'*15}|{'-'*15}|{'-'*15}|{'-'*16}|{'-'*15}")
                print(f"{habitacion["hab"]:^15}|{habitacion["precio"]:<15}|{habitacion["tipo"]:<15}|{habitacion["capacidad"]:<16}|{habitacion["estado"]:<15}")
                
        except (FileNotFoundError, OSError) as error:
            print(f"Error! {error}")
        except:
            print("Error inesperado. Intente nuevamente. ")
        finally: 
            numero = validar_entero("Número de habitación (-1 para salir): ")            

#LEER TIPOS Y SUS OPCIONES--------------------------------------------------------------------------------------------------------
tipos   = ["Single", "Doble", "Triple", "Suite"]
estados = ["Disponible", "Ocupada", "Mantenimiento"]
modos = ["Menor","Mayor","Igual"]

def leer_tipo():
    
    tipo = esta_vacio("Escribí el tipo de habitación (Single/Doble/Triple/Suite): ")
    valido = list(filter(lambda x: x == tipo, tipos))
    while len(valido) == 0:
        tipo = esta_vacio("Tipo inválido. Volvé a escribir: ")
        valido = list(filter(lambda x: x == tipo, tipos))
    return tipo

def leer_estado():
    estado = esta_vacio("Escribí el estado (Disponible/Ocupada/Mantenimiento): ")
    valido = list(filter(lambda x: x == estado, estados))
    while len(valido) == 0:
        estado = esta_vacio("Estado inválido. Volvé a escribir: ")
        valido = list(filter(lambda x: x == estado, estados))
    return estado

def menor_mayor_igual():
    modo = esta_vacio(f"Buscar mayores, menores o iguales a ese numero? (menor/mayor/igual):\nOpción: ")
    valido = list(filter(lambda x: x == modo, modos))
    while len(valido)==0:
        modo = esta_vacio("Modo invalido. Volve a escribir: ")
        valido = list(filter(lambda x: x == modo, modos))
    return modo

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

