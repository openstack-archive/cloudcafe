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

import json
import xml.etree.ElementTree as ET

from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.compute.common.constants import Constants
from cloudcafe.compute.common.models.metadata import Metadata


class CreateServer(AutoMarshallingModel):
    ROOT_TAG = 'server'

    def __init__(self, name, imageRef, flavorRef, adminPass=None,
                 diskConfig=None, metadata=None, personality=None,
                 accessIPv4=None, accessIPv6=None, networks=None):

        super(CreateServer, self).__init__()
        self.name = name
        self.imageRef = imageRef
        self.flavorRef = flavorRef
        self.diskConfig = diskConfig
        self.adminPass = adminPass
        self.metadata = metadata
        self.personality = personality
        self.accessIPv4 = accessIPv4
        self.accessIPv6 = accessIPv6
        self.networks = networks

    def _obj_to_json(self):
        body = {}
        body['name'] = self.name
        body['imageRef'] = self.imageRef
        body['flavorRef'] = self.flavorRef

        if self.diskConfig is not None:
            body['OS-DCF:diskConfig'] = self.diskConfig
        if self.adminPass is not None:
            body['adminPass'] = self.adminPass
        if self.metadata is not None:
            body['metadata'] = self.metadata
        if self.accessIPv4 is not None:
            body['accessIPv4'] = self.accessIPv4
        if self.accessIPv6 is not None:
            body['accessIPv6'] = self.accessIPv6
        if self.personality is not None:
            body['personality'] = self.personality
        if self.networks is not None:
            body['networks'] = self.networks

        return json.dumps({self.ROOT_TAG: body})

    def _obj_to_xml(self):
        element = ET.Element(self.ROOT_TAG)
        xml = Constants.XML_HEADER
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('name', self.name)
        element.set('imageRef', self.imageRef)
        element.set('flavorRef', self.flavorRef)
        if self.adminPass is not None:
            element.set('adminPass', self.adminPass)
        if self.diskConfig is not None:
            element.set('xmlns:OS-DCF',
                        Constants.XML_API_DISK_CONFIG_NAMESPACE)
            element.set('OS-DCF:diskConfig', self.diskConfig)
        if self.metadata is not None:
            meta_ele = ET.Element('metadata')
            for key, value in self.metadata.items():
                meta_ele.append(Metadata._dict_to_xml(key, value))
            element.append(meta_ele)
        if self.networks is not None:
            networks_ele = ET.Element('networks')
            for network_id in self.networks:
                network = ET.Element('network')
                network.set('uuid', network_id['uuid'])
                networks_ele.append(network)
            element.append(networks_ele)
        if self.personality is not None:
            personality_ele = ET.Element('personality')
            personality_ele.append(Personality._obj_to_xml(self.personality))
            element.append(personality_ele)
        if self.accessIPv4 is not None:
            element.set('accessIPv4', self.accessIPv4)
        if self.accessIPv6 is not None:
            element.set('accessIPv6', self.accessIPv6)
        xml += ET.tostring(element)
        return xml


class UpdateServer(AutoMarshallingModel):

    ROOT_TAG = 'server'

    def __init__(self, name=None, metadata=None,
                 accessIPv4=None, accessIPv6=None):
        self.name = name
        self.metadata = metadata
        self.accessIPv4 = accessIPv4
        self.accessIPv6 = accessIPv6

    def _obj_to_json(self):
        return json.dumps(self._auto_to_dict())

    def _obj_to_xml(self):
        element = ET.Element(self.ROOT_TAG)
        xml = Constants.XML_HEADER
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        if self.name is not None:
            element.set('name', self.name)
        if self.metadata is not None:
            meta_ele = ET.Element('metadata')
            for key, value in self.metadata.items():
                meta_ele.append(Metadata._dict_to_xml(key, value))
            element.append(meta_ele)
        if self.accessIPv4 is not None:
            element.set('accessIPv4', self.accessIPv4)
        if self.accessIPv6 is not None:
            element.set('accessIPv6', self.accessIPv6)
        xml += ET.tostring(element)
        return xml


class Reboot(AutoMarshallingModel):

    ROOT_TAG = 'reboot'

    def __init__(self, reboot_type):
        self.type = reboot_type

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('type', self.type)
        xml += ET.tostring(element)
        return xml


class Personality(AutoMarshallingModel):
    '''
    @summary: Personality Request Object for Server
    '''
    ROOT_TAG = 'personality'

    def __init__(self, type):
        self.type = type

    @classmethod
    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    @classmethod
    def _obj_to_xml(self, list_dicts):
        for pers_dict in list_dicts:
            pers_element = ET.Element('file')
            pers_element.set('path', pers_dict.get('path'))
            pers_element.text = pers_dict.get('contents')
        return pers_element


class Rebuild(CreateServer):
    """
    @summary: Rebuild Request Object for Server
    """

    ROOT_TAG = 'rebuild'

    def __init__(self, name, image_ref, admin_pass, disk_config=None,
                 metadata=None, personality=None, accessIPv4=None,
                 accessIPv6=None):
        super(Rebuild, self).__init__(name=name, imageRef=image_ref,
                                      flavorRef=None,
                                      adminPass=admin_pass,
                                      diskConfig=disk_config,
                                      metadata=metadata,
                                      personality=personality,
                                      accessIPv4=accessIPv4,
                                      accessIPv6=accessIPv6)


