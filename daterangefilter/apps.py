from django.apps import AppConfig
try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    from django.utils.translation import gettext_lazy as _

class DateRangeFilterAppConfig(AppConfig):
    name = 'daterangefilter'
    verbose_name = _('Date Range Filter')
