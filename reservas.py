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

def leer_reservas(archivo="data/txt/tabla_reservas.txt", modo_de_lectura="r"):
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

def pedir_fecha_mod(mensaje):
    valido = False
    while not valido:
        fecha_str = input(mensaje)
        if fecha_str=="":
            return fecha_str
        else:
            if verificar_formato_fecha(fecha_str):
                fecha = separar_en_lista(fecha_str)
                if verificar_ingresos_fecha(fecha):
                    valido = True
                else:
                    print("La fecha no existe, vuelva a intentar.")
            else:
                print("Formato incorrecto, use AAAA-MM-DD.")
    return fecha

def pedir_fecha_mod(mensaje):
    valido = False
    while not valido:
        fecha_str = input(mensaje)
        if fecha_str=="":
            return fecha_str
        else:
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
    with open("data/json/tabla_clientes.json", "r", encoding="UTF-8") as datos:
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
        
    nuevo_cliente = {"dni": dni, "nombre": nombre, "apellido": apellido, "telefono": telefono, "mail": mail}

    with open("data/json/tabla_clientes.json", "r", encoding="UTF-8") as datos:
        archivo = json.load(datos)
        archivo.append(nuevo_cliente)
        
    with open("data/json/tabla_clientes.json", "w", encoding="UTF-8") as datos:
        json.dump(archivo, datos, ensure_ascii=False, indent=4)

    print("Finalizo la carga, prosiguiendo con la reserva. ")

#VERIFICAR HABITACIÓN  ---------------------------------------------------------------------------------------
def verificar_formato_fecha(fecha):
    formato = r"^\d{4}-\d{2}-\d{2}$"
    if re.match(formato, str(fecha)):
        return True
    else:
        return False

def buscar_habitacion(nro_hab, i=0):
    with open("data/json/tabla_habitaciones.json", "r", encoding="UTF-8") as archivo:
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
    return fecha_1 < fecha_2

def coinciden_fechas(d1, h1, d2, h2):
    return comparar_fechas(d1, h2) and comparar_fechas(d2, h1)

def arreglar_fechas_archivo(fecha_str):
    año, mes, dia = tuple(map(int, fecha_str.strip("()").split(",")))
    fecha = (año, mes, dia)
    return fecha

def verificar_reservas_disponibilidad(nro_hab, check_in, check_out):
    try:
        with open("data/txt/tabla_reservas.txt", "r", encoding="UTF-8") as reservas:
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
        with open("data/json/tabla_habitaciones.json", "r", encoding="UTF-8") as habs:
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
        with open("data/json/tabla_habitaciones.json", "r", encoding="UTF-8") as habs:
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
            nro_reserva = cuantas_lineas_txt("data/txt/tabla_reservas.txt") + 1

            reserva_nueva=((f'{nro_reserva};{nro_dni};{check_in};{check_out};{dto};{cant_pax};{total}\n'))
        
            try:   
                with open("data/txt/tabla_reservas.txt", "a", encoding="UTF-8") as reservas_write:
                    reservas_write.write(reserva_nueva)
                
                print("Se agrego todo correctamente.")
                nro_dni= validar_entero("Ingrese el número de dni del cliente: (-1 para salir): ")
                reservas_write.close()
            except Exception as e:
                print(f"Ocurrio un error en la base de datos. {e}")

#UPDATE: ACTUALIZAR Y LEER ----------------------------------------------------------------------------------
def buscar_reserva_x_id(idd):

    try:
        with open("data/txt/tabla_reservas.txt", "r", encoding="UTF-8") as reservas:
                linea=reservas.readline()
                identificador, _, _, _, _, _, _ = linea.strip().split(";")
                identificador=str(identificador)
                while linea:
                    
                    if identificador == str(idd):
                        return True
                    else:
                        linea=reservas.readline()
                        identificador, _, _, _, _, _, _ = linea.strip().split(";")
                        identificador=str(identificador)
                    
                return -1
    except:
        print("Error, no se pudo acceder a la base de datos.")


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
    busq = validar_entero("Por favor, solo ingrese una opción correcta (-1 para salir): ")
    return busq

