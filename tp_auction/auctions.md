
# Ventes aux enchères

Les intérêts de ce TP

* utiliser l'**héritage** pour factoriser du code
* utiliser des **tests automatisés**  
  (c'est une pratique hyper-courante dans la vraie vie:
   comme ça on détecte tout de suite les régressions sur le code)

Les notions au coeur de ce TP
- **héritage**: déclarer une classe fille, **surcharger** une méthode, appeler `super()`
- la **méthode patron** (*template method*): une méthode écrite une seule fois dans la classe de base, qui appelle des méthodes que les classes filles redéfinissent  
- les méthodes "à implémenter par les filles" (`NotImplementedError`)
- les **tests unitaires** avec `unittest`: `TestCase`, `assertEqual`, `assertIn`, `assertRaises`
- les **faux objets** (*test doubles*): remplacer `print` et `input` par un objet qu'on contrôle, pour tester sans humain  
  ce qui suppose que l'objet soit **fourni** à la classe plutôt que créé en dur (*injection de dépendance*)
- les **régressions**: relancer les tests après chaque modification

## échauffement 1 : l'héritage

L'échauffement se passera entièrement dans le fichier test_warmup.py.

Avant de passer aux enchères, on s'assure qu'on a bien en tête les mécanismes de l'héritage

- `class Dog(Animal):` déclare que `Dog` **hérite** de `Animal`: toutes les méthodes et attributs d'`Animal` sont disponibles sur les instances de `Dog`
- une classe fille peut **surcharger** (*override*) une méthode, en la redéfinissant avec le même nom
- quand on écrit `self.methode()`, Python cherche d'abord dans la classe **réelle** de l'objet, puis dans ses parents: c'est ce qu'on appelle la *résolution dynamique*
- `super()` permet d'appeler la version de la classe parente, notamment `super().__init__(...)` pour que le parent initialise sa partie de l'objet


voici une classe `Animal`; remarquez que `describe()` **appelle** `self.sound()`

```{code-cell} ipython3
class Animal:
    def __init__(self, name):
        self.name = name

    def sound(self):
        return "..."

    def describe(self):
        return f"{self.name} says {self.sound()}"
```

### échauffement 1.1 : surcharger une méthode

**Énoncé :** écrivez deux classes `Dog` et `Cat`, filles d'`Animal`, qui font respectivement "Woof" et "Meow"  
vous ne devez **pas** réécrire `describe()`

```{code-cell} ipython3

# votre code

class Dog(Animal):
    pass

class Cat(Animal):
    pass
```

```{code-cell} ipython3

# pour tester

try:
    assert Dog("Rex").describe() == "Rex says Woof"
    assert Cat("Tom").describe() == "Tom says Meow"
    assert Animal("Ghost").describe() == "Ghost says ..."
    assert isinstance(Dog("Rex"), Animal)
    assert issubclass(Cat, Animal)
    assert "describe" not in vars(Dog), "describe must be inherited, not rewritten"
except Exception as e:
    print("OOPS - Something's wrong")
    print(f"Error message : {e}")
else:
    print('Congrats ! Your implementation works !')
```

<details>
<summary><b>Indice</b></summary>

il suffit de redéfinir `sound()` dans chacune des deux classes
</details>

**Questions :**
1. `describe()` n'est écrite que dans `Animal`; pourquoi `Dog("Rex").describe()` affiche-t-elle bien "Woof" et non "..." ?
2. que vous affiche `Dog.__mro__` ?

```{code-cell} ipython3
Dog.__mro__
```

<details>
<summary><b>Réponses</b></summary>

1. dans `describe()`, `self` désigne l'objet **réel**, ici un `Dog`; l'appel `self.sound()` démarre donc la recherche dans `Dog`, qui trouve sa propre version  
   c'est un mécanisme **essentiel** pour la suite: une méthode de la classe de base peut appeler des méthodes que seules les classes filles définissent
2. `(Dog, Animal, object)`: c'est l'ordre dans lequel Python cherche les méthodes (*Method Resolution Order*)
</details>

