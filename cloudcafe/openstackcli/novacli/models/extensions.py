extensions = []


class ExtensionType(type):
    def __new__(cls, clsname, bases, attrs):
        extension = super(ExtensionType, cls).__new__(
            cls, clsname, bases, attrs)
        if extension.__alias__ and extension.__attrname__:
            extensions.append(extension)
        return extension


class Extension(object):
    __metaclass__ = ExtensionType
    __alias__ = None
    __attrname__ = None

    @classmethod
    def _get(cls, kwdict, string):
        alias_prefixed_kw = "{0}:{1}".format(cls.__alias__, string)
        return str(kwdict.get(alias_prefixed_kw)).strip() or None


class ExtendedStatus(Extension):
    __alias__ = 'OS-EXT-STS'
    __attrname__ = 'os_ext_sts'

    def __init__(self, **kwargs):
        self.task_state = self._get(kwargs, 'task_state')
        self.vm_state = self._get(kwargs, 'vm_state')
        self.power_state = self._get(kwargs, 'power_state')


class DiskConfig(Extension):
    __alias__ = 'OS-DCF'
    __attrname__ = 'os_dcf'

    def __init__(self, **kwargs):
        self.disk_config = self._get(kwargs, 'diskConfig')


class ConfigDrive(Extension):
    """Currently, this extension doesn't honor the alias pattern and instead
       names itself 'config_drive', meaning that this needs to return a string
       for compatability"""

    __alias__ = 'os-config-drive'
    __attrname__ = 'os_config_drive'

    def __new__(cls, **kwargs):
        return str(kwargs.get('config_drive')).strip() or None
