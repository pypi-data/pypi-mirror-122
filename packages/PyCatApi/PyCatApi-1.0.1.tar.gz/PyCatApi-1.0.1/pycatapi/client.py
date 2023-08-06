import requests

from .cat import Cat

class Client:

    def __init__(self) -> None:
        self._session = requests.Session()

    @staticmethod
    def request(_session: requests.Session):
        r = _session.get("https://api.thecatapi.com/v1/images/search")
        json: list[dict] = r.json()
        return json[0]

    def get_cat(self) -> Cat:
        """Get a random cat pic UwU"""
        with self._session as ses:
            data = self.request(ses)
        return Cat(**data)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._session.close()
