import json
from pathlib import Path
from typing import Union


def load_jsondata(file_path: Union[str, Path]) -> dict:
    with open(file_path, "r") as f:
        return json.load(f)
