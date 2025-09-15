from listas_codeadas import *
from clientes import *
from habitaciones import *
import re

"""Lista para hacer: 

reservas = [
reservas = [
    [1, 30555999, [2025,8,15], [2025,8,20], 101, 2, 75000],
    [2, 28444888, [2025,8,18], [2025,8,25], 102, 3, 126000],
    [3, 33222111, [2025,9,1],  [2025,9,5],  103, 2, 72000],
    [4, 29888777, [2025,8,10], [2025,8,15], 104, 4, 106250],
    [5, 31222333, [2025,8,22], [2025,8,24], 105, 1, 22800]
]
    - Validar si existe el cliente, si no, crearlo.
    - Validar si la habitacion solicitada no esta ocupada en la fecha seleccionada.
    - falta el precio por noche, tiene que estar cargado en la lista habitaciones. 
    - Reordenar reservas. 
    - verificacion de cantidad de pasajeros. Se pueden 2 mas maximo de la capacidad de la habitacion, con adicional. 
    - verificar en la tabla reservas que no exista otra reserva para la fecha ingresada en el dto engresado. 
    
     """

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

def existe_cliente(matriz_clientes, dni):
    for c in matriz_clientes:
        if c[0] == dni:
            return True
    return False

def buscar_cliente(matriz_clientes, dni):
    if not existe_cliente(matriz_clientes, dni):
        print("El cliente ingresado no existe en nuestra base de datos. \n Por favor, ingrese los siguientes datos: ")
        llenar_clientes_desde_reservas(matriz_clientes, dni)
        
"""    if not existe_cliente(matriz_clientes, dni):
        print("El cliente ingresado no existe en nuestra base de datos. \n Por favor, ingrese los siguientes datos: ")
        llenar_clientes_desde_reservas(matriz_clientes, dni)"""
        
def llenar_clientes_desde_reservas(matriz_clientes, dni):
        nombre = input("Ingrese el nombre del cliente: ")
        apellido = input("Ingrese el apellido del cliente: ")
        telefono = input("Ingrese el telefono del cliente: ")
        mail = input("Ingrese el e-mail del cliente: ")
        matriz_clientes.append([dni,nombre,apellido,telefono,mail])
        print("Finalizo la carga, prosiguiendo con la reserva. ")

#VERIFICAR HABITACIÓN  ---------------------------------------------------------------------------------------
def comparar_fechas(fecha_1, fecha_2):
    return tuple(fecha_1) < tuple(fecha_2)

def coinciden_fechas(d1, h1, d2, h2):
    return comparar_fechas(d1, h2) and comparar_fechas(d2, h1)

def verificar_reservas_disponibilidad(matriz_reservas,nro_hab, check_in, check_out):
    for reserva in matriz_reservas:
        _, _, existente_desde, existente_hasta, hab, _, _ = reserva
        if hab == nro_hab and coinciden_fechas(check_in, check_out, existente_desde, existente_hasta):
            return False
    return True
    
def total_por_precio(matriz_habitaciones, dto, dias, ad):
 for hab in matriz_habitaciones:
     if hab[0] == dto:
         precio_noche = hab[1]
         return precio_noche * dias + ad * 4000

def verificar_cant_max(matriz_habitaciones, dto):
    for hab in matriz_habitaciones:
        if hab[0]==dto:
            cant_maxima = hab[3]
            return cant_maxima

def validar_cant(pax, matriz_habitaciones, dto):
    cap_max = verificar_cant_max(matriz_habitaciones,dto)
    pax = int(pax)
    if pax <= cap_max:
        return True, 0
    elif pax <= cap_max + 2:
        ad = pax - cap_max
        return True, ad
    else: 
        return False

def digito_unico(pax):
    return pax.isdigit() and len(pax) == 1

