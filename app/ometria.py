from typing import List, Dict, Any
import requests
import json

from app import config


class OmetriaClient:
    def __init__(self, api_key) -> None:
        self.url = config.OMETRIA_API_URL
        self.api_key = api_key

    def post_contact_records(
        self, contact_records: List[Dict[str, Any]]
    ) -> requests.Response:
        """Post a list of Ometria contact records to the configured Ometria API

        :param contact_records: the list of Ometria customer records
        :return: JSON response from the Ometria API
        """
        headers = {"Authorization": self.api_key, "Content-Type": "application/json"}
        data = json.dumps(contact_records)

        resp = requests.post(url=self.url, headers=headers, data=data)
        resp.raise_for_status()

        return resp.json()
