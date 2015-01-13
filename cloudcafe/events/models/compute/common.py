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

from cloudcafe.events.models.base import EventBaseModel, EventBaseListModel


class FixedIp(EventBaseModel):
    """Fixed IP Response Model

    @summary: Response model for a fixed IP address from a
        compute event notification
    @note: Represents a single fixed IP

    JSON Example:
        {
            "floating_ips": [],
            "meta": {},
            "type": "fixed",
            "version": 4,
            "address": "10.10.0.0",
            "label": "public"
        }
    """
    kwarg_map = {
        'floating_ips': 'floating_ips',
        'meta': 'meta',
        'type_': 'type',
        'version': 'version',
        'address': 'address',
        'label': 'label'}

    def __init__(self, floating_ips, meta, type_, version, address, label):
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
