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

from cafe.engine.models.base import BaseModel


class VirtualMachine(BaseModel):

    def __init__(self, label=None, description=None, vcpus_at_startup=None,
                 power_state=None, vcpus_params=None, vcpus_max=None,
                 xenstore_data=None, memory_static_min=None,
                 memory_static_max=None, memory_dynamic_min=None,
                 memory_dynamic_max=None, allowed_operations=None,
                 blocked_operations=None, ha_restart_priority=None,
                 pv_bootloader=None, snapshots=None, shutdown_delay=None,
                 domid=None, pci_bus=None, children=None,
                 hvm_shadow_multiplier=None, start_delay=None,
                 actions_after_crash=None, memory_target=None, uuid=None,
                 pv_ramdisk=None, tags=None, recommendations=None,
                 is_control_domain=None, hvm_boot_params=None,
                 snapshot_time=None, actions_after_shutdown=None,
                 user_version=None, snapshot_info=None,
                 transportable_snapshot_id=None, is_a_template=None,
                 crash_dumps=None, is_snapshot_from_vmpp=None,
                 is_a_snapshot=None, blobs=None, version=None,
                 current_operations=None, domarch=None,
                 pv_bootloader_args=None, snapshot_metadata=None,
                 other_config=None, actions_after_reboot=None,
                 attached_pcis=None, pv_legacy_args=None, bios_strings=None,
                 last_boot_cpu_flags=None, order=None):
        super(VirtualMachine, self).__init__()
        self.label = label
        self.description = description
        self.vcpus_at_startup = vcpus_at_startup
        self.power_state = power_state
        self.vcpus_params = vcpus_params
        self.vcpus_max = vcpus_max
        self.xenstore_data = xenstore_data
        self.memory_static_min = memory_static_min
        self.memory_static_max = memory_static_max
        self.memory_dynamic_max = memory_dynamic_min
        self.memory_dynamic_min = memory_dynamic_max
        self.allowed_operations = allowed_operations
        self.blocked_operations = blocked_operations
        self.ha_restart_priority = ha_restart_priority
        self.pv_bootloader = pv_bootloader
        self.snapshots = snapshots
        self.shutdown_delay = shutdown_delay
        self.domid = domid
        self.pci_bus = pci_bus
        self.children = children
        self.hvm_shadow_multiplier = hvm_shadow_multiplier
        self.start_delay = start_delay
        self.actions_after_crash = actions_after_crash
        self.memory_target = memory_target
        self.uuid = uuid
        self.pv_ramdisk = pv_ramdisk
        self.tags = tags
        self.recommendations = recommendations
        self.is_control_domain = is_control_domain
        self.hvm_boot_params = hvm_boot_params
        self.snapshot_time = snapshot_time
        self.actions_after_shutdown = actions_after_shutdown
        self.user_version = user_version
        self.snapshot_info = snapshot_info
        self.transportable_snapshot_id = transportable_snapshot_id
        self.is_a_template = is_a_template
        self.crash_dumps = crash_dumps
        self.is_snapshot_from_vmpp = is_snapshot_from_vmpp
        self.is_a_snapshot = is_a_snapshot
        self.blobs = blobs
        self.version = version
        self.current_operations = current_operations
        self.domarch = domarch
        self.pv_bootloader_args = pv_bootloader_args
        self.snapshot_metadata = snapshot_metadata
        self.other_config = other_config
        self.actions_after_reboot = actions_after_reboot
        self.attached_pcis = attached_pcis
        self.pv_legacy_args = pv_legacy_args
        self.bios_strings = bios_strings
        self.last_boot_cpu_flags = last_boot_cpu_flags
        self.order = order

    @classmethod
    def _dict_to_obj(cls, **kwargs):
        vm = VirtualMachine(
            label=kwargs.get('name_label'),
            description=kwargs.get('name_description'),
            vcpus_at_startup=kwargs.get('VCPUs_at_startup'),
            power_state=kwargs.get('power_state'),
            vcpus_params=kwargs.get('vcpus_params'),
            vcpus_max=kwargs.get('VCPUs_max'), version=kwargs.get('version'),
            xenstore_data=kwargs.get('xenstore_data'),
            memory_static_min=kwargs.get('memory_static_min'),
            memory_static_max=kwargs.get('memory_static_max'),
            memory_dynamic_min=kwargs.get('memory_dynamic_min'),
            memory_dynamic_max=kwargs.get('memory_dynamic_max'),
            allowed_operations=kwargs.get('allowed_operations'),
            blocked_operations=kwargs.get('blocked_operations'),
            ha_restart_priority=kwargs.get('ha_restart_priority'),
            pv_bootloader=kwargs.get('PV_bootloader'),
            snapshots=kwargs.get('snapshots'), domid=kwargs.get('domid'),
            shutdown_delay=kwargs.get('shutdown_delay'),
            pci_bus=kwargs.get('PCI_bus'), children=kwargs.get('children'),
            hvm_shadow_multiplier=kwargs.get('HVM_shadow_multiplier'),
            start_delay=kwargs.get('start_delay'), tags=kwargs.get('tags'),
            actions_after_crash=kwargs.get('actions_after_crash'),
            memory_target=kwargs.get('memory_target'),
            uuid=kwargs.get('uuid'), pv_ramdisk=kwargs.get('pv_ramdisk'),
            recommendations=kwargs.get('recommendations'),
            is_control_domain=kwargs.get('is_control_domain'),
            hvm_boot_params=kwargs.get('HVM_boot_params'),
            snapshot_time=kwargs.get('snapshot_time'),
            actions_after_shutdown=kwargs.get('actions_after_shutdown'),
            user_version=kwargs.get('user_version'),
            snapshot_info=kwargs.get('snapshot_info'),
            transportable_snapshot_id=kwargs.get('transportable_snapshot_id'),
            is_a_template=kwargs.get('is_a_template'),
            crash_dumps=kwargs.get('crash_dumps'), blobs=kwargs.get('blobs'),
            is_snapshot_from_vmpp=kwargs.get('is_snapshot_from_vmpp'),
            is_a_snapshot=kwargs.get('is_a_snapshot'),
            current_operations=kwargs.get('current_operations'),
            domarch=kwargs.get('domarch'), order=kwargs.get('order'),
            pv_bootloader_args=kwargs.get('PV_bootloader_args'),
            snapshot_metadata=kwargs.get('snapshot_metadata'),
            other_config=kwargs.get('other_config'),
            actions_after_reboot=kwargs.get('actions_after_reboot'),
            attached_pcis=kwargs.get('attached_PCIs'),
            pv_legacy_args=kwargs.get('PV_legacy_args'),
            bios_strings=kwargs.get('bios_strings'),
            last_boot_cpu_flags=kwargs.get('last_boot_cpu_flags'))
        return vm


