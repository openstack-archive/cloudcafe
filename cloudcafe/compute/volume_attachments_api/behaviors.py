from time import sleep, time
from cloudcafe.common.behaviors import (
    StatusProgressionVerifier, StatusProgressionVerifierError)
from cloudcafe.compute.common.behaviors import BaseComputeBehavior
from cloudcafe.compute.volume_attachments_api.config import \
    VolumeAttachmentsAPIConfig


class VolumeAttachmentBehaviorError(Exception):
    pass


class VolumeAttachmentsAPI_Behaviors(BaseComputeBehavior):

    def __init__(
            self, volume_attachments_client=None,
            volume_attachments_config=None, volumes_client=None):
        super(VolumeAttachmentsAPI_Behaviors, self).__init__()

        self.client = volume_attachments_client
        self.config = volume_attachments_config or VolumeAttachmentsAPIConfig()
        self.volumes_client = volumes_client

    def _validated_volume_attach(self, server_id, volume_id, device=None):
        """Performs a volume attach with response validation"""

        resp = self.client.attach_volume(server_id, volume_id, device=device)

        if not resp.ok:
            raise VolumeAttachmentBehaviorError(
                "Volume attachment failed in attach_volume_to_server "
                "with a '{0}'. Could not attach volume {1} to server {2}"
                .format(resp.status_code, volume_id, server_id))

        if resp.entity is None:
            raise VolumeAttachmentBehaviorError(
                "Volume attachment failed in auto_attach_volume_to_server. "
                "Could not deserialize volume attachment response body. "
                "Could not attach volume '{1}' to server '{2}'".format(
                    volume_id, server_id))

        return resp

    def _validated_volume_detach(self, attachment_id, server_id):

        resp = self.client.delete_volume_attachment(
            attachment_id, server_id)

        if not resp.ok:
            raise VolumeAttachmentBehaviorError(
                "Volume attachment DELETE failed in delete_volume_attachment "
                "with a {0}.  Could not delete attachment '{1}' on server "
                "'{2}'".format(resp.status_code, attachment_id, server_id))

        return resp

    def _get_volume_status(self, volume_id):
        resp = self.volumes_client.get_volume_info(volume_id=volume_id)
        if not resp.ok:
            msg = (
                "get_volume_status() failure:  get_volume_info() call"
                " failed with a {0} status code".format(resp.status_code))
            self._log.error(msg)
            raise Exception(msg)

        if resp.entity is None:
            msg = (
                "get_volume_status() failure:  unable to deserialize"
                " response from get_volume_info() call")
            self._log.error(msg)
            raise Exception(msg)

        return resp.entity.status

    def wait_for_attachment_to_propagate(
            self, attachment_id, server_id, timeout=None, poll_rate=5):

        timeout = timeout or self.config.attachment_propagation_timeout
        poll_rate = poll_rate or self.config.api_poll_rate
        endtime = time() + int(timeout)
        while time() < endtime:
            resp = self.client.get_volume_attachment_details(
                attachment_id, server_id)
            if resp.ok:
                return True
            sleep(poll_rate)
        else:
            return False

    def wait_for_attachment_to_delete(
            self, attachment_id, server_id, timeout=None, poll_rate=None):

        timeout = timeout or self.config.attachment_propagation_timeout
        poll_rate = poll_rate or self.config.api_poll_rate
        endtime = time() + int(timeout)

        while time() < endtime:
            resp = self.client.get_volume_attachment_details(
                attachment_id, server_id)
            if resp.status_code == 404:
                return None
            sleep(poll_rate)
        else:
            raise VolumeAttachmentBehaviorError(
                "Volume Attachment {0} still exists on server '{1}', {2} "
                "seconds after a successful DELETE. Could not verify that "
                "attachment was deleted.".format(
                    attachment_id, server_id, timeout))

    def verify_volume_status_progression_during_attachment(
            self, volume_id, state_list=None):

        verifier = StatusProgressionVerifier(
            'volume', volume_id, self._get_volume_status, volume_id)
        verifier.set_global_state_properties(
            timeout=self.config.attachment_timeout)

        verifier.add_state(
            expected_statuses=['available'],
            acceptable_statuses=['attaching', 'in-use'],
            error_statuses=['error', 'creating'],
            poll_rate=self.config.api_poll_rate,
            poll_failure_retry_limit=3)

        verifier.add_state(
            expected_statuses=['attaching'],
            acceptable_statuses=['in-use'],
            error_statuses=['error', 'creating'],
            poll_rate=self.config.api_poll_rate,
            poll_failure_retry_limit=3)

        verifier.add_state(
            expected_statuses=['in-use'],
            error_statuses=['available', 'error', 'creating'],
            poll_rate=self.config.api_poll_rate,
            poll_failure_retry_limit=3)

        verifier.start()

    def verify_volume_status_progression_during_detachment(
            self, volume_id, raise_on_error=True):
        """
        Track the status progression of volume volume_id being detached.

        Optionally fails silently if rais_on_error is set to False.
        :param volume_id: the uuid of the volume being tracked
        :returns: None
        """

        verifier = StatusProgressionVerifier(
            'volume', volume_id, self._get_volume_status, volume_id)
        verifier.set_global_state_properties(
            timeout=self.config.attachment_timeout)

        verifier.add_state(
            expected_statuses=['in-use'],
            acceptable_statuses=['detaching', 'available'],
            error_statuses=['error', 'attaching', 'creating', 'deleting'],
            poll_rate=self.config.api_poll_rate,
            poll_failure_retry_limit=3)

        verifier.add_state(
            expected_statuses=['detaching'],
            acceptable_statuses=['available'],
            error_statuses=['error', 'attaching', 'creating', 'deleting'],
            poll_rate=self.config.api_poll_rate,
            poll_failure_retry_limit=3)

        verifier.add_state(
            expected_statuses=['available'],
            error_statuses=[
                'error', 'attaching', 'creating', 'deleting', 'in-use'],
            poll_rate=self.config.api_poll_rate,
            poll_failure_retry_limit=3)

        try:
            verifier.start()
        except Exception as exception:
            if raise_on_error:
                raise exception

    def attach_volume_to_server(
            self, server_id, volume_id, device=None,
            attachment_propagation_timeout=60):
        """
        Performs response validation on attach call, confirms volume attachment
        propogation, and verifies volume status progression during the attach
        process.

        :rtype: VolumeAttachment model
        """

        attachment_propagation_timeout = (
            attachment_propagation_timeout
            or self.config.attachment_propagation_timeout)

        # Attach volume to server (validate response)
        resp = self._validated_volume_attach(server_id, volume_id, device)
        attachment = resp.entity

        # Confirm volume attachment propagation
        propagated = self.wait_for_attachment_to_propagate(
            attachment.id_, server_id, timeout=attachment_propagation_timeout)

        if not propagated:
            raise VolumeAttachmentBehaviorError(
                "Volume attachment '{0}' belonging to server '{1}' failed to "
                "propagate to the relevant cell within {2} seconds".format(
                    attachment.id_, server_id, attachment_propagation_timeout))

        # Confirm volume status progression
        self.verify_volume_status_progression_during_attachment(volume_id)

        return attachment

    def delete_volume_attachment(
            self, attachment_id, server_id, timeout=None, poll_rate=None):
        """Waits timeout seconds for volume attachment to 404 after issuing
        a delete to it.
        Raises exception on error.
        """
        self._validated_volume_detach(attachment_id, server_id)
        self.wait_for_attachment_to_delete(
            attachment_id, server_id, timeout, poll_rate)
