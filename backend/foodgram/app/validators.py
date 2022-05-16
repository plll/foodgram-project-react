import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def min_cooking_time_validator(value):
    if value < 1:
        raise ValidationError(
            _('%(value)s слишком маленькое число'),
            params={'value': value},
        )


def color_check(value):
    if len(value) > 7:
        raise ValidationError(
            _('%(value)s слишком длинная запись цвета'),
            params={'value': value},
        )
    if value[0] != '#':
        raise ValidationError(
            _('%(value)s запись должна начинаться с #'),
            params={'value': value},
        )


def check_slug(value):
    str = '^[-a-zA-Z0-9_]+$'
    if re.match(str, value) is not None:
        return value
    else:
        raise ValidationError(
            _('%(value)s не подходит'),
            params={'value': value},
        )