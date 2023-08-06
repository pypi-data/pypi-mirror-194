
from formant.sdk.cloud.v2.formant_admin_api_client.api.adapter import adapter_controller_post
from formant.sdk.cloud.v2.formant_admin_api_client.models import Adapter
from formant.sdk.cloud.v2.src.resources.resources import Resources

class Adapters(Resources):

    def create(self, adapter: Adapter):
        'Creates an Adapter'
        client = self._get_client()
        response = adapter_controller_post.sync_detailed(client=client, json_body=adapter)
        return response

    def create_async(self, adapter: Adapter):
        'Creates an Adapter'
        client = self._get_client()
        response = adapter_controller_post.asyncio_detailed(client=client, json_body=adapter)
        return response