### échauffement 1.2 : `super()`

**Énoncé :** écrivez une classe `Bird`, fille d'`Animal`, qui
- se construit avec `Bird(name, can_fly=True)`
- fait "Tweet"
- dont `describe()` **complète** celle du parent: si l'oiseau vole, on ajoute `" and flies"` à la fin de la phrase

```{code-cell} ipython3


# votre code

class Bird(Animal):
    pass
```

```{code-cell} ipython3


# pour tester

try:
    assert Bird("Tweety").describe() == "Tweety says Tweet and flies"
    assert Bird("Pingu", can_fly=False).describe() == "Pingu says Tweet"
    assert Bird("Tweety").name == "Tweety"
except Exception as e:
    print("OOPS - Something's wrong")
    print(f"Error message : {e}")
else:
    print('Congrats ! Your implementation works !')
```

<details>
<summary><b>Indice 1 : le constructeur</b></summary>

`Bird.__init__` prend un paramètre de plus que `Animal.__init__`; pour ne pas dupliquer le code du parent, appelez-le avec `super().__init__(name)`, puis rangez `can_fly`
</details>

<details>
<summary><b>Indice 2 : describe</b></summary>

récupérez le texte du parent avec `super().describe()`, puis ajoutez-y, ou non, la fin de phrase
</details>

**Questions :**
1. que se passe-t-il si on oublie d'appeler `super().__init__(name)` dans `Bird.__init__` ?
2. dans le code d'`Animal`, `sound()` retourne `"..."`: est-ce une bonne idée ? que vaudrait-il mieux faire pour une classe qui n'est pas censée être utilisée directement ?

<details>
<summary><b>Réponses</b></summary>

1. l'attribut `name` n'est jamais créé; on obtient une `AttributeError: 'Bird' object has no attribute 'name'` dès qu'on utilise `describe()`
2. avec `"..."`, une classe fille qui **oublie** de redéfinir `sound()` fonctionne quand même, en silence, avec un comportement faux; il vaut mieux que la méthode lève `NotImplementedError("Subclasses must implement this method")`: l'oubli se voit tout de suite  
   c'est exactement ce qu'on fera pour la méthode que chaque type d'enchère doit définir
</details>



## échauffement 2 : les tests unitaires

un **test unitaire** est un petit programme qui vérifie automatiquement qu'un morceau de code se comporte comme prévu  
avec le module `unittest` de la bibliothèque standard

