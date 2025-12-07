from reservas import *
from listas_codeadas import *
from habitaciones import *
from clientes import *
from functools import reduce

def _leer_reservas_lista_desde_txt(ruta="tabla_reservas.txt"):
    lista = []
    try:
        f = open(ruta, "r", encoding="UTF-8")
        linea = f.readline()

        while linea != "":
            linea = linea.strip()
            if linea != "":
                partes = linea.split(";")

                if len(partes) >= 7:
                    try:
                        id_reserva = int(partes[0])
                        dni = int(partes[1])
                        check_in = partes[2]
                        check_out = partes[3]
                        
                        hab = int(partes[4])
                        pax = int(partes[5])

                        try:
                            total = float(partes[6])
                        except:
                            total = int(partes[6])

                        lista.append([id_reserva, dni, check_in, check_out, hab, pax, total])
                    except Exception as e:
                        print(f"Error! {e}")

            linea = f.readline()

        f.close()
    except FileNotFoundError:
        print("No se encontró el archivo de reservas.")
    except OSError:
        print("Error al abrir el archivo de reservas.")

    return lista

def pasar_fecha(fecha):
    anio, mes, dia = arreglar_fechas_archivo(fecha)
    return f"{anio}-{mes}-{dia}"

def es_tupla(fecha):
    if type(fecha) == tuple:
        return fecha
    s = str(fecha).replace("(", "").replace(")", "")
    partes = s.split(",")
    if len(partes) == 3:
        try:
            return (int(partes[0]), int(partes[1]), int(partes[2]))
        except:
            return fecha
    return fecha


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
    opcion = int(input(f"Seleccione una opción de las anteriores: (-1 para salir): "))
    while opcion != -1 and (opcion < 1 or opcion > 5):
        print("Opcion no valida.")
        opcion = int(input(f"Seleccione una opción de las anteriores: (-1 para salir): "))
    while opcion != -1:
        datos = _leer_reservas_lista_desde_txt()
        if opcion == 1:
            estadisticas_globales(datos)
        if opcion == 2:
            stat_hab = estadisticas_habitacion(datos)
            mostrar_como_tabla(stat_hab)
        if opcion == 3:
            stats_mensual = estadisticas_mensuales(datos)
            mostrar_como_tabla(stats_mensual)
        if opcion == 4:
            max_min_n = max_min_noches(datos)
            max_min_t= max_min_totales(datos)
            print("Maximos y minimos de categoria noches: ")
            mostrar_diccionario_reservas(max_min_n)
            print(f"{LINEA}\n\
Máximos y minimos de categoria totales: \n ")
            mostrar_diccionario_reservas(max_min_t)
        if opcion == 5:
            porcentajes_reservas_x_habitacion(datos)
            

        print("")
        print(LINEA)
        opciones()
        opcion = int(input(f"Seleccione una opción de las anteriores: (-1 para salir): "))

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

    
def mostrar_diccionario_reservas(diccionario):
    print("------------------------------------------------------------------")
    print(f"{"":<5}|{"ID":<3}|{"DNI Cliente":<15}|{"Entrada":<10}|{"Salida":<10}|{"Hab":<5}|{"Pax":<4}|{"Total":<8}")
    print("------------------------------------------------------------------")
    for key in diccionario:
        check_in = diccionario[key][2]
        check_in = pasar_fecha(check_in)
        check_out = diccionario[key][3]
        check_out = pasar_fecha(check_out)
        print(f"{key:<5}|{diccionario[key][0]:<3}|{str(diccionario[key][1]).center(15)}|{check_in:<10}|{check_out:<10}|{diccionario[key][4]:<5}|{diccionario[key][5]:<4}|{diccionario[key][6]:<8}")

def aaaa_mm(fecha):
    t = es_tupla(fecha)
    return str(t[0]).zfill(4) + "-" + str(t[1]).zfill(2)

