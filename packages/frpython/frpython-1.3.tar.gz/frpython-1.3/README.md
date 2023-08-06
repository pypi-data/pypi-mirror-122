# Fr - Python

Ceci est une tentative de traduction des classes de base Python, de certaines conditions et certaines fonctions

| Version | Utilisable |
| ------- | ---------- |
| 1.0     | Non        |
| 1.1     | Non        |
| 1.2     | Non        |
| 1.2.4   | Oui        |
| 1.2.5   | Oui        |
| 1.2.6   | Oui        |
| 1.2.7   | Oui        |
| 1.3     | En Test    |


## Les classes

### Classe Entier

Initialiseur -> Peut convertir un booleen, un decimal ou une chaine de caractere en entier
-> Si impossible retourne une erreur

Mise en place des operateurs qui retourne un entier sauf la division qui retournera un decimal

### Classe Decimal

Initialiseur -> Peut convertir un decimal ou une chaine de caractere en entier

Mise en place des operateurs qui retourne un decimal

### Classe Chaine

Initialiseur -> Peut convertir un decimal ou une chaine de caractere en entier

Mise en place de la concatenation

## Les fonctions

### Imprimer

Permet d afficher des listes, des entiers et des decimaux dans la console
Prend un nombre illimite d'aguments

### Pour

Prend un parametre obligatoire la valeur maximale, prend un debut optionnel, ainsi qu un pas optionel
l argument peut etre un entier dans ce cas la boucle ira du debut jusqu a ce chiffre
si c est une liste ou une chaine de caractere elle passera chacun des elements de la liste en revue

### Si

Prend deux parametre un boolen et une fonction qui sera executee si le booleen est vrai
Un troisieme argument de la fonction peut etre ajoute si le booleen s avere etre faux

### Distance

Prendra au maximum 3 parametres et au minimum 1 elle génerera un tuple

## Installation

Actuellement le paquet est uniquement disponible sur test.pypi

Pour l'installer:

```
$ pip install -i https://test.pypi.org/simple/ frpython
```

Pour l'utiliser dans un script:

```py
from frpython import *
```

## Documentation

La Documentation est disponible dans le fichier du meme nom

## Bonus Traduction des Erreurs

Si le temps le permet une traduction de certaines erreurs sera effectuée
