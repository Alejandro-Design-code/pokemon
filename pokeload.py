from bs4 import BeautifulSoup
import requests
import pickle
from os import system, makedirs
from random import randint


# variables de acceso a internet
URL = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/pkmn&pk="
URL_IMAGES_INIT = "https://www.pokexperto.net/nds/artwork/"
URL_IMAGES_FINISH = ".jpg"
URL_MOVIMENTS = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_pokemon&pk="

# varible de numero de evoluciones por pokemon
GLOBAL_NUMBER_EVOLUTIONS = -1

first_generation = []

# diccionario de los pokemon
pokemon_base = {
    "name": "",
    "base_health": 100,
    "current_health": 100,
    "lvl": 10,
    "evolution": [],
    "current_exp": 0,
    "base_exp": 10,
    "type": None,
    "attack": []
}

# diccionario de los movimientos
movement_base = {
    "name": "",
    "type": None,
    "power": ""
}


# funcion encargada de leer datos de los pokemons de la base de datos
def read_database(archive_name):
    list_pokemon = []
    with open(archive_name, 'rb') as pokefile:
        list_pokemon = pickle.load(pokefile)

    print("Pokemons cargados de la base de datos")
    return list_pokemon


# escribir datos de los pokemons en la base de datos
def write_database(archive_name, data):
    with open(archive_name, 'wb') as pokefile:
        pickle.dump(data, pokefile)

    print("Pokemons guardados en la base de datos")


# funcion usada unicamente para preparacion; se usa para poder imprimir mejor la lista de pokemon
def test_print_pokemon(all_pokemon):
    for pokemon in all_pokemon:
        print(f"{pokemon}")


# funcion usada para poder iniciar sesion en la página y su codigo HTML
def get_session(index, url_argument):
    session = requests.get(f"{url_argument}{index}")
    html_content = session.text
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


# esta funcion es llamada para poder extraer el nombre del pokemon de la pagina
def get_name_pokemon(soup):
    name_pokemon = soup.find(class_="container").find(class_="scroller-inner").find(class_="mini").text
    return name_pokemon


# esta funcion es llamada para poder extraer el tipo de pokemon
def get_type_pokemon(soup):
    images = soup.find(class_="scroller-inner").find(class_="pkmain").find(class_="bordeambos").find_all('img')
    # accedemos a todas las etiquetas 'img' que es donde se encuentran los tipos
    type_pokemon = []
    for image in images:
        type_pokemon.append(image['alt'])
        # accedemos a los atributos 'alt' que se encuentra en cada imagen cuyo valor es los tipos del pokemon

    return type_pokemon


# esta funcion extrae el nombre de todos los ataques que el pokemon puede aprender
def get_name_attack(data):
    all_moviment = []
    for bordetodos_data in data:
        check_bazul_data = bordetodos_data.find_all('tr', class_="check3 bazul")
        for nowrap_data in check_bazul_data:
            all_moviment.append(nowrap_data.find(class_="nav6c").text)

    return all_moviment


"""
def get_type_attack_pokemon(attack_pokemon, data):
    type_pokemon = []
    for bordetodos_data in data:
        check_bazul_data = bordetodos_data.find_all(class_="check3 bazul")
        for centers in check_bazul_data:
            elements = centers.find('td', attrs={'sorttable_customkey': True})
            type_pokemon.append(elements.get('sorttable_customkey'))

    counter = 0
    for one_attack in attack_pokemon:
        one_attack["type"] = type_pokemon[counter]
        counter += 1

    return attack_pokemon

"""


