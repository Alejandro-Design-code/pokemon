from movload import read_pickle
from pokeload import read_database, write_database

# usado en read_pickle
name_save_pickle = "database/pickle/att.pkl"

# usado en read_database
name_save_database = "database/pickle/pokefile.pkl"


# vamos a necesitar que nos envien a la funcion la variable first_generation donde se encontraran todos los datos de los
# pkm
def receive_attack_pokeload(list_of_name):
    # esta lista tendrá la funcion de almacenar los ataques que los pokemon pueden aprender sin excluir nada
    all_attack = []

    # esta variable tiene la funcion de contar la posicion del pokemon para asi poder reescribir los datos de este
    count = 0

    # esta variable la usaremos para eliminar los ataques que no se encuentren en la lista; tendra los ataques en ella

    # importamos la lista desde pokeload
    # lo que estamos importando son todos los pokemons con cada una de sus informaciones, incluyendo los ataques
    pkm = read_database(name_save_database)

    # separamos cada pokemon de la lista
    for one_pokemon in pkm:
        # guardados para cuando acabemos la fase de recoleccion lo siguiente sera eliminarlos
        delete_attack = []
        # esta variable tendra todos y cada uno de los ataques que los pkm pueden aprender sin excluir nada! Por eso
        # tendremos que almacenar todos y cada uno de los datos con un append para despues se puedan eliminar!
        for single_attack in one_pokemon["attack"]:
            # guardamos los ataques que se encuentran en nuestra base de datos movload
            if single_attack not in list_of_name:
                # agregamos a la lista el ataque que vamos a eliminar
                delete_attack.append(single_attack)

        # este ciclo for se encargara de eliminar todos los ataques de la lista
        for single_attack in delete_attack:
            one_pokemon["attack"].remove(single_attack)
            if not one_pokemon["attack"]:
                break
        count += 1

    # ahora podemos retornar esta lista para trabajarla en la funcion que tendra los datos a excluir
    # la lista que retornamos contiene todos los ataques de todos los pokemones

    write_database(name_save_database, pkm)


# en esta funcion tendran que enviarnos la base de datos cargada sin ninguna modificacion
def receive_attack_movload():
    list_of_names = []

    # import data de movload
    # importamos los ataques guardados en la base de datos de movload
    information = read_pickle(name_save_pickle)

    # vamos acceder a cada dato para despues poder acceder a cada nombre y guardarlo
    for one_data in information:
        # guardamos en la siguiente lista los nombres de todos los ataques
        list_of_names.append(one_data["name"])

    # retornamos la lista de los ataques
    return list_of_names


# necesitaremos el size de la variable data para con esto poder modificar cada movimiento

# funcion de testeo
def compare():
    # en resumen: se encarga de extraer todos los nombres de los ataques que se encuentran en la base de datos de
    # ataques, esto tendrá un uso en la funcion a seguir
    list_of_names = receive_attack_movload()
    # se encarga de eliminar en la lista de pokemons los ataques que no se encuentran en la lista de ataques. Estas
    # funciones ya sobreescriben en las bases de datos para poder ser accedidos en otras bibliotecas
    receive_attack_pokeload(list_of_names)


#compare()
