#!/usr/bin/env python3

# Povolené knihovny: typing, math, collections
# Z knihovny collections je povolena pouze datová struktura deque
# reprezentující frontu. Pro její import použijte přesně následující řádek:
# from collections import deque

from typing import List

# IB002 Domácí úloha 11
#
# V tomto úkolu se podíváme na hledání silně souvislých komponent v grafu.
# Doporučujeme, abyste si předtím, než začnete programovat, připomněli,
# co to silně souvislé komponenty v grafu jsou a jaké známe algoritmy pro
# jejich počítání.
#
# Grafy budeme v tomto úkolu reprezentovat pomocí seznamů následníků.
# Každý graf ‹g› má tedy vrcholy očíslované 0, ..., g.size - 1 (včetně).
#
# Definici třídy Graph nijak nemodifikujte.


class Graph:
    """Třída Graph reprezentuje orientovaný graf pomocí seznamů následníků.

    Atributy:
        size    počet vrcholů grafu
                (vrcholy jsou očíslované 0, 1, ..., size - 1)
        succs   seznamy následníků
                (succs[v] obsahuje následníky vrcholu ‹v›)
    """
    __slots__ = 'size', 'succs'

    def __init__(self, size: int):
        self.size = size
        self.succs: List[List[int]] = [[] for _ in range(size)]


# Následují dvě ukázky grafů, ke kterým se budeme odkazovat v příkladech
# výstupů funkcí. Prvním z nich je graf, který jsme viděli v 11. kapitole
# sbírky.

def example_graph1() -> Graph:
    graph = Graph(10)
    graph.succs[0] = [2, 3, 6]
    graph.succs[1] = [4, 8]
    graph.succs[2] = [5]
    graph.succs[3] = [7, 8]
    graph.succs[4] = [8]
    graph.succs[5] = [6]
    graph.succs[6] = [2]
    graph.succs[7] = [6, 9]
    graph.succs[8] = [0]
    graph.succs[9] = [7]
    return graph


def example_graph2() -> Graph:
    graph = Graph(8)
    graph.succs[0] = [5, 1, 4]
    graph.succs[1] = [0, 6]
    graph.succs[2] = [7, 2]
    graph.succs[3] = [7]
    # vertex 4 has no successors
    graph.succs[5] = [5]
    graph.succs[6] = [7]
    graph.succs[7] = [6]
    return graph


# Pro všechny části níže platí, že zadané funkce nesmí nijak modifikovat
# vstupní graf.


# Část 1.
# Implementujte funkci strongly_connected_components, která najde všechny
# silně souvislé komponenty zadaného grafu.

def strongly_connected_components(graph: Graph) -> List[List[int]]:
    """
    vstup: ‹graph› – orientovaný graf (objekt typu ‹Graph›)
    výstup: seznam všech silně souvislých komponent grafu;
            každá komponenta je reprezentována seznamem svých vrcholů
            na pořadí prvků v seznamech nezáleží
    časová složitost: O(|V| + |E|)

    Příklady:
      Pro první ukázkový graf může být výsledkem např. tento seznam:
        [[1], [4], [0, 3, 8], [7, 9], [2, 5, 6]]
      Pro druhý ukázkový graf může být výsledkem např. tento seznam:
        [[0, 1], [2], [3], [4], [5], [6, 7]]
    """
    color = [False for _ in range(graph.size)]
    reached: List[int] = []
    result = []

    for vertex in range(graph.size):
        if not color[vertex]:
            dfs(graph, vertex, color, reached)

    transposed = transpose(graph)

    color = [False for _ in range(graph.size)]

    for i in range(transposed.size - 1, -1, -1):
        if not color[reached[i]]:
            c = find_component(transposed, reached[i], color)
            result.append(c)

    return result


def find_component(graph: Graph, vertex: int, color: List[bool]) -> List[int]:
    return find_component_rec(graph, vertex, color, [])


def find_component_rec(graph: Graph, vertex: int,
                       color: List[bool], component: List[int]) -> List[int]:
    component.append(vertex)
    color[vertex] = True
    for succ in graph.succs[vertex]:
        if not color[succ]:
            find_component_rec(graph, succ, color, component)

    return component


