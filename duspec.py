#!/usr/bin/python3

# UČO:
# Povolené knihovny: math, typing

from typing import Any, Callable, Iterable, List, Tuple, Optional
from math import inf

# --- Speciální domácí úkol IB002 2022 ---
#
# V tomto testu budeme pracovat s H-stromy. H-strom je binární vyhledávací
# strom, v němž jsou v uzlech místo hodnot uloženy uzavřené intervaly
# s celočíselnými mezemi.
#
# Pro uzel s intervalem [a, b] platí:
#   1. a <= b,
#   2. všechny intervaly v levém podstromě obsahují hodnoty menší než 'a',
#   3. všechny intervaly v pravém podstromě obsahuji hodnoty větší než 'b'.
#
# H-strom slouží k reprezentaci množiny celých čísel. Uzly v H-stromě mohou být
# aktivní nebo pasivní. Reprezentovaná množina je tvořena právě těmi celými
# čísly, která patří do intervalu některého z aktivních uzlů.
# (Hodnoty z intervalů pasivních uzlů tedy do reprezentované množiny nepatří;
# tyto intervaly reprezentují místo, kam může být vložena nová hodnota.)
#
# Příklad (hvězdičky označují aktivní uzly):
#
#                    [7,10]
#                   /      \
#              [3,4]*       [12,14]*
#             /     \              \
#          [0,2]   [5,5]*           [15,18]
#
# Tento strom reprezentuje množinu hodnot {3, 4, 5, 12, 13, 14}.
#
# Vaším úkolem bude implementovat ověření výše uvedených vlastností H-stromu
# (is_correct), vkládání (insert) a mazání (delete).
#
# Do následujících definic tříd nijak nezasahujte.
# Pro vykreslování stromů máte na začátku části s testy funkci draw_tree.
# V souboru dot jsou aktivní uzly vyznačeny hvězdičkou a červenou barvou.


class Node:
    """Třída reprezentující uzel H-stromu.

    Atributy:
        low      spodní mez intervalu
        high     horní mez intervalu
        active   True, pokud je uzel aktivní, jinak False
        left     odkaz na levého potomka nebo None
        right    odkaz na pravého potomka nebo None
    """
    __slots__ = "low", "high", "active", "left", "right"

    def __init__(self, low: int, high: int, active: bool = False) -> None:
        self.low = low
        self.high = high
        self.active = active
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None


class HTree:
    """Třída reprezentující H-strom

    Atributy:
        root    kořen stromu typu Node nebo None
    """
    __slots__ = "root"

    def __init__(self) -> None:
        self.root: Optional[Node] = None


# Úkol 1. is_correct (1 bod)
#
# Implementujte funkci is_correct, která oveří, zda je strom 'tree'
# korektním H-stromem.
# Tedy ověrte, jestli pro každý uzel s intervalem [a, b] platí, že:
#   1. a <= b,
#   2. všechny intervaly v levém podstromě obsahují hodnoty menší než 'a',
#   3. všechny intervaly v pravém podstromě obsahuji hodnoty větší než 'b'.
#
# Příklady nekorektních H-stromu:
#
#        [4,3]                      [7,8]
#       /     \                    /     \
#  [1,2]       [5,7]          [6,6]       [10,12]
#                                  \
#                                   [8,9]
# Příklad korektního H-stromu:
#            [6,6]
#          /       \
#      [1,3]        [9,10]
#    /       \             \
# [-7,0]      [4,5]         [14,19]


def is_correct(tree: HTree) -> bool:
    """
    vstup: 'tree' H-strom typu HTree,
    vystup: True, pokud strom 'tree' je korektním H-stromem
            False jinak
            Funkce nemodifikuje zadaný strom.
    časová složitost: O(n), kde n je počet uzlů stromu 'tree'
    extra prostorová složitost: O(h), kde h je výška stromu 'tree'
        (Do extra prostorové složitost nepočítáme velikost vstupu, ale
         počítáme do ní zásobník rekurze.)
    """
    if tree is None or tree.root is None:
        return True

    if tree.root.low > tree.root.high:
        return False

    return is_correct_rec(tree.root.left, -inf, tree.root.low) and is_correct_rec(tree.root.right, tree.root.high, inf)


def is_correct_rec(node: Optional[Node], minimum, maximum) -> bool:
    if node is None:
        return True

    if node.low > node.high or node.high >= maximum or node.low <= minimum:
        return False

    return is_correct_rec(node.left, minimum, node.low) and is_correct_rec(node.right, node.high, maximum)

# Úkol 2. insert (1 bod)
#
# Implementujte operaci 'insert', která vloži hodnotu 'key' do stromu 'tree'.
#
# Pokud existuje ve stromě 'tree' pasivní uzel s intervalem [a, b], do kterého
# je lze vložit hodnotu 'key' (tj. a <= key <= b), tak se tento uzel nahradí
# aktivním uzlem s intervalem [key, key].
#
# Jinak funguje vkládání stejně jako vkládání do binárního vyhledávacího
# stromu, tedy vytvoří aktivní uzel s intervalem [key, key] na správném místě.
#
# Pokud se ve stromě hodnota již nachází, tedy existuje aktivní uzel
# s intervalem [a, b] takovým, že a <= key <= b, tak operace strom nezmění.
#
# Příklad stromu t:
#
#       [4,6]
#      /     \
# [1,2]       [8,10]*
#
# strom po provedení operace insert(t, 5)
#
#       [5,5]*
#      /     \
# [1,2]       [8,10]*
#
# strom po následném provedení operace insert(t, 7)
#
#       [5,5]*
#      /     \
# [1,2]       [8,10]*
#            /
#       [7,7]*


def insert(tree: HTree, key: int) -> None:
    """
    vstup: 'tree' korektní H-strom typu HTree
           'key'  vkládaný klíč
    vystup: žádný, modifikuje zadaný H-strom dle popisu výše
    časová složitost: O(h), kde h je výška stromu 'tree'
    """
    if tree.root is None:
        tree.root = Node(key, key, True)
        return

    if tree.root.low <= key <= tree.root.high:  # kluc sa nachadza v intervale
        if tree.root.active:  # ak v aktivnom tak nic nerobim
            return
        # ak v neaktivnom tak len prepisem hodnoty low a high
        tree.root.low = key
        tree.root.high = key
        tree.root.active = True
        return

    if key < tree.root.low:
        insert_rec(tree.root, tree.root.left, key, True)
    else:
        insert_rec(tree.root, tree.root.right, key, False)


