import os
import pickle
import platform
from sys import exit

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
    "infect": False,
    "auto-destruct": False,
    "damage-constant": False,
    "turn": 0,
    "damage": None,
    "type": None
}

# global variables to confirm the data

modify = ["poison", "paralize", "sleep", "restore", "confuse", "infect", "auto-destruct", "damage-constant"]
types_attack_list = ["agua", "bicho", "dragon", "electrico", "fantasma", "fuego", "hielo", "lucha", "normal", "planta",
                     "psiquico", "roca", "tierra", "veneno", "volador"]
confirmation = ["y", "Y", "s", "S", "si", "Si", "SI", "sI"]
reject = ["n", "N", "no", "No", "NO", "nO"]

name_save = "database/pickle/attfile.pkl"


# inicio de funciones
def pause():
    input("Press Enter para continuar\n")


def confirm_os():
    return platform.system()


def write_pickle(archive_name, data):  # write pickle and save in variable
    with open(archive_name, 'wb') as pokefile:
        pickle.dump(data, pokefile)


def read_pickle(archive_name):  # read pickle and return in variable
    list_pokemon = []

    try:
        with open(archive_name, 'rb') as pokefile:
            list_pokemon = pickle.load(pokefile)

        return list_pokemon
    except FileNotFoundError:
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
    data = read_pickle(name_save)
    name = input("Escribe el nombre del elemento a eliminar:\n")
    for i, one_data in enumerate(data):
        if one_data["name"] == name:
            del data[i]

    write_pickle(name_save, data)


def new_moviment():
    # lista donde vamos a guardar los datos
    changes = []

    new_attack = moviment_base.copy()
    name = input("Nombre ataque:\n")
    typee = input("Tipo ataque:\n")
    damage = input("Daño del ataque:\n")
    state = input("Tiene cambios de estado?\n")
    while state in confirmation:
        change = input("Dime el cambio! (Comando 'help' para escribir en el terminal los cambios)\n")
        if change == 'help':
            print("Los cambios que pueden ser aplicados son:\n"
                  f"{modify}")
        if change in modify:
            changes.append(change)

        state = input("Mas cambios?\n")

    new_attack["name"] = name
    new_attack["type"] = typee
    new_attack["damage"] = damage
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
    data = read_pickle(name_save)
    confirm = False
    name = input("Escribe el nombre del ataque a editar:\n")
    change = int(input("Que quieres editar?\n"
                       "1. Nombre\n"
                       "2. Tipo\n"
                       "3. Daño\n"))
    new_data = input("Escribe el nuevo dato:\n")
    for i, one_data in enumerate(data):
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
        write_pickle(name_save, data)


def delete_all_database():  # the function delete the data in a pickle
    response = input("Quieres eliminar la base de datos actual?\n")
    if response in confirmation:
        response = input("Escribe el codigo para eliminar toda la base de datos:\n")
        if response == '1309':
            if os.path.exists(name_save):
                os.remove(name_save)
        else:
            print("!!!!!!!!!!Error!!!!!!!!!!")
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
                             "6. Cerrar programa\n"))

        match response:
            case 1:
                see_database()
            case 2:
                delete_a_move()
            case 3:
                new_moviment()
            case 4:
                edit_move()
            case 5:
                delete_all_database()
            case 6:
                print("close program!\n")
                exit()
            case _:
                print("Error al introducir instrucciones\n")

        pause()


menu()
