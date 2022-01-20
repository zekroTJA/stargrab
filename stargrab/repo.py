from os import path
import subprocess
from github import Repository


def mirror(root_dir: str, repo: Repository):
    repo_dir = path.join(root_dir, repo.owner_login, repo.name)
    if path.exists(repo_dir):
        _git(f"-C {repo_dir} fetch --all")
    else:
        _git(f"clone --bare {repo.url} {repo_dir}")


def _git(cmd: str):
    res = subprocess.run(f"git {cmd}".split())
    if res.returncode != 0:
        raise Exception(
            res.stderr or res.stdout or f"unknown error: {res.returncode}")
    return res.stdout
