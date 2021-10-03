from typing import List, Dict, Any

from .config import OMETRIA_API_URL, OMETRIA_API_KEY


class OmetriaClient:
    def __init__(self) -> None:
        self.url = OMETRIA_API_URL
        self.api_key = OMETRIA_API_KEY

    def post_contact_records(self, contact_records: List[Dict[str, Any]]):
        pass