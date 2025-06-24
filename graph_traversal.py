#!/usr/bin/env python3

# Povolené knihovny: typing, math, collections
# Z knihovny collections je povolena pouze datová struktura deque
# reprezentující frontu. Pro její import použijte přesně následující řádek:
from collections import deque

from typing import Any, List, Optional, Tuple, Deque

WHITE = 0
GREY = 1
BLACK = 2


# IB002 Domácí úloha 10
#
# V tomto úkolu se zameříme na základní aplikace průchodů grafem. Grafy
# budou zadány implicitně – vrcholy grafů budou objekty typu Vertex, které
# se odkazují na své následníky.
#
# V příkladech níže se budeme odkazovat na následující graf:
#
# Graf má vrcholy A, B, C, D, E, F, G.
# Orientované hrany grafu jsou:
#   A -> D
#   B -> A
#   B -> E
#   C -> E
#   C -> F
#   C -> G
#   D -> B
#   E -> F
#   E -> G
#
# Definici třídy Vertex nijak nemodifikujte (kromě typu atributu flag,
# viz níže).


class Vertex:
    """Třída Vertex reprezentuje vrchol grafu.

    Atributy:
        name    jméno vrcholu (libovolný řetězec)
        succs   seznam následníků vrcholu (odkazů na objekty typu Vertex)
        flag    libovolná extra informace přiřazená k vrcholu
    """
    __slots__ = "name", "succs", "flag"

    def __init__(self, name: str):
        self.name = name
        self.succs: List[Vertex] = []
        self.flag: Any = None


# V jednotlivých částech smíte předpokládat, že hodnota atributu ‹flag› je
# u všech vrcholů grafu nastavena na None. Tento atribut můžete využít pro
# zapamatování si libovolné informace příslušné k danému vrcholu.
# Chcete-li využít výhod statické typové kontroly, můžete ve svém řešení změnit
# typ atributu z Any na něco jiného, musíte ovšem zachovat možnost hodnoty
# None, tj. smíte použít např. Optional[int].
#
# Pro všechny části níže platí, že zadané funkce nesmí kromě hodnoty
# atributů ‹flag› objekty typu Vertex nijak modifikovat, ani vytvářet nové.
#
# Nápověda: Když si předem přečtete zadání všech částí a dobře si rozmyslíte,
# jak jednotlivé části budete řešit, můžete si ušetřit značné množství práce.


# Část 1.
# Implementujte funkci reachable_size, která zjistí počet vrcholů a hran
# dosažitelných ze zadaného vrcholu.

def reachable_size(source: Vertex) -> Tuple[int, int]:
    """
    vstup: ‹source› – počáteční vrchol grafu
    výstup: dvojice (|V|, |E|), kde
            |V| je počet vrcholů dosažitelných z vrcholu ‹source›
            |E| je počet hran dosažitelných z vrcholu ‹source›
    časová složitost: O(|V| + |E|)
    extra prostorová složitost: O(|V|)
        (do extra prostorové složitosti počítáme součet velikostí
         všech atributů ‹flag› a libovolných lokálních datových struktur)

    Příklady:
      pro počáteční vrchol A bude výsledkem dvojice (6, 6)
      pro počáteční vrchol C bude výsledkem dvojice (4, 5)
      pro počáteční vrchol E bude výsledkem dvojice (3, 2)
    """
    vertices_reached, edges_reached = 1, 0
    source.flag = GREY

    for s in source.succs:
        edges_reached += 1
        if s.flag is None:
            vertices_succ, edges_succ = reachable_size(s)
            vertices_reached += vertices_succ
            edges_reached += edges_succ

    return vertices_reached, edges_reached


# Část 2.
# Implementujte funkci has_cycle, která zjistí, zda v grafu existuje cyklus
# dosažitelný ze zadaného vrcholu.

def has_cycle(source: Vertex) -> bool:
    """
    vstup: ‹source› – počáteční vrchol grafu
    výstup: ‹True›, jestliže v grafu existuje cyklus dosažitelný
                    z vrcholu ‹source›
            ‹False› jinak
    časová složitost: O(|V| + |E|), kde |V| je počet vrcholů a |E| počet
                      hran dosažitelných z vrcholu ‹source›
    extra prostorová složitost: O(|V|)
        (do extra prostorové složitosti počítáme součet velikostí
         všech atributů ‹flag› a libovolných lokálních datových struktur)

    Příklady:
      pro počáteční vrchol A bude výsledkem ‹True›
      pro počáteční vrchol C bude výsledkem ‹False›
      pro počáteční vrchol E bude výsledkem ‹False›
    """
    source.flag = GREY

    for s in source.succs:
        if s.flag is None:

            if has_cycle(s):
                return True

        elif s.flag == GREY:
            return True

    source.flag = BLACK
    return False


