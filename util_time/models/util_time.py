# -*- coding: utf-8 -*-
#############################################################################
#
#    Copyright (c) 2007 Martin Reisenhofer <martin.reisenhofer@funkring.net>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime
from datetime import date

import time
import dateutil
from dateutil.relativedelta import relativedelta
import pytz

from openerp import models, fields, api, _


DT_FORMAT = "%Y-%m-%d"
DHMS_FORMAT = "%Y-%m-%d %H:%M:%S"
HMS_FORMAT = "%H:%M:%S"
HM_FORMAT_SHORT = "%H:%M"

ISO_FORMAT_UTC = "%Y-%m-%dT%H:%M:%SZ"


class UtilTime(models.AbstractModel):
    _name = "util.time"

    def _str_to_time(self, time_str):
        if not time_str:
            return time_str
        if isinstance(time_str, datetime):
            return time_str
        pos = time_str.find(".")
        if pos > 0:
            time_str = time_str[:pos]
        return datetime.strptime(time_str, DHMS_FORMAT)

    def _time_to_iso_str(self, time_str):
        time_str = self._str_to_time(time_str)
        return time.strftime(ISO_FORMAT_UTC)
 
    def _iso_to_time_str(self, iso_str):
        if not iso_str:
            return None
        val = dateutil.parser.parse(iso_str)
        if not val.tzinfo:
            val = pytz.utc.localize(val)
        val = val.astimezone(pytz.utc).replace(tzinfo=None)
        return self._time_to_str(val)

    def _time_to_str(self, time_dt):
        return datetime.strftime(time_dt, DHMS_FORMAT)

    def _time_to_date_str(self, time_str):
        time_dt = self._str_to_time(time_str)
        date_dt = date(time_dt.year, time_dt.month, time_dt.day)
        return self._date_to_str(date_dt)

    def _str_to_date(self, date_str):
        if not date_str:
            return date_str
        if isinstance(date_str, datetime):
            return date_str
        if len(date_str) > 10:
            date_str = self._time_to_date_str(date_str)
        return datetime.strptime(date_str, DT_FORMAT)

    def _date_to_str(self, date_dt):
        return datetime.strftime(date_dt, DT_FORMAT)

    def _date_to_time_str(self, date_str):
        if len(date_str) <= 10:
            return "%s 00:00:00" % date_str
        return date_str

    def _format_date_str(self, date_str, format_str):
        date_dt = self._str_to_date(date_str)
        return datetime.strftime(date_dt, format_str)

    def _format_time_str(self, time_str, format_str):
        time_dt = self._str_to_time(time_str)
        return datetime.strftime(time_dt, format_str)

    def _to_datetime_user_str(self, time_str):
        # check if it is date, convert it to time
        # if needed
        if len(time_str) <= 10:
            time_str = self._date_to_time_str(time_str)            
        user_tz = pytz.timezone(self.env.user.tz or pytz.utc)
        return datetime.strftime(
            pytz.utc.localize(datetime.strptime(time_str, DHMS_FORMAT)).astimezone(user_tz), DHMS_FORMAT
        )

    def _to_date_user_str(self, time_str):
        time_str = self._date_to_time_str(time_str)
        user_tz = pytz.timezone(self.env.user.tz or pytz.utc)
        return datetime.strftime(
            pytz.utc.localize(datetime.strptime(time_str, DHMS_FORMAT)).astimezone(user_tz), DT_FORMAT
        )

    def _to_datetime_utc_str(self, time_str):
        # check if it is date, convert it to time
        # if needed
        if len(time_str) <= 10:
            time_str = self._date_to_time_str(time_str)  
        user_tz = pytz.timezone(self.env.user.tz or pytz.utc)
        return datetime.strftime(
            user_tz.localize(datetime.strptime(time_str, DHMS_FORMAT)).astimezone(pytz.utc), DHMS_FORMAT
        )

    def _to_date_user_utc_str(self, time_str):
        time_str = self._date_to_str(time_str)
        user_tz = pytz.timezone(self.env.user.tz or pytz.utc)
        return datetime.strftime(
            user_tz.localize(datetime.strptime(time_str, DHMS_FORMAT)).astimezone(pytz.utc), DT_FORMAT
        )

    def _current_date_str(self):
        return time.strftime(DT_FORMAT)

    def _current_date_utc_str(self):
        return datetime.utcnow().strftime(DT_FORMAT)

    def _current_datetime_str(self):
        return time.strftime(DHMS_FORMAT)

    def _current_datetime_utc_str(self):
        return datetime.utcnow().strftime(DHMS_FORMAT)

    def _first_of_month_str(self, date_str):
        if not date_str:
            return date_str
        date_dt = self._str_to_date(date_str)
        return self._date_to_str(date(date_dt.year, date_dt.month, 1))
    
    def _first_of_last_month_str(self):
        return self._first_of_month_str(self._last_month_str(self._current_date_str()))

    def _next_day_str(self, date_str):
        date_dt = self._str_to_date(date_str)
        next_dt = date(date_dt.year, date_dt.month, date_dt.day)
        next_dt += relativedelta(days=1)
        return self._date_to_str(next_dt)

    def _get_day_str(self, date_str=None, days=0, months=0):
        if not date_str:
            return self._current_date_str()
        day_dt = self._str_to_date(date_str)
        if days:
            day_dt += relativedelta(days=days)
        if months:
            day_dt += relativedelta(months=months)
        return self._date_to_str(day_dt)
