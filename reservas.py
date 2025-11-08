from habitaciones import *
from clientes import *
import re
import json
import os
from validaciones import *


def cuantas_lineas_txt(archivo):
    f = open(archivo, "r", encoding="UTF-8")
    contador = 0
    linea = f.readline()
    while linea:
        if linea.strip():  # cuenta solo si no está vacía
            contador += 1
        linea = f.readline()
    f.close()
    return contador

def leer_reservas(archivo="tabla_reservas.txt", modo_de_lectura="r"):
    try:
        with  open(archivo, modo_de_lectura, encoding="UTF-8") as contenido:
                return contenido

    except FileNotFoundError:
        print("Error, no se pudo acceder a la base de datos.")


reservas=leer_reservas()

def recorrer_archivo(archivo):
    try:
        contenido = open(archivo, "rt", encoding="UTF-8")
        linea = archivo.readline()
        while linea:
            id_reserva, dni, check_in, check_out, hab, pax, total = linea.split(";").strip()
            linea = archivo.readline()

    except FileNotFoundError:
        print("Error, no se pudo acceder a la base de datos.")
    finally:
        try:
            contenido.close() # Siempre debe cerrarse
        except:
            print("Error al cerrar el archivo")

                    
def buscar_reserva_en_archivo(archivo, dato_a_buscar):
    try:
        contenido = open(archivo, "rt", encoding="UTF-8")
        linea = archivo.readline()
        flag=0
        while linea or flag:
            id_reserva, dni, check_in, check_out, hab, pax, total = linea.split(";").strip()
            if dato_a_buscar==id_reserva:
                flag=1
            else:
                linea = archivo.readline()
        
        if flag:
            return id_reserva, dni, check_in, check_out, hab, pax, total
        else:
            return "No se encontró la reserva."

    except FileNotFoundError:
        print("Error, no se pudo acceder a la base de datos.")
    finally:
        try:
            contenido.close() # Siempre debe cerrarse
        except:
            print("Error al cerrar el archivo")
           
#Validaciones de fecha ----------------------------------------------------------------------------------------

def separar_en_lista(fecha):
    matriz_fecha = fecha.split('-')
    anio = int(matriz_fecha[0])
    mes = int(matriz_fecha[1])
    dia = int(matriz_fecha[2])
    return (anio, mes, dia)

def bisiesto(anio):
    return((anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0))

def verificar_ingresos_fecha(fecha):
    if fecha[1] < 1 or fecha[1] > 12:
        return False


    if fecha[2] < 1 or fecha[2] > dias_en_mes(fecha[0], fecha[1]):
        return False
    return True
    
def verificar_egreso(check_in, check_out):
    if tuple(check_out) <= tuple(check_in):
        return False 
    else: 
        return True

def pedir_fecha(mensaje):
    valido = False
    while not valido:
        fecha_str = input(mensaje)
        if verificar_formato_fecha(fecha_str):
            fecha = separar_en_lista(fecha_str)
            if verificar_ingresos_fecha(fecha):
                valido = True
            else:
                print("La fecha no existe, vuelva a intentar.")
        else:
            print("Formato incorrecto, use AAAA-MM-DD.")
    return fecha

def dias_en_mes(anio, mes):
    dias_mes = [31, 29 if bisiesto(anio) else 28, 31, 30, 31, 30,
                31, 31, 30, 31, 30, 31]
    return dias_mes[mes - 1]

def contar_dias(fecha):
    anio, mes, dia = fecha
    dias = 0

    for a in range(1, anio):
        dias += 366 if bisiesto(a) else 365

    for m in range(1, mes):
        dias += dias_en_mes(anio, m)
        
    dias += dia

    return dias

def diferencia_dias_entre(check_in, check_out):
    return contar_dias(check_out) - contar_dias(check_in)

#VERIFICACIONES CLIENTE --------------------------------------------------------------------------------------

def existe_cliente(dni):
    with open("tabla_clientes.json", "r", encoding="UTF-8") as datos:
        clientes = json.load(datos)
        for c in clientes:
            if c["dni"] == dni:
                return True
    return False

