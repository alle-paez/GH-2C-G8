from validaciones import*


def test_verificar_formato_valido():
    assert verificar_formato("30555999") == True

def test_verificar_formato_invalido_menos_digitos():
    assert verificar_formato("1234567") == False

def test_verificar_formato_invalido_mas_digitos():
    assert verificar_formato("123456789") == False

def test_verificar_formato_invalido_letras():
    assert verificar_formato("30a55999") == False

def test_verificar_formato_invalido_vacio():
    assert verificar_formato("") == False


def test_verificar_formato_fecha_valida():
    assert verificar_formato_fecha("2024-01-01") == True

def test_verificar_formato_fecha_formato_dia_mes():
    assert verificar_formato_fecha("01-01-2024") == False

def test_verificar_formato_fecha_con_barra():
    assert verificar_formato_fecha("2024/01/01") == False

def test_verificar_formato_fecha_sin_guion():
    assert verificar_formato_fecha("20240101") == False

def test_verificar_formato_fecha_vacia():
    assert verificar_formato_fecha("") == False
