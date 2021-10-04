from datetime import datetime
from typing import Dict, Any

import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.util.retry import Retry


class PageRequest:
    def __init__(self, offset: int = 0, count: int = 500) -> None:
        self.offset = offset
        self.count = count

    def __repr__(self) -> str:
        return f"PageRequest(offset={self.offset}, count={self.count})"

    def next_page(self):
        """Return a new page request object to fetch the next page.
        Uses the limit used to originally construct the page request"""
        return PageRequest(self.offset + self.count, self.count)


class MailchimpClient:
    # Limit the mailchimp response to only the fields we need to fetch, minimise response size, increase response time
    # Can you not request specific merge fields? I tried members.merge_fields.FNAME but that returns whole merge_fields
    REQUIRED_FIELDS = (
        "members.email_address",
        "members.unique_email_id",
        "members.status",
        "members.merge_fields",
        "total_items",
    )

    def __init__(self, base_url: str, mailchimp_api_key: str) -> None:
        self.base_url = base_url
        self.auth = HTTPBasicAuth("elliot-ball-ometria-2021", mailchimp_api_key)

        # Some attempt to add in the retry logic we discussed in the previous interview
        retry_strategy = Retry(
            backoff_factor=2,
            total=3,
            status_forcelist=[413, 429, 500, 503],
            # This gives deprecation warnings but I cannot see the alternative parameter declared...
            method_whitelist=["GET"],
        )
        adaptor = HTTPAdapter(max_retries=retry_strategy)
        self.session = requests.session()
        self.session.mount("https://", adaptor)

    def get_members_info(
        self,
        list_id: str,
        since_last_changed: datetime = None,
        pagination: PageRequest = PageRequest(),
    ) -> Dict[Any, Any]:
        """Queries the Mailchimp /lists/{list_id}/members API, returning the JSON
        response body

        :param list_id: the mailchimp list id
        :param since_last_changed: used to restrict the result set to
        only include users whose information has changed after the given value
        :param pagination: the pagination
        :return: Mailchimp JSON body response
        """
        params = {"offset": pagination.offset, "count": pagination.count}
        params.update({"fields": ",".join(self.REQUIRED_FIELDS)})

        if since_last_changed:
            params["since_last_changed"] = since_last_changed.isoformat()

        # Should a sort be applied? Oldest users first?

        url = f"{self.base_url}/lists/{list_id}/members"

        resp = self.session.get(url=url, params=params, auth=self.auth)
        resp.raise_for_status()

        return resp.json()
