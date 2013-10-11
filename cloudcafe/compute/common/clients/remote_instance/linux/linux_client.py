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

    def can_authenticate(self):
        """
        Verifies that a connection was made to the remote server

        @return: Whether the connection was successful
        @rtype: bool
        """

        return self.ssh_client.is_connected()

    def get_hostname(self):
        """
        Gets the host name of the server

        @return: The host name of the server
        @rtype: string
        """

        output = self.ssh_client.execute_command("hostname")
        if output:
            return output.stdout.rstrip()

    def get_allocated_ram(self):
        """
        Returns the amount of RAM the server has

        @return: The RAM size in MB
        @rtype: string
        """

        output = self.ssh_client.execute_command('free -m | grep Mem')
        if output:
            return output.stdout.split()[1]

    def get_disk_size(self, disk_path):
        """
        Returns the size of a given disk

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
        Return the number of CPUs assigned to the server

        @return: The number of CPUs a server has
        @rtype: int
        """

        command = 'cat /proc/cpuinfo | grep processor | wc -l'
        output = self.ssh_client.execute_command(command)
        if output:
            return int(output.stdout)

    def get_uptime(self):
        """
        Get the uptime time of the server.

        @return: The uptime of the server in seconds
        @rtype: int
        """

        result = self.ssh_client.execute_command('cat /proc/uptime')
        if result:
            uptime = float(result.stdout.split(' ')[0])
            return uptime

    def create_file(self, file_name, file_content, file_path=None):
        """
        Creates a new file with the provided content.

        @param file_name: File name
        @type file_name: string
        @param file_content: File content
        @type file_content: String
        @rtype: FileDetails
        """

        if file_path is None:
            file_path = "/root/{file_name}".format(file_name=file_name)
        self.ssh_client.execute_command(
            'echo -n {file_content} >> {file_path}'.format(
                file_content=file_content, file_name=file_name))
        return FileDetails("644", file_content, file_path)

    def get_file_details(self, file_path):
        """
        Retrieves the contents of a file and its permissions.

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
        Verifies if the given file is present.

        @param file_path: Path to the file
        @type file_path: string
        @return: True if File exists, False otherwise
        @rtype: bool
        """

        command = ('[ -f {file_path} ] && echo "File exists" || '
                   'echo "File does not exist"'.format(file_path=file_path))
        output = self.ssh_client.execute_command(command).stdout
        if output:
            return output.rstrip('\n') == 'File exists'

    def mount_disk(self, source_path, destination_path):
        """
        Mounts a disk to specified destination.

        @param source_path: Path to file source
        @type source_path: string
        @param destination_path: Path to mount destination
        @type destination_path: string
        """

        self.ssh_client.execute_command(
            'mount {source_path} {destination_path}'.format(
                source_path=source_path, destination_path=destination_path))

    def get_xen_user_metadata(self):
        """
        Retrieves the user-metadata section from the XenStore.

        @return: The contents of the user-metadata
        @rtype: dict
        """

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
        """
        Returns the XenStore value for disk config.

        @return: Whether the virtual machine uses auto disk config
        @rtype: bool
        """
        command = 'xenstore-read vm-data/auto-disk-config'
        output = self.ssh_client.execute_command(command)
        if output is None:
            return None
        output = output.stdout
        return output.strip().lower() == 'true'

    def create_directory(self, path):
        """
        Creates a directory at the specified path.

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
        Check if given directory exists.

        @param directory_path: Path to the directory
        @type directory_path: string
        @return: Result of directory check
        @rtype: bool
        """
        cmd_str = "{0} {1} {2} {3} {4}"
        args = ["[ -d", directory_path,
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
        Retrieves informational data about a directory.

        @param dir_path: Path to the directory
        @type dir_path: string
        @return: Directory details
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
        """
        Returns a list of all block devices for a server.

        @return: The accessible block devices
        @rtype: list of dict
        """
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
