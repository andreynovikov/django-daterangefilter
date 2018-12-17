import datetime

from django.db import models
from django.contrib import admin
from django.utils import timezone
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
            # if we are filtering DateTimeField we should add one day to final date
            if isinstance(model._meta.get_field(field_path), models.DateTimeField):
                gte_date = datetime.datetime.strptime(self.lookup_gte, '%Y-%m-%d')
                lte_date = datetime.datetime.strptime(self.lookup_lte, '%Y-%m-%d')
                lte_date = lte_date + datetime.timedelta(seconds=3600*24-1)
                if settings.USE_TZ:
                    gte_date = timezone.make_aware(gte_date, timezone.get_current_timezone())
                    lte_date = timezone.make_aware(lte_date, timezone.get_current_timezone())
                params[self.lookup_kwarg_gte] = gte_date.strftime('%Y-%m-%d %H:%M:%S%z')
                params[self.lookup_kwarg_lte] = lte_date.strftime('%Y-%m-%d %H:%M:%S%z')
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
            'ranges_template': self.ranges_template,
            'value': self.lookup_val,
            'query_string': changelist.get_query_string(remove=self._get_expected_fields())
        }

    def expected_parameters(self):
        return self._get_expected_fields()

    def _get_expected_fields(self):
        return [self.lookup_kwarg_gte, self.lookup_kwarg_lte]

    template = property(get_template)
    ranges_template = None


class FutureDateRangeFilter(DateRangeFilter):
    ranges_template = 'daterangefilter/_future_ranges.html'


class PastDateRangeFilter(DateRangeFilter):
    ranges_template = 'daterangefilter/_past_ranges.html'
