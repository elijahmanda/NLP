from functools import cached_property
import regex
import re
from retrie.retrie import Whitelist
from nlp.utils.cache import single_cache
from nlp.utils.sequences import reverse_dict
from nlp.utils.regex import (
    join,
    bound,
    all_cases
)


B_LEFT = "(?<![a-zA-Z_])"
B_RIGHT = "(?![a-zA-Z_])"


class Data:

    def __init__(self, config):
        self.config = config

    @property
    def DEFAULT_RE_FLAGS(self):
        return "(?i)(?m)(?x)"

    @property
    def A(self):
        return ("a",)

    @property
    def ANDS(self):
        return ("and",)

    @property
    def POINTS(self):
        return ("point", ".")

    @property
    def NEGATIVES(self):
        return ("negative", "neg", "minus")

    @property
    def ZEROS(self):
        return ("zero", 0)

    @property
    @single_cache()
    def ONES(self):
        ones = dict([
            ("zero", 0),
            ("one", 1),
            ("two", 2),
            ("three", 3),
            ("four", 4),
            ("five", 5),
            ("six", 6),
            ("seven", 7),
            ("eight", 8),
            ("nine", 9),
        ])
        ones.update(self.ORDINAL_ONES)
        return ones

    @property
    @single_cache()
    def TEENS_AND_TEN(self):
        res = dict([
            ("ten", 10),
            ("eleven", 11),
            ("twelve", 12),
            ("thirteen", 13),
            ("fourteen", 14),
            ("fifteen", 15),
            ("sixteen", 16),
            ("seventeen", 17),
            ("eighteen", 18),
            ("nineteen", 19),
        ])
        res.update(self.ORDINAL_TEENS_AND_TEN)
        return res

    @property
    @single_cache()
    def TENS(self):
        res = dict([
            ("twenty", 20),
            ("thirty", 30),
            ("forty", 40),
            ("fifty", 50),
            ("sixty", 60),
            ("seventy", 70),
            ("eighty", 80),
            ("ninety", 90),
        ])
        res.update(self.ORDINAL_TENS)
        return res

    @property
    @single_cache()
    def MULTIPLES(self):
        res = reverse_dict(dict([
            (100, 'hundred'),
            (1000, 'thousand'),
            (1_000_000, 'million'),
            (1_000_000_000, "billion"),
            (1_000_000_000_000, 'trillion'),
            (int(1e15), "quadrillion"),
            (1e18, "quintillion"),
            (1e21, "sextillion"),
            (1e24, "septillion"),
            (1e27, "octillion"),
            (1e30, "nonillion"),
            (1e33, "decillion"),
            (1e36, "undecillion"),
            (1e39, "duodecillion"),
            (1e42, "tredecillion"),
            (1e45, "quattuordecillion"),
            (1e48, "quinquadecillion"),
            (1e51, "sedecillion"),
            (1e54, "septendecillion"),
            (1e57, "octodecillion"),
            (1e60, "novendecillion"),
            (1e63, "vigintillion"),
            (1e66, "unvigintillion"),
            (1e69, "uuovigintillion"),
            (1e72, "tresvigintillion"),
            (1e75, "quattuorvigintillion"),
            (1e78, "quinquavigintillion"),
            (1e81, "qesvigintillion"),
            (1e84, "septemvigintillion"),
            (1e87, "octovigintillion"),
            (1e90, "novemvigintillion"),
            (1e93, "trigintillion"),
            (1e96, "untrigintillion"),
            (1e99, "duotrigintillion"),
            (1e102, "trestrigintillion"),
            (1e105, "quattuortrigintillion"),
            (1e108, "quinquatrigintillion"),
            (1e111, "sestrigintillion"),
            (1e114, "septentrigintillion"),
            (1e117, "octotrigintillion"),
            (1e120, "noventrigintillion"),
            (1e123, "quadragintillion"),
        ]))
        res.update(self.ORDINAL_MULTIPLES)
        return dict(res)

    @property
    @single_cache()
    def ORDINAL_ONES(self):
        res = dict([
            ("first", 1),
            ("second", 2),
            ("third", 3),
            ("fourth", 4),
            ("fifth", 5),
            ("sixth", 6),
            ("seventh", 7),
            ("eighth", 8),
            ("ninth", 9),
        ])
        exclude_ordinal_ones = self.config.exclude_ordinal_ones
        if exclude_ordinal_ones:
            if isinstance(exclude_ordinal_ones, str):
                if exclude_ordinal_ones == "all":
                    return dict()
                raise ValueError("Expected `all` for exclude_ordinal_ones")
            for suffix in exclude_ordinal_ones:
                res.pop(suffix, None)
        return res

    @property
    def ORDINAL_TEENS_AND_TEN(self):
        res = dict([
            ("tenth", 10),
            ("eleventh", 11),
            ("twelfth", 12),
            ("thirteenth", 13),
            ("fourteenth", 14),
            ("fifteenth", 15),
            ("sixteenth", 16),
            ("seventeenth", 17),
            ("eighteenth", 18),
            ("nineteenth", 19),
        ])
        return res

    @property
    def ORDINAL_TENS(self):
        res = dict([
            ("twentieth", 20),
            ("thirtieth", 30),
            ("fortieth", 40),
            ("fiftieth", 50),
            ("sixtieth", 60),
            ("seventieth", 70),
            ("eightieth", 80),
            ("ninetieth", 90),
        ])
        return res

    @property
    @single_cache()
    def ORDINAL_MULTIPLES(self):
        res = dict([
            ("hundredth", 100),
            ("thousandth", 1000),
            ("millionth", 1_000_000),
            ("billionth", 1_000_000_000),
            ("trillionth", 1_000_000_000_000),
            ("quadrillionth", 1e24),
            ("quintillionth", 1e30),
            ("sextillionth", 1e36),
            ("septillionth", 1e42),
            ("octillionth", 1e48),
            ("nonillionth", 1e54),
            ("decillionth", 1e60),
        ])
        res.update(self.SUFFIXES_BY_NAME)
        return dict(res)

    @property
    @single_cache()
    def SUFFIXES(self):
        res = dict([
            ("y", 1e-24),  # Yocto
            ("z", 1e-21),  # Zepto
            ("a", 1e-18),  # Atto
            ("f", 1e-15),  # Femto
            ("p", 1e-12),  # Pico
            ("n", 1e-9),  # Nano
            # (chr(181), 1e-6), # Micro μ
            # (chr(956), 1e-6), # Micro
            ("m", 0.001),  # Milli
            ("c", 0.01),  # Centi
            ("d", 0.1),  # Deci
            ("da", 10),  # Deca
            ("h", 100),  # Hecto
            ("k", 1000),  # Kilo
            ("M", 1_000_000),  # Mega
            ("G", 1_000_000_000),  # Giga
            ("B", 1_000_000_000),  # Billion
            ("T", 1_000_000_000_000),  # Tera
            ("P", int(1e15)),  # Peta
            # ("E", 1e18), # Exa
            ("Z", 1e21),  # Zera
            ("Y", 1e24),  # Yotta
        ])
        exclude_suffixes = self.config.exclude_suffixes
        if exclude_suffixes:
            if isinstance(exclude_suffixes, str):
                if exclude_suffixes == "all":
                    return dict()
                raise ValueError("Expected `all` for exclude_suffixes")
            for suffix in exclude_suffixes:
                res.pop(suffix, None)
        return res

    @property
    def SUFFIXES_BY_NAME(self):
        res = dict([
            ("yocto", 1e-24),  # y
            ("zepto", 1e-21),  # z
            ("atto", 1e-18),  # a
            ("femto", 1e-15),  # f
            ("pico", 1e-12),  # p
            ("nano", 1e-9),  # n
            ("micro", 1e-6),  # μ
            ("milli", 0.001),  # m
            ("centi", 0.01),  # c
            ("deci", 0.1),  # d
            ("deca", 10),  # da
            ("hecto", 100),  # h
            ("kilo", 1000),  # k
            ("mega", 1_000_000),  # M
            ("giga", 1_000_000_000),  # G
            ("tera", 1_000_000_000_000),  # T
            ("peta", int(1e15)),  # P
            ("exa", 1e18),  # E
            ("zetta", 1e21),  # Z
            ("yotta", 1e24),  # Y
        ])
        return res

    @property
    def INFORMAL_EXACT(self):
        res = dict([
            # ("single", 1),
            # ("couple", 2),
            ("half", 0.5),
            ("quarter", 0.25),
            # ("pair", 2),
            # ("few", 3),
            ("dozen", 12),
        ])
        return res

    @property
    def INFORMALS_MULTIPLYABLE(self):
        """
         multiplyable such that NUM couples, NUM pairs, NUM couples of # a number can follow this, such that: 2 couples, 35 pairs, or 10 dozens.
         """
        res = dict([
            ("couples", 2),
            ("pairs", 2),
            ("dozens", 12),
            ("quarters", 0.25),
            ("halves", 0.5),
        ])
        return res

    @property
    def SUPERSCRIPT_ONES(self):
        res = {
            "⁰": 0,
            "¹": 1,
            "²": 2,
            "³": 3,
            "⁴": 4,
            "⁵": 5,
            "⁶": 6,
            "⁷": 7,
            "⁸": 8,
            "⁹": 9,
        }
        return res

    @cached_property
    def SUPERSCRIPT_ONES_REGEX(self):
        return re.compile("(?:["
                          + "".join(self.SUPERSCRIPT_ONES)
                          + "])+")

    @property
    def SUBSCRIPT_ONES(self):
        res = {
            "₀": 0,
            "₁": 1,
            "₂": 2,
            "₃": 3,
            "₄": 4,
            "₅": 5,
            "₆": 6,
            "₇": 7,
            "₈": 8,
            "₉": 9,
        }
        return res

    @cached_property
    def SUBSCRIPT_ONES_REGEX(self):
        return re.compile(
            "(?:["
            + ("".join(re.escape(c) for c in self.SUBSCRIPT_ONES))
            + "])+")

    @property
    def SUPERSCRIPT_FRACTIONS(self):
        res = dict({
            # 1
            "½": 0.5, "⅓": 1/3, "¼": 1/4,
            "⅕": 1/5, "⅙": 1/6, "⅐": 1/7,
            "⅛": 1/8, "⅑": 1/9, "⅒": 1/10,
            # 2
            "⅖": 2/5, "⅔": 2/3,
            # 3
            "¾": 3/4, "⅗": 3/5, "⅜": 3/8,
            # 4
            "⅘": 4/5,
            # 5
            "⅚": 5/6, "⅝": 5/8,
            # 7
            "⅞": 7/8,
        })
        return res

    @cached_property
    def SUPERSCRIPT_FRACTIONS_REGEX(self):
        return re.compile("(?:[" + ("".join(re.escape(c) for c in self.SUPERSCRIPT_FRACTIONS)) + "])")

    @property
    def ORDINAL_SUFFIXES(self):
        return ("st", "nd", "rd", "th")

    @property
    @single_cache()
    def ORDINALS(self):
        res = dict()
        res.update(self.ORDINAL_ONES)
        res.update(self.ORDINAL_TEENS_AND_TEN)
        res.update(self.ORDINAL_TENS)
        res.update(self.ORDINAL_MULTIPLES)
        return res

    @property
    @single_cache()
    def INFORMAL_ALL(self):
        res = dict()
        res.update(self.INFORMAL_EXACT)
        res.update(self.INFORMALS_MULTIPLYABLE)
        _infkeys = res.copy().keys()
        _infvals = res.copy().values()
        res.update(zip(_infvals, _infvals))
        return res

    @property
    def ALL_NUMS(self):
        res = dict()
        res.update(self.ONES)
        res.update(self.TEENS_AND_TEN)
        res.update(self.TENS)
        res.update(self.MULTIPLES)
        res.update(self.INFORMAL_ALL)
        return res

    @property
    @single_cache()
    def ALL_VALID(self):
        res = self.ALL_NUMS
        res.update(
            dict(
                zip(
                    map(str, res.values()),
                    res.values(),
                )
            )
        )
        other = self.A \
            + self.POINTS \
            + self.ANDS \
            + self.NEGATIVES
        res.update(
            zip(
                other,
                range(len(other))
            )
        )
        res.update(self.ORDINALS)
        return res

    @cached_property
    def _tens(self):
        return join(self.TENS.keys())

    @cached_property
    def _ones(self):
        return join([n for n in self.ONES if n != "zero"])

    @cached_property
    def _ordinal_ones(self):
        return join(self.ORDINAL_ONES.keys())

    @cached_property
    def _teens(self):
        return join([n for n in self.TEENS_AND_TEN if n != "ten"])

    @cached_property
    def _multiples(self):
        return join(self.MULTIPLES.keys())

    @cached_property
    def _negs(self):
        return join(self.NEGATIVES)

    @cached_property
    def _points(self):
        return join(self.POINTS)

    # tens-ones eg twenty-five, seventy-six
    @cached_property
    def HYPHEN(self):
        return re.compile(fr"""
        \b(
        ({self._tens})-({self._ones}
        |
        {self._ordinal_ones}
        |
        {self._multiples})
        |
        ({self._ones})-({self._multiples}|hundred)
        |
        ({self._teens})-({self._multiples})
        )\b
        """, re.I | re.VERBOSE)

    @cached_property
    def INTEGER_REGEX(self):
        seps = {",", "_", "'", " "}  # space Seperators doesn't work!
        if self.config.exclude_separators:
            seps -= set(self.config.exclude_separators)
        patterns = []
        for sep in seps:
            patterns.append(fr"\d{{,3}}(?:{sep}\d{{3}})+")
        patterns.append(r"\d+")
        pattern = "|".join(patterns)
        pattern = "(?:" + pattern + ")"
        if self.config.signs_allowed:
            pattern = r"(?:[\-\+])?" + pattern
        if self.config.bounded_numbers:
            pattern = r"\b" + pattern
        return re.compile(pattern)

    @cached_property
    def FLOAT_REGEX(self):
        intre = self.INTEGER_REGEX.pattern
        if self.config.bounded_numbers:
            intre = intre.lstrip(r"\b")
        pattern = (
            intre + r"(?:\.\d+(?:[eE][\-\+]?\d+)?)"
            "|" + intre + r"(?:(?:\.\d+)?[eE][\-\+]?\d+)"
            "|" + intre + r"(?:\.\d+(?:[eE][\-\+]?\d+)?)"
            "|" + intre + r"(?:(?:\.\d+)?[eE][\-\+]?\d+)"
            "|" + intre + r"(?:\.\d+(?:[eE][\-\+]?\d+)?)"
            "|" + intre + r"(?:(?:\.\d+)?[eE][\-\+]?\d+)"
            "|" + intre + r"(?:\.\d+)"
            "|" + "(?:\.\d+)(?:[eE][\-\+]?\d+)?"
        )
        pattern = "(?:" + pattern + ")"
        if self.config.bounded_numbers:
            pattern = B_LEFT + pattern
        return re.compile(pattern)

    @cached_property
    def ANY_NUMBER_REGEX(self):
        p = "(?:" + self.FLOAT_REGEX.pattern + \
            "|" + self.INTEGER_REGEX.pattern + ")"
        return re.compile(p)

    @cached_property
    def COMPLEX_NUMBER_REGEX(self):
        pattern = bound(fr"{self.ANY_NUMBER_REGEX.pattern}[ij]\b")
        return re.compile(pattern)

    @cached_property
    def BINARY_REGEX(self):
        return re.compile(B_LEFT + r"0[bB][01]+" + B_RIGHT)

    @cached_property
    def HEX_REGEX(self):
        return re.compile(B_LEFT + r"0[xX][0-9a-fA-F]+" + B_RIGHT)

    @cached_property
    def OCT_REGEX(self):
        return re.compile(B_LEFT + r"0[oO][0-7]+" + B_RIGHT)

    @cached_property
    def _all_ones(self):
        return tuple(
            map(
                str,
                self.ONES.values(),
            )
        ) + tuple(self.ONES.keys())

    # any Number followed by multiple 2.3 million 6 trillion
    @cached_property
    def NUMBER_FOLLOWED_BY_POWER_REGEX(self):
        pattern = r"(?P<number>{_any_number})\s*(?P<power>{_power_names}){b_right}".format(
            _any_number=self.ANY_NUMBER_REGEX.pattern,
            _power_names=self._multiples,
            b_right=B_RIGHT,
        )

        return regex.compile(pattern, regex.I | re.M | re.VERBOSE)

    @cached_property
    def SUFFIX_NAME_REGEX(self):
        suffix_names = join(self.SUFFIXES_BY_NAME.keys())
        return re.compile(bound(suffix_names), re.I)

    @cached_property
    def NUMBER_FOLLOWED_BY_SUFFIX_REGEX(self):
        # any Number followed by a multiple suffix
        _suffixes = join(self.SUFFIXES.keys())
        _suffixes_by_name = join(map(all_cases, self.SUFFIXES_BY_NAME.keys()))
        pattern = r"(?P<number>{_any_number})(?P<suffix>\s*(?:{_suffixes_by_name})|(?:{_suffixes}))\b".format(
            _any_number=self.ANY_NUMBER_REGEX.pattern,
            _suffixes=_suffixes,
            _suffixes_by_name=_suffixes_by_name,
        )
        return re.compile(pattern)

    @cached_property
    def INFORMALS_EXACT_REGEX(self):
        # infomals couple, pair, dozen...
        _informal = join(self.INFORMAL_EXACT.keys())
        _small = join(['1', '0', 'one', 'zero'])
        pattern = fr"(?:{_small})\s+(?:{_informal}){B_RIGHT}"
        return regex.compile(pattern, regex.I)

    @cached_property
    def INFORMALS_MULTIPLYABLE_REGEX(self):
        _informals_multiplyable = join(self.INFORMALS_MULTIPLYABLE.keys())
        pattern = r"(?:{_any_number})\s+(?:{_informals_multiplyable})".format(
            _any_number=self.ANY_NUMBER_REGEX.pattern,
            _informals_multiplyable=_informals_multiplyable,
        )
        pattern = bound(pattern)
        return re.compile(pattern, re.I | re.M)

    @cached_property
    def ORDINAL_NUMERAL_REGEX(self):
        _ordinal_suffixes = Whitelist(self.ORDINAL_SUFFIXES).pattern()
        pattern = r"(?P<number>{integer_regex})(?P<ordinal>{_ordinal_suffixes})".format(
            integer_regex=self.INTEGER_REGEX.pattern,
            _ordinal_suffixes=_ordinal_suffixes,
        )
        pattern = bound(pattern)
        return re.compile(pattern)

    @cached_property
    def FIRST_EXTRACTION_REGEXES(self):
        regexes = [
            self.NUMBER_FOLLOWED_BY_SUFFIX_REGEX,  # 0
            self.SUPERSCRIPT_ONES_REGEX,  # 1
            self.SUBSCRIPT_ONES_REGEX,
            self.SUPERSCRIPT_FRACTIONS_REGEX,  # 2
            self.HEX_REGEX,  # 3
            self.OCT_REGEX,  # 4
            self.BINARY_REGEX,  # 5
            self.ORDINAL_NUMERAL_REGEX,  # 6
            self.NUMBER_FOLLOWED_BY_POWER_REGEX,  # 7
            self.INFORMALS_MULTIPLYABLE_REGEX,  # 8
        ]
        if self.config.parse_complex:
            regexes.insert(6, self.COMPLEX_NUMBER_REGEX)
        return tuple(regexes)

    @cached_property
    def LAST_EXTRACTION_REGEXES(self):
        return (self.ANY_NUMBER_REGEX, )

    def get_suffix_value(self, suffix):
        mapping = dict(self.SUFFIXES)
        mapping.update(self.SUFFIXES_BY_NAME)
        return mapping.get(suffix)
