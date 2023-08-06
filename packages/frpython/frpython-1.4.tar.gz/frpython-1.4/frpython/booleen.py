from frpython.erreurs import TypeInconnu


class booleen:
    
    contenu : bool

    def __init__(self, o : object):
        
        

        if isinstance(o, (bool, booleen)):
            a = None
            if type(o) == bool:
                a = o
            else:
                a = o.contenu
            self.contenu = a

        elif isinstance(o, int):
            if o > 0:
                self.contenu = True
            else:
                self.contenu = False
        
        else:
            raise TypeInconnu("Le type entree ne peut etre converti en booleen")

    def __eq__(self, o: object) -> bool:
        if isinstance(o, bool):
            return self.contenu == o
        return self.contenu == o.contenu
    
    def __not__(self):
        if self.contenu:
            return booleen(False)
        return booleen(True)
