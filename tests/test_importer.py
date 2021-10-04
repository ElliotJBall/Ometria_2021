import os
import json
from app import importer, db
import unittest
from unittest import mock
from requests.exceptions import HTTPError


def capture_ometria_payload(json_payload):
    return json_payload


@mock.patch(
    "app.importer.ometria.OmetriaClient.post_contact_records",
    side_effect=capture_ometria_payload,
)
@mock.patch("app.importer.mailchimp.MailchimpClient.get_members_info")
class TestImporter(unittest.TestCase):
    def test_can_run_import_job_for_company_and_mailchimp_list_id(
        self, mock_mailchimp_membership_call, ometria_json_payload
    ):
        with open(
            os.path.join(os.getcwd(), "json_files", "mailchimp_membership_single.json")
        ) as json_f:
            mock_mailchimp_membership_call.return_value = json.load(json_f)

            importer.run_import()

            # Validate we received our Joe Bloggs user as a single entry in the list
            args = ometria_json_payload.call_args.args
            assert args is not None

            ometria_customer_record = args[0][0]
            self.assertEqual(ometria_customer_record["id"], "d973631199")
            self.assertEqual(ometria_customer_record["firstname"], "Joe")
            self.assertEqual(ometria_customer_record["lastname"], "Bloggs")
            self.assertEqual(ometria_customer_record["email"], "joebloggs@ometria.com")
            self.assertEqual(ometria_customer_record["status"], "subscribed")

    def test_running_import_job_updates_company_mailchimp_entry_last_success(
        self, mock_mailchimp_membership_call, ometria_json_payload
    ):
        with open(
            os.path.join(os.getcwd(), "json_files", "mailchimp_membership_single.json")
        ) as json_f:
            mock_mailchimp_membership_call.return_value = json.load(json_f)

            importer.run_import()

            self.assertIsNotNone(db.MOCK_COMPANY_MAILCHIMP_ENTRY.last_success)

    def test_mailchimp_client_throwing_error_correctly_reports_last_success_failure_times(
        self, mock_mailchimp_membership_call, ometria_json_payload
    ):
        mock_mailchimp_membership_call.side_effect = HTTPError(
            "Some error whilst calling Mailchimp API"
        )

        importer.run_import()

        self.assertIsNotNone(db.MOCK_COMPANY_MAILCHIMP_ENTRY.last_success)
        self.assertIsNotNone(db.MOCK_COMPANY_MAILCHIMP_ENTRY.last_failure)

    def test_ometria_client_throwing_error_correctly_reports_last_success_failure_time(
        self, mock_mailchimp_membership_call, ometria_json_payload
    ):
        ometria_json_payload.side_effect = HTTPError(
            "Some error whilst calling Ometria API"
        )

        importer.run_import()

        self.assertIsNotNone(db.MOCK_COMPANY_MAILCHIMP_ENTRY.last_success)
        self.assertIsNotNone(db.MOCK_COMPANY_MAILCHIMP_ENTRY.last_failure)

