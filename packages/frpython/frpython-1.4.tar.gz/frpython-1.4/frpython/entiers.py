from .erreurs import ErreurDeConversion, TypeInconnu
from .decimaux import decimal
from .booleen import booleen

class entier:

    contenu: int = 0

    chiffres = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    dictioChiffres = {"0": 0, "1": 1, "2": 2, "3": 3,
                      "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9}

    def __init__(self, o : object) -> None:

        if isinstance(o, int):
            self.contenu = o

        elif isinstance(o, (str)):
            for c in o:
                if not (c in self.chiffres):
                    raise ErreurDeConversion(
                        f"Il faut uniquement des chiffres dans la chaine: {o}")
            l = []
            for chiffre in o[::-1]:
                self.contenu += self.dictioChiffres[chiffre]

        elif isinstance(o, (float, decimal)):
            if type(o) == float:
                a = str(o.contenu)
            else:
                a = str(o)
            o = a.split(".")[0]
            for chiffre in o[::-1]:
                self.contenu += self.dictioChiffres[chiffre]
            if int(a.split(".")[1][0]) >= 5:
                self.contenu += 1

        elif isinstance(o, (bool, booleen)):
            if o:
                self.contenu = 1
            else:
                self.contenu = 0

        else:
            raise TypeInconnu(
                "La variable entrée n'est pas convertible en entier")

    def vers_int(self):
        return self.contenu

    def __eq__(self, o: object) -> bool:
        if isinstance(o, entier):
            return self.contenu == o.contenu
        return self.contenu == o

    def __gt__(self, o: object) -> bool:
        if isinstance(o, entier):
            return self.contenu > o.contenu
        return self.contenu > o

    def __ge__(self, o: object) -> bool:
        if isinstance(o, entier):
            return self.contenu >= o.contenu
        return self.contenu >= o

    def __lt__(self, o: object) -> bool:
        if isinstance(o, entier):
            return self.contenu < o.contenu
        return self.contenu < o

    def __le__(self, o: object) -> bool:
        if isinstance(o, entier):
            return self.contenu <= o.contenu
        return self.contenu <= o

    def __truth__(self) -> bool:
        return bool(self.contenu)
    
    def __add__(self, o : object) -> object:
        if isinstance(o, int):
            return entier(self.contenu + o)
        return entier(self.contenu + o.contenu)

    def __sub__(self, o : object):
        if isinstance(o, int):
            return entier(self.contenu - o)
        return entier(self.contenu - o.contenu)

    def __truediv__(self, o : object) -> decimal:
        if isinstance(o, int):
            return decimal(self.contenu / o)
        return decimal(self.contenu / o.contenu)

    def __floordiv__(self, o : object) -> object:
        if isinstance(o, int):
            return entier(self.contenu // o)
        return entier(self.contenu // o.contenu)

    def __neg__(self):
        return entier(-self.contenu)

    def __pow__(self, o : object):
        if isinstance(o, int):
            return entier(self.contenu ** o)
        return entier(self.contenu ** o.contenu)

    def __mod__(self, o : object):
        if isinstance(o, int):
            return entier(self.contenu % o)
        return entier(self.contenu % o.contenu)

    def __mul__(self, o : object):
        if isinstance(o, int):
            return entier(self.contenu * o)
        return entier(self.contenu * o.contenu)

    