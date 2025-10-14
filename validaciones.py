import re

def verificar_formato(dni):
    patron = r'^\d{8}$'
    if re.match(patron, dni):
        return True
    else: 
        return False
    

def verificar_formato_fecha(fecha):
    formato = r"^\d{4}-\d{2}-\d{2}$"
    if re.match(formato, fecha):
        return True
    else:
        return False