- on déclare une classe qui hérite de `unittest.TestCase` (voilà de l'héritage, encore !)
- chaque méthode dont le nom **commence par `test`** est un test
- à l'intérieur on utilise des assertions: `self.assertEqual(attendu, obtenu)`, `self.assertIn(element, conteneur)`, `with self.assertRaises(UneException):`...
- un test qui échoue affiche précisément ce qui était attendu et ce qui a été obtenu


### échauffement 2.1 : écrire des tests

**Énoncé :** complétez la classe `TestAnimals` pour tester `Dog` et `Bird`, avec **au moins trois tests**:
1. la phrase de `Dog("Rex")`
2. la phrase d'un oiseau qui ne vole pas
3. qu'on ne peut pas construire un `Dog` sans lui donner de nom (une `TypeError` est attendue)

```{code-cell} ipython3
# votre code

import unittest

class TestAnimals(unittest.TestCase):
    pass
```

pour exécuter les tests directement dans le notebook

**Pour vérifier que vos tests servent à quelque chose :** modifiez volontairement `Dog.sound` pour qu'il retourne autre chose que "Woof", ré-évaluez, et assurez-vous qu'au moins un de vos tests devient rouge; puis remettez le code correct

<details>
<summary><b>Indice 1</b></summary>

chaque test est une méthode dont le nom commence par `test_`; dans chacune, construisez un objet puis comparez avec `self.assertEqual(attendu, obtenu)` (dans ce TP, on met **l'attendu en premier**)
</details>

<details>
<summary><b>Indice 2 : tester une exception</b></summary>

```python
with self.assertRaises(TypeError):
    ...  # le code qui doit lever l'exception
```
</details>

### échauffement 2.2 : un faux objet pour remplacer `input` et `print`

comment tester un programme interactif, qui pose des questions à l'utilisateur ? on ne va pas taper les réponses à la main à chaque fois !

la solution consiste à **ne pas appeler `print` et `input` directement**: la classe reçoit un objet `cli` qui sait faire `display` et `prompt`; en production c'est un vrai terminal, dans les tests c'est un **faux**

```{code-cell} ipython3
class Greeter:
    def __init__(self, cli):
        self.cli = cli

    def play(self):
        name = self.cli.prompt("What is your name?")
        self.cli.display(f"Hello {name}!")
```

**Énoncé :** écrivez une classe `ScriptedCli`, qui
- se construit avec la liste des réponses que "taperait" l'utilisateur: `ScriptedCli(["Ada"])`
- possède `prompt(message)`, qui retourne la réponse suivante
- possède `display(message)`
- conserve dans un attribut `displayed` la liste de **tous** les messages affichés, dans l'ordre, qu'ils viennent de `display` ou de `prompt`

```{code-cell} ipython3
# votre code

class ScriptedCli:
    pass
```

```{code-cell} ipython3
# pour tester

try:
    cli = ScriptedCli(["Ada"])
    Greeter(cli).play()
    assert cli.displayed == ["What is your name?", "Hello Ada!"], cli.displayed
except Exception as e:
    print("OOPS - Something's wrong")
    print(f"Error message : {e}")
else:
    print('Congrats ! Your implementation works !')
```

<details>
<summary><b>Indice</b></summary>

`prompt` doit à la fois **enregistrer** son message dans `displayed` (puisque l'utilisateur le voit à l'écran) et **retourner** une réponse; `list.pop(0)` retire et retourne le premier élément d'une liste
</details>

**Question :** pourquoi `Greeter` reçoit-il son `cli` dans son constructeur, au lieu d'appeler `input()` et `print()` directement ?

<details>
<summary><b>Réponse</b></summary>

si `Greeter` appelait `input()` en dur, on ne pourrait pas le tester sans un humain devant le clavier  
en lui **fournissant** l'objet dont il a besoin, on peut lui en donner un faux, déterministe et instantané: c'est l'**injection de dépendance**  
c'est pour cette raison que, dans ce TP, `print()` et `input()` sont **interdits**: il faut passer par `self.cli`
</details>



***



## Avant toute chose



### Consignes générales

- Chacune des enchères a déjà un constructeur. Vous pouvez ajouter des choses dans ce constructeur, mais **pas en supprimer**.
- Pour intéragir avec la ligne de commande, vous devez **impérativement** utiliser l'utilitaire `self.cli` qui est dans les enchères.
  - Vous pouvez faire l'équivalent de `print()` en faisant `self.cli.display()`
  - Vous pouvez demander à l'utilisateur de saisir des choses sur la ligne de commande, l'équivalent de `value = input("Entrez une valeur")`, en faisant `value = self.cli.prompt("Entrez une valeur")`
  - L'usage direct de `print()` et `input()` est proscrit, sinon les tests ne marcheront pas
  - Cette classe nous sert à simuler `print` et `input` dans les tests automatisés (c'est exactement ce que vous venez de faire avec `ScriptedCli`)
- Pour ce TP, vous pouvez estimer que les utilisateurs du programme ne font que des choses "légales"
  - Par exemple, quand on leur demande d'enchérir, ils tapent "10" ou "115", mais ils ne tapent pas "toto 1234 %&@# 💣💩🤮"
  - Par exemple, quand on leur demande de sur-enchérir sur une enchère de 30, ils tapent "45" ou une chaîne vide pour passer leur tour, mais pas "12"
  - Le but n'est pas de tester toutes les possibilités !

Attention à "passer son tour"

Quand l'utilisateur tape juste entrée, le vrai `Cli` retourne une **chaine vide** `""`, alors que le faux `Cli` des tests retourne **`None`**  
pensez à gérer les deux: `if not bid:` plutôt que `if bid is None:` (et souvenez-vous que `int("")` lève une `ValueError`)




### Comment exécuter les tests

Dans ce TP on vous fournit des tests unitaires, ce qui vous permet de savoir rapidement si vous avez bien respecté les consignes ou non (enfin c'est l'idée, mais il se peut que les tests soient un peu superficiels ici..)

Les imports sont relatifs
Les fichiers du TP font partie d'un **paquet** (le dossier `auctions/`, qui contient un fichier `__init__.py`), et s'importent entre eux avec la syntaxe `from .utils import Cli`  
du coup on ne lance **pas** `python blind.py`, mais on utilise `python -m`, **depuis le dossier qui contient `auctions/`**




#### depuis le terminal

```shell
$ python -m auctions.blind                    # faire une vente, à la main
```

pour les tests, vous pouvez en lancer un seul fichier (normalement le test est OK pour `blind` à ce stade)

```shell
$ python -m unittest auctions.test_blind
...
----------------------------------------------------------------------
Ran 3 tests in 0.306s

OK
```

ou tous d'un coup

```shell
$ python -m unittest discover -s auctions -t .
```

ou encore, si vous avez installé avec `pip install pytest`

```shell
$ pytest auctions/test_blind.py
================================ test session starts ================================
collected 3 items

auctions/test_blind.py ...                                                    [100%]

================================= 3 passed in 0.39s =================================
```



#### depuis VSCode

1. Ouvrez tout le dossier dans VSCode
2. Choisissez sur la gauche l'onglet 'Testing', et configurez les tests Python pour utiliser `unittest` et aux questions suivantes, répondez:

* Q: `Select the directory containing the tests:`  
  A: `. Root directory`
* Q: `Select the pattern to identify test files:`  
  A: `test_*.py` (vous devez avoir des fichiers de ce genre, comme `test_blind.py`)

3. À ce stade vous devriez voir les testeurs, toujours dans l'onglet gauche `Testing`

#### comment fonctionnent ces tests ?

Lecture d'un test

voici le début de `test_blind.py`

```python
def test_opening_bid(self):
    cli = make_auction(BlindAuction)
    self.assertEqual(
        ['Started auction of type: Blind',
         'Please enter the amount for the opening bid:'],
        cli.get_displayed()
    )
    cli.type('30')
    self.assertIn('Opening bid is: 30', cli.get_displayed())
```

- `make_auction(BlindAuction)` crée un faux `cli`, une enchère qui l'utilise, et lance `auction.play()` **dans un thread**
- `cli.get_displayed()` retourne ce qui a été affiché depuis le dernier appel
- `cli.type('30')` "tape" une réponse au clavier

**Question :** pourquoi `play()` tourne-t-elle dans un thread, alors que dans `ScriptedCli` on avait simplement donné toutes les réponses à l'avance ?

<details>
<summary><b>Réponse</b></summary>

ici on veut **vérifier ce qui est affiché au milieu** de la vente: après le prix de départ, après chaque nom, avant chaque enchère...  
or `play()` se **bloque** dans `prompt()` tant que personne n'a tapé de réponse; en la lançant dans un thread, le test peut inspecter l'affichage, puis taper la réponse suivante, et ainsi de suite, comme le ferait un humain  
(avec `ScriptedCli`, on ne vérifie que le résultat final)
</details>


---

Mais passons au TP, enfin !



## 1. Blind auction: les règles

Voici les règles des enchères à l'aveugle, ou [Blind auction](https://en.wikipedia.org/wiki/First-price_sealed-bid_auction):

- Les enchères démarrent avec un prix minimum
- Les enchérisseurs doivent sur-enchérir par rapport au prix minimum
- Les enchérisseurs ne savent pas quel est la plus haute enchère (on estime qu'ils ne peuvent pas lire ce que les autres on saisi dans le terminal)
- Il n'y a qu'un seul tour
- Le gagnant est celui qui a proposé le prix le plus haut
- Le prix final est le prix le plus haut proposé

Exemple:

```shell
$ python -m auctions.blind
Started auction of type: Blind
Please enter the amount for the opening bid: 50
Opening bid is: 50
Enter name for bidder 1 (enter nothing to move on): alice
Enter name for bidder 2 (enter nothing to move on): bob
Enter name for bidder 3 (enter nothing to move on): carol
Enter name for bidder 4 (enter nothing to move on):

Bidders are: alice, bob, carol

Opening bid is 50. alice bids: 60
Opening bid is 50. bob bids: 80
Opening bid is 50. carol bids: 70

~~~~~~~~

Winner is bob. Winning bid is 80.
```

## 2. Blind auction: le code

 Regardez le fichier `blind.py`, tout a déjà été implémenté pour vous. Lisez le code, exécutez le fichier, faites une partie d'enchères.

Vous pouvez également regarder `test_blind.py` pour avoir une idée de comment les tests sont écrits, si vous êtes curieux.

 Exécutez `test_blind.py`, de préférence avec VS Code. C'est important, parce que vous allez, plus tard dans le TP, modifier `blind.py`.

**Questions de lecture :**
1. pourquoi le constructeur prend-il un paramètre `cli=None` ?
2. quelles parties du code de `BlindAuction.play()` vous semblent **ne pas dépendre** du type d'enchère ? gardez-les en tête pour l'étape 4

<details>
<summary><b>Réponses</b></summary>

1. quand on lance la vente "pour de vrai", on ne passe rien et le constructeur crée un vrai `Cli()`; les tests passent leur faux `cli` à la place (injection de dépendance, cf. l'échauffement 2.2)
2. presque tout, sauf la boucle sur les enchères elle-même: la saisie du prix de départ, la saisie des noms des enchérisseurs, l'annonce du gagnant
</details>



## 3. English auction: les règles

Vous allez maintenant implémenter des enchères anglaises, ou [English auction](https://en.wikipedia.org/wiki/English_auction). Voici les règles:

- Les enchères démarrent avec un prix minimum
- Les enchérisseurs voient cette fois la plus haute enchère en cours
- Les enchérisseurs doivent sur-enchérir par rapport à la meilleure enchère en cours
- Il y a plusieurs tours
- L'enchère est finie lorsque tous les participants passent leur tour (ne tapent rien dans le terminal)
- Le gagnant est celui qui a proposé le prix le plus haut
- Le prix final est le prix le plus haut proposé

**NOTES**

- un participant qui passe n'est pas éliminé, il peut encore parler au tour suivant s'il y en a un
- du coup la vente s'arrête sur un tour où tous les participants passent


Exemple:

```shell
$ python -m auctions.english
Started auction of type: English
Please enter the amount for the opening bid: 30
Opening bid is: 30
Enter name for bidder 1 (enter nothing to move on): alice
Enter name for bidder 2 (enter nothing to move on): bob
Enter name for bidder 3 (enter nothing to move on): carol
Enter name for bidder 4 (enter nothing to move on):

Bidders are: alice, bob, carol

Standing bid is 30. alice bids: 35
Standing bid is 35. bob bids: 40
Standing bid is 40. carol bids:
Standing bid is 40. alice bids: 45
Standing bid is 45. bob bids:
Standing bid is 45. carol bids:
Standing bid is 45. alice bids:
Standing bid is 45. bob bids:
Standing bid is 45. carol bids:

~~~~~~~~

Winner is alice. Winning bid is 45.
```

 Implémentez l'English auction dans `english.py`. Vous avez le droit de tout copier-coller depuis `blind.py` pour commencer! Vous devez exécuter les tests jusqu'à ce que `test_english.py` fonctionne à 100%.

<details>
<summary><b>Indice 1 : par quoi commencer</b></summary>

copiez `blind.py` dans `english.py`, renommez la classe en `EnglishAuction` et le nom d'enchère en `"English"`  
tout ce qui précède la boucle des enchères reste **identique**: seule la boucle change
</details>

<details>
<summary><b>Indice 2 : la boucle</b></summary>

il faut une boucle **extérieure** (les tours) et une boucle **intérieure** (les enchérisseurs, dans l'ordre)  
la boucle extérieure s'arrête quand un tour complet s'est déroulé **sans qu'aucune enchère** n'ait été posée; pensez à un booléen qu'on remet à `False` au début de chaque tour, et qu'on passe à `True` dès que quelqu'un enchérit
</details>

<details>
<summary><b>Indice 3 : passer son tour</b></summary>

relisez l'encadré sur "passer son tour" plus haut: la réponse est vide (`""` ou `None`), pas un entier  
attention à ne pas convertir en `int` avant d'avoir traité ce cas
</details>

## 4. Mise en commun: le facile

Remarquez maintenant les similitudes entre `blind` et `english`.

 Introduisez une classe de base, par exemple `Auction` dans le fichier `auction.py`, et mutualisez les étapes en commun dans `blind` et `english`, par exemple en introduisant des méthodes ou fonctions spécifiques.

N'oubliez pas d'exécuter les tests de `blind` et `english` pour être sûrs que vous n'avez rien cassé!

<details>
<summary><b>Indice 1 : qu'est-ce qui est commun ?</b></summary>

comparez les deux `play()`: les blocs identiques sont
1. le constructeur
2. la saisie du prix de départ
3. la saisie des enchérisseurs
4. l'annonce du gagnant

un bloc → une méthode de `Auction`
</details>

<details>
<summary><b>Indice 2 : les constructeurs</b></summary>

le constructeur de la classe fille ne doit pas recopier celui du parent: il l'appelle avec `super().__init__(cli)`, puis ajoute ce qui lui est propre (ici, le nom de l'enchère)  
rappelez-vous la consigne: on ne **supprime** pas le constructeur des enchères, on peut seulement l'enrichir
</details>

## 5. Mise en commun: un peu plus intéressant

 Essayez de ne définir la méthode "play" que dans la classe de base, `auction`. Comment s'y prendre ?

Dans tous les cas, essayez de factoriser au maximum entre les deux modes que l'on a vus jusqu'ici, de façon à minimiser le code qui va être nécessaire pour la 3éme variante que nous allons voir tout de suite.

<details>
<summary><b>Indice 1 : ce qui change</b></summary>

dans les deux `play()` de l'étape précédente, **une seule chose** diffère: la boucle des enchères  
`play()` est donc "le même squelette" pour tout le monde: prix de départ, enchérisseurs, **boucle**, annonce
</details>

<details>
<summary><b>Indice 2 : la méthode patron</b></summary>

écrivez `play()` dans `Auction`, avec un appel à une méthode, disons `auction_loop(opening_bid, bidders)`, qui **n'est pas implémentée** dans `Auction` (elle lève `NotImplementedError`), et que chaque classe fille **surcharge**  
souvenez-vous de l'échauffement 1: dans `play()`, `self.auction_loop(...)` cherche la méthode dans la classe **réelle** de l'objet
</details>

<details>
<summary><b>Indice 3 : ce que doit retourner la boucle</b></summary>

`play()` a besoin de deux informations pour annoncer le résultat: le gagnant (ou `None` si personne n'a enchéri) et le prix final  
la boucle les retourne sous la forme d'un tuple `(winner, price)`
</details>

## 6. Vickrey auction

Il devrait être facile d'implémenter une nouvelle enchère!

Voici les règles des enchères en plis cachetés à un tour au second prix, ou [Enchère de Vickrey](https://en.wikipedia.org/wiki/Vickrey_auction):

- Les enchères démarrent avec un prix minimum
- Les enchérisseurs doivent sur-enchérir par rapport au prix minimum
- Les enchérisseur ne savent pas quel est la plus haute enchère (on estime qu'ils ne peuvent pas lire ce que les autres ont saisi dans le terminal)
- Il n'y a qu'un seul tour
- Le gagnant est celui qui a proposé le prix le plus haut
- Le prix final est la _deuxième enchère la plus haute_

Exemple:

```
Started auction of type: Vickrey
Please enter the amount for the opening bid: 50
Opening bid is: 50
Enter name for bidder 1 (enter nothing to move on): alice
Enter name for bidder 2 (enter nothing to move on): bob
Enter name for bidder 3 (enter nothing to move on): carol
Enter name for bidder 4 (enter nothing to move on):

Bidders are: alice, bob, carol

Opening bid is 50. alice bids: 60
Opening bid is 50. bob bids: 80
Opening bid is 50. carol bids: 70

~~~~~~~~

Winner is bob. Winning bid is 70.
```

 A vous de jouer, comme d'habitude vous avez un fichier de test `test_vickrey.py`. Le cas ci-dessus est intéressant pour votre implémentation.

<details>
<summary><b>Indice 1 : par quoi commencer</b></summary>

si votre factorisation de l'étape 5 est bonne, la nouvelle classe tient en **une seule méthode**: `auction_loop`  
le constructeur, la saisie du prix et des noms, l'annonce du gagnant: tout est hérité
</details>

<details>
<summary><b>Indice 2 : le calcul</b></summary>

contrairement à la Blind auction, on ne peut plus se contenter de garder "la meilleure offre" au fil de l'eau: il faut connaître la **deuxième** meilleure  
conservez toutes les offres (par exemple une liste de couples `(montant, nom)`), puis triez-les par montant décroissant: la première est celle du gagnant, la deuxième donne le prix
</details>

<details>
<summary><b>Indice 3 : les cas limites</b></summary>

que doit valoir le prix s'il n'y a **qu'un seul** enchérisseur ? (le prix de départ)
</details>

## 7. Jeu libre

Si vous avez encore le temps, n'hésitez pas à modifier votre programme pour mettre une méthode qui représente "un tour" d'enchères dans la classe de base, et voir comment modifier vos classes filles pour l'utiliser. Pas de test particulier pour ça, mais, comme d'habitude, il ne faut rien casser !

## 8. Bonus : écrivez vos propres tests

les tests fournis sont, de l'aveu même de l'énoncé, un peu superficiels; à vous d'en ajouter deux, dans un nouveau fichier `test_bonus.py`

1. **English**: personne n'enchérit (tous les enchérisseurs passent dès le premier tour); la vente doit se terminer par le message `No winner for this auction.`
2. **Vickrey**: il n'y a qu'**un seul** enchérisseur, qui enchérit 60 sur un prix de départ de 30; il gagne, au prix de départ

pour vous assurer que vos tests sont sensibles, cassez volontairement le code (par exemple, faites retourner à Vickrey la meilleure offre au lieu de la deuxième) et vérifiez que **les tests deviennent rouges**; remettez ensuite le bon code

<details>
<summary><b>Indice</b></summary>

inspirez-vous de `test_english.py` et de `test_vickrey.py`: `make_auction(...)`, puis une série de `cli.type(...)`, avec des `get_displayed()` pour vérifier ce qui est affiché  
`cli.type(None)` "tape" juste entrée, c'est-à-dire passe son tour; et le **dernier** message affiché est `cli.get_displayed()[-1]`
</details>

D'autres idées pour aller plus loin
- rendre `Auction` réellement **abstraite** avec le module `abc` (`ABC` et `@abstractmethod`), de sorte qu'`Auction()` ne puisse même pas être instanciée
- `VickreyAuction` pourrait-elle hériter de `BlindAuction` ? que faudrait-il isoler dans une méthode pour que ce soit élégant ?
- une quatrième enchère: l'enchère **hollandaise**, où le prix part haut et descend jusqu'à ce que quelqu'un accepte



***
