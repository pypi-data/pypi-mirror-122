from django.core.exceptions import FieldDoesNotExist
from django.utils.encoding import force_text

from corfmann.utils import verbose_name
from import_export import fields, resources


class ModelResource(resources.ModelResource):

    def _get_verbose_name(self, field):
        app_model_name = self._meta.model._meta.label
        return verbose_name(app_model_name, field.column_name)

    def get_export_headers(self):
        headers = []
        for field in self.get_export_fields():
            if field.attribute is None:
                headers.append(field.column_name)
            else:
                try:
                    headers.append(
                        force_text(self._get_verbose_name(field))
                    )
                except FieldDoesNotExist:
                    headers.append(field.column_name)
        return headers
