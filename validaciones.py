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
    
def filtrar_reservas_por_dni(matriz, dni):
    dni_norm = str(dni).strip()
    return [r for r in matriz if str(r[1]).strip() == dni_norm]

def ordenar(lista, dato):
    if len(lista) <= 1:
        return lista
    
    menor = min(lista, key=lambda x: x[dato])
    resto = [x for x in lista if x is not menor]
    return [menor] + ordenar(resto, dato)

if __name__ == "__main__":
    xd = esta_vacio("xdxd: ")
