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

from time import time

from cafe.engine.behaviors import BaseBehavior, behavior
from cloudcafe.blockstorage.volumes_api.volumes_client import VolumesClient
from cloudcafe.blockstorage.volumes_api.config import VolumesAPIConfig


class BehaviorResponse(object):
    '''An object to represent the result of behavior.
    @ivar response: Last response returned from last client call
    @ivar ok: Represents the success state of the behavior call
    @type ok:C{bool}
    @ivar entity: Data model created via behavior calls, if applicable
    @TODO:  This should probably be moved to the base behavior module,
            or even into the engine's models
    '''
    def __init__(self):
        self.response = None
        self.ok = False
        self.entity = None


class VolumesAPI_Behaviors(BaseBehavior):

    def __init__(self, volumes_client=None):
        self._client = volumes_client
        self.config = VolumesAPIConfig()

    @behavior(VolumesClient)
    def wait_for_volume_status(
            self, volume_id, expected_status, timeout, wait_period=None):
        ''' Waits for a specific status and returns a BehaviorResponse object
        when that status is observed.
        Note:  Shouldn't be used for transient statuses like 'deleting'.
        '''
        wait_period = wait_period or self.config.volume_status_poll_frequency
        behavior_response = BehaviorResponse()
        end_time = time() + timeout

        while time() < end_time:
            resp = self._client.get_volume_info(volume_id=volume_id)
            behavior_response.response = resp
            behavior_response.entity = resp.entity

            if not resp.ok:
                behavior_response.ok = False
                self._log.error(
                    "get_volume_info() call failed with status_code {0} while "
                    "waiting for volume status".format(resp.status_code))
                break

            if resp.entity is None:
                behavior_response.ok = False
                self._log.error(
                    "get_volume_info() response body did not deserialize as "
                    "expected")
                break

            if resp.entity.status == expected_status:
                behavior_response.ok = True
                self._log.info('Volume status "{0}" observed'.format(
                    expected_status))
                break
        else:
            behavior_response.ok = False
            self._log.info(
                "wait_for_volume_status() ran for {0} seconds and did not "
                "observe the volume achieving the {1} status.".format(
                timeout, expected_status))

        return behavior_response

    @behavior(VolumesClient)
    def wait_for_snapshot_status(
            self, snapshot_id, expected_status, timeout, wait_period=None):
        ''' Waits for a specific status and returns a BehaviorResponse object
        when that status is observed.
        Note:  Shouldn't be used for transient statuses like 'deleting'.
        '''
        wait_period = wait_period or self.config.snapshot_status_poll_frequency
        behavior_response = BehaviorResponse()
        end_time = time() + timeout

        while time() < end_time:
            resp = self._client.get_snapshot_info(snapshot_id=snapshot_id)
            behavior_response.response = resp
            behavior_response.entity = resp.entity

            if not resp.ok:
                behavior_response.ok = False
                self._log.error(
                    "get_snapshot_info() call failed with status_code {0} "
                    "while waiting for snapshot status".format(
                        resp.status_code))
                break

            if resp.entity is None:
                behavior_response.ok = False
                self._log.error(
                    "get_snapshot_info() response body did not deserialize as "
                    "expected")
                break

            if resp.entity.status == expected_status:
                behavior_response.ok = True
                self._log.info('Snapshot status "{0}" observed'.format(
                    expected_status))
                break
        else:
            behavior_response.ok = False
            self._log.error(
                "wait_for_snapshot_status() ran for {0} seconds and did not "
                "observe the snapshot achieving the '{1}' status.".format(
                    timeout, expected_status))

        return behavior_response

    @behavior(VolumesClient)
    def create_available_volume(
            self, display_name, size, volume_type, display_description=None,
            metadata=None, availability_zone=None, timeout=None,
            wait_period=None):

        expected_status = 'available'
        metadata = metadata or {}
        timeout = timeout or self.config.volume_create_timeout
        behavior_response = BehaviorResponse()

        self._log.info("create_available_volume() is creating a volume")
        resp = self._client.create_volume(
            display_name=display_name, size=size, volume_type=volume_type,
            display_description=display_description, metadata=metadata,
            availability_zone=availability_zone)

        behavior_response.response = resp
        behavior_response.entity = resp.entity

        if not resp.ok:
            behavior_response.ok = False
            self._log.error(
                "create_available_volume() call failed with status_code {0} "
                "while attempting to create a volume".format(resp.status_code))

        if resp.entity is None:
            behavior_response.ok = False
            self._log.error(
                "create_available_volume() response body did not deserialize "
                "as expected")

        #Bail on fail
        if not behavior_response.ok:
            return behavior_response

        # Wait for expected_status on success
        wait_resp = self.wait_for_volume_status(
            resp.entity.id_, expected_status, timeout, wait_period)

        if not wait_resp.ok:
            behavior_response.ok = False
            self._log.error(
                "Something went wrong while create_available_volume() was "
                "waiting for the volume to reach the '{0}' status")
        else:
            behavior_response.ok = True

        return behavior_response

    @behavior(VolumesClient)
    def create_available_snapshot(
            self, volume_id, display_name=None, display_description=None,
            force_create='False', name=None, timeout=None, wait_period=None):

        expected_status = 'available'
        timeout = timeout or self.config.snapshot_create_timeout
        behavior_response = BehaviorResponse()

        self._log.info("create_available_snapshot() is creating a snapshot")
        resp = self._client.create_snapshot(
            volume_id, display_name=display_name,
            display_description=display_description,
            force_create=force_create, name=name)

        behavior_response.response = resp
        behavior_response.entity = resp.entity

        if not resp.ok:
            behavior_response.ok = False
            self._log.error(
                "create_available_volume() call failed with status_code {0} "
                "while attempting to create a volume".format(resp.status_code))

        if resp.entity is None:
            behavior_response.ok = False
            self._log.error(
                "create_available_volume() response body did not deserialize "
                "as expected")

        # Bail on fail
        if not behavior_response.ok:
            return behavior_response

        # Wait for expected_status on success
        wait_resp = self.wait_for_volume_status(
            resp.entity.id_, expected_status, timeout, wait_period)

        if not wait_resp.ok:
            behavior_response.ok = False
            self._log.error(
                "Something went wrong while create_available_volume() was "
                "waiting for the volume to reach the '{0}' status")
        else:
            behavior_response.ok = True

        return behavior_response

    @behavior(VolumesClient)
    def list_volume_snapshots(self, volume_id):
        behavior_response = BehaviorResponse()

        # List all snapshots
        resp = self._client.list_all_snapshots_info()
        behavior_response.response = resp
        behavior_response.entity = resp.entity

        if not resp.ok:
            behavior_response.ok = False
            self._log.error(
                "list_volume_snapshots() failed to get a list of all snapshots"
                "due to a '{0}' response from list_all_snapshots_info()"
                .format(resp.status_code))
            return behavior_response

        if resp.entity is None:
            behavior_response.ok = False
            self._log.error(
                "list_all_snapshots_info() response body did not deserialize "
                "as expected")
            return behavior_response

        # Expects an entity of type VolumeSnapshotList
        volume_snapshots = [s for s in resp.entity if s.volume_id == volume_id]
        behavior_response.entity = volume_snapshots

        return behavior_response

    @behavior(VolumesClient)
    def delete_volume_confirmed(
            self, volume_id, size=None, timeout=None, wait_period=None):

        if size is not None:
            if self.config.volume_delete_wait_per_gig is not None:
                wait_per_gig = self.config.volume_snapshot_delete_wait_per_gig
                timeout = timeout or size * wait_per_gig

        if self.config.volume_delete_min_timeout is not None:
            min_timeout = self.config.volume_snapshot_delete_min_timeout
            timeout = timeout if timeout > min_timeout else min_timeout

        if self.config.volume_delete_max_timeout is not None:
            max_timeout = self.config.volume_snapshot_delete_max_timeout
            timeout = timeout if timeout < max_timeout else max_timeout

        end = time() + timeout
        while time() < end:
            #issue DELETE request on volume
            behavior_response = BehaviorResponse()
            resp = self._client.delete_volume(volume_id)
            behavior_response.response = resp
            behavior_response.entity = resp.entity

            if not resp.ok:
                behavior_response.ok = False
                self._log.error(
                    "delete_volume_confirmed() call to delete_volume() failed "
                    "with a '{0}'".format(resp.status_code))
                return behavior_response

            #Poll volume status to make sure it deleted properly
            status_resp = self._client.get_volume_info(volume_id)
            if status_resp.status_code == 404:
                behavior_response.ok = True
                self._log.info(
                    "Status request on volume {0} returned 404, volume delete"
                    "confirmed".format(volume_id))
                break

            if (not status_resp.ok) and (status_resp.status_code != 404):
                behavior_response.ok = False
                self._log.error(
                    "Status request on volume {0} failed with a {0}".format(
                        volume_id))
                break
        else:
            behavior_response.ok = False
            self._log.error(
                "delete_volume_confirmed() was unable to verify the volume"
                "delete withing the alloted {0} second timeout".format())

        return behavior_response

    @behavior(VolumesClient)
    def delete_snapshot_confirmed(
            self, snapshot_id, size=None, timeout=None, wait_period=None):

        if size is not None:
            if self.config.volume_snapshot_delete_wait_per_gig is not None:
                wait_per_gig = self.config.volume_snapshot_delete_wait_per_gig
                timeout = timeout or size * wait_per_gig

        if self.config.volume_snapshot_delete_min_timeout is not None:
            min_timeout = self.config.volume_snapshot_delete_min_timeout
            timeout = timeout if timeout > min_timeout else min_timeout

        if self.config.volume_snapshot_delete_max_timeout is not None:
            max_timeout = self.config.volume_snapshot_delete_max_timeout
            timeout = timeout if timeout < max_timeout else max_timeout

        end = time() + timeout
        while time() < end:
            # issue DELETE request on volume snapshot
            behavior_response = BehaviorResponse()
            resp = self._client.delete_snapshot(snapshot_id)
            behavior_response.response = resp
            behavior_response.entity = resp.entity

            if not resp.ok:
                behavior_response.ok = False
                self._log.error(
                    "delete_snapshot_confirmed() call to delete_snapshot()"
                    "failed with a '{0}'".format(resp.status_code))
                return behavior_response

            # Poll snapshot status to make sure it deleted properly
            status_resp = self._client.get_snapshot_info(snapshot_id)
            if status_resp.status_code == 404:
                behavior_response.ok = True
                self._log.info(
                    "Status request on snapshot {0} returned 404, snapshot"
                    "delete confirmed".format(snapshot_id))
                break

            if not status_resp.ok and status_resp.status_code != 404:
                behavior_response.ok = False
                self._log.error(
                    "Status request on snapshot {0} failed with a {0}".format(
                        snapshot_id))
                break
        else:
            behavior_response.ok = False
            self._log.error(
                "delete_snapshot_confirmed() was unable to verify the snapshot"
                "was delete within the alloted {0} second timeout".format())

        return behavior_response

    @behavior(VolumesClient)
    def delete_volume_with_snapshots_confirmed(self, volume_id):
        behavior_response = BehaviorResponse()

        resp = self._client.list_all_snapshots_info()
        if not resp.status:
            self._log.error(
                "delete_volume_with_snapshots_confirmed() could not retrieve"
                "list of snapshots.  Expected 2XX but revieved {0}")

        #Attempt to delete all snapshots associated with provided volume_id
        snapshots = resp.entity
        if snapshots is not None:
            for snap in snapshots:
                if snap.volume_id != volume_id:
                    continue

                resp = self.delete_snapshot_confirmed(snap.id)

                if not resp.ok:
                    self._log.error(
                        "delete_volume_with_snapshots_confirmed() unable"
                        "to confirm delete of snapshot {0} for volume {1}."
                        .format(snap.id, volume_id))

        resp = self.delete_volume_confirmed(volume_id)
        behavior_response.ok = resp.ok
        behavior_response.response = resp
        if not resp.ok:
            self._log.error(
                "delete_volume_with_snapshots_confirmed() unable to confirm"
                "delete of volume {0}.".format(volume_id))

        return behavior_response
