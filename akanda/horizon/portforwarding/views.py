from django.utils.translation import ugettext as _

from horizon import exceptions
from horizon import workflows

from akanda.horizon.api import neutron_extensions_client
from akanda.horizon.portforwarding.workflows import (
    PortForwardingRule, EditPortForwardingRule)


class CreatePortForwardingRuleView(workflows.WorkflowView):
    workflow_class = PortForwardingRule


class EditPortForwardingRuleView(workflows.WorkflowView):
    workflow_class = EditPortForwardingRule

    def _get_object(self, ):
        if not hasattr(self, "_object"):
            try:
                self._object = neutron_extensions_client.portforward_get(
                    self.request, self.kwargs['portforward_rule_id'])
            except:
                msg = _('Unable to retrieve firewall rule.')
                redirect = self.get_success_url()
                exceptions.handle(self.request, msg, redirect=redirect)
        return self._object

    def get_context_data(self, **kwargs):
        context = super(EditPortForwardingRuleView,
                        self).get_context_data(**kwargs)
        context['portforward_rule_id'] = self._get_object()
        return context

    def get_initial(self):
        rule = self._get_object()
        initial_data = {'id': self.kwargs['portforward_rule_id'],
                        'rule_name': rule['name'],
                        'instance': rule['port']['device_id'],
                        'public_protocol': rule['protocol'],
                        'public_port': rule['public_port'],
                        'private_protocol': rule['protocol'],
                        'private_port': rule['private_port'],
                        }

        return initial_data
