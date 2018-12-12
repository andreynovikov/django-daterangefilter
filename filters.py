from django.contrib import admin
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class DateRangeFilter(admin.FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field_name = field_path
        self.lookup_kwarg_gte = '{}__gte'.format(field_path)
        self.lookup_kwarg_lte = '{}__lte'.format(field_path)
        self.lookup_gte = params.get(self.lookup_kwarg_gte)
        self.lookup_lte = params.get(self.lookup_kwarg_lte)
        # todo: check if this is required in default admin
        if self.lookup_gte == '':
            params.pop(self.lookup_kwarg_gte)
        if self.lookup_lte == '':
            params.pop(self.lookup_kwarg_lte)
        if self.lookup_gte and self.lookup_lte:
            self.lookup_val = '{} - {}'.format(self.lookup_gte.replace('-','.'), self.lookup_lte.replace('-','.'))
        else:
            self.lookup_val = ''
        super(DateRangeFilter, self).__init__(field, request, params, model, model_admin, field_path)

    def get_template(self):
        if 'suit' in settings.INSTALLED_APPS:
            return 'daterangefilter/suit_daterangefilter.html'
        else:
            return 'daterangefilter/daterangefilter.html'

    def choices(self, changelist):
        yield {
            'field_name': self.field_path,
            'value': self.lookup_val,
            'query_string': changelist.get_query_string(remove=self._get_expected_fields())
        }

    def expected_parameters(self):
        return self._get_expected_fields()

    def _get_expected_fields(self):
        return [self.lookup_kwarg_gte, self.lookup_kwarg_lte]

    template = property(get_template)
