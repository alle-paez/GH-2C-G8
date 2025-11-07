from habitaciones import*

def test_ubicar_existente():
    matriz = [
        [101, 15000, "Doble", 2, "Disponible"],
        [102, 18000, "Triple", 3, "Ocupada"]
    ]
    assert ubicar(matriz,102) == 1

def test_ubicar_inexistente():
    matriz = [
        [101, 15000, "Doble", 2, "Disponible"]
    ]
    assert ubicar(matriz, 999) == -1