def estadisticas_globales(reservas):
    if type(reservas) != list:
        reservas = _leer_reservas_lista_desde_txt()
    glob = {
        "total_reservas": 0,
        "noches_totales":0,
        "ingreso_total":0,
        "pax_total":0  }
    for res in reservas: 
        _, _, desde, hasta, _, pax, total = res
        d = es_tupla(desde)
        h = es_tupla(hasta)        
        glob["total_reservas"] += 1
        glob["noches_totales"] += diferencia_dias_entre(d,h)
        glob["ingreso_total"] += total
        glob["pax_total"] += pax

        may = max(1, glob["total_reservas"])
        glob["estadia promedio"] = glob["noches_totales"] / may
        glob["Facturación promedio"] = glob["ingreso_total"] / may
        glob["pax_promedio"] = glob["pax_total"] / may

    print(f"Reservas Totales: {glob["total_reservas"]}")
    print(f"Noches Totales: {glob["noches_totales"]}")
    print(f"Ingresos Totales: {glob["ingreso_total"]}")
    print(f"Pasajeros Totales: {glob['pax_total']}")

def estadisticas_habitacion(reservas_lista):
    if type(reservas_lista) != list:
        reservas_list = _leer_reservas_lista_desde_txt()    
    estadistica_hab = {}
    for res in reservas_lista:
        checkin, checkout, hab, pax, total = res[2:7]
        ci = es_tupla(checkin)
        co = es_tupla(checkout)        
        if hab not in estadistica_hab:
            estadistica_hab[hab] = {"reservas":0,"noches":0,"ingresos":[],"pax":0}

        estadistica_hab[hab]["reservas"] += 1
        estadistica_hab[hab]["noches"]   += diferencia_dias_entre(ci, co)
        estadistica_hab[hab]["ingresos"].append(total) 
        estadistica_hab[hab]["pax"]      += pax

    for hab, stat in estadistica_hab.items():
        stat["ingresos"] = round(reduce(lambda acc, x: acc + x, stat["ingresos"], 0),2)
        stat["Ingresos de la habitación"] = round((stat["ingresos"] / stat["noches"] if stat["noches"]>0 else 0),2)
    return estadistica_hab

def  estadisticas_mensuales(reservas):
    stats_mensuales = {} 
    for res in reservas:
        _, _, checkin, checkout, _, pax, total = res
        ci = es_tupla(checkin)
        co = es_tupla(checkout)        
        mm = aaaa_mm(ci)
        if mm not in stats_mensuales:
            stats_mensuales[mm] = {"reservas":0,"noches":0,"ingresos":0,"pax":0}

        stats_mensuales[mm]["reservas"] += 1
        stats_mensuales[mm]["noches"]   += diferencia_dias_entre(ci, co)
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
    print(f"{"Hab":<5} | {"Porcentaje"}")
    print(f"{"-":<20}")
    for hab, cant in conteo.items():
        porcentajes[hab] = (cant / total) * 100
        print(f"{hab:<5} | {round(porcentajes[hab],2)}% ")
    


def max_min_noches(reservas):
    if len(reservas) == 0:
        return {"max noches": None, "min noches": None}
    max_res = reservas[0]
    min_res = reservas[0]
    for res in reservas:
        ci = es_tupla(res[2]); co = es_tupla(res[3])
        noches_res = diferencia_dias_entre(ci, co)

        m_ci = es_tupla(max_res[2]); m_co = es_tupla(max_res[3])
        n_ci = es_tupla(min_res[2]); n_co = es_tupla(min_res[3])

        if diferencia_dias_entre(m_ci, m_co) < noches_res:
            max_res = res
        if diferencia_dias_entre(n_ci, n_co) > noches_res:
            min_res = res
    return {"max":max_res, "min":min_res}

def max_min_totales(reservas):
    max_res = reservas[0]
    min_res = reservas[0]

    for res in reservas:
        if res[6]>max_res[6]:
            max_res = res
        if res[6]<min_res[6]:
            min_res = res

    return {"max":max_res,"min":min_res}