def insert_rec(parent: Node, node: Optional[Node], key: int, is_left: bool):
    if node is None:  # kluc key sa v povodnom strome nenachadza
        if is_left:  # z parenta som siel dolava tak insertnem laveho syna
            parent.left = Node(key, key, True)
        else:  # z parenta som siel doprava tak insertnem praveho syna
            parent.right = Node(key, key, True)
        return

    if node.low <= key <= node.high:  # kluc sa nachadza v intervale
        if node.active:  # ak v aktivnom tak nic nerobim
            return
        # ak v neaktivnom tak len prepisem hodnoty low a high
        node.low = key
        node.high = key
        node.active = True
        return

    # nie sme ani v liste ani v spravnom intervale
    if key < node.low:
        insert_rec(node, node.left, key, True)
    else:
        insert_rec(node, node.right, key, False)


# Úkol 3. delete (1 bod)
#
# Implementujte operaci 'delete', která smaže hodnotu 'key' z aktivního uzlu
# H-stromu 'tree'. Pokud se hodnota ve stromě nenachází, operace delete nedělá
# nic.
#
# Pokud se hodnota 'key' nachází uvnitř aktivního intervalu [a, b],
# 1. operace vytvoří pasivní uzel s intervalem [key, key] na místě původního
#    uzlu a
# 2. rozdělí původní interval [a, b] na 2 aktivní uzly s intervaly [a, key - 1]
#    a [key + 1, b] a umístí je na pozici předchůdce, resp. následníka uzlu,
#    z nějž byla hodnota 'key' smazána.
#    V případě, že se hodnota 'key' rovná levé (resp. pravé) hranici původního
#    intervalu, tak se uzel s intervalem [a, key - 1] (resp. [key + 1, b])
#    nevytvoří.
#
# Příklad:
#
# iniciální strom t:
#
#          [4,7]*
#         /     \
#    [2,3]       [8,10]*
#
# delete(t, 5):
#
#       [5,5]
#      /     \
# [2,3]       [8,10]*
#      \     /
#    [4,4]* [6,7]*
#
# a poté delete(t, 8):
#
#       [5,5]
#      /     \
# [2,3]       [8,8]
#      \      /    \
#    [4,4]* [6,7]*  [9,10]*


def delete(tree: HTree, key: int) -> None:
    """
    vstup: 'tree' H-strom typu HTree
           'key'  klíč ke smazání
    vystup: žadný, modifikuje zadaný H-strom podle popisu výše
    časová složitost: O(h), kde h je výška stromu 'tree'
    """
    if tree is None or tree.root is None:
        return

    may_be_root = delete_node(tree.root, key, None, False)
    if may_be_root is not None:
        tree.root = may_be_root


def implant(low: int, high: int, node: Node) -> Tuple[Node, bool]:
    """
    :param low: dolna hranica intervalu, ktory chcem pridat do podstromu s korenom node
    :param high: horna hranica intervalu, ktory chcem pridat do podstromu s korenom node
    :param node: koren podstromu, kam vkladam interval
    :return: parent node intervalu, ktory chcem pridat; true ak to ma byt lavy potomok, false inak
    """
    if low > node.high:
        if node.right is None:
            return node, False
        return implant(low, high, node.right)
    elif high < node.low:
        if node.left is None:
            return node, True
        return implant(low, high, node.left)


def delete_node(node: Node, key: int, parent, is_left) -> Optional[Node]:
    """
    :param node: koren podstromu, v ktorom chcem vymazat hodnotu key
    :param key: hodnota, ktora ma byt odstranena zo stromu
    :param parent: rodicovsky uzol uzlu node, None ak je to koren stromu
    :param is_left: true ak node je lavy podstrom svojho rodica, false inak
    :return: ak sa rozbijal koren povodneho stromu, tak vrati novy koren, inak None
    """
    if node is None:
        return
    if (node.low <= key <= node.high) and node.active:
        new_node = Node(key, key, False)
        # lavy podstrom
        if node.low == key:  # dolna hranica je rovna key, netreba vytvarat novy uzol
            new_node.left = node.left
        else:  # treba vyrobit nocy uzol a korektne ho vlozit do podstromu
            new_left_node = Node(node.low, key - 1, True)
            if node.left is None:
                new_node.left = new_left_node
            else:  # hladanie korektneho umiestnenie noveho uzla v lavom podstrome
                insert_node, left = implant(node.low, key - 1, node.left)
                if left:
                    insert_node.left = new_left_node
                else:
                    insert_node.right = new_left_node
                new_node.left = node.left

        # pravy podstrom
        if node.high == key:  # horna hranica je rovna key, netreba vytvarat novy uzol
            new_node.right = node.right
        else:  # treba vyrobit nocy uzol a korektne ho vlozit do podstromu
            new_right_node = Node(key + 1, node.high, True)
            if node.right is None:
                new_node.right = new_right_node
            else:  # hladanie korektneho umiestnenie noveho uzla v pravom podstrome
                insert_node, left = implant(key + 1, node.high, node.right)
                if left:
                    insert_node.left = new_right_node
                else:
                    insert_node.right = new_right_node
                new_node.right = node.right
        # fcia rozbila koren povodneho stromu
        if parent is None:
            return new_node
        # fcia nerzbila koren, iba sa upravi potomok rodica uzlu, ktory sa rozbil
        if is_left:
            parent.left = new_node
        else:
            parent.right = new_node
    # key sa nenachadzal v aktualnom node
    elif node.low > key:
        delete_node(node.left, key, node, True)
    elif node.high < key:
        delete_node(node.right, key, node, False)


# Soubory .dot z testů vykreslíte např. programem xdot;
# případně použijte online verzi: http://dreampuf.github.io/GraphvizOnline/
#
# Pokud si pro ladění kódu chcete vypsat vlastní strom, můžete použít
# funkci draw_tree. Druhým parametrem je jméno souboru (např. „my_tree.dot“).


########################################################################
#               Nasleduje kod testu, NEMODIFIKUJTE JEJ                 #
########################################################################


class Ib002TreePrinter:
    def __init__(self, tree: HTree, filename: str):
        self.tree = tree
        self.f = open(filename, 'w')
        self.counter = 0

    def make_node(self, node: Node) -> None:
        if node.active:
            colour = ",color=red,fontcolor=red"
            star = "*"
        else:
            colour = star = ""

        self.f.write(f'{id(node)} '
                     f'[label="[{node.low},{node.high}]{star}"{colour}];\n')

    def make_edge(self, n1: Node, n2: Optional[Node]) -> None:
        if n2 is None:
            null = f"null{self.counter}"
            self.counter += 1
            self.f.write(f"{null} [shape=point];\n{id(n1)} -> {null}\n")
        else:
            self.f.write(f"{id(n1)} -> {id(n2)}\n")

    def make_graphviz(self, node: Optional[Node]) -> None:
        if node is None:
            return

        self.make_node(node)

        for child in node.left, node.right:
            self.make_edge(node, child)
            self.make_graphviz(child)

    def draw_tree(self) -> None:
        self.f.write('digraph Tree {\nnode [color=black, ordering="out"];\n')
        self.make_graphviz(self.tree.root)
        self.f.write("}\n")
        self.f.close()


