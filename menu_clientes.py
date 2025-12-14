from validaciones import validar_entero
from habitaciones import leer_habitaciones
from login import login


# ================== UTILIDAD FECHA ==================
def formatear_fecha(fecha_txt):
    s = str(fecha_txt).strip()

    if s.startswith("(") and s.endswith(")"):
        s = s[1:-1]

    partes = []
    for p in s.split(","):
        partes.append(p.strip())

    if len(partes) != 3:
        return str(fecha_txt)

    anio = partes[0]
    mes = partes[1].zfill(2)
    dia = partes[2].zfill(2)
    return f"{dia}/{mes}/{anio}"


# ================== MENÚ CLIENTE ==================
def menu_clientes(
    dni_login,
    archivo_reservas="data/txt/tabla_reservas.txt",
    archivo_habitaciones="data/json/tabla_habitaciones.json"
):
    print("")
    print("Sistema de Gestión Hotelera".center(80, "-"))
    print("MENÚ CLIENTE".center(80))
    print("-" * 80)

    if dni_login is None:
        print("Error: no se recibió el DNI del cliente.")
        return

    dni_login_norm = str(dni_login).strip()

    salir = False
    while not salir:
        print("\n1-Ver mis reservas")
        print("2-Ver mis habitaciones")
        print("Salir con 0 o -1")
        print("-" * 80)

        opcion = validar_entero("Ingrese numéricamente la opción deseada: ")

        if opcion in (-1, 0):
            print("Saliendo del menú cliente...")
            salir = True

        elif opcion == 1:
            mostrar_reservas_cliente(dni_login_norm, archivo_reservas)
            input("\nPresione Enter para volver al menú...")

        elif opcion == 2:
            mostrar_habitaciones_cliente(
                dni_login_norm,
                archivo_reservas,
                archivo_habitaciones
            )
            input("\nPresione Enter para volver al menú...")

        else:
            print("Opción inválida. Intente nuevamente.")


# ================== RESERVAS DEL CLIENTE ==================
def mostrar_reservas_cliente(dni_login_norm, archivo_reservas):
    try:
        hay_reservas = False

        print("")
        print("MIS RESERVAS".center(80, "-"))
        print("-" * 80)
        print(f'{"ID":<4} | {"DNI":<10} | {"Entrada":<10} | {"Salida":<10} | {"Hab":<3} | {"Pax":<3} | {"Total":>10}')
        print("-" * 80)

        with open(archivo_reservas, "r", encoding="UTF-8") as f:
            for linea in f:
                s = linea.strip()
                if s == "":
                    continue

                p = s.split(";")
                if len(p) >= 7 and str(p[1]).strip() == dni_login_norm:
                    rid, dni, ci, co, hab, pax, total = p[:7]
                    ci_fmt = formatear_fecha(ci)
                    co_fmt = formatear_fecha(co)

                    print(
                        f'{str(rid):<4} | '
                        f'{str(dni):<10} | '
                        f'{ci_fmt:<10} | '
                        f'{co_fmt:<10} | '
                        f'{str(hab):<3} | '
                        f'{str(pax):<3} | '
                        f'{str(total):>10}'
                    )
                    hay_reservas = True

        if not hay_reservas:
            print("No se encontraron reservas para este cliente.")

        print("-" * 80)

    except FileNotFoundError:
        print("No se encontró el archivo de reservas.")
    except OSError:
        print("Error al acceder al archivo de reservas.")


# ================== HABITACIONES DEL CLIENTE ==================
def mostrar_habitaciones_cliente(dni_login_norm, archivo_reservas, archivo_habitaciones):
    try:
        habs_cliente = []

        with open(archivo_reservas, "r", encoding="UTF-8") as f:
            for linea in f:
                s = linea.strip()
                if s == "":
                    continue

                p = s.split(";")
                if len(p) >= 5 and str(p[1]).strip() == dni_login_norm:
                    try:
                        nro_hab = int(p[4])
                        if nro_hab not in habs_cliente:
                            habs_cliente.append(nro_hab)
                    except ValueError:
                        pass

        if not habs_cliente:
            print("No hay habitaciones registradas para este cliente.")
            return

        habitaciones = leer_habitaciones(archivo_habitaciones)
        if habitaciones is None:
            habitaciones = []

        print("")
        print("HABITACIONES RESERVADAS".center(80, "-"))
        print("-" * 80)
        print(f'{"Nro":<4} | {"Precio":<8} | {"Tipo":<15} | {"Capacidad":<9} | {"Estado":<15}')
        print("-" * 80)

        mostradas = 0
        for h in habitaciones:
            if isinstance(h, dict) and "hab" in h and h["hab"] in habs_cliente:
                print(
                    f"{h['hab']:<4} | "
                    f"{h['precio']:<8} | "
                    f"{h['tipo']:<15} | "
                    f"{h['capacidad']:<9} | "
                    f"{h['estado']:<15}"
                )
                mostradas += 1

        if mostradas == 0:
            print("No se encontraron habitaciones para este cliente.")

        print("-" * 80)

    except FileNotFoundError:
        print("No se encontró el archivo de reservas o habitaciones.")
    except OSError:
        print("Error de acceso a archivos.")


# ================== EJECUCIÓN ==================
if __name__ == "__main__":
    rol, dni_login = login()
    if rol == "cliente":
        menu_clientes(dni_login)
    else:
        print("Ingresá como cliente para ver este menú.")