def buscar_cliente(dni):
    if not existe_cliente(dni):
        print("El cliente ingresado no existe en nuestra base de datos. \n Por favor, ingrese los siguientes datos: ")
        llenar_clientes_desde_reservas(dni)
        
def pedir_nombre():
    while True:
        try:
            nombre = input(str("Ingrese el nombre del cliente: "))
            break
        except ValueError:
            print("Error, ingrese un nombre válido.")

    return nombre

def pedir_apellido():
    while True:
        try:
            apellido = input(str("Ingrese el apellido del cliente: "))
            break
        except ValueError:
            print("Error, ingrese un apellido válido.")
            
    return apellido

def pedir_telefono():
    while True:
        try:
            telefono = input("Ingrese el telefono del cliente: ")
            assert len(telefono) >= 8
            break
        except ValueError:
            print("Error, ingrese un teléfono válido.")
            
        except AssertionError:
            print("Error, el teléfono debe tener al menos 8 dígitos.")
            
    return telefono

def pedir_mail():
    while True:
        try:
            mail = input(str("Ingrese el e-mail del cliente: "))
            mail_correcto = mail.count("@")
            assert mail_correcto == 1
            break
        except AssertionError:
            print("Error, ingrese un e-mail válido.")
            
        except ValueError:
            print("Error, el mail debe ser texto.")
            
    return mail

def llenar_clientes_desde_reservas(dni):
    nombre=pedir_nombre()
    apellido=pedir_apellido()
    telefono=pedir_telefono()
    mail=pedir_mail()
        
    nuevo_cliente = {"dni": dni, "nombre": nombre, "apellido": apellido, "teléfono": telefono, "mail": mail}

    with open("tabla_clientes.json", "r", encoding="UTF-8") as datos:
        archivo = json.load(datos)
        archivo.append(nuevo_cliente)
        
    with open("tabla_clientes.json", "w", encoding="UTF-8") as datos:
        json.dump(archivo, datos, ensure_ascii=False, indent=4)

    print("Finalizo la carga, prosiguiendo con la reserva. ")

#VERIFICAR HABITACIÓN  ---------------------------------------------------------------------------------------
def buscar_habitacion(nro_hab, i=0):
    with open("tabla_habitaciones.json", "r", encoding="UTF-8") as archivo:
        tabla_habitaciones = json.load(archivo)

        if i >= len(tabla_habitaciones):
            return False
        else:
            if str(tabla_habitaciones[i]["hab"]) == str(nro_hab):
                return True
        return buscar_habitacion(nro_hab, i + 1)

def verificar_existencia_habitación():
    while True:
        try:
            hab=input("Ingrese el número de habitación: ")
            assert buscar_habitacion(hab) == True
            return int(hab)
        except AssertionError:
            print("La habitación ingresada no existe.")
   
def comparar_fechas(fecha_1, fecha_2):
    return tuple(fecha_1) < tuple(fecha_2)

def coinciden_fechas(d1, h1, d2, h2):
    return comparar_fechas(d1, h2) and comparar_fechas(d2, h1)

def arreglar_fechas_archivo(fecha_str):
    año, mes, dia = tuple(map(int, fecha_str.strip("()").split(",")))
    fecha = (año, mes, dia)
    return fecha

def verificar_reservas_disponibilidad(nro_hab, check_in, check_out):
    try:
        with open("tabla_reservas.txt", "r", encoding="UTF-8") as reservas:
            linea=reservas.readline()
            linea=linea.strip()
            flag=0
            problema=0
            while flag==0:
                if not linea.strip():
                    flag=1  
                else:   
                    _, _, existente_desde, existente_hasta, hab, _, _ = linea.split(';')
                    existente_desde = arreglar_fechas_archivo(existente_desde)
                    existente_hasta = arreglar_fechas_archivo(existente_hasta)
                    if hab == str(nro_hab): 
                        flag=1
                        problema=coinciden_fechas(check_in, check_out, existente_desde, existente_hasta)
                    linea = reservas.readline()           
            if problema:
                return False
            else:
                return True
            
    except FileNotFoundError:
        print("Error, no se pudo acceder a la base de datos.")

    