def draw_tree(tree: HTree, filename: str) -> None:
    """
    Vygeneruje do souboru `filename` reprezentaci stromu `tree` pro graphviz.
    """
    Ib002TreePrinter(tree, filename).draw_tree()


def ib002_build_tree(array: Optional[List[Any]]) -> Optional[Node]:
    if not array:
        return None

    node = Node(array[0][0], array[0][1], array[0][2])
    node.left = ib002_build_tree(array[1])
    node.right = ib002_build_tree(array[2])
    return node


class Ib002TestCase:
    def __init__(self, array: List[Any], correct: bool):
        self.tree = HTree()
        self.tree.root = ib002_build_tree(array)
        self.correct = correct

        self.array = array if array else None
        self.inputs: List[Any] = []
        self.remove: List[Any] = []
        self.expected = None
        self.tree_copy: Optional[HTree] = None

    def copy_node(self, node: Optional[Node]) -> Optional[Node]:
        if not node:
            return None
        new = Node(node.low, node.high, node.active)
        new.left = self.copy_node(node.left)
        new.right = self.copy_node(node.right)
        return new

    def get_tree(self) -> HTree:
        self.tree_copy = HTree()
        self.tree_copy.root = self.copy_node(self.tree.root)
        return self.tree_copy

    def add_insert(self, cases: List[Any]) -> 'Ib002TestCase':
        self.inputs = cases
        return self

    def add_remove(self, cases: List[Any]) -> 'Ib002TestCase':
        self.remove = cases
        return self

    def to_array(self, node: Optional[Node]) -> Optional[List[Any]]:
        return None if node is None else \
            [(node.low, node.high, node.active),
             self.to_array(node.left), self.to_array(node.right)]

    def to_key_array(self, node: Optional[Node]) \
            -> List[Tuple[int, int, bool]]:
        return [] if node is None else \
            self.to_key_array(node.left) + \
            [(node.low, node.high, node.active)] + \
            self.to_key_array(node.right)

    def check_tree(self) -> bool:
        if self.array == self.to_array(self.tree.root):
            return True

        print("Došlo k modifikaci vstupního stromu.")
        self.tree_copy = None  # invalidate the copy
        return False


