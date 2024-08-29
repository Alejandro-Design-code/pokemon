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
            # siempre un respaldo para el usuario poder usar siempre nuestra base de datos ya creada, esta se encuentra
            # en el repositorio respaldo que tengo de github
            movload.git_database()
        else:
            # el usuario crea su propio database!
            while True:
                exiting = movload.menu()
                if exiting:
                    break

    if not old_database:
        compationAttack.compare()


if __name__ == "__main__":
    main()
