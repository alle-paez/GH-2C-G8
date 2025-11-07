from listas_codeadas import *

def test_telefono_valido():
    assert es_telefono("1234-5678") is True

def test_telefono_invalido_sin_guion():
    assert es_telefono("12345678") is False

def test_telefono_invalido_con_letras():
    assert es_telefono("12a4-5678") is False


def test_mail_valido_gmail():
    assert es_mail("messi123@gmail.com") is True

def test_mail_invalido_otro_dominio():
    assert es_mail("chaco123@yahoo.com") is False

def test_mail_invalido_sin_arroba():
    assert es_mail("formosa123gmail.com") is False


def test_texto_valido_simple():
    assert es_texto("Hernan") is True

def test_texto_valido_con_acentos():
    assert es_texto("Tutankamon") is True

def test_texto_invalido_con_numero():
    assert es_texto("M3s1i") is False

def test_texto_invalido_con_espacio():
    assert es_texto("Juan Carlos") is False

