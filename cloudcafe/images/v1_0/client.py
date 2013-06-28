from cafe.engine.clients.rest import AutoMarshallingRestClient
from cloudcafe.images.v1_0.models.image import Image


class ImagesClient(AutoMarshallingRestClient):
    '''
    Client for Image API
    '''

    def __init__(self, url, auth_token, serialize_format, deserialize_format):
        """
        @param url: Base URL for the compute service
        @type url: String
        @param auth_token: Auth token to be used for all requests
        @type auth_token: String
        @param serialize_format: Format for serializing requests
        @type serialize_format: String
        @param deserialize_format: Format for de-serializing responses
        @type deserialize_format: String
        """
        super(ImagesClient, self).__init__(
            serialize_format,
            deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format
        )
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.deserialize_format
        )
        self.url = url

    def list_images(self, requestslib_kwargs=None):
        url = '{0}/images'.format(self.url)
        return self.request('GET', url, response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def list_images_detail(self, parameters_list, requestslib_kwargs=None):
        url = '{0}/images/detail'.format(self.url)
        return self.request('GET', url, params=parameters_list,
                            response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def get_image(self, image_id, requestslib_kwargs=None):
        url = '{0}/images/{1}'.format(self.url, image_id)
        return self.request('GET', url, response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_image(self, image_id, requestslib_kwargs=None):
        url = '{0}/images/{1}'.format(self.url, image_id)
        return self.request('DELETE', url, response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def filter_images_list(self, parameters_list, requestslib_kwargs=None):
        url = '{0}/images'.format(self.url)
        return self.request('GET', url, params=parameters_list,
                            response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def retrieve_metadata(self, image_id, requestslib_kwargs=None):
        url = '{0}/images/{1}'.format(self.url, image_id)
        return self.request('HEAD',
                            url,
                            requestslib_kwargs=requestslib_kwargs)

    def retrieve_raw_image_data(self, image_id, requestslib_kwargs=None):
        url = '{0}/images/{1}'.format(self.url, image_id)
        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)

    def add_image(self, image_name, image_data, headers=None,
                  image_meta_id=None, image_meta_store=None,
                  image_meta_disk_format=None,
                  image_meta_container_format=None, image_meta_size=None,
                  image_meta_checksum=None, image_meta_is_public=None,
                  image_meta_min_ram=None, image_meta_min_disk=None,
                  image_meta_owner=None, image_meta_property={},
                  image_meta_location=None,
                  requestslib_kwargs=None):

        headers = headers if headers else {}

        if image_data:
            headers['Content-Type'] = 'application/octet-stream'

        headers['x-image-meta-name'] = image_name
        headers['x-image-meta-id'] = image_meta_id
        headers['x-image-meta-store'] = image_meta_store
        headers['x-image-meta-disk-format'] = image_meta_disk_format
        headers['x-image-meta-container-format'] = image_meta_container_format
        headers['x-image-meta-size'] = image_meta_size
        headers['x-image-meta-checksum'] = image_meta_checksum
        headers['x-image-meta-is-public'] = image_meta_is_public
        headers['x-image-meta-min-ram'] = image_meta_min_ram
        headers['x-image-meta-min-disk'] = image_meta_min_disk
        headers['x-image-meta-owner'] = image_meta_owner
        headers['x-image-meta-location'] = image_meta_location
        for key, val in image_meta_property.items():
            headers['x-image-meta-property-{0}'.format(key)] = val

        url = '{0}/images'.format(self.url)
        return self.request('POST', url, headers=headers, data=image_data,
                            response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def list_image_membership(self, image_id, requestslib_kwargs=None):
            url = '{0}/images/{1}/members'.format(self.url, image_id)

            return self.request('GET', url,
                                requestslib_kwargs=requestslib_kwargs)

    def update_image(self, image_id, image_data=None, headers=None,
                     image_meta_name=None, image_meta_store=None,
                     image_meta_disk_format=None,
                     image_meta_container_format=None, image_meta_size=None,
                     image_meta_checksum=None, image_meta_is_public=None,
                     image_meta_min_ram=None, image_meta_min_disk=None,
                     image_meta_owner=None, image_meta_property={},
                     image_meta_location=None,
                     requestslib_kwargs=None):

        headers = headers if headers else {}

        if image_data:
            headers['Content-Type'] = 'application/octet-stream'

        headers['x-image-meta-name'] = image_meta_name
        headers['x-image-meta-store'] = image_meta_store
        headers['x-image-meta-disk-format'] = image_meta_disk_format
        headers['x-image-meta-container-format'] = image_meta_container_format
        headers['x-image-meta-size'] = image_meta_size
        headers['x-image-meta-checksum'] = image_meta_checksum
        headers['x-image-meta-is-public'] = image_meta_is_public
        headers['x-image-meta-min-ram'] = image_meta_min_ram
        headers['x-image-meta-min-disk'] = image_meta_min_disk
        headers['x-image-meta-owner'] = image_meta_owner
        headers['x-image-meta-location'] = image_meta_location
        for key, val in image_meta_property.items():
            headers['x-image-meta-property-{0}'.format(key)] = val

        url = '{0}/images/{1}'.format(self.url, image_id)
        return self.request('PUT', url, headers=headers,
                            data=image_data,
                            response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def list_shared_images(self, member_id, requestslib_kwargs=None):
        url = '{0}/shared-images/{1}'.format(self.url, member_id)

        return self.request('GET', url, response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def add_member_to_image(self, image_id, member_id,
                            requestslib_kwargs=None):
        url = '{0}/images/{1}/members/{2}'.format(self.url, image_id,
                                                  member_id)
        return self.request('PUT', url, requestslib_kwargs=requestslib_kwargs)

    def delete_member_from_image(self, image_id, member_id,
                                 requestslib_kwargs=None):
        url = '{0}/images/{1}/members/{2}'.format(self.url, image_id,
                                                  member_id)
        return self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)

    def replace_members_list(self, image_id, requestslib_kwargs=None):
        url = '{0}/images/{1}/members'.format(self.url, image_id)
        return self.request('PUT', url, requestslib_kwargs=requestslib_kwargs)
