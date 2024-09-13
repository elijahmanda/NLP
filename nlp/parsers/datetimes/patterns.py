import itertools

from nlp.utils.regex import (
    join,
    bound,
    retrie,
    no_digits_bound,
    B_LEFT_NO_DIGIT,
    B_RIGHT_NO_DIGIT,
    B_LEFT_NO_LETTER,
    B_RIGHT_NO_LETTER,
    B_LEFT,
    B_RIGHT,
)

from nlp.parsers.datetimes.constants import (
    TIMEZONE_ABBREVIATIONS,
    MONTHS,
    MONTH_ALIAS,
    WEEKDAYS,
    WEEKDAY_ALIAS,
    TIMEUNITS_SINGULAR,
    TIMEUNITS_PLURAL,
    TIMEUNITS_ALIAS,
    TIME_MODIFIER_WORDS,
    TIME_WORDS,
    OTHER_WORDS,
)

YYYY = r"(?:[12]\d{3}|[1-9]\d)"
DD = r"(?:(?:1\d|2[0-9]|3[01]|0?[1-9])|(?:[23]1|0?1)|(?:22|0?2))"
MM = r"(?:1[12]|0?[1-9])"
YY = r"(?:[1-9]\d|0?[1-9])"
MS = r"(?:\d+)"
HH = r"(?:1\d|2[123]|0?[1-9])"
HH_12 = r"(?:1[0-2]|0?[1-9])"
MIN = r"(?:[1-5]\d|0?\d)"
SEC = MIN

MONTH_PATTERN = join(MONTHS)

MONTH_ALIAS_PATTERN = join(MONTH_ALIAS)

WEEKDAY_PATTERN = bound(join(WEEKDAYS))

WEEKDAY_ALIAS_PATTERN = bound(join(WEEKDAY_ALIAS))

TIMEUNITS_SINGULAR_PATTERN = bound(join(TIMEUNITS_SINGULAR))

TIMEUNITS_PLURAL_PATTERN = bound(join(TIMEUNITS_PLURAL))

TIMEUNITS_ALIAS_PATTERN = bound(join(TIMEUNITS_ALIAS))

TIME_MODIFIER_WORD_PATTERN = bound(join(TIME_MODIFIER_WORDS))

TIME_WORD_PATTERN = bound(join(TIME_WORDS))

OTHER_WORD_PATTERN = bound(join(OTHER_WORDS))

# explicit north american timezones that get replaced
NA_TIMEZONES_PATTERN = "(?:pacific|eastern|mountain|central)"
ALL_TIMEZONES_PATTERN = bound(
    join([
        *TIMEZONE_ABBREVIATIONS,
        NA_TIMEZONES_PATTERN,
    ]),
)

TIME_PERIOD_PATTERN = fr"{B_LEFT_NO_LETTER}(?:a\.m\.?|am|p\.m\.?|pm)\b"

TIME_PERIOD_PATTERN = bound(TIME_PERIOD_PATTERN)

ISO8601_PATTERN = r"""
(?P<years>-?(\:[1-9][0-9]*)?[0-9]{4})
\-
(?P<months>1[0-2]|0[1-9])
\-
(?P<days>3[01]|0[1-9]|[12][0-9])T
(?P<hours>2[0-3]|[01][0-9])
:
(?P<minutes>[0-5][0-9])
:
(?P<seconds>[0-5][0-9])
(?:[\.,]+(?P<microseconds>[0-9]+))?
(?P<offset>(?:Z|[+-](?:2[0-3]|[01][0-9])\:[0-5][0-9]))?
"""


DATETIME_PATTERNS = [
    # rfc3339
    # 2021-05-01T01:17:02.604456Z
    # 2017-11-25T22:34:50Z
    (fr"\b{YYYY}\-{MM}\-{DD}T{HH}:{MIN}:{SEC}(?:\.{MS})?Z\b", "rfc3339"),
    # rfc2822
    # Wed, 02 Jun 2021 06:31:39 GMT
    (fr"\b{MONTH_ALIAS_PATTERN}[,]\s*{DD}\s*{YYYY}\s*{HH}:{MIN}:{SEC}\s*{ALL_TIMEZONES_PATTERN}\b", "rfc2822"),
    (ISO8601_PATTERN, "iso8601"),
]
DATETIME_PATTERNS.sort(key=lambda x: len(x[0]), reverse=True)


def generate_permutations(patterns, separator):
    patterns = itertools.permutations(patterns)
    patterns = [separator.join(p) for p in patterns]
    return patterns


