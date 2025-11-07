from listas_codeadas import *
from clientes import *  
from habitaciones import *

import os

#print(total_por_precio(102, 18, 3))
#WRITELINE!!!!!!!!

#print(type(habitaciones))

#print(verificar_cant_max(102))
#print(validar_cant(4, 102))

#print(validar_cant(2, 102))

#llenar_reservas()

#print(comparar_fechas("2025-12-01", "2025-12-10"))
def bisiesto(anio):
    return((anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0))

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

def imprimir_factura(dni_clt_act, hoy):

    with open("tabla_clientes.json", "r", encoding="UTF-8") as datos:
        clientes = json.load(datos)
        for c in clientes:
            if c["Dni"] == dni_clt_act:
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
    total=0
    for i in range(len(reservas)):
        if reservas[i][1]==cliente_act["dni"]:
            reservas_del_clt.append(reservas[i])
    for i in range(len(reservas_del_clt)):
        dias=diferencia_dias_entre(check_in=reservas_del_clt[i][2],check_out=reservas_del_clt[i][3])
        valor=reservas_del_clt[i][6]*dias
        total+=valor
        print(f'|{reservas_del_clt[i][0]:^17}|{"Habitación "+str(reservas_del_clt[i][4]):^19}|{reservas_del_clt[i][6]:^18}|{dias:^10}|{valor:^10}|')
    print(LINEA)
    print(f'{"Fecha de impresión: "+ str(hoy):<40}{"Subtotal: "+str(total):>40}\n{"Total IVA: "+str(0.21*total):>80}\n{"Total: "+ str((IVA(total))):>80}\n')

    imprimir_factura(dni_clt_act=46751671, hoy="2025-08-25")