from cafe.engine.clients.rest import AutoMarshallingRestClient
from cloudcafe.images.v2_0.models.image import Image, ImagePatch


class ImageClient(AutoMarshallingRestClient):
    """
        Client for Openstack Image API V2.0
    """

    def __init__(self, base_url, auth_token, serialize_format='json',
                 deserialize_format='json'):
        """@Summary construct an Image API client
        """
        super(ImageClient, self).__init__(
            serialize_format,
            deserialize_format)
        self.base_url = base_url
        self.serialize_format = serialize_format
        self.deserialize_format = deserialize_format
        self.default_headers['X-Auth-Token'] = auth_token

    def get_images_schema(self, requestslib_kwargs=None):
        """
            Get JSON-schema of the images object.
        """
        url = '{0}{1}'.format(self.base_url, '/schemas/images')
        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)

    def get_image_schema(self, requestslib_kwargs=None):
        """
            Get JSON-schema of the image object.
        """
        url = '{0}{1}'.format(self.base_url, '/schemas/image')
        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)

    def create_image(self, id_=None, name=None, visibility=None,
                     status=None, protected=None, tags=None, checksum=None,
                     size=None, created_at=None, updated_at=None, file_=None,
                     self_=None, schema=None, container_format=None,
                     disk_format=None, min_disk=None, min_ram=None,
                     kernel_id=None, ramdisk_id=None, requestslib_kwargs=None):
        """
            Create a new Image.
        """
        image = Image(id_=id_, name=name, visibility=visibility,
                      status=status, protected=protected, tags=tags,
                      checksum=checksum, size=size, created_at=created_at,
                      updated_at=updated_at, file_=file_, self_=self_,
                      schema=schema, container_format=container_format,
                      disk_format=disk_format, min_disk=min_disk,
                      min_ram=min_ram, kernel_id=kernel_id,
                      ramdisk_id=ramdisk_id)
        url = '{0}/images'.format(self.base_url)

        return self.request('POST', url, request_entity=image,
                            response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def update_image(self, image_id, replace=None, add=None, remove=None,
                     requestslib_kwargs=None):
        """
            Update an Image.
            @param add a dictionary of properties to be added,
            @param replace a dictionary of properties to be replaced,
            @param remove a list of properties to be removed
        """
        url = '{0}/images/{1}'.format(self.base_url, image_id)

        image_patch = ImagePatch(add, replace, remove)

        return self.request('PATCH', url,
                            request_entity=image_patch,
                            response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def add_tag(self, image_id, tag, requestslib_kwargs=None):
        url = '{base_url}/images/{image_id}/tags/{tag}'.format(
            base_url=self.base_url,
            image_id=image_id,
            tag=tag)

        return self.request('PUT', url,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_tag(self, image_id, tag, requestslib_kwargs=None):
        url = '{base_url}/images/{image_id}/tags/{tag}'.format(
            base_url=self.base_url,
            image_id=image_id,
            tag=tag)

        return self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)

    def list_images(self, filters={}, sort_key='updated_at', sort_dir='desc',
                    requestslib_kwargs=None):
        url = '{base_url}/images'.format(base_url=self.base_url)
        params = filters
        params['sort_key'] = sort_key
        params['sort_dir'] = sort_dir
        return self.request('GET', url, params=params,
                            response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def get_image(self, image_id, requestslib_kwargs=None):
        url = '{0}/images/{1}'.format(self.base_url, image_id)
        return self.request('GET', url, response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_image(self, image_id, requestslib_kwargs=None):
        url = '{0}/images/{1}'.format(self.base_url, image_id)
        return self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)

    def store_raw_image_data(self, image_id, requestslib_kwargs=None):
        raise NotImplementedError

    def get_raw_image_data(self, image_id, requestslib_kwargs=None):
        raise NotImplementedError
