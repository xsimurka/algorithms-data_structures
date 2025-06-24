#!/usr/bin/env python3

# Povolené knihovny: typing, math, fractions

from typing import Optional, TextIO, List

# IB002 Domácí úloha 9
#
# V tomto úkolu budeme pracovat s binárními vyhledávacími stromy, jejichž
# uzly si budou pamatovat velikost (počet uzlů) svých podstromů.
# Dále zde budeme používat následující pojem vyváženosti:
# Řekneme, že uzel ‹u› je k-vyvážený (pro číslo k mezi 1/2 a 1 včetně),
# pokud pro oba jeho potomky platí, že velikost jejich podstromů je nejvýše
# k-násobkem velikosti podstromu uzlu ‹u›.
# O celém stromu řekneme, že je k-vyvážený, pokud jsou všechny jeho uzly
# k-vyvážené.
#
#
# Příklady:
#         3
#        /
#       2
#      /
#     1
#
# Tento strom není 3/5-vyvážený (kořen stromu není 3/5-vyvážený, protože
# podstrom jeho levého potomka má dva uzly, zatímco celý strom má tři uzly
# a 2 > 3/5 · 3), a tedy není ani 1/2-vyvážený. Je ovšem 2/3-vyvážený.
#
#        4
#       / \
#      2   5
#     / \
#    1   3
#
# Tento strom je 2/3-vyvážený i 3/5-vyvážený, ale není 1/2-vyvážený (opět je
# problém v kořeni stromu; podstrom jeho levého potomka má tři uzly, zatímco
# celý strom má pět uzlů a 3 > 1/2 · 5).
#
#        4
#      /   \
#     2     6
#    / \   / \
#   1   3 5   7
#
# Tento strom je 1/2-vyvážený (a tedy je i k-vyvážený pro každé k > 1/2).
#
#        4
#       / \
#      3   6
#     /   / \
#    2   5   8
#   /       / \
#  1       7   9
#
# Tento strom není 3/5-vyvážený (problém je v uzlu s klíčem 3), ale je
# 2/3-vyvážený.
#
#         4
#       /   \
#      2     6
#     / \   / \
#    1   3 5   8
#   /         / \
#  0         7   9
#
# Tento strom je 3/5-vyvážený, ale není 1/2-vyvážený (problém je v uzlu
# s klíčem 6).
#
# Všechny stromy, které zde budeme uvažovat, budou mít unikátní klíče
# (tj. nestane se, že by ve stromě existovaly dva uzly se stejným klíčem).
#
# Do následujících definic tříd nijak nezasahujte.
# Pro vykreslování stromů máte na konci tohoto souboru k dispozici
# funkci draw_tree.


