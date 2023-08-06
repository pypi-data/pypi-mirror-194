
from formant.sdk.cloud.v2.formant_admin_api_client.models import EventQuery
from formant.sdk.cloud.v2.formant_admin_api_client.api.event import event_controller_query
from formant.sdk.cloud.v2.src.resources.resources import Resources

class Events(Resources):

    def query(self, event_query: EventQuery):
        'Get an event'
        client = self._get_client()
        response = event_controller_query.sync_detailed(client=client, json_body=event_query)
        return response

    def query_async(self, event_query: EventQuery):
        'Get an event'
        client = self._get_client()
        response = event_controller_query.asyncio_detailed(client=client, json_body=event_query)
        return response
