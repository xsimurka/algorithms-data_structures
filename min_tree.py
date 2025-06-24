#!/usr/bin/env python3

# Povolené knihovny: typing, math

from typing import List, Optional, TextIO, Tuple

# IB002 Domácí úloha 7
#
# V tomto úkolu budeme pracovat s binárními stromy, kterým budeme říkat
# „levé minimové stromy“. Levé minimové stromy mají následující vlastnosti:
#
# * všechny listy levého minimového stromu jsou ve stejné hloubce;
# * levý minimový strom je zarovnaný doleva, což znamená, že:
#    a) pokud má některý uzel jen jednoho potomka, pak je to levý potomek;
#    b) pokud má některý uzel oba potomky, pak ten levý je kořenem perfektního
#       stromu (tj. úplného stromu se zaplněným posledním patrem);
# * klíče vnitřních uzlů jsou minima jejich podstromů
#   (skutečné hodnoty jsou tedy uloženy pouze v listech).
#
# Příklady levých minimových stromů:
#
#           1
#         /   \
#        2     1
#       / \   /
#      2   3 1
#
#         1
#      /     \
#     1       3
#    / \     /
#   2   1   3
#   ∧   ∧   ∧
#  2 3 1 4 3 5
#
# Příklady binárních stromů, které nejsou levými minimovými stromy:
#
#           1
#         /   \
#        2     1
#       / \
#      2   3
#  (porušuje první podmínku)
#
#           1
#         /   \
#        2     1
#       / \     \
#      2   3     1
#  (porušuje odrážku a) z druhé podmínky)
#
#           1
#         /   \
#        2     1
#       /     /
#      2     1
#  (porušuje odrážku b) z druhé podmínky)
#
#           1
#         /   \
#        2     0
#       / \   /
#      2   3 1
#  (porušuje třetí podmínku)
#
# Do následujících definic tříd nijak nezasahujte.
# Pro vykreslování stromů máte na konci tohoto souboru k dispozici
# funkci draw_tree.


class Node:
    """Třída Node reprezentuje uzel binárního stromu.

    Atributy:
        key     klíč uzlu
        left    odkaz na levý potomek uzlu nebo ‹None›
        right   odkaz na pravý potomek uzlu nebo ‹None›
    """
    __slots__ = "key", "left", "right"

    def __init__(self, key: int,
                 left: Optional['Node'] = None,
                 right: Optional['Node'] = None):
        self.key = key
        self.left = left
        self.right = right


class BinTree:
    """Třída BinTree reprezentuje binární strom.

    Atributy:
        root    odkaz na kořenový uzel stromu nebo ‹None›
    """
    __slots__ = "root"

    def __init__(self, root: Optional[Node] = None):
        self.root = root


# Část 1.
# Implementujte funkci build_min_tree, která vybuduje levý minimový strom
# se zadanými hodnotami v listech. Strom musí být co nejnižší.

def build_min_tree(leaves: List[int]) -> BinTree:
    """
    vstup: ‹leaves› – pole celých čísel
    výstup: korektní levý minimový strom, který má co nejmenší výšku
            a v listech obsahuje hodnoty z pole ‹leaves› ve stejném pořadí
            zleva doprava; funkce nijak nemodifikuje zadaný vstup
    časová složitost: O(n), kde n je délka pole ‹leaves›

    Příklad: Pro vstupy [2, 3, 1] a [2, 3, 1, 4, 3, 5] mají odpovídajícími
    výstupy být stromy uvedené výše.
    """
    if not leaves:
        return BinTree()

    act_level: List[Optional[Node]] = list(map(lambda x: Node(x), leaves))
    next_level: List[Node] = []

    while len(act_level) > 1:
        if len(act_level) % 2 == 1:
            act_level.append(None)

        for i in range(0, len(act_level), 2):
            left_son = act_level[i]
            right_son = act_level[i + 1]

            if right_son is None:
                parent_key = left_son.key
            else:
                parent_key = min(left_son.key, right_son.key)

            parent = Node(parent_key, left_son, right_son)
            next_level.append(parent)

        act_level = next_level
        next_level = []

    return BinTree(act_level[0])


# Část 2.
# Implementujte následující tři predikáty, které reprezentují výše uvedené tři
# podmínky levého minimového stromu. Každá predikát má jako vstupní podmínku
# platnost předchozích predikátů. Predikáty nemodifikují vstupní stromy.

def check_leaf_depth(tree: BinTree) -> bool:
    """
    vstup: ‹tree› – binární strom
    výstup: ‹True›, pokud mají všechny listy stromu stejnou hloubku;
            ‹False› jinak
    časová složitost: O(n), kde ‹n› je počet uzlů stromu
    extra prostorová složitost: O(h), kde ‹h› je výška stromu
        (Do extra prostorové složitost nepočítáme velikost vstupu, ale
         počítáme do ní zásobník rekurze.)
    """
    if tree.root is None:
        return True
    left = check_leaf_depth_rec(tree.root.left)
    right = check_leaf_depth_rec(tree.root.right)
    if left == -1 or right == -1:
        return False
    if left == 0 or right == 0:
        return True
    return left == right


