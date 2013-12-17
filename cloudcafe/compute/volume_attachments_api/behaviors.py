from time import sleep, time
from cafe.engine.behaviors import BaseBehavior, behavior
from cloudcafe.compute.volume_attachments_api.client import \
    VolumeAttachmentsAPIClient
from cloudcafe.compute.volume_attachments_api.config import \
    VolumeAttachmentsAPIConfig
from cloudcafe.blockstorage.v1.volumes_api.client import VolumesClient
from cloudcafe.blockstorage.v1.volumes_api.config import VolumesAPIConfig
from cloudcafe.blockstorage.v1.volumes_api.behaviors import \
    VolumesAPI_Behaviors


class VolumeAttachmentBehaviorError(Exception):
    pass


class VolumeAttachmentsAPI_Behaviors(BaseBehavior):

    def __init__(
            self, volume_attachments_client=None, volumes_client=None,
            volume_attachments_config=None, volumes_config=None):

        self.client = volume_attachments_client
        self.config = volume_attachments_config or VolumeAttachmentsAPIConfig()

        self.volumes_client = volumes_client
        self.volumes_behaviors = VolumesAPI_Behaviors(volumes_client)
        self.volumes_config = volumes_config or VolumesAPIConfig()

    @behavior(VolumeAttachmentsAPIClient)
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

    @behavior(VolumesClient)
    def verify_volume_status_progression_during_attachment(
            self, volume_id, state_list=None):

        # (status, transient, timeout, poll_rate)
        state_list = [
            ('available', True, 5, 0),
            ('attaching', False, 30, 1),
            ('in-use', False, 60, 5)]

        self.volumes_behaviors.verify_volume_status_progression(
            volume_id, state_list)

    @behavior(VolumeAttachmentsAPIClient, VolumesClient)
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
