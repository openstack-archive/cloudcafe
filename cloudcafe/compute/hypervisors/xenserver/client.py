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

import XenAPI

from cafe.common.reporting import cclogging
from cafe.engine.clients.base import BaseClient
from cloudcafe.compute.hypervisors.xenserver.models.virtual_machine \
    import VirtualMachine, VirtualBlockDevice, VirtualDiskImage


def _log_failure(log):
    def _decorator(func):
        def _wrapper(*args, **kwargs):

            try:
                response = func(*args, **kwargs)
            except XenAPI.Failure as exception:
                log.error(exception)
                raise exception

            return response
        return _wrapper
    return _decorator


class XenAPIClient(BaseClient):

    def __init__(self, url, username, password):

        self.session = XenAPI.Session(url)
        self.session.xenapi.login_with_password(username, password)

    def get_vm_record(self, server_id):
        vm = self._get_vm_by_compute_id(server_id)
        record = self.session.xenapi.VM.get_record(vm)
        virtual_machine = VirtualMachine._dict_to_obj(**record)
        return virtual_machine

    def get_vbd_record(self, vbd):
        record = self.session.xenapi.VBD.get_record(vbd)
        block_device = VirtualBlockDevice._dict_to_obj(record)
        return block_device

    def get_vdi_record(self, vdi):
        record = self.session.xenapi.VDI.get_record(vdi)
        vdi = VirtualDiskImage._dict_to_obj(record)
        return vdi

    def _get_vm_by_compute_id(self, server_id):
        expected_vm_name = 'instance-{uuid}'.format(uuid=server_id)
        virtual_machines = self.session.xenapi.VM.get_all()
        for vm in virtual_machines:
            vm_name = self.session.xenapi.VM.get_name_label(vm)
            if expected_vm_name == vm_name:
                    return vm
        return None
