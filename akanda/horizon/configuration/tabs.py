import collections

from django.utils.translation import ugettext as _

from openstack_dashboard.api import quantum
from horizon import tabs

from akanda.horizon.configuration.tables.publicips import PublicIPsTable


# The table rendering code assumes it is getting an
# object with an "id" property and other properties
# based on the column definitions for the table.
# This is a light-weight data structure that looks
# like what we need for the publicips table.
PublicIP = collections.namedtuple('PublicIP', 'id router_name ipaddr')


class ConfigurationTab(tabs.TableTab):
    """Tab to show the user generic configuration settings.
    """
    name = _("Configuration")
    slug = "configuration_tab"
    template_name = "akanda/configuration/index.html"
    table_classes = (PublicIPsTable,)

    def get_publicips_data(self):
        data = []
        for router in quantum.router_list(
                self.request, tenant_id=self.request.user.tenant_id):
            router_info = quantum.router_get(self.request, router.id)
            for port in router_info.get('ports', []):
                if port.get('device_owner') != 'network:router_gateway':
                    continue
                ips = [i['ip_address'] for i in port.get('fixed_ips', [])]
                data.append(PublicIP(None, router.get('name'), ips))
        return data
