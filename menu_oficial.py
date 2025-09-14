from listas_codeadas import *
from clientes import *
from habitaciones import *
from reservas import *
from opcion_habitaciones import *

def menu_administrador():

    print("")
    print(f'Sistema de Gestión Hotelera'.center(80,"-"))
    print(f'\n\
1-Gestionar Habitaciones\n\
2-Gestionar Reservas\n\
3-Gestionar Clientes\n\
Salir del programa con -1 \n\
{LINEA}')
    opcion=int(input("Ingrese numéricamente la opción deseada: "))

    while opcion!=-1:
        if opcion==1:
            print(f'{LINEA}\n\
1-Agregar habitación\n\
2-Modificar habitación\n\
3-Borrar habitación\n\
4-Ver habitaciones\n\
5-Papelera de reciclaje\n\
Volver para atrás con -1 \n\
{LINEA}')
            opcion_habitaciones=int(input("Ingrese numéricamente la opción deseada: "))

            while opcion_habitaciones!=-1:
                if opcion_habitaciones==1:#AGREGAR HABITACIONES
                    llenar_habitaciones(habitaciones)
                    #AGREGAR CHECKEOS
                elif opcion_habitaciones==2: #MODIFICAR HABITACIONES
                    modificar_habitacion(habitaciones)
                elif opcion_habitaciones==3: #ELIMINAR HABITACIONES
                    print_habitaciones(habitaciones)
                    eliminar_hab(habitaciones, habitaciones_borradas)
                elif opcion_habitaciones==4:#VER HABITACIONES
                    print_habitaciones(habitaciones)
                
                print(f'{LINEA}\n\
1-Agregar habitación\n\
2-Modificar habitación\n\
3-Borrar habitación\n\
4-Ver habitaciones\n\
5-Papelera de reciclaje\n\
Volver para atrás con -1\n\
{LINEA}')
                opcion_habitaciones=int(input("Ingrese numéricamente la opción deseada: "))

        elif opcion==2:
            print(f'\
1-Agregar reserva\n\
2-Modificar reserva\n\
3-Cancelar reserva\n\
4-Ver reservas\n\
5-Papelera de reciclaje\n\
Volver para atrás con -1')
            opcion_reservas=int(input("Ingrese numéricamente la opción deseada: "))

            while opcion_reservas!=-1:

                if opcion_reservas==1: #AGREGAR RESERVA
                    llenar_reservas()
                elif opcion_reservas==2: #MODIFICAR RESERVA
                    modificacion()
                elif opcion_reservas==3: # CANCELAR RESERVA
                    pass
                elif opcion_reservas==4: #VER RESERVAS
                    print_reservas(reservas)

                print(f'{LINEA}\n\
1-Agregar reserva\n\
2-Modificar reserva\n\
3-Cancelar reserva\n\
4-Ver reservas\n\
5-Papelera de reciclaje\n\
Volver para atrás con -1\n\
    {LINEA}')
                opcion_reservas=int(input("Ingrese numéricamente la opción deseada: "))
        elif opcion==3:
            print(f'{LINEA}\n\
1-Agregar cliente\n\
2-Modificar cliente\n\
3-Eliminar cliente\n\
4-Ver clientes\n\
5-Papelera de reciclaje\n\
Volver para atrás con -1\n\
{LINEA}')
            opcion_clientes=int(input("Ingrese numéricamente la opción deseada: "))

            while opcion_clientes!=-1:

                if opcion_clientes==1: #AGREGAR CLIENTES
                    llenar_clientes(clientes)
                    
                elif opcion_clientes==2: #MODIFICAR CLIENTES
                    pass
                elif opcion_clientes==3: # BORRAR CLIENTES
                    llenar_clientes(clientes)
                elif opcion_clientes==4: #VER CLIENTES
                    print_clientes(clientes)
            print(f'{LINEA}\n\
1-Agregar cliente\n\
2-Modificar cliente\n\
3-Eliminar cliente\n\
4-Ver clientes\n\
5-Papelera de reciclaje\n\
Volver para atrás con -1\n\
{LINEA}')
        opcion_clientes=int(input("Ingrese numéricamente la opción deseada: "))
            
        print(f'{LINEA}\n\
1-Gestionar Habitaciones\n\
2-Gestionar Reservas\n\
3-Ver Estadísticas\n\
Salir del programa con -1\n\
{LINEA}')
        opcion=int(input("Ingrese numéricamente la opción deseada: "))

menu_administrador()
