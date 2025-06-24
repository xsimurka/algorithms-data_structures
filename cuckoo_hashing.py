#!/usr/bin/env python3

# Povolené knihovny: typing, math

from typing import Callable, Optional, List, Tuple


# IB002 Domácí úloha 10
#
# V tomto úkolu budeme pracovat s variantou hašovací tabulky, která používá
# tzv. kukaččí hašování (cuckoo hashing).
# Kukaččí hašovací tabulka obsahuje dvě stejně velká pole a používá dvě různé
# hašovací funkce. Pro každý klíč tedy máme dvě různá místa, kam jej můžeme
# vložit: do prvního pole na index daný první hašovací funkcí nebo do
# druhého pole na index daný druhou hašovací funkcí.
#
# Vyhledávání a mazání klíčů z kukaččí hašovací tabulky je velmi jednoduché.
# Stačí se podívat na obě místa, kde se klíč v tabulce může nacházet.
#
# Vkládání do hašovací tabulky probíhá následovně:
# 1. Pokud je jedno ze dvou výše uvedených míst volné, vložíme klíč do něj.
#    Přitom preferujeme první pole.
# 2. Pokud jsou obě možná místa zaplněna, „vykopneme“ (podobně jako kukačka
#    vykopne vejce z cizího hnízda) klíč, který se nachází na prvním místě
#    a místo něj vložíme náš klíč. Vykopnutý klíč se potom pokusíme vložit
#    na jeho místo v druhé tabulce. Tím může dojít k vykopnutí dalšího klíče,
#    který se naopak musí vložit na své místo v první tabulce atd.
#    Pokud se tento proces zacyklí, vkládání nebylo úspěšné a tabulka se musí
#    zvětšit a přehašovat. My v této úloze pro jednoduchost nebudeme
#    implementovat zvětšování tabulky a smíříme se s neúspěchem. Budeme ovšem
#    vyžadovat, aby se při neúspěšném vkládání tabulka vrátila do původního
#    stavu.
# Existují různé metody detekce zacyklení. My zde budeme používat velmi
# jednoduchou: každé vkládání bude mít jako parametr limit na maximální počet
# „vykopnutí“. Pokud je tento limit překročen, vkládání považujeme za
# neúspěšné.
#
# (Můžete si jako zajímavé algoritmické cvičení zkusit rozmyslet, jak by se
#  zacyklení detekovalo bez tohoto limitu. Pomůže znalost některých pojmů
#  z teorie grafů.)
#
# Příklad:
# Mějme kukaččí hašovací tabulku velikosti 5 s hašovacími funkcemi
# h1(x) = x % 5
# h2(x) = x // 5 % 5
#
# Na začátku jsou obě pole tabulky prázdná (tj. v naší implementaci budou
# obsahovat položky None).
#
#           0   1   2   3   4
#         ┌───┬───┬───┬───┬───┐
# 1.pole: │   │   │   │   │   │
#         └───┴───┴───┴───┴───┘
#         ┌───┬───┬───┬───┬───┐
# 2.pole: │   │   │   │   │   │
#         └───┴───┴───┴───┴───┘
#
# Vložíme klíč 7. h1(7) = 2, h2(7) = 1, první pole má přednost.
#
#           0   1   2   3   4
#         ┌───┬───┬───┬───┬───┐
# 1.pole: │   │   │ 7 │   │   │
#         └───┴───┴───┴───┴───┘
#         ┌───┬───┬───┬───┬───┐
# 2.pole: │   │   │   │   │   │
#         └───┴───┴───┴───┴───┘
#
# Vložíme klíč 22. h1(22) = 2, h2(22) = 4, v prvním poli na indexu 2
# už nějaký klíč je, ale v druhém poli na indexu 4 je prázdno.
#
#           0   1   2   3   4
#         ┌───┬───┬───┬───┬───┐
# 1.pole: │   │   │ 7 │   │   │
#         └───┴───┴───┴───┴───┘
#         ┌───┬───┬───┬───┬───┐
# 2.pole: │   │   │   │   │22 │
#         └───┴───┴───┴───┴───┘
#
# Vložíme klíč 47. h1(47) = 2, h2(47) = 4. Obě možná místa jsou zaplněna,
# budeme muset vykopnout klíč z prvního pole – h2(7) = 1, takže vykopnutý
# klíč 7 se umístí do druhého pole na index 1.
#
#           0   1   2   3   4
#         ┌───┬───┬───┬───┬───┐
# 1.pole: │   │   │47 │   │   │
#         └───┴───┴───┴───┴───┘
#         ┌───┬───┬───┬───┬───┐
# 2.pole: │   │ 7 │   │   │22 │
#         └───┴───┴───┴───┴───┘
#
# Vložíme klíč 5. h1(5) = 0, h2(5) = 1, první pole má přednost.
#
#           0   1   2   3   4
#         ┌───┬───┬───┬───┬───┐
# 1.pole: │ 5 │   │47 │   │   │
#         └───┴───┴───┴───┴───┘
#         ┌───┬───┬───┬───┬───┐
# 2.pole: │   │ 7 │   │   │22 │
#         └───┴───┴───┴───┴───┘
#
# Vložíme klíč 25. h1(25) = 0, h2(25) = 0, v prvním poli na indexu 0 je plno,
# ale ve druhém poli na indexu 0 je prázdno.
#
#           0   1   2   3   4
#         ┌───┬───┬───┬───┬───┐
# 1.pole: │ 5 │   │47 │   │   │
#         └───┴───┴───┴───┴───┘
#         ┌───┬───┬───┬───┬───┐
# 2.pole: │25 │ 7 │   │   │22 │
#         └───┴───┴───┴───┴───┘
#
# Pokusíme se vložit klíč 27. h1(27) = 2, h2(27) = 0, obě místa jsou zaplněna.
# Pokusíme se vykopnout klíč 47 z indexu 2 v prvním poli.
# h2(47) = 4, pokusíme se vykopnout klíč 22 z indexu 4 ve druhém poli.
# h1(22) = 2, pokusíme se vykopnout klíč 27 z indexu 2 v prvním poli.
# h2(27) = 0, pokusíme se vykopnout klíč 25 z indexu 0 ve druhém poli.
# h1(25) = 0, pokusíme se vykopnout klíč 5 z indexu 0 v pvrním poli.
# h2(5) = 1, pokusíme se vykopnout klíč 7 z indexu 1 ve druhém poli.
# h1(7) = 2, pokusíme se vykopnout klíč 22 z indexu 2 v prvním poli.
# h2(22) = 4, pokusíme se vykopnout klíč 47 z indexu 4 ve druhém poli.
# h1(47) = 2, pokusíme se vykopnout klíč 7 z indexu 2 v prvním poli.
# h2(7) = 1, pokusíme se vykopnout klíč 5 z indexu 1 ve druhém poli.
# h1(5) = 0, pokusíme se vykopnout klíč 25 z indexu 0 v prvním poli.
# h2(25) = 0, pokusíme se vykopnout klíč 27 z indexu 0 ve druhém poli.
# h1(27) = 2, pokusíme se vykopnout klíč 47 z indexu 2 v prvním poli.
# … a takhle bychom mohli pokračovat donekonečna.
# Vkládání prvku 27 tedy není úspěšné a tabulku vrátíme do původního stavu.
#
#           0   1   2   3   4
#         ┌───┬───┬───┬───┬───┐
# 1.pole: │ 5 │   │47 │   │   │
#         └───┴───┴───┴───┴───┘
#         ┌───┬───┬───┬───┬───┐
# 2.pole: │25 │ 7 │   │   │22 │
#         └───┴───┴───┴───┴───┘
#
# Vložíme klíč 11. h1(11) = 1, h2(11) = 2, první pole má přednost.
#
#           0   1   2   3   4
#         ┌───┬───┬───┬───┬───┐
# 1.pole: │ 5 │11 │47 │   │   │
#         └───┴───┴───┴───┴───┘
#         ┌───┬───┬───┬───┬───┐
# 2.pole: │25 │ 7 │   │   │22 │
#         └───┴───┴───┴───┴───┘
#
# Smažeme klíč 25. h1(25) = 0, h2(25) = 0. Klíč 25 jsme našli ve druhém poli.
#
#           0   1   2   3   4
#         ┌───┬───┬───┬───┬───┐
# 1.pole: │ 5 │11 │47 │   │   │
#         └───┴───┴───┴───┴───┘
#         ┌───┬───┬───┬───┬───┐
# 2.pole: │   │ 7 │   │   │22 │
#         └───┴───┴───┴───┴───┘
#
# Vložíme klíč 76. h1(76) = 1, h2(76) = 0. Ve druhém poli je volno.
#
#           0   1   2   3   4
#         ┌───┬───┬───┬───┬───┐
# 1.pole: │ 5 │11 │47 │   │   │
#         └───┴───┴───┴───┴───┘
#         ┌───┬───┬───┬───┬───┐
# 2.pole: │76 │ 7 │   │   │22 │
#         └───┴───┴───┴───┴───┘
#
# Opět vložíme klíč 25. h1(25) = 0, h2(25) = 0. Obě místa jsou zaplněna.
# Vykopneme klíč 5 z indexu 0 v prvním poli.
# h2(5) = 1, vykopneme klíč 7 z indexu 1 ve druhém poli.
# h1(7) = 2, vykopneme klíč 47 z indexu 2 v prvním poli.
# h2(47) = 4, vykopneme klíč 22 z indexu 4 ve druhém poli.
# h1(22) = 2, vykopneme klíč 7 z indexu 2 v prvním poli.
# h2(7) = 1, vykopneme klíč 5 z indexu 1 ve druhém poli.
# h1(5) = 0, vykopneme klíč 25 z indexu 0 v prvním poli.
# h2(25) = 0, vykopneme klíč 76 z indexu 0 ve druhém poli.
# h1(76) = 1, vykopneme klíč 11 z indexu 1 v prvním poli.
# h2(11) = 2, na indexu 2 ve druhém poli je prázdno, umístíme tam 11.
#
#           0   1   2   3   4
#         ┌───┬───┬───┬───┬───┐
# 1.pole: │ 5 │76 │22 │   │   │
#         └───┴───┴───┴───┴───┘
#         ┌───┬───┬───┬───┬───┐
# 2.pole: │25 │ 7 │11 │   │47 │
#         └───┴───┴───┴───┴───┘
#
# Vidíme, že v posledním případě jsme museli provést celkem 9 vykopnutí.
# Volání funkce insert s nižším limitem vykopnutí než 9 by tedy skončilo
# neúspěchem.
#
#
# Do následující definice třídy CuckooHashTable nijak nezasahujte.