def total_por_precio(dto, dias, ad):
    try:
        with open("tabla_habitaciones.json", "r", encoding="UTF-8") as habs:
            habitaciones = json.load(habs)
        for hab in habitaciones:
            if hab["hab"] == dto:
                precio_noche =hab["precio"]
                precio_total= int(precio_noche) * int(dias) + int(ad) * 4000
                return precio_total
    except:
        print("Error al acceder a la base de datos. ")

def verificar_cant_max(dto):
    try:
        with open("tabla_habitaciones.json", "r", encoding="UTF-8") as habs:
            habitaciones = json.load(habs)
        cant_maxima=0
        for hab in habitaciones:
            if int(hab["hab"]) == dto:
                cant_maxima=int(hab["capacidad"])

        if cant_maxima==0:
            print(f"No se encontró la habitación {dto}")
            return 0
        else:
            return cant_maxima
        
    except (FileNotFoundError, OSError) as e:
        print(f"error! {e}")

def validar_cant(pax, dto):
    cap_max = verificar_cant_max(dto)
    pax = int(pax)
    if int(pax) <= cap_max:
        return True, 0
    elif pax <= cap_max + 2:
        ad = pax - cap_max
        return True, ad
    else: 
        return False, 0

def digito_unico(pax):
    pax_str = str(pax)
    return pax_str.isdigit() and len(pax_str) == 1

#LLENAR RESERVAS: CREATE ---------------------------------------------------------------------------------------------
def llenar_reservas():  
        nro_dni = validar_entero("Ingrese el número de dni del cliente: (-1 para salir): ")
        ver_dni = verificar_formato(nro_dni)

        while not ver_dni and nro_dni != -1:
            print("Se ingreso un dni Invalido.")
            nro_dni= validar_entero("Ingrese el número de dni del cliente: (-1 para salir): ")
            ver_dni = verificar_formato(nro_dni)
            if nro_dni == -1:
                ver_dni = True

        while nro_dni != -1:
        #Validación ----------------------------------------------
            ver_dni = verificar_formato(nro_dni)
            while not ver_dni:
                print("Se ingreso un dni Invalido.")
                nro_dni= validar_entero("Ingrese el número de dni del cliente: (-1 para salir): ")
                ver_dni = verificar_formato(nro_dni)

        #Busqueda en clientes ------------------------------------
            buscar_cliente(nro_dni)
        #check-in y check-out -------------------------------------------
            check_in = pedir_fecha("Ingrese fecha inicio (AAAA-MM-DD): ")
            check_out = pedir_fecha("Ingrese fecha final (AAAA-MM-DD): ")
            while not verificar_egreso(check_in, check_out):
                print("El egreso debe ser posterior al ingreso.")
                check_out = pedir_fecha("Reingrese fecha fin (AAAA-MM-DD): ")

            dias = diferencia_dias_entre(check_in, check_out)
    #Validar habitaciones y fechas --------------------------------------------------
            
            dto = verificar_existencia_habitación() #VERIFICAR QUE EXISTA
            while not verificar_reservas_disponibilidad(dto, check_in, check_out):
                print(f"La habitación {dto} ya está ocupada en ese rango.")
                dto = int(input("Ingrese el numero de habitación: "))

