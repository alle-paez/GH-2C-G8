from listas_codeadas import *
from clientes import *  
from habitaciones import *
from reservas import *
import os

#print(total_por_precio(102, 18, 3))
#WRITELINE!!!!!!!!

#print(type(habitaciones))

#print(verificar_cant_max(102))
#print(validar_cant(4, 102))

#print(validar_cant(2, 102))

#llenar_reservas()

#print(comparar_fechas("2025-12-01", "2025-12-10"))

def modificacion():
    busq = modo_busqueda()
    idd= None
    while busq != 1 and busq != 2:
        busq = modo_busqueda()
    if busq == 1: 
        id_reserva = int(input("Ingrese el id de reserva: "))
        existe = buscar_reserva_x_id(id_reserva)
        while not existe:
            id_reserva = int(input("Ingrese el id de reserva: "))
            existe = buscar_reserva_x_id(id_reserva)  
              
    elif busq == 2:
        while True:
            try:
                nro_dni= input("Ingrese el número de dni del cliente: (-1 para salir): ")
                assert verificar_formato(nro_dni)== True
                assert existe_cliente(int(nro_dni)) == True
                break
            except AssertionError as dni:
                print("Se ingreso un dni Invalido.")
            except AssertionError:
                print(" El cliente no existe en la base de datos.")
           
        mostrar_reservas_por_hab_o_clt(int(nro_dni), x=1)
            
        print("Se mostraron las reservas del cliente junto a su id, por favor elija una opción: ")
        id_reserva = int(input("Ingrese el id de reserva: "))

        existe = buscar_reserva_x_id(id_reserva)
        while not existe:
            id_reserva = int(input("Ingrese el id de reserva: "))
            existe = buscar_reserva_x_id(id_reserva)  
              
    with open("tabla_reservas.txt", "r", encoding="UTF-8") as archivo:
        linea=archivo.readline()
        aux=open("temp.txt", "w", encoding="UTF-8")
        encontrado=False
        for linea in archivo:
            idd, dni, check_in, check_out, hab, pax, _ = linea.strip().split(";")

            while linea:
                if str(id_reserva)!=idd:
                    aux.write(linea)
                    linea = archivo.readline()
                    idd, dni, check_in, check_out, hab, pax, _ = linea.strip().split(";")
                else:
                    encontrado=True
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
                                check_in_nuevo = tuple(check_in)
                            break
                        except AssertionError:
                            print("El formato ingresado es inválido.")
                    while True:
                        try:
                            check_out_nuevo = pedir_fecha_mod(f"Ingrese nueva fecha de check-out ({check_out}) AAAA-MM-DD: ")
                            if check_out_nuevo == "":
                                check_out_nuevo = tuple(check_out)
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
                                    print(f"La habitación {dto} ya está ocupada en ese rango.")
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
                            else:
                                valido, adicionales = validar_cant(int(cant_pax_nuevo), int(dto_nuevo))
                                assert valido == True
                            break
                        except AssertionError:
                            print("Exceso de pasajeros para la habitación seleccionada.")
                    dias = diferencia_dias_entre(check_in_nuevo, check_out_nuevo)
                    total_nuevo = total_por_precio(int(dto_nuevo), dias, adicionales)

                    nueva_linea=(f'{idd};{dni_nuevo};{check_in_nuevo};{check_out_nuevo};{dto_nuevo};{cant_pax_nuevo};{total_nuevo}\n')
                    aux.write(nueva_linea)
                    linea = archivo.readline()
    aux.close()
    archivo.close()

    if encontrado:
        try:
            os.remove("tabla_reservas.txt")       # elimina el original
            os.rename("temp.txt", "tabla_reservas.txt") # renombra el temporal
            print(f"La reserva {idd} ha sido correctamente.")
        except OSError as error:
            print("Error al reemplazar el archivo:", error)
    else:
        os.remove("temp.txt")  # eliminamos el temporal si no se usó
        print(f"No se encontró la reserva {idd}.")
        

modificacion()
