from listas_codeadas import *
import json

def login():
    print("----Login-----")
    user = input("Usuario (admin o DNI): ").strip()
    pwd  = input("Contraseña: ").strip()

    pos = -1
    i = 0
    while i < len(usuarios) and pos == -1:
        if usuarios[i][0] == user and usuarios[i][1] == pwd:
            pos = i
        else:
            i += 1

    if pos == -1 and user.isdigit():
        dni = int(user)
        existe = False

        try:
            with open("data/json/tabla_clientes.json", "r", encoding="UTF-8") as f:
                clientes = json.load(f)
                if clientes is None:
                    clientes = []
        except:
            clientes = []

        j = 0
        while j < len(clientes) and not existe:
            if str(clientes[j]["dni"]).strip() == str(dni).strip():
                existe = True
            else:
                j += 1

        if existe:
            print("Bienvenido Cliente.")
            return "cliente", dni

    while pos == -1:
        print("Usuario o contraseña incorrectos.")
        user = input("Usuario (admin o DNI): ").strip()
        pwd  = input("Contraseña: ").strip()

        pos = -1
        i = 0
        while i < len(usuarios) and pos == -1:
            if usuarios[i][0] == user and usuarios[i][1] == pwd:
                pos = i
            else:
                i += 1

        if pos == -1 and user.isdigit():
            dni = int(user)
            existe = False

            try:
                with open("data/json/tabla_clientes.json", "r", encoding="UTF-8") as f:
                    clientes = json.load(f)
                    if clientes is None:
                        clientes = []
            except:
                clientes = []

            j = 0
            while j < len(clientes) and not existe:
                if str(clientes[j]["dni"]).strip() == str(dni).strip():
                    existe = True
                else:
                    j += 1

            if existe:
                print("Bienvenido Cliente.")
                return "cliente", dni

    rol_txt = usuarios[pos][2].lower()
    dni_login = int(user) if rol_txt == "cliente" and user.isdigit() else None

    print(f"Bienvenido {rol_txt.title()}.")
    return rol_txt, dni_login
