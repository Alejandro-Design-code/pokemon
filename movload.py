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
types_attack_list = ["Agua", "Bicho", "Dragon", "Electrico", "Fantasma", "Fuego", "Hielo", "Lucha", "Normal", "Planta"
                     "Psiquico", "Roca", "Tierra", "Veneno", "Volador"]


# inicio de funciones

def take_name():
    name = input("Dime el nombre del ataque: ")
    return name


def take_damage():
    damage = input("Dime el daño del ataque (si el ataque no hace daño escribe '--' o escribe 0): ")

    if damage == '--':
        damage = 0

    return damage


def take_type():
    type_attack = input("Dime el tipo del ataque: ")
    return type_attack


def take_data():
    count = 0
    list_of_attack = []

    while True:
        count += 1
        attack = moviment_base.copy()
        attack["name"] = take_name()
        attack["damage"] = take_damage()
        attack["type"] = take_type()

        change_state = input("El ataque tiene algun cambio de estado?\n")
        while change_state == "si" == "s" == "SI" == "Si":
            state = input("Dime el estado a cambiar: ")
            if state in types_attack_list:
                attack[state] = not attack[state]
                change_state = input("Otro estado?")

        list_of_attack.append(attack)

        if count == 5:
            break

    print(list_of_attack)


take_data()
