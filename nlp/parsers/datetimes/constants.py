from typing import List, Dict, Set


class Attributes:
    # Vocab fields
    TAG = "tag"
    CATEGORY = "category"
    FEATURES = "features"

    # Time
    TIME = "time"
    DATE = "date"
    TIMEZONE = "timezone"
    TIME_PERIOD = "time_period"

    # Tags
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    ARTICLE = "article"
    MONTH = "month"
    TIME_UNIT = "time_unit"
    WEEKDAY = "weekday"
    NOUN = "noun"
    PREPOSITION = "preposition"
    CONJUNCTION = "conjunction"
    SEPERATOR = "seperator"
    DETERMINER = "determiner"

    # Categories
    PART_OF_DAY = "part_of_day"
    RELATIONSHIP = "relationship"
    POINTER = "pointer"
    MODIFIER = "modifier"
    MONTH_NAME = "month_name"
    WEEKDAY_NAME = "weekday_name"
    DAY_ALIAS = "day_alias"
    ARTICLE = "article"
    TIME_SPAN = "time_span"

    # Features
    SINGULAR = "singular"
    PLURAL = "plural"
    FULL = "full"
    SHORT = "short"
    ALIAS = "alias"
    START_TIME_SPAN = "start_time_span"
    END_TIME_SPAN = "end_time_span"


MONTHS: Dict[str, int] = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}

MONTH_ALIAS: Dict[str, str] = {
    "jan": "january",
    "feb": "february",
    "mar": "march",
    "apr": "april",
    "jun": "june",
    "jul": "july",
    "aug": "august",
    "sept": "september",
    "sep": "september",
    "oct": "october",
    "nov": "november",
    "dec": "december",
}

WEEKDAYS: Dict[str, int] = {
    "sunday": 1,
    "monday": 2,
    "tuesday": 3,
    "wednesday": 4,
    "thursday": 5,
    "friday": 6,
    "saturday": 7,
}

WEEKDAY_ALIAS: Dict[str, str] = {
    "sun": "sunday",
    "mon": "monday",
    "tues": "tuesday",
    "tue": "tuesday",
    "wed": "wednesday",
    "thurs": "thursday",
    "thur": "thursday",
    "fri": "friday",
    "sat": "saturday",
}

TIMEUNITS_SINGULAR: List[str] = [
    "nanosecond",
    "microsecond",
    "millisecond",
    "second",
    "minute",
    "hour",
    "day",
    "week",
    "month",
    "year",
    "decade",
    "century",
    "millenium",
]
TIMEUNITS_PLURAL: List[str] = [
    "nanoseconds",
    "microseconds",
    "milliseconds",
    "seconds",
    "minutes",
    "hours",
    "days",
    "weeks",
    "months",
    "years",
    "decades",
    "centuries",
    "millennia",
]

TIMEUNITS_ALIAS: Dict[str, List[str]] = {
    "ns": ["nanosecond", "nanoseconds"],
    f"{chr(181)}s": ["microsecond", "microseconds"],
    f"{chr(956)}s": ["microsecond", "microseconds"],
    "microsec": ["microsecond"],
    "microsecs": ["microsecond", "microseconds"],
    "ms": ["millisecond", "milliseconds"],
    "s": ["second", "seconds"],
    "sec": ["second"],
    "secs": ["second", "seconds"],
    "m": ["minute"],
    "min": ["minute"],
    "mins": ["minutes"],
    "h": ["hour"],
    "hr": ["hour"],
    "hrs": ["hours"],
    "d": ["day"],
    "dy": ["day"],
    "dys": ["days"],
    "wk": ["week"],
    "wks": ["weeks"],
    "mon": ["month"],
    "y": ["year"],
    "yr": ["year"],
    "yrs": ["years"],
}

TIME_MODIFIER_WORDS: List[str] = [
    "from",
    "in",
    "of",
    "on",
    "past",
    "after",
    "at",
    "before",
    "by",
    "up coming",
    "coming",
    "ago",
    "last",
    "until",
    "untill",
    "till",
    "to",
    "this",
    "end of",
    "previous",
    "next",
    "following",
]

