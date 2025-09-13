from listas_codeadas import *
from clientes import *
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
    return fecha  #Sale [año, mes, dia]

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
    patron = '^{0-9}{8}$'
    if re.match(patron, dni):
        return True
    else: 
        return False

def buscar_cliente(matriz_clientes, dni):
    existe = False
    for i in range(len(matriz_clientes)):
        if matriz_clientes[i][0] == dni:
            existe = True
        if not existe:
            print("El cliente ingresado no existe en nuestra base de datos. \n Por favor, ingrese los siguientes datos: ")
            llenar_clientes_desde_reservas(matriz_clientes, dni)
            existe = True

def llenar_clientes_desde_reservas(matriz_clientes, dni):
        nombre = input("Ingrese el nombre del cliente: ")
        apellido = input("Ingrese el apellido del cliente: ")
        telefono = input("Ingrese el telefono del cliente: ")
        mail = input("Ingrese el e-mail del cliente: ")
        matriz_clientes.append([dni,nombre,apellido,telefono,mail])
        print("Finalizo la carga, prosiguiendo con la reserva. ")

#VERIFICAR HABITACIÓN  ---------------------------------------------------------------------------------------
def _tupla(fecha):
    return tuple(fecha)

def verificar_reservas(matriz_reservas, check_in, check_out):
    pass

def total_por_precio(matriz_habitaciones, dto, dias):
    pos_hab = matriz_habitaciones.index(dto)
    total = matriz_habitaciones[pos_hab][1] * dias
    return total
        

#LLENAR RESERVAS ---------------------------------------------------------------------------------------------
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
        cant_pax = int(input("Ingrese la cantidad de pasajeros: "))

    #check-in y check-out -------------------------------------------
        check_in = pedir_fecha("Ingrese fecha inicio (AAAA-MM-DD): ")
        check_out = pedir_fecha("Ingrese fecha final (AAAA-MM-DD): ")
        while not verificar_egreso(check_in, check_out):
            print("El egreso debe ser posterior al ingreso.")
            check_out = pedir_fecha("Reingrese fecha fin (AAAA-MM-DD): ")

        dias = diferencia_dias_entre(check_in, check_out)
        if dias > 31:
            continuar = int(input("Cantidad de días mayor a 31, desea continuar? 1 - Si | 2 - No "))
            while continuar != 1 and continuar != 2: 
                print("Se debe ingresar 1 o 2.")
                continuar = int(input("Cantidad de días mayor a 31, desea continuar? 1 - Si | 2 - No "))
            if continuar == 1:
                pass
            if continuar == 2:
                pass 

#Total y habitación -------------------------------------------------------------
        total = total_por_precio(matriz_habitaciones)
        nro_reserva = len(matriz_reservas) + 1


def print_reservas(matriz):
    print("NroReserva|DNI       |Pax       |Desde     |Hasta     |Total     |")
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            #print(espaciado(10, matriz[i][j], "i"), end="")
            print(f'{matriz[i][j]}'.center(10," "), end='')
        print()
    return matriz


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
    
