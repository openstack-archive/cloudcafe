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


class VolumeMockResponse():

    def __init__(self, format):
        self.format = format

    def create_volume(self):
        return getattr(self, 'create_volume_{0}'.format(self.format))()

    def create_volume_json(self):
        return """
        {
    "volume": {
        "id": "521752a6-acf6-4b2d-bc7a-119f9148cd8c",
        "display_name": "vol-001",
        "display_description": "Another volume.",
        "size": 30,
        "volume_type": "289da7f8-6440-407c-9fb4-7db01ec49164",
        "metadata": {"contents": "junk"},
        "availability_zone": "us-east1",
        "snapshot_id": null,
        "attachments": [],
        "created_at": "2012-02-14T20:53:07Z"
     }
}
        """

    def create_volume_xml(self):
        return """
        <?xml version="1.0" encoding="UTF-8"?>
<volume xmlns="http://docs.openstack.org/volume/api/v1"
        id="521752a6-acf6-4b2d-bc7a-119f9148cd8c"
        display_name="vol-001"
        display_description="Another volume."
        status="active"
        size="30"
        volume_type="289da7f8-6440-407c-9fb4-7db01ec49164"
        availability_zone="us-east1"
        created_at="2012-02-14T20:53:07Z">
    <metadata>
        <meta key="contents">junk</meta>
    </metadata>
</volume>
        """