OTHER_WORDS: List[str] = [
    "an",
    "the",
    "and",
]

TIME_WORDS: List[str] = [
    "noon",
    "afternoon",
    "morning",
    "midmorning",
    "night",
    "midnight",
    "midday",
    "tomorrow",
    "yesterday",
    "today",
    "weekend",
    "evening",
    "everyday",
    "annual",
    "autumn",
    "anytime",
    "autumnal equinox",
    "bedtime",
    "ante meridian",
    "bicentennial",
    "biennial",
    "calendar year",
    "daylight",
    "daylight savings time",
    "days of the week",
    "daytime",
    "early",
    "eon",
    "epoch",
    "equinox",
    "fallfiscal year",
    "fortnight",
    "future",
    "galactic year",
    "geologic time",
    "high noon",
    "late",
    "later",
    "leap second",
    "leap year",
    "lunar month",
    "meridian",
    "midafternoon",
    "nighttime",
    "now",
    "o'clock",
    "per annum",
    "per diem",
    "period",
    "post meridian",
]


TIMEZONE_ABBREVIATIONS: List[str] = [
    "ACDT",
    "ACST",
    "ACT",
    "ACWDT",
    "ACWST",
    "ADDT",
    "ADMT",
    "ADT",
    "AEDT",
    "AEST",
    "AFT",
    "AHDT",
    "AHST",
    "AKDT",
    "AKST",
    "AKTST",
    "AKTT",
    "ALMST",
    "ALMT",
    "AMST",
    "AMT",
    "ANAST",
    "ANAT",
    "ANT",
    "APT",
    "AQTST",
    "AQTT",
    "ARST",
    "ART",
    "ASHST",
    "ASHT",
    "AST",
    "AWDT",
    "AWST",
    "AWT",
    "AZOMT",
    "AZOST",
    "AZOT",
    "AZST",
    "AZT",
    "BAKST",
    "BAKT",
    "BDST",
    "BDT",
    "BEAT",
    "BEAUT",
    "BIOT",
    "BMT",
    "BNT",
    "BORT",
    "BOST",
    "BOT",
    "BRST",
    "BRT",
    "BST",
    "BTT",
    "BURT",
    "CANT",
    "CAPT",
    "CAST",
    "CAT",
    "CAWT",
    "CCT",
    "CDDT",
    "CDT",
    "CEDT",
    "CEMT",
    "CEST",
    "CET",
    "CGST",
    "CGT",
    "CHADT",
    "CHAST",
    "CHDT",
    "CHOST",
    "CHOT",
    "CIST",
    "CKHST",
    "CKT",
    "CLST",
    "CLT",
    "CMT",
    "COST",
    "COT",
    "CPT",
    "CST",
    "CUT",
    "CVST",
    "CVT",
    "CWT",
    "CXT",
    "ChST",
    "DACT",
    "DAVT",
    "DDUT",
    "DFT",
    "DMT",
    "DUSST",
    "DUST",
    "EASST",
    "EAST",
    "EAT",
    "ECT",
    "EDDT",
    "EDT",
    "EEDT",
    "EEST",
    "EET",
    "EGST",
    "EGT",
    "EHDT",
    "EMT",
    "EPT",
    "EST",
    "ET",
    "EWT",
    "FET",
    "FFMT",
    "FJST",
    "FJT",
    "FKST",
    "FKT",
    "FMT",
    "FNST",
    "FNT",
    "FORT",
    "FRUST",
    "FRUT",
    "GALT",
    "GAMT",
    "GBGT",
    "GEST",
    "GET",
    "GFT",
    "GHST",
    "GILT",
    "GIT",
    "GMT",
    "GST",
    "GYT",
    "HAA",
    "HAC",
    "HADT",
    "HAE",
    "HAP",
    "HAR",
    "HAST",
    "HAT",
    "HAY",
    "HDT",
    "HKST",
    "HKT",
    "HLV",
    "HMT",
    "HNA",
    "HNC",
    "HNE",
    "HNP",
    "HNR",
    "HNT",
    "HNY",
    "HOVST",
    "HOVT",
    "HST",
    "ICT",
    "IDDT",
    "IDT",
    "IHST",
    "IMT",
    "IOT",
    "IRDT",
    "IRKST",
    "IRKT",
    "IRST",
    "ISST",
    "IST",
    "JAVT",
    "JCST",
    "JDT",
    "JMT",
    "JST",
    "JWST",
    "KART",
    "KDT",
    "KGST",
    "KGT",
    "KIZST",
    "KIZT",
    "KMT",
    "KOST",
    "KRAST",
    "KRAT",
    "KST",
    "KUYST",
    "KUYT",
    "KWAT",
    "LHDT",
    "LHST",
    "LINT",
    "LKT",
    "LMT",
    "LMT",
    "LMT",
    "LMT",
    "LRT",
    "LST",
    "MADMT",
    "MADST",
    "MADT",
    "MAGST",
    "MAGT",
    "MALST",
    "MALT",
    "MART",
    "MAWT",
    "MDDT",
    "MDST",
    "MDT",
    "MEST",
    "MET",
    "MHT",
    "MIST",
    "MIT",
    "MMT",
    "MOST",
    "MOT",
    "MPT",
    "MSD",
    "MSK",
    "MSM",
    "MST",
    "MUST",
    "MUT",
    "MVT",
    "MWT",
    "MYT",
    "NCST",
    "NCT",
    "NDDT",
    "NDT",
    "NEGT",
    "NEST",
    "NET",
    "NFT",
    "NMT",
    "NOVST",
    "NOVT",
    "NPT",
    "NRT",
    "NST",
    "NT",
    "NUT",
    "NWT",
    "NZDT",
    "NZMT",
    "NZST",
    "OMSST",
    "OMST",
    "ORAST",
    "ORAT",
    "PDDT",
    "PDT",
    "PEST",
    "PET",
    "PETST",
    "PETT",
    "PGT",
    "PHOT",
    "PHST",
    "PHT",
    "PKST",
    "PKT",
    "PLMT",
    "PMDT",
    "PMMT",
    "PMST",
    "PMT",
    "PNT",
    "PONT",
    "PPMT",
    "PPT",
    "PST",
    "PT",
    "PWT",
    "PYST",
    "PYT",
    "QMT",
    "QYZST",
    "QYZT",
    "RET",
    "RMT",
    "ROTT",
    "SAKST",
    "SAKT",
    "SAMT",
    "SAST",
    "SBT",
    "SCT",
    "SDMT",
    "SDT",
    "SET",
    "SGT",
    "SHEST",
    "SHET",
    "SJMT",
    "SLT",
    "SMT",
    "SRET",
    "SRT",
    "SST",
    "STAT",
    "SVEST",
    "SVET",
    "SWAT",
    "SYOT",
    "TAHT",
    "TASST",
    "TAST",
    "TBIST",
    "TBIT",
    "TBMT",
    "TFT",
    "THA",
    "TJT",
    "TKT",
    "TLT",
    "TMT",
    "TOST",
    "TOT",
    "TRST",
    "TRT",
    "TSAT",
    "TVT",
    "ULAST",
    "ULAT",
    "URAST",
    "URAT",
    "UTC",
    "UYHST",
    "UYST",
    "UYT",
    "UZST",
    "UZT",
    "VET",
    "VLAST",
    "VLAT",
    "VOLST",
    "VOLT",
    "VOST",
    "VUST",
    "VUT",
    "WARST",
    "WART",
    "WAST",
    "WAT",
    "WDT",
    "WEDT",
    "WEMT",
    "WEST",
    "WET",
    "WFT",
    "WGST",
    "WGT",
    "WIB",
    "WIT",
    "WITA",
    "WMT",
    "WSDT",
    "WSST",
    "WST",
    "WT",
    "XJT",
    "YAKST",
    "YAKT",
    "YAPT",
    "YDDT",
    "YDT",
    "YEKST",
    "YEKST",
    "YEKT",
    "YEKT",
    "YERST",
    "YERT",
    "YPT",
    "YST",
    "YWT",
    "zzz"
]
