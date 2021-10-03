import os

# Mailchimp specific config
MAILCHIMP_BASE_URL = os.environ.get("MAILCHIMP_BASE_URL")
MAILCHIMP_API_KEY = os.environ.get("MAILCHIMP_API_KEY")
MAILCHIMP_LIST_ID = os.environ.get("MAILCHIMP_LIST_ID")

# Ometria specific config
OMETRIA_API_URL = os.environ.get("OMETRIA_API_URL")
OMETRIA_API_KEY = os.environ.get("OMETRIA_API_KEY")

# Application config
# I didn't want to import the logging module into here
LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", 20)
