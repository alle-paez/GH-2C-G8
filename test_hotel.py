import pytest
from habitaciones import validar_incremento
from validaciones import verificar_formato, verificar_formato_fecha, ordenar


@pytest.fixture
def habitaciones_base():
    return [
        {"hab": 102, "precio": 18000},
        {"hab": 101, "precio": 15000},
        {"hab": 103, "precio": 20000}
    ]

def test_ordenar_por_numero(habitaciones_base):
    # Arrange
    habitaciones = list(habitaciones_base)
    # Act
    resultado = ordenar(habitaciones, "hab")

    # Assert
    assert [h["hab"] for h in resultado] == [101, 102, 103]


def test_ordenar_por_precio(habitaciones_base):
    # Arrange
    habitaciones = list(habitaciones_base)

    # Act
    resultado = ordenar(habitaciones, "precio")

    # Assert
    assert [h["precio"] for h in resultado] == [15000, 18000, 20000]


@pytest.mark.parametrize(
    "dni, esperado",
    [
        ("30555999", True),
        ("1234567", False),
        ("123456789", False),
        ("30a55999", False),
        ("", False),
    ]
)
def test_verificar_formato_dni(dni, esperado):
    # Arrange
    dni_ingresado = dni

    # Act
    resultado = verificar_formato(dni_ingresado)

    # Assert
    assert resultado == esperado


@pytest.mark.parametrize(
    "fecha, esperado",
    [
        ("2024-01-01", True),
        ("01-01-2024", False),
        ("2024/01/01", False),
        ("20240101", False),
        ("", False),
    ]
)
def test_verificar_formato_fecha(fecha, esperado):
    # Arrange
    fecha_ingresada = fecha

    # Act
    resultado = verificar_formato_fecha(fecha_ingresada)

    # Assert
    assert resultado == esperado

def test_incremento_menor_a_75():
    with pytest.raises(ValueError) as info:
        validar_incremento(-80)

    assert str(info.value) == "No se puede bajar más de un 75%."

def test_incremento_mayor_a_300():
    with pytest.raises(ValueError) as info:
        validar_incremento(350)

    assert str(info.value) == "No se puede aumentar más de un 300%."

def test_incremento_valido():
    resultado = validar_incremento(10)
    assert resultado == 10
