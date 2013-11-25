from cafe.engine.behaviors import BaseBehavior, behavior

from cloudcafe.compute.volume_attachments_api.client import \
    VolumeAttachmentsAPIClient
from cloudcafe.compute.volume_attachments_api.config import VolumeAttachmentsAPIConfig

from cloudcafe.blockstorage.v1.volumes_api.config import VolumesAPIConfig
from cloudcafe.blockstorage.v1.volumes_api.client import VolumesClient
from cloudcafe.blockstorage.v1.volumes_api.behaviors import \
    VolumesAPI_Behaviors
from cloudcafe.compute.servers_api.behaviors import ServerBehaviors
from time import sleep, time


class VolumeAttachmentBehaviorError(Exception):
    pass


class VolumeAttachmentsAPI_Behaviors(BaseBehavior):

    def __init__(
            self, volume_attachments_client=None, volumes_client=None,
            volume_attachments_config=None, volumes_config=None):

        self.volume_attachments_client = volume_attachments_client
        self.volume_attachments_config = volume_attachments_config or VolumesAPIConfig()
        self.volumes_config = volumes_config or VolumesAPIConfig()

        self.volumes_config = volumes_config or VolumesAPI_Behaviors(volumes_client)
        self.volumes_behaviors = VolumesAPI_Behaviors(volumes_client)

    @behavior(VolumeAttachmentsAPIClient)
    def wait_for_attachment_to_propagate(
            self, attachment_id, server_id, timeout=60, wait_period=5):

        endtime = time() + int(timeout)
        while time() < endtime:
            resp = \
                self.volume_attachments_client.get_volume_attachment_details(
                    attachment_id, server_id)
            if resp.ok:
                return True
            sleep(wait_period)
        else:
            return False

    @behavior(VolumeAttachmentsAPIClient, VolumesClient)
    def attach_volume(
            self, server_id, volume_id, device=None,
            expected_volume_status='in-use', volume_status_timeout=120,
            attachment_propagation_timeout=60):

        """Returns a VolumeAttachment object"""

        resp = self.volume_attachments_client.attach_volume(
            server_id, volume_id, device=device)

        if not resp.ok:
            raise VolumeAttachmentBehaviorError(
                msg="Volume attachment failed in auto_attach_volume_to_server"
                " with a {0}".format(resp.status_code))

        if resp.entity is None:
            raise VolumeAttachmentBehaviorError(
                msg="Volume attachment failed in auto_attach_volume_to_server."
                " Could not deserialize volume attachment response body")

        if str(resp.entity.volume_id) != str(volume_id):
            raise VolumeAttachmentBehaviorError(
                msg="Volume attachment failed in auto_attach_volume_to_server."
                "Volume attachment volume_id did not match expected volume_id")

        attachment = resp.entity

        #Confirm volume attachment propogation
        propagated = self.wait_for_attachment_to_propagate(
            attachment.id_, server_id, timeout=attachment_propagation_timeout)

        if not propagated:
            raise VolumeAttachmentBehaviorError(
                msg="Volume attachment {0} failed to propagate to the "
                "relevant cell within {1} seconds".format(
                    attachment.id_, server_id))

        # Confirm volume status
        confirmed_vol_status = self.volumes_behaviors.wait_for_volume_status(
            volume_id, expected_volume_status, volume_status_timeout)

        if not confirmed_vol_status:
            raise VolumeAttachmentBehaviorError(
                msg="Volume did not attain the {0} status within {1} seconds "
                " after being attached to a server")

        return attachment
