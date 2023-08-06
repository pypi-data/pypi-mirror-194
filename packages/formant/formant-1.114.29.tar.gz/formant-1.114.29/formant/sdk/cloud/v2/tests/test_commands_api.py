import unittest
from formant.sdk.cloud.v2.src.admin_api import AdminAPI
from formant.sdk.cloud.v2.formant_admin_api_client.models import (
    Command,
    CommandParameter,
    CommandQuery,
)
from dateutil import parser
import os

EMAIL = os.getenv("FORMANT_EMAIL")
PASSWORD = os.getenv("FORMANT_PASSWORD")
ADMIN_API_URL = "https://api.formant.io/v1/admin"


class TestCommands(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCommands, self).__init__(*args, **kwargs)
        self.client = AdminAPI(email=EMAIL, password=PASSWORD, api_url=ADMIN_API_URL)

    def test_create_command(self):
        device_id = "404e2d2c-f95f-41d8-bce1-915e314a6898"
        command_name = "return_to_charge_station"
        scrubber_time = parser.parse("2014-11-03T19:38:34.203Z")
        parameter = CommandParameter(scrubber_time=scrubber_time)
        command = Command(
            device_id=device_id,
            command=command_name,
            parameter=parameter,
            organization_id=self.client.organization_id,
        )
        result = self.client.commands.create(command)
        self.assertEqual(result.status_code, 201)

    def test_query_commands(self):
        device_id = "404e2d2c-f95f-41d8-bce1-915e314a6898"
        command_query = CommandQuery(device_id=device_id)
        result = self.client.commands.query(command_query)
        self.assertEqual(result.status_code, 200)


unittest.main()
