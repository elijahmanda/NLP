import pprint

from loguru import logger
from colorama import Fore
from nlp.parsers import load_parser
from nlp.parsers.number.normalize import Pipe
from nlp.parsers.number.config import Config
# logger.enable("nlp.parsers.number.merger")

txt = """
²³ ⅙⅗ ⁷⁸⁹
one hundred and twenty-one
17 billion
900 billion

ten thousand six hundred and ninety-five
one and half
five hundred and half one nine
half
2 and half
two and half
789 and half
5 hundred
10 million 200 million 1 thousand 17 billion 550 million 600 and 25

hello, there,
1,2,3,4,5 list of nums
jc-em
5kg
Area51
Haha1000ahaH
127.0.0.1:5000 ip

1 200 6 899,799 95 123,689

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
2.5c .577G 1.2e2T 23E3Z -208.89years
"""
# expected = txt.split()
# print("Expected:")
# print("Expected length:", len(expected))
# pprint.pprint(expected)
# txt = txt.split("\n")

config = Config(
    bounded_numbers=False,
    signs_allowed=True,
    exclude_separators=(),
)
np = load_parser("number", config=config)
tokens = np(txt)
print("Number parser:")
print("Length:", len(tokens))
for t in tokens:
    print(
        Fore.CYAN, t.text,
        Fore.WHITE, "->",
        Fore.YELLOW, t.metadata["value"], Fore.RESET
    )
