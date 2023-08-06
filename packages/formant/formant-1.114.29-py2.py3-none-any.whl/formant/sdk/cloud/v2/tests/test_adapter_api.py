import unittest
from formant.sdk.cloud.v2.src.admin_api import AdminAPI
from formant.sdk.cloud.v2.formant_admin_api_client.models import Adapter
import os

EMAIL = os.getenv("FORMANT_EMAIL")
PASSWORD = os.getenv("FORMANT_PASSWORD")
ADMIN_API_URL = "https://api.formant.io/v1/admin"


class TestAdapters(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAdapters, self).__init__(*args, **kwargs)
        self.client = AdminAPI(email=EMAIL, password=PASSWORD, api_url=ADMIN_API_URL)

    # def test_create_adapter(self):
    #     name = "generic-test"
    #     file_id = "cd860575-df44-40ea-a1ef-c5860c1a8992"
    #     exec_command = "test"
    #     adapter = Adapter(name, file_id, exec_command)
    #     result = self.client.adapters.create(adapter)
    #     self.assertEqual(result.status_code, 201)


unittest.main()
