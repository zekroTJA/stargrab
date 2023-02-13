from os import path, environ
from types import FunctionType
from typing import Dict, List
import json
import yaml
from pathlib import Path


_DEF_CFG = {
    "github_token": "",
    "user": "",
    "target": "repositories",
    "ignore": "",
    "depth": "",
    "max_size": ""
}


def parse() -> Dict:
    cfg = _DEF_CFG
    _parse_config_files([
        path.join("/etc/stargrab/config"),
        path.join(Path.home(), ".stargrab/config"),
        "./config",
    ], cfg)
    _parse_env("SG", cfg)
    return cfg


def _parse_env(prefix: str, target: Dict):
    for k in target.keys():
        v = environ.get(f"{prefix}_{k}".upper())
        if v:
            target[k] = v


def _parse_config_files(pathes: List[str], target: Dict):
    for p in pathes:
        _merge(_parse_yaml(p+".yml"), target)
        _merge(_parse_yaml(p+".yaml"), target)
        _merge(_parse_json(p+".json"), target)


def _parse_json(path: str) -> Dict:
    return _parse_file(json.load, path)


def _parse_yaml(path: str) -> Dict:
    return _parse_file(lambda p: yaml.load(p, Loader=yaml.FullLoader), path)


def _parse_file(parser: FunctionType, path: str) -> Dict:
    try:
        with open(path) as f:
            return parser(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        raise e


def _merge(source: Dict, target: Dict) -> Dict:
    for k in target.keys():
        if source.get(k):
            target[k] = source[k]