#Total y habitación -------------------------------------------------------------
            cant_pax = input("Ingrese la cantidad de pasajeros: ")
            while not digito_unico(cant_pax):
                cant_pax = int(input("Ingrese la cantidad de pasajeros: "))

            valido, adicionales = validar_cant(cant_pax, dto)
            while not valido:
                print("Exceso de pasajeros.")
                cant_pax = int(input("Ingrese la cantidad de pasajeros: "))
                while not digito_unico(cant_pax):
                    cant_pax = int(input("Ingrese la cantidad de pasajeros: "))    
                valido, adicionales = validar_cant(cant_pax, dto)

            total = total_por_precio(dto, dias, adicionales)
            nro_reserva = cuantas_lineas_txt("tabla_reservas.txt") + 1

            reserva_nueva=((f'{nro_reserva};{nro_dni};{check_in};{check_out};{dto};{cant_pax};{total}\n'))
        
            try:   
                with open("tabla_reservas.txt", "a", encoding="UTF-8") as reservas_write:
                    reservas_write.write(reserva_nueva)
                
                print("Se agrego todo correctamente.")
                nro_dni= validar_entero("Ingrese el número de dni del cliente: (-1 para salir): ")
                reservas_write.close()
            except Exception as e:
                print(f"Ocurrio un error en la base de datos. {e}")

#UPDATE: ACTUALIZAR Y LEER ----------------------------------------------------------------------------------
def buscar_reserva_x_id(idd):

    linea=reservas.readline()
    
    while linea:
        identificador, _, _, _, _, _, _ = linea.split(";").strip()
        if identificador == idd:
            return True
        linea=reservas.readline()
    return -1

"""def dar_reserva_x_id(matriz_reservas, idd):
    i = buscar_reserva_x_id(matriz_reservas, idd)
    if i == -1:
        return False
    else: 
        return matriz_reservas[i]"""


def mostrar_opciones_mod():
    print(f"¿Que elemento/s de la reserva desea modificar?:\n \
(El id, dni del cliente y el total de la reserva no son posibles de modificar.) \n \
1-Fechas de entrada y salida\n \
2-Número de habitación\n \
3-Cantidad de pasajeros")

def modo_busqueda():
    print(f"¿Como desea buscar la reserva? \n \
    1 - ID de reserva. \n \
    2 - DNI del cliente.")
    busq = int(input("Por favor, solo ingrese una opción correcta: "))
    return busq

def formatear_fecha(fecha):
    return str(fecha[0]).zfill(4) + "-" + str(fecha[1]).zfill(2) + "-" + str(fecha[2]).zfill(2)

def print_reserva(matriz, pos):
    fila = matriz[pos]
    id_reserva, dni, check_in, check_out, hab, pax, total = fila
    print("")
    print("------------------------------------------------------------------")
    print("ID   | DNI Cliente | Entrada     | Salida      | Hab | Pax | Total")
    print("------------------------------------------------------------------")
    print(str(id_reserva).ljust(4), "|",
          str(dni).ljust(11), "|",
          arreglar_fechas_archivo(check_in).ljust(11), "|",
          arreglar_fechas_archivo(check_out).ljust(11), "|",
          str(hab).ljust(3), "|",
          str(pax).ljust(3), "|",
          str(total).ljust(6))

def menu_mostrar():
    print(f"¿Que desea ver? Ingrese una opción: \n \
        1 - Tabla reservas completa. \n \
        2 - Buscar por DNI. \n \
        3 - Buscar por habitación. \n \
        4 - Totales: Mayor a menor. \n \
        5 - Totales: Menor a mayor. \n\
        6 - Ordenar por fecha de entrada: \n \
")

def mostrar_reservas_por_hab_o_clt(hab, x):
    #return [res for res in matriz if res[x] == hab]
    with open("tabla_reservas.txt", "r", encoding="UTF-8") as reservas: 
        linea=reservas.readline()
        reservas_hab=[]
        while linea:
            id_reserva, dni, check_in, check_out, nro_hab, pax, total = list(map(str, linea.strip().split(";")))
            check_in = arreglar_fechas_archivo(check_in)
            check_out = arreglar_fechas_archivo(check_out)
            if x==4:
                if int(nro_hab) == hab:
                    reservas_hab.append([id_reserva, dni, check_in, check_out, nro_hab, pax, total])
                linea=reservas.readline()
            if x==1:
                if int(dni) == hab:
                    reservas_hab.append([id_reserva, dni, check_in, check_out, nro_hab, pax, total])
                linea=reservas.readline()
        reservas.close()
        return [res for res in reservas_hab]


