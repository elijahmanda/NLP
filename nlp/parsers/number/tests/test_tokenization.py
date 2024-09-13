import unittest

from nlp.parsers.number.ejtoken import tokenize


class TestTokenization(unittest.TestCase):
    def test_integrity(self):
        text = """
    1 -89 +799 588
    2.5 .577 1.2e2 23E3 -208.89 +13.7
    -2.7e2 +199.123E90 +5e-12 -.5
    -0.244e+19
    2,000 12,999 123,689 2,078,689
    12,089,688 1,230.0971 799,089.13
    124,799,799,588.8981349901
    2,008e10 -12,899 +77,089 9,000.7
    -134,799 -6,799.999 +13,689E-12
    +799,799e+1 -67,799.968e-123
    +78,000E10 -123,147E2
    2'000 12'999 123'689 2'078'689
    12'089'688 1'230.0971 799'089.13
    124'799'799'588.8981349901
    2'008e10 -12'899 +77'089 9'000.7
    -134'799 -6'799.999 +13'689E-12
    +799'799e+1 -67'799.968e-123
    +144'478E10 -133'899E2
    1k -89M +799B 588m
    2.5c .577G 1.2e2T 23E3Z -208.89y
        """
        expected = len(text.split())
        toktok = len(tokenize(text))
        assert expected == toktok

    def test_integrity_tokenkzers_2(self):
        text = (
            # 1_900_000_000
            # "the company had one point five nine two billion dollars in total revenue."
            " This is a list of spoken numbers without any delimiters"
            # 221_655
            " two hundred and twenty-one thousand six hundred and fifty six"
            # 9_000_065
            " nine million sixty five"
            # 27_000_924_099
            " twenty seven billion nine hundred and twenty-four thousand and ninety nine"
            # 2.5
            " Two And half is not enough."
            # 67.5
            " Sixty seven and a half"
            # 6.25
            " six and a quarter"
            # 12.5
            " it had twelve and half total ratings."
            # 2_900_000_000
            " 2.9 trillion Euros is spent each year alone."
            # 9_500_000_000
            " the total damage cost 9 point 5 trillion Canadian dollars."
            " one point two"
            " 509 million"
            " this is a hex number: \"0x12f1\"."
            # 9
            " this is a binary number: \"0b1001\"."
            " this is an octal number: \"0o1723\""
            # 222_000
            " 2.22E+5 was the sum of products offered."
            # 50
            # " 0.5e+2 people are in class."
            " this is a pretty small number: \"2,078e-8\"."
            " \"1'688e8\" is not a very common number format."
            " 79.6818 is a decimal number."
            " .578 is an ambiguous decimal number."
            " 2,000.013 is not a very common number format either."
            " 8'968.688 is a weird number format."
            " 23,000,135 can be ambiguous too because the comma may indicate a list if numbers."
            # " 5,999 same applies to this number."
            " 688,799,778 hi I'm a number."
            " 12,788 don't no if this is common."
            " 68e2 is my exponent friend!"
        )
        toktok = len(tokenize(text))


unittest.main()
