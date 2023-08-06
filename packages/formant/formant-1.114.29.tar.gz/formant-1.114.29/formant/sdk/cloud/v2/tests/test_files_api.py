import unittest
from formant.sdk.cloud.v2.src.admin_api import AdminAPI
import os
import aiounittest
import uuid

EMAIL = os.getenv("FORMANT_EMAIL")
PASSWORD = os.getenv("FORMANT_PASSWORD")
ADMIN_API_URL = "https://api.formant.io/v1/admin"


class TestFiles(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestFiles, self).__init__(*args, **kwargs)
        self.client = AdminAPI(email=EMAIL, password=PASSWORD, api_url=ADMIN_API_URL)

    def test_upload(self):
        random_name = str(uuid.uuid4())
        file = open(f"{random_name}.txt", "w")
        file.write("Sample Data")
        file.close()
        path = file.name
        result = self.client.files.upload(path)
        os.remove(path)
        self.assertTrue(result)


class TestFilesAsync(aiounittest.AsyncTestCase):
    def __init__(self, *args, **kwargs):
        super(TestFilesAsync, self).__init__(*args, **kwargs)
        self.client = AdminAPI(email=EMAIL, password=PASSWORD, api_url=ADMIN_API_URL)

    async def test_async_upload(self):
        random_name = str(uuid.uuid4())
        file = open(f"test_{random_name}.txt", "w")
        file.write("Sample Data")
        file.close()
        path = file.name
        result = await self.client.files.upload_async(path)
        os.remove(path)
        self.assertTrue(result)


unittest.main()
