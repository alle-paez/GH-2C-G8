# menu_oficial.py — unificado con login + submenús completos (Habitaciones/Reservas/Clientes/Estadísticas)

from listas_codeadas import LINEA, habitaciones, reservas, clientes
from habitaciones import (
    print_habitaciones, llenar_habitaciones,
    modificar_habitacion, eliminar_hab, deshacer_borrar, ordenar_hab
)
from clientes import (
    print_clt,
    llenar_clientes,       # AGREGAR
    modificar_clientes,    # MODIFICAR
    borrar_clientes,       # BORRAR (papelera)
    deshacer_borrar_clt    # DESHACER
)
from reservas import (
    print_reserva,             # firma: (matriz, pos)
    llenar_reservas,           # AGREGAR
    modificacion,              # MODIFICAR
    reservas_eliminadas,       # CANCELAR (papelera)
    print_elegir_opcion,       # VER (tu selector/visor)
    deshacer_eliminar_reserva  # DESHACER
)
from mas_auxiliares import leer_opcion, filtrar_reservas_por_dni
from estadisticas import *

# ===========================
# SUBMENÚ HABITACIONES (ADMIN)
# ===========================
def submenu_habitaciones():
    if "_hab_borradas" not in globals():
        globals()["_hab_borradas"] = []

    seguir = True
    while seguir:
        print("\n" + "=" * 70)
        print("              GESTIÓN DE HABITACIONES")
        print("=" * 70)
        print(" 1) Ver TODAS")
        print(" 2) Alta (llenar)")
        print(" 3) Modificar")
        print(" 4) Eliminar")
        print(" 5) Deshacer eliminación")
        print(" 6) Ordenar por número")
        print(" -1) Volver")
        print(LINEA)

        op = leer_opcion("Opción (-1 para volver): ", permitir_menos1=True)

        if op == -1:
            seguir = False
        elif op == 1:
            print_habitaciones(habitaciones); input("\n(Enter)")
        elif op == 2:
            llenar_habitaciones(habitaciones); input("\n(Enter)")
        elif op == 3:
            modificar_habitacion(habitaciones); input("\n(Enter)")
        elif op == 4:
            eliminar_hab(habitaciones, globals()["_hab_borradas"]); input("\n(Enter)")
        elif op == 5:
            deshacer_borrar(habitaciones, globals()["_hab_borradas"]); input("\n(Enter)")
        elif op == 6:
            ordenar_hab(habitaciones)
            print("\n(Habitaciones ordenadas)\n")
            print_habitaciones(habitaciones); input("\n(Enter)")
        else:
            print("Opción inválida.")


# ===========================
# SUBMENÚ RESERVAS (ADMIN)
# ===========================
def submenu_reservas():
    seguir = True
    while seguir:
        print("\n" + "=" * 70)
        print("              GESTIÓN DE RESERVAS")
        print("=" * 70)
        print(" 1) Agregar reserva")
        print(" 2) Modificar reserva")
        print(" 3) Cancelar reserva (papelera)")
        print(" 4) Ver reservas")
        print(" 5) Deshacer eliminación")
        print(" -1) Volver")
        print(LINEA)

        op = leer_opcion("Opción (-1 para volver): ", permitir_menos1=True)

        if op == -1:
            seguir = False
        elif op == 1:            # AGREGAR RESERVA
            llenar_reservas(); input("\n(Enter)")
        elif op == 2:            # MODIFICAR RESERVA
            modificacion(); input("\n(Enter)")
        elif op == 3:            # CANCELAR / ELIMINAR (papelera)
            reservas_eliminadas(); input("\n(Enter)")
        elif op == 4:            # VER RESERVAS (tu visor)
            print_elegir_opcion(); input("\n(Enter)")
        elif op == 5:            # DESHACER ELIMINACIÓN
            deshacer_eliminar_reserva(); input("\n(Enter)")
        else:
            print("Opción inválida.")


