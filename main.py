import os.path
from random import randint
import pokeload, movload, compationAttack
from pokeload import pokemon_base
import combatePkm

confirmation = ["y", "Y", "s", "S", "si", "Si", "SI", "sI"]
reject = ["n", "N", "no", "No", "NO", "nO"]


def database_exist(old_database):
    # caso la base de datos sea nueva ejecutaremos la funcion compare de la biblioteca compationAttack para que asi
    # puedan ser eliminados los ataques que no se encuentran en nuestra base de datos
    if not os.path.exists(movload.name_save):
        response = input("Tienes la obligacion de crear una nueva base de datos de los ataques, quieres que el propio "
                         "programa "
                         "reactive la que ya tenia?\n")
        if response in confirmation:
            # siempre un respaldo para el usuario poder usar siempre nuestra base de datos ya creada, esta se encuentra
            # en el repositorio respaldo que tengo de github
            movload.git_database()
        else:
            # el usuario crea su propio database!
            while True:
                exiting = movload.menu()
                if exiting:
                    break

    # caso sea falso...
    if not old_database:
        # accederemos a la funcion compare de comparationAttack
        compationAttack.compare()


def copy_pokemon(pokemon, pokemon_not):
    # copiar nombre en el pokemon
    pokemon["name"] = pokemon_not["name"]

    # copiar base type
    pokemon["type"] = pokemon_not["type"]

    # copiar los ataques
    number_attack = []

    # caso el pokemon no posea mas de 4
    if len(pokemon_not["attack"]) > 4:
        # cuatro ataques, tenemos que seleccionarlos
        for n in range(4):

            # creamos un numero random entre 0 y el numero maximo-1 de ataques que el pokemon posee
            number = randint(0, len(pokemon_not["attack"]) - 1)

            # si el numero esta repetido no lo sobreescribe
            if number not in number_attack:
                # guardamos el numero
                number_attack.append(number)

        for number in number_attack:
            # guardamos los ataques seleccionados
            pokemon["attack"].append(pokemon_not["attack"][number])

    else:
        pokemon["attack"] = pokemon_not["attack"]


def new_pokemon():
    # creamos la copia donde vamos a guardar al pokemon
    pokemon = pokemon_base.copy()

    # creamos la copia del pokemon real para poder editarlo y guardarlo
    pokemon_not_ready = (pokeload.give_pokemon()).copy()

    # copiamos los datos de nombre, ataques, etc
    copy_pokemon(pokemon, pokemon_not_ready)

    return pokemon


def first_pokemon_user(pokemons_user):
    pokemon = new_pokemon()
    pokemons_user.append(pokemon)
    return pokemons_user


def main():

    pokemons_user = []

    # el resultado que vamos a obtener puede ser True o False
    old_database = pokeload.get_first_generation()

    # busca las bases de datos que se encuentran en internet caso no esten descargadas en el programa
    database_exist(old_database)

    # primer pokemon usuario
    pokemons_user = first_pokemon_user(pokemons_user)

    # pokemon enemigo
    pokemon_enemy = new_pokemon()

    # iniciamos el combate pokemon
    combatePkm.combat_pkm(pokemons_user, pokemon_enemy)


if __name__ == "__main__":
    main()