IB002_CASES = [
    # 0
    Ib002TestCase([(6, 6, False),
                   [(1, 3, False), [(-7, 0, False), None, None],
                    [(4, 5, False), None, None]],
                   [(9, 10, False), None,
                    [(14, 19, False), None, None]]],
                  True)
    .add_insert([(6,
                  [(6, 6, True),
                   [(1, 3, False), [(-7, 0, False), None, None],
                    [(4, 5, False), None, None]],
                   [(9, 10, False), None,
                    [(14, 19, False), None, None]]]),
                 (1,
                  [(6, 6, False),
                   [(1, 1, True), [(-7, 0, False), None, None],
                    [(4, 5, False), None, None]],
                   [(9, 10, False), None,
                    [(14, 19, False), None, None]]]),
                 (3,
                  [(6, 6, False),
                   [(3, 3, True), [(-7, 0, False), None, None],
                    [(4, 5, False), None, None]],
                   [(9, 10, False), None,
                    [(14, 19, False), None, None]]]),
                 (-10,
                  [(6, 6, False),
                   [(1, 3, False),
                    [(-7, 0, False), [(-10, -10, True), None, None],
                     None],
                    [(4, 5, False), None, None]],
                   [(9, 10, False), None,
                    [(14, 19, False), None, None]]]),
                 (-4,
                  [(6, 6, False),
                   [(1, 3, False), [(-4, -4, True), None, None],
                    [(4, 5, False), None, None]],
                   [(9, 10, False), None,
                    [(14, 19, False), None, None]]]),
                 (5,
                  [(6, 6, False),
                   [(1, 3, False), [(-7, 0, False), None, None],
                    [(5, 5, True), None, None]],
                   [(9, 10, False), None,
                    [(14, 19, False), None, None]]]),
                 (9,
                  [(6, 6, False),
                   [(1, 3, False), [(-7, 0, False), None, None],
                    [(4, 5, False), None, None]],
                   [(9, 9, True), None, [(14, 19, False), None, None]]]),
                 (10,
                  [(6, 6, False),
                   [(1, 3, False), [(-7, 0, False), None, None],
                    [(4, 5, False), None, None]],
                   [(10, 10, True), None,
                    [(14, 19, False), None, None]]]),
                 (11,
                  [(6, 6, False),
                   [(1, 3, False), [(-7, 0, False), None, None],
                    [(4, 5, False), None, None]],
                   [(9, 10, False), None,
                    [(14, 19, False), [(11, 11, True), None, None],
                     None]]]),
                 (14,
                  [(6, 6, False),
                   [(1, 3, False), [(-7, 0, False), None, None],
                    [(4, 5, False), None, None]],
                   [(9, 10, False), None,
                    [(14, 14, True), None, None]]]),
                 (16,
                  [(6, 6, False),
                   [(1, 3, False), [(-7, 0, False), None, None],
                    [(4, 5, False), None, None]],
                   [(9, 10, False), None,
                    [(16, 16, True), None, None]]]),
                 (19,
                  [(6, 6, False),
                   [(1, 3, False), [(-7, 0, False), None, None],
                    [(4, 5, False), None, None]],
                   [(9, 10, False), None,
                    [(19, 19, True), None, None]]]),
                 (22,
                  [(6, 6, False),
                   [(1, 3, False), [(-7, 0, False), None, None],
                    [(4, 5, False), None, None]],
                   [(9, 10, False), None,
                    [(14, 19, False), None,
                     [(22, 22, True), None, None]]]])]),
    # 1
    Ib002TestCase([(4, 3, False), [(1, 2, False), None, None],
                   [(5, 7, False), None, None]],
                  False),
    # 2
    Ib002TestCase([(7, 8, False),
                   [(6, 6, False), None, [(8, 9, False), None, None]],
                   [(10, 12, False), None, None]],
                  False),
    # 3
    Ib002TestCase([(4, 6, False), [(1, 3, False), None, None],
                   [(8, 10, True), None, None]],
                  True)
    .add_insert([(-1,
                  [(4, 6, False),
                   [(1, 3, False), [(-1, -1, True), None, None], None],
                   [(8, 10, True), None, None]]),
                 (0,
                  [(4, 6, False),
                   [(1, 3, False), [(0, 0, True), None, None], None],
                   [(8, 10, True), None, None]]),
                 (1,
                  [(4, 6, False), [(1, 1, True), None, None],
                   [(8, 10, True), None, None]]),
                 (2,
                  [(4, 6, False), [(2, 2, True), None, None],
                   [(8, 10, True), None, None]]),
                 (3,
                  [(4, 6, False), [(3, 3, True), None, None],
                   [(8, 10, True), None, None]]),
                 (4,
                  [(4, 4, True), [(1, 3, False), None, None],
                   [(8, 10, True), None, None]]),
                 (5,
                  [(5, 5, True), [(1, 3, False), None, None],
                   [(8, 10, True), None, None]]),
                 (6,
                  [(6, 6, True), [(1, 3, False), None, None],
                   [(8, 10, True), None, None]]),
                 (8,
                  [(4, 6, False), [(1, 3, False), None, None],
                   [(8, 10, True), None, None]]),
                 (9,
                  [(4, 6, False), [(1, 3, False), None, None],
                   [(8, 10, True), None, None]]),
                 (10,
                  [(4, 6, False), [(1, 3, False), None, None],
                   [(8, 10, True), None, None]]),
                 (15,
                  [(4, 6, False), [(1, 3, False), None, None],
                   [(8, 10, True), None, [(15, 15, True), None, None]]])]),
    # 4
    Ib002TestCase([(4, 5, True),
                   [(1, 2, True), None, [(3, 3, True), None, None]],
                   [(7, 7, True), None, [(8, 9, False), None, None]]],
                  True)
    .add_insert([(-1,
                  [(4, 5, True),
                   [(1, 2, True), [(-1, -1, True), None, None],
                    [(3, 3, True), None, None]],
                   [(7, 7, True), None, [(8, 9, False), None, None]]]),
                 (0,
                  [(4, 5, True),
                   [(1, 2, True), [(0, 0, True), None, None],
                    [(3, 3, True), None, None]],
                   [(7, 7, True), None, [(8, 9, False), None, None]]]),
                 (1,
                  [(4, 5, True),
                   [(1, 2, True), None, [(3, 3, True), None, None]],
                   [(7, 7, True), None, [(8, 9, False), None, None]]]),
                 (2,
                  [(4, 5, True),
                   [(1, 2, True), None, [(3, 3, True), None, None]],
                   [(7, 7, True), None, [(8, 9, False), None, None]]]),
                 (8,
                  [(4, 5, True),
                   [(1, 2, True), None, [(3, 3, True), None, None]],
                   [(7, 7, True), None, [(8, 8, True), None, None]]]),
                 (10,
                  [(4, 5, True),
                   [(1, 2, True), None, [(3, 3, True), None, None]],
                   [(7, 7, True), None,
                    [(8, 9, False), None,
                     [(10, 10, True), None, None]]]]),
                 (15,
                  [(4, 5, True),
                   [(1, 2, True), None, [(3, 3, True), None, None]],
                   [(7, 7, True), None,
                    [(8, 9, False), None,
                     [(15, 15, True), None, None]]]])])
    .add_remove([(1,
                  [(4, 5, True),
                   [(1, 1, False), None,
                    [(3, 3, True), [(2, 2, True), None, None], None]],
                   [(7, 7, True), None, [(8, 9, False), None, None]]]),
                 (2,
                  [(4, 5, True),
                   [(2, 2, False), [(1, 1, True), None, None],
                    [(3, 3, True), None, None]],
                   [(7, 7, True), None, [(8, 9, False), None, None]]]),
                 (3,
                  [(4, 5, True),
                   [(1, 2, True), None, [(3, 3, False), None, None]],
                   [(7, 7, True), None, [(8, 9, False), None, None]]]),
                 (4,
                  [(4, 4, False),
                   [(1, 2, True), None, [(3, 3, True), None, None]],
                   [(7, 7, True), [(5, 5, True), None, None],
                    [(8, 9, False), None, None]]]),
                 (5,
                  [(5, 5, False),
                   [(1, 2, True), None,
                    [(3, 3, True), None, [(4, 4, True), None, None]]],
                   [(7, 7, True), None, [(8, 9, False), None, None]]]),
                 (7,
                  [(4, 5, True),
                   [(1, 2, True), None, [(3, 3, True), None, None]],
                   [(7, 7, False), None, [(8, 9, False), None, None]]]),
                 (10,
                  [(4, 5, True),
                   [(1, 2, True), None, [(3, 3, True), None, None]],
                   [(7, 7, True), None, [(8, 9, False), None, None]]])]),
    # 5
    Ib002TestCase([(4, 5, False),
                   [(1, 2, False), None, [(3, 3, False), None, None]],
                   [(6, 7, True), None, [(8, 9, False), None, None]]],
                  True)
    .add_insert([(-1,
                  [(4, 5, False),
                   [(1, 2, False), [(-1, -1, True), None, None],
                    [(3, 3, False), None, None]],
                   [(6, 7, True), None, [(8, 9, False), None, None]]]),
                 (0,
                  [(4, 5, False),
                   [(1, 2, False), [(0, 0, True), None, None],
                    [(3, 3, False), None, None]],
                   [(6, 7, True), None, [(8, 9, False), None, None]]]),
                 (1,
                  [(4, 5, False),
                   [(1, 1, True), None, [(3, 3, False), None, None]],
                   [(6, 7, True), None, [(8, 9, False), None, None]]]),
                 (3,
                  [(4, 5, False),
                   [(1, 2, False), None, [(3, 3, True), None, None]],
                   [(6, 7, True), None, [(8, 9, False), None, None]]]),
                 (9,
                  [(4, 5, False),
                   [(1, 2, False), None, [(3, 3, False), None, None]],
                   [(6, 7, True), None, [(9, 9, True), None, None]]])])
    .add_remove([(6,
                  [(4, 5, False),
                   [(1, 2, False), None, [(3, 3, False), None, None]],
                   [(6, 6, False), None,
                    [(8, 9, False), [(7, 7, True), None, None], None]]]),
                 (7,
                  [(4, 5, False),
                   [(1, 2, False), None, [(3, 3, False), None, None]],
                   [(7, 7, False), [(6, 6, True), None, None],
                    [(8, 9, False), None, None]]])]),
    # 6
    Ib002TestCase([(7, 8, True),
                   [(2, 3, True), [(1, 1, True), None, None],
                    [(4, 6, True), None, None]],
                   [(10, 11, True), [(9, 9, True), None, None],
                    [(12, 13, True), None, None]]],
                  True)
    .add_remove([(0,
                  [(7, 8, True),
                   [(2, 3, True), [(1, 1, True), None, None],
                    [(4, 6, True), None, None]],
                   [(10, 11, True), [(9, 9, True), None, None],
                    [(12, 13, True), None, None]]]),
                 (1,
                  [(7, 8, True),
                   [(2, 3, True), [(1, 1, False), None, None],
                    [(4, 6, True), None, None]],
                   [(10, 11, True), [(9, 9, True), None, None],
                    [(12, 13, True), None, None]]]),
                 (2,
                  [(7, 8, True),
                   [(2, 2, False), [(1, 1, True), None, None],
                    [(4, 6, True), [(3, 3, True), None, None], None]],
                   [(10, 11, True), [(9, 9, True), None, None],
                    [(12, 13, True), None, None]]]),
                 (3,
                  [(7, 8, True),
                   [(3, 3, False),
                    [(1, 1, True), None, [(2, 2, True), None, None]],
                    [(4, 6, True), None, None]],
                   [(10, 11, True), [(9, 9, True), None, None],
                    [(12, 13, True), None, None]]]),
                 (4,
                  [(7, 8, True),
                   [(2, 3, True), [(1, 1, True), None, None],
                    [(4, 4, False), None, [(5, 6, True), None, None]]],
                   [(10, 11, True), [(9, 9, True), None, None],
                    [(12, 13, True), None, None]]]),
                 (5,
                  [(7, 8, True),
                   [(2, 3, True), [(1, 1, True), None, None],
                    [(5, 5, False), [(4, 4, True), None, None],
                     [(6, 6, True), None, None]]],
                   [(10, 11, True), [(9, 9, True), None, None],
                    [(12, 13, True), None, None]]]),
                 (6,
                  [(7, 8, True),
                   [(2, 3, True), [(1, 1, True), None, None],
                    [(6, 6, False), [(4, 5, True), None, None], None]],
                   [(10, 11, True), [(9, 9, True), None, None],
                    [(12, 13, True), None, None]]]),
                 (7,
                  [(7, 7, False),
                   [(2, 3, True), [(1, 1, True), None, None],
                    [(4, 6, True), None, None]],
                   [(10, 11, True),
                    [(9, 9, True), [(8, 8, True), None, None], None],
                    [(12, 13, True), None, None]]]),
                 (8,
                  [(8, 8, False),
                   [(2, 3, True), [(1, 1, True), None, None],
                    [(4, 6, True), None, [(7, 7, True), None, None]]],
                   [(10, 11, True), [(9, 9, True), None, None],
                    [(12, 13, True), None, None]]]),
                 (9,
                  [(7, 8, True),
                   [(2, 3, True), [(1, 1, True), None, None],
                    [(4, 6, True), None, None]],
                   [(10, 11, True), [(9, 9, False), None, None],
                    [(12, 13, True), None, None]]]),
                 (10,
                  [(7, 8, True),
                   [(2, 3, True), [(1, 1, True), None, None],
                    [(4, 6, True), None, None]],
                   [(10, 10, False), [(9, 9, True), None, None],
                    [(12, 13, True), [(11, 11, True), None, None],
                     None]]]),
                 (11,
                  [(7, 8, True),
                   [(2, 3, True), [(1, 1, True), None, None],
                    [(4, 6, True), None, None]],
                   [(11, 11, False),
                    [(9, 9, True), None, [(10, 10, True), None, None]],
                    [(12, 13, True), None, None]]]),
                 (12,
                  [(7, 8, True),
                   [(2, 3, True), [(1, 1, True), None, None],
                    [(4, 6, True), None, None]],
                   [(10, 11, True), [(9, 9, True), None, None],
                    [(12, 12, False), None,
                     [(13, 13, True), None, None]]]]),
                 (13,
                  [(7, 8, True),
                   [(2, 3, True), [(1, 1, True), None, None],
                    [(4, 6, True), None, None]],
                   [(10, 11, True), [(9, 9, True), None, None],
                    [(13, 13, False), [(12, 12, True), None, None],
                     None]]]),
                 (14,
                  [(7, 8, True),
                   [(2, 3, True), [(1, 1, True), None, None],
                    [(4, 6, True), None, None]],
                   [(10, 11, True), [(9, 9, True), None, None],
                    [(12, 13, True), None, None]]])]),
    # 7
    Ib002TestCase([], True)
    .add_insert([(1, [(1, 1, True), None, None])])
    .add_remove([(7, None)]),
    # 8
    Ib002TestCase([(4, 8, False), [(1, 4, False), None, None], None],
                  False),
    # 9
    Ib002TestCase([(4, 8, False), None, [(8, 12, False), None, None]],
                  False),
    # 10
    Ib002TestCase([(4, 8, True),
                   [(2, 3, True),
                    [(1, 1, True), [(0, 0, True), None, None], None],
                    None],
                   [(9, 9, True), None,
                    [(10, 12, True), None,
                     [(13, 14, True), None,
                      [(15, 20, True), None, None]]]]],
                  True)
    .add_insert([(15,
                  [(4, 8, True),
                   [(2, 3, True),
                    [(1, 1, True), [(0, 0, True), None, None], None],
                    None],
                   [(9, 9, True), None,
                    [(10, 12, True), None,
                     [(13, 14, True), None,
                      [(15, 20, True), None, None]]]]]),
                 (16,
                  [(4, 8, True),
                   [(2, 3, True),
                    [(1, 1, True), [(0, 0, True), None, None], None],
                    None],
                   [(9, 9, True), None,
                    [(10, 12, True), None,
                     [(13, 14, True), None,
                      [(15, 20, True), None, None]]]]]),
                 (21,
                  [(4, 8, True),
                   [(2, 3, True),
                    [(1, 1, True), [(0, 0, True), None, None], None],
                    None],
                   [(9, 9, True), None,
                    [(10, 12, True), None,
                     [(13, 14, True), None,
                      [(15, 20, True), None,
                       [(21, 21, True), None, None]]]]]])])
    .add_remove([(1,
                  [(4, 8, True),
                   [(2, 3, True),
                    [(1, 1, False), [(0, 0, True), None, None], None],
                    None],
                   [(9, 9, True), None,
                    [(10, 12, True), None,
                     [(13, 14, True), None,
                      [(15, 20, True), None, None]]]]]),
                 (5,
                  [(5, 5, False),
                   [(2, 3, True),
                    [(1, 1, True), [(0, 0, True), None, None], None],
                    [(4, 4, True), None, None]],
                   [(9, 9, True), [(6, 8, True), None, None],
                    [(10, 12, True), None,
                     [(13, 14, True), None,
                      [(15, 20, True), None, None]]]]]),
                 (3,
                  [(4, 8, True),
                   [(3, 3, False),
                    [(1, 1, True), [(0, 0, True), None, None],
                     [(2, 2, True), None, None]],
                    None],
                   [(9, 9, True), None,
                    [(10, 12, True), None,
                     [(13, 14, True), None,
                      [(15, 20, True), None, None]]]]]),
                 (11,
                  [(4, 8, True),
                   [(2, 3, True),
                    [(1, 1, True), [(0, 0, True), None, None], None],
                    None],
                   [(9, 9, True), None,
                    [(11, 11, False), [(10, 10, True), None, None],
                     [(13, 14, True), [(12, 12, True), None, None],
                      [(15, 20, True), None, None]]]]]),
                 (4,
                  [(4, 4, False),
                   [(2, 3, True),
                    [(1, 1, True), [(0, 0, True), None, None], None],
                    None],
                   [(9, 9, True), [(5, 8, True), None, None],
                    [(10, 12, True), None,
                     [(13, 14, True), None,
                      [(15, 20, True), None, None]]]]]),
                 (17,
                  [(4, 8, True),
                   [(2, 3, True),
                    [(1, 1, True), [(0, 0, True), None, None], None],
                    None],
                   [(9, 9, True), None,
                    [(10, 12, True), None,
                     [(13, 14, True), None,
                      [(17, 17, False), [(15, 16, True), None, None],
                       [(18, 20, True), None, None]]]]]])]),
    # 11
    Ib002TestCase([(24, 27, False),
                   [(15, 16, True),
                    [(10, 14, True), [(0, 9, False), None, None], None],
                    [(17, 22, True), None,
                     [(23, 23, False), None, None]]],
                   None],
                  True)
    .add_insert([(25,
                  [(25, 25, True),
                   [(15, 16, True),
                    [(10, 14, True), [(0, 9, False), None, None], None],
                    [(17, 22, True), None,
                     [(23, 23, False), None, None]]],
                   None]),
                 (23,
                  [(24, 27, False),
                   [(15, 16, True),
                    [(10, 14, True), [(0, 9, False), None, None], None],
                    [(17, 22, True), None,
                     [(23, 23, True), None, None]]],
                   None]),
                 (7,
                  [(24, 27, False),
                   [(15, 16, True),
                    [(10, 14, True), [(7, 7, True), None, None], None],
                    [(17, 22, True), None,
                     [(23, 23, False), None, None]]],
                   None])])
    .add_remove([(16,
                  [(24, 27, False),
                   [(16, 16, False),
                    [(10, 14, True), [(0, 9, False), None, None],
                     [(15, 15, True), None, None]],
                    [(17, 22, True), None,
                     [(23, 23, False), None, None]]],
                   None]),
                 (19,
                  [(24, 27, False),
                   [(15, 16, True),
                    [(10, 14, True), [(0, 9, False), None, None], None],
                    [(19, 19, False), [(17, 18, True), None, None],
                     [(23, 23, False), [(20, 22, True), None, None],
                      None]]],
                   None]),
                 (10,
                  [(24, 27, False),
                   [(15, 16, True),
                    [(10, 10, False), [(0, 9, False), None, None],
                     [(11, 14, True), None, None]],
                    [(17, 22, True), None,
                     [(23, 23, False), None, None]]],
                   None])]),
    # 12
    Ib002TestCase([(24, 27, False),
                   [(15, 16, True),
                    [(10, 14, True), [(0, 9, False), None, None], None],
                    [(17, 23, True), None, None]],
                   None],
                  True),
    # 13
    Ib002TestCase([(24, 27, True),
                   [(15, 16, False),
                    [(10, 14, False), [(0, 9, True), None, None], None],
                    [(17, 22, False), None,
                     [(23, 23, True), None, None]]],
                   None],
                  True)
    .add_remove([(25,
                  [(25, 25, False),
                   [(15, 16, False),
                    [(10, 14, False), [(0, 9, True), None, None], None],
                    [(17, 22, False), None,
                     [(23, 23, True), None,
                      [(24, 24, True), None, None]]]],
                   [(26, 27, True), None, None]])]),
    # 14
    Ib002TestCase([(93, 95, True),
                   [(45, 47, True),
                    [(21, 23, True),
                     [(9, 11, True),
                      [(3, 5, True),
                       [(0, 2, True), None, None],
                       [(6, 8, True), None, None]],
                      [(15, 17, True),
                       [(12, 14, True), None, None],
                       [(18, 20, True), None, None]]],
                     [(33, 35, True),
                      [(27, 29, True),
                       [(24, 26, True), None, None],
                       [(30, 32, True), None, None]],
                      [(39, 41, True),
                       [(36, 38, True), None, None],
                       [(42, 44, True), None, None]]]],
                    [(69, 71, True),
                     [(57, 59, True),
                      [(51, 53, True),
                       [(48, 50, True), None, None],
                       [(54, 56, True), None, None]],
                      [(63, 65, True),
                       [(60, 62, True), None, None],
                       [(66, 68, True), None, None]]],
                     [(81, 83, True),
                      [(75, 77, True),
                       [(72, 74, True), None, None],
                       [(78, 80, True), None, None]],
                      [(87, 89, True),
                       [(84, 86, True), None, None],
                       [(90, 92, True), None, None]]]]],
                   [(141, 143, False),
                    [(117, 119, False),
                     [(105, 107, False),
                      [(99, 101, False),
                       [(96, 98, False), None, None],
                       [(102, 104, False), None, None]],
                      [(111, 113, False),
                       [(108, 110, False), None, None],
                       [(114, 116, False), None, None]]],
                     [(129, 131, False),
                      [(123, 125, False),
                       [(120, 122, False), None, None],
                       [(126, 128, False), None, None]],
                      [(135, 137, False),
                       [(132, 134, False), None, None],
                       [(138, 140, False), None, None]]]],
                    [(165, 167, False),
                     [(153, 155, False),
                      [(147, 149, False),
                       [(144, 146, False), None, None],
                       [(150, 152, False), None, None]],
                      [(159, 161, False),
                       [(156, 158, False), None, None],
                       [(162, 164, False), None, None]]],
                     [(177, 179, False),
                      [(171, 173, False),
                       [(168, 170, False), None, None],
                       [(174, 176, False), None, None]],
                      [(183, 185, False),
                       [(180, 182, False), None, None],
                       [(186, 188, False), None, None]]]]]], True)
    .add_insert([(-1,
                  [(93, 95, True),
                   [(45, 47, True),
                    [(21, 23, True),
                     [(9, 11, True),
                      [(3, 5, True),
                       [(0, 2, True), [(-1, -1, True), None, None], None],
                       [(6, 8, True), None, None]],
                      [(15, 17, True),
                       [(12, 14, True), None, None],
                       [(18, 20, True), None, None]]],
                     [(33, 35, True),
                      [(27, 29, True),
                       [(24, 26, True), None, None],
                       [(30, 32, True), None, None]],
                      [(39, 41, True),
                       [(36, 38, True), None, None],
                       [(42, 44, True), None, None]]]],
                    [(69, 71, True),
                     [(57, 59, True),
                      [(51, 53, True),
                       [(48, 50, True), None, None],
                       [(54, 56, True), None, None]],
                      [(63, 65, True),
                       [(60, 62, True), None, None],
                       [(66, 68, True), None, None]]],
                     [(81, 83, True),
                      [(75, 77, True),
                       [(72, 74, True), None, None],
                       [(78, 80, True), None, None]],
                      [(87, 89, True),
                       [(84, 86, True), None, None],
                       [(90, 92, True), None, None]]]]],
                   [(141, 143, False),
                    [(117, 119, False),
                     [(105, 107, False),
                      [(99, 101, False),
                       [(96, 98, False), None, None],
                       [(102, 104, False), None, None]],
                      [(111, 113, False),
                       [(108, 110, False), None, None],
                       [(114, 116, False), None, None]]],
                     [(129, 131, False),
                      [(123, 125, False),
                       [(120, 122, False), None, None],
                       [(126, 128, False), None, None]],
                      [(135, 137, False),
                       [(132, 134, False), None, None],
                       [(138, 140, False), None, None]]]],
                    [(165, 167, False),
                     [(153, 155, False),
                      [(147, 149, False),
                       [(144, 146, False), None, None],
                       [(150, 152, False), None, None]],
                      [(159, 161, False),
                       [(156, 158, False), None, None],
                       [(162, 164, False), None, None]]],
                     [(177, 179, False),
                      [(171, 173, False),
                       [(168, 170, False), None, None],
                       [(174, 176, False), None, None]],
                      [(183, 185, False),
                       [(180, 182, False), None, None],
                       [(186, 188, False), None, None]]]]]]),
                 (166,
                  [(93, 95, True),
                   [(45, 47, True),
                    [(21, 23, True),
                     [(9, 11, True),
                      [(3, 5, True),
                       [(0, 2, True), None, None],
                       [(6, 8, True), None, None]],
                      [(15, 17, True),
                       [(12, 14, True), None, None],
                       [(18, 20, True), None, None]]],
                     [(33, 35, True),
                      [(27, 29, True),
                       [(24, 26, True), None, None],
                       [(30, 32, True), None, None]],
                      [(39, 41, True),
                       [(36, 38, True), None, None],
                       [(42, 44, True), None, None]]]],
                    [(69, 71, True),
                     [(57, 59, True),
                      [(51, 53, True),
                       [(48, 50, True), None, None],
                       [(54, 56, True), None, None]],
                      [(63, 65, True),
                       [(60, 62, True), None, None],
                       [(66, 68, True), None, None]]],
                     [(81, 83, True),
                      [(75, 77, True),
                       [(72, 74, True), None, None],
                       [(78, 80, True), None, None]],
                      [(87, 89, True),
                       [(84, 86, True), None, None],
                       [(90, 92, True), None, None]]]]],
                   [(141, 143, False),
                    [(117, 119, False),
                     [(105, 107, False),
                      [(99, 101, False),
                       [(96, 98, False), None, None],
                       [(102, 104, False), None, None]],
                      [(111, 113, False),
                       [(108, 110, False), None, None],
                       [(114, 116, False), None, None]]],
                     [(129, 131, False),
                      [(123, 125, False),
                       [(120, 122, False), None, None],
                       [(126, 128, False), None, None]],
                      [(135, 137, False),
                       [(132, 134, False), None, None],
                       [(138, 140, False), None, None]]]],
                    [(166, 166, True),
                     [(153, 155, False),
                      [(147, 149, False),
                       [(144, 146, False), None, None],
                       [(150, 152, False), None, None]],
                      [(159, 161, False),
                       [(156, 158, False), None, None],
                       [(162, 164, False), None, None]]],
                     [(177, 179, False),
                      [(171, 173, False),
                       [(168, 170, False), None, None],
                       [(174, 176, False), None, None]],
                      [(183, 185, False),
                       [(180, 182, False), None, None],
                       [(186, 188, False), None, None]]]]]])])
    .add_remove([(94,
                  [(94, 94, False),
                   [(45, 47, True),
                    [(21, 23, True),
                     [(9, 11, True),
                      [(3, 5, True),
                       [(0, 2, True), None, None],
                       [(6, 8, True), None, None]],
                      [(15, 17, True),
                       [(12, 14, True), None, None],
                       [(18, 20, True), None, None]]],
                     [(33, 35, True),
                      [(27, 29, True),
                       [(24, 26, True), None, None],
                       [(30, 32, True), None, None]],
                      [(39, 41, True),
                       [(36, 38, True), None, None],
                       [(42, 44, True), None, None]]]],
                    [(69, 71, True),
                     [(57, 59, True),
                      [(51, 53, True),
                       [(48, 50, True), None, None],
                       [(54, 56, True), None, None]],
                      [(63, 65, True),
                       [(60, 62, True), None, None],
                       [(66, 68, True), None, None]]],
                     [(81, 83, True),
                      [(75, 77, True),
                       [(72, 74, True), None, None],
                       [(78, 80, True), None, None]],
                      [(87, 89, True),
                       [(84, 86, True), None, None],
                       [(90, 92, True), None,
                        [(93, 93, True), None, None]]]]]],
                   [(141, 143, False),
                    [(117, 119, False),
                     [(105, 107, False),
                      [(99, 101, False),
                       [(96, 98, False), [(95, 95, True), None, None], None],
                       [(102, 104, False), None, None]],
                      [(111, 113, False),
                       [(108, 110, False), None, None],
                       [(114, 116, False), None, None]]],
                     [(129, 131, False),
                      [(123, 125, False),
                       [(120, 122, False), None, None],
                       [(126, 128, False), None, None]],
                      [(135, 137, False),
                       [(132, 134, False), None, None],
                       [(138, 140, False), None, None]]]],
                    [(165, 167, False),
                     [(153, 155, False),
                      [(147, 149, False),
                       [(144, 146, False), None, None],
                       [(150, 152, False), None, None]],
                      [(159, 161, False),
                       [(156, 158, False), None, None],
                       [(162, 164, False), None, None]]],
                     [(177, 179, False),
                      [(171, 173, False),
                       [(168, 170, False), None, None],
                       [(174, 176, False), None, None]],
                      [(183, 185, False),
                       [(180, 182, False), None, None],
                       [(186, 188, False), None, None]]]]]])]),
    # 15
    Ib002TestCase([(-(2 ** 27), 2 ** 65, True),
                   [(-(2 ** 100), -(2 ** 27) - 1, True), None, None],
                   [(2 ** 67, 2 ** 99, False), None, None]], True)
    .add_insert([(2 ** 66,
                 [(-(2 ** 27), 2 ** 65, True),
                  [(-(2 ** 100), -(2 ** 27) - 1, True), None, None],
                  [(2 ** 67, 2 ** 99, False),
                   [(2 ** 66, 2 ** 66, True), None, None], None]])])
    .add_remove([(0,
                 [(0, 0, False),
                  [(-(2 ** 100), -(2 ** 27) - 1, True), None,
                   [(-(2 ** 27), -1, True), None, None]],
                  [(2 ** 67, 2 ** 99, False),
                   [(1, 2 ** 65, True), None, None], None]])]),
    # 16
    Ib002TestCase([(24, 27, False),
                   [(15, 16, True),
                    [(10, 14, True), [(10, 9, False), None, None], None],
                    [(17, 23, True), None, None]],
                   None],
                  False),
    # 17
    Ib002TestCase([(24, 27, False),
                   [(15, 16, True),
                    [(10, 14, True), [(0, 9, False), None, None], None],
                    [(17, 23, True), None, None]],
                   None],
                  True)
    .add_remove([(25,
                 [(24, 27, False),
                  [(15, 16, True),
                   [(10, 14, True), [(0, 9, False), None, None], None],
                   [(17, 23, True), None, None]],
                  None])]),
    # 18
    Ib002TestCase([(24, 27, False),
                   [(15, 16, True),
                    [(10, 14, True), [(0, 9, False), None, None], None],
                    [(17, 23, True), None, None]],
                   None],
                  True)
    .add_insert([(25,
                 [(25, 25, True),
                  [(15, 16, True),
                   [(10, 14, True), [(0, 9, False), None, None], None],
                   [(17, 23, True), None, None]],
                  None])]),
    # 19
    Ib002TestCase([(24, 27, False), None, None],
                  True)
    .add_insert([(29,
                 [(24, 27, False), None, [(29, 29, True), None, None]])]),
]