class CuckooHashTable:
    """Třída CuckooHashTable reprezentuje kukaččí hašovací tabulku.

    Atributy:
        array1  první pole
        array2  druhé pole
        hash1   hašovací funkce pro první pole
        hash2   hašovací funkce pro druhé pole

    Hašovací funkce voláme takto – je-li table objekt typu CuckooHashTable:
        table.hash1(key)
        table.hash2(key)

    Velikost polí musí během libovolných operací s tabulkou zůstat fixní.
    (Tj. chovejte se k nim skutečně jako k polím, ne jako k rozšiřitelným
     seznamům.)
    """
    __slots__ = "array1", "array2", "hash1", "hash2"

    def __init__(self, size: int,
                 hash1: Callable[[int], int],
                 hash2: Callable[[int], int]):
        self.array1: List[Optional[int]] = [None for _ in range(size)]
        self.array2: List[Optional[int]] = [None for _ in range(size)]
        self.hash1 = hash1
        self.hash2 = hash2


# Část 1.
# Implementuje predikát contains, který ověří, zda tabulka obsahuje zadaný
# klíč. Tabulku nijak nemodifikujte.

def is_first_free(table: CuckooHashTable, key: int) -> bool:
    return table.array1[table.hash1(key)] is None


def is_second_free(table: CuckooHashTable, key: int) -> bool:
    return table.array2[table.hash2(key)] is None


