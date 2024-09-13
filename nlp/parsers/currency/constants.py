from __future__ import annotations

from typing import List, TypedDict

from nlp.parsers.gpe.demonym import Demonym


NAME = "name"
DEMONYM = "demonym"
MAJOR_SINGLE = "majorSingle"
MAJOR_PLURAL = "majorPlural"
SYMBOL = "symbol"
SYMBOL_NATIVE = "symbolNative"
MINOR_SINGLE = "minorSingle"
MINOR_PLURAL = "minorPlural"
ALIAS = "alias"


class CurrencyAlias(TypedDict):

    demonym: str
    major_plural: str
    major_single: str
    minor_plural: str
    minor_single: str


CURRENCY_ALIASES: List[CurrencyAlias] = [
    {
        DEMONYM: Demonym.US,
        MAJOR_PLURAL: ["bucks"],
        MAJOR_SINGLE: ["buck"],
        MINOR_PLURAL: [],
        MINOR_SINGLE: [],
    },
    {
        DEMONYM: Demonym.ZAMBIAN,
        MAJOR_PLURAL: ["ZMK"],
        MAJOR_SINGLE: ["ZMK"],
        MINOR_PLURAL: [],
        MINOR_SINGLE: [],
    }
]

OTHER_CURRENCIES: List[str] = ['₿', '₤', ' تومان', 'ރ', 'WS$', 'د.ع.\u200f', 'د.ك.\u200f', 'د.ج.\u200f', 'د.م.\u200f', 'د.إ.\u200f', 'د.ت.\u200f', 'د.ل.\u200f', 'د.ب.\u200f', 'د.أ.\u200f', '₢', 'динар', 'Dinara', 'тңг', 'টকা', '₶', '₠', '৲', 'EUR', 'дин.', 'DKK',
                               'BN$', 'ل.س.\u200f', 'ل.ل.\u200f', '₳', 'ℳ', 'US$', '₷', 'eur', 'LB£', 'CHF', 'تومان', '₧', 'ج.م.\u200f', '₰', '₯', '￥', 'नेरू', '૱', '₨', 'ман.', 'ر.ق.\u200f', 'ر.ع.\u200f', 'ر.ي.\u200f', 'ر.س.\u200f', 'SY£', 'лв', 'руб', '௹', 'грн.', 'Bds$', 'A$', 'тңг.']
OTHER_CURRENCIES.sort(key=len, reverse=True)
