from openerp.tests.common import TransactionCase
from openerp.addons.at_base import util
from openerp.addons.at_base import helper

class TestUtilTime(TransactionCase):
    """
    Compare old util function with new util function
    """

    def test_str_to_time(self):
        time_util_obj = self.env["util.time"]
        time_str = util.currentDateTime()
        self.assertEqual(util.strToTime(time_str), time_util_obj._str_to_time(time_str))

    def test_time_to_iso(self):
        time_util_obj = self.env["util.time"]
        time_str = util.currentDateTime()
        self.assertEqual(util.strToIsoTime(time_str), time_util_obj._time_to_iso_str(time_str))
        
    def test_iso_to_time(self):
        time_util_obj = self.env["util.time"]
        time_str = util.currentDateTime()
        self.assertEqual(util.isoToStrTime(time_str), time_util_obj._iso_to_time_str(time_str))        

    def test_time_to_str(self):
        time_util_obj = self.env["util.time"]
        time_dt = util.strToTime(util.currentDateTime())
        self.assertEqual(util.timeToStr(time_dt), time_util_obj._time_to_str(time_dt))

    def test_str_to_date(self):
        time_util_obj = self.env["util.time"]
        time_str = util.currentDateTime()
        self.assertEqual(util.strToDate(time_str), time_util_obj._str_to_date(time_str))

    def test_date_to_str(self):
        time_util_obj = self.env["util.time"]
        date_dt = util.strToDate(util.currentDateTime())
        self.assertEqual(util.dateToStr(date_dt), time_util_obj._date_to_str(date_dt))

    def test_format_date_str(self):
        time_util_obj = self.env["util.time"]
        date_str = util.currentDate()
        self.assertEqual(util.formatDate(date_str, "YYYY/MM"), 
                        time_util_obj._format_date_str(date_str, "YYYY/MM"))        
    
    def test_datetime_timezone(self):
        time_util_obj = self.env["util.time"]
        test_time = ["2020-01-01 23:00:00", "2020-07-01 23:00:00"]

        cr = self.env
        uid = self.env.user.id
        user_context = user_context = self.env["res.users"].context_get()
        
        for time_str in test_time:
            # check local conversion
            local_time_str = helper.strToLocalTimeStr(cr, uid, time_str, user_context)
            self.assertEqual(local_time_str,
                time_util_obj._to_datetime_user_str(time_str),
                "Check to local time conversion")
            
            # check utc conversion
            self.assertEqual(time_str, 
                        time_util_obj._to_datetime_utc_str(local_time_str),
                        "Check to utc time conversion")

            utc_time_str = helper.strTimeToUTCTimeStr(cr, uid, local_time_str, user_context)            
            self.assertEqual(utc_time_str, time_str, "Check (old) to utc time conversion")
           

            # check to local date conversion
            local_date_str = helper.strToLocalDateStr(cr, uid, time_str, 
                            user_context)

            self.assertEqual(local_date_str, 
                    time_util_obj._to_date_user_str(time_str),
                    "Check to local date conversion")

            # check to local time conversion from dae            
            utc_time_from_date_str = helper.strDateToUTCTimeStr(cr, uid, local_date_str, user_context)

            self.assertEqual(utc_time_from_date_str, 
                    time_util_obj._to_datetime_utc_str(local_date_str),
                    "Check to local date conversion from date")

          
    def test_first_of_month_str(self):
        date_str = util.currentDate()
        time_util_obj = self.env["util.time"]
        self.assertEqual(util.getFirstOfMonth(date_str), time_util_obj._first_of_month_str(date_str))

    def test_last_month_day(self):
        date_str = util.currentDate()
        time_util_obj = self.env["util.time"]
        self.assertEqual(util.getPrevDayDate(date_str), time_util_obj._get_day_str(date_str, days=-1))                

    def test_next_day_str(self):
        date_str = util.currentDate()
        time_util_obj = self.env["util.time"]
        self.assertEqual(util.getNextDayDate(date_str), time_util_obj._next_day_str(date_str))