# esta funcion es usada para poder saber cuando los pokemons van a poder evolucionar
def get_evolutions(soup):
    global GLOBAL_NUMBER_EVOLUTIONS
    evolutions = []
    center = soup.find(class_="scroller-inner").find(class_="pkmain").find_all(class_="bordeambos")
    counter = 0
    have_evolution = False
    for bordeambos in center:           # este paso es para descubrir en que bordeambos esta la evolucion
        if "Nivel" in str(bordeambos):
            have_evolution = True
            break
        counter += 1

    if have_evolution:
        data = center[counter].find_all('td', string=lambda text: text and "Nivel")
        if GLOBAL_NUMBER_EVOLUTIONS == -1:
            GLOBAL_NUMBER_EVOLUTIONS = 0
            for evolution in data:
                if "Nivel" in evolution.text:
                    GLOBAL_NUMBER_EVOLUTIONS += 1
                    evolutions.append(int(evolution.text.split()[1]))   # guardamos todas las evoluciones en el array
        elif GLOBAL_NUMBER_EVOLUTIONS == 1:
            for evolution in data:
                if "Nivel" in evolution.text:
                    evolutions.append(int(evolution.text.split()[1]))   # guardamos todas las evoluciones en el array

            evolutions.pop(0)

        if GLOBAL_NUMBER_EVOLUTIONS >= 0:
            GLOBAL_NUMBER_EVOLUTIONS -= 1

        return evolutions
    else:
        GLOBAL_NUMBER_EVOLUTIONS = -1
        return evolutions


# inicio de session para poder obtener todos los ataques de un pokemon
# esta funcion puede no ser necesaria porque la funcion get_name_attack() podria hacer esto
def get_attack_pokemon(index):
    soup = get_session(index, URL_MOVIMENTS)
    data = soup.find_all('td', class_="bordetodos")
    attack_pokemon = get_name_attack(data)

    return attack_pokemon


# esta funcion lo que hace es descargar la imagen que corresponde al pokemon y tambien guardarla en una carpeta
def get_image_pokemon(index):
    session = requests.get(f"{URL_IMAGES_INIT}{index}{URL_IMAGES_FINISH}", stream=True)

    if session.status_code == 200:
        makedirs("database/images", exist_ok=True)

        with open(f"database/images/{index}.jpg", 'wb') as image:
            for chunk in session.iter_content(1024):
                image.write(chunk)


# descarga la informacion de un pokemon en especifico, despues va a ser llamada para descargar los datos de todos los
# pokemons que sean necesarios
def get_data_one_pokemon(index):

    # excluir los siguientes pokemons
    exclude_pkm = ["Magmar", "Jynx", "Electabuzz", "Snorlax", "Gastly", "Golem"]

    # iniciamos la pagina para buscar los datos pkm
    soup = get_session(index, URL)
    pokemon = pokemon_base.copy()

    # comprobacion que el pokemon no tiene preevoluciones en generaciones siguientes
    name_pokemon = get_name_pokemon(soup)

    if name_pokemon not in exclude_pkm:

        # extraemos los datos de los pokemon por separado
        pokemon["name"] = name_pokemon
        pokemon["type"] = get_type_pokemon(soup)
        pokemon["attack"] = get_attack_pokemon(index)
        pokemon["evolution"] = get_evolutions(soup)
        return pokemon

    else:
        return None


# esta funcion se encarga de conseguir un pokemon de manera aleatoria para poder usarlo en los combates y como
# primer pokemon
def give_pokemon():

    global first_generation
    # indice para conseguir un pokemon
    index = randint(0, len(first_generation)-1)
    pokemon = first_generation[index]
    return pokemon


# esta funcion es para extrar los pokemons de la primera generacion usando en ciclo la funcion anterior
def get_first_generation():

    # variable para comprobar si fue leida la base de datos; esto afectara en gran medida el funcionamento del programa
    lecture = False

    # funcion que va a llamar al resto para obtener todos los datos de los pokemons, vida, nombre, index, ataques, etc.
    global first_generation
    try:
        first_generation = read_database("database/pickle/pokefile.pkl")
        lecture = True
    except FileNotFoundError:
        index_first_generation = 151            # primera generacion hasta 151
        makedirs('database/pickle', exist_ok=True)
        for index_pokemon in range(1, index_first_generation+1):

            # descargar imagenes
            get_image_pokemon(index_pokemon)

            porcentaje = round(index_pokemon * 100 / index_first_generation)
            system('clear')
            print(f"En este momento nos encontramos al {porcentaje}% del proceso")
            pokemon = get_data_one_pokemon(index_pokemon)
            if pokemon is not None:
                first_generation.append(pokemon)

        write_database("database/pickle/pokefile.pkl", first_generation)

    # al retornar lecture sabremos si fue leida la base de datos o no!
    return lecture