def ordenar_menor_mayor(parametro):
    try:
        matriz_reservas=[]
        with open("tabla_reservas.txt", 'r', encoding="UTF-8") as reservas:
            linea=reservas.readline()
            while linea:
                id_reserva, dni, check_in, check_out, hab, pax, total = list(map(str, linea.strip().split(";")))
                check_in = arreglar_fechas_archivo(check_in)
                check_out = arreglar_fechas_archivo(check_out)
                total = int(total)
                matriz_reservas.append([id_reserva, dni, check_in, check_out, hab, pax, total])
                linea=reservas.readline()

            matriz_reservas.sort(key=lambda x: x[parametro])
            return matriz_reservas
    except Exception as e:
        print(f"Error con la base de datos. {e}")

def ordenar_totales_mayor_menor():
    try:
        matriz_reservas=[]
        with open("tabla_reservas.txt", 'r', encoding="UTF-8") as reservas:
            linea=reservas.readline()
            while linea:
                id_reserva, dni, check_in, check_out, hab, pax, total = list(map(str, linea.strip().split(";")))
                check_in = arreglar_fechas_archivo(check_in)
                check_out = arreglar_fechas_archivo(check_out)
                total = int(total)
                matriz_reservas.append([id_reserva, dni, check_in, check_out, hab, pax, total])
                linea=reservas.readline()

            matriz_reservas.sort(key=lambda x: x[6], reverse=True)
            return matriz_reservas
    except Exception as e:
        print(f"Error con la base de datos. {e}")
    

#MOSTRAR LEER ETC
def print_elegir_opcion():
    menu_mostrar()
    op = int(input("Ingrese la opción elegida:"))
    if op == 1:
        print_tabla_reservas("tabla_reservas.txt")
    elif op == 2:
        cliente = input("Ingrese el DNI del cliente: ")
        ver_dni = verificar_formato(cliente)
        while not ver_dni:
            print("Se ingreso un dni Invalido.")
            cliente= input("Ingrese el número de dni del cliente: (-1 para salir): ")
            ver_dni = verificar_formato(cliente)
        cliente = int(cliente)
        reservas_cliente = mostrar_reservas_por_hab_o_clt(cliente, x=1)
        if len(reservas_cliente)==0:
            print(f"El Dni {cliente} no tiene ninguna reserva en el alojamiento.")
        else: 
            print_tabla_reservas_lst(reservas_cliente)
    elif op == 3:
        print("Elija el numero de habitación: ")
        print_habitaciones("tabla_habitaciones.json")
        hab = int(input("Habitación elegida: "))
        reservas_habitacion = mostrar_reservas_por_hab_o_clt(hab, x=4)
        print_tabla_reservas_lst(reservas_habitacion)
    elif op == 4:
        totales_ord = ordenar_totales_mayor_menor()
        print_tabla_reservas_lst(totales_ord)
    elif op == 5:
        totales_ord = ordenar_menor_mayor(6)
        print_tabla_reservas_lst(totales_ord)
    elif op==6:
        totales_ord = ordenar_menor_mayor(2)
        print_tabla_reservas_lst(totales_ord)

def print_tabla_reservas(archivo):
    try:
        with open(archivo, "rt", encoding="UTF-8") as data:
            linea = data.readline()
            print("")
            print("------------------------------------------------------------------")
            print("ID   | DNI Cliente | Entrada     | Salida      | Hab | Pax | Total")
            print("------------------------------------------------------------------")

            while linea:
                id_reserva, dni, check_in, check_out, hab, pax, total = list(map(str, linea.strip().split(";")))
                check_in = arreglar_fechas_archivo(check_in)
                check_out = arreglar_fechas_archivo(check_out)
                check_in_str = f"{check_in[0]}-{check_in[1]}-{check_in[2]}"
                check_out_str = f"{check_out[0]}-{check_out[1]}-{check_out[2]}"
                print(str(id_reserva).ljust(4), "|",
                str(dni).ljust(11), "|",
                check_in_str.ljust(11), "|",
                check_out_str.ljust(11), "|",
                str(hab).ljust(3), "|",
                str(pax).ljust(3), "|",
                str(total).ljust(6))
                linea = data.readline() # Leemos la línea siguiente
    except OSError:
        print("No se pudo leer el archivo")

