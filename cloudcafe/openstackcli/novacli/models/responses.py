from cloudcafe.openstackcli.common.models.responses import \
    BasePrettyTableResponseModel, BasePrettyTableResponseListModel
from cloudcafe.openstackcli.novacli.models import extensions


class ExtendableResponseType(type):
    """Metaclass that registers relevant response extensions with
       inheriting Response classes"""
    def __new__(cls, class_name, parents, attrs):
        for ext in extensions.extensions:
            attrs[ext.__attrname__] = ext
        return super(ExtendableResponseType, cls).__new__(
            cls, class_name, parents, attrs)


class ExtendableResponse(BasePrettyTableResponseModel):
    __metaclass__ = ExtendableResponseType

    def __init__(self, *args, **kwargs):
        """Passes key word arguments from inheriting class to all relevant
        extensions, creating attributes for their values"""
        for ext in extensions.extensions:
            setattr(self, ext.__attrname__, ext(**kwargs))


class ServerResponse(ExtendableResponse):

    def __init__(
            self, status=None, updated=None, key_name=None, image=None,
            host_id=None, flavor=None, id_=None, user_id=None, name=None,
            admin_pass=None, tenant_id=None, created_at=None, access_ipv4=None,
            access_ipv6=None, progress=None, metadata=None,
            private_network=None, public_network=None, **kwargs):

        super(ServerResponse, self).__init__(**kwargs)
        self.status = status
        self.updated = updated
        self.key_name = key_name
        self.image = image
        self.host_id = host_id
        self.flavor = flavor
        self.id_ = id_
        self.user_id = user_id
        self.name = name
        self.admin_pass = admin_pass
        self.tenant_id = tenant_id
        self.created_at = created_at
        self.access_ipv4 = access_ipv4
        self.access_ipv6 = access_ipv6
        self.progress = progress
        self.metadata = metadata
        self.private_network = private_network
        self.public_network = public_network

    @classmethod
    def _prettytable_str_to_obj(cls, prettytable_string):
        kwdict = cls._property_value_table_to_dict(prettytable_string)
        kwmap = {
            'id_': 'id',
            'private_network': 'private network',
            'public_network': 'public network',
            'host_id': 'hostId',
            'access_ipv4': 'accessIPv4',
            'access_ipv6': 'accessIPv6',
            'admin_pass': 'adminPass'}

        kwdict = cls._apply_kwmap(kwmap, kwdict)
        return ServerResponse(**kwdict)

