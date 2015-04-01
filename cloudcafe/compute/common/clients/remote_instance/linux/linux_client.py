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

import os
import re
import time

from cafe.common.reporting import cclogging
from cafe.engine.ssh.client import SSHAuthStrategy, SSHClient
from IPy import IP

from cloudcafe.common.tools import datagen
from cloudcafe.compute.common.clients.ping import PingClient
from cloudcafe.compute.common.clients.remote_instance.base_client import \
    RemoteInstanceClient
from cloudcafe.compute.common.exceptions import FileNotFoundException, \
    SshConnectionException, InvalidAddressFormat, DirectoryNotFoundException
from cloudcafe.compute.common.models.dir_details \
    import DirectoryDetails
from cloudcafe.compute.common.models.file_details \
    import FileDetails
from cloudcafe.common.tools.md5hash import get_md5_hash


class LinuxClient(RemoteInstanceClient):

    def __init__(self, ip_address=None, username='root', password=None,
                 key=None, connection_timeout=600, retry_interval=10):
        self.client_log = cclogging.getLogger(
            cclogging.get_object_namespace(self.__class__))

        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.connection_timeout = connection_timeout

        # Verify the IP address has a valid format
        try:
            IP(ip_address)
        except ValueError:
            raise InvalidAddressFormat(ip_address)

        # Verify the server can be pinged before attempting to connect
        PingClient.ping_until_reachable(ip_address,
                                        timeout=connection_timeout,
                                        interval_time=retry_interval)

        if key is not None:
            auth_strategy = SSHAuthStrategy.KEY_STRING
        else:
            auth_strategy = SSHAuthStrategy.PASSWORD

        allow_agent = True
        if not key:
            allow_agent = False

        self.ssh_client = SSHClient(
            username=self.username, password=self.password,
            host=self.ip_address, tcp_timeout=20, auth_strategy=auth_strategy,
            look_for_keys=False, key=key, allow_agent=allow_agent)
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

        disks = self.get_all_disks()
        return disks.get(disk_path)

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

    def get_local_users(self):
        """
        Get a list of the local user accounts on the server

        @return: A list of users
        @rtype: List of strings
        """

        command = 'cat /etc/passwd | cut -d: -f1'
        output = self.ssh_client.execute_command(command)
        if output:
            return output.stdout.split()

    def create_file(self, file_name, file_content, file_path=None):
        """
        Creates a new file with the provided content.

        @param file_name: File name
        @type file_name: string
        @param file_content: File content
        @type file_content: String
        @rtype: FileDetails
        """

        file_path = file_path or "/root"

        if not file_path.endswith("/"):
            file_path = "{0}/".format(file_path)

        file_path = "{0}{1}".format(file_path, file_name)

        self.ssh_client.execute_command(
            'echo -n {file_content} >> {file_path}'.format(
                file_content=file_content, file_path=file_path))

        return FileDetails("644", file_content, file_path)

    def create_large_file(self, filepath='/var/tmp/file.txt',
                          multiplier=1):
        """
        @summary: Creates a large file on the remote host
            with a base size in Gigabytes
        @param filepath: The filepath including filename
        @type filepath: String
        @param multiplier: A decimal number indicating the number of Gigabytes
            for example: 0.1 multiplier will create a 1.07374e8 byte file
        @type multiplier: Float
        @return: Data read from standard output during execution of the command
        @rtype: String
        """
        seek = int(1024 * 1024 * multiplier)
        cmd = ('dd if=/dev/zero of={0} count=0 bs=1024 seek={1} && '
               'echo "File created" || echo "File not created"'
               .format(filepath, str(seek)))
        output = self.ssh_client.execute_command(cmd).stdout
        return output.rstrip('\n') == 'File created'

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

    def generate_mountpoint(self, prefix=None):
        """
        Generates a string to use as a path for mounting drives on the
        remote linux os

        @param prefix:  Optional string to prepend to the mountpoint name
                        default prefix is 'mountpoint'
        @type source_path: string
        """

        return "/{0}".format(
            datagen.random_string(prefix=prefix or "mountpoint_"))

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

    def unmount_disk(self, disk_path):
        """
        Unmounts the disk at the specified location.

        @param disk_path: Path to file source
        @type disk_path: string
        """

        self.ssh_client.execute_command(
            'umount {disk_path}'.format(disk_path=disk_path))

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
        command = ("[ -d {path} ] && echo 'Directory found'"
                   "|| echo 'Directory {path} not found'".format(
                       path=directory_path))

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

    def get_all_disks(self):
        """
        Returns a list of all block devices for a server.

        @return: The accessible block devices
        @rtype: dict
        """

        disks_raw = self.ssh_client.execute_command('fdisk -l')
        if disks_raw is None:
            return None
        disks_raw = disks_raw.stdout
        p = re.compile('Disk /dev/\w+: \d+.*')
        disks_list = p.findall(disks_raw)

        disks = {}
        for disk in disks_list:
            items = disk.split()
            disk_name = items[1].replace(':', '')
            size = int(items[4])/(1 << 30)
            disks[disk_name] = size
        return disks

    def get_all_disk_details(self):
        """
        Returns a list of dictionaries, each containing the name,
        type, and size in bytes of all devices)

        @return: The accessible disks
        @rtype: list
        """
        disk_list = []
        info = self.ssh_client.execute_command(
            'lsblk -bio KNAME,TYPE,SIZE').stdout
        if info is None:
            return None
        info = info.splitlines()[1::]
        for line in info:
            group = re.split('\s*', line)
            if len(group) != 3:
                return None
            disk_list.append(
                {'name': group[0], 'type': group[1], 'size': group[2]})

        return disk_list

    def format_disk(self, disk, filesystem_type):
        """
        Formats a disk to the provided filesystem type.

        @param disk: The path to the disk to be formatted
        @type disk: string
        @param filesystem_type: The filesystem type to format the disk to
        @type filesystem_type: string

        @return: Output of command execution
        @rtype: string
        """

        out = self.ssh_client.execute_command('mkfs -t {type} {disk}'.format(
            type=filesystem_type, disk=disk))
        if out is None:
            return None
        return out.stdout

    def get_disk_fs_type(self, device_path):
        """ Expects full path to device like so: /dev/sda1
        Returns file system type as a string.
        """
        out = self.ssh_client.execute_command(
            'sudo lsblk -bio FSTYPE {0} -n'.format(device_path))
        if out is None:
            return None
        return out.stdout

    def get_md5sum_for_remote_file(self, file_location, file_name):
        """
        @summary: Gets the md5sum of file on the server
        @param filepath: The path name including file name
        @type filepath: String
        """
        output = self.ssh_client.execute_command('md5sum {0}/{1}'.format(
            file_location, file_name)).stdout
        if output:
            return output.split()[0]

    def get_network_bytes_for_interface(self, interface):
        """
        @summary: Retrieves the byte counters from a given network interface.
        @param interface: The network interface of an instance.
        @type interface: String
        @return: The received bytes and transmitted bytes
            from the network interface, respectively
        @rtype: Tuple
        """
        cmd = "ifconfig {0}".format(interface)
        output = self.ssh_client.execute_command(cmd).stdout
        rx_bytes = re.findall('RX bytes:([0-9]*) ', output)[0]
        tx_bytes = re.findall('TX bytes:([0-9]*) ', output)[0]
        return rx_bytes, tx_bytes

    def generate_bandwidth_from_server_to_client(self, public_ip_address,
                                                 gb_file_size, server_filepath,
                                                 client_filepath):
        """
        @summary: Creates and transfers a file from server to client
        @param linux_client: A linux client for a given instance
        @type address: Instance
        @param public_ip_address: The eth0 address of the instance
        @type public_ip_address: String
        @param gb_file_size: The size of the file to be generated in Gigabytes
        @type gb_file_size: Float
        @param server_filepath: The path name including file name on server
        @type server_filepath: String
        @param client_filepath: The path name including file name on client
        @type client_filepath: String
        @return: On successful bandwidth generation, return tx_bytes
        @rtype: int
        @todo: Use json bridge to poll global db for bw_usage_cache update
            instead of sleeping on ssh_timeout
        """
        time.sleep(self.connection_timeout)
        # delete same filename locally if it existed in a prior run
        if os.path.exists(client_filepath):
            os.remove(client_filepath)

        # get the initial values from the network interface
        rx_bytes, tx_bytes = self.get_network_bytes_for_interface('eth0')

        if not self.create_large_file(server_filepath, gb_file_size):
            raise Exception("File was not created on server: {0}, {1}"
                            .format(public_ip_address, server_filepath))

        server_filelocation, server_filename = os.path.split(server_filepath)

        md5sum_server = self.get_md5sum_for_remote_file(server_filelocation,
                                                        server_filename)
        if not md5sum_server:
            raise Exception("No md5sum from file on server: {0}, {1}"
                            .format(public_ip_address, server_filepath))

        if not self.ssh_client.retrieve_file_from(client_filepath,
                                                  server_filepath):
            raise Exception("The file {0} was not downloaded from "
                            "the server {1}, {2}".format(client_filepath,
                                                         public_ip_address,
                                                         server_filepath))

        md5sum_client = get_md5_hash(data=client_filepath,
                                     block_size_multiplier=16)
        if md5sum_server != md5sum_client:
            raise Exception("The md5sums did not match: {0}, {1} != {2}, {3}"
                            .format(md5sum_server, public_ip_address,
                                    md5sum_client, "localhost"))

        # clean up and delete the local file we just downloaded
        if os.path.exists(client_filepath):
            os.remove(client_filepath)

        # get the byte values after generating bandwidth and subtract
        rx_bytes_after, tx_bytes_after = (
            self.get_network_bytes_for_interface('eth0'))
        tx_bytes = int(tx_bytes_after) - int(tx_bytes)

        time.sleep(self.connection_timeout)
        return tx_bytes

    def check_rhel_activation(self):
        """
        @summary: Returns boolean - true or false depending of the activation
        if it is passed or failed
        @return: Activation status
        @rtype: bool
        """
        status_of_activation = False
        command = 'rhn_check -v'
        echo_call = 'echo $?'
        rhel_network_satellite = self.ssh_client.execute_command(command)
        if rhel_network_satellite.stdout is '':
            output = self.ssh_client.execute_command(echo_call)
            if int(output.stdout) is 0:
                status_of_activation = True
        return status_of_activation

    def get_distribution_and_version(self):
        """
        Get the distribution and version of the server
        Works for all Linux distibutions, not working for freebsd
        example root@ivo-ubuntu-2:~# lsb_release -d
            Description:    Ubuntu 12.04.4 LTS
        @return: Full name of the distibution
        @rtype: int
        """

        result = self.ssh_client.execute_command('lsb_release -d')
        if result:
            try:
                distro = result.stdout.split(':')[1]
                return distro
            except IndexError:
                result = self.ssh_client.execute_command('cat /etc/*-release |'
                                                         ' head -1')
                if result:
                    return result.stdout.split(':')[1]
                else:
                    return ''

    def filesystem_sync(self):
        self.ssh_client.execute_command('sync')
