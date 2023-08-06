
from formant.sdk.cloud.v2.src.resources.resources import Resources
from formant.sdk.cloud.v2.formant_admin_api_client.api.view import view_controller_get_one, view_controller_get_all, view_controller_patch
from formant.sdk.cloud.v2.formant_admin_api_client.models import PartialView

class Views(Resources):

    def get(self, device_id: str):
        'Get a device layout'
        client = self._get_client()
        response = view_controller_get_one.sync_detailed(client=client, id=device_id)
        return response

    def get_async(self, device_id: str):
        'Get a device layout'
        client = self._get_client()
        response = view_controller_get_one.asyncio_detailed(client=client, id=device_id)
        return response

    def get_all(self):
        'List all device layouts'
        client = self._get_client()
        response = view_controller_get_all.sync_detailed(client=client)
        return response

    def get_all_async(self):
        'List all device layouts'
        client = self._get_client()
        response = view_controller_get_all.asyncio_detailed(client=client)
        return response

    def patch(self, id: str, partial_view: PartialView):
        'Update a device layout'
        client = self._get_client()
        response = view_controller_patch.sync_detailed(client=client, id=id, json_body=partial_view)
        return response

    def patch_async(self, id: str, partial_view: PartialView):
        'Update a device layout'
        client = self._get_client()
        response = view_controller_patch.asyncio_detailed(client=client, id=id, json_body=partial_view)
        return response
