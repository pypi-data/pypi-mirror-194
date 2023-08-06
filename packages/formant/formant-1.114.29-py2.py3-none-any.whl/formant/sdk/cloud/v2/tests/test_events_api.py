import unittest
from formant.sdk.cloud.v2.src.admin_api import AdminAPI
from formant.sdk.cloud.v2.formant_admin_api_client.models import EventQuery
from datetime import datetime
import os

EMAIL = os.getenv("FORMANT_EMAIL")
PASSWORD = os.getenv("FORMANT_PASSWORD")
ADMIN_API_URL = "https://api.formant.io/v1/admin"


class TestEvents(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestEvents, self).__init__(*args, **kwargs)
        self.client = AdminAPI(email=EMAIL, password=PASSWORD, api_url=ADMIN_API_URL)

    def test_query(self):
        event_query = EventQuery(count=3)
        result = self.client.events.query(event_query)
        self.assertEqual(result.status_code, 200)


unittest.main()
