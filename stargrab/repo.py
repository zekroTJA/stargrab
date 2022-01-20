import json
from os import path
import subprocess
from typing import List
from github import Repository


def mirror(root_dir: str, repo: Repository):
    repo_dir = path.join(root_dir, repo.owner_login, repo.name)
    if path.exists(repo_dir):
        _git(f"-C {repo_dir} fetch --all")
    else:
        _git(f"clone --bare {repo.url} {repo_dir}")


def store_meta(root_dir: str, repos: List[Repository]):
    curr = {}
    try:
        with open(path.join(root_dir, "meta.json"), mode='r') as f:
            for r in json.load(f):
                curr[f"{r.get('owner_login')}/{r.get('name')}"] = r
    except Exception as e:
        print("error: ", e)
        pass
    with open(path.join(root_dir, "meta.json"), mode='w+') as f:
        for r in repos:
            curr[f"{r.owner_login}/{r.name}"] = r.map()
        json.dump(list(curr.values()), f, indent=2)


def _git(cmd: str):
    res = subprocess.run(f"git {cmd}".split())
    if res.returncode != 0:
        raise Exception(
            res.stderr or res.stdout or f"unknown error: {res.returncode}")
    return res.stdout
