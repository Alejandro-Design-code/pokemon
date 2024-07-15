import pickle
from sys import exit
from os import remove

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
    "damage": True,
    "type": None
}

# global variables to confirm the data

modify = ["poison", "paralize", "sleep", "restore", "confuse", "infect", "auto-destruct", "damage-constant"]
types_attack_list = ["agua", "bicho", "dragon", "electrico", "fantasma", "fuego", "hielo", "lucha", "normal", "planta"
                     "psiquico", "roca", "tierra", "veneno", "volador"]
confirmation = ["y", "Y", "s", "S", "si", "Si", "SI", "sI"]
reject = ["n", "N", "no", "No", "NO", "nO"]

name_save = "database/pickle/attfile.pkl"

# inicio de funciones


def transform_name_in_minus(name):                  # funtion to transform a word to minus
    name = name.lower()
    return name


def show_data_save(attack, list_of_attack):                         # show data before to send inside the database
    print("Seguro que quieres guardar el ataque?\n"
          "Aqui la descripcion:\n")

    keys = []
    for key in attack.keys():
        keys.append(key)

    data = []
    for value in attack.values():
        data.append(value)

    for i in range(len(data)):
        print(f"{keys[i]}= {data[i]}")

    response = input("save?\n")
    if response in confirmation:
        list_of_attack.append(attack)  # save data in array

    return list_of_attack


def take_name():                                    # function to receive de name of attack
    name = input("Dime el nombre del ataque: ")
    return name


def take_damage():                                  # function to receive the damage
    damage = input("Dime el daño del ataque (si el ataque no hace daño escribe '--' o escribe 0): ")

    if damage == '--':
        damage = 0
    else:
        damage = int(damage)

    return damage


def take_type():                                    # function to receive the type of the attack
    type_attack = None
    while type_attack not in types_attack_list:
        type_attack = input("Dime el tipo del ataque: ")        # receive the type attack
        type_attack = transform_name_in_minus(type_attack)      # transform the name to lower

    return type_attack


def take_change_state(attack):                      # change in the state to the movement
    change_state = input("El ataque tiene algun cambio de estado?\n")
    while change_state in confirmation:
        state = input("Dime el estado a cambiar: ")
        if state in modify:
            attack[state] = not attack[state]
        else:
            print("Error!!\n")

        change_state = input("Otro estado?\n")

    return attack


def write_pickle(archive_name, data):               # write pickle and save in variable

    with open(archive_name, 'wb') as pokefile:
        pickle.dump(data, pokefile)

    print("Attack save in database")

    print("Cerrando programa!!")
    exit()


def read_pickle(archive_name):                      # read pickle and return in variable
    list_pokemon = []

    response = input("Quieres cargar la base de datos?\n")
    if response in confirmation:
        try:
            with open(archive_name, 'rb') as pokefile:
                list_pokemon = pickle.load(pokefile)

            print("attack load in database")
            return list_pokemon
        except FileNotFoundError:
            print("Error to load database")
            exit()
    else:
        print("No load attack")
        return []


def show_data_base(archive_name):                   # see the database in pickle
    response = input("Quieres ver la lista?\n")
    if response in confirmation:
        list_attack = read_pickle(archive_name)
        print(f"La lista de ataques guardado es:\n{list_attack}")


def save_data_base(archive_name, list_of_attack):
    response = input("Quieres guardar en la base de datos?\n")
    if response in confirmation:
        write_pickle(archive_name, list_of_attack)


def delete_database(archive_name):                  # the function delete the data in a pickle
    response = input("Quieres eliminar la base de datos actual?\n")
    if response in confirmation:
        remove(archive_name)
        print(f"El archivo guardado: {archive_name} fue eliminado")


def take_data():
    show_data_base(name_save)
    list_of_attack = read_pickle(name_save)

    while True:
        attack = moviment_base.copy()
        attack["name"] = take_name()                                    # variable receive the data
        attack["damage"] = take_damage()                                # variable receive the data
        attack["type"] = take_type()                                    # variable receive the data
        attack = take_change_state(attack)                              # actualizate the data
        list_of_attack = show_data_save(attack, list_of_attack)         # show the create data
        show_data_base(name_save)                                       # see array of data
        save_data_base(name_save, list_of_attack)


take_data()
