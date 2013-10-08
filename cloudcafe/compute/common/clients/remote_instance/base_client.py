import abc

from cafe.engine.clients.base import BaseClient

class RemoteInstanceClient(BaseClient):
    __metaclass__ = abc.ABCMeta

    def get_hostname(self):
        """Returns the machine's hostname."""
        pass

    def get_allocated_ram(self):
        """Returns the amount of RAM in megabytes."""
        pass

    def get_disk_size(self, disk_path):
        """Returns the size of the disk in gigabytes."""
        pass

    def get_number_of_cpus(self):
        """Returns the number of CPUs the remote machine has."""
        pass

    def get_uptime(self):
        """Returns the amount of time since the last reboot."""
        pass

    def create_directory(self, path):
        """Creates a directory at the given path."""
        pass

    def get_disks(self):
        """Returns a list of the physical disks available to the server."""
        pass

    def mount_file_to_destination_directory(self, source_path, destination):
        pass

    def get_directory_details(self, dirpath):
        pass

    def get_file_details(self, filepath):
        pass

    def is_file_present(self, filepath):
        pass

    def is_directory_present(self, dirpath):
        pass

    def can_connect_to_public_ip(self):
        pass

    def get_partition_details(self):
        pass

