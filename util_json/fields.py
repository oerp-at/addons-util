# -*- coding: utf-8 -*--
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
from odoo import fields


class Json(fields.Field):
    """Provide a json field type
    """

    type = "json"
    column_type = ("json", "json")

    def __init__(self,
                 string=fields.Default,
                 base_type=fields.Default,
                 **kwargs):
        super().__init__(string=string, _base_type=base_type, **kwargs)

    def convert_to_column(self, value, record, values=None, validate=True):
        return self.convert_to_cache(value, record, validate=validate)

    def convert_to_cache(self, value, record, validate=True):
        if value is None or value is False:
            return False
        return value

    def convert_to_export(self, value, record):
        if not value:
            return ""
        if isinstance(value, str):
            return value
        return json.dumps(value)

    def convert_to_read(self, value, record, use_name_get=True):
        if not value:
            return ""
        if isinstance(value, str):
            return value
        return json.dumps(value, indent=4)

    def convert_to_display_name(self, value, record):
        if not value:
            return ""
        if isinstance(value, str):
            return value
        return json.dumps(value)
