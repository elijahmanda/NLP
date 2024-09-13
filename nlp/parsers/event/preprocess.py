# pylint:disable=E1101
import json
import pickle

from nlp.constants import EVENT
from nlp.data import get_data_path
from nlp.utils.regex import preprocess_names_to_patterns
from nlp.parsers.event.generate_holidays_list import generate_list

from nlp.utils.timer import timer  # Performance test

PATTERNS_FILE = get_data_path("event/preprocessed_patterns.json")
PICKLE_PATTERNS_FILE = get_data_path("event/preprocessed_patterns.pkl")


data_noise = {']', '[', ';', '&', "'", ' ', '.', '/', '-', '*', '(', ')'}
SPLITS = ";/"


@timer()
def save_preprocessed_patterns():
    names = generate_list()
    preprocessed_patterns = preprocess_names_to_patterns(names)
    with PATTERNS_FILE.open(mode="w", encoding="utf-8") as f:
        json.dump(preprocessed_patterns, f, indent=2, ensure_ascii=False)


@timer()
def dump_patterns():
    save_preprocessed_patterns()
    with PATTERNS_FILE.open(mode="r", encoding="utf-8") as f:
        names = json.load(f)
    patterns = list(zip(map(lambda n: n, names), [EVENT] * len(names)))
    with PICKLE_PATTERNS_FILE.open(mode="wb") as f:
        pickle.dump(patterns, f, protocol=pickle.HIGHEST_PROTOCOL)
    return patterns


if __name__ == "__main__":
    import pprint

    _names = generate_list()
    preprocessed = preprocess_names_to_patterns(_names)
    pprint.pprint(preprocessed)
    print("Total patterns:", len(preprocessed))

    if input("Save preprocessed patterns?: ").strip().lower() in ("y", "yes"):
        print("Saving patterns ...")
        dump_patterns()
        print("Saved patterns!")
