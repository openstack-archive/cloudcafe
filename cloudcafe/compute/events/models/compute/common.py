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

from cloudcafe.compute.events.models.base import EventBaseModel, EventBaseListModel


class Bandwidth(EventBaseModel):
    """Bandwidth Response Model

    @summary: Response model for bandwidth from a compute
        event notification
    @note: Although the 'public' and 'private' interfaces are
        not required, they are the most common names, and are
        included as optional attributes for the sake of convenience
    @note: This type may contain additional unspecified
        BandwidthInterface fields, which will be captured in a
        dictionary called kwargs

    JSON Example:
        {
            "private": { <BandwidthInterface> },
            "public": { <BandwidthInterface> }
        }
    """
    kwarg_map = {'private': 'private',
                 'public': 'public'}
    optional_kwargs = ['private', 'public']
    strict_checking = False

    def __init__(self, private=None, public=None, **kwargs):
        super(Bandwidth, self).__init__(locals())

    @classmethod
    def _dict_to_obj(cls, json_dict):
        """Override dict_to_obj implementation"""
        obj = cls._map_values_to_kwargs(json_dict)

        for key in obj.kwargs:
            obj.kwargs[key] = BandwidthInterface._dict_to_obj(obj.kwargs[key])

        if obj.private:
            obj.private = BandwidthInterface._dict_to_obj(obj.private)
        if obj.public:
            obj.public = BandwidthInterface._dict_to_obj(obj.public)

        return obj


class BandwidthInterface(EventBaseModel):
    """Bandwidth Interface Response Model

    @summary: Response model for bandwidth on an interface from
        a compute event notification
    @note: Sub-model of Bandwidth

    JSON Example:
        {
            "bw_in": 123456,
            "bw_out": 654321
        }
    """
    kwarg_map = {'bw_in': 'bw_in',
                 'bw_out': 'bw_out'}

    def __init__(self, bw_in, bw_out):
        super(BandwidthInterface, self).__init__(locals())


class FixedIp(EventBaseModel):
    """Fixed IP Response Model

    @summary: Response model for a fixed IP address from a
        compute event notification
    @note: Represents a single fixed IP

    JSON Example:
        {
            "address": "10.10.0.0",
            "floating_ips": [],
            "label": "public",
            "meta": {},
            "type": "fixed",
            "version": 4,
            "vif_mac": "FE:ED:FA:00:1C:D4"
        }
    """
    kwarg_map = {
        'address': 'address',
        'floating_ips': 'floating_ips',
        'label': 'label',
        'meta': 'meta',
        'type_': 'type',
        'version': 'version',
        'vif_mac': 'vif_mac'}

    def __init__(self, address, floating_ips, label, meta, type_, version,
                 vif_mac):
        super(FixedIp, self).__init__(locals())


class FixedIps(EventBaseListModel):
    """Fixed IPs Model

    @summary: Response model for a list of fixed IP addresses
        from a compute event notification
    @note: Returns a list of elements of type 'FixedIp'

    JSON Example:
        {
            "fixed_ips": [
                { <FixedIp> },
                { <FixedIp> }
            ]
        }
    """
    list_model_key = 'fixed_ips'
    ObjectModel = FixedIp


class ImageMeta(EventBaseModel):
    """Image Metadata Model

    @summary: Response model for image metadata from a compute
        event notification
    @note: This type may contain additional unspecified
        fields, which will be captured in a dictionary called kwargs

    JSON Example:
        {
            "image_meta": {
                "auto_disk_config": "disabled",
                "base_image_ref": "5e91ad7f-afe4-4a83-bd5f-84673462cae1",
                "container_format": "ovf",
                "disk_format": "vhd",
                "image_type": "base",
                "min_disk": "20",
                "min_ram": "512",
                "org.openstack__1__architecture": "x64",
                "org.openstack__1__os_distro": "com.ubuntu",
                "org.openstack__1__os_version": "12.04",
                "os_type": "linux"
            }
        }
    """
    kwarg_map = {
        'auto_disk_config': 'auto_disk_config',
        'base_image_ref': 'base_image_ref',
        'container_format': 'container_format',
        'disk_format': 'disk_format',
        'image_type': 'image_type',
        'min_disk': 'min_disk',
        'min_ram': 'min_ram',
        'org_openstack__1__architecture': 'org.openstack__1__architecture',
        'org_openstack__1__os_distro': 'org.openstack__1__os_distro',
        'org_openstack__1__os_version': 'org.openstack__1__os_version',
        'os_type': 'os_type'}
    strict_checking = False

    def __init__(self, auto_disk_config, base_image_ref, container_format,
                 disk_format, image_type, min_disk, min_ram,
                 org_openstack__1__architecture, org_openstack__1__os_distro,
                 org_openstack__1__os_version, os_type, **kwargs):
        super(ImageMeta, self).__init__(locals())


class InstanceException(EventBaseModel):
    """Instance Exception Model

    @summary: Response model for an instance exception from a
        compute event notification
    @note: Represents a single instance exception

    JSON Example:
        {
            "exception": {
                "kwargs": {
                    "instance_uuid": "5e91ad7f-afe4-4a83-bd5f-84673462cae1",
                    "reason": "Something broke",
                    "code": 500
                }
            }
        }
    """
    kwarg_map = {'kwargs': 'kwargs'}

    def __init__(self, kwargs):
        super(InstanceException, self).__init__(locals())
