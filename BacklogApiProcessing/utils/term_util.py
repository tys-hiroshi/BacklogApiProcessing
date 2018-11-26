# -*- coding: utf-8 -*-
import datetime
import calendar

class TermUtil():
    """description of class"""
    def __init__(self):
        pass

    def select_next_month_datetime(self, dt):
        max_day = calendar.monthrange(dt.year, dt.month)[1]
        nm = datetime.date(dt.year, dt.month, max_day) + datetime.timedelta(days=1)
        return nm.strftime('%Y-%m-%d')