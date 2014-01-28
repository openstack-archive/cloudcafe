from cloudcafe.openstackcli.common.models.extensions import \
    ResponseExtensionType, SingleAttributeResponseExtension

# Extensions defined here are registered in this list
extensions = []


class OS_DCF_show(SingleAttributeResponseExtension):
    __extends__ = 'ServerResponse'
    key_name = 'OS-DCF:diskConfig'
    attr_name = 'disk_config'


class ConfigDrive(SingleAttributeResponseExtension):
    __extends__ = 'ServerResponse'
    key_name = 'config_drive'
    attr_name = 'config_drive'


class OS_EXT_STS_show(object):
    __metaclass__ = ResponseExtensionType
    __extends__ = 'ServerResponse'
    _prefix = 'OS-EXT-STS'
    _sub_attr_map = {
        'OS-EXT-STS:power_state': 'power_state',
        'OS-EXT-STS:task_state': 'task_state',
        'OS-EXT-STS:vm_state': 'vm_state'}

    def extend(cls, obj, **kwargs):
        if obj.__class__.__name__ not in cls.__extends__:
            return obj

        for kw_name, attr_name in cls._sub_attr_map.items():
            setattr(obj, attr_name, kwargs.get(kw_name, None))
        return obj


class OS_EXT_STS_list(object):
    __metaclass__ = ResponseExtensionType
    __extends__ = '_ServerListItem'
    _sub_attr_map = {
        'Power State': 'power_state',
        'Task State': 'task_state'}

    def extend(cls, obj, **kwargs):
        if obj.__class__.__name__ not in cls.__extends__:
            return obj

        for kw_name, attr_name in cls._sub_attr_map.items():
            setattr(obj, attr_name, kwargs.get(kw_name, None))
        return obj
