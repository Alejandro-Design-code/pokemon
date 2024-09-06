from os import system


def select_pokemon_user(pokemons_user):
    # empezamos con un caso imposible
    response = -1

    # entramos en el ciclo while porque el caso es imposible
    while response >= len(pokemons_user) or response < 0:

        # comenzamos con un clear para limpiar la pantalla
        system('clear')

        # comenzamos con la seleccion de todos los pokemons del usuario
        print("Selecciona tu pokemon:\n")

        # mostramos el indice del pokemon junto con su nombre
        for index, name in enumerate(pokemons_user):
            print(f"{index}. {name["name"]}")

        # pedimos al usuario que pokemon quiere usar
        response = int(input())

    return pokemons_user[response]


def my_pkm_defeat():
    pass


def select_my_attack(pokemon):
    correct_answer = [0, 1, 2, 3]
    response = -1
    while response not in correct_answer:
        print(f"Selecciona un ataque:\n"
              f"0. ")

def combat_pkm(pokemons_user, pokemon_enemy):

    # seleccionamos el pokemon del usuario
    select_pkm = select_pokemon_user(pokemons_user)

    # mientras la vida de mi pokemon o el adversario no sea 0 no se acaba el combate
    while select_pkm["current_health"] > 0 or pokemon_enemy["current_health"]:
        #while
        pass