def formatear_fecha(fecha):
    return str(fecha[0]).zfill(4) + "-" + str(fecha[1]).zfill(2) + "-" + str(fecha[2]).zfill(2)


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
    with open("data/txt/tabla_reservas.txt", "r", encoding="UTF-8") as reservas: 
        linea=reservas.readline()
        reservas_hab=[]
        while linea:
            id_reserva, dni, check_in, check_out, nro_hab, pax, total = list(map(str, linea.strip().split(";")))
            check_in = arreglar_fechas_archivo(check_in)
            check_out = arreglar_fechas_archivo(check_out)
            id_reserva, dni, check_in, check_out, nro_hab, pax, total = linea.strip().split(";")
            if x==4:
                if int(nro_hab) == hab:
                    reservas_hab.append([id_reserva, dni, check_in, check_out, nro_hab, pax, total])
                linea=reservas.readline()
            if x==1:
                if int(dni) == hab:
                    reservas_hab.append([id_reserva, dni, check_in, check_out, nro_hab, pax, total])
                linea=reservas.readline()
        reservas.close()
    if len(reservas_hab)>=1:
        return [res for res in reservas_hab]#ARREGLAR SALIDA, ES UNA TUPLA FOR SOME REASON
    else:
        return 0

def ordenar_menor_mayor(parametro):
    try:
        matriz_reservas=[]
        with open("data/txt/tabla_reservas.txt", 'r', encoding="UTF-8") as reservas:
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
        with open("data/txt/tabla_reservas.txt", 'r', encoding="UTF-8") as reservas:
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
    op = int(input("Ingrese la opción elegida: "))
    if op == 1:
        print_tabla_reservas("data/txt/tabla_reservas.txt")
    elif op == 2:
        cliente = validar_entero("Ingrese el DNI del cliente: ")
        ver_dni = verificar_formato(cliente)
        while not ver_dni and cliente != -1:
            print("Se ingreso un dni Invalido.")
            cliente= validar_entero("Ingrese el número de dni del cliente: (-1 para salir): ")
            ver_dni = verificar_formato(cliente)
        cliente = int(cliente)
        reservas_cliente = mostrar_reservas_por_hab_o_clt(cliente, x=1)
        if not reservas_cliente:
            print(f"El Dni {cliente} no tiene ninguna reserva en el alojamiento.")          
        elif cliente != -1: 
            print_tabla_reservas_lst(reservas_cliente)

    elif op == 3:
        print("Elija el numero de habitación: ")
        print_habitaciones("data/json/tabla_habitaciones.json")
        hab = validar_entero("Habitación elegida: ")
        reservas_habitacion = mostrar_reservas_por_hab_o_clt(hab, x=4)
        if not reservas_habitacion:
            print(f"La habitación {hab} no tiene reservas. ")
        elif hab != -1:
            print_tabla_reservas_lst(reservas_habitacion)

    elif op == 4:
        totales_ord = ordenar_totales_mayor_menor()
        print_tabla_reservas_lst2(totales_ord)
    elif op == 5:
        totales_ord = ordenar_menor_mayor(6)
        print_tabla_reservas_lst2(totales_ord)
    elif op==6:
        totales_ord = ordenar_menor_mayor(2)
        print_tabla_reservas_lst2(totales_ord)

def print_tabla_reservas(archivo):
    try:
        with open(archivo, "rt", encoding="UTF-8") as data:
            linea = data.readline()
            print(f'\n{LINEA}\n{"ID":^9}|{"DNI Cliente":^13}|{"Entrada":^11}|{"Salida":^11}|{"Hab":^10}|{"Pax":^10}|{"Total":^10}\n\
{"-"*9}|{"-"*13}|{"-"*11}|{"-"*11}|{"-"*10}|{"-"*10}|{"-"*10}')

            while linea:
                id_reserva, dni, check_in, check_out, hab, pax, total = list(map(str, linea.strip().split(";")))
                check_in = arreglar_fechas_archivo(check_in)
                check_out = arreglar_fechas_archivo(check_out)
                check_in_str = f"{check_in[0]}-{check_in[1]}-{check_in[2]}"
                check_out_str = f"{check_out[0]}-{check_out[1]}-{check_out[2]}"
                print(f'{id_reserva:^9}|{dni:^13}|{check_in_str:^11}|{check_out_str:^11}|{hab:^10}|{pax:^10}|{total:^10}')

                linea = data.readline() # Leemos la línea siguiente
    except OSError:
        print("No se pudo leer el archivo")

