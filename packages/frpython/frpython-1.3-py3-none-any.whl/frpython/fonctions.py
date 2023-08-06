from typing import List
from .chaines import chaine


def si(condition: bool, A, B=None, Aargs: list = [], Baargs: list = []):
    """
    Les fonctions entree dans cette fonction doivent avoir un argument qui est une liste si rien n est mis la liste sera vide
    Retourne le resultat de la fonction
    """
    if condition:
        return A(Aargs)
    else:
        return B(Baargs)


def dans(a : bool, L : List) -> bool:
    for i in L:
        if i == a:
            return True
    return False

def imprimer(*args) -> None:
    """Traduction de la fonction print"""
    res = chaine()
    for a in args:
        if isinstance(a, chaine):
            res += a
        else:
            res += chaine(a)
    print(res)