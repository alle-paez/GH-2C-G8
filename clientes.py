from listas_codeadas import *
import re
from habitaciones import *
from validaciones import *
import json
from validaciones import *


def leer_clientes(archivo="data/json/tabla_clientes.json", modo="r"):
    contenido = None
    try:
        contenido = open(archivo, modo, encoding="UTF-8")
        clientes = json.load(contenido)
        clientes_ordenados_por_dni = ordenar(clientes, "dni")
        return clientes_ordenados_por_dni
    except:
        print("Error, no se pudo acceder a la base de datos")
    finally:
        if contenido:  # solo cerramos si se abrió
            try:
                contenido.close()
            except:
                print("Error al cerrar el archivo")

        
#AGREGAR CLIENTES--------------------------------------------------------------------------------

def llenar_clientes(archivo="data/json/tabla_clientes.json"):
    dni = validar_entero("Ingrese el Dni del cliente: (-1 para finalizar la carga): ")

    while dni != -1 and not verificar_formato(dni):
        dni = validar_entero("Ingrese el Dni del cliente nuevamente: (-1 para finalizar la carga): ")

    # si salió con -1, termina
    if dni == -1:
        return

    while dni != -1:
        try:
            with open(archivo, 'r', encoding="UTF-8") as data:
                clientes = json.load(data)
                clientes_ordenados_por_dni = ordenar(clientes, "dni")

            dni_norm = str(dni).strip()
            dnis_existentes = [str(cli["dni"]).strip() for cli in clientes_ordenados_por_dni]

            if dni_norm in dnis_existentes:
                print("El dni ingresado ya existe, por favor, ingrese otro.")
                dni = validar_entero("Ingrese el dni del cliente nuevamente (-1 para finalizar): ")

                while dni != -1 and not verificar_formato(dni):
                    dni = validar_entero("Ingrese el dni del cliente nuevamente (-1 para finalizar): ")

            if dni != -1:
                nombre = esta_vacio("Ingrese el nombre del cliente: ")
                while not es_texto(nombre):
                    nombre = esta_vacio("Ingrese el nombre del cliente nuevamente: ")

                apellido = esta_vacio("Ingrese el apellido del cliente: ")
                while not es_texto(apellido):
                    apellido = esta_vacio("Ingrese el apellido del cliente: ")

                telefono = input("Ingrese el telefono del cliente: ").strip()
                while not es_telefono(telefono):
                    telefono = input("Telefono invalido. Reingrese: ").strip()


                mail = esta_vacio("Ingrese el e-mail del cliente: ")
                while not es_mail(mail):
                    mail = esta_vacio("Ingrese el e-mail del cliente: ")

                nuevo_cliente = {
                    "dni": dni,
                    "nombre": nombre,
                    "apellido": apellido,
                    "telefono": telefono,
                    "mail": mail
                }

                clientes.append(nuevo_cliente)
                with open(archivo, 'w', encoding="UTF-8") as data:
                    json.dump(clientes, data, ensure_ascii=False, indent=4)

                print(f"Se ha agregado al cliente {nuevo_cliente['nombre']} {nuevo_cliente['apellido']} de dni {nuevo_cliente['dni']}.")

                dni = validar_entero("Ingrese el Dni del cliente: (-1 para finalizar la carga): ")
                while dni != -1 and not verificar_formato(dni):
                    dni = validar_entero("Formato incorrecto, ingrese el Dni del cliente nuevamente: (-1 para finalizar la carga): ")

        except (FileNotFoundError, OSError) as error:
            print(f"Error! {error}")
        except:
            print("Error inesperado. Intente nuevamente. ")
            

#MODIFICAR CLIENTES-------------------------------------------------------------------------------------------------------
def abrir_archivo(archivo):
    try:
        with open(archivo, 'r', encoding="UTF-8") as data:
            tabla = json.load(data)
            clientes_ordenados_por_dni = ordenar(tabla, "dni")
        return clientes_ordenados_por_dni
    except (FileNotFoundError, OSError) as error:
        print(f"Error! No se pudo abrir el archivo. {error}")
    except Exception as e:
        print(f"Error! {e}")
    except:
        print("Error inesperado. Intente nuevamente. ")

def escribir_archivo(archivo,tabla,mensaje="Dump generado con exito"):
    try:
        with open(archivo, 'w', encoding="UTF-8") as data:
            json.dump(tabla,data,ensure_ascii=False, indent=4)
        print(mensaje)
    except (FileNotFoundError, OSError) as error:
        print(f"Error! No se pudo abrir el archivo. {error}")
    except Exception as e:
        print(f"Error! {e}")
    