# Část 3.
# Orientovaný strom je kořenový strom, v němž jsou všechny hrany orientovány
# směrem od kořene k listům. Implementujte funkci is_tree, která zjistí,
# zda je graf dosažitelný ze zadaného vrcholu orientovaným stromem.

def is_tree(source: Vertex) -> bool:
    """
    vstup: ‹source› – počáteční vrchol grafu
    výstup: ‹True›, jestliže je graf dosažitelný z vrcholu ‹source›
                    orientovaným stromem (s kořenem ‹source›)
            ‹False› jinak
    časová složitost: O(|V| + |E|), kde |V| je počet vrcholů a |E| počet
                      hran dosažitelných z vrcholu ‹source›
    extra prostorová složitost: O(|V|)
        (do extra prostorové složitosti počítáme součet velikostí
         všech atributů ‹flag› a libovolných lokálních datových struktur)

    Příklady:
      pro počáteční vrchol A bude výsledkem ‹False›
      pro počáteční vrchol C bude výsledkem ‹False›
      pro počáteční vrchol E bude výsledkem ‹True›
    """
    source.flag = GREY

    for s in source.succs:
        if s.flag is None:
            if not is_tree(s):
                return False
        else:
            return False
    return True


# Část 4.
# Jak už jistě víte, vzdálenost vrcholů v orientovaném (neohodnoceném) grafu
# je délka nejkratší orientované cesty začínající v zadaném zdrojovém
# vrcholu a končící v zadaném cílovém vrcholu.
# Implementujte funkci distance, která vrátí vzdálenost mezi zadanými
# vrcholy.

def distance(source: Vertex, target: Vertex) -> Optional[int]:
    """
    vstup: ‹source› – zdrojový vrchol
           ‹target› – cílový vrchol
    výstup: vzdálenost ze ‹source› do ‹target›, pokud existuje cesta
            ze ‹source› do ‹target›; ‹None› jinak
    časová složitost: O(|V| + |E|), kde |V| je počet vrcholů a |E| počet
                      hran dosažitelných z vrcholu ‹source›
    extra prostorová složitost: O(|V|)
        (do extra prostorové složitosti počítáme součet velikostí
         všech atributů ‹flag› a libovolných lokálních datových struktur)

    Příklady:
      pro zdroj A a cíl G bude výsledkem číslo 4
      pro zdroj C a cíl G bude výsledkem číslo 1
      pro zdroj E a cíl D bude výsledkem ‹None›
    """
    source.flag = 0
    d: Deque[Vertex] = deque([source])

    while d:
        act_vertex = d.popleft()
        if act_vertex == target:
            return act_vertex.flag

        for s in act_vertex.succs:
            if s.flag is None:
                s.flag = act_vertex.flag + 1
                d.append(s)

    return None


# Následující funkci můžete použít pro vykreslení grafu při vlastním
# testování. Použití:
# draw_graph(seznam všech vrcholů, název souboru)

def draw_graph(vertices: List[Vertex], filename: str) -> None:
    with open(filename, 'w') as file:
        file.write("digraph G {\n"
                   "node [color=lightblue2, style=filled]\n")
        for vertex in vertices:
            label = vertex.name
            if vertex.flag is not None:
                label += f"\\n(flag={vertex.flag})"
            file.write(f'"{id(vertex)}" [label="{label}"]\n')
            for succ in vertex.succs:
                file.write(f'"{id(vertex)}" -> "{id(succ)}"\n')
        file.write("}\n")


# Zde si můžete nechat vykreslit graf z příkladu nahoře:

def draw_example() -> None:
    a = Vertex("A")
    b = Vertex("B")
    c = Vertex("C")
    d = Vertex("D")
    e = Vertex("E")
    f = Vertex("F")
    g = Vertex("G")

    a.succs = [d]
    b.succs = [e, a]
    c.succs = [e, f, g]
    d.succs = [b]
    e.succs = [g, f]

    draw_graph([a, b, c, d, e, f, g], "ib002_graph.dot")