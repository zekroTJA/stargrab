import json
from typing import Dict, List
import requests


_GH_GQL_ENDPOINT = "https://api.github.com/graphql"


class Repository:
    def __init__(self, v: Dict):
        self.owner_login = v.get('owner').get('login')
        self.name = v.get('name')
        self.url = v.get('url')


class Client:
    def __init__(self, token: str):
        if not token:
            raise Exception("GitHub Token must be specified")
        self._token = token

    def get_starred_repositories(self,
                                 user_override=None) -> List[Repository]:
        user = f'user(login:"{user_override}")' if user_override else "viewer"
        query = f"""
            query {{
                {user} {{
                    starredRepositories {{
                        edges {{
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
        repos = res.get("data") \
                   .get("user" if user_override else "viewer") \
                   .get("starredRepositories") \
                   .get("edges")
        return [Repository(r.get("node")) for r in repos]

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
