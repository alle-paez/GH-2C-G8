from listas_codeadas import *
from clientes import *
from habitaciones import *
import re
import json

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

                    
def buscar_en_archivo():
    pass


def abrirArchivo(arch):
    try:
        contenido = open(arch, "rt", encoding="UTF-8")
        for linea in contenido:
            print(linea)
            #print(linea.strip()) # strip() elimina los caracteres de fin de línea (\n)
    except FileNotFoundError:
        print("Error, el archivo no existe")
    except OSError: # Incluye IOError y otros problemas del sistema operativo
        print("Error, no se pudo abrir el archivo")
    finally:
        try:
            contenido.close() # Siempre debe cerrarse
        except:
            print("Error al cerrar el archivo")

"""def leerArchivo(archivo, modo):
    try:
        arch = open(archivo, modo, encoding="UTF-8")
        linea = arch.readline()
        while linea:
            id_reserva, dni, check_in, check_out, hab, pax, total = linea.split(";").strip()
            linea = arch.readline() # Leemos la línea siguiente
    except OSError:
        print("No se pudo leer el archivo")
    finally:
        try:
            arch.close()
        except:
            print("No se pudo cerrar el archivo")
        
leerArchivo("reservas.txt","rt")"""
           
abrirArchivo("reservas.txt")
#Validaciones de fecha ----------------------------------------------------------------------------------------
def verificar_formato_fecha(fecha):
    formato = r"^\d{4}-\d{2}-\d{2}$"
    if re.match(formato, fecha):
        return True
    else:
        return False
        
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

def verificar_formato(dni):
    patron = r'^\d{8}$'
    if re.match(patron, dni):
        return True
    else: 
        return False

def existe_cliente(dni):
    clientes=leer_clientes()
    for c in clientes:
        if c["Dni"] == dni:
            return True
    return False

def buscar_cliente(dni):
    clientes=leer_clientes()
    if not existe_cliente(dni):
        print("El cliente ingresado no existe en nuestra base de datos. \n Por favor, ingrese los siguientes datos: ")
        llenar_clientes_desde_reservas(clientes, dni)
        
"""    if not existe_cliente(matriz_clientes, dni):
        print("El cliente ingresado no existe en nuestra base de datos. \n Por favor, ingrese los siguientes datos: ")
        llenar_clientes_desde_reservas(matriz_clientes, dni)"""
        
def llenar_clientes_desde_reservas(dni):
        nombre = input("Ingrese el nombre del cliente: ")
        apellido = input("Ingrese el apellido del cliente: ")
        telefono = input("Ingrese el telefono del cliente: ")
        mail = input("Ingrese el e-mail del cliente: ")
        archivo=leer_clientes()
        archivo.append(f'\"Dni\": {dni},\n\"Nombre\": {nombre}, \n\"Apellido\": {apellido}, \n\"Teléfono\": {telefono},\n\"Mail\": {mail}')
        json.dump(archivo, "tabla_clientes.json")
        print("Finalizo la carga, prosiguiendo con la reserva. ")

#VERIFICAR HABITACIÓN  ---------------------------------------------------------------------------------------
def comparar_fechas(fecha_1, fecha_2):
    return tuple(fecha_1) < tuple(fecha_2)

def coinciden_fechas(d1, h1, d2, h2):
    return comparar_fechas(d1, h2) and comparar_fechas(d2, h1)

def verificar_reservas_disponibilidad(archivo, nro_hab, check_in, check_out):
    try:
        contenido = open(archivo, "rt", encoding="UTF-8")
        linea = archivo.readline()
        es_hab=0
        while linea or es_hab==0:
            _, _, existente_desde, existente_hasta, hab, _, _ = linea.split(";").strip()
            
            if hab == nro_hab: 
                es_hab=1
                if coinciden_fechas(check_in, check_out, existente_desde, existente_hasta):
                    return False
            linea = archivo.readline()
        
        if es_hab==0:
            return True
    
    except FileNotFoundError:
        print("Error, no se pudo acceder a la base de datos.")

    finally:
        try:
            contenido.close() # Siempre debe cerrarse
        except:
            print("Error al cerrar el archivo")
    