DATE_PATTERNS = [
    # Dates
    ###########
    # DD MM YYYY
    # 12-01-1990
    (fr"\b{DD}\-{MM}\-{YYYY}\b", "date-dd-mm-yyyy"),
    # 12/01/1990
    (fr"\b{DD}/{MM}/{YYYY}\b", "date-dd/mm/yyyy"),
    # 12.01.1990
    (fr"\b{DD}\.{MM}\.{YYYY}\b", "date-dd.mm.yyyy"),
    ###########
    # YYYY MM DD
    # 2019-11-29
    (fr"\b{YYYY}\-{MM}\-{DD}\n", "date-yyyy-mm-dd"),
    # 2019/11/29
    (fr"\b{YYYY}/{MM}/{DD}\b", "date-yyyy/mm/dd"),
    # 2019.11.29
    (fr"\b{YYYY}\.{MM}\.{DD}\b", "date-yyyy.mm.dd"),
    ###########
    # MM DD YYYY
    # 01-12-1990 # bloody ambiguous
    (fr"\b{MM}\-{DD}\-{YYYY}\b", "date-mm-dd-yyyy"),
    # 01/12/1990
    (fr"\b{MM}/{DD}/{YYYY}\b", "date-mm/dd/yyyy"),
    # 01.12.1990
    (fr"\b{MM}\.{DD}\.{YYYY}\b", "date-mm.dd.yyyy"),
    ###########
    # DD YYYY MM
    # 01-12-1990 # more bloody ambiguity 🤦🏾‍♂️
    (fr"\b{DD}\-{YYYY}\-{MM}\b", "date-dd-yyyy-mm"),
    # 01/12/1990
    (fr"\b{DD}/{YYYY}/{MM}\b", "date-dd/yyyy/mm"),
    # 01.12.1990
    (fr"\b{DD}\.{YYYY}\.{MM}\b", "date-dd.yyyy.mm"),
    ###########
    # YYYY DD MM
    # 2924-12-12 # bloody ambiguous
    (fr"\b{YYYY}\-{DD}\-{MM}\b", "date-yyyy-dd-mm"),
    # 2012/12/11
    (fr"\b{YYYY}/{DD}/{MM}\b", "date-yyyy/dd/mm"),
    # 2034.12.10
    (fr"\b{YYYY}\.{DD}\.{MM}\b", "date-yyyy.dd.mm"),
    ###########
    # MM DD YYYY
    # 12-12-12 # bloody ambiguous
    (fr"\b{MM}\-{DD}\-{YYYY}\b", "date-mm-dd-yyyy"),
    # 11/12/11
    (fr"\b{MM}/{DD}/{YYYY}\b", "mm/dd/yyyy"),
    # 04.12.10
    # (fr"\b{MM}\.{DD}\.{YYYY}\b", "mm.dd.yyyy"),
    ###########
    # YYYY MM DD
    # 2924-12-12 # bloody ambiguous
    (fr"\b{YYYY}\-{MM}\-{DD}\b", "date-yyyy--mm-dd"),
    # 2012/12/11
    (fr"\b{YYYY}/{MM}/{DD}\b", "date-yyyy/mm/dd"),
    # 2034.12.10
    (fr"\b{YYYY}\.{MM}\.{DD}\b", "date-yyyy.mm.dd"),
]
OTHER_DATE_PATTERNS = [

    ###########
    # Hyphen separated
    # 21-Feb-2024
    (fr"\b{DD}\-(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\-(?:{YYYY}|{YY})\b", "dd-month-yyyy"),
    # 21-2024-December
    (fr"\b{DD}\-(?:{YYYY}|{YY})\-(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\b", "dd-yyyy-month"),
    # Feb-21-2024
    (fr"\b(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\-{DD}\-(?:{YYYY}|{YY})\b", "month-dd-yyyy"),
    # Feb-2024-21
    (fr"\b(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\-(?:{YYYY}|{YY}\-{DD})\b", "month-dd-yyyy"),
    # 2024-21-January
    (fr"\b(?:{YYYY}|{YY})\-{DD}\-(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\b", "yyyy-dd-month"),
    # 2024-January-20
    (fr"\b(?:{YYYY}|{YY})\-(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\-{DD}\b", "yyyy-month-dd"),

    #########
    # Slash separated
    # 21/Feb/2024
    (fr"\b{DD}/(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})/(?:{YYYY}|{YY})\b", "dd/month/yyyy"),
    # 21/2024/December
    (fr"\b{DD}/(?:{YYYY}|{YY})/(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\b",
     "dd-l/yyyy/month"),
    # Feb/21/2024
    (fr"\b(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})/{DD}/(?:{YYYY}|{YY})\b", "month-dd-yyyy"),
    # Feb/2024/21
    (fr"\b(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})/(?:{YYYY}|{YY})/{DD}\b", "month/dd/yyyy"),
    # 2024/21/January
    (fr"\b(?:{YYYY}|{YY})/{DD}/(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\b", "yyyy/dd/month"),
    # 2024/January/20
    (fr"\b(?:{YYYY}|{YY})/(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})/{DD}\b", "yyyy/month/dd"),

    ##########
    # Full stop separated
    # 21.Feb.2024
    (fr"\b{DD}\.{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN}\.(?:{YYYY}|{YY})\b", "dd.month.yyyy"),
    # 21.2024.December
    (fr"\b{DD}\.(?:{YYYY}|{YY})\.(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\b", "dd.yyyy.month"),
    # Feb.21.2024
    (fr"\b(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\.{DD}\.(?:{YYYY}|{YY})\b", "month.dd.yyyy"),
    # Feb.2024.21
    (fr"\b(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\.(?:{YYYY}|{YY})\.{DD}\b", "month.dd.yyyy"),
    # 2024.21.January
    (fr"\b(?:{YYYY}|{YY})\.{DD}\.(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\b", "yyyy.dd.month"),
    # 2024.January.20
    (fr"\b(?:{YYYY}|{YY})\.(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\.{DD}\b", "yyyy.month.dd"),

    # September 17,? 2012
    (fr"\b(?:{MONTH_PATTERN})\s*{DD},?\s*(?:{YYYY}|{YY})\b", "month dd yyyy"),
    # oct 7, 1970
    # oct 7, 70
    # oct. 7, 1970
    # oct. 7, 70
    (fr"\b(?:{MONTH_ALIAS_PATTERN})[.]?\s*{DD}[,]?\s*{YYYY}|{YY}\b",
     "month dd yyyy"),
    # dd Mon yyyy
    # 7 oct 70
    # 7 oct 1970
    # 03 February 2013
    # 1 July 2013
    (fr"\b{DD}\s*(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\s*(?:{YYYY}|{YY})\b", "dd-mm-yyyy"),

    # Space separated
    # 21 Feb 2024
    (fr"\b{DD}\*(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\s*(?:{YYYY}|{YY})\b", "dd month yyyy"),
    # 21 2024 December
    (fr"\b{DD}\s*(?:{YYYY}|{YY})\s*(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\b", "dd yyyy month"),
    # Feb 21 2024
    (fr"\b(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\s*{DD}\s*(?:{YYYY}|{YY})\b", "month dd yyyy"),
    # Feb 2024 21
    (fr"\b(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\s*(?:{YYYY}|{YY})\s*{DD}\b", "month dd yyyy"),
    # 2024 21 January
    (fr"\b(?:{YYYY}|{YY})\s*{DD}\s*(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\b", "yyyy-dd-month"),
    # 2024 January 20
    (fr"\b(?:{YYYY}|{YY})\s*(?:{MONTH_PATTERN}|{MONTH_ALIAS_PATTERN})\s*{DD}\b", "yyyy-month-dd"),


]
DATETIME_PATTERNS.sort(key=lambda x: len(x[0]), reverse=True)

