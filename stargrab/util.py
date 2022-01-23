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


def _fullmatch(
    patterns: List[Pattern],
    repo: Repository,
) -> bool:
    fqn = repo.fqn()
    for p in patterns:
        if p.fullmatch(fqn):
            return True
    return False
