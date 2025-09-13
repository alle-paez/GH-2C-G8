import re

tipos   = ["Single", "Doble", "Triple", "Suite"]
estados = ["Disponible", "Ocupada", "Mantenimiento"]

def leer_tipo():
    tipo = input("Escribí el tipo de habitación (Single/Doble/Triple/Suite): ").capitalize()
    valido = list(filter(lambda x: x == tipo, tipos))
    while len(valido) == 0:
        tipo = input("Tipo inválido. Volvé a escribir: ").capitalize()
        valido = list(filter(lambda x: x == tipo, tipos))
    return tipo

def leer_estado():
    estado = input("Escribí el estado (Disponible/Ocupada/Mantenimiento): ").capitalize()
    valido = list(filter(lambda x: x == estado, estados))
    while len(valido) == 0:
        estado = input("Estado inválido. Volvé a escribir: ").capitalize()
        valido = list(filter(lambda x: x == estado, estados))
    return estado

def ubicar(matriz, item):
    flag = 0
    i = 0
    pos = -1
    while flag != 1:
        if matriz[i][0] == item:
            flag = 1
            pos = i
        i += 1
        if i == len(matriz):
            flag = 1
    return pos

def leer_numero(mensaje, permitir_menos1=False):
    """
    Pide un número entero validado con expresión regular.
    Si permitir_menos1=True, se permite el valor -1 como salida.
    """
    patron = r"^-?[0-9]+$"
    nro = input(mensaje).strip()
    while not re.match(patron, nro) or (not permitir_menos1 and int(nro) < 1):
        print("Entrada inválida. Solo números enteros válidos.")
        nro = input(mensaje).strip()
    return int(nro)
