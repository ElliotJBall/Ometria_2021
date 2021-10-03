from datetime import datetime
from requests.auth import HTTPBasicAuth


class PageRequest:
    def __init__(self, offset: int, count: int) -> None:
        self.offset = offset
        self.count = count


class MailchimpClient:
    def __init__(self, base_url: str, mailchimp_api_key: str) -> None:
        self.base_url = base_url
        self.mailchimp_api_key = mailchimp_api_key

    def list_members_info(self, list_id: str, pagination: PageRequest = PageRequest(0, 500)):
        pass