def print_tabla_reservas_lst(lista):
    print("")
    print("------------------------------------------------------------------")
    print("ID   | DNI Cliente | Entrada     | Salida      | Hab | Pax | Total")
    print("------------------------------------------------------------------")
    for li in lista:
        id_reserva, dni, check_in, check_out, hab, pax, total = li
        check_in_str = f"{check_in[0]}-{check_in[1]}-{check_in[2]}"
        check_out_str = f"{check_out[0]}-{check_out[1]}-{check_out[2]}"
        print(str(id_reserva).ljust(4), "|",
        str(dni).ljust(11), "|",
        check_in_str.ljust(11), "|",
        check_out_str.ljust(11), "|",
        str(hab).ljust(3), "|",
        str(pax).ljust(3), "|",
        str(total).ljust(6))





#MODIFICACION --------------------------------------------------------------------------------------------------------------
def modificacion():
    busq = modo_busqueda()
    while busq != 1 and busq != 2:
        busq = modo_busqueda()
    if busq == 1: 
        id_reserva = int(input("Ingrese el id de reserva: "))
        existe = buscar_reserva_x_id(id_reserva)
        while not existe:
            id_reserva = int(input("Ingrese el id de reserva: "))
            existe = buscar_reserva_x_id(id_reserva)  
              
        i = buscar_reserva_x_id(id_reserva)

    elif busq == 2:
        nro_dni= input("Ingrese el número de dni del cliente: (-1 para salir): ")
        ver_dni = verificar_formato(nro_dni)
        existe = existe_cliente(int(nro_dni))
        reservas_cliente = mostrar_reservas_por_hab_o_clt(int(nro_dni), x=1)
        while not ver_dni or not existe or reservas_cliente == 0:
            if not ver_dni: 
                print("Se ingreso un dni Invalido.")
            elif not existe:
                print(" El cliente no existe en la base de datos.")
            elif len(reservas_cliente) == 0:
                print(" El cliente no tiene reservas registradas.")

            nro_dni= input("Ingrese el número de dni del cliente: (-1 para salir): ")
            ver_dni = verificar_formato(nro_dni)
            existe = existe_cliente(int(nro_dni))


        print(f" ID | DNI Cliente | Entrada | Salida | Habitación | Pax | Total")
        for el in reservas_cliente:
            print(el, end=" ") 
            print("")   

        print("Se mostraron las reservas del cliente junto a su id, por favor elija una opción: ")
        id_reserva = int(input("Ingrese el id de reserva: "))
        existe = buscar_reserva_x_id(id_reserva)
        while not existe:
            id_reserva = int(input("Ingrese el id de reserva: "))
            existe = buscar_reserva_x_id(id_reserva)  
              
        i = buscar_reserva_x_id(id_reserva)

    mostrar_opciones_mod()
    opcion_elegida = int(input("Ingrese la opción elegida: (-1 para retroceder.)"))

