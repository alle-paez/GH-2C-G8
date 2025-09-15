from listas_codeadas import LINEA, habitaciones, reservas
from habitaciones import print_habitaciones
from reservas import print_reserva as print_reserva_uno, formatear_fecha
from mas_auxiliares import leer_opcion, filtrar_reservas_por_dni

def print_reservas_tabla(m):
    if not m:
        return
    print("")
    print("------------------------------------------------------------------")
    print("ID   | DNI Cliente | Entrada     | Salida      | Hab | Pax | Total")
    print("------------------------------------------------------------------")
    for fila in m:
        id_reserva, dni, check_in, check_out, hab, pax, total = fila
        print(str(id_reserva).ljust(4), "|",
              str(dni).ljust(11), "|",
              formatear_fecha(check_in).ljust(11), "|",
              formatear_fecha(check_out).ljust(11), "|",
              str(hab).ljust(3), "|",
              str(pax).ljust(3), "|",
              str(total).ljust(6))
        
def menu_cliente(dni_login):
    seguir = True
    while seguir:
        print(f'{LINEA}\n'
              f'1- Ver habitaciones\n'
              f'2- Ver mis reservas\n'
              f'Volver con -1\n'
              f'{LINEA}')
        op = leer_opcion("Opción (-1 para volver): ", permitir_menos1=True)

        if op == -1:
            seguir = False

        elif op == 1:
            print_habitaciones(habitaciones)

        elif op == 2:
            mias = filtrar_reservas_por_dni(reservas, dni_login)
            if mias:
                print_reservas_tabla(mias)   # imprime todas con un solo header
                input("\n(Enter para continuar) ")
            else:
                print(f"(No hay reservas para el DNI {dni_login})")

if __name__ == "__main__":
    from login import login
    rol, dni_login = login()
    if rol == "cliente":
        menu_cliente(dni_login)
