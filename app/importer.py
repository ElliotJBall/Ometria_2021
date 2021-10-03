import logging
from datetime import datetime

from . import mailchimp, ometria, db, mapper

logger = logging.getLogger(__name__)


def run_import() -> None:
    """Runs the import/sync job for a given companies mailchimp listing id"""
    job_start_time = datetime.now()

    # Pretend we've extracted the company id/mailchimp list id from the message
    company = db.get_company(1)

    logger.info(
        f"Starting import/sync job for company id: [{company.id}] "
        f"and mailchimp list id: [{company.mailchimp_entry.mailchimp_list_id}]"
    )

    mailchimp_client = mailchimp.MailchimpClient(
        company.mailchimp_base_url, company.mailchimp_api_key
    )
    ometria_client = ometria.OmetriaClient(company.ometria_api_key)

    pages_remaining = True
    page_req = mailchimp.PageRequest()
    total_processed = 0

    try:
        while pages_remaining:
            logger.debug(
                f"Company id: [{company.id}], "
                f"mailchimp list id: [{company.mailchimp_entry.mailchimp_list_id}], "
                f"page request: [{page_req}], total processed: [{total_processed}]"
            )

            # Fetch the data from the mailchimp API
            mailchimp_resp = mailchimp_client.get_members_info(
                list_id=company.mailchimp_entry.mailchimp_list_id,
                since_last_changed=company.mailchimp_entry.last_success,
                pagination=page_req,
            )

            # Convert each mailchimp member into the Ometria contact record
            contact_records = mapper.convert(mailchimp_resp)
            total_processed += len(contact_records)

            # Post the data to the Ometria endpoint
            ometria_client.post_contact_records(contact_records)

            # Check if we need to continue to the next page
            pages_remaining = page_req.offset < mailchimp_resp["total_items"]
            page_req = page_req.next_page()

        # Update the company mailchimp entry, completion time etc.
        company.mailchimp_entry.last_success = job_start_time
        db.save(company)

        elapsed = datetime.now() - job_start_time

        logger.info(
            f"Finished import/sync job for company id: [{company.id}] "
            f"and mailchimp list id: [{company.mailchimp_entry.mailchimp_list_id}]. "
            f"Processed a total of: {total_processed} Mailchimp membership records. Total time taken: [{elapsed}]"
        )
    except Exception as err:
        logger.error(
            f"Failed to run import/sync job for company id: {company.id}"
            f"and mailchimp list id: [{company.mailchimp_entry.mailchimp_list_id}].",
            err,
        )

        company.mailchimp_entry.last_failure = job_start_time
        db.save(company)