#LLENAR RESERVAS: CREATE ---------------------------------------------------------------------------------------------
def llenar_reservas(matriz_reservas= reservas, matriz_clientes= clientes, matriz_habitaciones= habitaciones):
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
        buscar_cliente(matriz_clientes, nro_dni)

    #check-in y check-out -------------------------------------------
        check_in = pedir_fecha("Ingrese fecha inicio (AAAA-MM-DD): ")
        check_out = pedir_fecha("Ingrese fecha final (AAAA-MM-DD): ")
        while not verificar_egreso(check_in, check_out):
            print("El egreso debe ser posterior al ingreso.")
            check_out = pedir_fecha("Reingrese fecha fin (AAAA-MM-DD): ")

        dias = diferencia_dias_entre(check_in, check_out)
#Validar habitaciones y fechas --------------------------------------------------
        
        dto = int(input("Ingrese el numero de habitación: "))
        while not verificar_reservas_disponibilidad(matriz_reservas, dto, check_in, check_out):
            print(f"La habitación {dto} ya está ocupada en ese rango.")
            dto = int(input("Ingrese el numero de habitación: "))

#Total y habitación -------------------------------------------------------------
        cant_pax = input("Ingrese la cantidad de pasajeros: ")
        while not digito_unico(cant_pax):
            cant_pax = int(input("Ingrese la cantidad de pasajeros: "))

        valido, adicionales = validar_cant(cant_pax, matriz_habitaciones, dto)
        while not valido:
            print("Exceso de pasajeros.")
            cant_pax = int(input("Ingrese la cantidad de pasajeros: "))
            while not digito_unico(cant_pax):
                cant_pax = int(input("Ingrese la cantidad de pasajeros: "))    
            valido, adicionales = validar_cant(cant_pax, matriz_habitaciones, dto)

        total = total_por_precio(matriz_habitaciones, dto, dias, adicionales)
        nro_reserva = len(matriz_reservas) + 1

        matriz_reservas.append([nro_reserva, nro_dni, check_in, check_out, dto, int(cant_pax), total])
        print(f"{nro_reserva, nro_dni, check_in, check_out, dto, cant_pax, total}")
        print("Se agrego todo correctamente.")
        nro_dni= input("Ingrese el número de dni del cliente: (-1 para salir): ")

#UPDATE: ACTUALIZAR Y LEER ----------------------------------------------------------------------------------
def buscar_reserva_x_id(matriz_reservas, idd):
    for i in range(len(matriz_reservas)):
        if matriz_reservas[i][0] == idd:
            return i
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
        print_tabla_reservas(matriz_reservas)
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
        print_habitaciones(habitaciones)
        hab = int(input("Habitación elegida: "))
        reservas_habitacion = mostrar_reservas(matriz_reservas, hab, 4)
        print_tabla_reservas(reservas_habitacion)
    elif op == 4:
        ordenar_totales_mayor_menor(matriz_reservas)
        print_tabla_reservas(matriz_reservas)
    elif op == 5:
        ordenar_menor_mayor(matriz_reservas, 6)
        print_tabla_reservas(matriz_reservas)
    elif op==6:
        ordenar_menor_mayor(matriz_reservas, 2)
        print_tabla_reservas(matriz_reservas)




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
          str(total).ljust(6))




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





#FACTURA    
def imprimir_factura():
    #ENCABEZADO
    linea=("-")*80
    factura=(f'{str(nro_factura[0]).zfill(4)}-{str(nro_factura[1]).zfill(8)}'.ljust(40))
    print(f'{linea}\n{empresa['nombre'].capitalize().ljust(80)}\n{linea}\nFactura: {factura}\n\
Domicilio fiscal: {empresa['dirección'].capitalize().ljust(40)}    CUIT:{empresa['cuit'].rjust(10)} \n\
Web: {empresa['web'].ljust(80)}\nPeríodo: 2025-08\n\
Soporte: {empresa['email']}')
    print (f'{linea}\n')
    nro_factura[0]+=1
    nro_factura[1]+=1
    #CUERPO
    #print(f'Total: {IVA(total_por_precio())}'.ljust(80))
    