def total_por_precio(dto, dias, ad):
    habitaciones=open("tabla_habitaciones.json", "r", encoding="utf-8")
    matriz_habitaciones = json.load(habitaciones)
    for hab in matriz_habitaciones:
        if hab == dto:
            precio_noche = hab["Precio"]
            return precio_noche * dias + ad * 4000

def verificar_cant_max(matriz_habitaciones, dto):
    habitaciones=open("tabla_habitaciones.json", "r", encoding="utf-8")
    matriz_habitaciones = json.load(habitaciones)
    for hab in matriz_habitaciones:
        if hab==dto:
            cant_maxima = hab["Capacidad"]
            return cant_maxima

def validar_cant(pax, matriz_habitaciones, dto):
    cap_max = verificar_cant_max(matriz_habitaciones,dto)
    pax = int(pax)
    if int(pax) <= cap_max:
        return True, 0
    elif pax <= cap_max + 2:
        ad = pax - cap_max
        return True, ad
    else: 
        return False

def digito_unico(pax):
    return pax.isdigit() and len(pax) == 1

#LLENAR RESERVAS: CREATE ---------------------------------------------------------------------------------------------
def llenar_reservas():

    reservas=open("tabla_reservas.txt", "rt", encoding="UTF-8")
    reservas_write=open("tabla_reservas.txt", "wt", encoding="UTF-8")

    habitaciones=open("tabla_habitaciones.json", "r", encoding="utf-8")
    dic_habitaciones = json.load(habitaciones)

    clientes=open("tabla_habitaciones.json", "r", encoding="utf-8")
    matriz_dic_clientes = json.load(clientes)

    nro_dni= input("Ingrese el número de dni del cliente: (-1 para salir): ")
    ver_dni = verificar_formato(nro_dni)
    while not ver_dni:
        print("Se ingreso un dni Invalido.")
        nro_dni= input("Ingrese el número de dni del cliente: (-1 para salir): ")
        ver_dni = verificar_formato(nro_dni)

    while int(nro_dni) != -1:
    #Validación ----------------------------------------------

        ver_dni = verificar_formato(nro_dni)
        while not ver_dni:
            print("Se ingreso un dni Invalido.")
            nro_dni= input("Ingrese el número de dni del cliente: (-1 para salir): ")
            ver_dni = verificar_formato(nro_dni)
        nro_dni = int(nro_dni)

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
        
        dto = int(input("Ingrese el numero de habitación: "))
        while not verificar_reservas_disponibilidad("tabla_reservas.txt", dto, check_in, check_out):
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

        reservas_write.write((f'{nro_reserva}, {nro_dni}, {check_in}, {check_out}, {dto}, {cant_pax}, {total}'))
        print(f"{nro_reserva, nro_dni, check_in, check_out, dto, cant_pax, total}")
        print("Se agrego todo correctamente.")
        nro_dni= input("Ingrese el número de dni del cliente: (-1 para salir): ")

    reservas.close()
    reservas_write.close()

#UPDATE: ACTUALIZAR Y LEER ----------------------------------------------------------------------------------
def buscar_reserva_x_id(idd):
    reservas=open("tabla_reservas.txt", "rt", encoding="UTF-8")
    linea=reservas.readline()
    
    while linea:
        id, _, existente_desde, existente_hasta, hab, _, _ = linea.split(";").strip()
        if id == idd:
            return True
        linea=reservas.readline()
    return -1

def dar_reserva_x_id(matriz_reservas, idd):
    i = buscar_reserva_x_id(matriz_reservas, idd)
    if i == -1:
        return False
    else: 
        return matriz_reservas[i]


