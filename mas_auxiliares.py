import json

def leer_opcion(prompt, permitir_menos1=False):
    while True:
        txt = input(prompt).strip()


        if permitir_menos1 and txt == "-1":
            return -1


        if txt.isdigit():
            return int(txt)

        if txt.startswith("-") and txt != "-1":
            print("No se admiten negativos (solo -1 para volver).")
        else:
            print("Entrada inválida. Ingrese un número entero.")
def filtrar_reservas_por_dni(matriz, dni):
    dni_norm = str(dni).strip()
    return [r for r in matriz if str(r[1]).strip() == dni_norm]

def ordenar(lista, dato):
    if len(lista) <= 1:
        return lista
    
    menor = min(lista, key=lambda x: x[dato])
    resto = [x for x in lista if x is not menor]
    return [menor] + ordenar(resto, dato)
