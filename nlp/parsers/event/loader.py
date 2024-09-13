# pylint:disable=E1101
import pickle
from functools import lru_cache
from nlp.data import get_data_path


patterns_file = get_data_path("event/preprocessed_patterns.pkl")


@lru_cache(maxsize=1)
def load_patterns():
    data = patterns_file.read_bytes()
    patterns = pickle.loads(data)
    return patterns