def mostrar_opciones_mod():
    print(f"¿Que elemento/s de la reserva desea modificar?:\n \
(El id, dni del cliente y el total de la reserva no son posibles de modificar.) \n \
    Fechas de entrada y salida: 1 \n \
    Número de habitación: 2 \n \
    Cantidad de pasajeros: 3")

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
          formatear_fecha(check_in).ljust(11), "|",
          formatear_fecha(check_out).ljust(11), "|",
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

def mostrar_reservas(matriz, hab, x):
    return [res for res in matriz if res[x] == hab]

def ordenar_menor_mayor(reservas, i):
    reservas.sort(key=lambda x: x[i])
    return reservas

def ordenar_totales_mayor_menor(reservas):
    reservas.sort(key=lambda x: x[6], reverse=True)
    return reservas

def print_elegir_opcion(matriz_reservas= reservas):
    menu_mostrar()
    op = int(input("Ingrese la opción elegida:"))
    if op == 1:
        print_tabla_reservas("reservas.txt")
    elif op == 2:
        cliente = input("Ingrese el DNI del cliente: ")
        ver_dni = verificar_formato(cliente)
        while not ver_dni:
            print("Se ingreso un dni Invalido.")
            cliente= input("Ingrese el número de dni del cliente: (-1 para salir): ")
            ver_dni = verificar_formato(cliente)
        cliente = int(cliente)
        reservas_cliente = mostrar_reservas(matriz_reservas,cliente,1)
        if len(reservas_cliente)==0:
            print(f"El Dni {cliente} no tiene ninguna reserva en el alojamiento.")
        else: 
            print_tabla_reservas(reservas_cliente)
    elif op == 3:
        print("Elija el numero de habitación: ")
        print_habitaciones()
        hab = int(input("Habitación elegida: "))
        reservas_habitacion = mostrar_reservas(matriz_reservas, hab, 4)
        print_tabla_reservas(reservas_habitacion)
    elif op == 4:
        ordenar_totales_mayor_menor(matriz_reservas)
        print_tabla_reservas(matriz_reservas)
    elif op == 5:
        ordenar_menor_mayor(matriz_reservas, 6)
        print_tabla_reservas("reservas.txt")
    elif op==6:
        ordenar_menor_mayor(matriz_reservas, 2)
        print_tabla_reservas("reservas.txt")

"""
def print_tabla_reservas(matriz):
    print("")
    print("------------------------------------------------------------------")
    print("ID   | DNI Cliente | Entrada     | Salida      | Hab | Pax | Total")
    print("------------------------------------------------------------------")
    for valor in matriz:
        fila = valor
        id_reserva, dni, check_in, check_out, hab, pax, total = fila
        print(str(id_reserva).ljust(4), "|",
          str(dni).ljust(11), "|",
          formatear_fecha(check_in).ljust(11), "|",
          formatear_fecha(check_out).ljust(11), "|",
          str(hab).ljust(3), "|",
          str(pax).ljust(3), "|",
          str(total).ljust(6))"""


def print_tabla_reservas(archivo):
    try:
        arch = open(archivo, "rt", encoding="UTF-8")
        linea = arch.readline()
        print("")
        print("------------------------------------------------------------------")
        print("ID   | DNI Cliente | Entrada     | Salida      | Hab | Pax | Total")
        print("------------------------------------------------------------------")
        while linea:
            id_reserva, dni, check_in, check_out, hab, pax, total = linea.split(";").strip()
            print(str(id_reserva).ljust(4), "|",
            str(dni).ljust(11), "|",
            formatear_fecha(check_in).ljust(11), "|",
            formatear_fecha(check_out).ljust(11), "|",
            str(hab).ljust(3), "|",
            str(pax).ljust(3), "|",
            str(total).ljust(6))

            linea = arch.readline() # Leemos la línea siguiente
    except OSError:
        print("No se pudo leer el archivo")
    finally:
        try:
            arch.close()
        except:
            print("No se pudo cerrar el archivo")
        


