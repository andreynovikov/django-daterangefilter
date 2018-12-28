# Django admin date range filter

[![Build Status](https://travis-ci.org/andreynovikov/django-daterangefilter.svg?branch=master)](https://travis-ci.org/andreynovikov/django-daterangefilter)
[![GitHub release](https://img.shields.io/github/release/andreynovikov/django-daterangefilter.svg)](https://github.com/andreynovikov/django-daterangefilter/releases/latest)
[![PyPI release](https://img.shields.io/pypi/v/django-daterangefilter.svg)](https://pypi.org/project/django-daterangefilter/)
[![Python version](https://img.shields.io/pypi/pyversions/django-daterangefilter.svg)](https://pypi.org/project/django-daterangefilter/)
[![GitHub issues](https://img.shields.io/github/issues/andreynovikov/django-daterangefilter.svg)](https://github.com/andreynovikov/django-daterangefilter/issues)
[![Code quality](https://img.shields.io/codacy/grade/e90b9f21941a4d8c93edb4a58caa3667.svg)](https://www.codacy.com/app/novikov/django-daterangefilter)
[![Coverage](https://img.shields.io/codacy/coverage/e90b9f21941a4d8c93edb4a58caa3667.svg)](https://www.codacy.com/app/novikov/django-daterangefilter)
[![GitHub license](https://img.shields.io/github/license/andreynovikov/django-daterangefilter.svg)](LICENSE)

Application adds three Django admin list filters: ```DateRangeFilter```, ```PastDateRangeFilter``` and ```FutureDateRangeFilter```. These filters let user filter models by date range. ```PastDateRangeFilter``` and ```FutureDateRangeFilter``` add quick selection of predefined date ranges. Filters can be applied to any model date fields. Application supports default Django admin theme and [Suit theme](https://github.com/darklow/django-suit).

![Admin screenshot](https://raw.githubusercontent.com/andreynovikov/django-daterangefilter/master/screenshot-admin.png)

## Requirements

* Python 2.7+ or Python 3.3+
* Django 1.9+

## Installation

Install ```django-daterangefilter``` using pip:

```shell
pip install django-daterangefilter
```

Add ```daterangefilter``` to ```INSTALLED_APPS```. Example:

```python
INSTALLED_APPS = (
    ...
    'daterangefilter',
    ...
)
```

Application uses static files so do not forget to issue ```collectstatic``` management command in production environment.

## Example usage

in admin.py:

```python
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