"""while opcion_elegida != -1:

#FECHAS ----------------------------------------------------------------------       
        if opcion_elegida == 1:
            check_in = pedir_fecha("Ingrese fecha inicio (AAAA-MM-DD): ")
            check_out = pedir_fecha("Ingrese fecha final (AAAA-MM-DD): ")
            #modificados_reservas = matriz_reservas.pop(i)

            while not verificar_egreso(check_in, check_out):
                print("El egreso debe ser posterior al ingreso.")
                check_out = pedir_fecha("Reingrese fecha fin (AAAA-MM-DD): ")
            
            dias = diferencia_dias_entre(check_in, check_out)

            dto = modificados_reservas[4]
            while not verificar_reservas_disponibilidad(nro_hab=dto, check_in=check_in, check_out=check_out):
                print(f"La habitación {dto} ya está ocupada en ese rango.")
                dto = int(input("Ingrese el numero de habitación: "))
            
            cant_pax = modificados_reservas[5]
            valido, adicionales = validar_cant(cant_pax, dto)
            while not valido:
                print("Exceso de pasajeros.")
                cant_pax = int(input("Ingrese la cantidad de pasajeros: "))
                while not digito_unico(cant_pax):
                    cant_pax = int(input("Ingrese la cantidad de pasajeros: "))    
                valido, adicionales = validar_cant(cant_pax, dto)

            total = total_por_precio(dto, dias, adicionales)
            print(total)
            modif = [modificados_reservas[0], modificados_reservas[1], check_in, check_out, dto, cant_pax, total]
          mat_mod_anterior.append(modificados_reservas.pop())
            mat_mod_posterior.append(modif)
            matriz_reservas.insert(i, modif)
            print_reserva(matriz_reservas, i)
        
        if opcion_elegida == 2:
            modificados_reservas = matriz_reservas.pop(i)
            check_in = modificados_reservas[2]
            check_out = modificados_reservas[3]
            dias = diferencia_dias_entre(check_in, check_out)
            dto = int(input("Ingrese el número de habitación: "))
            while not verificar_reservas_disponibilidad(dto, check_in, check_out):
                print(f"La habitación {dto} ya está ocupada en ese rango.")
                dto = int(input("Ingrese el numero de habitación: "))
            
            cant_pax = modificados_reservas[5]
            valido, adicionales = validar_cant(cant_pax, dto)
            while not valido:
                print("Exceso de pasajeros.")
                cant_pax = int(input("Ingrese la cantidad de pasajeros: "))
                while not digito_unico(cant_pax):
                    cant_pax = int(input("Ingrese la cantidad de pasajeros: "))    
                valido, adicionales = validar_cant(cant_pax, dto)
            
            total = total_por_precio(dto, dias, adicionales)
            modif = [modificados_reservas[0], modificados_reservas[1], check_in, check_out, dto, cant_pax, total]
            mat_mod_anterior.append(modificados_reservas.pop())
            mat_mod_posterior.append(modif)
            matriz_reservas.insert(i, modif)
            print_reserva(matriz_reservas, i)

        if opcion_elegida == 3:
            modificados_reservas = matriz_reservas.pop(i)
            check_in = modificados_reservas[2]
            check_out = modificados_reservas[3]
            dias = diferencia_dias_entre(check_in, check_out)
            dto = modificados_reservas[4]

            cant_pax = int(input("Ingrese la cantidad de pasajeros: "))
            valido, adicionales = validar_cant(cant_pax, dto)
            while not valido:
                print("Exceso de pasajeros.")
                cant_pax = int(input("Ingrese la cantidad de pasajeros: "))
                while not digito_unico(cant_pax):
                    cant_pax = int(input("Ingrese la cantidad de pasajeros: "))    
                valido, adicionales = validar_cant(cant_pax, dto)

            total = total_por_precio(dto, dias, adicionales)
            modif = [modificados_reservas[0], modificados_reservas[1], check_in, check_out, dto, cant_pax, total]
            mat_mod_anterior.append(modificados_reservas.pop())
            mat_mod_posterior.append(modif)
            matriz_reservas.insert(i, modif)
            
            print_reserva(matriz_reservas, i)

        opcion_elegida = int(input("Ingrese la opción elegida: (-1 para retroceder.)"))"""

