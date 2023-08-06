
from formant.sdk.cloud.v2.formant_admin_api_client.api.command import command_controller_post, command_controller_query
from formant.sdk.cloud.v2.formant_admin_api_client.models import Command, CommandQuery
from formant.sdk.cloud.v2.src.resources.resources import Resources

class Commands(Resources):

    def create(self, command: Command):
        'Creates a command'
        client = self._get_client()
        response = command_controller_post.sync_detailed(client=client, json_body=command)
        return response

    def create_async(self, command: Command):
        'Creates a command'
        client = self._get_client()
        response = command_controller_post.asyncio_detailed(client=client, json_body=command)
        return response

    def query(self, command_query: CommandQuery):
        'Query undelivered commands by device ID'
        client = self._get_client()
        response = command_controller_query.sync_detailed(client=client, json_body=command_query)
        return response

    def query_async(self, command_query: CommandQuery):
        'Query undelivered commands by device ID'
        client = self._get_client()
        response = command_controller_query.asyncio_detailed(client=client, json_body=command_query)
        return response
