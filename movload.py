import pickle

# datos para la creacion del programa, como estructuras

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

modify = ["poison", "paralize", "sleep", "restore", "confuse", "infect", "auto-destruct", "damage-constant"]
types_attack_list = ["agua", "bicho", "dragon", "electrico", "fantasma", "fuego", "hielo", "lucha", "normal", "planta"
                     "psiquico", "roca", "tierra", "veneno", "volador"]
confirmation = ["y", "Y", "s", "S", "si", "Si", "SI", "sI"]
reject = ["n", "N", "no", "No", "NO", "nO"]


# inicio de funciones

def transform_name_in_minus(name):          # funtion to transform a word to minus
    name = name.lower()
    return name


def show_data_save(attack):
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


def take_name():                            # function to receive de name of attack
    name = input("Dime el nombre del ataque: ")
    return name


def take_damage():                          # function to receive the damage
    damage = input("Dime el daño del ataque (si el ataque no hace daño escribe '--' o escribe 0): ")

    if damage == '--':
        damage = 0
    else:
        damage = int(damage)

    return damage


def take_type():                            # function to receive the type of the attack
    type_attack = None
    while type_attack not in types_attack_list:
        type_attack = input("Dime el tipo del ataque: ")        # receive the type attack
        type_attack = transform_name_in_minus(type_attack)      # transform the name to lower

    return type_attack


def take_change_state(attack):
    change_state = input("El ataque tiene algun cambio de estado?\n")
    while change_state in confirmation:
        state = input("Dime el estado a cambiar: ")
        if state in modify:
            attack[state] = not attack[state]
        else:
            print("Error!!\n")

        change_state = input("Otro estado?\n")

    return attack


def take_data():
    list_of_attack = []

    while True:
        attack = moviment_base.copy()
        attack["name"] = take_name()                # variable receive the data
        attack["damage"] = take_damage()            # variable receive the data
        attack["type"] = take_type()                # variable receive the data
        attack = take_change_state(attack)          # actualizate the data
        show_data_save(attack)                      # show the create data

        list_of_attack.append(attack)

take_data()