#DELETE: BORRAR --------------------------------------------------------------------------------------
def eliminar_reserva(archivo_del_que_eliminar, archivo_al_que_guardar, eliminar_o_recuperar="eliminar"):
    with open(archivo_del_que_eliminar, "r", encoding="UTF-8") as reservass:
        id_eliminar = int(input(f"Ingrese el número de reserva que quiera {eliminar_o_recuperar}: "))
        aux=open("temp.txt", "w", encoding="UTF-8")
        encontrado=False
        #linea = reservas.readline()
        for linea in reservass:
            id_reserva, _, _, _, _, _, _ = linea.strip().split(";")
            if str(id_eliminar)!=id_reserva:
                while linea:
                    aux.write(linea)
                    linea = reservass.readline()
            else:
                encontrado=True
                with open(archivo_al_que_guardar, "a", encoding="UTF-8") as eliminadas:
                    eliminadas.write("\n", linea)
                linea = reservass.readline()
        aux.close()
        reservass.close()

        if encontrado:
            try:
                os.remove(archivo_del_que_eliminar)       # elimina el original
                os.rename("temp.txt", archivo_del_que_eliminar) # renombra el temporal
                print(f"Producto {id_eliminar} procesado correctamente.")
            except OSError as error:
                print("Error al reemplazar el archivo:", error)
        else:
            os.remove("temp.txt")  # eliminamos el temporal si no se usó
            print(f"No se encontró el producto {id_eliminar}.")

"""def deshacer_eliminar_reserva(matriz_reservas=reservas, reservas_eliminadas=reservas_eliminadas):
    id_recuperar = int(input("Ingrese el número de reserva que quisiera recuperar: "))
    flag = 1
    while flag == 1: 
        flag = 0
        pos=buscar_reserva_x_id(reservas_eliminadas, id_recuperar)
        if pos != -1:
            reserva = reservas_eliminadas.pop(pos)
            matriz_reservas.insert(reserva[0]-1, reserva)
            print(f"La reserva nro {id_recuperar} ha sido recuperada con exito.")
            flag = int(input("Si desea recuperar otra habitación, ingrese 1, si no, ingrese 0: "))
        else: 
            print(f"No se encontro la habitación {id_recuperar}.")
            id_recuperar = int(input("Ingrese el número de reserva nuevamente: "))
        if flag == 1:
            id_recuperar = int(input("Ingrese el número de reserva que quiera recuperar: "))"""

def imprimir_factura(clt_act, hoy):
    #encabezado
    linea=("-")*80
    factura=(f'{str(nro_factura[0]).zfill(4)}-{str(nro_factura[1]).zfill(8)}')
    print(f'{linea}\n'\
    f'{empresa["nombre"].title():^80}\n'\
    f'{linea}\n'\
    f'{"Factura: "+factura:<40}{"Cuit: "+empresa["cuit"]:>40}\n'\
    f'{"Domicilio fiscal: "+empresa['dirección'].title():<80}\n'\
    f'{"Web: "+empresa['web']:<80}\n'\
    f'Período: 2025-08\n'\
    f'{"Soporte: "+empresa['email']:<80}\n'\
    f'{linea}\n')
    
    nro_factura[0]+=1
    nro_factura[1]+=1
    #cuerpo
    print(f'{'Datos del cliente':^80}\n'\
    f'{"Nombre y Apellido: "+ m_clientes[clt_act][1]+" "+ m_clientes[clt_act][2]:<80}\n'\
    f'{"Dni: "+ str(m_clientes[clt_act][0])}\n')

    print(f'{LINEA}\n|{"Nro. de reserva":^17}|{"Descripción":^19}|{"Precio por día":^18}|{"Días":^10}|{"Valor":^10}|\n{LINEA}')
    reservas_del_clt=[]
    total=0
    for i in range(len(reservas)):
        if reservas[i][1]==m_clientes[clt_act][0]:
            reservas_del_clt.append(reservas[i])
    for i in range(len(reservas_del_clt)):
        dias=diferencia_dias_entre(check_in=reservas_del_clt[i][2],check_out=reservas_del_clt[i][3])
        valor=reservas_del_clt[i][6]*dias
        total+=valor
        print(f'|{reservas_del_clt[i][0]:^17}|{"Habitación "+str(reservas_del_clt[i][4]):^19}|{reservas_del_clt[i][6]:^18}|{dias:^10}|{valor:^10}|')
    print(LINEA)
    print(f'{"Fecha de impresión: "+ str(hoy):<40}{"Subtotal: "+str(total):>40}\n{"Total IVA: "+str(0.21*total):>80}\n{"Total: "+ str((IVA(total))):>80}\n')


if __name__ == "__main__":
    # pruebas manuales acá
    pass

