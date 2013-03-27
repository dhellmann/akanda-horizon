from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _

from horizon import tables

from akanda.horizon.api import quantum_extensions_client


class Delete(tables.DeleteAction):
    name = 'delete'
    data_type_singular = _("Network")
    data_type_plural = _("Networks")
    success_url = reverse_lazy('horizon:project:networking:index')

    def delete(self, request, obj_id):
        quantum_extensions_client.networkalias_delete(request, obj_id)


class Create(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Alias")
    url = "horizon:project:networking:alias:networks:create"
    classes = ("ajax-modal", "btn-create")


class Edit(tables.LinkAction):
    name = "edit"
    verbose_name = _("Edit Alias")
    url = "horizon:project:networking:alias:networks:edit"
    classes = ("ajax-modal", "btn-edit")


class NetworkAliasTable(tables.DataTable):
    alias_name = tables.Column('alias_name', verbose_name=_("Alias Name"))
    cidr = tables.Column('cidr', verbose_name=_("CIDR"))

    class Meta:
        name = "networks"
        verbose_name = _("Network Aliases")
        table_actions = (Create, Delete,)
        row_actions = (Edit,)

    def get_object_display(self, datum):
        return datum.alias_name