def print_tabla_reservas_lst(lista):
    if len(lista) == 0:
        print("No posee información.")
    else:
        print("")
        print("------------------------------------------------------------------")
        print("ID   | DNI Cliente | Entrada     | Salida      | Hab | Pax | Total")
        print("------------------------------------------------------------------")
        for li in lista:
            id_reserva, dni, check_in, check_out, hab, pax, total = li
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

def print_tabla_reservas_lst2(lista):
    if len(lista) == 0:
        print("No posee información.")
    else:
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
    idd= None
    while busq != 1 and busq != 2 and busq != -1:
        busq = modo_busqueda()
    if busq == 1: 
        id_reserva = validar_entero("Ingrese el id de reserva (-1 para salir): ")
        existe = buscar_reserva_x_id(id_reserva)
        while not existe and id_reserva != -1:
            id_reserva = validar_entero("La reserva no existe. Ingrese un id existente. (-1 para salir): ")
            existe = buscar_reserva_x_id(id_reserva)  
            
    elif busq == 2:
        while True:
            try:
                nro_dni= input("Ingrese el número de dni del cliente: ")
                assert verificar_formato(nro_dni)== True
                assert existe_cliente(int(nro_dni)) == True
                break
            except AssertionError as dni:
                print("Se ingreso un dni Invalido.")
            except AssertionError:
                print(" El cliente no existe en la base de datos.")

        while True:
            try:
                assert mostrar_reservas_por_hab_o_clt(int(nro_dni), x=1)!=0
                reservas_cliente = mostrar_reservas_por_hab_o_clt(int(nro_dni), x=1)
                print_tabla_reservas_lst(reservas_cliente)
                print("Se mostraron las reservas del cliente junto a su id, por favor elija una opción: ")
                break
            except:
                print("El cliente no posee reservas.")
                while True or nro_dni==-1:
                    try:
                        nro_dni= input("Ingrese el número de dni del cliente: ")
                        assert verificar_formato(nro_dni)== True
                        assert existe_cliente(int(nro_dni)) == True
                        break
                    except AssertionError as dni:
                        print("Se ingreso un dni Invalido.")
                    except AssertionError:
                        print(" El cliente no existe en la base de datos.")

        id_reserva = validar_entero("Ingrese el id de reserva (-1 para salir): ")

        existe = buscar_reserva_x_id(id_reserva)
        while not existe:
            id_reserva = validar_entero("Ingrese el id de reserva (-1 para salir): ")
            existe = buscar_reserva_x_id(id_reserva)  
    else:
        id_reserva = -1
