#!/usr/bin/env python

from __future__ import unicode_literals

import django

from django.conf import settings
from django.core.management import call_command


settings.configure(
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'django.contrib.admin',
        'django.contrib.sessions',
        'django.contrib.messages',
        'daterangefilter',
    ),
    MIDDLEWARE=(
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
    ),
    TEMPLATES=(
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'OPTIONS': {
                'context_processors': (
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                )
            },
        },
    ),
    DATABASES={
        'default': {'ENGINE': 'django.db.backends.sqlite3'}
    },
    DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
    TEST_RUNNER='django.test.runner.DiscoverRunner',
    USE_TZ=True,
    TIME_ZONE='UTC',
    SECRET_KEY='*',
)

django.setup()

if __name__ == '__main__':
    call_command('test', 'daterangefilter')
