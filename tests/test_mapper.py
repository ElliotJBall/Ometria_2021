import json
import os
import unittest
from app import mapper


class TestMapper(unittest.TestCase):
    def test_can_successfully_map_mailchimp_member_to_ometria_customer_record(self):
        with open(
            os.path.join(os.getcwd(), "json_files", "mailchimp_membership_single.json")
        ) as json_f:
            json_data = json.load(json_f)

            customer_records = mapper.convert(json_data)

            self.assertEqual(len(customer_records), 1)

            customer_record = customer_records[0]
            self.assertEqual(customer_record["id"], "d973631199")
            self.assertEqual(customer_record["firstname"], "Joe")
            self.assertEqual(customer_record["lastname"], "Bloggs")
            self.assertEqual(customer_record["email"], "joebloggs@ometria.com")
            self.assertEqual(customer_record["status"], "subscribed")

    def test_ometria_customer_record_not_created_if_mailchimp_unique_email_id_missing(
        self,
    ):
        with open(
            os.path.join(os.getcwd(), "json_files", "mailchimp_membership_single.json")
        ) as json_f:
            json_data = json.load(json_f)
            json_data["members"][0]["unique_email_id"] = ""

            customer_records = mapper.convert(json_data)

            self.assertEqual(len(customer_records), 0)

    def test_can_map_multiple_mailchimp_users_to_ometria_customer_records(self):
        with open(
            os.path.join(
                os.getcwd(), "json_files", "mailchimp_membership_multiple.json"
            )
        ) as json_f:
            json_data = json.load(json_f)

            customer_records = mapper.convert(json_data)

            self.assertEqual(len(customer_records), 5)


if __name__ == "__main__":
    unittest.main()
