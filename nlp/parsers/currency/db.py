import json
from typing import (
    List,
    Dict,
    ClassVar,
    Any,
    Iterator,
    Optional,
)

from tinydb import TinyDB, Query

from nlp.data import get_data_path
from nlp.parsers.currency import constants as C

CURRENCY_FILE = get_data_path("currency") / "currencies.json"
CURRENCY_DB_FILE = CURRENCY_FILE.parent / "currency_db.json"


def _convert_to_tinydb_format(data) -> List[Dict]:
    temp = []
    for _, value in data.items():
        temp.append(value)
    return temp


def _read_db(update: bool = True) -> TinyDB:
    if CURRENCY_DB_FILE.exists() and not update:
        return TinyDB(CURRENCY_DB_FILE)
    if CURRENCY_DB_FILE.exists():
        CURRENCY_DB_FILE.unlink()
    fp = CURRENCY_FILE.open()
    data = _convert_to_tinydb_format(json.load(fp))
    for d in data:
        for currency_alias in C.CURRENCY_ALIASES:
            currency_alias = currency_alias.copy()
            demonym = currency_alias.pop(C.DEMONYM)
            other = d[C.DEMONYM]
            if other == demonym:
                d["alias"] = currency_alias
                break
    db = TinyDB(CURRENCY_DB_FILE)
    db.insert_multiple(data)
    return db


_UPDATE = True


class Queries:
    NAME = Query().name
    SYMBOL = Query().symbol
    SYMBOL_NATIVE = Query().symbol_native
    MAJOR_PLURAL = Query().majorPlural
    MAJOR_SINGLE = Query().majorSingle
    MINOR_PLURAL = Query().minorPlural
    MINOR_SINGLE = Query().minorSingle
    ALIAS_MAJOR_PLURAL = Query().alias.majorPlural
    ALIAS_MAJOR_SINGLE = Query().alias.majorSingle
    ALIAS_MINOR_PLURAL = Query().alias.minorPlural
    ALIAS_MINOR_SINGLE = Query().alias.minorSingle


class CurrencyDB:

    __db: ClassVar[TinyDB] = _read_db(_UPDATE)

    @classmethod
    def search(cls, query: Query) -> Any:
        results = cls.__db.search(query)
        return results

    @classmethod
    def all_entries(cls, entry: Optional[str] = None, alias: bool = False) -> Optional[Iterator[Any]]:
        if entry is None and not alias:
            yield from cls.__db.all()
            return
        for value in cls.__db.all():
            if alias:
                value = value.get(C.ALIAS)
                if value is None:
                    continue
            if entry is not None:
                yield value[entry]
            else:
                yield value

    @classmethod
    def get_db(cls) -> TinyDB:
        return cls.__db
