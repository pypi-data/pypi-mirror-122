import datetime

from django.utils import timezone
from django.core.exceptions import ValidationError


class PresentTimeValidator:

    def __call__(self, value):
        if isinstance(value, datetime.datetime):
            if value > timezone.now():
                raise ValidationError(_('The datetime must be greater than the current time.'))

        if isinstance(value, datetime.date):
            if value > timezone.now().date():
                raise ValidationError(_("The date can't be less than the current date."))
