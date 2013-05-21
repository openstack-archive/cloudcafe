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


class HostsClientMockResponse(object):

    @classmethod
    def list_hosts(cls):
        return '{"hosts":[{' \
               '"host_name": "787f4f6dda1b409bb8b2f9082349690e",' \
               '"service": "compute",' \
               '"zone": "nova"},' \
               '"{host_name": "a98b433151084aee8b1a986e28823b36",' \
               '"service": "cert",' \
               '"zone": "internal"}]}'

    @classmethod
    def get_host(cls):
        return '{"host":' \
               ' [{"resource":' \
               ' {"cpu": 1,' \
               '"disk_gb": 1028,' \
               '"host": "787f4f6dda1b409bb8b2f9082349690e",' \
               '"memory_mb": 8192,"project": "(total)"}},' \
               '{"resource":' \
               ' {"cpu": 0,' \
               '"disk_gb": 0,' \
               '"host": "787f4f6dda1b409bb8b2f9082349690e",' \
               '"memory_mb": 512,' \
               '"project": "(used_now)"}}]}'
