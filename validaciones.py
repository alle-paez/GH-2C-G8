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

            if int(valor) != -1 and int(valor) < 0:
                raise Exception("El número ingresado no puede ser negativo.")
            error = False

        except ValueError:
            print("Se ingreso un formato incorrecto. ")
        except Exception as e:
            print(f"Error! {e}")
        except: 
            print("Error inesperado. Intente nuevamente. ")
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
        except:
            print("Error inesperado. Intente nuevamente. ")
    return txt
    


if __name__ == "__main__":
    xd = esta_vacio("xdxd: ")

"""def buscar_habitacion(nro_hab, i=0):
    with open("tabla_habitaciones.json", "r", encoding="UTF-8") as archivo:
        tabla_habitaciones = json.load(archivo)

        if i >= len(tabla_habitaciones):
            return False
        else:
            if str(tabla_habitaciones[i]["hab"]) == str(nro_hab):
                return True
        return buscar_habitacion(nro_hab, i + 1)
    



def verificar_existencia_habitación():
    while True:
        try:
            hab=input("Ingrese el número de habitación: ")
            assert buscar_habitacion(hab) == True
            return hab
        except AssertionError:
            print("La habitación ingresada no existe.")"""