import json
from typing import Dict, List, Tuple
import requests


_GH_GQL_ENDPOINT = "https://api.github.com/graphql"


class Repository:
    def __init__(self, v: Dict):
        self.cursor = v.get("cursor")
        self.owner_login = v.get("node").get('owner').get('login')
        self.name = v.get("node").get('name')
        self.url = v.get("node").get('url')


class Client:
    def __init__(self, token: str):
        if not token:
            raise Exception("GitHub Token must be specified")
        self._token = token

    def get_starred_repositories(self,
                                 user_override=None) -> List[Repository]:
        repos = []
        after = ""
        while True:
            (total, r) = self._get_starred_repositories_paged(
                user_override, after)
            repos += r
            if len(repos) >= total:
                break
            after = r[-1].cursor
        return repos

    def _get_starred_repositories_paged(self,
                                        user_override: str,
                                        after: str
                                        ) -> Tuple[int, List[Repository]]:
        user = f'user(login:"{user_override}")' if user_override else "viewer"
        query = f"""
            query {{
                {user} {{
                    starredRepositories(after:"{after}") {{
                        totalCount
                        edges {{
                            cursor
                            node {{
                                owner {{
                                    login
                                }},
                                name,
                                url
                            }}
                        }}
                    }}
                }}
            }}
        """
        res = self._request(query)
        starred = res.get("data") \
                     .get("user" if user_override else "viewer") \
                     .get("starredRepositories")
        total = starred.get("totalCount")
        repos = starred.get("edges")
        return (total, [Repository(r) for r in repos])

    def _request(self, query: str):
        data = json.dumps({
            "query": query
        })
        res = requests.post(_GH_GQL_ENDPOINT, data, headers={
            "Authorization": f"bearer {self._token}"
        })
        if not res.ok:
            raise Exception(f"Request failed: {res.status_code}")
        return res.json()