def transpose(graph: Graph) -> Graph:
    result = Graph(graph.size)
    for i in range(graph.size):
        for succ in graph.succs[i]:
            result.succs[succ].append(i)
    return result


def dfs(graph: Graph, vertex: int, color: List[bool],
        stack: List[int]) -> None:
    color[vertex] = True
    for succ in graph.succs[vertex]:
        if not color[succ]:
            dfs(graph, succ, color, stack)
    stack.append(vertex)


# Část 2.
# O silně souvislé komponentě grafu řekneme, že je «terminální» (někdy také
# spodní, koncová, listová), pokud z ní nevedou žádné hrany do jiných
# komponent.
# Implementujte funkci terminal_sccs, která najde všechny terminální silně
# souvislé komponenty zadaného grafu.

def terminal_sccs(graph: Graph) -> List[List[int]]:
    """
    vstup: ‹graph› – orientovaný graf (objekt typu ‹Graph›)
    výstup: seznam všech terminálních silně souvislých komponent grafu;
            každá komponenta je reprezentována seznamem svých vrcholů
            na pořadí prvků v seznamech nezáleží
    časová složitost: O(|V| + |E|)

    Příklady:
      Pro první ukázkový graf může být výsledkem např. tento seznam:
        [[2, 5, 6]]
      Pro druhý ukázkový graf může být výsledkem např. tento seznam:
        [[4], [5], [6, 7]]
    """
    components = strongly_connected_components(graph)
    groups = shrink(graph, components)
    result = []
    for i in range(groups.size):
        if out_degree(groups, i) == 0:
            result.append(components[i])
    return result


def out_degree(graph: Graph, component: int) -> int:
    return len(graph.succs[component])


def shrink(graph: Graph, components: List[List[int]]) -> Graph:
    result = Graph(len(components))
    lst = [-1 for _ in range(graph.size)]
    for i in range(len(components)):
        for j in components[i]:
            lst[j] = i

    for i in range(graph.size):
        component_from = lst[i]
        for succ in graph.succs[i]:
            component_to = lst[succ]
            if component_from != component_to:
                result.succs[component_from].append(component_to)

    return result

# Část 3.
# O silně souvislé komponentě grafu řekneme, že je «iniciální» (někdy také
# počáteční, horní, kořenová), pokud do ní nevedou žádné hrany z jiných
# komponent.
# Implementujte funkci initial_sccs, která najde všechny iniciální silně
# souvislé komponenty zadaného grafu.


def initial_sccs(graph: Graph) -> List[List[int]]:
    """
    vstup: ‹graph› – orientovaný graf (objekt typu ‹Graph›)
    výstup: seznam všech iniciálních silně souvislých komponent grafu;
            každá komponenta je reprezentována seznamem svých vrcholů
            na pořadí prvků v seznamech nezáleží
    časová složitost: O(|V| + |E|)

    Příklady:
      Pro první ukázkový graf musí být výsledkem tento seznam:
        [[1]]
      Pro druhý ukázkový graf může být výsledkem např. tento seznam:
        [[0, 1], [2], [3]]
    """
    components = strongly_connected_components(graph)
    groups = shrink(graph, components)
    indegrees = in_degrees(groups)
    result = []
    for i in range(len(components)):
        if indegrees[i] == 0:
            result.append(components[i])
    return result


def in_degrees(graph: Graph) -> List[int]:
    in_degrees = [0 for _ in range(graph.size)]
    for i in range(graph.size):
        for succ in graph.succs[i]:
            in_degrees[succ] += 1
    return in_degrees


# Následující funkci můžete použít pro vykreslení grafu při vlastním
# testování.

def draw_graph(graph: Graph, filename: str) -> None:
    with open(filename, 'w') as file:
        file.write("digraph G {\n"
                   "node [color=lightblue2, style=filled]\n")
        for vertex in range(graph.size):
            for succ in graph.succs[vertex]:
                file.write(f'"{vertex}" -> "{succ}"\n')
        file.write("}\n")