#MODIFICACION --------------------------------------------------------------------------------------------------------------
def modificacion(matriz_clientes=clientes, matriz_reservas= reservas, matriz_habitaciones=habitaciones, mat_mod_anterior= reservas_ant_mod, mat_mod_posterior= reservas_post_mod):
    busq = modo_busqueda()
    while busq != 1 and busq != 2:
        busq = modo_busqueda()
    if busq == 1: 
        id_reserva = int(input("Ingrese el id de reserva: "))
        existe = dar_reserva_x_id(matriz_reservas, id_reserva)
        while not existe:
            id_reserva = int(input("Ingrese el id de reserva: "))
            existe = dar_reserva_x_id(matriz_reservas, id_reserva)  
              
        i = buscar_reserva_x_id(matriz_reservas, id_reserva)

    elif busq == 2:
        nro_dni= input("Ingrese el número de dni del cliente: (-1 para salir): ")
        ver_dni = verificar_formato(nro_dni)
        existe = existe_cliente(matriz_clientes, int(nro_dni))
        reservas_cliente = mostrar_reservas(matriz_reservas, int(nro_dni), 1)
        while not ver_dni or not existe or reservas_cliente == 0:
            if not ver_dni: 
                print("Se ingreso un dni Invalido.")
            elif not existe:
                print(" El cliente no existe en la base de datos.")
            elif len(reservas_cliente) == 0:
                print(" El cliente no tiene reservas registradas.")

            nro_dni= input("Ingrese el número de dni del cliente: (-1 para salir): ")
            ver_dni = verificar_formato(nro_dni)
            existe = existe_cliente(matriz_clientes, int(nro_dni))


        print(f" ID | DNI Cliente | Entrada | Salida | Habitación | Pax | Total")
        for el in reservas_cliente:
            print(el, end=" ") 
            print("")   

        print("Se mostraron las reservas del cliente junto a su id, por favor elija una opción: ")
        id_reserva = int(input("Ingrese el id de reserva: "))
        existe = dar_reserva_x_id(matriz_reservas, id_reserva)
        while not existe:
            id_reserva = int(input("Ingrese el id de reserva: "))
            existe = dar_reserva_x_id(matriz_reservas, id_reserva)  
              
        i = buscar_reserva_x_id(matriz_reservas, id_reserva)


    mostrar_opciones_mod()
    opcion_elegida = int(input("Ingrese la opción elegida: (-1 para retroceder.)"))
    while opcion_elegida != -1:

#FECHAS ----------------------------------------------------------------------       
        if opcion_elegida == 1:
            check_in = pedir_fecha("Ingrese fecha inicio (AAAA-MM-DD): ")
            check_out = pedir_fecha("Ingrese fecha final (AAAA-MM-DD): ")
            modificados_reservas = matriz_reservas.pop(i)

            while not verificar_egreso(check_in, check_out):
                print("El egreso debe ser posterior al ingreso.")
                check_out = pedir_fecha("Reingrese fecha fin (AAAA-MM-DD): ")
            
            dias = diferencia_dias_entre(check_in, check_out)

            dto = modificados_reservas[4]
            while not verificar_reservas_disponibilidad(matriz_reservas, dto, check_in, check_out):
                print(f"La habitación {dto} ya está ocupada en ese rango.")
                dto = int(input("Ingrese el numero de habitación: "))
            
            cant_pax = modificados_reservas[5]
            valido, adicionales = validar_cant(cant_pax, matriz_habitaciones, dto)
            while not valido:
                print("Exceso de pasajeros.")
                cant_pax = int(input("Ingrese la cantidad de pasajeros: "))
                while not digito_unico(cant_pax):
                    cant_pax = int(input("Ingrese la cantidad de pasajeros: "))    
                valido, adicionales = validar_cant(cant_pax, matriz_habitaciones, dto)

            total = total_por_precio(matriz_habitaciones, dto, dias, adicionales)
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
            while not verificar_reservas_disponibilidad(matriz_reservas, dto, check_in, check_out):
                print(f"La habitación {dto} ya está ocupada en ese rango.")
                dto = int(input("Ingrese el numero de habitación: "))
            
            cant_pax = modificados_reservas[5]
            valido, adicionales = validar_cant(cant_pax, matriz_habitaciones, dto)
            while not valido:
                print("Exceso de pasajeros.")
                cant_pax = int(input("Ingrese la cantidad de pasajeros: "))
                while not digito_unico(cant_pax):
                    cant_pax = int(input("Ingrese la cantidad de pasajeros: "))    
                valido, adicionales = validar_cant(cant_pax, matriz_habitaciones, dto)
            
            total = total_por_precio(matriz_habitaciones, dto, dias, adicionales)
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
            valido, adicionales = validar_cant(cant_pax, matriz_habitaciones, dto)
            while not valido:
                print("Exceso de pasajeros.")
                cant_pax = int(input("Ingrese la cantidad de pasajeros: "))
                while not digito_unico(cant_pax):
                    cant_pax = int(input("Ingrese la cantidad de pasajeros: "))    
                valido, adicionales = validar_cant(cant_pax, matriz_habitaciones, dto)

            total = total_por_precio(matriz_habitaciones, dto, dias, adicionales)
            modif = [modificados_reservas[0], modificados_reservas[1], check_in, check_out, dto, cant_pax, total]
            mat_mod_anterior.append(modificados_reservas.pop())
            mat_mod_posterior.append(modif)
            matriz_reservas.insert(i, modif)
            
            print_reserva(matriz_reservas, i)

        opcion_elegida = int(input("Ingrese la opción elegida: (-1 para retroceder.)"))

