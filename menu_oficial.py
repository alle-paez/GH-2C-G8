from listas_codeadas import *
from clientes import *
from habitaciones import *
#from reservas import *
from login import *
#from estadisticas import *
from validaciones import *
def menu_administrador():

    print("")
    print(f'Sistema de Gestión Hotelera'.center(80,"-"))
    print(f'\n\
1-Gestionar Habitaciones\n\
2-Gestionar Reservas\n\
3-Gestionar Clientes\n\
4-Estadísticas\n\
Salir del programa con -1 \n\
{LINEA}')
    
    opcion=validar_entero("Ingrese numéricamente la opción deseada: ")
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
  
            opcion_habitaciones = validar_entero("Ingrese numéricamente la opción deseada: ")
            while opcion_habitaciones!=-1:
                if opcion_habitaciones==1:#AGREGAR HABITACIONES
                    llenar_habitaciones()
                    #AGREGAR CHECKEOS
                elif opcion_habitaciones==2: #MODIFICAR HABITACIONES
                    modificar_habitacion()
                elif opcion_habitaciones==3: #ELIMINAR HABITACIONES
                    eliminar_hab()
                elif opcion_habitaciones==4:#VER HABITACIONES
                    busquedas_habitaciones()
                elif opcion_habitaciones==5:
                    deshacer_borrar()
                
                print(f'{LINEA}\n\
1-Agregar habitación\n\
2-Modificar habitación\n\
3-Borrar habitación\n\
4-Ver habitaciones\n\
5-Papelera de reciclaje\n\
Volver para atrás con -1\n\
{LINEA}')
                opcion_habitaciones = validar_entero("Ingrese numéricamente la opción deseada: ")

        elif opcion==2:
            print(f'\
    1-Agregar reserva\n\
    2-Modificar reserva\n\
    3-Cancelar reserva\n\
    4-Ver reservas\n\
    5-Papelera de reciclaje\n\
    Volver para atrás con -1')

            opcion_reservas = validar_entero("Ingrese numéricamente la opción deseada: ")

            while opcion_reservas!=-1:

                if opcion_reservas==1: #AGREGAR RESERVA
                    llenar_reservas()
                elif opcion_reservas==2: #MODIFICAR RESERVA
                    modificacion()
                elif opcion_reservas==3: # CANCELAR RESERVA
                    eliminar_reserva()
                elif opcion_reservas==4: #VER RESERVAS
                    print_elegir_opcion()
                elif opcion_reservas==5:
                    deshacer_eliminar_reserva()

            print(f'{LINEA}\n\
1-Agregar reserva\n\
2-Modificar reserva\n\
3-Cancelar reserva\n\
4-Ver reservas\n\
5-Papelera de reciclaje\n\
Volver para atrás con -1\n\
{LINEA}')
            opcion_reservas = validar_entero("Ingrese numéricamente la opción deseada: ")

    
        elif opcion==3:
            print(f'{LINEA}\n\
1-Agregar cliente\n\
2-Modificar cliente\n\
3-Eliminar cliente\n\
4-Ver clientes\n\
5-Papelera de reciclaje\n\
Volver para atrás con -1\n\
{LINEA}')   
        
            opcion_clientes=validar_entero("Ingrese numéricamente la opción deseada: ")

            while opcion_clientes!=-1:

                if opcion_clientes==1: #AGREGAR CLIENTES
                    llenar_clientes(m_clientes)
                elif opcion_clientes==2: #MODIFICAR CLIENTES
                    pass
                elif opcion_clientes==3: # BORRAR CLIENTES
                    print_clt(m_clientes)
                    borrar_clientes(m_clientes, clientes_borrados)
                elif opcion_clientes==4: #VER CLIENTES
                    print_clt(m_clientes)
                elif opcion_clientes==5:
                    print_clt(clientes_borrados)
                    deshacer_borrar_clt(m_clientes, clientes_borrados)
                print(f'{LINEA}\n\
1-Agregar cliente\n\
2-Modificar cliente\n\
3-Eliminar cliente\n\
4-Ver clientes\n\
5-Papelera de reciclaje\n\
Volver para atrás con -1\n\
{LINEA}')   
            opcion_clientes=validar_entero("Ingrese numéricamente la opción deseada: ")
        elif opcion==4:
            elegir_opcion_estadistica()

        print(f'{LINEA}\n\
1-Gestionar Habitaciones\n\
2-Gestionar Reservas\n\
3-Gestionar Clientes\n\
4-Ver Estadísticas\n\
Salir del programa con -1\n\
{LINEA}')
        opcion=validar_entero("Ingrese numéricamente la opción deseada: ")


if __name__=="__main__":
    login()
    menu_administrador()