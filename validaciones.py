import re

def verificar_formato(dni):
    patron = r'^\d{8}$'
    if re.match(patron, str(dni)):
        return True
    else: 
        return False
    

def verificar_formato_fecha(fecha):
    formato = r"^\d{4}-\d{2}-\d{2}$"
    if re.match(formato, fecha):
        return True
    else:
        return False
    
def validar_entero(mensaje):
    error = True
    while error: 
        valor = input(mensaje).strip()
        try: 
            num = int(valor)
            error = False
        except ValueError:
            print("Se ingreso un formato incorrecto. ")
    return num

def esta_vacio(mensaje):
    error = True
    while error:
        try:
            txt = input(mensaje).strip().capitalize()
            if not txt: #vacio
                raise ValueError("Debe ingresar algo.")
            error = False
        except ValueError as err:
            print(f"error! {err}")
    return txt
    


if __name__ == "__main__":
    xd = esta_vacio("xdxd: ")