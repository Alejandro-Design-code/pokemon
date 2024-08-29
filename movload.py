import os
import pickle
import platform
from sys import exit
import requests

# datos para la creacion del programa, como estructuras

# dicionario

moviment_base = {
    "name": "",
    "poison": False,
    "paralize": False,
    "sleep": False,
    "restore": False,
    "live-restore": 0,
    "confuse": False,
    "auto-destruct": False,
    "damage-constant": False,
    "turn": 0,
    "damage": None,
    "type": None
}

# global variables to confirm the data

modify = ["poison", "paralize", "sleep", "restore", "confuse", "auto-destruct", "damage-constant"]
types_attack_list = ["agua", "bicho", "dragon", "electrico", "fantasma", "fuego", "hielo", "lucha", "normal", "planta",
                     "psiquico", "roca", "tierra", "veneno", "volador"]
confirmation = ["y", "Y", "s", "S", "si", "Si", "SI", "sI"]
reject = ["n", "N", "no", "No", "NO", "nO"]

# Tuvimos un problema al tener el programa con el .exe y el .py. Cuando tenemos el programa en .py
# nuestro address tiene que ser:
# 'database/pickle/att.pkl'
# Cuando el programa es .exe tenemos que tener el siguiente address:
# 'Documents/Python/databases/pickle/att.pkl'
# esto es para que la carpeta de databases sea creada en la carpeta Python

directory = "database/pickle/"
name_save = "database/pickle/att.pkl"
file_name = "att.pkl"
path_github = "https://github.com/Alejandro-Design-code/pokemon/raw/main/database/pickle/att.pkl"

# inicio de funciones


def pause():
    input("Press Enter para continuar\n")


def git_database():
    with requests.get(path_github, stream=True) as data:
        data.raise_for_status()
        with open(name_save, 'wb') as pokefile:
            pokefile.write(data.content)


def formater(word):

    # transformamos la string en minusculas
    word = str.lower(word)

    # guardamos la primera letra de la string
    letter = word[0]

    # transformamos la letra en mayuscula
    letter = str.upper(letter)

    # guardamos la nueva palabra cuya primera letra es mayus y el resto es minus
    word = letter + word[1:]

    return word


def confirm_os():
    return platform.system()


def write_pickle(archive_name, data):  # write pickle and save in variable

    # caso no exista el directorio se crea
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    # creamos el documento de la base de datos y guardamos la informacion
    with open(archive_name, 'wb') as pokefile:
        pickle.dump(data, pokefile)


def read_pickle(archive_name):  # read pickle and return in variable

    # intentaremos cargar los datos de la base de datos cuya localizacion es arquive_name
    try:
        with open(archive_name, 'rb') as pokefile:
            list_pokemon = pickle.load(pokefile)

        # retornamos lista cargada en el documento
        return list_pokemon
    except FileNotFoundError:

        # no retorna nada porque no encuentró la lista o no existe esta.
        return []


def important_database(data):
    organization = {
        "name": "",
        "type": "",
        "damage": None
    }

    important_data = []
    for one_data in data:
        # prepare information to print
        data_prepare = organization.copy()
        data_prepare["name"] = one_data["name"]
        data_prepare["type"] = one_data["type"]
        data_prepare["damage"] = one_data["damage"]

        # save information
        important_data.append(data_prepare)

    return important_data


def see_database():
    data = read_pickle(name_save)
    important_data = important_database(data)
    if not important_data:
        print("No hay datos almacenados!\n")
    else:
        print("Los datos almacenados en la base de datos son:")
        for one_data in important_data:
            print(one_data)

        response = input("Desea ver los datos mas complejos?\n")
        if response in confirmation:
            print("Los datos almacenados en la base de datos son:")
            for one_data in data:
                print(one_data)


def delete_a_move():

    # extraemos los datos de la base de datos
    data = read_pickle(name_save)

    # recibimos el nombre del ataque del cual estamos interesados a eliminar, recordar que el formateo es necesario para
    # poder trabajar en la base de datos
    name = input("Escribe el nombre del elemento a eliminar:\n")
    name = formater(name)

    # vamos a navegar en la base de datos en busca del dato que tenga el nombre en específico para poder eliminarlo
    for i, one_data in enumerate(data):
        if one_data["name"] == name:
            del data[i]

    # guardamos los datos en la base de datos para no perder las modificaciones
    write_pickle(name_save, data)


def new_moviment():
    # lista donde vamos a guardar los datos
    changes = []

    # inicializacion de variables (necesarias)
    typee = None

    # copia de formato de ataque
    new_attack = moviment_base.copy()

    # recibir nombre
    name = input("Nombre ataque:\n")
    name = formater(name)

    # recibir tipo del ataque
    while typee not in types_attack_list:
        typee = input("Tipo ataque:\n")
    typee = formater(typee)

    # recibir el daño del ataque
    damage = input("Daño del ataque:\n")

    # recibir el estado del ataque
    state = input("Tiene cambios de estado?\n")

    # guardaremos los cambios de estado que vamos a modificar
    while state in confirmation:
        change = input("Dime el cambio! (Comando 'help' para escribir en el terminal los cambios)\n")
        if change == 'help':
            print("Los cambios que pueden ser aplicados son:\n"
                  f"{modify}")
        if change in modify:
            changes.append(change)
            state = input("Mas cambios?\n")

    # guardando datos en la copia del diccionario
    new_attack["name"] = name
    new_attack["type"] = typee
    new_attack["damage"] = damage

    # modificamos los cambios de estado en la lista
    for change in changes:
        new_attack[change] = True
        if change == 'restore':
            restore = int(input("Cuanto restaura?\n"))
            new_attack["restore"] = restore
        elif change == 'damage-constant':
            damage_constant = int(input("Cuanto daño constante hace?\n"))
            new_attack["damage-constant"] = damage_constant

    data = read_pickle(name_save)
    data.append(new_attack)
    write_pickle(name_save, data)