IB002_BASIC = [[0, 1, 2, 7, 8, 9],
               [0, 3, 7, 10],
               [4, 5, 10, 11, 12],
               [5, 7, 10, 11, 12],
               [4, 5, 7, 10, 11]]


def ib002_test_report(ok: bool, basic: bool) -> bool:
    if ok:
        print("[ OK ] {} prošel.".format("Základní test" if basic else "Test"))
        return True

    if basic:
        print("[FAIL] Základní test neprošel.",
              "Tato část bude automaticky hodnocena 0 body.")
    else:
        print("[FAIL] Test neprošel.")

    return False


def ib002_test_header(msg: str, basic: bool) -> None:
    print("\n*** {} {}:".format("Základní test" if basic else "Test", msg))


def ib002_report_tree(name: str, tree: HTree,
                      tag: str = "input", adj: str = "Vstupní") -> None:
    filename = f"Er_{name}_{tag}.dot"
    draw_tree(tree, filename)
    print(adj + " H-strom je v souboru " + filename)


def ib002_report_output_tree(name: str, tree: HTree) -> None:
    ib002_report_tree(name, tree, "output", "Výsledný")


def ib002_report_expected_tree(name: str, tree: HTree) -> None:
    ib002_report_tree(name, tree, "expected", "Očekávaný")


