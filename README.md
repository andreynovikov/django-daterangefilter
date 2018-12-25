# Django admin date range filter

[![Build Status](https://travis-ci.org/andreynovikov/django-daterangefilter.svg?branch=master)](https://travis-ci.org/andreynovikov/django-daterangefilter)
[![GitHub release](https://img.shields.io/github/release/andreynovikov/django-daterangefilter.svg)](https://github.com/andreynovikov/django-daterangefilter/releases/latest)
[![PyPI release](https://img.shields.io/pypi/v/django-daterangefilter.svg)](https://pypi.org/project/django-daterangefilter/)
[![Python version](https://img.shields.io/pypi/pyversions/django-daterangefilter.svg)](https://pypi.org/project/django-daterangefilter/)
[![GitHub issues](https://img.shields.io/github/issues/andreynovikov/django-daterangefilter.svg)](https://github.com/andreynovikov/django-daterangefilter/issues)
[![LGTM code quality](https://img.shields.io/lgtm/grade/python/g/andreynovikov/django-daterangefilter.svg)](https://lgtm.com/projects/g/andreynovikov/django-daterangefilter/)
[![LGTM code quality](https://img.shields.io/lgtm/grade/javascript/g/andreynovikov/django-daterangefilter.svg)](https://lgtm.com/projects/g/andreynovikov/django-daterangefilter/)
[![GitHub license](https://img.shields.io/github/license/andreynovikov/django-daterangefilter.svg)](LICENSE)

Application adds three Django admin list filters: ```DateRangeFilter```, ```PastDateRangeFilter``` and ```FutureDateRangeFilter```. These filters let user filter models by date range. ```PastDateRangeFilter``` and ```FutureDateRangeFilter``` add quick selection of predefined date ranges. Filters can be applied to any model date fields. Application supports default Django admin theme and [Suit theme](https://github.com/darklow/django-suit).

![Admin screenshot](https://raw.githubusercontent.com/andreynovikov/django-daterangefilter/master/screenshot-admin.png)

## Requirements

* Python 2.7+ or Python 3.3+
* Django 1.9+

## Installation

Install ```django-daterangefilter``` using pip:

```
pip install django-daterangefilter
```

Add ```daterangefilter``` to ```INSTALLED_APPS```. Example:

```
INSTALLED_APPS = (
    ...
    'daterangefilter',
    ...
)
```

Application uses static files so do not forget to issue ```collectstatic``` management command in production environment.

## Example usage

in admin.py:

```
from django.contrib import admin
from daterangefilter.filters import PastDateRangeFilter, FutureDateRangeFilter

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = [
        ('created_at', PastDateRangeFilter), ('publish_at', FutureDateRangeFilter)
    ]
```

## Advanced usage

Predefined ranges can be completely redefined by overriding ```_past_ranges.html``` and ```_future_ranges.html``` templates.
Take into account that these templates are inserted in the middle of the javascript code and may contain nothing but ranges
definition. For more examples on using ```moment``` library refer to [library documentation](https://momentjs.com/docs/#/manipulating/).

## Credits

Filter widget uses a great JavaScript date range picker component - [Date Range Picker](https://github.com/dangrossman/daterangepicker) by Dan Grossman.
