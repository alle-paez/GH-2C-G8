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
    
def validar_entero(mensaje):
    while True: 
        valor = input(mensaje).strip()
        try: 
            num = int(valor)
            break
        except ValueError:
            print("Se ingreso un formato incorrecto. ")
    return num

def esta_vacio(mensaje):
    while True:
        try:
            txt = input(mensaje).strip().capitalize()
            if not txt: #vacio
                raise ValueError("Debe ingresar algo.")
            return txt
        except ValueError as error:
            print(f"error! {error}")
    


if __name__ == "__main__":
    validar_entero("Ingrese un numero: ")