def edit_move():

    # carregamos datos da base de datos
    data = read_pickle(name_save)

    # varible para  (...)
    confirm = False

    # vamos confirmar recibir el nombre para poder buscar el ataque
    name = input("Escribe el nombre del ataque a editar:\n")

    # preguntamos el dato que se quiere editar
    change = int(input("Que quieres editar?\n"
                       "1. Nombre\n"
                       "2. Tipo\n"
                       "3. Daño\n"))

    # escribimos el dato correcto, este se substituira en la porcion de dato que esté mal o se quiera editar
    new_data = input("Escribe el nuevo dato:\n")

    # el for que se encuentra en la siguiente linea se encarga de separar todos los datos que se encuentran en la varia-
    # ble 'data', de todos los datos en la variable data buscara la que corresponde a los nombres; la funcion enumerate
    # se encarga de ir contando el numero de variables que ya han pasado por el ciclo for, es decir, supongamos que en
    # la lista se encuentran los siguientes datos (de una manera muy resumida):
    # one_data[0] = 'Carlos' -> variable i correspondiente con i = 0
    # one_data[1] = 'Antonio' -> variable i correspondiente con i = 1
    # onde_data[2] = 'Juan' -> variable i correspondiente con i = 2
    for i, one_data in enumerate(data):

        # cuando el nombre de la varible one_data sea identica al nombre que fue introducido por el usuario en ese
        # en ese momento modificaremos la variable confirm como True para identificar que existe el nombre y que si fue
        # modificado el archivo, caso no sea modificado esta variable se mantendra como False resultando en un mensaje
        # del programa que indique que no se pudieron modificar los datos.
        if one_data["name"] == name:
            confirm = True
            del data[i]
            match change:
                case 1:
                    one_data["name"] = new_data
                case 2:
                    if new_data in types_attack_list:
                        one_data["type"] = new_data
                    else:
                        confirm = False
                case 3:
                    one_data["damage"] = int(new_data)
            data.append(one_data)
    if not confirm:
        print("No se pudo modificar el archivo!")
    else:
        # guardar los datos modificados en la base de datos, únicamente guardaremos si los datos fueron realmente modi-
        # ficados por el programa, esto se sabrá gracias a la varible de tipo boolean que se llama confirm
        write_pickle(name_save, data)


def delete_all_database():  # the function delete the data in a pickle

    # confirmaremos con el usuario si se desea eliminar la base de datos!
    response = input("Quieres eliminar la base de datos actual?\n")

    # tenemos una lista con las posibles respuestas afirmativas, con esta determinaremos si el usuario quiere de verdad
    # proceder
    if response in confirmation:
        # pediremos al usuario un código que se encuentra únicamente en el programa, viene este predefinido y no puede
        # modificarse
        response = input("Escribe el codigo para eliminar toda la base de datos:\n")

        # caso el codigo de seguridad sea correcto accederemos dentro del ciclo if para poder continuar con la elimina-
        # ción de la base de datos
        if response == '1309':
            if os.path.exists(name_save):
                os.remove(name_save)
        else:
            print("!!!!!!!!!!Error!!!!!!!!!!")

            # tenemos que identificar que tipo de sistema operativo nos encontramos trabajando, el sistema operativo de
            # el pc en el que me encuentro es mac
            so = confirm_os()
            if so == "Windows":
                os.system('pause')
            else:
                input("Enter para continuar")
            exit()


def menu():
    # função que imprime no terminal as opções para trabalhar o programa
    response_chose = [1, 2, 3, 4, 5, 6]
    response = None
    while True:
        os.system('clear')
        response = int(input("1. Mostrar base de datos\n"
                             "2. Eliminar un movimiento\n"
                             "3. Agregar nuevo movimiento\n"
                             "4. Editar movimiento\n"
                             "5. Eliminar toda la base de datos\n"
                             "6. Cerrar el creador de database\n"
                             "7. Cerrar programa\n"))

        # corresponde a un switch del lenguaje C y C++, con este podremos acceder a cada caso que nos sea identificado
        # en la variable response; cada número a la izquierda de la opcion en el menu corresponde a cada una de las op-
        # ciones aqui abajo
        match response:
            # Mostrar base de datos
            case 1:
                see_database()
            # Eliminar un movimiento
            case 2:
                delete_a_move()
            # Agregar nuevo movimiento
            case 3:
                new_moviment()
            # Editar movimiento
            case 4:
                edit_move()
            # Eliminar toda la base de datos
            case 5:
                delete_all_database()
            # Cerrar programa
            case 6:
                break
            case 7:
                print("close program!\n")
                exit()
            # este toma en cuenta cualquier otra opcion que sea introducida por el usuario
            case _:
                print("Error al introducir instrucciones\n")

        pause()

    return True

# recordar comentar el menu() porque sino no se puede testear en otras funciones
#menu()