class Node:
    """Třída Node reprezentuje uzel binárního vyhledávacího stromu.

    Atributy:
        key     klíč uzlu
        left    odkaz na levý potomek uzlu nebo ‹None›
        right   odkaz na pravý potomek uzlu nebo ‹None›
        parent  odkaz na rodiče uzlu nebo ‹None›
        size    velikost (počet uzlů) podstromu tohoto uzlu
    """
    __slots__ = "key", "left", "right", "parent", "size"

    def __init__(self, key: int,
                 left: Optional['Node'] = None,
                 right: Optional['Node'] = None,
                 parent: Optional['Node'] = None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent
        self.size = 1


class BSTree:
    """Třída BSTree reprezentuje binární vyhledávací strom.

    Atributy:
        root    odkaz na kořenový uzel stromu nebo ‹None›
    """
    __slots__ = "root"

    def __init__(self, root: Optional[Node] = None):
        self.root = root


# Část 1.
# Implementuje predikát check_size ověřující podmínku, že hodnota atributu
# ‹size› je ve všech uzlech stromu správná, a predikát check_3_5_balanced
# ověřující podmínku, že zadaný strom je 3/5-vyvážený.
# Predikáty nemodifikují vstupní stromy.

def check_size(tree: BSTree) -> bool:
    """
    vstup: ‹tree› – binární vyhledávací strom
                    (nemusí být vyvážený, nemusí mít správné atributy ‹size›)
    výstup: ‹True›, pokud jsou všechny atributy ‹size› správné, tj.
                    odpovídají počtu uzlů v podstromě (včetně uzlu samotného)
            ‹False› jinak
    časová složitost: O(n), kde ‹n› je počet uzlů stromu
    extra prostorová složitost: O(h), kde ‹h› je výška stromu
        (Do extra prostorové složitost nepočítáme velikost vstupu, ale
         počítáme do ní zásobník rekurze.)
    """
    if tree is None or tree.root is None:
        return True

    return check_size_rec(tree.root)


def check_size_rec(node: Optional[Node]) -> bool:
    if node.left is None and node.right is None:
        return node.size == 1

    if node.left is None:
        return check_size_rec(node.right) and node.right.size + 1 == node.size

    if node.right is None:
        return check_size_rec(node.left) and node.left.size + 1 == node.size

    return check_size_rec(node.left) and check_size_rec(node.right) \
        and node.left.size + node.right.size + 1 == node.size


def check_3_5_balanced(tree: BSTree) -> bool:
    """
    vstup: ‹tree› – binární vyhledávací strom se správnými atributy ‹size›
    výstup: ‹True›, jestliže je zadaný strom 3/5-vyvážený
            ‹False› jinak
    časová složitost: O(n), kde ‹n› je počet uzlů stromu
    extra prostorová složitost: O(h), kde ‹h› je výška stromu
        (Do extra prostorové složitost nepočítáme velikost vstupu, ale
         počítáme do ní zásobník rekurze.)
    """
    if tree is None:
        return True

    return check_m_n_balanced_rec(tree.root, 3/5)


def check_m_n_balanced_rec(node: Optional[Node], m_n: float) -> bool:
    if node is None:
        return True

    if not is_node_balanced(node, m_n):
        return False

    return check_m_n_balanced_rec(node.left, m_n) and \
        check_m_n_balanced_rec(node.right, m_n)


def is_node_balanced(node: Optional[Node], m_n: float) -> bool:
    if node is None:
        return True

    left_balanced = True if node.left is None else \
        node.left.size <= m_n * node.size
    right_balanced = True if node.right is None else \
        node.right.size <= m_n * node.size

    return left_balanced and right_balanced


# Část 2.
# Implementujte funkci pro vkládání nového klíče do stromu (pokud už klíč
# ve stromě existuje, nic se nevloží). Pokud se vložením klíče poruší
# 3/5-vyváženost stromu, funkce vrátí odkaz na problémový uzel.

def insert(tree: BSTree, key: int) -> Optional[Node]:
    r"""
    vstup: ‹tree› – 3/5-vyvážený binární vyhledávací strom
                    se správnými atributy ‹size›
           ‹key› – celé číslo
    výstup: Funkce vloží klíč do stromu podle pravidel binárního vyhledávacího
            stromu; pokud už klíč ve stromě existuje, nevloží nic.
            (Nezapomeňte na správné nastavení atributu ‹parent›.)
            Funkce dále upraví atributy ‹size› v uzlech tak, aby byly korektní.
            Pokud se neporušila vlastnost 3/5-vyváženosti, funkce vrátí ‹None›;
            v opačném případě funkce vrátí odkaz na uzel, který není
            3/5-vyvážený. Je-li takových uzlů více, funkce vrátí odkaz na ten,
            který je ve stromě nejvýše (tj. nejblíže ke kořeni).
    časová složitost: O(log n), kde ‹n› je počet uzlů stromu

    Příklady:  (v závorce je hodnota atributu size)

    strom:  3(2)   a klíč 1
           /
         2(1)
    po vložení bude stav stromu:
            3(3)
           /
         2(2)
         /
        1(1)
    a funkce vrátí odkaz na kořen stromu.

    strom:      4(7)        a klíč 1
               /    \
             3(2)   6(4)
             /      /  \
            2(1)  5(1) 8(2)
                       /
                    7(1)
    po vložení bude stav stromu:
                4(8)
               /    \
             3(3)   6(4)
             /      /  \
            2(2)  5(1) 8(2)
           /           /
         1(1)       7(1)
    a funkce vrátí odkaz na uzel s klíčem 3.

    strom:     4(7)      a klíč 0
             /      \
          2(3)      6(3)
          / \       / \
       1(1) 3(1) 5(1) 7(1)
    po vložení bude stav stromu:
               4(8)
             /      \
          2(4)      6(3)
          / \       / \
       1(2) 3(1) 5(1) 7(1)
       /
      0(1)
    a funkce vrátí ‹None›.
    """
    if tree.root is None:
        tree.root = Node(key)
        return None

    new_node_parent = insert_key(tree, key)
    if new_node_parent is None:
        return None

    return find_3_5_disbalance(new_node_parent)


def find_3_5_disbalance(node: Optional[Node]) -> Optional[Node]:
    disbalanced_node = None

    while node is not None:
        node.size += 1
        if not is_node_balanced(node, 3/5):
            disbalanced_node = node
        node = node.parent

    return disbalanced_node


def insert_key(tree: BSTree, key: int) -> Optional[Node]:
    act_node = tree.root

    while True:
        if act_node.key < key:
            if act_node.right is None:
                act_node.right = Node(key=key, parent=act_node)
                return act_node
            act_node = act_node.right

        elif act_node.key > key:
            if act_node.left is None:
                act_node.left = Node(key=key, parent=act_node)
                return act_node
            act_node = act_node.left
        else:
            return None


# Část 3.
# Implementuje funkci rebalance, která přebuduje podstrom zadaného uzlu tak,
# aby byl 1/2-vyvážený.
#
# Nápověda: Pomůže Vám, když si nejprve pomocí inorder průchodu vyrobíte
# seznam všech uzlů zadaného podstromu seřazený podle klíčů.

def rebalance(tree: BSTree, node: Node) -> None:
    r"""
    vstup: ‹tree› – binární vyhledávací strom se správnými atributy ‹size›
                    (nemusí být vyvážený)
           ‹node› – uzel patřící do stromu ‹tree›
    výstup: Funkce reorganizuje podstrom uzlu ‹node› (včetně tohoto uzlu)
            tak, aby byl 1/2-vyvážený; výsledný podstrom pak zavěsí na původní
            místo uzlu ‹node›. Samozřejmě je třeba zachovat vlastnost binárního
            vyhledávacího stromu a případně upravit atributy ‹size›.
            Při reorganizaci neměňte klíče uzlů ani nevytvářejte nové uzly;
            pouze přeskládejte existující.
            (Nezapomeňte na atributy ‹parent›.)
    časová složitost: O(m), kde ‹m› je velikost podstromu uzlu ‹node›

    Příklad:  (v závorce je hodnota atributu size)
                4(9)
               /    \
             3(3)   6(5)
             /      /  \
            2(2)  5(1) 8(3)
           /           / \
         1(1)       7(1)  9(1)
    po zavolání rebalance na uzlu s klíčem 3:
                  4(9)
                /      \
             2(3)       6(5)
             /  \      /   \
           1(1) 3(1) 5(1)  8(3)
                           /  \
                        7(1)  9(1)
    po dalším zavolání rebalance na uzlu s klíčem 6:
    (zde je více možností výsledku, tohle je jeden z možných)
                  4(9)
                /      \
             2(3)       7(5)
             /  \      /   \
           1(1) 3(1) 6(2)  8(2)
                     /       \
                   5(1)     9(1)
    po dalším zavolání rebalance na uzlu s klíčem 4:
    (opět je více možností výsledku, tohle je jeden z možných)
                  5(9)
                /      \
             2(4)       7(4)
             /  \      /   \
           1(1) 3(2) 6(1)  8(2)
                  \          \
                 4(1)         9(1)
    """
    if check_m_n_balanced_rec(node, 1/2):
        return

    subtree_nodes = []
    inorder(node, subtree_nodes)
    if node == tree.root:
        is_left = None
    else:
        is_left = True if node.parent.left == node else False
    rebalance_rec(tree, 0, len(subtree_nodes), subtree_nodes, node.parent, is_left)


def rebalance_rec(tree: BSTree, lower: int, upper: int, lst: List[Node],
                  parent: Optional[Node], is_left: Optional[bool]) -> None:
    if lower == upper:
        return

    act_node = lst[(upper + lower) // 2]

    if is_left is None:
        tree.root = act_node
    elif is_left:
        parent.left = act_node
    else:
        parent.right = act_node

    act_node.left = None
    act_node.right = None
    act_node.parent = parent

    if lower + 1 == upper:
        act_node.size = 1
        return
    act_node.size = upper - lower

    rebalance_rec(tree, lower, (upper + lower) // 2, lst, act_node, True)
    rebalance_rec(tree, (upper + lower) // 2 + 1, upper, lst, act_node, False)


def inorder(node: Optional[Node], lst: List[Node]) -> None:
    if node is not None:
        inorder(node.left, lst)
        lst.append(node)
        inorder(node.right, lst)


# Následující funkci můžete použít pro vykreslení stromu při vlastním
# testování. Použití: draw_tree(strom, název souboru).
# Výstupem je soubor ve formátu GraphViz.

def draw_tree(tree: BSTree, filename: str) -> None:
    with open(filename, 'w') as file:
        file.write("digraph BinTree {\n"
                   "node [color=lightblue2, style=filled]\n")
        if tree.root is not None:
            draw_node(tree.root, file)
        file.write("}\n")


def draw_node(node: Node, file: TextIO) -> None:
    file.write(f'"{id(node)}" [label="{node.key}\\n(size={node.size})"]\n')
    for child, side in (node.left, 'L'), (node.right, 'R'):
        if child is None:
            nil = f"{side}{id(node)}"
            file.write(f'"{nil}" [label="", color=white]\n'
                       f'"{id(node)}" -> "{nil}"\n')
        else:
            file.write(f'"{id(node)}" -> "{id(child)}"\n')
            draw_node(child, file)
