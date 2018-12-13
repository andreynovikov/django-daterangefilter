# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime

from django.utils import timezone
from django.test import RequestFactory, TestCase
from django.test.utils import override_settings
from django.db import models
from django.contrib.admin import ModelAdmin, site
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.models import User
from django.utils.encoding import force_text

from .filters import DateRangeFilter, PastDateRangeFilter, FutureDateRangeFilter


class MyModel(models.Model):
    created_at = models.DateTimeField()
    publish_at = models.DateTimeField()
    review_at = models.DateTimeField()

    class Meta:
        ordering = ['created_at']


class MyModelAdmin(ModelAdmin):
    list_filter = [
        ('created_at', PastDateRangeFilter),
        ('publish_at', FutureDateRangeFilter),
        ('review_at', DateRangeFilter)
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
            review_at=timezone.now()
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

    def test_datefilter(self):
        self.request_factory = RequestFactory()
        modeladmin = MyModelAdmin(MyModel, site)

        request = self.request_factory.get('/')
        request.user = self.user

        changelist = self.get_changelist(request, MyModel, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.object_two, self.object_one])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_text(filterspec.title), 'created at')

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
        self.assertEqual(force_text(filterspec.title), 'created at')

        choice = select_by(filterspec.choices(changelist))
        self.assertEqual(choice['query_string'], '?')
        self.assertEqual(choice['field_name'], 'created_at')
