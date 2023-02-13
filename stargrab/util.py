from typing import Dict, List, Pattern
from repo import Repository
import re


def filter_ignore(
    cfg: Dict,
    repos: List[Repository]
) -> List[Repository]:
    patterns = cfg.get("ignore")
    if not patterns:
        return repos
    if type(patterns) is str:
        patterns = [patterns]
    patterns = [re.compile(p) for p in patterns]
    return [r for r in repos
            if not _fullmatch(patterns, r)]


def filter_size(
    cfg: Dict,
    repos: List[Repository]
) -> List[Repository]:
    max_size = parse_size(str(cfg.get("max_size")))
    if max_size <= 0:
        return repos
    return [r for r in repos if r.size * 1024 < max_size]


def parse_size(v: str) -> int:
    if len(v) == 0:
        return 0
    v = v.lower()
    rx = r'([\d\.]+)([kmgtp]?i?b?)?'
    res = re.search(rx, v)
    (n, suffix) = res.groups()
    n = float(n)
    if len(suffix) == 0 or suffix[0] == 'b':
        pass
    elif suffix[0] == 'k':
        n *= 1024
    elif suffix[0] == 'm':
        n *= 1024 * 1024
    elif suffix[0] == 'g':
        n *= 1024 * 1024 * 1024
    elif suffix[0] == 't':
        n *= 1024 * 1024 * 1024 * 1024
    elif suffix[0] == 'p':
        n *= 1024 * 1024 * 1024 * 1024 * 1014
    else:
        raise Exception("invalid scale suffix")
    return int(n)


def _fullmatch(
    patterns: List[Pattern],
    repo: Repository,
) -> bool:
    fqn = repo.fqn()
    for p in patterns:
        if p.fullmatch(fqn):
            return True
    return False