class VirtualBlockDevice(BaseModel):

    def __init__(
            self, userdevice=None, runtime_properties=None,
            allowed_operations=None, uuid=None, storage_lock=None,
            qos_supported_algorithms=None, status_code=None,
            type=None, empty=None, status_detail=None, device=None,
            qos_algorithm_type=None, unpluggable=None,
            current_operations=None, bootable=None, other_config=None,
            currently_attached=None, mode=None, qos_algorithm_params=None):
        super(VirtualBlockDevice, self).__init__()
        self.userdevice = userdevice
        self.runtime_properties = runtime_properties
        self.allowed_operations = allowed_operations
        self.uuid = uuid
        self.storage_lock = storage_lock
        self.qos_supported_algorithms = qos_supported_algorithms
        self.status_code = status_code
        self.type = type
        self.empty = empty
        self.status_detail = status_detail
        self.device = device
        self.qos_algorithm_type = qos_algorithm_type
        self.unpluggable = unpluggable
        self.current_operations = current_operations
        self.bootable = bootable
        self.other_config = other_config
        self.currently_attached = currently_attached
        self.mode = mode
        self.qos_algorithm_params = qos_algorithm_params

    @classmethod
    def _dict_to_obj(cls, **kwargs):
        vbd = VirtualBlockDevice(
            userdevice=kwargs.get('userdevice'),
            runtime_properties=kwargs.get('runtime_properties'),
            allowed_operations=kwargs.get('allowed_operations'),
            uuid=kwargs.get('uuid'), storage_lock=kwargs.get('storage_lock'),
            qos_supported_algorithms=kwargs.get('qos_supported_algorithms'),
            status_code=kwargs.get('status_code'), type=kwargs.get('type'),
            empty=kwargs.get('empty'), device=kwargs.get('device'),
            status_detail=kwargs.get('status_detail'),
            qos_algorithm_type=kwargs.get('qos_algorithm_type'),
            unpluggable=kwargs.get('unpluggable'),
            current_operations=kwargs.get('current_operations'),
            bootable=kwargs.get('bootable'), mode=kwargs.get('mode'),
            other_config=kwargs.get('other_config'),
            currently_attached=kwargs.get('currently_attached'),
            qos_algorithm_params=kwargs.get('qos_algorithm_params'))
        return vbd


