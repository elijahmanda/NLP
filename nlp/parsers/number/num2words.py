
# https://leetcode.com/problems/integer-to-english-words/
# Convert a non-negative integer to its english words representation.
# Given input is guaranteed to be less than 2**31 - 1.

# Build the words from left to right in blocks of 3 digits.
# Time - O(log n)
# Space - O(log n)

from collections import deque

int_to_word = {
    1: 'one', 2: 'two',
    3: 'three', 4: 'four',
    5: 'five', 6: 'six',
    7: 'seven', 8: 'eight',
    9: 'nine', 10: 'ten',
    11: 'eleven', 12: 'twelve',
    13: 'thirteen', 14: 'fourteen',
    15: 'fifteen', 16: 'sixteen',
    17: 'seventeen', 18: 'eighteen',
    19: 'nineteen', 20: 'twenty',
    30: 'thirty', 40: 'forty',
    50: 'fifty', 60: 'sixty',
    70: 'seventy', 80: 'eighty',
    90: 'ninety',
}

DIGITS_TO_WORD = dict([
    (2, 'hundred'),
    (3, 'thousand'),
    (6, 'million'),
    (9, "billion"),
    (12, 'trillion'),
    (15, "quadrillion"),
    (18, "quintillion"),
    (21, "sextillion"),
    (24, "septillion"),
    (27, "octillion"),
    (30, "nonillion"),
    (33, "decillion"),
    (36, "undecillion"),
    (39, "duodecillion"),
    (42, "tredecillion"),
    (45, "quattuordecillion"),
    (48, "quinquadecillion"),
    (51, "sedecillion"),
    (54, "septendecillion"),
    (57, "octodecillion"),
    (60, "novendecillion"),
    (63, "vigintillion"),
    (66, "unvigintillion"),
    (69, "uuovigintillion"),
    (72, "tresvigintillion"),
    (75, "quattuorvigintillion"),
    (78, "quinquavigintillion"),
    (81, "qesvigintillion"),
    (84, "septemvigintillion"),
    (87, "octovigintillion"),
    (90, "novemvigintillion"),
    (93, "trigintillion"),
    (96, "untrigintillion"),
    (99, "duotrigintillion"),
    (102, "trestrigintillion"),
    (105, "quattuortrigintillion"),
    (108, "quinquatrigintillion"),
    (111, "sestrigintillion"),
    (114, "septentrigintillion"),
    (117, "octotrigintillion"),
    (120, "noventrigintillion"),
    (123, "quadragintillion"),
])


class Num2Words:

    def number_to_words(self, num):
        """
        :type num: int
        :rtype: str
        """
        english = deque()
        digits = 0
        if num == 0:
            return "Zero"

        while num:

            # section is the block of 3 digits
            num, section = divmod(num, 1000)
            hundreds, tens = divmod(section, 100)

            if section and digits > 0:
                english.appendleft(DIGITS_TO_WORD[digits])
            digits += 3

            if tens >= 20:
                if tens % 10:
                    english.appendleft(int_to_word[tens % 10])
                english.appendleft(int_to_word[10*(tens//10)])
            elif tens:
                english.appendleft(int_to_word[tens])

            if hundreds:
                english.appendleft("hundred")
                english.appendleft(int_to_word[hundreds])

        return " ".join(english)


def num2words(num, point=None, negative=None):
    neg = " "
    if num < 0:
        num = abs(num)
        neg = "negative " if negative is None else f"{negative} "
    dec = None
    if isinstance(num, float) and "." in str(num):
        num, dec = str(num).split(".")
        num = int(num)
        dec = list(map(int, dec))
    n2w = Num2Words()
    try:
        num = n2w.numberToWords(num)
    except KeyError:
        raise Exception("Number %d too large" % num) from None
    if dec is not None:
        point = "point" if point is None else point
        # print(num, dec, point)
        num += f" {point} " + \
            " ".join(map(lambda x: int_to_word.get(x, "zero"), dec))
    return (neg + num).lower().strip()