class Resize(AutoMarshallingModel):
    '''
    @summary: Resize Request Object for Server
    '''
    ROOT_TAG = 'resize'

    def __init__(self, flavorRef, diskConfig=None):
        self.flavorRef = flavorRef
        self.diskConfig = diskConfig

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('flavorRef', self.flavorRef)
        if self.diskConfig is not None:
            element.set('xmlns:OS-DCF', Constants.XML_API_ATOM_NAMESPACE)
            element.set('OS-DCF:diskConfig', self.diskConfig)
        xml += ET.tostring(element)
        return xml


class ResetState(AutoMarshallingModel):
    '''
    @summary: Reset State Request Object for Server
    '''
    ROOT_TAG = 'os-resetState'

    def __init__(self, state):
        self.state = state

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('state', self.state)
        xml += ET.tostring(element)
        return xml


class ConfirmResize(AutoMarshallingModel):
    '''
    @summary: Confirm Resize Request Object for Server
    '''
    ROOT_TAG = 'confirmResize'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        #        element = self._auto_to_xml()
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class RevertResize(AutoMarshallingModel):
    '''
    @summary: Revert Resize Request Object for Server

    '''
    ROOT_TAG = 'revertResize'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        #        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class MigrateServer(AutoMarshallingModel):
    '''
    @summary: Migrate Server Request Object
    '''
    ROOT_TAG = 'migrate'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class ConfirmServerMigration(AutoMarshallingModel):
    '''
    @summary: Confirm Server Migration Request Object
    '''
    ROOT_TAG = 'confirmResize'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Lock(AutoMarshallingModel):
    '''
    @summary: Lock Server Request Object
    '''
    ROOT_TAG = 'lock'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Unlock(AutoMarshallingModel):
    '''
    @summary: Unlock Server Request Object
    '''
    ROOT_TAG = 'unlock'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Start(AutoMarshallingModel):
    '''
    @summary: Start Server Request Object
    '''
    ROOT_TAG = 'os-start'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Stop(AutoMarshallingModel):
    '''
    @summary: Stop Server Request Object
    '''
    ROOT_TAG = 'os-stop'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Suspend(AutoMarshallingModel):
    '''
    @summary: Suspend Server Request Object
    '''
    ROOT_TAG = 'suspend'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Resume(AutoMarshallingModel):
    '''
    @summary: Resume Server Request Object
    '''
    ROOT_TAG = 'resume'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Pause(AutoMarshallingModel):
    '''
    @summary: Pause Server Request Object
    '''
    ROOT_TAG = 'pause'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Unpause(AutoMarshallingModel):
    '''
    @summary: Unpause Server Request Object
    '''
    ROOT_TAG = 'unpause'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class CreateImage(AutoMarshallingModel):
    '''
    Create Image Server Action Request Object
    '''
    ROOT_TAG = 'createImage'

    def __init__(self, name, metadata=None):
        self.name = name
        self.metadata = metadata

    def _obj_to_json(self):
        ret = self._auto_to_dict()

        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        element.set('name', self.name)
        if self.metadata is not None:
            meta_ele = ET.Element('metadata')
            for key, value in self.metadata.items():
                meta_ele.append(Metadata._dict_to_xml(key, value))
            element.append(meta_ele)
        xml += ET.tostring(element)
        return xml


class CreateBackup(AutoMarshallingModel):
    """
    Create Backup Server Action Request Object
    """
    ROOT_TAG = 'createBackup'

    def __init__(self, name, backup_type, backup_rotation, metadata=None):
        self.name = name
        self.backup_type = backup_type
        self.rotation = backup_rotation
        self.metadata = metadata

    def _obj_to_json(self):
        ret = self._auto_to_dict()

        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        element.set('name', self.name)
        element.set('backup_type', self.backup_type)
        element.set('rotation', self.rotation)
        if self.metadata is not None:
            meta_ele = ET.Element('metadata')
            for key, value in self.metadata.items():
                meta_ele.append(Metadata._dict_to_xml(key, value))
            element.append(meta_ele)
        xml += ET.tostring(element)
        return xml


class ChangePassword(AutoMarshallingModel):

    ROOT_TAG = 'changePassword'

    def __init__(self, adminPassword):
        self.adminPass = adminPassword

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('adminPass', self.adminPass)
        xml += ET.tostring(element)
        return xml


class AddFixedIP(AutoMarshallingModel):
    '''
    Add Fixed IP Action Request Object
    '''
    ROOT_TAG = 'addFixedIp'

    def __init__(self, networkId):
        self.networkId = networkId

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        #TODO: Implement when xml is known
        raise NotImplementedError


class RemoveFixedIP(AutoMarshallingModel):
    '''
    Remove Fixed IP Action Request Object
    '''
    ROOT_TAG = 'removeFixedIp'

    def __init__(self, networkId):
        self.networkId = networkId

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        #TODO: Implement when xml is known
        raise NotImplementedError
