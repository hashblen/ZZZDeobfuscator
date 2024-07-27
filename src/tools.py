import json
import pathlib

BASE_OBF_PATH = pathlib.Path("TvGameData/FileCfg")
BASE_DEOBF_PATH = pathlib.Path("DeobfData/FileCfg")
BASE_DEOBF_PATH.mkdir(parents=True, exist_ok=True)
BASE_DIR_PATH = pathlib.Path("src/files")


def read_obfuscated(filename: str):
    with open(BASE_OBF_PATH / filename, 'r') as file:
        data = json.load(file)
    return data


def read_example(filename: str):
    with open(BASE_DIR_PATH / filename, 'r') as file:
        data = json.load(file)
    return data


def write_deobfuscated(data: dict, filename: str):
    with open(BASE_DEOBF_PATH / filename, 'w') as file:
        json.dump(data, file, indent=2)