def modificar_clientes(archivo="data/json/tabla_clientes.json"):
    print_clt(archivo)
    dni = validar_entero("\nIngrese DNI del cliente a modificar (-1 para salir): ")
    while dni != -1:
        if re.match(r"^\d{8}$", str(dni)):
            dni = int(dni)
            
            clientes = abrir_archivo(archivo)
            dnis_cli = [cli["dni"] for cli in clientes]

            if dni in dnis_cli:
                pos = dnis_cli.index(dni)            
            else:
                pos = -1

            if pos != -1:
                cliente = clientes[pos]
                print("Cliente encontrado:")
                print(f'{"Dni":<10}{"Nombre":<10}{"Apellido":<10}{"Teléfono":<15}{"Mail":<15}')
                print(f'{cliente["dni"]:<10}{cliente["nombre"]:<10}{cliente["apellido"]:<10}{cliente["telefono"]:<15}{cliente["mail"]:<15}')

                nuevo_nombre   = input(f"Nuevo nombre ({cliente['nombre']})(Enter para continuar): ").strip()
                if nuevo_nombre != "":
                    while not es_texto(nuevo_nombre) and nuevo_nombre != "":
                        nuevo_nombre = input("Nombre inválido. Reingrese: ").strip()
                    if nuevo_nombre != "":
                        clientes[pos]["nombre"] = nuevo_nombre.title()


                nuevo_apellido = input(f"Nuevo apellido ({cliente['apellido']})(Enter para continuar):").strip()
                if nuevo_apellido != "":
                    while not es_texto(nuevo_apellido) and nuevo_apellido != "":
                        nuevo_apellido = input("Apellido inválido. Reingrese: ").strip()
                    if nuevo_apellido != "":
                        clientes[pos]["apellido"] = nuevo_apellido.title()

                nuevo_tel = input(f"Nuevo teléfono ({cliente['telefono']})(Enter para continuar): ").strip()
                if nuevo_tel != "":
                    while not es_telefono(nuevo_tel) and nuevo_tel != "":
                        nuevo_tel = input("Teléfono inválido. Reingrese (ARG: 10 dígitos): ").strip()
                    if nuevo_tel != "":
                        clientes[pos]["telefono"] = nuevo_tel

                nuevo_mail = input(f"Nuevo mail ({cliente['mail']}): ").strip()
                if nuevo_mail != "":
                    while not es_mail(nuevo_mail) and nuevo_mail != "":
                        nuevo_mail = input("Mail inválido (solo @gmail.com). Reingrese: ").strip()
                    if nuevo_mail != "":
                        clientes[pos]["mail"] = nuevo_mail

                escribir_archivo(archivo,clientes,"Cliente modificado con éxito.")
                cliente = clientes[pos]
                print(f'{"Dni":<10}{"Nombre":<10}{"Apellido":<10}{"Teléfono":<15}{"Mail":<15}')
                print(f'{cliente["dni"]:<10}{cliente["nombre"]:<10}{cliente["apellido"]:<10}{cliente["telefono"]:<15}{cliente["mail"]:<15}')

            else:
                print("No existe cliente con ese DNI.")
        else:
            print("DNI inválido.")
        dni = validar_entero("\nIngrese DNI del cliente a modificar (-1 para salir): ")
    

#VALIDACIONES DE FORMATO--------------------------------------------------------------------------------------------------
es_texto=lambda x: re.search(r'^[a-zA-Z ]+$', x)is not None
es_telefono= lambda x: re.search(r'^\d{10}$', x) is not None
es_mail= lambda x: re.search(r'\w*@gmail\.com$', x) is not None

#IMPRESIÓN DE CLIENTES----------------------------------------------------------------------------------------------------
def print_clt(archivo):
    try:
        with open(archivo, 'r', encoding="UTF-8") as data:
            clientes = json.load(data)
        clientes_ordenados_por_dni = ordenar(clientes, "dni")
        print("Tabla clientes -------------------------------------")
        print(f'{"Dni":<10}{"Nombre":<10}{"Apellido":<10}{"Teléfono":<15}{"Mail":<15}')
        for cli in clientes_ordenados_por_dni:
            print(f"{cli['dni']:<10}{cli['nombre']:<10}{cli['apellido']:<10}{cli['telefono']:<15}{cli['mail']:<15}")
    except (FileNotFoundError, OSError) as error:
        print(f"Error! {error}")
    except:
        print("Error inesperado. Intente nuevamente. ")

def opciones_busquedas_cli():
    print(f"seleccione un filtro:\n\
    1 - Todos los clientes.\n\
    2 - Busqueda por DNI.\n\
    3 - Coincidencias nombre y apellido.\n\
    4 - Ver opciones de busqueda.")

def busquedas_clientes(archivo="data/json/tabla_clientes.json"):
    opciones_busquedas_cli()
    op = validar_entero("Ingrese una opción de las disponibles. (1-4)(-1 para salir): ")

    while op not in (-1,1,2,3,4):
        op = validar_entero("Ingrese una opción de las disponibles. (1-4)(-1 para salir): ")
    
    while op != -1:
        clientes = abrir_archivo(archivo)
        match op:
            case 1:
                cadena = "Resultados de la busqueda"
                print(cadena.center(50,"-"))
                print_clt(archivo)
                print()
            case 2:
                busq_dni(clientes)
                print()
            case 3:
                coincidencias_n_y_a(clientes)
                print()
            case 4:
                opciones_busquedas_cli()
        
        op = validar_entero("Ingrese una opción de las disponibles. (1-4)(-1 para salir, 4 para ver opciones): ")

        while op not in (-1,1,2,3,4):
            op = validar_entero("Ingrese una opción de las disponibles. (1-4)(-1 para salir): ")
    
