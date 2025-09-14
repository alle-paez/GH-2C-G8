from listas_codeadas import habitaciones
from auxiliar_habitaciones import *

def print_habitaciones(matriz):
    print("Número    |Precio    |Tipo      |Capacidad |Estado    |")
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(f'{matriz[i][j]} '.center(10, " "), end="")
        print()
    return matriz

es_entero = lambda x: re.search(r'^-?[0-9]+$', x) is not None

def llenar_habitaciones(matriz):
    numero = input("Número de habitación (-1 para salir): ")
    flag=es_entero(numero)
    #chekeo que el número sea válido
    while flag==False:
        numero = input("El valor ingresado no es válido, ingrese nuevamente(-1 para salir): ")
        flag=es_entero(numero)
    #checkeo que no exista ya
    while int(numero) != -1:
        idx = ubicar(matriz, int(numero))
        while idx != -1:
            print("Esta habitación ya existe.")
            while flag==False or idx!=-1:
                numero = input("Número de habitación (-1 para salir): ")
                flag=es_entero(numero)
                idx = ubicar(matriz, int(numero))

        if int(numero) != -1 and idx == -1 and flag:
            precio = input("Precio (entero > 0): ")
            es_entero(precio)

            tipo_txt = leer_tipo()
            capacidad = input("Capacidad (> 0): ")

            estado_txt = leer_estado()

            matriz.append([numero, precio, tipo_txt, capacidad, estado_txt])
            print("Habitación agregada.")

            numero = input("Número de habitación (-1 para salir): ")
            idx = ubicar(matriz, int(numero))
            flag=es_entero(numero)



def modificar_habitacion(matriz):
    numero = leer_numero("Número de habitación a modificar (-1 para volver): ", permitir_menos1=True)

    while numero != -1:
        idx = ubicar(matriz, numero)
        while idx == -1 and numero != -1:
            print("No existe esa habitación.")
            numero = leer_numero("Número de habitación a modificar (-1 para volver): ", permitir_menos1=True)
            if numero != -1:
                idx = ubicar(matriz, numero)

        if numero != -1:
            fila = matriz[idx]  # [nro, precio, tipo, capacidad, estado]
            print("\nActual →",
                  "Nro:", fila[0],
                  "Precio:", fila[1],
                  "Tipo:", fila[2],
                  "Capacidad:", fila[3],
                  "Estado:", fila[4])

            op_txt = input("\n¿Qué modificar?  1-Precio  2-Tipo  3-Capacidad  4-Estado  5-Todos  (-1 volver)\nOpción: ").strip()
            while not (op_txt.lstrip("-").isdigit() and int(op_txt) in {1,2,3,4,5,-1}):
                print("Opción inválida.")
                op_txt = input("\n1-Precio  2-Tipo  3-Capacidad  4-Estado  5-Todos  (-1 volver)\nOpción: ").strip()
            op = int(op_txt)

            while op != -1:
                if op == 1:
                    nuevo = leer_numero("Nuevo precio (> 0): ")
                    matriz[idx][1] = nuevo
                    print("Precio actualizado.")

                elif op == 2:
                    matriz[idx][2] = leer_tipo()
                    print("Tipo actualizado.")

                elif op == 3:
                    cap = leer_numero("Nueva capacidad (> 0): ")
                    matriz[idx][3] = cap
                    print("Capacidad actualizada.")

                elif op == 4:
                    matriz[idx][4] = leer_estado()
                    print("Estado actualizado.")

                elif op == 5:
                    nuevo = leer_numero("Nuevo precio (> 0): ")
                    t_txt = leer_tipo()
                    cap = leer_numero("Nueva capacidad (> 0): ")
                    e_txt = leer_estado()

                    matriz[idx][1] = nuevo
                    matriz[idx][2] = t_txt
                    matriz[idx][3] = cap
                    matriz[idx][4] = e_txt
                    print("Todos los campos actualizados.")

                op_txt = input("\n1-Precio  2-Tipo  3-Capacidad  4-Estado  5-Todos  (-1 volver)\nOpción: ").strip()
                while not (op_txt.lstrip("-").isdigit() and int(op_txt) in {1,2,3,4,5,-1}):
                    print("Opción inválida.")
                    op_txt = input("\n1-Precio  2-Tipo  3-Capacidad  4-Estado  5-Todos  (-1 volver)\nOpción: ").strip()
                op = int(op_txt)

            numero = leer_numero("\nNúmero de otra habitación a modificar (-1 para volver): ", permitir_menos1=True)