#-----------------------------------------------------------------------------------------------------------------------------
#borro la que voy a modificar antes de modificarla
    while id_reserva != -1:
        with open("data/txt/tabla_reservas.txt", "r", encoding="UTF-8") as reservass:
            aux=open("data/txt/temp.txt", "w", encoding="UTF-8")
            reserva_a_mod= open("data/txt/reserva_a_mod.txt", "w", encoding="UTF-8")
            encontrado=False
        
            for linea in reservass:
                id_rsrv_a_mod, _, _, _, _, _, _ = linea.strip().split(";")
                if str(id_reserva)!=id_rsrv_a_mod:
                    aux.write(linea)
                else:
                    encontrado=True
                    reserva_a_mod.write(linea)

            aux.close()
            reservass.close()
            reserva_a_mod.close()

        if encontrado:
            try:
                os.remove("data/txt/tabla_reservas.txt")       # elimina el original
                os.rename("data/txt/temp.txt", "data/txt/tabla_reservas.txt") # renombra el temporal
        
            except OSError as error:
                print("Error al reemplazar el archivo:", error)
        else:
            os.remove("data/txt/temp.txt")  # eliminamos el temporal si no se usó

    #-----------------------------------------------------------------------------------------------------------------------------
        reserva_a_mod=open("data/txt/reserva_a_mod.txt", "r", encoding="UTF-8")
        linea_mod= reserva_a_mod.readline()

        idd, dni, check_in, check_out, hab, pax, _ = linea_mod.strip().split(";")

        reserva_a_mod.close()
        os.remove("data/txt/reserva_a_mod.txt")   

    #-----------------------------------------------------------------------------------------------------------------------------

        print("Si no desea modificar un campo, presione Enter para continuar.")
        while True:
            try:
                dni_nuevo = input(f"Ingrese nuevo DNI del cliente ({dni}): ").strip()
                if dni_nuevo == "":
                    dni_nuevo = dni
                else:
                    assert verificar_formato(dni_nuevo) == True
                    assert existe_cliente(int(dni_nuevo)) == True
                break
            except AssertionError as formato:
                print("DNI inválido.")
            except AssertionError as cliente:
                print("El cliente no existe en la base de datos.")
                llenar_clientes_desde_reservas(dni_nuevo)
                print("Cliente agregado a la base de datos.")
                dni_nuevo = dni_nuevo 
        while True:
            try:
                check_in_nuevo = pedir_fecha_mod(f"Ingrese nueva fecha de check-in ({check_in})AAAA-MM-DD: ")
                if check_in_nuevo == "":
                    check_in_nuevo = arreglar_fechas_archivo(check_in)
                break
            except AssertionError:
                print("El formato ingresado es inválido.")
        while True:
            try:
                check_out_nuevo = pedir_fecha_mod(f"Ingrese nueva fecha de check-out ({check_out}) AAAA-MM-DD: ")
                if check_out_nuevo == "":
                    check_out_nuevo = arreglar_fechas_archivo(check_out)
                else:
                    assert verificar_egreso(check_in_nuevo, check_out_nuevo) == True
                break
            except AssertionError as formato:
                print("Fecha inválida.")
            except AssertionError as egreso:
                print("La fecha de check-out debe ser posterior a la de check-in.")
        while True:
            try:
                dto_nuevo = input(f"Ingrese nuevo número de habitación ({hab}): ").strip()
                if dto_nuevo == "":
                    dto_nuevo = hab
                    while not verificar_reservas_disponibilidad(dto_nuevo, check_in_nuevo, check_out_nuevo):
                        print(f"La habitación {dto_nuevo} ya está ocupada en ese rango.")
                        dto = int(input("Ingrese el numero de habitación: "))
                else:
                    assert buscar_habitacion(dto_nuevo) == True
                break
            except AssertionError:
                print("La habitación ingresada no existe.") 
        while True:
            try:
                cant_pax_nuevo = input(f"Ingrese nueva cantidad de pasajeros ({pax}): ").strip()
                if cant_pax_nuevo == "":
                    cant_pax_nuevo = pax
                    valido, adicionales = validar_cant(int(cant_pax_nuevo), int(dto_nuevo))
                else:
                    valido, adicionales = validar_cant(int(cant_pax_nuevo), int(dto_nuevo))
                    assert valido == True
                break          
            except AssertionError:
                print("Exceso de pasajeros para la habitación seleccionada.")
                    
        dias = diferencia_dias_entre(check_in_nuevo, check_out_nuevo)
        total_nuevo = total_por_precio(int(dto_nuevo), dias, adicionales)

        nueva_linea=(f'{idd};{dni_nuevo};{check_in_nuevo};{check_out_nuevo};{dto_nuevo};{cant_pax_nuevo};{total_nuevo}\n')
        with open("data/txt/tabla_reservas.txt", "a", encoding="UTF-8") as archivo:
            archivo.write(nueva_linea)

#DELETE: BORRAR --------------------------------------------------------------------------------------
def eliminar_reserva(archivo_del_que_eliminar, archivo_al_que_guardar, eliminar_o_recuperar="eliminar"):
    with open(archivo_del_que_eliminar, "r", encoding="UTF-8") as reservass:
        id_eliminar = validar_entero(f"Ingrese el número de reserva que quiera {eliminar_o_recuperar}: ")
        aux=open("data/txt/temp.txt", "w", encoding="UTF-8")
        encontrado=False
        #linea = reservas.readline()
        for linea in reservass:
            id_reserva, _, _, _, _, _, _ = linea.strip().split(";")
            if str(id_eliminar)==id_reserva:
                encontrado=True
                with open(archivo_al_que_guardar, "a", encoding="UTF-8") as eliminadas:
                    eliminadas.write(linea)
            else:
                aux.write(linea)

        aux.close()
        reservass.close()

        if encontrado:
            try:
                os.remove(archivo_del_que_eliminar)       # elimina el original
                os.rename("data/txt/temp.txt", archivo_del_que_eliminar) # renombra el temporal
                print(f"Producto {id_eliminar} procesado correctamente.")
                print_tabla_reservas(archivo_del_que_eliminar)
            except OSError as error:
                print("Error al reemplazar el archivo:", error)
        else:
            os.remove("data/txt/temp.txt")  # eliminamos el temporal si no se usó
            print(f"No se encontró el producto {id_eliminar}.")