def contains(table: CuckooHashTable, key: int) -> bool:
    """
    vstup: ‹table› – korektní kukaččí hašovací tabulka
           ‹key› – celé číslo
    výstup: ‹True›, pokud tabulka ‹table› obsahuje klíč ‹key›
            ‹False› jinak
    časová složitost: O(1), tedy konstantní
    """
    return table.array1[table.hash1(key)] == key or\
        table.array2[table.hash2(key)] == key


# Část 2.
# Implementujte funkci delete, která ze zadané tabulky odstraní zadaný klíč.

def delete(table: CuckooHashTable, key: int) -> bool:
    """
    vstup: ‹table› – korektní kukaččí hašovací tabulka
           ‹key› – celé číslo
    výstup: ‹True›, pokud skutečně došlo k odstranění klíče
            ‹False› jinak
            Funkce z tabulky ‹table› odstraní klíč ‹key›, pokud jej
            tabulka obsahuje.
    časová složitost: O(1), tedy konstantní
    """
    if table.array1[table.hash1(key)] == key:
        table.array1[table.hash1(key)] = None
        return True
    if table.array2[table.hash2(key)] == key:
        table.array2[table.hash2(key)] = None
        return True
    return False


# Část 3.
# Implementujte funkci insert, která do tabulky vloží klíč.
# Pro návratovou hodnotu použijte následující konstanty (jejich hodnoty
# nijak neměňte):

