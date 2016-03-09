from time import time, sleep

from cafe.engine.behaviors import BaseBehavior
from cloudcafe.common.behaviors import StatusProgressionVerifier


class VolumesAPIBehaviorException(Exception):
    pass


class VolumesAPI_CommonBehaviors(BaseBehavior):
    statuses = None

    def _verify_entity(self, resp):
        # Verify volume create call succeeded
        if not resp.ok:
            msg = "Call failed with status_code {0} ".format(resp.status_code)
            self._log.error(msg)
            raise VolumesAPIBehaviorException(msg)

        # Verify volume response entity deserialized correctly
        if resp.entity is None:
            msg = "Response body did not deserialize as expected"
            self._log.error(msg)
            raise VolumesAPIBehaviorException(msg)

        return resp.entity

    @staticmethod
    def _calculate_timeout(
            size=None, timeout=None, min_timeout=None, max_timeout=None,
            wait_per_gb=None):

        # Prevents comparison with None in min() and max()
        timeout = timeout or 0

        if wait_per_gb is not None and size is not None:
            timeout = timeout or size * wait_per_gb

        if min_timeout is not None:
            timeout = max(timeout, min_timeout)

        if max_timeout is not None:
            timeout = min(timeout, max_timeout)

        return timeout

    def calculate_volume_create_timeout(self, volume_size):
        timeout = self._calculate_timeout(
            size=volume_size,
            max_timeout=self.config.volume_create_max_timeout,
            min_timeout=self.config.volume_create_min_timeout,
            wait_per_gb=self.config.volume_create_wait_per_gigabyte)
        if not timeout:
            timeout = self.config.volume_create_base_timeout
        else:
            timeout += self.config.volume_create_base_timeout

        return timeout

    def calculate_volume_clone_timeout(self, original_volume_size):
        timeout = self._calculate_timeout(
            size=original_volume_size,
            max_timeout=self.config.volume_clone_max_timeout,
            min_timeout=self.config.volume_clone_min_timeout,
            wait_per_gb=self.config.volume_clone_wait_per_gigabyte)
        if not timeout:
            timeout = self.config.volume_clone_base_timeout
        else:
            timeout += self.config.volume_clone_base_timeout

        return timeout

    def calculate_copy_image_to_volume_timeout(self, image_size):
        timeout = self._calculate_timeout(
            size=image_size,
            max_timeout=self.config.copy_image_to_volume_max_timeout,
            min_timeout=self.config.copy_image_to_volume_min_timeout,
            wait_per_gb=self.config.copy_image_to_volume_wait_per_gigabyte)
        if not timeout:
            timeout = self.config.copy_image_to_volume_base_timeout
        else:
            timeout += self.config.copy_image_to_volume_base_timeout

        return timeout

    def calculate_snapshot_restore_timeout(self, image_size):
        timeout = self._calculate_timeout(
            size=image_size,
            max_timeout=self.config.snapshot_restore_max_timeout,
            min_timeout=self.config.snapshot_restore_min_timeout,
            wait_per_gb=self.config.snapshot_restore_wait_per_gigabyte)
        if not timeout:
            timeout = self.config.snapshot_restore_base_timeout
        else:
            timeout += self.config.snapshot_restore_base_timeout
        return timeout

    def calculate_snapshot_create_timeout(self, volume_size):
        timeout = self._calculate_timeout(
            size=volume_size,
            max_timeout=self.config.snapshot_create_max_timeout,
            min_timeout=self.config.snapshot_create_min_timeout,
            wait_per_gb=self.config.snapshot_create_wait_per_gigabyte)
        if not timeout:
            timeout = self.config.snapshot_create_base_timeout
        else:
            timeout += self.config.snapshot_create_base_timeout

        return timeout

    def calculate_snapshot_delete_timeout(self, original_volume_size):
        timeout = self._calculate_timeout(
            size=original_volume_size,
            max_timeout=self.config.snapshot_delete_max_timeout,
            min_timeout=self.config.snapshot_delete_min_timeout,
            wait_per_gb=self.config.snapshot_delete_wait_per_gigabyte)
        if not timeout:
            timeout = self.config.snapshot_delete_max_timeout
        else:
            timeout += self.config.snapshot_delete_base_timeout

        return timeout

    def create_volume(
            self, size, volume_type, name=None, description=None,
            availability_zone=None, metadata=None, bootable=None,
            image_ref=None, snapshot_id=None, source_volid=None):
        """This should be implemented by the inheriting class.  It's
        purpose is to hide the parameter name differences between the v1
        and v2 volumes api's for other methods in this behavior that
        also call create_volume."""
        raise NotImplementedError

    def create_snapshot(
            self, volume_id, name=None, description=None,
            force_create=False, requestslib_kwargs=None):
        """This should be implemented by the inheriting class.  It's
        purpose is to hide the parameter name differences between the v1
        and v2 volumes api's for other methods in this behavior that
        also call create_volume."""
        raise NotImplementedError

    def get_configured_volume_type_property(
            self, configured_property, id_=None, name=None):
        configured_data = self.config.volume_type_properties

        # Raise an exception if any of the configured data has null
        # values in it
        property_names = ["name", "id"]
        for entry in configured_data:
            for pname in property_names:
                if hasattr(entry, pname):
                    if entry.get(pname) is None:
                        raise Exception(
                            "Ambiguous volume type properties: 'null' value "
                            "found for configured volume type property '{0}'"
                            .format(pname))

            if name and str(entry.get('name') == str(name)):
                return entry.get(configured_property)
            if id_ is not None and str(entry.get('id')) == str(id_):
                return entry.get(configured_property)

    def get_volume_info(self, volume_id):
        resp = self.client.get_volume_info(volume_id=volume_id)
        self._verify_entity(resp)
        return resp.entity

    def get_volume_status(self, volume_id):
        return self.get_volume_info(volume_id).status

    def wait_for_volume_status(
            self, volume_id, expected_status, timeout, poll_rate=None):
        """ This method can end up polling for the entire timeout if the
        volume enters a permament unexpected state.
        It's been included for backwards compatibility only and should
        generally be avoided.
        """

        verifier = StatusProgressionVerifier(
            'volume', volume_id, self.get_volume_status, volume_id)

        verifier.set_global_state_properties(timeout)
        verifier.add_state(
            expected_statuses=[expected_status],
            poll_rate=self.config.volume_status_poll_frequency,
            poll_failure_retry_limit=(
                self.config.volume_status_poll_failure_max_retries))
        verifier.start()

    def get_snapshot_info(self, snapshot_id):
        resp = self.client.get_snapshot_info(snapshot_id=snapshot_id)
        self._verify_entity(resp)
        return resp.entity

    def get_snapshot_status(self, snapshot_id):
        return self.get_snapshot_info(snapshot_id).status

    def wait_for_snapshot_status(
            self, snapshot_id, expected_status, timeout, poll_rate=None):
        """ This method can end up polling for the entire timeout if the
        snapshot enters a permament unexpected state.
        It's been included for backwards compatibility only and should
        generally be avoided."""

        verifier = StatusProgressionVerifier(
            'snapshot', snapshot_id, self.get_snapshot_status, snapshot_id)

        verifier.set_global_state_properties(timeout)
        verifier.add_state(
            expected_statuses=[expected_status],
            poll_rate=self.config.snapshot_status_poll_frequency,
            poll_failure_retry_limit=(
                self.config.snapshot_status_poll_failure_max_retries))
        verifier.start()

    def create_available_volume(
            self, size, volume_type, name=None, description=None,
            availability_zone=None, metadata=None, bootable=None,
            image_ref=None, snapshot_id=None, source_volid=None, timeout=None):
        """Create a volume and wait for it to reach the 'available' status"""

        metadata = metadata or {}
        timeout = timeout or self.calculate_volume_create_timeout(size)

        try:
            if image_ref:
                timeout = self.calculate_copy_image_to_volume_timeout(size)
                self._log.info(
                    "Copy image to volume timeout calculated at {0} "
                    "seconds".format(timeout))

            elif snapshot_id:
                timeout = self.calculate_snapshot_restore_timeout(size)
                self._log.info(
                    "Create volume from snapshot timeout calculated at {0} "
                    "seconds".format(timeout))

            elif source_volid:
                timeout = self.calculate_volume_clone_timeout(size)
                self._log.info(
                    "Clone a volume timeout calculated at {0} "
                    "seconds".format(timeout))
        except:
            # Worst case if no config values are set.
            # Use the default volume create timeout.
            self._log.info(
                "Unable to use create-method-specific timeout, "
                "defaulting to normal volume create timeout of {0} "
                "seconds".format(timeout))

        start_time = time()
        resp = self.create_volume(
            size, volume_type, name=name, description=description,
            availability_zone=availability_zone, metadata=metadata,
            bootable=bootable, image_ref=image_ref, snapshot_id=snapshot_id,
            source_volid=source_volid)

        # Remove the time it took to create the volume from the total timeout
        timeout = timeout - (time() - start_time)

        # Verify volume progression from 'creating' to 'available'
        volume = self._verify_entity(resp)
        self.verify_volume_create_status_progresion(volume.id_, timeout)

        resp = self.client.get_volume_info(volume.id_)
        volume = self._verify_entity(resp)
        return volume

    def verify_volume_create_status_progresion(self, volume_id, timeout):
        """Raises an exception if the volume doesn't pass through
        the normal expected series of states for a volume create.
        """
        verifier = StatusProgressionVerifier(
            'volume', volume_id, self.get_volume_status, volume_id)

        verifier.set_global_state_properties(timeout)
        verifier.add_state(
            expected_statuses=[self.statuses.Volume.CREATING],
            acceptable_statuses=[self.statuses.Volume.AVAILABLE],
            error_statuses=[self.statuses.Volume.ERROR],
            poll_rate=self.config.volume_status_poll_frequency,
            poll_failure_retry_limit=(
                self.config.volume_status_poll_failure_max_retries))

        verifier.add_state(
            expected_statuses=[self.statuses.Volume.AVAILABLE],
            error_statuses=[self.statuses.Volume.ERROR],
            poll_rate=self.config.volume_status_poll_frequency,
            poll_failure_retry_limit=(
                self.config.volume_status_poll_failure_max_retries))

        verifier.start()

    def create_available_snapshot(
            self, volume_id, name=None, description=None, force_create=True,
            timeout=None):

        # Try and get volume size to calculate minimum wait time
        vol_size = None
        if not timeout:
            try:
                resp = self.client.get_volume_info(volume_id)
                self._verify_entity(resp)
                vol_size = resp.entity.size
            except:
                # If volume size isn't available, timeout defaults to
                # a non-optimized value
                pass
        timeout = self.calculate_snapshot_create_timeout(vol_size)
        self._log.debug(
            "create_available_snapshot() timeout set to {0}".format(timeout))

        # Create the snapshot
        self._log.info("create_available_snapshot is creating a snapshot")
        resp = self.create_snapshot(
            volume_id, force_create=force_create, name=name,
            description=description)
        snapshot = self._verify_entity(resp)

        # Verify snapshot status progression
        self.verify_snapshot_create_status_progression(snapshot.id_, timeout)

        # Return snapshot model
        resp = self.client.get_snapshot_info(snapshot.id_)
        snapshot = self._verify_entity(resp)
        return snapshot

    def verify_snapshot_create_status_progression(self, snapshot_id, timeout):
        verifier = StatusProgressionVerifier(
            'snapshot', snapshot_id, self.get_snapshot_status, snapshot_id)

        verifier.add_state(
            expected_statuses=[self.statuses.Snapshot.CREATING],
            acceptable_statuses=[self.statuses.Snapshot.AVAILABLE],
            error_statuses=[self.statuses.Snapshot.ERROR],
            timeout=self.config.snapshot_create_min_timeout,
            poll_rate=self.config.snapshot_status_poll_frequency,
            poll_failure_retry_limit=(
                self.config.snapshot_status_poll_failure_max_retries))
        verifier.add_state(
            expected_statuses=[self.statuses.Snapshot.AVAILABLE],
            error_statuses=[self.statuses.Snapshot.ERROR],
            timeout=timeout,
            poll_rate=self.config.snapshot_status_poll_frequency,
            poll_failure_retry_limit=(
                self.config.snapshot_status_poll_failure_max_retries))
        verifier.start()

    def list_volume_snapshots(self, volume_id):

        resp = self.client.list_all_snapshots_info()
        self._verify_entity(resp)

        # Expects an entity of type VolumeSnapshotList
        volume_snapshots = [s for s in resp.entity if s.volume_id == volume_id]
        return volume_snapshots

    def delete_volume_confirmed(
            self, volume_id, size=None, timeout=None, poll_rate=None):
        """Returns True if volume deleted, False otherwise"""

        timeout = self._calculate_timeout(
            size=size, timeout=timeout,
            min_timeout=self.config.volume_delete_min_timeout,
            max_timeout=self.config.volume_delete_max_timeout,
            wait_per_gb=self.config.volume_delete_wait_per_gigabyte)

        poll_rate = poll_rate or self.config.volume_status_poll_frequency

        timeout_msg = (
            "delete_volume_confirmed() was unable to confirm the volume"
            "delete within the alloted {0} second timeout".format(timeout))

        end = time() + timeout
        while time() < end:
            # issue DELETE request on volume
            resp = self.client.delete_volume(volume_id)

            if not resp.ok and resp.status_code not in [404, 400]:
                msg = (
                    "delete_volume_confirmed() call to delete_volume() failed "
                    "with a '{0}'".format(resp.status_code))
                self._log.error(msg)
                return False
            else:
                break
            sleep(poll_rate)
        else:
            self._log.error(timeout_msg)
            return False

        # Contine where last timeout loop left off
        while time() < end:
            # Poll volume status to make sure it deleted properly
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

            sleep(poll_rate)
        else:
            self._log.error(timeout_msg)
            return False

    def delete_snapshot_confirmed(
            self, snapshot_id, vol_size=None, timeout=None, poll_rate=None):
        """Returns True if snapshot deleted, False otherwise"""

        timeout = self.calculate_snapshot_delete_timeout(vol_size)
        poll_rate = poll_rate or self.config.snapshot_status_poll_frequency
        timeout_msg = (
            "delete_snapshot_confirmed() was unable to confirm the snapshot "
            "deleted within the alloted {0} second timeout".format(timeout))

        end = time() + timeout
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

            sleep(poll_rate)
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

            sleep(poll_rate)
        else:
            self._log.error(timeout_msg)
            return False

    def delete_volume_with_snapshots_confirmed(self, volume_id):
        """Returns True if volume deleted, False otherwise"""

        # Attempt to delete all snapshots associated with provided volume_id
        snapshots = self.list_volume_snapshots(volume_id)
        if snapshots:
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

    def get_volume_type_list(self):
        resp = self.client.list_all_volume_types()
        self._verify_entity(resp)
        return resp.entity

    def get_volume_list(self):
        resp = self.client.list_all_volumes()
        self._verify_entity(resp)
        return resp.entity

    def find_volume_by_name(self, volume_name):
        for v in self.get_volume_list():
            if v.name == volume_name:
                return v

    def find_volume_by_id(self, volume_id):
        for v in self.get_volume_list():
            if v.id_ == volume_id:
                return v

    def get_snapshot_list(self):
        resp = self.client.list_all_volumes()
        self._verify_entity(resp)
        return resp.entity
