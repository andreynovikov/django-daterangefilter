import datetime

from django.utils import timezone
from django.template.loader import render_to_string
from django.test import RequestFactory, TestCase
from django.db import models
from django.contrib.admin import ModelAdmin, site
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.models import User
try:
    from django.utils.encoding import force_str
except:
    from django.utils.encoding import force_text as force_str

from .filters import DateRangeFilter, PastDateRangeFilter, FutureDateRangeFilter


class MyModel(models.Model):
    created_at = models.DateTimeField()
    publish_at = models.DateTimeField()
    review_at = models.DateTimeField()
    checked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']


class MyModelAdmin(ModelAdmin):
    list_filter = [
        ('created_at', PastDateRangeFilter),
        ('publish_at', FutureDateRangeFilter),
        ('review_at', DateRangeFilter),
        ('checked_at', PastDateRangeFilter),
    ]
    ordering = ['-id']


def select_by(dictlist):
    return [x for x in dictlist][0]


class DateRangeFilterTestCase(TestCase):
    def setUp(self):
        self.today = datetime.date.today()
        self.tomorrow = self.today + datetime.timedelta(days=1)
        self.one_week_ago = self.today - datetime.timedelta(days=7)

        self.object_one = MyModel.objects.create(
            created_at=timezone.now(),
            publish_at=timezone.now(),
            review_at=timezone.now(),
            checked_at=timezone.now()
        )
        self.object_two = MyModel.objects.create(
            created_at=timezone.now() - datetime.timedelta(days=7),
            publish_at=timezone.now(),
            review_at=timezone.now()
        )

        self.user = User.objects.create_user(username='test', password='top_secret')


    def get_changelist(self, request, model, modeladmin):
        if getattr(modeladmin, 'get_changelist_instance', None):
            return modeladmin.get_changelist_instance(request)

        return ChangeList(
            request, model, modeladmin.list_display,
            modeladmin.list_display_links, modeladmin.list_filter,
            modeladmin.date_hierarchy, modeladmin.search_fields,
            modeladmin.list_select_related, modeladmin.list_per_page,
            modeladmin.list_max_show_all, modeladmin.list_editable, modeladmin,
        )


    def test_get_template(self):
        self.request_factory = RequestFactory()
        modeladmin = MyModelAdmin(MyModel, site)

        request = self.request_factory.get('/')
        request.user = self.user

        changelist = self.get_changelist(request, MyModel, modeladmin)
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(filterspec.template, 'daterangefilter/daterangefilter.html')


    def test_datefilter(self):
        self.request_factory = RequestFactory()
        modeladmin = MyModelAdmin(MyModel, site)

        request = self.request_factory.get('/')
        request.user = self.user

        changelist = self.get_changelist(request, MyModel, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.object_two, self.object_one])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), 'created at')


    def test_datefilter_filtered(self):
        self.request_factory = RequestFactory()
        modeladmin = MyModelAdmin(MyModel, site)

        request = self.request_factory.get('/', {'created_at__gte': self.today,
                                                 'created_at__lte': self.tomorrow})
        request.user = self.user

        changelist = self.get_changelist(request, MyModel, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.object_one])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), 'created at')

        choice = select_by(filterspec.choices(changelist))
        self.assertEqual(choice['query_string'], '?')
        self.assertEqual(choice['field_name'], 'created_at')


    def test_datefilter_empty_values(self):
        self.request_factory = RequestFactory()
        modeladmin = MyModelAdmin(MyModel, site)

        request = self.request_factory.get('/', {'created_at__gte': '',
                                                 'created_at__lte': ''})
        request.user = self.user

        changelist = self.get_changelist(request, MyModel, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.object_two, self.object_one])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), 'created at')

        choice = select_by(filterspec.choices(changelist))
        self.assertEqual(choice['query_string'], '?')
        self.assertEqual(choice['field_name'], 'created_at')


    def test_datefilter_no_date(self):
        self.request_factory = RequestFactory()
        modeladmin = MyModelAdmin(MyModel, site)

        request = self.request_factory.get('/', {'checked_at__isnull': 'True'})
        request.user = self.user

        changelist = self.get_changelist(request, MyModel, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.object_two])
        filterspec = changelist.get_filters(request)[0][3]
        self.assertEqual(force_str(filterspec.title), 'checked at')

        choice = select_by(filterspec.choices(changelist))
        self.assertEqual(choice['query_string'], '?')
        self.assertEqual(choice['field_name'], 'checked_at')
        self.assertTrue(choice['nullable'])
        self.assertTrue(choice['no_date'])
        self.assertEqual(choice['value'], '')


    def test_datefilter_not_nullable(self):
        self.request_factory = RequestFactory()
        modeladmin = MyModelAdmin(MyModel, site)

        request = self.request_factory.get('/')
        request.user = self.user

        changelist = self.get_changelist(request, MyModel, modeladmin)
        filters = changelist.get_filters(request)[0]

        self.assertFalse(select_by(filters[0].choices(changelist))['nullable'])
        self.assertFalse(select_by(filters[0].choices(changelist))['no_date'])
        self.assertTrue(select_by(filters[3].choices(changelist))['nullable'])
        self.assertFalse(select_by(filters[3].choices(changelist))['no_date'])


    def test_datefilter_template_no_date(self):
        self.request_factory = RequestFactory()
        modeladmin = MyModelAdmin(MyModel, site)

        request = self.request_factory.get('/', {'checked_at__isnull': 'True'})
        request.user = self.user

        changelist = self.get_changelist(request, MyModel, modeladmin)
        filters = changelist.get_filters(request)[0]

        def render(filterspec):
            return render_to_string(filterspec.template, {
                'title': filterspec.title, 'choices': list(filterspec.choices(changelist))})

        nullable = render(filters[3])
        self.assertIn("options.ranges[noDate]", nullable)
        self.assertIn("'&checked_at__isnull=True'", nullable)
        self.assertIn("$drp_input.val(noDate);", nullable)
        not_nullable = render(filters[0])
        self.assertNotIn("options.ranges[noDate]", not_nullable)
        self.assertNotIn("$drp_input.val(noDate);", not_nullable)
