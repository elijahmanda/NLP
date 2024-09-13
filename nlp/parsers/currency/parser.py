# -*- coding: utf-8 -*-
import re
import string
from typing import Callable, Optional, Pattern, List, Tuple

from nlp.parsers.currenci._currencies import (
    CURRENCY_CODES,
    CURRENCY_NATIONAL_SYMBOLS,
    CURRENCY_SYMBOLS
)


def or_regex(symbols: List[str]) -> Pattern:
    """ Return a regex which matches any of ``symbols`` """
    return re.compile('|'.join(re.escape(s) for s in symbols))


# If one of these symbols is found either in price or in currency,
# it is considered currency symbol, and returned as a currency, regardless
# of its position in text.
SAFE_CURRENCY_SYMBOLS = [
    # Variants of $, etc. They need to be before $.
    'Bds$', 'CUC$', 'MOP$',
    'AR$', 'AU$', 'BN$', 'BZ$', 'CA$', 'CL$', 'CO$', 'CV$', 'HK$', 'MX$',
    'NT$', 'NZ$', 'TT$', 'RD$', 'WS$', 'US$',
    '$U', 'C$', 'J$', 'N$', 'R$', 'S$', 'T$', 'Z$', 'A$',
    'SY£', 'LB£', 'CN¥', 'GH₵',

    # unique currency symbols
    '$', '€', '£', 'zł', 'Zł', 'Kč', '₽', '¥', '￥',
    '฿', 'դր.', 'դր', '₦', '₴', '₱', '৳', '₭', '₪',  '﷼', '៛', '₩', '₫', '₡',
    'টকা', 'ƒ', '₲', '؋', '₮', 'नेरू', '₨',
    '₶', '₾', '֏', 'ރ', '৲', '૱', '௹', '₠', '₢', '₣', '₤', '₧', '₯',
    '₰', '₳', '₷', '₸', '₹', '₺', '₼', '₾', '₿', 'ℳ',
    'ر.ق.\u200f', 'د.ك.\u200f', 'د.ع.\u200f', 'ر.ع.\u200f', 'ر.ي.\u200f',
    'ر.س.\u200f', 'د.ج.\u200f', 'د.م.\u200f', 'د.إ.\u200f', 'د.ت.\u200f',
    'د.ل.\u200f', 'ل.س.\u200f', 'د.ب.\u200f', 'د.أ.\u200f', 'ج.م.\u200f',
    'ل.ل.\u200f',

    ' تومان', 'تومان',

    # other common symbols, which we consider unambiguous
    'EUR', 'euro', 'eur', 'CHF', 'DKK', 'Rp', 'lei',
    'руб.', 'руб',  'грн.', 'грн', 'дин.', 'Dinara', 'динар', 'лв.', 'лв',
    'р.', 'тңг', 'тңг.', 'ман.',
]

# "D" in some abbreviations means "dollar", and so currency
# can be written as SGD$123 or NZD $123. Currency code should take priority
# over $ symbol in this case.
DOLLAR_CODES = [k for k in CURRENCY_CODES if k.endswith('D')]
_DOLLAR_REGEX = re.compile(
    r'''
        \b
        (?:{})  # currency code like NZD
        (?=
            \$?  # dollar sign to ignore if attached to the currency code
            (?:[\W\d]|$)  # not a letter
        )
    '''.format('|'.join(re.escape(k) for k in DOLLAR_CODES)),
    re.VERBOSE,
)


# Other common currency symbols: 3-letter codes, less safe abbreviations
OTHER_CURRENCY_SYMBOLS_SET = (
    set(
        CURRENCY_CODES +
        CURRENCY_SYMBOLS +
        CURRENCY_NATIONAL_SYMBOLS +

        # even if they appear in text, currency is likely to be rouble
        ['р', 'Р']
    )
    - set(SAFE_CURRENCY_SYMBOLS)   # already handled
    - {'-', 'XXX'}                 # placeholder values
    - set(string.ascii_uppercase)  # very unreliable on their own
)
OTHER_CURRENCY_SYMBOLS = sorted(OTHER_CURRENCY_SYMBOLS_SET,
                                key=len, reverse=True)

_search_dollar_code = _DOLLAR_REGEX.search
_search_safe_currency = or_regex(SAFE_CURRENCY_SYMBOLS).search
_search_unsafe_currency = or_regex(OTHER_CURRENCY_SYMBOLS).search


def extract_currency_symbol(price: Optional[str],
                            currency_hint: Optional[str]) -> Optional[str]:
    """
    Guess currency symbol from extracted price and currency strings.
    Return an empty string if symbol is not found.
    """
    methods: List[Tuple[Callable, Optional[str]]] = [
        (_search_safe_currency, price),
        (_search_safe_currency, currency_hint),
        (_search_unsafe_currency, price),
        (_search_unsafe_currency, currency_hint),
    ]

    if currency_hint and '$' in currency_hint:
        methods.insert(0, (_search_dollar_code, currency_hint))

    if price and '$' in price:
        methods.insert(0, (_search_dollar_code, price))

    for meth, attr in methods:
        m = meth(attr) if attr else None
        if m:
            return m.group(0)

    return None