class VirtualDiskImage(BaseModel):

    def __init__(self, managed=None, snapshots=None, allowed_operations=None,
                 on_boot=None, description=None, read_only=None, uuid=None,
                 storage_lock=None, label=None, tags=None, location=None,
                 type=None, shareable=None, snapshot_time=None, missing=None,
                 xenstore_data=None, crash_dumps=None, virtual_size=None,
                 is_a_snapshot=None, current_operations=None,
                 physical_utilisation=None, allow_caching=None,
                 metadata_latest=None):
        super(VirtualDiskImage, self).__init__()
        self.managed = managed
        self.snapshots = snapshots
        self.allowed_operations = allowed_operations
        self.on_boot = on_boot
        self.description = description
        self.read_only = read_only
        self.uuid = uuid
        self.storage_lock = storage_lock
        self.label = label
        self.tags = tags
        self.location = location
        self.type = type
        self.shareable = shareable
        self.snapshot_time = snapshot_time
        self.missing = missing
        self.xenstore_data = xenstore_data
        self.crash_dumps = crash_dumps
        self.virtual_size = virtual_size
        self.is_a_snapshot = is_a_snapshot
        self.current_operations = current_operations
        self.physical_utilisation = physical_utilisation
        self.allow_caching = allow_caching
        self.metadata_latest = metadata_latest

    @classmethod
    def _dict_to_obj(cls, **kwargs):
        vdi = VirtualDiskImage(
            managed=kwargs.get('managed'), snapshots=kwargs.get('snapshots'),
            allowed_operations=kwargs.get('allowed_operations'),
            on_boot=kwargs.get('on_boot'), read_only=kwargs.get('read_only'),
            description=kwargs.get('description'), uuid=kwargs.get('uuid'),
            storage_lock=kwargs.get('storage_lock'), tags=kwargs.get('tags'),
            label=kwargs.get('label'), location=kwargs.get('location'),
            type=kwargs.get('type'), shareable=kwargs.get('shareable'),
            snapshot_time=kwargs.get('snapshot_time'),
            missing=kwargs.get('missing'),
            virtual_size=kwargs.get('virtual_size'),
            crash_dumps=kwargs.get('crash_dumps'),
            xenstore_data=kwargs.get('xenstore_data'),
            is_a_snapshot=kwargs.get('is_a_snapshot'),
            current_operations=kwargs.get('current_operations'),
            physical_utilisation=kwargs.get('physical_utilisation'),
            allow_caching=kwargs.get('allow_caching'),
            metadata_latest=kwargs.get('metadata_latest'))
        return vdi
