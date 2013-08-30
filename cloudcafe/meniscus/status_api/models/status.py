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
from json import loads as str_to_dict, dumps as dict_to_str
from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.meniscus.common.models.system \
    import SystemInfo, LoadAverage, DiskUsage


class WorkerStatus(AutoMarshallingModel):
    ROOT_TAG = 'status'

    def __init__(self, hostname, worker_id, ip_v4, ip_v6, personality, status,
                 system_info):
        super(WorkerStatus, self).__init__()
        self.hostname = hostname
        self.worker_id = worker_id
        self.ip_v4 = ip_v4
        self.ip_v6 = ip_v6
        self.personality = personality
        self.status = status
        self.system_info = system_info

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, json_dict):
        try:
            sys_info = SystemInfo._dict_to_obj(json_dict.get('system_info'))
        except:
            sys_info = 'Invalid System Info'
        args = {
            'hostname': json_dict.get('hostname'),
            'worker_id': json_dict.get('worker-id'),
            'ip_v4': json_dict.get('ip_address_v4'),
            'ip_v6': json_dict.get('ip_address_v6'),
            'personality': json_dict.get('personality'),
            'status': json_dict.get('status'),
            'system_info': sys_info
        }
        return WorkerStatus(**args)


class AllWorkersStatus(AutoMarshallingModel):
    ROOT_TAG = 'status'

    def __init__(self, workers=[]):
        super(AllWorkersStatus, self).__init__()
        self.workers = workers

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, json_dict):
        workers = [WorkerStatus._dict_to_obj(worker) for worker in json_dict]
        return AllWorkersStatus(workers)


class WorkerLoadAverage(LoadAverage):
    ROOT_TAG = 'load_average'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    def _obj_to_json(self):
        usage = super(WorkerLoadAverage, self)._obj_to_dict()
        return dict_to_str({'load_average': usage})


class WorkerDiskUsage(DiskUsage):
    ROOT_TAG = 'disk_usage'

    def __init__(self):
        super(WorkerDiskUsage, self).__init__()

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    def _obj_to_json(self):
        usage = super(WorkerDiskUsage, self)._obj_to_dict()
        return dict_to_str({'disk_usage': usage})


class WorkerStatusUpdate(AutoMarshallingModel):
    ROOT_TAG = 'worker_status'

    def __init__(self, status=None, system_info=None):
        super(WorkerStatusUpdate, self).__init__()

        self.status = status
        self.system_info = system_info

    def _obj_to_json(self):
        body = {
            "status": self.status,
            "system_info": self.system_info._obj_to_dict()
        }
        return dict_to_str({"worker_status": body})
