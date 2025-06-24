#!/usr/bin/env python3

# Povolené knihovny: typing, math

from typing import List, Tuple

# IB002 Domácí úloha 3.
#
# Vaším úkolem bude implementovat dvě funkce s využitím principu binárního
# vyhledávání. V obou případech musí být časová složitost vašeho algoritmu
# nejvýše logaritmická, tedy být ve třídě O(log n).
#
# Dejte si dobrý pozor na složitosti operací s Pythonovskými seznamy.
# Nezapomeňte, že slicing s[x:y] vytváří kopii části seznamu a má tedy nutně
# časovou složitost lineární vůči velikosti vytvořené kopie.
#
# Obě zadané funkce musí být čisté, tj. nesmí modifikovat zadaný vstup.
#
# V tomto a dalších úkolech budeme používat pojem „pole“ pro zdůraznění
# skutečnosti, že se k Pythonovským seznamům chováme jako k polím,
# tj. zejména zde nevyužíváme jejich schopnosti se rozšiřovat a zkracovat.
#
# (Pythonovské seznamy jsou ve skutečnosti tzv. dynamická pole, což je
#  komplikovanější datová struktura, která si zachovává některé dobré
#  vlastnosti pole, např. konstantní přístup k libovolnému prvku.)


# Část 1.
# Implementujte funkci partition, která rozdělí zadané seřazené pole na tři
# části: část s prvky menšími než zadaný klíč, část s prvky rovnými zadanému
# klíči a část s prvky většími než zadaný klíč.
def partition(numbers: List[int], key: int) -> Tuple[int, int]:
    """
    vstup: ‹numbers› – seřazené pole celých čísel
           ‹key›     – celé číslo
    výstup: dvojice ‹left, right› splňující následující podmínky
        left a right jsou celá čísla v rozsahu od 0 do len(numbers) včetně
        prvky na indexech z intervalu [0, left) jsou menší než ‹key›
        prvky na indexech z intervalu [left, right) jsou rovné ‹key›
        prvky na indexech z intervalu [right, len(numbers)) jsou > ‹key›
        (zápis [a, b) znamená polouzavřený interval, tedy včetně a, ale bez b)
    časová složitost: O(log n), kde n je velikost vstupního pole

    Příklady:
    Pro vstup ([1, 3, 3, 7], 3) funkce vrátí dvojici (1, 3).
    Pro vstup ([1, 3, 3, 7, 17, 42, 69, 420], 11) funkce vrátí dvojici (4, 4).
    """

    if not numbers or key < numbers[0]:
        return 0, 0

    if key > numbers[-1]:
        return len(numbers), len(numbers)

    left = 0
    right = len(numbers) - 1
    mid = (left + right) // 2

    while numbers[mid] != key:

        if numbers[mid] <= key:
            left = mid + 1
        else:
            right = mid - 1

        if right < left:  # key sa v poli vobec nenachadza
            return left, left  # prostredny interval je prazdny

        mid = (right + left) // 2

    return find_left_bound(numbers, key, mid), find_right_bound(numbers, key, mid)


def find_left_bound(numbers: List[int], key: int, key_index: int):
    left = 0
    right = key_index
    mid = (left + right) // 2

    while left < right:

        if numbers[mid] == key:
            right = mid
        else:
            left = mid + 1

        mid = (right + left) // 2

    return mid


def find_right_bound(numbers: List[int], key: int, key_index: int):
    left = key_index
    right = len(numbers)
    mid = (left + right) // 2

    while left < right:

        if numbers[mid] == key:
            left = mid + 1
        else:
            right = mid

        mid = (right + left) // 2

    return mid


# Část 2.
# Implementujte funkci minimum, která najde minimální hodnotu v poli
# různých čísel s jediným lokálním minimem.
def minimum(numbers: List[int]) -> int:
    """
    vstup: ‹numbers› – pole vzájemně různých čísel, které obsahuje
                       právě jedno lokální minimum
           lokální minimum definujeme jako prvek pole takový,
           že je menší než jeho sousední prvky (má-li nějaké;
           lokální minimum může být i na kraji pole)
    výstup: hodnota minimálního prvku
    časová složitost: O(log n), kde n je velikost vstupního pole

    Příklady:
    Pro vstup [10, 8, 6, 4, 2, 1, 3, 5, 7, 9] funkce vrátí číslo 1.
    Pro vstup [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] funkce vrátí číslo 0.
    """

    left = 0
    right = len(numbers) - 1
    mid = (left + right) // 2

    while right - left > 1:  # zabrani peeku mimo pola

        if numbers[mid - 1] > numbers[mid] < numbers[mid + 1]:
            return numbers[mid]

        elif numbers[mid - 1] > numbers[mid] > numbers[mid + 1]:
            left = mid + 1

        elif numbers[mid - 1] < numbers[mid] < numbers[mid + 1]:
            right = mid - 1

        mid = (right + left) // 2

    return min(numbers[left], numbers[right])
