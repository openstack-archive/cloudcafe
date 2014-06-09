"""
Copyright 2013 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from cafe.engine.models.base import CommonToolsMixin

from cloudcafe.compute.images_api.common.client import BaseImagesClient
from cloudcafe.compute.images_api.models import requests
from cloudcafe.compute.images_api.models import responses


class ImagesClient(BaseImagesClient):
    def get_images(
            self, server=None, name=None, status=None, changes_since=None,
            marker=None, limit=None, type_=None, requestslib_kwargs=None):
        params = {
            "server": server, "name": name, "status": status,
            "changes-since": changes_since, "marker": marker, "limit": limit,
            "type": type_}
        params = CommonToolsMixin._remove_empty_values(params)
        url = '{0}/images'.format(self.url)
        return self.get(
            url, #response_entity_type=responses.TenantList,
            requestslib_kwargs=requestslib_kwargs)
"""
    def get_images_detail(self, id_=None, requestslib_kwargs=None):


    def get_image(self, id_=None, requestslib_kwargs=None):


    def delete_image(self, id_=None, requestslib_kwargs=None):



GET /images?server=serverRef&name=imageName&status=imageStatus&changes-since=dateTime&marker=markerID&limit=int&type=(BASE|SNAPSHOT)
Lists IDs, names, and links for all available images.


GET /images/detail?server=serverRef&name=imageName&status=imageStatus&changes-since=dateTime&marker=markerID&limit=int&type=(BASE|SNAPSHOT)
List all details for all available images.


GET /images/id Lists details of the specified image.
DELETE /images/id"""