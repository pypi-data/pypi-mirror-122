class ReadOnlyAdminMixin(object):
    """Disables all editing capabilities."""
    # change_form_template = "admin/view.html"

    # TODO: Bring this back after writing tests
    # def __init__(self, *args, **kwargs):
    #     super(ReadOnlyAdminMixin, self).__init__(*args, **kwargs)
    #     try:
    #         readonly_fields = self.model._meta.get_all_field_names()
    #     except AttributeError:
    #         readonly_fields = self.model._meta.get_fields()
    #     self.readonly_fields = readonly_fields

    def get_actions(self, request):
        actions = super(ReadOnlyAdminMixin, self).get_actions(request)
        if not self.has_delete_permission(request):
            del_action = "delete_selected"
            if del_action in actions:
                del actions[del_action]
        return actions

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False