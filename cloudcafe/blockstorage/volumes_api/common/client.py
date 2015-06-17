"""
Copyright 2015 Rackspace

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
import abc
from cafe.engine.http.client import AutoMarshallingHTTPClient


class BaseVolumesClient(AutoMarshallingHTTPClient):
    __metaclass__ = abc.ABCMeta

    def __init__(
            self, url, auth_token, serialize_format=None,
            deserialize_format=None):

        super(BaseVolumesClient, self).__init__(
            serialize_format, deserialize_format)

        self.url = url
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.deserialize_format)

    @abc.abstractproperty
    def request_models(self):
        pass

    @abc.abstractproperty
    def response_models(self):
        pass

    @abc.abstractmethod
    def create_volume(self):
        pass

    @abc.abstractmethod
    def update_volume(self):
        pass

    @abc.abstractmethod
    def create_snapshot(self):
        pass

    # Volumes
    def list_all_volumes(self, requestslib_kwargs=None):

        """GET /volumes"""

        url = '{0}/volumes'.format(self.url)
        return self.request(
            'GET', url,
            response_entity_type=self.response_models.VolumeListResponse,
            requestslib_kwargs=requestslib_kwargs)

    def list_all_volumes_info(self, requestslib_kwargs=None):

        """GET /volumes/detail"""

        url = '{0}/volumes/detail'.format(self.url)
        return self.request(
            'GET', url,
            response_entity_type=self.response_models.VolumeListResponse,
            requestslib_kwargs=requestslib_kwargs)

    def get_volume_info(self, volume_id, requestslib_kwargs=None):

        """GET /volumes/{volume_id}"""

        url = '{0}/volumes/{1}'.format(self.url, volume_id)
        return self.request(
            'GET', url,
            response_entity_type=self.response_models.VolumeResponse,
            requestslib_kwargs=requestslib_kwargs)

    def delete_volume(self, volume_id, requestslib_kwargs=None):

        """DELETE /volumes/{volume_id}"""

        url = '{0}/volumes/{1}'.format(self.url, volume_id)
        return self.request(
            'DELETE', url,
            response_entity_type=self.response_models.VolumeResponse,
            requestslib_kwargs=requestslib_kwargs)

    def set_volume_status(self, volume_id, status, requestslib_kwargs=None):
        url = '{0}/volumes/{1}/action'.format(self.url, volume_id)

        request_entity = self.request_models.StatusResetRequest(
            status=status)

        return self.request(
            'POST', url, request_entity=request_entity,
            requestslib_kwargs=None)

    # Volume Types
    def list_all_volume_types(self, requestslib_kwargs=None):

        """GET /types """
        url = '{0}/types'.format(self.url)
        return self.request(
            'GET', url,
            response_entity_type=self.response_models.VolumeTypeListResponse,
            requestslib_kwargs=requestslib_kwargs)

    def get_volume_type_info(self, volume_type_id, requestslib_kwargs=None):

        """GET /types/{volume_type_id}"""

        url = '{0}/types/{1}'.format(self.url, volume_type_id)
        return self.request(
            'GET', url,
            response_entity_type=self.response_models.VolumeTypeResponse,
            requestslib_kwargs=requestslib_kwargs)

    def create_volume_type(
            self, name, extra_specs=None, requestslib_kwargs=None):
        """ POST /types"""

        url = '{url}/types'.format(url=self.url)

        request_entity = self.request_models.VolumeTypeCreateRequest(
            name=name, extra_specs=extra_specs)

        return self.request(
            'POST', url, request_entity=request_entity,
            response_entity_type=self.response_models.VolumeTypeResponse,
            requestslib_kwargs=requestslib_kwargs)

    def delete_volume_type(self, volume_type_id, requestslib_kwargs=None):
        """ DELETE /types/{volume_type_id} """

        url = '{url}/types/{volume_type_id}'.format(
            url=self.url, volume_type_id=volume_type_id)

        return self.request(
            'DELETE', url, requestslib_kwargs=requestslib_kwargs)

    def update_volume_type_extra_specs(
            self, volume_type_id, extra_specs=None, requestslib_kwargs=None):
        """ POST /types/{volume_type_id}/extra_specs """

        extra_specs = extra_specs or dict()
        url = '{url}/types/{volume_type_id}/extra_specs'.format(
            url=self.url, volume_type_id=volume_type_id)

        request_entity = self.request_models.VolumeTypeExtraSpecsUpdateRequest(
            extra_specs=extra_specs)

        return self.request(
            'POST', url, request_entity=request_entity,
            response_entity_type=self.response_models.VolumeTypeResponse,
            requestslib_kwargs=requestslib_kwargs)

    def delete_volume_type_extra_spec(
            self, volume_type_id, extra_spec_key, requestslib_kwargs=None):
        """ DELETE /types/{volume_type_id}/extra_specs/{extra_spec_key} """

        url = '{url}/types/{vtype_id}/extra_specs/{extra_spec_key}'.format(
            url=self.url, vtype_id=volume_type_id,
            extra_spec_key=extra_spec_key)

        return self.request(
            'DELETE', url, requestslib_kwargs=requestslib_kwargs)

    # Snapshots
    def list_all_snapshots(self, requestslib_kwargs=None):

        """GET /snapshots"""

        url = '{0}/snapshots'.format(self.url)

        return self.request(
            'GET', url, response_entity_type=
            self.response_models.VolumeSnapshotListResponse,
            requestslib_kwargs=requestslib_kwargs)

    def list_all_snapshots_info(self, requestslib_kwargs=None):

        """GET /snapshots/detail"""

        url = '{0}/snapshots/detail'.format(self.url)
        return self.request(
            'GET', url, response_entity_type=
            self.response_models.VolumeSnapshotListResponse,
            requestslib_kwargs=requestslib_kwargs)

    def get_snapshot_info(self, snapshot_id, requestslib_kwargs=None):

        """GET /snapshots/{snapshot_id}"""

        url = '{0}/snapshots/{1}'.format(self.url, snapshot_id)

        return self.request(
            'GET', url,
            response_entity_type=self.response_models.VolumeSnapshotResponse,
            requestslib_kwargs=requestslib_kwargs)

    def delete_snapshot(self, snapshot_id, requestslib_kwargs=None):

        """Delete /snapshots/{snapshot_id} """

        url = '{0}/snapshots/{1}'.format(self.url, snapshot_id)
        return self.request(
            'DELETE', url,
            response_entity_type=self.response_models.VolumeSnapshotResponse,
            requestslib_kwargs=requestslib_kwargs)

    def set_snapshot_status(
            self, snapshot_id, status, requestslib_kwargs=None):
        url = '{0}/snapshots/{1}/action'.format(self.url, snapshot_id)

        request_entity = self.request_models.StatusResetRequest(
            status=status)

        return self.request(
            'POST', url, request_entity=request_entity,
            requestslib_kwargs=None)

    # Quotas
    def list_quotas(self, target_tenant_id, requestslib_kwargs=None):
        """GET /{admin_tenant_id}/os-quota-sets/{target_tenant_id}"""

        url = '{url}/os-quota-sets/{target_tenant_id}'.format(
            url=self.url, target_tenant_id=target_tenant_id)

        return self.request(
            'GET', url,
            response_entity_type=self.response_models.QuotaListResponse,
            requestslib_kwargs=requestslib_kwargs)

    def list_quotas_usage(self, target_tenant_id, requestslib_kwargs=None):
        """GET /{admin_tenant_id}/os-quota-sets/{target_tenant_id}"""

        url = '{url}/os-quota-sets/{target_tenant_id}'.format(
            url=self.url, target_tenant_id=target_tenant_id)

        params = {'usage': True}

        return self.request(
            'GET', url,
            response_entity_type=self.response_models.QuotaUsageResponse,
            params=params, requestslib_kwargs=requestslib_kwargs)
