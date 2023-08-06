
from formant.sdk.cloud.v2.src.resources.resources import Resources
from formant.sdk.cloud.v2.formant_admin_api_client.api.annotation import annotation_controller_post
from formant.sdk.cloud.v2.formant_admin_api_client.api.annotation_template import annotation_template_controller_list, annotation_template_controller_get_one
from formant.sdk.cloud.v2.formant_admin_api_client.models import Annotation

class Annotations(Resources):

    def list_templates(self):
        'List all annotations'
        client = self._get_client()
        response = annotation_template_controller_list.sync_detailed(client=client)
        return response

    def list_templates_async(self):
        'List all annotations'
        client = self._get_client()
        response = annotation_template_controller_list.asyncio_detailed(client=client)
        return response

    def get_template(self, id: str):
        'Get an annotation'
        client = self._get_client()
        response = annotation_template_controller_get_one.sync_detailed(client=client, id=id)
        return response

    def get_template_async(self, id: str):
        'Get an annotation'
        client = self._get_client()
        response = annotation_template_controller_get_one.asyncio_detailed(client=client, id=id)
        return response

    def post(self, annotation: Annotation):
        'Creates an annotation'
        client = self._get_client()
        response = annotation_controller_post.sync_detailed(client=client, json_body=annotation)
        return response

    def post_async(self, annotation: Annotation):
        'Creates an annotation'
        client = self._get_client()
        response = annotation_controller_post.asyncio_detailed(client=client, json_body=annotation)
        return response
