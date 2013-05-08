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

from urlparse import urlparse

from cafe.engine.clients.rest import AutoMarshallingRestClient
from cloudcafe.compute.common.datagen import rand_name
from cloudcafe.compute.common.models.metadata import Metadata
from cloudcafe.compute.common.models.metadata import MetadataItem
from cloudcafe.compute.servers_api.models.servers import Server
from cloudcafe.compute.servers_api.models.servers import Addresses
from cloudcafe.compute.servers_api.models.requests import CreateServer
from cloudcafe.compute.servers_api.models.requests import UpdateServer
from cloudcafe.compute.servers_api.models.requests import ChangePassword, \
    ConfirmResize, RevertResize, Resize, Reboot, MigrateServer, Lock, \
    Unlock, Start, Stop, Suspend, Resume, Pause, Unpause, CreateImage, \
    Rebuild, ResetState, CreateBackup


class ServersClient(AutoMarshallingRestClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
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
        super(ServersClient, self).__init__(serialize_format,
                                            deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def list_servers(self, name=None, image=None, flavor=None,
                     status=None, marker=None, limit=None, changes_since=None,
                     requestslib_kwargs=None):
        """
        @summary: Lists all servers with minimal details. Additionally,
         can filter results by params. Maps to /servers
        @param image: Image id to filter by
        @type image: String
        @param flavor: Flavor id to filter by
        @type flavor: String
        @param name: Server name to filter by
        @type name: String
        @param status: Server status to filter by
        @type status: String
        @param marker: Server id to be used as a marker for the next list
        @type marker: String
        @param limit: The maximum number of results to return
        @type limit: Int
        @param changes_since: Will only return servers where the updated time
         is later than the changes-since parameter.
        @return: resp
        @rtype: Requests.response
        """

        params = {'image': image, 'flavor': flavor, 'name': name,
                  'status': status, 'marker': marker,
                  'limit': limit, 'changes-since': changes_since}
        url = '%s/servers' % self.url
        resp = self.request('GET', url, params=params,
                            response_entity_type=Server,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_servers_with_detail(self, image=None, flavor=None, name=None,
                                 status=None, marker=None,
                                 limit=None, changes_since=None,
                                 requestslib_kwargs=None):
        """
        @summary: Lists all servers with full details. Additionally,
         can filter results by params. Maps to /servers/detail
        @param image: Image id to filter by
        @type image: String
        @param flavor: Flavor id to filter by
        @type flavor: String
        @param name: Server name to filter by
        @type name: String
        @param status: Server status to filter by
        @type status: String
        @param marker: Server id to be used as a marker for the next list
        @type marker: String
        @param limit: The maximum number of results to return
        @type limit: Int
        @param changes-since: Will only return servers where the updated time
         is later than the changes-since parameter.
        @return: resp
        @rtype: Requests.response
        """

        params = {'image': image, 'flavor': flavor, 'name': name,
                  'status': status, 'marker': marker, 'limit': limit,
                  'changes-since': changes_since}
        url = '%s/servers/detail' % self.url
        resp = self.request('GET', url, params=params,
                            response_entity_type=Server,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def get_server(self, server_id, requestslib_kwargs=None):
        """
        @summary: Retrieves the details of the specified server
        @param server_id: The id of an existing server
        @type server_id: String
        @return: resp
        @rtype: Requests.response
        """

        self.server_id = server_id
        url_new = str(server_id)
        url_scheme = urlparse(url_new).scheme
        url = url_new if url_scheme else '%s/servers/%s' % (self.url,
                                                            self.server_id)
        resp = self.request('GET', url,
                            response_entity_type=Server,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def delete_server(self, server_id, requestslib_kwargs=None):
        """
        @summary: Deletes the specified server
        @param server_id: The id of a server
        @type server_id: String
        @return: resp
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s' % (self.url, self.server_id)
        resp = self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def create_server(self, name, image_ref, flavor_ref, personality=None,
                      metadata=None, accessIPv4=None, accessIPv6=None,
                      disk_config=None, networks=None, admin_pass=None,
                      requestslib_kwargs=None):
        """
        @summary: Creates an instance of a server given the
         provided parameters
        @param name: Name of the server
        @type name: String
        @param image_ref: Identifier for the image used to build the server
        @type image_ref: String
        @param flavor_ref: Identifier for the flavor used to build the server
        @type flavor_ref: String
        @param metadata: A dictionary of values to be used as server metadata
        @type meta: Dictionary
        @param personality: A list of dictionaries for files to be
         injected into the server.
        @type personality: List
        @param accessIPv4: IPv4 address for the server.
        @type accessIPv4: String
        @param accessIPv6: IPv6 address for the server.
        @type accessIPv6: String
        @param disk_config: MANUAL/AUTO/None
        @type disk_config: String
        @return: Response Object containing response code and
         the server domain object
        @rtype: Requests.response
        """

        server_request_object = CreateServer(name=name, flavorRef=flavor_ref,
                                             imageRef=image_ref,
                                             personality=personality,
                                             metadata=metadata,
                                             accessIPv4=accessIPv4,
                                             accessIPv6=accessIPv6,
                                             diskConfig=disk_config,
                                             networks=networks,
                                             adminPass=admin_pass)

        url = '%s/servers' % self.url
        resp = self.request('POST', url,
                            response_entity_type=Server,
                            request_entity=server_request_object,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def update_server(self, server_id, name=None, metadata=None,
                      accessIPv4=None, accessIPv6=None,
                      requestslib_kwargs=None):
        """
        @summary: Updates the properties of an existing server.
        @param server_id: The id of an existing server.
        @type server_id: String
        @param name: The name of the server.
        @type name: String
        @param metadata: A dictionary of values to be used as metadata.
        @type metadata: Dictionary.
        @param accessIPv4: IPv4 address for the server.
        @type accessIPv4: String
        @param accessIPv6: IPv6 address for the server.
        @type accessIPv6: String
        @return: The response code and the updated Server
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s' % (self.url, self.server_id)
        request = UpdateServer(name=name, metadata=metadata,
                               accessIPv4=accessIPv4, accessIPv6=accessIPv6)
        resp = self.request('PUT', url,
                            response_entity_type=Server,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_addresses(self, server_id, requestslib_kwargs=None):
        """
        @summary: Lists all addresses for a server.
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Response code and the Addresses
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s/ips' % (self.url, self.server_id)
        resp = self.request('GET', url,
                            response_entity_type=Addresses,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_addresses_by_network(self, server_id, network_id,
                                  requestslib_kwargs=None):
        """
        @summary: Lists all addresses of a specific network type for a server.
        @param server_id: The id of an existing server.
        @type server_id: String
        @param network_id: The ID of a network.
        @type network_id: String
        @return: Response code and the Addresses by network.
        @rtype: Requests.response
        """

        self.server_id = server_id
        self.network_id = network_id
        url = '%s/servers/%s/ips/%s' % (self.url, self.server_id,
                                        self.network_id)
        resp = self.request('GET', url,
                            response_entity_type=Addresses,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def change_password(self, server_id, password, requestslib_kwargs=None):
        """
        @summary: Changes the root password for the server.
        @param server_id: The id of an existing server.
        @type server_id: String
        @param password: The new password.
        @type password: String.
        @return: Response Object containing response code and the empty
         body on success
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=ChangePassword(password),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def reboot(self, server_id, reboot_type, requestslib_kwargs=None):
        """
        @summary: Reboots the server - soft/hard based on reboot_type.
        @param server_id: The id of an existing server.
        @type server_id: String
        @param reboot_type: Soft or Hard.
        @type reboot_type: String.
        @return: Response Object containing response code and the empty body
        after the server reboot is applied
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=Reboot(reboot_type),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def rebuild(self, server_id, image_ref, name=None,
                admin_pass=None, disk_config=None, metadata=None,
                personality=None, accessIPv4=None, accessIPv6=None,
                requestslib_kwargs=None):
        """
        @summary: Rebuilds the server
        @param server_id: The id of an existing server.
        @type server_id: String
        @param name: The new name for the server
        @type name: String
        @param image_ref:The image ID.
        @type image_ref: String
        @param admin_pass:The administrator password
        @type admin_pass: String
        @param disk_config: The disk configuration value (AUTO or MANUAL)
        @type disk_config: String
        @param metadata:A metadata key and value pair.
        @type metadata: Dictionary
        @param personality:The file path and file contents
        @type personality: String
        @param accessIPv4:The IP version 4 address.
        @type accessIPv4: String
        @param accessIPv6:The IP version 6 address
        @type accessIPv6: String
        @return: Response Object containing response code and
         the server domain object
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        rebuild_request_object = Rebuild(name=name, image_ref=image_ref,
                                         admin_pass=admin_pass,
                                         disk_config=disk_config,
                                         metadata=metadata,
                                         personality=personality,
                                         accessIPv4=accessIPv4,
                                         accessIPv6=accessIPv6)

        resp = self.request('POST', url,
                            response_entity_type=Server,
                            request_entity=rebuild_request_object,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def resize(self, server_id, flavorRef, diskConfig=None,
               requestslib_kwargs=None):
        """
        @summary: Resizes the server to specified flavorRef.
        @param server_id: The id of an existing server.
        @type server_id: String
        @param flavorRef: The flavor id.
        @type flavorRef: String.
        @return: Response Object containing response code and
         the empty body after the server resize is applied
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resize_request_object = Resize(flavorRef, diskConfig)

        resp = self.request('POST', url,
                            request_entity=resize_request_object,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def confirm_resize(self, server_id, requestslib_kwargs=None):
        """
        @summary: Confirms resize of server
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Response Object containing response code and the empty
         body after the server resize is applied
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        confirm_resize_request_object = ConfirmResize()
        resp = self.request('POST', url,
                            request_entity=confirm_resize_request_object,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def revert_resize(self, server_id, requestslib_kwargs=None):
        """
        @summary: Reverts resize of the server
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Response Object containing response code and the empty body
         after the server resize is applied
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=RevertResize(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def migrate_server(self, server_id, requestslib_kwargs=None):
        """
        @summary: Migrates a server to a new host
        @param server_id: The id of the server to migrate
        @type server_id: String
        @return: An object that represents the response to the request
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=MigrateServer(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def live_migrate_server(self, server_id, requestslib_kwargs=None):
        """
        @summary: Migrates a server live to a new host
        @param server_id: The id of the server to migrate
        @type server_id: String
        @return: An object that represents the response to the request
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=MigrateServer(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def lock_server(self, server_id, requestslib_kwargs=None):
        """
        @summary: Locks an existing server
        @param server_id: The id of the server to lock
        @type server_id: String
        @return: An object that represents the response to the request
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=Lock(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def unlock_server(self, server_id, requestslib_kwargs=None):
        """
        @summary: Locks an existing server
        @param server_id: The id of the server to unlock
        @type server_id: String
        @return: An object that represents the response to the request
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=Unlock(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def stop_server(self, server_id, requestslib_kwargs=None):
        """
        @summary: Stops a server
        @param server_id: The id of the target server
        @type server_id: String
        @return: An object that represents the response to the request
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=Stop(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def start_server(self, server_id, requestslib_kwargs=None):
        """
        @summary: Starts a stopped server
        @param server_id: The id of the target server
        @type server_id: String
        @return: An object that represents the response to the request
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=Start(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def suspend_server(self, server_id, requestslib_kwargs=None):
        """
        @summary: Suspends a server
        @param server_id: The id of the target server
        @type server_id: String
        @return: An object that represents the response to the request
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=Suspend(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def resume_server(self, server_id, requestslib_kwargs=None):
        """
        @summary: Resumes a suspended server
        @param server_id: The id of the target server
        @type server_id: String
        @return: An object that represents the response to the request
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=Resume(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def pause_server(self, server_id, requestslib_kwargs=None):
        """
        @summary: Pauses a server
        @param server_id: The id of the target server
        @type server_id: String
        @return: An object that represents the response to the request
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=Pause(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def unpause_server(self, server_id, requestslib_kwargs=None):
        """
        @summary: Un-pauses a paused server
        @param server_id: The id of the target server
        @type server_id: String
        @return: An object that represents the response to the request
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=Unpause(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def reset_state(self, server_id, state='error',
                    requestslib_kwargs=None):
        """
        @summary: Resets a server's state
        @param server_id: The id of the target server
        @type server_id: String
        @param state: The state to reset the server to
        @type state: String
        @return: An object that represents the response to the request
        @rtype: Requests.response
        """

        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=ResetState(state),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def create_image(self, server_id, name=None, metadata=None,
                     requestslib_kwargs=None):
        """
        @summary: Creates snapshot of the server
        @param server_id: The id of an existing server.
        @type server_id: String
        @param: metadata: A metadata key and value pair.
        @type: Metadata Object
        @return: Response Object containing response code and the empty body
         after the server resize is applied
        @rtype: Requests.response
        """

        self.server_id = server_id
        if name is None:
            name = rand_name("TestImage")
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        create_image_request_object = CreateImage(name, metadata)
        resp = self.request('POST', url,
                            request_entity=create_image_request_object,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_server_metadata(self, server_id, requestslib_kwargs=None):
        """
        @summary: Returns metadata associated with an server
        @param server_id: server ID
        @type server_id:String
        @return: Metadata associated with an server on success
        @rtype: Requests.response
        """

        url = '%s/servers/%s/metadata' % (self.url, server_id)
        resp = self.request('GET', url,
                            response_entity_type=Metadata,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def set_server_metadata(self, server_id, metadata,
                            requestslib_kwargs=None):
        """
        @summary: Sets metadata for the specified server
        @param server_id: server ID
        @type server_id:String
        @param metadata: Metadata to be set for an server
        @type metadata: dictionary
        @return: Metadata associated with an server on success
        @rtype:  Requests.response
        """

        url = '%s/servers/%s/metadata' % (self.url, server_id)
        request_metadata_object = Metadata(metadata)
        self.request = self.request('PUT', url, response_entity_type=Metadata,
                                    request_entity=request_metadata_object,
                                    requestslib_kwargs=requestslib_kwargs)
        resp = self.request
        return resp

    def update_server_metadata(self, server_id, metadata,
                               requestslib_kwargs=None):
        """
        @summary: Updates metadata items for the specified server
        @param server_id: server ID
        @type server_id:String
        @param metadata: Metadata to be updated for an server
        @type metadata: dictionary
        @return: Metadata associated with an server on success
        @rtype:  Requests.response
        """

        url = '%s/servers/%s/metadata' % (self.url, server_id)
        request_metadata_object = Metadata(metadata)
        resp = self.request('POST', url,
                            response_entity_type=Metadata,
                            request_entity=request_metadata_object,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def get_server_metadata_item(self, server_id, key,
                                 requestslib_kwargs=None):
        """
        @summary: Retrieves a single metadata item by key
        @param server_id: server ID
        @type server_id:String
        @param key: Key for which metadata item needs to be retrieved
        @type key: String
        @return: Metadata Item for a key on success
        @rtype:  Requests.response
        """

        url = '%s/servers/%s/metadata/%s' % (self.url, server_id, key)
        resp = self.request('GET', url,
                            response_entity_type=MetadataItem,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def set_server_metadata_item(self, server_id, key, value,
                                 requestslib_kwargs=None):
        """
        @summary: Sets a metadata item for a specified server
        @param server_id: server ID
        @type server_id:String
        @param key: Key for which metadata item needs to be set
        @type key: String
        @return: Metadata Item for the key on success
        @rtype:  Requests.response
        """

        url = '%s/servers/%s/metadata/%s' % (self.url, server_id, key)
        request = MetadataItem({key: value})
        resp = self.request('PUT', url,
                            response_entity_type=MetadataItem,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def delete_server_metadata_item(self, server_id, key,
                                    requestslib_kwargs=None):
        """
        @summary: Sets a metadata item for a specified server
        @param server_id: server ID
        @type server_id:String
        @param key: Key for which metadata item needs to be set
        @type key: String
        @return: Metadata Item for the key on success
        @rtype:  Requests.response
        """

        url = '%s/servers/%s/metadata/%s' % (self.url, server_id, key)
        resp = self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def create_backup(self, server_id, backup_type, backup_rotation,
                      name=None, metadata=None, requestslib_kwargs=None):
        """
        @summary: Creates backup of the server
        @param server_id: The id of an existing server.
        @type server_id: String
        @param backup_type: The type of the backup, either daily or weekly.
        @type backup_type: String
        @param backup_rotation: Number of backups to maintain.
        @type backup_type: Integer
        @param: metadata: A metadata key and value pair.
        @type: Metadata Object
        @return: Response Object containing response code and the empty body
         after the server resize is applied
        @rtype: Requests.response
        """

        self.server_id = server_id
        if name is None:
            name = rand_name("TestBackup")
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        create_backup_request_object = CreateBackup(
            name, backup_type, backup_rotation, metadata)
        resp = self.request('POST', url,
                            request_entity=create_backup_request_object,
                            requestslib_kwargs=requestslib_kwargs)
        return resp
