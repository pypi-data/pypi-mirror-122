import re
from datetime import datetime
from django.utils.translation import ugettext as _

from rest_framework import serializers

from corfmann.validators import PresentTimeValidator


class TimestampField(serializers.DateTimeField):
    """
    Convert a django datetime to/from timestamp.
    """
    default_error_messages = {
        'invalid': _('A valid timestamp is required.'),
    }
    re_decimal = re.compile(r'\.0*\s*$')  # allow e.g. '1.0' as an int, but not '1.2'

    def __init__(self, allow_zero=True, allow_future=True, *args, **kwargs):
        self.allow_zero = allow_zero
        self.allow_future = allow_future
        if not self.allow_future:
            self.validators.append(PresentTimeValidator())

        super(TimestampField, self).__init__(*args, **kwargs)
        self.style['input_type'] = 'number'

    def to_representation(self, value):
        if not value:
            return None

        value = self.enforce_timezone(value)
        return int(value.timestamp())

    def to_internal_value(self, data):
        """
        deserialize a timestamp to a DateTime value
        :param value: the timestamp value
        :return: a django DateTime value
        """
        try:
            data = int(self.re_decimal.sub('', str(data)))
            if data < 0:
                raise ValueError
            if self.allow_zero or data:
                data = datetime.fromtimestamp(data)
        except (ValueError, TypeError):
            self.fail('invalid')

        return super(TimestampField, self).to_representation(data)

    class Meta:
        swagger_schema_fields = {
            'type': 'integer',
            'format': 'timestamp',
            # 'title': 'Client date time suu',
            # 'description': 'Date time in unix timestamp format',
        }
