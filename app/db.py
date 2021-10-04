from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app import config


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


MOCK_COMPANY_MAILCHIMP_ENTRY = CompanyMailchimpEntry(1, 1, config.MAILCHIMP_LIST_ID)
MOCK_COMPANY = Company(
    1,
    "ACME",
    config.MAILCHIMP_BASE_URL,
    config.MAILCHIMP_API_KEY,
    config.OMETRIA_API_KEY,
    MOCK_COMPANY_MAILCHIMP_ENTRY,
)

COMPANIES = [MOCK_COMPANY]


def get_company(company_id: int) -> Optional[Company]:
    return MOCK_COMPANY


def save(company: Company) -> Company:
    global COMPANIES
    COMPANIES = [company]
    return company
