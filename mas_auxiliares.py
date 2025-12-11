
def filtrar_reservas_por_dni(matriz, dni):
    dni_norm = str(dni).strip()
    return [r for r in matriz if str(r[1]).strip() == dni_norm]

def ordenar(lista, dato):
    if len(lista) <= 1:
        return lista
    
    menor = min(lista, key=lambda x: x[dato])
    resto = [x for x in lista if x is not menor]
    return [menor] + ordenar(resto, dato)
