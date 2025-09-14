from listas_codeadas import LINEA, habitaciones, reservas
from opcion_habitaciones import print_habitaciones
from reservas import print_reservas
from mas_auxiliares import leer_opcion, filtrar_reservas_por_dni


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
                print_reservas(mias)
            else:
                print(f"(No hay reservas para el DNI {dni_login})")

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    from login import login
    rol, dni_login = login()
    if rol == "cliente":
        menu_cliente(dni_login)
