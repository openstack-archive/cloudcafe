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

import time

from cafe.common.reporting import cclogging
from cafe.engine.clients.remote_instance.models.dir_details \
    import DirectoryDetails
from cafe.engine.clients.remote_instance.exceptions \
    import DirectoryNotFoundException
from cafe.engine.clients.remote_instance.models.file_details \
    import FileDetails
from cafe.engine.clients.ssh import SSHAuthStrategy, SSHBehaviors
from cloudcafe.compute.common.clients.ping import PingClient
from cloudcafe.compute.common.clients.remote_instance.base_client import \
    RemoteInstanceClient
from cloudcafe.compute.common.exceptions import FileNotFoundException, \
    ServerUnreachable, SshConnectionException


class LinuxClient(RemoteInstanceClient):

    def __init__(self, ip_address=None, username='root', password=None,
                 key=None, connection_timeout=600, retry_interval=10):
        self.client_log = cclogging.getLogger(
            cclogging.get_object_namespace(self.__class__))

        if ip_address is None:
            raise ServerUnreachable("None")
        self.ip_address = ip_address
        self.username = username
        self.password = password

        # Verify the server can be pinged before attempting to connect
        start = int(time.time())
        reachable = False
        while not reachable:
            reachable = PingClient.ping(ip_address)
            if reachable:
                break
            time.sleep(retry_interval)
            if int(time.time()) - start >= connection_timeout:
                raise ServerUnreachable(ip_address)

        if key is not None:
            auth_strategy = SSHAuthStrategy.KEY_STRING
        else:
            auth_strategy = SSHAuthStrategy.PASSWORD

        self.ssh_client = SSHBehaviors(
            username=self.username, password=self.password,
            host=self.ip_address, tcp_timeout=20, auth_strategy=auth_strategy,
            look_for_keys=False, key=key)
        self.ssh_client.connect_with_timeout(
            cooldown=20, timeout=connection_timeout)
        if not self.ssh_client.is_connected():
            message = ('SSH timeout after {timeout} seconds: '
                       'Could not connect to {ip_address}.')
            raise SshConnectionException(message.format(
                timeout=connection_timeout, ip_address=ip_address))

    def can_connect_to_public_ip(self):
        """
        @summary: Checks if you can connect to server using public ip
        @return: True if you can connect, False otherwise
        @rtype: bool
        """
        # This returns true since the connection has already been verified
        # in the init function

        return self.ssh_client.is_connected()

    def can_authenticate(self):
        """
        @summary: Checks if you can authenticate to the server
        @return: True if you can connect, False otherwise
        @rtype: bool
        """

        return self.ssh_client.is_connected()

    def get_hostname(self):
        """
        @summary: Gets the host name of the server
        @return: The host name of the server
        @rtype: string
        """

        output = self.ssh_client.execute_command("hostname")
        if output:
            return output.stdout.rstrip()

    def get_allocated_ram(self):
        """
        @summary: Returns the RAM size in MB
        @return: The RAM size in MB
        @rtype: string
        """

        output = self.ssh_client.execute_command('free -m | grep Mem')
        if output:
            return output.stdout.split()[1]

    def get_disk_size(self, disk_path):
        """
        @summary: Returns the disk size in GB
        @return: The disk size in GB
        @rtype: int
        """

        command = "df -h | grep '{disk_path}'".format(disk_path=disk_path)
        output = self.ssh_client.execute_command(command)
        if output is None:
            return None
        output = output.stdout
        size = output.split()[1]

        def is_decimal(char):
            return str.isdigit(char) or char == "."
        size = filter(is_decimal, size)
        return float(size)

    def get_number_of_cpus(self):
        """
        @summary: Get the number of vcpus assigned to the server
        @return: The number of vcpus assigned to the server
        @rtype: int
        """
        command = 'cat /proc/cpuinfo | grep processor | wc -l'
        output = self.ssh_client.execute_command(command)
        if output:
            return int(output.stdout)

    def get_partitions(self):
        """
        @summary: Returns the contents of /proc/partitions
        @return: The partitions attached to the instance
        @rtype: string
        """

        command = 'cat /proc/partitions'
        output = self.ssh_client.execute_command(command)
        if output:
            return output.stdout

    def get_uptime(self):
        """
        @summary: Get the uptime time of the server
        @return: The uptime of the server
        """

        result = self.ssh_client.execute_command('cat /proc/uptime')
        if result:
            uptime = float(result.stdout.split(' ')[0])
            return uptime

    def create_file(self, file_name, file_content, file_path=None):
        """
        @summary: Create a new file
        @param file_name: File Name
        @type file_name: String
        @param file_content: File Content
        @type file_content: String
        @return filedetails: File details such as content, name and path
        @rtype filedetails; FileDetails
        """

        if file_path is None:
            file_path = "/root/{file_name}".format(file_name=file_name)
        self.ssh_client.execute_command(
            'echo -n {file_content} >> {file_path}'.format(
                file_content=file_content, file_name=file_name))
        return FileDetails("644", file_content, file_path)

    def get_file_details(self, file_path):
        """
        @summary: Get the file details
        @param file_path: Path to the file
        @type file_path: string
        @return: File details including permissions and content
        @rtype: FileDetails
        """

        command = ('[ -f {file_path} ] && echo "File exists" || '
                   'echo "File does not exist"'.format(file_path=file_path))
        output = self.ssh_client.execute_command(command)
        if output is None:
            return None
        output = output.stdout

        if not output.rstrip('\n') == 'File exists':
            raise FileNotFoundException(
                "File {file_path} not found on instance.".format(
                    file_path=file_path))

        file_permissions = self.ssh_client.execute_command(
            'stat -c %a {file_path}'.format(
                file_path=file_path)).stdout.rstrip("\n")
        file_contents = self.ssh_client.execute_command(
            'cat {file_path}'.format(file_path=file_path)).stdout
        return FileDetails(file_permissions, file_contents, file_path)

    def is_file_present(self, file_path):
        """
        @summary: Check if the given file is present
        @param file_path: Path to the file
        @type file_path: string
        @return: True if File exists, False otherwise
        """

        command = ('[ -f {file_path} ] && echo "File exists" || '
                   'echo "File does not exist"'.format(file_path=file_path))
        output = self.ssh_client.execute_command(command).stdout
        if output:
            return output.rstrip('\n') == 'File exists'

    def mount_file_to_destination_directory(self, source_path,
                                            destination_path):
        """
        @summary: Mounts the file to destination directory
        @param source_path: Path to file source
        @type source_path: String
        @param destination_path: Path to mount destination
        @type destination_path: String
        """
        self.ssh_client.execute_command(
            'mount {source_path} {destination_path}'.format(
                source_path=source_path, destination_path=destination_path))

    def get_xen_user_metadata(self):
        command = 'xenstore-ls vm-data/user-metadata'
        output = self.ssh_client.execute_command(command)
        if not output:
            return None

        output = output.stdout
        meta_list = output.split('\n')
        meta = {}
        for item in meta_list:
            # Skip any blank lines
            if item:
                meta_item = item.split("=")
                key = meta_item[0].strip()
                value = meta_item[1].strip('" ')
                meta[key] = value
        return meta

    def get_xenstore_disk_config_value(self):
        """Returns the xenstore value for disk config (True/False)"""
        command = 'xenstore-read vm-data/auto-disk-config'
        output = self.ssh_client.execute_command(command)
        if output is None:
            return None
        output = output.stdout
        return output.strip().lower() == 'true'

    def create_directory(self, path):
        """
        @summary: Creates Directory
        @param path: Directory path
        @type path: string
        """
        command = "mkdir -p {path}".format(path=path)
        output = self.ssh_client.execute_command(command)
        if output is None:
            return None
        return output.stdout

    def is_directory_present(self, directory_path):
        """
        @summary: Check if directory is present
        @param directory_path: Path for the directory
        @type directory_path: string
        """
        cmd_str = "{0} {1} {2} {3} {4}"
        args = ["[ -d",
                directory_path,
                "] && echo 'Directory found' || echo 'Directory",
                directory_path, "not found'"]
        command = cmd_str.format(*args)
        output = self.ssh_client.execute_command(command)
        if output is None:
            return None
        output = output.stdout
        return output.rstrip('\n') == 'Directory found'

    def get_directory_details(self, dir_path):
        """
        @summary: Get the directory details
        @param dir_path: Path to the directory
        @type dir_path: string
        @return: Directory details including permissions and content
        @rtype: DirectoryDetails
        """
        output = self.is_directory_present(dir_path)
        if output is None:
            raise DirectoryNotFoundException(
                "Directory: {0} not found.".format(dir_path))
        dir_permissions = self.ssh_client.execute_command(
            "stat -c %a {0}".format(dir_path)).stdout.rstrip("\n")
        dir_size = float(self.ssh_client.execute_command(
            "du -s {0}".format(dir_path)).stdout.split('\t', 1)[0])
        return DirectoryDetails(dir_permissions, dir_size, dir_path)

    def get_block_devices(self):
        disks_raw = self.ssh_client.execute_command('lsblk -dn')
        if disks_raw is None:
            return None
        disks_raw = disks_raw.stdout
        disks_raw_list = disks_raw.split('\n')
        devices = []
        for disk in disks_raw_list:
            disk_params = disk.split()
            if disk_params:
                devices.append({'name': disk_params[0],
                                'size': disk_params[3]})
        return devices
