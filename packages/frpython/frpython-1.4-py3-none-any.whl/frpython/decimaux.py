from typing import Any

from frpython.erreurs import TypeInconnu


class decimal:

    contenu: float

    def __init__(self, o: Any) -> None:
        if isinstance(o, float):
            self.contenu = float

    def __add__(self, o: object):
        if isinstance(o, float):
            return decimal(self.contenu + o)
        elif isinstance(o, decimal):
            return decimal(self.contenu + o.contenu)
        else:
            raise TypeInconnu(
                "Le type utilise ne peut etre additione a un decimal")

    def __eq__(self, o: object) -> bool:

        if isinstance(o, float):
            return self.contenu == o

        elif isinstance(o, decimal):
            return self.contenu == o.contenu

    def __add__(self, o : object):
        if isinstance(o, float):
            return decimal(self.contenu + o)
        return decimal(self.contenu + o.contenu)