ALREADY_PRESENT = 0
INSERT_SUCCESSFUL = 1
INSERT_FAILED = 2


def insert(table: CuckooHashTable, key: int, max_kicks: int) -> int:
    """
    vstup: ‹table› – korektní kukaččí hašovací tabulka
           ‹key› – celé číslo
           ‹max_kicks› – nezáporné celé číslo
           (Smíte předpokládat, že hodnota ‹max_kicks› je nižší než
            limit rekurze.)
    výstup: ‹ALREADY_PRESENT›, pokud tabulka ‹table› už klíč ‹key› obsahuje
            ‹INSERT_SUCCESSFUL›, pokud se vkládání podařilo
            ‹INSERT_FAILED›, pokud se vkládání nepodařilo
            Funkce se pokusí vložit klíč ‹key› do tabulky ‹table› dle
            postupu popsaného na začátku tohoto souboru.
            Parametr ‹max_kicks› označuje maximální počet „vykopnutí“,
            které smí funkce provést.
            V případě, že se vkládání nepodaří, je třeba tabulku uvést
            do původního stavu.
    časová složitost: O(max_kicks)
    """
    changes: List[Tuple[int, int, int]] = []
    if contains(table, key):
        return ALREADY_PRESENT

    if is_first_free(table, key):
        table.array1[table.hash1(key)] = key
        return INSERT_SUCCESSFUL

    if is_second_free(table, key):
        table.array2[table.hash2(key)] = key
        return INSERT_SUCCESSFUL

    result = insert_to_first(table, key, max_kicks, changes)

    if result == INSERT_FAILED:
        repair(table, changes)

    return result


def repair(table: CuckooHashTable,
           changes: List[Tuple[int, int, int]]) -> None:
    for i in range(len(changes) - 1, -1, -1):
        value, index, array = changes[i]
        if array == 1:
            table.array1[index] = value
        else:
            table.array2[index] = value


def insert_to_first(table: CuckooHashTable, key: int, rem_kicks: int,
                    changes: List[Tuple[int, int, int]]) -> int:
    if rem_kicks < 0:
        return INSERT_FAILED

    hash = table.hash1(key)
    kicked = table.array1[hash]

    table.array1[hash] = key
    if kicked is None:
        return INSERT_SUCCESSFUL

    changes.append((kicked, hash, 1))
    return insert_to_second(table, kicked, rem_kicks - 1, changes)


def insert_to_second(table: CuckooHashTable, key: int, rem_kicks: int,
                     changes: List[Tuple[int, int, int]]) -> int:
    if rem_kicks < 0:
        return INSERT_FAILED

    hash = table.hash2(key)
    kicked = table.array2[hash]

    table.array2[hash] = key
    if kicked is None:
        return INSERT_SUCCESSFUL

    changes.append((kicked, hash, 2))
    return insert_to_first(table, kicked, rem_kicks - 1, changes)


def h1(key: int) -> int:
    return key % 5


def h2(key: int) -> int:
    return key // 5 % 5


def test() -> None:
    table = CuckooHashTable(5, h1, h2)
    for key in 7, 22, 47, 5, 25:
        assert insert(table, key, 10) == INSERT_SUCCESSFUL

    assert table.array1 == [5, None, 47, None, None]
    assert table.array2 == [25, 7, None, None, 22]

    assert insert(table, 27, 12) == INSERT_FAILED

    assert table.array1 == [5, None, 47, None, None]
    assert table.array2 == [25, 7, None, None, 22]

    assert insert(table, 11, 0) == INSERT_SUCCESSFUL

    assert contains(table, 25)
    assert delete(table, 25)
    assert not contains(table, 25)

    assert table.array1 == [5, 11, 47, None, None]
    assert table.array2 == [None, 7, None, None, 22]

    assert insert(table, 76, 0) == INSERT_SUCCESSFUL
    assert insert(table, 25, 8) == INSERT_FAILED
    assert insert(table, 25, 9) == INSERT_SUCCESSFUL

    assert table.array1 == [5, 76, 22, None, None]
    assert table.array2 == [25, 7, 11, None, 47]
