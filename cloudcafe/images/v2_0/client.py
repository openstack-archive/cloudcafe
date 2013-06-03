from cafe.engine.clients.rest import AutoMarshallingRestClient
from cloudcafe.images.v2_0.models.image import Image


class ImageClient(AutoMarshallingRestClient):
    """Client for Openstack Image API V2.0
    """

    def __init__(self, base_url, auth_token, serialize_format='json', deserialize_format='json'):
        """@Summary construct an Image API client
        """
        super(ImageClient, self).__init__(
            serialize_format,
            deserialize_format)
        self.base_url = base_url
        self.serialize_format = serialize_format
        self.deserialize_format = deserialize_format
        self.default_headers['X-Auth-Token'] = auth_token

    def get_images_schema(self, **requestslib_kwargs):
        url = '{0}{1}'.format(self.base_url, '/schemas/images')
        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)

    def get_image_schema(self, **requestslib_kwargs):
        url = '{0}{1}'.format(self.base_url, '/schemas/image')
        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)

    def create_image(self, image, **requestslib_kwargs):
        serialized_obj = image._obj_to_json()
        url = '{0}{1}'.format(self.base_url, '/images')

        return self.request('POST', url, body=serialized_obj, requestslib_kwargs=requestslib_kwargs)

    def update_image(self, image_id, **requestslib_kwargs):
        pass

    def add_tag(self, image_id, tag, **requestslib_kwargs):
        pass

    def delete_tag(self, image_id, tag, **requestslib_kwargs):
        pass

    def list_images(self, filters, sort, **requestslib_kwargs):
        pass

    def get_image(self, image_id, **requestslib_kwargs):
        url = '{0}/images/{1}'.format(self.base_url, image_id)
        return self.request('GET', url, response_entity_type=Image, requestslib_kwargs=requestslib_kwargs)

    def delete_image(self, image_id, **requestslib_kwargs):
        pass

    def store_raw_image_data(self, image_id, **requestslib_kwargs):
        pass

    def get_raw_image_data(self, image_id, **requestslib_kwargs):
        pass
