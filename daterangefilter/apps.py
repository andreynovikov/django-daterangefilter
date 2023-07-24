from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DateRangeFilterAppConfig(AppConfig):
    name = 'daterangefilter'
    verbose_name = _('Date Range Filter')