# ===========================
# SUBMENÚ CLIENTES (ADMIN)
# ===========================
def submenu_clientes():
    # buffer local de “papelera” para clientes (si no existe uno global)
    if "clientes_borrados" not in globals():
        globals()["clientes_borrados"] = []

    seguir = True
    while seguir:
        print("\n" + "=" * 70)
        print("            👥  GESTIÓN DE CLIENTES")
        print("=" * 70)
        print(" 1) Agregar cliente")
        print(" 2) Modificar cliente")
        print(" 3) Borrar cliente (papelera)")
        print(" 4) Ver clientes")
        print(" 5) Deshacer eliminación")
        print(" -1) Volver")
        print(LINEA)

        op = leer_opcion("Opción (-1 para volver): ", permitir_menos1=True)

        if op == -1:
            seguir = False
        elif op == 1:   # AGREGAR
            llenar_clientes(clientes); input("\n(Enter)")
        elif op == 2:   # MODIFICAR
            print_clt(clientes)
            modificar_clientes(clientes); input("\n(Enter)")
        elif op == 3:   # BORRAR (papelera)
            print_clt(clientes)
            borrar_clientes(clientes, globals()["clientes_borrados"]); input("\n(Enter)")
        elif op == 4:   # VER
            print_clt(clientes); input("\n(Enter)")
        elif op == 5:   # DESHACER
            # mostrar papelera y deshacer
            if globals()["clientes_borrados"]:
                print_clt(globals()["clientes_borrados"])
            deshacer_borrar_clt(clientes, globals()["clientes_borrados"]); input("\n(Enter)")
        else:
            print("Opción inválida.")


# ===========================
# SUBMENÚ ESTADÍSTICAS (ADMIN)
# ===========================
def submenu_estadisticas():
    seguir = True
    while seguir:
        print("\n" + "=" * 70)
        print("                  ESTADÍSTICAS")
        print("=" * 70)
        print(" 1) Mostrar resumen global")
        print(" 2) Estadísticas de habitaciones")
        print(" 3) Estadísticas mensuales")
        print(" 4) Resumen máximos y mínimos")
        print(" 5) Porcentajes por habitación")
        print(" -1) Volver")
        print(LINEA)

        op = leer_opcion("Opción (-1 para volver): ", permitir_menos1=True)

        if op == -1:
            seguir = False
        elif op == 1:
            mostrar_diccionario(estadisticas_globales(reservas)); input("\n(Enter)")
        elif op == 2:
            mostrar_como_tabla(estadisticas_habitacion(reservas), titulo_clave="Hab"); input("\n(Enter)")
        elif op == 3:
            mostrar_como_tabla(estadisticas_mensuales(reservas), titulo_clave="Mes"); input("\n(Enter)")
        elif op == 4:
            print("Máximos y mínimos por NOCHES:")
            mostrar_diccionario(max_min_noches(reservas))
            print(LINEA)
            print("Máximos y mínimos por TOTAL:")
            mostrar_diccionario(max_min_totales(reservas))
            input("\n(Enter)")
        elif op == 5:
            mostrar_diccionario(porcentajes_reservas_x_habitacion(reservas)); input("\n(Enter)")
        else:
            print("Opción inválida.")
# ===========================
# MENÚ ADMIN (usa submenús)
# ===========================
def menu_admin(dni_admin):
    seguir = True
    while seguir:
        print("\n" + "=" * 70)
        print("                 MENÚ ADMINISTRADOR")
        print("=" * 70)
        print(" 1) Habitaciones")
        print(" 2) Reservas")
        print(" 3) Clientes")
        print(" 4) Estadísticas")
        print(" -1) Salir")
        print(LINEA)

        op = leer_opcion("Opción (-1 para salir): ", permitir_menos1=True)

        if op == -1:
            seguir = False
        elif op == 1:
            submenu_habitaciones()
        elif op == 2:
            submenu_reservas()
        elif op == 3:
            submenu_clientes()
        elif op == 4:
            submenu_estadisticas()
        else:
            print("Opción inválida.")


# ===========================
# MENÚ CLIENTE (ve solo lo suyo)
# ===========================
def menu_cliente(dni_login):
    seguir = True
    while seguir:
        print(f'{LINEA}\n'
              f'** MENÚ CLIENTE **\n'
              f'1- Ver habitaciones\n'
              f'2- Ver mis reservas\n'
              f'Volver con -1\n'
              f'{LINEA}')
        op = leer_opcion("Opción (-1 para volver): ", permitir_menos1=True)

        if op == -1:
            seguir = False
        elif op == 1:
            print_habitaciones(habitaciones); input("\n(Enter)")
        elif op == 2:
            mias = filtrar_reservas_por_dni(reservas, dni_login)
            if mias:
                for i in range(len(mias)):
                    print_reserva(mias, i)
            else:
                print(f"(No hay reservas para el DNI {dni_login})")
            input("\n(Enter)")
        else:
            print("Opción inválida.")


# ===========================
# Main con login
# ===========================
if __name__ == "__main__":
    from login import login
    rol, dni_login = login()
    if rol == "admin":
        menu_admin(dni_login)
    elif rol == "cliente":
        menu_cliente(dni_login)
    else:
        print("Rol no reconocido.")
