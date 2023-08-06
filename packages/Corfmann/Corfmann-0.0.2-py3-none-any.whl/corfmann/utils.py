import base64
import datetime
import json
import os
import tempfile
import pandas as pd
import pytz

from django.utils import dateparse
from django.apps import apps
from django.utils.text import capfirst


def verbose_name(app_model, field=None, cap_first=True):
    """Get verbose name of field or model"""
    if isinstance(app_model, str):
        opts = apps.get_model(app_model, require_ready=False)._meta
    else:
        opts = app_model._meta

    if field is not None:
        if isinstance(field, str):
            verbose_name = opts.get_field(field).verbose_name
        else:
            names = []
            for field_name in field:
                verbose_name = opts.get_field(field_name).verbose_name
                names.append(str(capfirst(verbose_name) if cap_first else verbose_name))
            return names
    else:
        verbose_name = opts.verbose_name

    return capfirst(verbose_name) if cap_first else verbose_name


class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ExcelConverter:

    def __init__(self, data, columns=None):
        self.columns = columns
        if columns:
            self.data = [tuple(d.values()) for d in data]
        else:
            self.data = data

    def _to_excel(self, file_path):
        df = pd.DataFrame(self.data, columns=self.columns)
        df.to_excel(file_path, index=False)

    def to_excel(self, file_path):
        self._to_excel(file_path)

    def base64_content(self, filename):
        file_path = os.path.join(tempfile.gettempdir(), filename)
        f = open(file_path, 'rb')
        self._to_excel(f)
        file_content = f.read()
        return base64.b64encode(file_content).decode('UTF-8')


def str_to_date(date_str, format=None, to_utc=False):
    if format is None:
        dt = dateparse.parse_datetime(date_str)
    else:
        if isinstance(format, list):
            for f in format:
                try:
                    dt = datetime.datetime.strptime(date_str, f)
                except ValueError:
                    continue
                else:
                    break
        else:
            dt = datetime.datetime.strptime(date_str, format)
    if dt is None:
        raise ValueError('Unable to convert date string')
    if to_utc:
        dt = dt.astimezone(pytz.utc)
    return dt


def format_date_str(str, target_format, original_format=None, to_utc=False):
    dt = str_to_date(str, format=original_format, to_utc=to_utc)
    return dt.strptime(target_format)



