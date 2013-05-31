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

from time import time, sleep

from cafe.engine.behaviors import BaseBehavior, behavior
from cloudcafe.blockstorage.v1.volumes_api.client import VolumesClient
from cloudcafe.blockstorage.v1.volumes_api.config import VolumesAPIConfig
from cloudcafe.blockstorage.v1.volumes_api.models.statuses import \
    VolumeStatuses, SnapshotStatuses


class VolumesAPIBehaviorException(Exception):
    pass


class VolumesAPI_Behaviors(BaseBehavior):

    def __init__(self, volumes_api_client=None, volumes_api_config=None):
        super(VolumesAPI_Behaviors, self).__init__()
        self.client = volumes_api_client
        self.config = volumes_api_config or VolumesAPIConfig()

    @staticmethod
    def _calculate_timeout(
            size=None, timeout=None, min_timeout=None, max_timeout=None,
            wait_per_gb=None):

        if wait_per_gb is not None:
            if size is not None:
                timeout = timeout or size * wait_per_gb

        if min_timeout is not None:
            timeout = timeout if timeout > min_timeout else min_timeout

        if max_timeout is not None:
            timeout = timeout if timeout < max_timeout else max_timeout

        return timeout

    @behavior(VolumesClient)
    def wait_for_volume_status(
            self, volume_id, expected_status, timeout, wait_period=None):
        ''' Waits for a specific status and returns a BehaviorResponse object
        when that status is observed.
        Note:  Shouldn't be used for transient statuses like 'deleting'.
        '''
        wait_period = float(
            wait_period or self.config.volume_status_poll_frequency)
        end_time = time() + int(timeout)

        while time() < end_time:
            resp = self.client.get_volume_info(volume_id=volume_id)

            if not resp.ok:
                msg = (
                    "get_volume_info() call failed with status_code {0} "
                    "while waiting for volume to reach the {1} status".format(
                        resp.status_code, expected_status))
                self._log.error(msg)
                raise VolumesAPIBehaviorException(msg)

            if resp.entity is None:
                msg = (
                    "get_volume_info() response body did not deserialize.")
                self._log.error(msg)
                raise VolumesAPIBehaviorException(msg)

            if resp.entity.status == expected_status:
                self._log.info(
                    'Volume status "{0}" observed as expected'.format(
                        expected_status))
                break

            sleep(wait_period)

        else:
            msg = (
                "wait_for_volume_status() ran for {0} seconds and did not "
                "observe the volume attain the {1} status.".format(
                    timeout, expected_status))
            self._log.info(msg)
            raise VolumesAPIBehaviorException(msg)

    @behavior(VolumesClient)
    def wait_for_snapshot_status(
            self, snapshot_id, expected_status, timeout, wait_period=None):
        ''' Waits for a specific status and returns a BehaviorResponse object
        when that status is observed.
        Note:  Shouldn't be used for transient statuses like 'deleting'.
        '''
        wait_period = float(
            wait_period or self.config.snapshot_status_poll_frequency)
        end_time = time() + int(timeout)

        while time() < end_time:
            resp = self.client.get_snapshot_info(snapshot_id=snapshot_id)

            if not resp.ok:
                msg = (
                    "get_snapshot_info() call failed with status_code {0} "
                    "while waiting for snapshot status".format(
                        resp.status_code))
                self._log.error(msg)
                raise VolumesAPIBehaviorException(msg)

            if resp.entity is None:
                msg = (
                    "get_snapshot_info() response body did not deserialize as "
                    "expected")
                self._log.error(msg)
                raise VolumesAPIBehaviorException(msg)

            if resp.entity.status == expected_status:
                self._log.info('Snapshot status "{0}" observed'.format(
                    expected_status))
                break

            sleep(wait_period)

        else:
            msg = (
                "wait_for_snapshot_status() ran for {0} seconds and did not "
                "observe the snapshot achieving the '{1}' status.".format(
                    timeout, expected_status))
            self._log.error(msg)
            raise VolumesAPIBehaviorException(msg)

    @behavior(VolumesClient)
    def create_available_volume(
            self, display_name, size, volume_type, display_description=None,
            metadata=None, availability_zone=None, timeout=None):

        expected_status = VolumeStatuses.AVAILABLE
        metadata = metadata or {}

        timeout = self._calculate_timeout(
            size=size, timeout=timeout,
            max_timeout=self.config.volume_create_max_timeout)

        self._log.info("create_available_volume() is creating a volume")
        resp = self.client.create_volume(
            display_name=display_name, size=size, volume_type=volume_type,
            display_description=display_description, metadata=metadata,
            availability_zone=availability_zone)

        if not resp.ok:
            msg = (
                "create_available_volume() call failed with status_code {0} "
                "while attempting to create a volume".format(resp.status_code))
            self._log.error(msg)
            raise VolumesAPIBehaviorException(msg)

        if resp.entity is None:
            msg = (
                "create_available_volume() response body did not deserialize "
                "as expected")
            self._log.error(msg)
            raise VolumesAPIBehaviorException(msg)

        # Wait for expected_status on success
        self.wait_for_volume_status(resp.entity.id_, expected_status, timeout)

        return resp.entity

    @behavior(VolumesClient)
    def create_available_snapshot(
            self, volume_id, display_name=None, display_description=None,
            force_create='False', name=None, timeout=None):

        expected_status = SnapshotStatuses.AVAILABLE

        #Try and get volume size
        vol_size = None
        try:
            resp = self.client.get_volume_info(volume_id)
            #translate this to gigabytes
            vol_size = resp.entity.size
        except:
            pass

        timeout = self._calculate_timeout(
            size=vol_size, timeout=timeout,
            max_timeout=self.config.snapshot_create_max_timeout,
            min_timeout=self.config.snapshot_create_min_timeout,
            wait_per_gb=self.config.snapshot_create_wait_per_gigabyte)
        timeout += self.config.snapshot_create_base_timeout
        self._log.debug(
            "create_available_snapshot() timeout set to {0}".format(timeout))

        self._log.info("create_available_snapshot() is creating a snapshot")
        resp = self.client.create_snapshot(
            volume_id, display_name=display_name,
            display_description=display_description,
            force_create=force_create, name=name)

        if not resp.ok:
            msg = (
                "create_available_snapshot() call failed with status_code {0} "
                "while attempting to create a snapshot".format(
                    resp.status_code))
            self._log.error(msg)
            raise VolumesAPIBehaviorException(msg)

        if resp.entity is None:
            msg = (
                "create_available_volume() response body did not deserialize")
            self._log.error(msg)
            raise VolumesAPIBehaviorException(msg)

        # Wait for expected_status on success
        self.wait_for_snapshot_status(
            resp.entity.id_, expected_status, timeout)

        return resp.entity

    @behavior(VolumesClient)
    def list_volume_snapshots(self, volume_id):

        resp = self.client.list_all_snapshots_info()

        if not resp.ok:
            msg = (
                "list_volume_snapshots() failed to get a list of all snapshots"
                "due to a '{0}' response from list_all_snapshots_info()"
                .format(resp.status_code))
            self._log.error(msg)
            raise VolumesAPIBehaviorException(msg)

        if resp.entity is None:
            msg = (
                "list_all_snapshots_info() response body did not deserialize")
            self._log.error(msg)
            raise VolumesAPIBehaviorException(msg)

        # Expects an entity of type VolumeSnapshotList
        volume_snapshots = [s for s in resp.entity if s.volume_id == volume_id]
        return volume_snapshots

    @behavior(VolumesClient)
    def delete_volume_confirmed(
            self, volume_id, size=None, timeout=None, wait_period=None):
        '''Returns True if volume deleted, False otherwise'''

        timeout = self._calculate_timeout(
            size=size, timeout=timeout,
            min_timeout=self.config.volume_delete_min_timeout,
            max_timeout=self.config.volume_delete_max_timeout,
            wait_per_gb=self.config.volume_delete_wait_per_gigabyte)

        wait_period = float(
            wait_period or self.config.volume_status_poll_frequency)

        timeout_msg = (
            "delete_volume_confirmed() was unable to confirm the volume"
            "delete within the alloted {0} second timeout".format(timeout))

        end = time() + int(timeout)
        while time() < end:
            #issue DELETE request on volume
            resp = self.client.delete_volume(volume_id)
            if not resp.ok:
                msg = (
                    "delete_volume_confirmed() call to delete_volume() failed "
                    "with a '{0}'".format(resp.status_code))
                self._log.error(msg)
                return False
            else:
                break
        else:
            self._log.error(timeout_msg)
            return False

        #Contine where last timeout loop left off
        while time() < end:
            #Poll volume status to make sure it deleted properly
            status_resp = self.client.get_volume_info(volume_id)
            if status_resp.status_code == 404:
                self._log.info(
                    "Status request on volume {0} returned 404, volume delete"
                    "confirmed".format(volume_id))
                return True

            if not status_resp.ok and status_resp.status_code != 404:
                self._log.error(
                    "Status request on volume {0} failed with a {1}".format(
                        volume_id, status_resp.status_code))
                return False

            sleep(wait_period)

        else:
            self._log.error(timeout_msg)
            return False

    @behavior(VolumesClient)
    def delete_snapshot_confirmed(
            self, snapshot_id, vol_size=None, timeout=None, wait_period=None):
        '''Returns True if snapshot deleted, False otherwise'''

        timeout = self._calculate_timeout(
            size=vol_size, timeout=timeout,
            min_timeout=self.config.snapshot_delete_min_timeout,
            max_timeout=self.config.snapshot_delete_max_timeout,
            wait_per_gb=self.config.snapshot_delete_wait_per_gigabyte)

        wait_period = float(
            wait_period or self.config.snapshot_status_poll_frequency)

        timeout_msg = (
            "delete_snapshot_confirmed() was unable to confirm the snapshot "
            "deleted within the alloted {0} second timeout".format(timeout))

        end = time() + int(timeout)
        while time() < end:
            # issue DELETE request on volume snapshot
            resp = self.client.delete_snapshot(snapshot_id)

            if not resp.ok:
                msg = (
                    "delete_snapshot_confirmed() call to delete_snapshot()"
                    "failed with a '{0}'".format(resp.status_code))
                self._log.error(msg)
                return False
            else:
                break

            sleep(wait_period)
        else:
            self._log.error(timeout_msg)
            return False

        while time() < end:
            # Poll snapshot status to make sure it deleted properly
            status_resp = self.client.get_snapshot_info(snapshot_id)
            if status_resp.status_code == 404:
                self._log.info(
                    "Status request on snapshot {0} returned 404, snapshot"
                    "delete confirmed".format(snapshot_id))
                return True

            if not status_resp.ok and status_resp.status_code != 404:
                self._log.error(
                    "Status request on snapshot {0} failed with a {1}".format(
                        snapshot_id, resp.status_code))
                return False

            sleep(wait_period)
        else:
            self._log.error(timeout_msg)
            return False

    @behavior(VolumesClient)
    def delete_volume_with_snapshots_confirmed(self, volume_id):
        '''Returns True if volume deleted, False otherwise'''

        #Attempt to delete all snapshots associated with provided volume_id
        snapshots = self.list_volume_snapshots(volume_id)
        if snapshots is not None and len(snapshots) > 0:
            for snap in snapshots:
                if not self.delete_snapshot_confirmed(snap.id_):
                    self._log.warning(
                        "delete_volume_with_snapshots_confirmed() unable"
                        "to confirm delete of snapshot {0} for volume {1}."
                        "Still attempting to delete volume..."
                        .format(snap.id_, volume_id))

        if not self.delete_volume_confirmed(volume_id):
            self._log.warning(
                "delete_volume_with_snapshots_confirmed() unable to confirm"
                "delete of volume {0}.".format(volume_id))
            return False
        return True
