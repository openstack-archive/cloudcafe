from time import sleep, time
from cafe.engine.behaviors import BaseBehavior
from cloudcafe.common.behaviors import StatusProgressionVerifier
from cloudcafe.compute.volume_attachments_api.config import \
    VolumeAttachmentsAPIConfig


class VolumeAttachmentBehaviorError(Exception):
    pass


class VolumeAttachmentsAPI_Behaviors(BaseBehavior):

    def __init__(
            self, volume_attachments_client=None,
            volume_attachments_config=None, volumes_client=None):

        self.client = volume_attachments_client
        self.config = volume_attachments_config or VolumeAttachmentsAPIConfig()
        self.volumes_client = volumes_client

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

    def verify_volume_status_progression_during_attachment(
            self, volume_id, state_list=None):

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

        verifier = StatusProgressionVerifier(
            'volume', volume_id, _get_volume_status, [self, volume_id])

        #verifier.add_state(status, timeout, pollrate, retries, transient)
        verifier.add_state('available', 30, 5, 3, True)
        verifier.add_state('attaching', 120, 5, 3, True)
        verifier.add_state('in-use', 30, 5, 3, False)
        verifier.start()

    def attach_volume_to_server(
            self, server_id, volume_id, device=None,
            attachment_propagation_timeout=60):
        """Returns a VolumeAttachment object"""

        attachment_propagation_timeout = (
            attachment_propagation_timeout
            or self.config.attachment_propagation_timeout)

        resp = self.client.attach_volume(server_id, volume_id, device=device)

        if not resp.ok:
            raise VolumeAttachmentBehaviorError(
                "Volume attachment failed in auto_attach_volume_to_server"
                " with a {0}. Could not attach volume {1} to server {2}"
                .format(resp.status_code, volume_id, server_id))

        if resp.entity is None:
            raise VolumeAttachmentBehaviorError(
                "Volume attachment failed in auto_attach_volume_to_server."
                " Could not deserialize volume attachment response body. Could"
                " not attach volume {1} to server {2}".format(
                    volume_id, server_id))

        attachment = resp.entity

        #Confirm volume attachment propagation
        propagated = self.wait_for_attachment_to_propagate(
            attachment.id_, server_id, timeout=attachment_propagation_timeout)

        if not propagated:
            raise VolumeAttachmentBehaviorError(
                "Volume attachment {0} belonging to server {1} failed to"
                "propagate to the relevant cell within {2} seconds".format(
                    attachment.id_, server_id, attachment_propagation_timeout))

        # Confirm volume status progression
        self.verify_volume_status_progression_during_attachment(volume_id)

        return attachment
