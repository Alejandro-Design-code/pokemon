import os

creator_user = 'cf'
my_diretory = "Documents/Bases de datos"
another_diretory = "Documents/Pokemon"


def give_user():
    name_user = os.getlogin()
    return name_user


def compare_user():
    you_are_creator = False
    if give_user() == creator_user:
        you_are_creator = True

    return you_are_creator


def create_path_database():
    path_database = None
    if compare_user():
        path_database = os.path.expanduser("~")
        path_database = os.path.join(path_database, my_diretory)
    else:
        path_database = os.path.expanduser("~")
        path_database = os.path.join(path_database, another_diretory)

    return path_database
