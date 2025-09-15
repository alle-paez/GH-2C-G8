from listas_codeadas import usuarios

def login():
    print("----Login-----")
    user = input("Usuario (admin o DNI): ").strip()
    pwd  = input("Contraseña: ").strip()

    i = 0
    pos = -1
    while i < len(usuarios) and pos == -1:
        if usuarios[i][0] == user and usuarios[i][1] == pwd:
            pos = i
        else:
            i += 1

    while pos == -1:
        print("Usuario o contraseña incorrectos.")
        user = input("Usuario (admin o DNI): ").strip()
        pwd  = input("Contraseña: ").strip()
        i = 0
        pos = -1
        while i < len(usuarios) and pos == -1:
            if usuarios[i][0] == user and usuarios[i][1] == pwd:
                pos = i
            else:
                i += 1

    rol_txt = usuarios[pos][2].lower()  # "admin" o "cliente"
    dni_login = int(user) if rol_txt == "cliente" and user.isdigit() else None

    print(f"Bienvenido {rol_txt.title()}.")
    return rol_txt, dni_login