def ib002_check_simple(result: Any, correct: Any) -> bool:
    if result == correct:
        return True
    print(f"Špatný výsledek {result}, měl být {correct}.")
    return False


Ib002Test = Tuple[Callable[..., Any], Callable[..., bool], int]


def ib002_check_iscorrect(_name: str, case: Ib002TestCase,
                          result: Any) -> bool:
    return ib002_check_simple(result, case.correct)


def ib002_check_expected(name: str, case: Ib002TestCase, result: Any) -> bool:
    stud = case.to_array(result.root)
    if stud == case.expected:
        return True

    tree = HTree()
    tree.root = ib002_build_tree(case.expected)
    ib002_report_output_tree(name, result)
    ib002_report_expected_tree(name, tree)
    return False


def ib002_run_checks(test: Ib002Test, case: Ib002TestCase,
                     result: Any, *args: Any) -> bool:
    name = test[0].__name__
    check = test[1]

    if (test[2] == 0 and not case.check_tree()) or \
       not check(name, case, result):
        ib002_report_tree(name, case.tree)
        if args:
            print("Vstupní parametr key:", args[0])
        return False

    return True


def ib002_check_array(fun: Callable[[HTree, int], None],
                      test: Ib002Test, name: str, case: Ib002TestCase,
                      data: List[Tuple[int, Any]]) -> bool:
    if not case.correct:
        return True
    for key, exp in data:
        case.expected = exp
        tree = case.get_tree()
        fun(tree, key)
        if not ib002_run_checks(test, case, tree, key):
            return False
        case.tree_copy = None
        case.expected = None
    return True


