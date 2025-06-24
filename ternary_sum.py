#!/usr/bin/env python3

# Povolené knihovny: typing, math

from typing import List

# IB002 Domácí úloha 4
#
# Trojková (ternární) soustava je poziční číselná soustava o základu 3,
# která používá číslice 0, 1, 2. Tedy např. číslo 42 ve trojkové soustavě
# zapíšeme jako (1120)₃.
#
# Vaším úkolem bude implementovat funkci, která pro zadané parametry
# ‹length› a ‹total› vrátí vzestupně seřazený Pythonovský seznam všech
# kladných celých čísel, která mají ve trojkové soustavě právě ‹length›
# číslic a jejichž součet trojkových číslic je právě ‹total›. Přitom
# uvažujeme pouze zápis čísla bez zbytečných levostranných nul, tedy
# např. číslo 42 má ve trojkové soustavě právě čtyři číslice, ne více.
#
# Příklady:
# Pro vstup ‹length = 3› a ‹total = 5› bude výstupem seznam:
#   [17, 23, 25]
# ve trojkové soustavě bychom totiž tato čísla zapsali jako:
#   (122)₃, (212)₃, (221)₃
#
# Pro vstup ‹length = 4› a ‹total = 2› bude výstupem seznam:
#   [28, 30, 36, 54]
# ve trojkové soustavě bychom totiž tato čísla zapsali jako:
#   (1001)₃, (1010)₃, (1100)₃, (2000)₃
#
# Počty čísel splňujících zadanou podmínku se dají zapsat do takovéto
# tabulky:
#
#          │                    total
#   length │  1   2   3   4   5   6   7   8   9  10  11  ...
#   ───────┼────────────────────────────────────────────
#      1   │  1   1   0   0   0   0   0   0   0   0   0
#      2   │  1   2   2   1   0   0   0   0   0   0   0
#      3   │  1   3   5   5   3   1   0   0   0   0   0
#      4   │  1   4   9  13  13   9   4   1   0   0   0
#      5   │  1   5  14  26  35  35  26  14   5   1   0
#     ...
#
# Při podrobnějším zkoumání této tabulky si můžete všimnout jisté
# pravidelnosti; snadno pak dopočítáte další řádky. Hodnoty v tabulce
# jednak můžete využít pro částečnou kontrolu toho, že vaše řešení
# počítá správně, jednak budou hrát roli v časové složitosti řešení.
#
# Smyslem tohoto úkolu je procvičit si rekurzi. Vstupy v testech budou
# takové, aby rozumně použitá rekurze nenarazila na žádný limit.
#
# Kritickou částí tohoto úkolu je časová složitost řešení. Pro splnění
# požadavků je třeba si jednak dobře rozmyslet, ve kterých chvílích
# je vhodné rekurzi ukončit, jednak si dát pozor na to, co přesně
# děláte s Pythonovskými seznamy a jakou mají tyto operace složitost.
#
# Při analýze časové složitosti jako obvykle zanedbáváme přesnou složitost
# aritmetických operací s čísly, tj. považujeme ji za konstantní.
#
# Nezapomeňte, že si můžete definovat pomocné funkce. V tomto úkolu je
# to určitě velmi vhodné.


def ternary_sum(length: int, total: int) -> List[int]:
    """
    vstup: ‹length› – kladné celé číslo
           ‹total› – kladné celé číslo
    výstup: vzestupně seřazený seznam všech kladných celých čísel,
            která mají ve trojkové soustavě právě ‹length› číslic
            a součet jejichž trojkových číslic je právě ‹total›
    časová složitost: O(T(length, total) · length),
        kde T(length, total) je hodnota z tabulky naznačené výše
    """

    result: List[int] = []
    ternary_sum_rec(result, [], length, total, True)
    return result


def ternary_sum_rec(result: List[int], actual: List[int], length: int,
                    remaining: int, first: bool) -> None:
    if len(actual) == length:
        if remaining == 0:
            result.append(from_ternary_to_decimal(actual))

        actual.pop()
        return

    for i in range(1 if first else 0, 3):
        # zareze pripady ked uz nie je mozne dosiahnut ciel
        if remaining < i or remaining > 2 * (length - len(actual)):
            break

        actual.append(i)
        ternary_sum_rec(result, actual, length, remaining - i, False)

    not first and actual.pop()  # zabrani popnut z prazdneho zoznamu


def from_ternary_to_decimal(num: List[int]) -> int:
    result = 0
    exponent = len(num) - 1

    for i in range(len(num)):
        result += num[i] * (3 ** exponent)
        exponent -= 1

    return result
