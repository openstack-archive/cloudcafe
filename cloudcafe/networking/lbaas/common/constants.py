"""
Copyright 2014 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Constants for Neutron-LBaaS
"""


class Constants(object):
    XML_HEADER = "<?xml version='1.0' encoding='UTF-8'?>"
    XML_API_NAMESPACE = ''


class Algorithms(object):
    RR = 'ROUND_ROBIN'
    WRR = 'WEIGHTED_ROUND_ROBIN'
    LEAST_CONN = 'LEAST_CONNECTIONS'
    W_LEAST_CONN = 'WEIGHTED_LEAST_CONNECTIONS'
    RANDOM = 'RANDOM'


class Protocols(object):
    FTP = 'FTP'
    MYSQL = 'MYSQL'
    TCP = 'TCP'
    UDP = 'UDP'
    HTTP = 'HTTP'
    HTTPS = 'HTTPS'
    TCP_CLIENT_FIRST = 'TCP_CLIENT_FIRST'
    DEFINED_PORTS = {HTTP: 80, HTTPS: 443, FTP: 22, MYSQL: 3306,
                     TCP: 8008, UDP: 32768, TCP_CLIENT_FIRST: 8008}
