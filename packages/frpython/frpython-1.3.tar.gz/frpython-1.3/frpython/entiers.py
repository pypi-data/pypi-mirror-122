from .erreurs import ErreurDeConversion, TypeInconnu
from .chaines import chaine

class entier:

    contenu: int = 0

    chiffres = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    dictioChiffres = {"0": 0, "1": 1, "2": 2, "3": 3,
                      "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9}

    def __init__(self, o) -> None:

        if isinstance(o, int):
            self.contenu = o

        elif isinstance(o, (str, chaine)):
            for c in o:
                if not (c in self.chiffres):
                    raise ErreurDeConversion(
                        f"Il faut uniquement des chiffres dans la chaine: {o}")
            l = []
            for chiffre in o[::-1]:
                self.contenu += self.dictioChiffres[chiffre]

        elif isinstance(o, float):
            a = str(o)
            o = a.split(".")[0]
            for chiffre in o[::-1]:
                self.contenu += self.dictioChiffres[chiffre]
            if int(a.split(".")[1][0]) >= 5:
                self.contenu += 1

        else:
            raise TypeInconnu(
                "La variable entrée n'est pas convertible en entier")

    def __eq__(self, o: object) -> bool:
        if isinstance(o, entier):
            return self.contenu == o.contenu
        return self.contenu == o

    def __gt__(self, o: object) -> bool:
        return self.contenu > o.contenu

    def __lt__(self, o: object) -> bool:
        return self.contenu < o.contenu
