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


class Constants:
    XML_HEADER = "<?xml version='1.0' encoding='UTF-8'?>"
    XML_API_NAMESPACE = ''


class TrafficGen(object):
    ACTUAL = 'actual'
    AH = 'atom_hopper'
    AH_BW_IN = 'bandWidthIn'
    AH_BW_OUT = 'bandWidthOut'
    AH_SSL_IN = 'bandWidthInSsl'
    AH_SSL_OUT = 'bandWidthOutSsl'
    ALLOWED = 'allowed'
    BANDWIDTH_ACCEPTANCE_RATIO = 0.20
    BYTES = 'bytes'
    DATA = 'data'
    DELETE_RECORD = 'delete'
    DIFFERENCE = 'difference'
    DIRECTION = 'direction'
    EXPECTED = 'expected'
    INTERVAL = 'interval'
    LB_ID = 'lb_id'
    PATH = 'path'
    POLL_TIME = 'poll_time'
    STATE = 'state'
    TEST_INFO = 'test_info'
    TRAFFIC_KEYS = ['bw_in', 'bw_out', 'ssl_in', 'ssl_out']
    TYPE = 'type'
    UPTIME = 'uptime'
    VALIDATION_ERROR = 'validation_error'


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
    DEFINED_PORTS = {'HTTP': 80, 'HTTPS': 443, 'FTP': 22, 'MYSQL': 3306,
                     'TCP': 8008, 'UDP': 32768, 'TCP_CLIENT_FIRST': 8008}
