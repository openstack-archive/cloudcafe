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
from datetime import datetime
from json import dumps as json_to_str
from cafe.engine.models.base import (AutoMarshallingModel,
                                     AutoMarshallingListModel)


class SystemInfo(AutoMarshallingModel):
    def __init__(self, disk_usage=None, os_type=None, memory_mb=None,
                 architecture=None, cpu_cores=None, load_average=None,
                 timestamp=None):
        super(SystemInfo, self).__init__()

        self.os_type = os_type
        self.memory_mb = memory_mb
        self.architecture = architecture
        self.cpu_cores = cpu_cores
        self.load_average = load_average
        self.disk_usage = disk_usage
        self.timestamp = timestamp

    def _obj_to_json(self):
        return json_to_str(self._obj_to_dict())

    def _obj_to_dict(self):
        return {
            'os_type': self.os_type,
            'memory_mb': self.memory_mb,
            'architecture': self.architecture,
            'cpu_cores': self.cpu_cores,
            'disk_usage': self.disk_usage._obj_to_dict(),
            'load_average': self.load_average._obj_to_dict(),
            'timestamp': self.timestamp or datetime.utcnow().isoformat()
        }

    @classmethod
    def _dict_to_obj(cls, dic):
        disk_usage = DiskUsage._dict_to_obj(dic.get('disk_usage'))
        load_average = LoadAverage._dict_to_obj(dic.get('load_average'))

        kwargs = {
            'os_type': dic.get('os_type'),
            'memory_mb': dic.get('memory_mb'),
            'architecture': dic.get('architecture'),
            'cpu_cores': dic.get('cpu_cores'),
            'disk_usage': disk_usage,
            'load_average': load_average,
            'timestamp': dic.get('timestamp')
        }
        return SystemInfo(**kwargs)


class LoadAverage(AutoMarshallingModel):

    def __init__(self, one_average=None, five_average=None,
                 fifteen_average=None):
        super(LoadAverage, self).__init__()

        self.one_average = one_average
        self.five_average = five_average
        self.fifteen_average = fifteen_average

    def _obj_to_dict(self):
        return {
            '1': self.one_average,
            '5': self.five_average,
            '15': self.fifteen_average
        }

    def _obj_to_json(self):
        return json_to_str(self._obj_to_dict())

    @classmethod
    def _dict_to_obj(cls, dic):
        kwargs = {
            'one_average': dic.get('1'),
            'five_average': dic.get('5'),
            'fifteen_average': dic.get('5')
        }
        return LoadAverage(**kwargs)


class DiskUsage(AutoMarshallingListModel):

    def _obj_to_dict(self):
        return [disk._obj_to_dict() for disk in self]

    def _obj_to_json(self):
        return json_to_str(self._obj_to_dict())

    @classmethod
    def _dict_to_obj(cls, json_dict):
        usage = cls()
        for disk in json_dict:
            part = Partition(name=disk.get('device'),
                             used=disk.get('used'),
                             total=disk.get('total'))
            usage.append(part)
        return usage


class Partition(AutoMarshallingModel):

    def __init__(self, name=None, total=None, used=None):
        super(Partition, self).__init__()

        self.name = name
        self.total = total
        self.used = used

    def _obj_to_dict(self):
        body = {
            'device': self.name,
            'total': self.total,
            'used': self.used
        }
        return body

    def _obj_to_json(self):
        return json_to_str(self._obj_to_dict())
