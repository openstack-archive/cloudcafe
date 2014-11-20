import abc

from cafe.engine.clients.base import BaseClient


class RemoteInstanceClient(BaseClient):
    __metaclass__ = abc.ABCMeta

    def get_hostname(self):
        """Returns the machine's hostname."""
        raise NotImplementedError

    def get_allocated_ram(self):
        """Returns the amount of RAM in megabytes."""
        raise NotImplementedError

    def get_disk_size(self, disk_path):
        """Returns the size of the disk in gigabytes."""
        raise NotImplementedError

    def get_number_of_cpus(self):
        """Returns the number of CPUs the remote machine has."""
        raise NotImplementedError

    def get_uptime(self):
        """Returns the amount of time since the last reboot."""
        raise NotImplementedError

    def create_directory(self, path):
        """Creates a directory at the given path."""
        raise NotImplementedError

    def get_all_disks(self):
        """Returns a list of the physical disks available to the server."""
        raise NotImplementedError

    def mount_disk(self, source_path, destination):
        """Mounts a disk to a given path."""
        raise NotImplementedError

    def get_directory_details(self, dir_path):
        """Returns data about the given directory."""
        raise NotImplementedError

    def get_file_details(self, file_path):
        """Returns the permissions and contents of a file."""
        raise NotImplementedError

    def is_file_present(self, file_path):
        """Verifies that the file at the given path exists."""
        raise NotImplementedError

    def is_directory_present(self, dir_path):
        """Verifies that the given directory exists."""
        raise NotImplementedError

    def can_authenticate(self):
        """Verifies a remote connection can be made to the server."""
        raise NotImplementedError

    def get_distribution_and_version(self):
        """Gets the distribution and version of a server."""
        raise NotImplementedError
