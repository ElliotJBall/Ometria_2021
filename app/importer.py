import logging
import time
from datetime import datetime
from .db import get_company_mailchimp_entry


from .config import MAILCHIMP_LIST_ID

logger = logging.getLogger(__name__)


def run_import() -> None:
    """Runs the import/sync job for a given companies mailchimp listing id"""
    job_start_time = datetime.now()

    # Pretend we've extracted the company id and mailchimp list id from the message
    company_id = 1
    mailchimp_list_id = MAILCHIMP_LIST_ID

    logger.info(
        f"Starting import/sync job for company id: [{company_id}] and mailchimp list id: [{mailchimp_list_id}]"
    )

    company_mailchimp_entry = get_company_mailchimp_entry(company_id, MAILCHIMP_LIST_ID)




    elapsed = datetime.now() - job_start_time

    logger.info(
        f"Finished import/sync job for company id: [{company_id}] "
        f"and mailchimp list id: [{mailchimp_list_id}]. Total time taken: [{elapsed}]"
    )
