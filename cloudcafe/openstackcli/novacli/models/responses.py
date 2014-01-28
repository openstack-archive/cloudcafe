# Used by models that inherit from an *Extensible* model
from cloudcafe.openstackcli.novacli.models.extensions import extensions

from cloudcafe.openstackcli.common.models.responses import (
    BaseExtensibleModel, BasePrettyTableResponseModel,
    BasePrettyTableResponseListModel)


class ServerResponse(BasePrettyTableResponseModel):

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


class _ServerListItem(BaseExtensibleModel):

    def __init__(
            self, id_=None, name=None, status=None, networks=None, **kwargs):

        super(_ServerListItem, self).__init__(**kwargs)
        self.id_ = id_
        self.name = name
        self.status = status
        self.networks = networks


class ServerListResponse(BasePrettyTableResponseListModel):

    @classmethod
    def _prettytable_str_to_obj(cls, prettytable_string):
        server_list_response = ServerListResponse()
        datatuple = cls._load_prettytable_string(prettytable_string)
        for datadict in datatuple:
            kwmap = {
                'id_': 'ID',
                'name': 'Name',
                'status': 'Status',
                'networks': 'Networks'}
            kwdict = cls._apply_kwmap(kwmap, datadict)
            server_list_response.append(_ServerListItem(**kwdict))
        return server_list_response
