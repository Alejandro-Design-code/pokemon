import os.path
import pokeload, movload, compationAttack

confirmation = ["y", "Y", "s", "S", "si", "Si", "SI", "sI"]
reject = ["n", "N", "no", "No", "NO", "nO"]


def main():
    old_database = pokeload.get_first_generation()

    # caso la base de datos sea nueva ejecutaremos la funcion compare de la biblioteca compationAttack para que asi
    # puedan ser eliminados los ataques que no se encuentran en nuestra base de datos
    if not os.path.exists(movload.name_save):
        response = input("Tienes la obligacion de crear una nueva base de datos de los ataques, quieres que el propio "
                         "programa "
                         "reactive la que ya tenia?\n")
        if response in confirmation:
            # tenemos que tener la funcion que tenga en si almacenada nuestra propia base de datos! Con esto tendriamos
            # siempre un respaldo para el usuario poder usar siempre nuestra base de datos;
            # otra opcion es que se encargue el solo de descargar la base de datos de la web!
            movload.git_database()

        movload.menu()
    if not old_database:
        compationAttack.compare()


if __name__ == "__main__":
    main()
