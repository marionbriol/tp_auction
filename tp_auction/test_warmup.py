"""
Script d'échauffement pour le TP sur les enchères.

Ce script vous permet de pratiquer deux concepts essentiels :
1. L'HÉRITAGE en programmation orientée objet
2. Les TESTS UNITAIRES et les MOCKS (objets de test)

À COMPLÉTER : Recherchez les sections marquées avec "TODO" et complétez le code en suivant le tp.
"""

import unittest


# =============================================================================
# ÉCHAUFFEMENT 1 : L'HÉRITAGE
# =============================================================================

"""
=== CONCEPT D'HÉRITAGE ===

L'héritage permet à une classe (classe fille) de réutiliser le code d'une autre classe (classe mère).
C'est un mécanisme fondamental de la programmation orientée objet.

Points clés :
- class Fille(Mere): déclare que Fille hérite de Mere
- La classe fille hérite de TOUTES les méthodes et attributs de la classe mère
- La classe fille peut SURCHARGER (redéfinir) une méthode de la classe mère
- super() permet d'appeler la version de la classe mère (rarement utilisé)
- self.methode() cherche d'abord dans la classe réelle de l'objet, puis dans les parents
"""

class Animal:
    """
    Classe de base pour les animaux.
    C'est la classe MERE.

    Remarquez que describe() APPELLE self.sound().
    Quand on appellera describe() sur un Dog, self sera un Dog,
    donc self.sound() trouvera la version de Dog !
    """

    def __init__(self, name):
        # TODO : Créez l'attribut self.name avec le paramètre name
        pass

    def sound(self):
        """
        Méthode qui retourne le son de l'animal.
        Dans la classe de base, on retourne "..." par défaut.
        """
        return "..."

    def describe(self):
        """
        Méthode qui décrit l'animal.
        Elle utilise self.sound() pour obtenir le son spécifique.
        C'est la MÉTHODE PATRON (template method) : le squelette est écrit ici,
        mais le comportement spécifique est délégué aux classes filles.
        """
        return f"{self.name} says {self.sound()}"


class Dog(Animal):
    """
    Classe fille d'Animal.
    Hérite de tout le code d'Animal (init, describe).

    TODO : Vous devez uniquement redéfinir sound() pour retourner "Woof"
    Ne réécrivez PAS describe() ! Elle est héritée d'Animal.
    """

    # TODO : Redéfinissez la méthode sound() pour retourner "Woof"
    pass


class Cat(Animal):
    """
    Classe fille d'Animal.
    TODO : Redéfinissez sound() pour retourner "Meow"
    """

    # TODO : Redéfinissez la méthode sound() pour retourner "Meow"
    pass


class Bird(Animal):
    """
    Classe fille d'Animal.
    Plus complexe : elle a un paramètre supplémentaire can_fly.

    TODO :
    1. Dans __init__, appelez super().__init__(name) pour que la classe mère initialise name
    2. Ensuite, stockez can_fly dans self.can_fly
    3. Redéfinissez sound() pour retourner "Tweet"
    4. Redéfinissez describe() pour :
       - Appeler super().describe() pour obtenir le texte de base
       - Ajouter " and flies" à la fin si can_fly est True
    """

    def __init__(self, name, can_fly=True):
        # TODO : Appelez super().__init__(name) puis stockez can_fly
        pass

    # TODO : Redéfinissez sound() pour retourner "Tweet"
    pass

    # TODO : Redéfinissez describe() pour compléter celle du parent
    pass


# =============================================================================
# ÉCHAUFFEMENT 2 : LES TESTS UNITAIRES ET LES MOCKS
# =============================================================================

"""
=== CONCEPT DE TESTS UNITAIRES ===

Un test unitaire est un petit programme qui vérifie automatiquement qu'un morceau de code
se comporte comme prévu. C'est essentiel pour détecter les régressions (bugs introduits
quand on modifie du code existant).

Avec unittest :
- On crée une classe qui hérite de unittest.TestCase
- Chaque méthode dont le nom commence par "test_" est un test
- On utilise des assertions : assertEqual, assertIn, assertRaises, etc.
- Si une assertion échoue, le test échoue et on voit ce qui était attendu vs obtenu

=== CONCEPT DE MOCKS (OBJETS DE TEST) ===

Pour tester du code interactif (qui utilise input() et print()), on ne peut pas tester
avec un vrai humain. La solution est d'utiliser des MOCKS (faux objets).

PRINCIPE DE L'INJECTION DE DÉPENDANCE :
- Au lieu d'appeler input() et print() directement en dur dans le code
- On passe un objet "cli" au constructeur, qui a les méthodes display() et prompt()
- En production : le vrai Cli utilise input() et print()
- Dans les tests : un ScriptedCli (mock) retourne des réponses pré-programmées

Avantages :
- Tests automatiques, rapides et déterministes
- Pas besoin d'humain pour taper les réponses
- On peut vérifier exactement ce qui est affiché
"""