#DELETE: BORRAR --------------------------------------------------------------------------------------
def eliminar_reserva(matriz_reservas=reservas, reservas_eliminadas=reservas_eliminadas):
    id_eliminar = int(input("Ingrese el número de reserva que quiera eliminar: "))
    flag = 1
    while flag == 1:
        flag = 0
        pos = buscar_reserva_x_id(matriz_reservas, id_eliminar)
        if pos != -1:
            reserva = matriz_reservas.pop(pos)
            reservas_eliminadas.append(reserva)
            print(f"La reserva nro {id_eliminar} ha sido eliminada con exito.")
            flag = int(input("Si desea eliminar otra habitación, ingrese 1, si no, ingrese 0: "))
        else: 
            print(f"No se encontro la habitación {id_eliminar}.")
            id_eliminar = int(input("Ingrese el número de reserva nuevamente: "))

        if flag == 1:
            id_eliminar = int(input("Ingrese el número de reserva que quiera eliminar: "))

def deshacer_eliminar_reserva(matriz_reservas=reservas, reservas_eliminadas=reservas_eliminadas):
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
            id_recuperar = int(input("Ingrese el número de reserva que quiera recuperar: "))

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
    f'{"Nombre y Apellido: "+ clientes[clt_act][1]+" "+ clientes[clt_act][2]:<80}\n'\
    f'{"Dni: "+ str(clientes[clt_act][0])}\n')

    print(f'{LINEA}\n|{"Nro. de reserva":^17}|{"Descripción":^19}|{"Precio por día":^18}|{"Días":^10}|{"Valor":^10}|\n{LINEA}')
    reservas_del_clt=[]
    total=0
    for i in range(len(reservas)):
        if reservas[i][1]==clientes[clt_act][0]:
            reservas_del_clt.append(reservas[i])
    for i in range(len(reservas_del_clt)):
        dias=diferencia_dias_entre(check_in=reservas_del_clt[i][2],check_out=reservas_del_clt[i][3])
        valor=reservas_del_clt[i][6]*dias
        total+=valor
        print(f'|{reservas_del_clt[i][0]:^17}|{"Habitación "+str(reservas_del_clt[i][4]):^19}|{reservas_del_clt[i][6]:^18}|{dias:^10}|{valor:^10}|')
    print(LINEA)
    print(f'{"Fecha de impresión: "+ str(hoy):<40}{"Subtotal: "+str(total):>40}\n{"Total IVA: "+str(0.21*total):>80}\n{"Total: "+ str((IVA(total))):>80}\n')
#f'{pi:.2f}'