TIME_PATTERNS = [
    # 06:20:00
    (fr"\b{HH}:{MIN}:{SEC}\b",
     "hh:mm:ss",
     ),
    # 06:20:00AM
    (fr"\b{HH_12}:{MIN}:{SEC}\s*{TIME_PERIOD_PATTERN}\b",
     "hh:mm:ss p",
     ),
    # 06:20
    (fr"\b{HH}:{MIN}\b",
     "hh:mm",
     ),
    # 06:20p.m
    (fr"\b{HH_12}:{MIN}\s*{TIME_PERIOD_PATTERN}\b",
     "hh:mm p",
     ),
    # 06:20:00 AM UTC
    (fr"\b{HH_12}:{MIN}\s*{TIME_PERIOD_PATTERN}\s+{ALL_TIMEZONES_PATTERN}\b",
     "hh:mm zzz",
     ),
    # 06:20:00 UTC
    (fr"\b{HH}:{MIN}:{SEC}\s*{ALL_TIMEZONES_PATTERN}\b",
     "hh:mm:ss zzz",
     ),
    # 18:48:56.35272715 UTC
    (fr"\b{HH}:{MIN}:{SEC}\.{MS}\s*{ALL_TIMEZONES_PATTERN}\b",
     "hh:mm:ss.ms zzz",
     ),
    # 18:48:56.35272715 PM UTC
    (fr"\b{HH}:{MIN}:{SEC}\.{MS}\s*{TIME_PERIOD_PATTERN}\s+{ALL_TIMEZONES_PATTERN}\b",
     "hh:mm:ss.ms p zzz",
     ),
    # 13:13:44 +09:00
    # 18:31:59.257000000 +0000,
    (fr"\b{HH}:{MIN}(?:[:]{SEC}(?:\.{MS})?)?\s*[-+](?:\d\d(?:[:]?\d\d)?)\b",
     "hh:mm(:ss(.ms))",
     ),
    (fr"\b{HH}:{MIN}:{SEC}\.{MS}\s*[-+](?:\d\d(?:[:]\d\d)?)\b",
     "hh:mm:ss.ms +-zzzz",
     ),
    (fr"\b{HH}:{MIN}:{SEC}\.{MS}\s*[-+](?:\d\d(?:[:]\d\d)?)\b",
     "hh:mm:ss.ms +-zzzz",
     ),
]
TIME_PATTERNS.sort(key=lambda x: len(x[0]), reverse=True)


def test(patterns):
    import re
    for i, (pattern, name) in enumerate(patterns):
        print(i+1, name)
        print(pattern)
        re.compile(pattern, re.VERBOSE)


if __name__ == "__main__":
    test(DATE_PATTERNS)
