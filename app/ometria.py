from typing import List, Dict, Any
import requests
import json

from .config import OMETRIA_API_URL


class OmetriaClient:
    def __init__(self, api_key) -> None:
        self.url = OMETRIA_API_URL
        self.api_key = api_key

    def post_contact_records(
        self, contact_records: List[Dict[str, Any]]
    ) -> requests.Response:
        # FIXME: We're going to need to email Ometria their API appears to be unavailable
        #  (03/10/2021) ~20:45 Was when I started trying to use it
        pass
        # headers = {"Authorization": self.api_key}
        # data = json.dumps(contact_records)
        #
        # resp = requests.post(url=self.url, headers=headers, data=data)
        # resp.raise_for_status()
        #
        # return resp.json()
