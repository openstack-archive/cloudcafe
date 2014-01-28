from time import time, sleep

from cafe.engine.behaviors import behavior

from cloudcafe.common.tools.datagen import random_string
from cloudcafe.openstackcli.common.behaviors import (
    OpenstackCLI_BaseBehavior, OpenstackCLI_BehaviorError)
from cloudcafe.openstackcli.cindercli.client import CinderCLI
from cloudcafe.openstackcli.cindercli.config import CinderCLI_Config
from cloudcafe.blockstorage.volumes_api.v1.config import VolumesAPIConfig
from cloudcafe.blockstorage.volumes_api.v1.models import statuses


class CinderCLIBehaviorError(OpenstackCLI_BehaviorError):
    pass


class CinderCLI_Behaviors(OpenstackCLI_BaseBehavior):

    _default_error = CinderCLIBehaviorError

    def __init__(
            self, cinder_cli_client, cinder_cli_config=None,
            volumes_api_client=None, volumes_api_config=None):

        super(CinderCLI_Behaviors, self).__init__()
        self.client = cinder_cli_client
        self.config = cinder_cli_config or CinderCLI_Config()

        self.api_client = volumes_api_client
        self.api_config = volumes_api_config or VolumesAPIConfig()

    @behavior(CinderCLI)
    def create_available_volume(self, name=None, type_=None, size=None):
        name = random_string(prefix="Volume_", size=10)
        size = size or self.api_config.min_volume_size
        type_ = type_ or self.api_config.default_volume_type

        resp = self.client.create_volume(
            size=size, volume_type=type_, display_name=name)

        self.raise_on_error(resp, "Cinder CLI Volume Create call failed.")
        volume = resp.entity
        self.wait_for_volume_status(volume.id_, statuses.Volume.AVAILABLE)
        return volume

    @behavior(CinderCLI)
    def get_volume_status(self, volume_id):
        resp = self.client.show_volume(volume_id=volume_id)
        self.raise_on_error(resp, "Cinder CLI Show Volume call failed.")
        return resp.entity.status

    @behavior(CinderCLI)
    def wait_for_volume_status(
            self, volume_id, expected_status, timeout=None, poll_rate=None):
        """ Waits for a specific status and returns None when that status is
        observed.
        Note:  Unreliable for transient statuses like 'deleting'.
        """

        poll_rate = int(
            poll_rate or self.api_config.volume_status_poll_frequency)
        timeout = int(timeout or self.api_config.volume_create_timeout)
        end_time = time() + int(timeout)

        while time() < end_time:
            status = self.get_volume_status(volume_id)
            if status == expected_status:
                self._log.info(
                    "Expected Volume status '{0}' observed as expected".format(
                        expected_status))
                break
            sleep(poll_rate)

        else:
            msg = (
                "wait_for_volume_status() ran for {0} seconds and did not "
                "observe the volume attain the {1} status.".format(
                    timeout, expected_status))
            self._log.info(msg)
            raise self._default_error(msg)

    @behavior(CinderCLI)
    def list_volumes(self):
        resp = self.client.list_volumes

        self.raise_on_error(resp, "Unable to list volumes via the cinder cli")

        return resp.entity

    @behavior(CinderCLI)
    def delete_volume(self, volume_id):
        resp = self.client.delete_volume(volume_id)
        self.raise_if(
            self.is_process_error(resp),
            "Cinder CLI Volume Delete did not execute successfully")

    @behavior(CinderCLI)
    def delete_volume_confirmed(self, volume_id, timeout=60, poll_rate=5):
        self.delete_volume(volume_id)
        return self.wait_for_volume_delete(volume_id, timeout, poll_rate)

    @behavior(CinderCLI)
    def wait_for_volume_delete(
            self, volume_id, timeout=60, poll_rate=5):
        expected_err_msg = (
            "ERROR: No volume with a name or ID of '{0}' exists.".format(
                volume_id))
        end = time() + timeout
        while time() <= end:
            resp = self.client.show_volume(volume_id)
            if self.is_cli_error(resp) or self.is_process_error(resp):
                if resp.standard_error[-1] == expected_err_msg:
                    return True
            sleep(poll_rate)
        else:
            return False

# snapshots
    @behavior(CinderCLI)
    def list_snapshots(self):
        resp = self.client.list_snapshots

        self.raise_on_error(resp, "Unable to list snapshots via the cinder cli")

        return resp.entity

    @behavior(CinderCLI)
    def delete_snapshot(self, snapshot_id):
        resp = self.client.delete_snapshot()

        self.raise_if(
            self.is_process_error(resp),
            "Cinder CLI Snapshot Delete did not execute successfully")

    @behavior(CinderCLI)
    def get_snapshot_status(self, snapshot_id):
        resp = self.client.show_snapshot(snapshot_id=snapshot_id)
        self.raise_on_error(resp, "Cinder CLI snapshot-show call failed.")
        return resp.entity.status

    @behavior(CinderCLI)
    def list_volume_snapshot_ids(self, volume_id):
        snapshots = self.list_snapshots()
        return [snap.id_ for snap in snapshots if snap.volume_id == volume_id]

    @behavior(CinderCLI)
    def wait_for_snapshot_status(
            self, snapshot_id, expected_status, timeout, poll_rate=None):
        """ Waits for a specific status and returns None when that status is
        observed.
        Note:  Unreliable for transient statuses like 'deleting'.
        """

        poll_rate = int(
            poll_rate or self.api_config.snapshot_status_poll_frequency)
        end_time = time() + int(timeout)

        while time() < end_time:
            status = self.get_snapshot_status(snapshot_id)
            if status == expected_status:
                self._log.info(
                    "Expected snapshot status '{0}' observed as "
                    "expected".format(expected_status))
                break
            sleep(poll_rate)

        else:
            msg = (
                "wait_for_snapshot_status() ran for {0} seconds and did not "
                "observe the volume attain the {1} status.".format(
                    timeout, expected_status))
            self._log.info(msg)
            raise self._default_error(msg)

    @behavior(CinderCLI)
    def wait_for_snapshot_delete(self, snapshot_id, timeout=60, poll_rate=5):

        expected_err_msg = (
            "ERROR: No snapshot with a name or ID of '{0}' exists.".format(
                snapshot_id))

        end = time() + timeout
        while time() <= end:
            resp = self.client.show_snapshot(snapshot_id)
            if self.is_cli_error(resp) or self.is_process_error(resp):
                if resp.standard_error[-1] == expected_err_msg:
                    return True
            sleep(poll_rate)
        else:
            return False

# volume types
    @behavior(CinderCLI)
    def list_volume_types(self):
        resp = self.client.list_volume_types()
        self.raise_on_error(resp, "Unable to list snapshots via the cinder cli")
        return resp.entity
