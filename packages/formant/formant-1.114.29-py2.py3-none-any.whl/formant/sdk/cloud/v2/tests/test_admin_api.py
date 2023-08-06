import unittest
from formant.sdk.cloud.v2.src.admin_api import AdminAPI
from formant.sdk.cloud.v2.formant_admin_api_client import AuthenticatedClient
import os

EMAIL = os.getenv("FORMANT_EMAIL")
PASSWORD = os.getenv("FORMANT_PASSWORD")
ADMIN_API_URL = "https://api.formant.io/v1/admin"


class TestAuthentication(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAuthentication, self).__init__(*args, **kwargs)
        self.client = AdminAPI(email=EMAIL, password=PASSWORD, api_url=ADMIN_API_URL)

    def test_authenticate(self):
        new_client = self.client.get_client()
        self.assertIs(type(new_client), AuthenticatedClient)

    def test_authenticate_refresh(self):
        _ = self.client.get_client()
        new_client = self.client.get_client()
        self.assertIs(type(new_client), AuthenticatedClient)


unittest.main()
