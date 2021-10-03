from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .config import (
    MAILCHIMP_BASE_URL,
    MAILCHIMP_LIST_ID,
    MAILCHIMP_API_KEY,
    OMETRIA_API_KEY,
)


# Pretend these are some DB models from our interview, Company - (One to many) -> Mailchimp listings
# I'm cheating here and only setting it up as a one to one mapping
@dataclass
class CompanyMailchimpEntry:
    id: int
    company_id: int
    mailchimp_list_id: str
    last_success: datetime = None
    last_failure: datetime = None


@dataclass
class Company:
    id: int
    name: str
    mailchimp_base_url: str
    mailchimp_api_key: str
    ometria_api_key: str
    # This would be a list but for simplicity I'll just set it up as one to one
    mailchimp_entry: Optional[CompanyMailchimpEntry]


MOCK_COMPANY_MAILCHIMP_ENTRY = CompanyMailchimpEntry(1, 1, MAILCHIMP_LIST_ID)
MOCK_COMPANY = Company(
    1,
    "ACME",
    MAILCHIMP_BASE_URL,
    MAILCHIMP_API_KEY,
    OMETRIA_API_KEY,
    MOCK_COMPANY_MAILCHIMP_ENTRY,
)

COMPANIES = [MOCK_COMPANY]


def get_company_by_id(company_id: int) -> Optional[Company]:
    return MOCK_COMPANY


def get_company_mailchimp_entry(
    company_id: int, mailchimp_list_id: int
) -> Optional[CompanyMailchimpEntry]:
    return MOCK_COMPANY_MAILCHIMP_ENTRY


def save_company(company: Company) -> Company:
    global COMPANIES
    COMPANIES = [company]
    return company