def busq_dni(clientes):
    cli = validar_entero("Ingrese el dni del cliente que desea buscar: ")
    if verificar_formato(cli):

        cli_norm = str(cli).strip()
        dnis_cli = [str(clt["dni"]).strip() for clt in clientes]

        if cli_norm in dnis_cli:
            i = dnis_cli.index(cli_norm)
            cadena = "Resultados de la busqueda"
            print(cadena.center(50,"-"))
            print(f'{"Dni":<10}{"Nombre":<10}{"Apellido":<10}{"Teléfono":<15}{"Mail":<15}')
            print(f'{str(clientes[i]["dni"]):<10}{clientes[i]["nombre"]:<10}{clientes[i]["apellido"]:<10}{str(clientes[i]["telefono"]):<15}{clientes[i]["mail"]:<15}')
        else:
            print("No existe cliente con ese DNI.")
    else:
        print("Dni invalido.")

def coincidencias_n_y_a(clientes):
    ingreso = esta_vacio("Ingrese el nombre o apellido que desea buscar: ")
    flag_ing = es_texto(ingreso)
    while not flag_ing:
        ingreso = esta_vacio("Formato Incorrecto, ingrese el nombre o apellido que desea buscar: ")
        flag_ing = es_texto(ingreso)

    patron = re.compile(ingreso.strip(), re.IGNORECASE)
    cadena = "Resultados de la busqueda"
    print(cadena.center(50,"-"))
    print(f'{"Dni":<10}{"Nombre":<10}{"Apellido":<10}{"Teléfono":<15}{"Mail":<15}')
    for cli in clientes:
        nombre = cli["nombre"]
        apellido = cli["apellido"]
        nombre_completo = f"{nombre} {apellido}"
        if (re.search(patron, nombre) or re.search(patron, apellido) or re.search(patron, nombre_completo)):
            print(f'{cli["dni"]:<10}{cli["nombre"]:<10}{cli["apellido"]:<10}{cli["telefono"]:<15}{cli["mail"]:<15}')

#ELIMINAR CLIENTES-----------------------------------------------------------------------------------------------------------
def borrar_clientes(archivo1, archivo2, mensaje):
    print_clt(archivo1)
    dni=validar_entero(f"Ingrese el dni del cliente que quiera {mensaje}r: ")
    formato=verificar_formato(dni)
    flag=1
    while flag ==1:
        flag=0
        clientes = abrir_archivo(archivo1)
        clientes_borrados = abrir_archivo(archivo2)
        dni_norm = str(dni).strip()
        dnis_cli = [str(cli["dni"]).strip() for cli in clientes]


        if dni_norm in dnis_cli:
            pos = dnis_cli.index(dni_norm)
        else: 
            pos = -1
        
        if pos!=-1 and formato:
            eliminado = clientes.pop(pos)
            clientes_borrados.append(eliminado)
            escribir_archivo(archivo1,clientes,f'El cliente {eliminado["nombre"]} {eliminado["apellido"]} ha sido {mensaje}do con éxito. ')
            escribir_archivo(archivo2, clientes_borrados,"")
            
            flag=validar_entero(f"Si desea {mensaje}r otro cliente ingrese 1, si no, ingrese 0: ")
            while flag !=1 and flag !=0:
                flag=validar_entero(f"Si desea {mensaje}r otro cliente ingrese 1, si no, ingrese 0: ")
        else:
            while pos == -1 and dni != -1:
                print("No existe cliente con ese DNI.")
                dni = validar_entero("Ingrese el DNI nuevamente (-1 para salir): ")

                if dni == -1:
                    print("Operación cancelada.")
                    return

                formato = verificar_formato(dni)
                if not formato:
                    continue

                dni_norm = str(dni).strip()
                if dni_norm in dnis_cli:
                    pos = dnis_cli.index(dni_norm)
                else:
                    pos = -1
                    print("No existe cliente con ese DNI.")
       
                    if pos!=-1:
                        eliminado = clientes.pop(pos)
                        clientes_borrados.append(eliminado)

                        escribir_archivo(archivo1,clientes,f'El cliente {eliminado["nombre"]} {eliminado["apellido"]} ha sido {mensaje}do con éxito. ')
                        escribir_archivo(archivo2, clientes_borrados,"") 

                        flag=validar_entero(f"Si desea {mensaje}r otro cliente ingrese 1, si no, ingrese 0: ")
                        while flag !=1 and flag !=0:
                            flag=validar_entero(f"Si desea {mensaje}r otro cliente ingrese 1, si no, ingrese 0: ")
                        
                        if flag == 1:
                            dni=validar_entero(f"Ingrese el dni del cliente que quiera {mensaje}r (-1 para salir): ")
                            if dni == -1:
                                print("Operación cancelada.")
                                flag = 0

#ORDENAR POR NOMBRE-----------------------------------------------------------------------------------------------------------