def check_leaf_depth_rec(node: Optional[Node]) -> int:
    if node is None:
        return 0

    left = check_leaf_depth_rec(node.left)
    right = check_leaf_depth_rec(node.right)

    if left == -1 or right == -1:
        return -1
    if left == 0:
        return right + 1
    if right == 0:
        return left + 1
    if left == right:
        return left + 1
    return -1


def check_left_align(tree: BinTree) -> bool:
    """
    vstup: ‹tree› – binární strom, jehož všechny listy mají stejnou hloubku
                    (tj. předpokládáme, že platí ‹check_leaf_depth(tree)›)
    výstup: ‹True›, pokud je strom zarovnaný doleva (dle popisu nahoře);
            ‹False› jinak
    časová složitost: O(n), kde ‹n› je počet uzlů stromu
    extra prostorová složitost: O(h), kde ‹h› je výška stromu
        (Do extra prostorové složitost nepočítáme velikost vstupu, ale
         počítáme do ní zásobník rekurze.)
    """
    if tree.root is None:
        return True

    if tree.root.right is None and tree.root.left is None:
        return True

    if tree.root.left is None:
        return False

    if tree.root.right is None:
        return check_left_align_rec(tree.root.left, False)

    return check_left_align_rec(tree.root.right, False) and \
        check_left_align_rec(tree.root.left, True)


def check_left_align_rec(node: Node, is_left: bool) -> bool:
    if node.left is None and node.right is None:
        return True

    if node.left is None:
        return False

    if node.right is None:
        if is_left:
            return False
        return check_left_align_rec(node.left, is_left or False)

    return check_left_align_rec(node.left, True) and \
        check_left_align_rec(node.right, is_left or False)


def check_min(tree: BinTree) -> bool:
    """
    vstup: ‹tree› – binární strom, jehož všechny listy mají stejnou hloubku
                    a který je doleva zarovnaný dle podmínek nahoře
                    (tj. předpokládáme, že platí ‹check_leaf_depth(tree)›
                     i ‹check_left_align(tree)›)
    výstup: ‹True›, pokud je klíčem každého vnitřního uzlu minimum
                    jeho podstromu;
            ‹False› jinak
    časová složitost: O(n), kde ‹n› je počet uzlů stromu
    extra prostorová složitost: O(h), kde ‹h› je výška stromu
        (Do extra prostorové složitost nepočítáme velikost vstupu, ale
         počítáme do ní zásobník rekurze.)
    """
    if tree.root is None:
        return True

    if tree.root.right is None and tree.root.left is None:
        return True

    if tree.root.right is None:
        l_min, l_correct = check_min_rec(tree.root.left)
        return l_correct and l_min == tree.root.key

    l_min, l_correct = check_min_rec(tree.root.left)
    r_min, r_correct = check_min_rec(tree.root.right)

    if not l_correct or not r_correct:
        return False

    if l_min < tree.root.key or r_min < tree.root.key:
        return False

    return r_min == tree.root.key or l_min == tree.root.key


def check_min_rec(node: Optional[Node]) -> Tuple[int, bool]:
    if node.left is None and node.right is None:
        return node.key, True

    if node.right is None:
        l_min, l_correct = check_min_rec(node.left)
        return node.key, l_correct and l_min == node.key

    l_min, l_correct = check_min_rec(node.left)
    r_min, r_correct = check_min_rec(node.right)

    return node.key, l_correct and r_correct and l_min >= node.key and r_min >= node.key \
        and (r_min == node.key or l_min == node.key)


# Následující funkci můžete použít pro vykreslení stromu při vlastním
# testování. Použití: draw_tree(strom, název souboru).
# Výstupem je soubor ve formátu GraphViz.

def draw_tree(tree: BinTree, filename: str) -> None:
    with open(filename, 'w') as file:
        file.write("digraph BinTree {\n"
                   "node [color=lightblue2, style=filled]\n")
        if tree.root is not None:
            draw_node(tree.root, file)
        file.write("}\n")


def draw_node(node: Node, file: TextIO) -> None:
    file.write(f'"{id(node)}" [label="{node.key}"]\n')
    for child, side in (node.left, 'L'), (node.right, 'R'):
        if child is None:
            nil = f"{side}{id(node)}"
            file.write(f'"{nil}" [label="", color=white]\n'
                       f'"{id(node)}" -> "{nil}"\n')
        else:
            file.write(f'"{id(node)}" -> "{id(child)}"\n')
            draw_node(child, file)
