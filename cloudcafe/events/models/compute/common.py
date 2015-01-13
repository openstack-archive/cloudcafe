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
