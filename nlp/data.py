from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_PATH = HERE / "data"


def get_data_path(path: str) -> Path:
    return DATA_PATH / path
