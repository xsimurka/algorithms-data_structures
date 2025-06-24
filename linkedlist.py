#!/usr/bin/env python3

from typing import Optional, Tuple

# IB002 Domácí úloha 1.
#
# V této úloze budete implementovat operace nad jednosměrně zřetězeným
# seznamem. Jednosměrně zřetězený seznam ma pouze jeden atribut ‹first›,
# který se odkazuje na začátek seznamu. Každý uzel v seznamu pak má dva
# atributy: ‹value›, který drží hodnotu daného uzlu, a ‹next›, který ukazuje
# na další uzel v seznamu nebo ‹None›, pokud je aktuální uzel poslední.
#
# Korektní jednosměrně zřetězený seznam je takový, že buď je ‹first› None
# nebo se odkazuje na uzel takový, že procházením skrze odkazy ‹next› dojdeme
# k poslednímu uzlu. To znamená, že korektní jednosměrně zřetězený seznam
# se nikde nesmí zacyklit.
#
# Smyslem této úlohy je připomenout si práci s odkazy.
# V celé této úloze je zakázáno v implementaci používat vestavěné Pythonovské
# datové typy seznam (list), slovník (dict), množina (set).
# Pokud chcete tyto datové typy používat pro vlastní testování, nezapomeňte
# je před odevzdáním vymazat nebo zakomentovat.
#
# Povolená je pouze jediná Pythonovská knihovna, a to typing.
# (Vřele doporučujeme používat nástroje pro statickou analýzu typových anotací,
#  např. nástroj ‹mypy›. Může vám pomoci včas odhalit typové chyby, které
#  se mnohem hůře odhalují za běhu.)
#
# V příkladech a ve výstupu z testů znázorňujeme jednosměrně zřetězené
# seznamy následovně:
#
#   → 3 → 4 → 5 → 7
# Toto reprezentuje seznam o čtyřech uzlech. První uzel má hodnotu 3, jeho
# následníkem je uzel s hodnotou 4 atd. Poslední uzel má hodnotu 7.
#
# Prázdný seznam (tj. seznam, jehož ‹first› je ‹None›) znázorníme takto:
#   →
#
# Jednoprvkový seznam znázorníme takto:
#   → 17
#
# Do definic tříd LinkedList a Node nijak nezasahujte.
# (Pro zvídavé: Deklarace __slots__ mimo jiné zaručuje, že se objektům daných
#  tříd nedá přidat žádný jiný atribut než ty deklarované, což pomáhá odhalit
#  překlepy typu ‹frist›.)


class LinkedList:
    """Třída LinkedList reprezentuje jednosměrně zřetězený seznam.

    Atributy:
        first   odkaz na první uzel seznamu (nebo ‹None›)
    """
    __slots__ = "first"

    def __init__(self) -> None:
        self.first: Optional[Node] = None


class Node:
    """Třída Node reprezenujte uzel ve zřetězeném seznamu.
    Objekty typu Node se inicializují jako ‹Node(hodnota)›.

    Atributy:
        value   hodnota uzlu
        next    odkaz na další uzel seznamu (nebo ‹None›)
    """
    __slots__ = "value", "next"

    def __init__(self, value: int) -> None:
        self.value = value
        self.next: Optional[Node] = None


# Část 1.
# Implementujte funkci keep_each, která ze zadaného jednosměrně zřetězeného
# seznamu odstraní uzly tak, aby zůstal pouze každý k. uzel. Číslo k je vždy
# alespoň 2.

def keep_each(linked_list: LinkedList, k: int) -> None:
    """
    vstup: ‹linked_list› – korektní jednosměrně zřetězený seznam
           ‹k›           – celé číslo ≥ 2
    výstup: žádný,
            ze vstupního seznamu ‹linked_list› jsou odstraněny uzly tak,
            aby v něm zůstal pouze každý ‹k›. uzel
            (seznam musí samozřejmě zůstat korektní)
    časová složitost: O(n), kde n je délka vstupního seznamu, tedy lineární
    extra prostorová složitost: O(1), tedy konstantní
        (zejména tedy nesmíte vytvářet nový seznam;
         smíte jen modifikovat ten vstupní)

    Příklady:
    Pro vstup → 1 → 2 → 3 → 4 → 5 a k = 2 bude seznam modifikován
    na → 2 → 4.
    Pro vstup → 10 → 7 → 1 → 2 → 3 → 4 → 19 a k = 3 bude seznam
    modifikován na → 1 → 4.
    """
    index = 1
    actual = linked_list.first
    last: Optional[Node] = None

    while actual is not None:
        if index % k == 0:
            if last is None:
                linked_list.first = actual
            else:
                last.next = actual

            last = actual

        actual = actual.next
        index += 1

    if last is None:
        linked_list.first = None
    else:
        last.next = None


# Část 2.
# Implementuje funkci split_by_value, která rozdělí zadaný jednosměrně
# zřetězený seznam na dva – uzly s hodnotami menší nebo rovné zadané hodnotě
# budou v „levém“ seznamu, ostatní uzly budou v „pravém“ seznamu. Pořadí uzlů
# ve výsledných seznamech musí odpovídat jejich pořadí v původním seznamu.

def split_by_value(linked_list: LinkedList, value: int) \
        -> Tuple[LinkedList, LinkedList]:
    """
    vstup: ‹linked_list› – korektní jednosměrně zřetězený seznam
           ‹value›       – hodnota, podle které chceme seznam rozdělit
    výstup: dvojice korektních jednosměrně zřetězených seznamů (levý, pravý)
            levý seznam obsahuje uzly s hodnotami ≤ ‹value›,
            pravý seznam obsahuje uzly s hodnotami > ‹value›
            pořadí uzlů v seznamech odpovídá pořadí v původním seznamu
    časová složitost: O(n), kde n je délka vstupního seznamu, tedy lineární
    extra prostorová složitost: O(1), tedy konstantní
        (zejména tedy nesmíte vytvářet nové uzly;
         modifikujte jen jejich atributy ‹next›)

    Příklady:
    Pro vstup → 17 → 42 → 0 → -7 a value = 0 funkce vrátí dvojici
    seznamů → 0 → -7 (levý) a → 17 → 42 (pravý).
    Pro vstup → 1 → 7 → 2 → 5 → 3 → 4 a value = 6 funkce vrátí dvojici
    seznamů → 1 → 2 → 5 → 3 → 4 a → 7.
    """
    left, right = LinkedList(), LinkedList()
    left_last: Optional[Node] = None
    right_last: Optional[Node] = None
    actual = linked_list.first

    while actual is not None:
        if actual.value <= value:
            if left_last is None:
                left.first = actual
            else:
                left_last.next = actual

            left_last = actual

        else:
            if right_last is None:
                right.first = actual
            else:
                right_last.next = actual

            right_last = actual

        actual = actual.next

    if left_last is not None:
        left_last.next = None

    if right_last is not None:
        right_last.next = None

    return left, right
