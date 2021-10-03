import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def convert(mailchimp_members: Dict[Any, Any]) -> List[Dict[str, Any]]:
    """
    Converts the mailchimp members response into a list of Ometria contact records format.

    Notes:
    I read the documentation as the fields are always present but nullable (Though actual responses
    look to just be empty strings), Perhaps I should use try-except here?
    From the Ometria API snippet I assume the only valid thing I need is an ID so I'll just check to make sure it
    actually exists, before adding it to the list
    :param mailchimp_members: the mailchimp users API response
    :return: a list of users in Ometria contact records format
    """
    result = []

    if not mailchimp_members or "members" not in mailchimp_members:
        return result

    for member in mailchimp_members["members"]:
        ometria_user = {
            "id": member.get("unique_email_id"),
            "firstname": member.get("merge_fields", {}).get("FNAME"),
            "lastname": member.get("merge_fields", {}).get("LNAME"),
            "email": member.get("email_address"),
            "status": member.get("status"),
        }

        logger.debug(
            f"Converted Mailchimp member: {member} into Ometria contact record: {ometria_user}"
        )

        if ometria_user.get("id"):
            result.append(ometria_user)
        else:
            logger.warning(
                f"Skipping mailchimp user, no valid unique email id: {member}"
            )

    return result
