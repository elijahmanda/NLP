import json

from nlp.data import get_data_path
from nlp.utils.timer import timer

WORLD_HOLIDAYS_FILE = get_data_path("event/world_holidays.json")


@timer()
def generate_list():
    with WORLD_HOLIDAYS_FILE.open(encoding="utf-8") as f:
        all_holidays_by_country = json.load(f)
    all_holidays = set()
    for _, holidays in all_holidays_by_country.items():
        all_holidays.update(holidays.keys())
    return list(all_holidays)