class TestAnimals(unittest.TestCase):
    """
    Classe de tests pour les animaux.
    Hérite de unittest.TestCase (voilà encore de l'héritage !).

    TODO : Écrivez 3 tests :
    1. test_dog : vérifie que Dog("Rex").describe() == "Rex says Woof"
    2. test_bird_no_fly : vérifie que Bird("Pingu", can_fly=False).describe() == "Pingu says Tweet"
    3. test_dog_needs_name : vérifie que Dog() sans paramètre lève une TypeError

    Utilisez self.assertEqual(attendu, obtenu) pour les tests 1 et 2
    Utilisez "with self.assertRaises(TypeError):" pour le test 3
    """

    # TODO : Écrivez le test pour Dog
    pass

    # TODO : Écrivez le test pour Bird qui ne vole pas
    pass

    # TODO : Écrivez le test pour Dog sans nom (doit lever TypeError)
    pass


class Greeter:
    """
    Exemple de classe qui interagit avec l'utilisateur via un CLI.
    Elle NE PASSE PAS input() et print() en dur, mais utilise self.cli.

    C'est ce qui permet de la tester avec un mock !
    """

    def __init__(self, cli):
        self.cli = cli

    def play(self):
        name = self.cli.prompt("What is your name?")
        self.cli.display(f"Hello {name}!")


class ScriptedCli:
    """
    C'est un MOCK (faux objet) pour simuler un CLI dans les tests.

    TODO : Implémentez cette classe avec :
    1. __init__(self, answers) : stocke les réponses dans self.answers (en copiant la liste)
       et initialise self.displayed comme une liste vide
    2. display(self, message) : ajoute message à self.displayed
    3. prompt(self, message) :
       - Ajoute message à self.displayed (l'utilisateur voit aussi la question)
       - Retourne la première réponse de self.answers (utilise list.pop(0))
    """

    def __init__(self, answers):
        # TODO : Stockez les réponses et initialisez displayed
        pass

    def display(self, message):
        # TODO : Ajoutez le message à displayed
        pass

    def prompt(self, message):
        # TODO : Ajoutez le message à displayed et retournez la première réponse
        pass


# =============================================================================
# TESTS AUTOMATIQUES (ne pas modifier)
# =============================================================================

def test_inheritance():
    """Teste les classes d'héritage une fois complétées."""
    print("\n=== Test de l'héritage ===")

    try:
        # Test Dog
        assert Dog("Rex").describe() == "Rex says Woof"
        print("[OK] Dog: Rex says Woof")

        # Test Cat
        assert Cat("Tom").describe() == "Tom says Meow"
        print("[OK] Cat: Tom says Meow")

        # Test Animal
        assert Animal("Ghost").describe() == "Ghost says ..."
        print("[OK] Animal: Ghost says ...")

        # Test isinstance et issubclass
        assert isinstance(Dog("Rex"), Animal)
        assert issubclass(Cat, Animal)
        print("[OK] Dog est bien un Animal")
        print("[OK] Cat est bien une sous-classe d'Animal")

        # Vérifier que describe n'est pas réécrite dans Dog
        assert "describe" not in vars(Dog), "describe must be inherited, not rewritten"
        print("[OK] describe est bien héritée de Animal")

        # Test Bird qui vole
        assert Bird("Tweety").describe() == "Tweety says Tweet and flies"
        print("[OK] Bird (volant): Tweety says Tweet and flies")

        # Test Bird qui ne vole pas
        assert Bird("Pingu", can_fly=False).describe() == "Pingu says Tweet"
        print("[OK] Bird (non-volant): Pingu says Tweet")

        # Test MRO (Method Resolution Order)
        print(f"[OK] Dog.__mro__ = {Dog.__mro__}")

        print("\n=== Tous les tests d'héritage réussis ! ===\n")
        return True
    except Exception as e:
        print(f"\n[ERREUR] Test d'héritage échoué : {e}\n")
        return False


def test_scripted_cli():
    """Teste la classe ScriptedCli une fois complétée."""
    print("=== Test de ScriptedCli ===")

    try:
        cli = ScriptedCli(["Ada"])
        Greeter(cli).play()

        expected = ["What is your name?", "Hello Ada!"]
        assert cli.displayed == expected, f"Expected {expected}, got {cli.displayed}"
        print(f"[OK] Messages affichés: {cli.displayed}")

        print("\n=== Tous les tests ScriptedCli réussis ! ===\n")
        return True
    except Exception as e:
        print(f"\n[ERREUR] Test ScriptedCli échoué : {e}\n")
        return False


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print(" ÉCHAUFFEMENT TP ENCHÈRES")
    print("="*60)
    print("\nComplétez les sections marquées avec TODO")
    print("Puis relancez ce script pour vérifier votre travail.\n")

    # Exécuter les tests d'héritage
    inheritance_ok = test_inheritance()

    # Exécuter les tests unitaires avec unittest
    print("=== Exécution des tests unitaires (unittest) ===")
    try:
        unittest.main(argv=["ignored"], exit=False, verbosity=2)
        unittest_ok = True
    except:
        unittest_ok = False

    # Exécuter les tests ScriptedCli
    cli_ok = test_scripted_cli()

    print("\n" + "="*60)
    if inheritance_ok and unittest_ok and cli_ok:
        print(" BRAVO ! ÉCHAUFFEMENT TERMINÉ AVEC SUCCÈS !")
    else:
        print(" Certains tests échouent. Continuez à compléter le code !")
    print("="*60 + "\n")