def obtener_id_reserva(linea):
    try:
        if not linea.strip():
            return 9999999
        
        id_reserva, _, _, _, _, _, _ = linea.strip().split(";")
        return int(id_reserva)

    except (ValueError, IndexError):
        print(f"Advertencia: Línea mal formateada: {linea.strip()}")
        return 9999999

def ordenar_archivo_reservas(archivo):
    lineas = []
    try: 
        with open(archivo, 'r', encoding="UTF-8") as reservas:
            linea = reservas.readline()
            while linea: 
                if linea.strip():
                    lineas.append(linea)
                linea = reservas.readline()
            
        if not lineas:
            print("archivo vacio.")
        
        lineas_ordenadas = sorted(lineas, key=obtener_id_reserva)

        with open(archivo, "w", encoding="UTF-8") as reservas:
            reservas.writelines(lineas_ordenadas)
    
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo}' no fue encontrado.")
    
    except OSError as e:
        print(f"Error al escribir en el archivo: {e}")


if __name__ == "__main__":
    pass
#FACTURACIÓN --------------------------------------------------------------------------------------------------------------

def ver_factura():
    dni_cli = validar_entero("Ingrese el Dni del cliente para generar la factura: ")
    fecha_hoy = pedir_fecha("Ingrese la fecha de hoy (AAAA-MM-DD): ")
    imprimir_factura(dni_cli, fecha_hoy)

def imprimir_factura(dni_clt_act, hoy):

    with open("data/json/tabla_clientes.json", "r", encoding="UTF-8") as datos:
        clientes = json.load(datos)
        for c in clientes:
            if c["dni"] == dni_clt_act:
                cliente_act = c
    print(type(cliente_act))
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
    f'{"Nombre y Apellido: "+ cliente_act["nombre"]+" "+ cliente_act["apellido"]:<80}\n'\
    f'{"Dni: "+ str(cliente_act["dni"])}\n')

    print(f'{LINEA}\n|{"Nro. de reserva":^17}|{"Descripción":^19}|{"Precio por día":^18}|{"Días":^10}|{"Valor":^10}|\n{LINEA}')
    reservas_del_clt=[]
    total = 0

    with open("data/txt/tabla_reservas.txt", "r", encoding="UTF-8") as archivo:
        for linea in archivo:

            id_reserva, dni, check_in, check_out, hab, pax, total = linea.strip().split(";")
            if dni==str(dni_clt_act):
                reservas_del_clt.append([id_reserva, dni, check_in, check_out, hab, pax, total])
    archivo.close()

    total_sin_iva = 0
    for i in range(len(reservas_del_clt)):
        check_in= arreglar_fechas_archivo(reservas_del_clt[i][2])
        check_out = arreglar_fechas_archivo(reservas_del_clt[i][3])
        dias=diferencia_dias_entre(check_in,check_out)
        valor=int(reservas_del_clt[i][6])
        total_sin_iva = total_sin_iva + valor
        print(f'|{reservas_del_clt[i][0]:^17}|{"Habitación "+str(reservas_del_clt[i][4]):^19}|{reservas_del_clt[i][6]:^18}|{dias:^10}|{valor:^10}|')
    print(LINEA)
    iva_monto = float(total_sin_iva) * 0.21
    total_con_iva = float(total_sin_iva) + iva_monto
    print(f'{"Fecha de impresión: "+ str(formatear_fecha(hoy)):<40}{"Subtotal: "+str(total):>40}\n{"Total IVA: " + str(round(iva_monto, 2)):>80}\n{"Total: "+ str(round(total_con_iva, 2)):>80}\n')
