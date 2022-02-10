import requests
import re
import sys
import pickle
import time


class Leakix:
    def __init__(self, login: str, password: str, scope: str = "leak"):
        self.login = login
        self.password = password
        self.scope = scope
        self.session = requests.session()
        self.csrf = None

    @property
    def _headers(self) -> dict:
        return {"Accept": "application/json"}

    @property
    def _get_csrf(self) -> str:
        r = self.session.get("https://leakix.net/auth/login")
        if r.status_code == 200:
            return re.findall(
                '\<input type="hidden" name="csrf_token" value="(.*)"\>', r.text
            )[0]
        return ""

    @property
    def cookies(self) -> bool:
        try:
            with open("cookies", "rb") as _:
                return pickle.load(_)
        except FileNotFoundError:
            return False

    def auth(self) -> bool:
        r = self.session.post(
            "https://leakix.net/auth/login",
            data={
                "inputUsername": self.login,
                "inputPassword": self.password,
                "csrf_token": self._get_csrf,
            },
        )
        if r.status_code == 200:
            with open("cookies", "wb") as _:
                pickle.dump(self.session.cookies, _)
                return True
        return False

    def check_auth(self) -> bool:
        if not self.cookies:
            self.auth()

        self.session.cookies.update(self.cookies)
        for cookie in self.cookies:
            if cookie.name == "LEAKIX_SESSION":
                if int(time.time()) > cookie.expires:
                    self.auth()

        return True

    def search_leaks(self, query: str) -> list:
        results = list()

        r = self.session.get(
            "https://leakix.net/search?scope={scope}&q={query}".format(
                query=query, scope=self.scope
            ),
            headers=self._headers,
        )
        if r.status_code != 200 or r.json() == None:
            return []

        for data in r.json():
            if data["ip"] == "":
                continue
            results.append(data)
        return results
