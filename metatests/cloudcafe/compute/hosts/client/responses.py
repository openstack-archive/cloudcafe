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


class HostsMockResponse():

    def __init__(self, format):
        self.format = format

    def list_hosts(self):
        return getattr(self, '_{0}_hosts'.format(self.format))()

    def get_host(self):
        return getattr(self, '_{0}_host'.format(self.format))()

    def _json_hosts(self):
        return ('{"hosts":[{'
                '"host_name": "787f4f6dda1b409bb8b2f9082349690e",'
                '"service": "compute",'
                '"zone": "nova"},'
                '"{host_name": "a98b433151084aee8b1a986e28823b36",'
                '"service": "cert",'
                '"zone": "internal"}]}')

    def _xml_hosts(self):
        return ('<?xml version="1.0" encoding="UTF-8"?>'
                '<hosts>'
                '<host host_name="461697a871354212908d82bbb0f9f5ee"'
                ' service="compute"/>'
                '<host host_name="272ab5d262994ebdaf228935c8ecf57e"'
                ' service="cert"/>'
                '<host host_name="2d1bdd671b5d41fd89dec74be5770c63"'
                ' service="network"/>'
                '<host host_name="7c2dd5ecb7494dd1bf4240b7f7f9bf3a"'
                ' service="scheduler"/>'
                '<host host_name="f9c273d8e03141a2a01def0ad18e5be4"'
                ' service="conductor"/>'
                '<host host_name="2b893569cd824b979bd80a2c94570a1f"'
                ' service="cells"/>'
                '</hosts>')

    def _xml_host(self):
        return ('<?xml version="1.0" encoding="UTF-8"?>'
                '<host>'
                '<resource>'
                '<project>(total)</project>'
                '<memory_mb>8192</memory_mb>'
                '<host>ecf3458ac6bf4a299cc2e0efa740f426</host>'
                '<cpu>1</cpu>'
                '<disk_gb>1028</disk_gb>'
                '</resource>'
                '</host>')

    def _json_host(cls):
        return ('{"host":'
                ' [{"resource":'
                ' {"cpu": 1,'
                '"disk_gb": 1028,'
                '"host": "787f4f6dda1b409bb8b2f9082349690e",'
                '"memory_mb": 8192,"project": "(total)"}},'
                '{"resource":'
                ' {"cpu": 0,'
                '"disk_gb": 0,'
                '"host": "787f4f6dda1b409bb8b2f9082349690e",'
                '"memory_mb": 512,'
                '"project": "(used_now)"}}]}')