def ib002_test_template(test: Ib002Test, case: Ib002TestCase) -> bool:
    fun, _, which = test

    if which == 0:
        result = fun(case.tree)
        return ib002_run_checks(test, case, result)

    if which == 1:
        return ib002_check_array(fun, test, "insert", case, case.inputs)

    if which == 2:
        return ib002_check_array(fun, test, "delete", case, case.remove)

    return True


def ib002_run_test(test: Ib002Test, cases: Iterable[Ib002TestCase],
                   basic: bool) -> bool:
    msg = test[0].__name__
    ib002_test_header(msg, basic)

    return ib002_test_report(
        all(ib002_try_test(ib002_test_template, test, case)
            for case in cases), basic)


def ib002_run_both_tests(test: Ib002Test) -> bool:
    basic_cases = (IB002_CASES[i] for i in IB002_BASIC[test[2]])

    # if basic test fails, full tests are not run
    return ib002_run_test(test, basic_cases, basic=True) and \
        ib002_run_test(test, IB002_CASES, basic=False)


def ib002_try_test(test: Callable[..., bool], *args: Any) -> bool:
    import traceback
    import sys
    try:
        return test(*args)
    except Exception:
        print("Test vyhodil výjimku:")
        traceback.print_exc(file=sys.stdout)
        return False


IB002_TEST_DESCRIPTIONS: List[Ib002Test] = [
    (is_correct, ib002_check_iscorrect, 0),
    (insert, ib002_check_expected, 1),
    (delete, ib002_check_expected, 2),
]


def ib002_main() -> None:
    for test in IB002_TEST_DESCRIPTIONS:
        ib002_run_both_tests(test)


if __name__ == '__main__':
    ib002_main()
