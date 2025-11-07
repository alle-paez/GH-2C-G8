from validaciones import validar_entero
from habitaciones import leer_habitaciones
from login import login


def menu_clientes(dni_login,
                  archivo_reservas="tabla_reservas.txt",
                  archivo_habitaciones="tabla_habitaciones.json"):
    print("")
    print(f"Sistema de Gestión Hotelera".center(70, "-"))
    print("===== MENÚ CLIENTE =====")

    if dni_login is None:
        print("Error: no se recibió el DNI del cliente.")
    else:
        salir = False
        while salir == False:
            print("\n1-Ver mis reservas\n2-Ver mis habitaciones\nSalir con 0 o -1")
            print("-" * 70)
            opcion = validar_entero("Ingrese numéricamente la opción deseada: ")

            if opcion == -1 or opcion == 0:
                print("Saliendo del menú cliente...")
                salir = True
            else:
                if opcion == 1:
                    mostrar_reservas_cliente(dni_login, archivo_reservas)
                else:
                    if opcion == 2:
                        mostrar_habitaciones_cliente(dni_login, archivo_reservas, archivo_habitaciones)
                    else:
                        print("Opción inválida. Intente nuevamente.")


def mostrar_reservas_cliente(dni_login, archivo_reservas):
    try:
        f = open(archivo_reservas, "r", encoding="UTF-8")
        linea = f.readline()

        hay_reservas = 0
        print("")
        print("-" * 70)
        print("ID   | DNI Cliente | Entrada     | Salida      | Hab | Pax | Total")
        print("-" * 70)

        while linea != "":
            s = linea.strip()
            if s != "":
                p = s.split(";")
                if len(p) >= 7 and p[1] == str(dni_login):
                    rid, dni, ci, co, hab, pax, total = p[:7]
                    print(str(rid).ljust(4), "|",
                          str(dni).ljust(11), "|",
                          str(ci).ljust(11), "|",
                          str(co).ljust(11), "|",
                          str(hab).ljust(3), "|",
                          str(pax).ljust(3), "|",
                          str(total).ljust(6))
                    hay_reservas = 1
            linea = f.readline()

        if hay_reservas == 0:
            print("No se encontraron reservas para este cliente.")
        print("-" * 70)
        f.close()

    except FileNotFoundError:
        print("No se encontró el archivo de reservas.")
    except OSError:
        print("Error al acceder al archivo de reservas.")


def mostrar_habitaciones_cliente(dni_login, archivo_reservas, archivo_habitaciones):
    try:
        habs_cliente = []
        f = open(archivo_reservas, "r", encoding="UTF-8")
        linea = f.readline()
        while linea != "":
            s = linea.strip()
            if s != "":
                p = s.split(";")
                if len(p) >= 5 and p[1] == str(dni_login):
                    try:
                        nro_hab = int(p[4])
                        if nro_hab not in habs_cliente:
                            habs_cliente.append(nro_hab)
                    except ValueError:
                        pass
            linea = f.readline()
        f.close()

        if len(habs_cliente) == 0:
            print("No hay habitaciones registradas para este cliente.")
        else:
            habitaciones = leer_habitaciones(archivo_habitaciones)
            if habitaciones == None:
                habitaciones = []

            print("\n--- Habitaciones reservadas ---")
            print(f'{"Nro":<10}{"Precio":<10}{"Tipo":<12}{"Capacidad":<12}{"Estado":<10}')
            print("-" * 70)

            i = 0
            mostradas = 0
            while i < len(habitaciones):
                h = habitaciones[i]
                if type(h) == dict and "hab" in h and h["hab"] in habs_cliente:
                    print(f"{h['hab']:<10}{h['precio']:<10}{h['tipo']:<12}{h['capacidad']:<12}{h['estado']:<10}")
                    mostradas += 1
                i += 1

            if mostradas == 0:
                print("No hay habitaciones registradas para este cliente.")

    except FileNotFoundError:
        print("No se encontró el archivo de reservas o habitaciones.")
    except OSError:
        print("Error de acceso a archivos.")


if __name__ == "__main__":
    rol, dni_login = login()
    if rol == "cliente":
        menu_clientes(dni_login)
    else:
        print("Ingresá como cliente para ver este menú.")
