from .erreurs import *
from .entiers import entier
from .decimaux import decimal
from .chaines import chaine
from typing import List, Tuple
from .fonctions import *


def distance(*args) -> tuple:
    """Remplacement de la fonction range"""
    res = []
    if len(args) > 3:
        raise ErreurArguments(
            "La fonction a été appelée avec trop d arguments")
    elif len(args) == 0:
        raise ErreurArguments("La fonction nécessite au moins 1 argument")

    for v in args:
        if not isinstance(v, (int, entier)):
            raise TypeInconnu("Les arguments doivent etre des entiers")

    a = 0
    max = args[0]
    pas = 1

    if len(args) != 1:
        a = args[0]
        max = args[1]

    if len(args) == 3:
        pas = args[2]

    while a != max:
        res.append(a)
        a += pas
    return tuple(res)


def pour(fonction, *args):
    """Equivalent de la fonction for + ajout du support de l ecriture c de for"""
    res = 0
    if len(args) > 3:
        raise ErreurArguments(
            "La fonction a été appelée avec trop d arguments")
    elif len(args) == 0:
        raise ErreurArguments("La fonction nécessite au moins 2 argument")
    elif len(args) == 1:
        if isinstance(args[0], (List, Tuple, str, chaine)):
            i = 0
            while i < len(args[0]):
                fonction(args[0][i])
                i += 1
        elif isinstance(args[0], (int, entier)):
            i = 0
            r = distance(args[0])
            while i < len(r):
                fonction(r[i])
                i += 1
    elif isinstance(args[0], (int, entier)):
        i = 0
        if len(args) == 2:
            r = distance(args[0], args[1])
        else:
            r = distance(args[0], args[1], args[2])
        while i < len(r):
            fonction(r[i])
            i += 1
