import loguru
from nlp.utils.timer import timer
from colorama import Fore
from humanize.number import intword, scientific
from nlp.parsers.number.config import Config
from nlp.entity import ExtractionPipeline
from nlp.parsers import load_parser
import random

random.seed = 42


# loguru.logger.enable("nlp")

np = load_parser("number", config=Config(merge=True))
extraction = ExtractionPipeline([
    np,
])


text = (
    # 1_900_000_000
    # "the company had one point five nine two billion dollars in total revenue."
    " This is a list of spoken numbers without any delimiters"
    # 221_655
    " two hundred and twenty-one thousand six hundred and fifty six"
    # 9_000_065
    " nine million sixty five"
    # 27_000_924_099
    " twenty seven billion nine hundred twenty five thousand and ninety nine"
    # 2.5
    " Two and a Half is not enough."
    # 67.5
    " seventy seven and a half"
    # 6.25
    " six and quarter"
    # 12.5
    " it had twelve and half total ratings."
    # 2_900_000_000
    " 2.9 trillion Euros is spent each year alone."
    # 9_500_000_000
    " 9.5 trillion Canadian dollars."
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

sep = Fore.WHITE + " ->"
# res = timer()(np.parse_tokenize)(text)
res = timer()(extraction.extract)(text)
print("TEXT LENGTH:", len(text), "NUMBERS:", len(
    [t for t in res if t.entity == "number"]))
# 27, 000, 925, 099

for i, r in enumerate(res):
    print("-" * 42)
    if r.text.isspace():
        continue
    if r.entity == "number":
        meta = r.metadata
        spoken_value = meta["value"]
        value = spoken_value
        ntype = meta["number_type"]
        if value > 1000:
            spoken_value = intword(value, format="%.0f")
        elif abs(value) < 0.0001:
            spoken_value = scientific(value)

        print(
            f"{i}. ",
            Fore.YELLOW,
            r.text,
            sep,
            Fore.LIGHTCYAN_EX,
            f"{value:,}",
            sep,
            Fore.CYAN,
            spoken_value,
            sep,
            Fore.BLUE,
            ntype,
            Fore.RESET,
        )
    else:
        if r.entity:
            print(Fore.LIGHTMAGENTA_EX, r.text, sep,
                  Fore.LIGHTRED_EX, r.entity, Fore.RESET)
        else:
            print(r.text)
