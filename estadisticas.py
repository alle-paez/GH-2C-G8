from reservas import *
from listas_codeadas import *
from habitaciones import *
from clientes import *


def opciones():
    print("")
    print(LINEA)
    print(f"Elija la opción deseada: \n\
        1 - Mostrar resumen global. \n\
        2 - Estadisticas de habitaciones. \n\
        3 - Estadisticas Mensuales. \n\
        4 - Resumen Maximos y minimos. \n\
        5 - Porcentajes de habitaciones. \n\
        ")
    
def elegir_opcion_estadistica(reservas=reservas):
    opciones()
    opcion = int(input(f"Seleccione una opción de las anteriores: (-1 para salir)\n"))
    while opcion < 1 or opcion > 5:
        print("Opcion no valida.")
        opcion = opcion = int(input(f"Seleccione una opción de las anteriores: (-1 para salir)\n"))
    while opcion != -1:
        if opcion == 1:
            globales = estadisticas_globales(reservas)
            mostrar_diccionario(globales)
        if opcion == 2:
            stat_hab = estadisticas_habitacion(reservas)
            mostrar_como_tabla(stat_hab)
        if opcion == 3:
            stats_mensual = estadisticas_mensuales(reservas)
            mostrar_como_tabla(stats_mensual)
        if opcion == 4:
            max_min_n = max_min_noches(reservas)
            max_min_t= max_min_totales(reservas)
            print("Maximos y minimos de categoria noches: ")
            mostrar_diccionario(max_min_n)
            print(f"{LINEA}\n\
            Máximos y minimos de categoria totales: \n ")
            mostrar_diccionario(max_min_t)
        if opcion == 5:
            porcentajes = porcentajes_reservas_x_habitacion(reservas)
            mostrar_diccionario(porcentajes)

        print("")
        print(LINEA)
        opciones()
        opcion = int(input(f"Seleccione una opción de las anteriores: (-1 para salir)\n"))

def mostrar_como_tabla(diccionario, titulo_clave ="Clave"):
    claves = list(diccionario.keys())
    primera = diccionario[claves[0]]
    campos = list(primera.keys())
    encabezado = titulo_clave.ljust(10) + " " + " ".join([c.ljust(12) for c in campos])
    print(encabezado)
    print("-"*len(encabezado))
    for clave, datos in diccionario.items():
        fila = str(clave).ljust(10) + " " + " ".join([str(datos[c]).ljust(12) for c in campos])
        print(fila)

    
def mostrar_diccionario(diccionario):
    for key in diccionario:
        print(f"{key}:{diccionario[key]}")



def aaaamm(fecha):
    return str(fecha[0]).zfill(4) + "-" + str(fecha[1]).zfill(2)

def estadisticas_globales(reservas):
    glob = {
        "total_reservas": 0,
        "noches_totales":0,
        "ingreso_total":0,
        "pax_total":0  }
    for res in reservas: 
        _, _, desde, hasta, _, pax, total = res
        glob["total_reservas"] += 1
        glob["noches_totales"] += diferencia_dias_entre(desde,hasta)
        glob["ingreso_total"] += total
        glob["pax_total"] += pax

        may = max(1, glob["total_reservas"])
        glob["estadia promedio"] = glob["noches_totales"] / may
        glob["Facturación promedio"] = glob["ingreso_total"] / may
        glob["pax_promedio"] = glob["pax_total"] / may
    return glob

def estadisticas_habitacion(reservas=reservas):
    estadistica_hab = {}
    for res in reservas:
        _, _, checkin, checkout, hab, pax, total = res
        if hab not in estadistica_hab:
            estadistica_hab[hab] = {"reservas":0,"noches":0,"ingresos":0,"pax":0}

        estadistica_hab[hab]["reservas"] += 1
        estadistica_hab[hab]["noches"]   += diferencia_dias_entre(checkin, checkout)
        estadistica_hab[hab]["ingresos"] += total
        estadistica_hab[hab]["pax"]      += pax

    for hab, stat in estadistica_hab.items():
        stat["Ingresos de la habitación"] = stat["ingresos"] / stat["noches"] if stat["noches"]>0 else 0
    return estadistica_hab

def  estadisticas_mensuales(reservas):
    stats_mensuales = {} 
    for res in reservas:
        _, _, checkin, checkout, _, pax, total = res
        mm = aaaamm(checkin)
        if mm not in stats_mensuales:
            stats_mensuales[mm] = {"reservas":0,"noches":0,"ingresos":0,"pax":0}

        stats_mensuales[mm]["reservas"] += 1
        stats_mensuales[mm]["noches"]   += diferencia_dias_entre(checkin, checkout)
        stats_mensuales[mm]["ingresos"] += total
        stats_mensuales[mm]["pax"]      += pax
    
    return stats_mensuales

def porcentajes_reservas_x_habitacion(reservas):
    conteo = {}
    total = len(reservas)
    for res in reservas:
        hab = res[4]
        conteo[hab] = conteo.get(hab, 0) + 1

    porcentajes = {}
    for hab, cant in conteo.items():
        porcentajes[hab] = (cant / total) * 100
    return porcentajes 


def max_min_noches(reservas):
    max_res = reservas[0]
    min_res = reservas[0]
    for res in reservas:
        noches_res = diferencia_dias_entre(res[2], res[3])
        if diferencia_dias_entre(max_res[2], max_res[3]) < noches_res:
            max_res = res
        if diferencia_dias_entre(min_res[2], min_res[3]) > noches_res:
            min_res = res
    return {"max noches":max_res, "min noches":min_res}

def max_min_totales(reservas):
    max_res = reservas[0]
    min_res = reservas[0]

    for res in reservas:
        if res[6]>max_res[6]:
            max_res = res
        if res[6]<min_res[6]:
            min_res = res

    return {"Pago total máximo":max_res,"Pago total minimo":min_res}



