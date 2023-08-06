
from pandas.tseries.offsets import BMonthBegin, BDay
from datetime import date
import holidays

# Creating a list of Indian holidays


def get_holidays(year):
    # Get the holiday dates for the given year
    holiday_dates = holidays.CountryHoliday('IN', years=year).items()
    
    # Convert the holiday dates to a list of strings
    holidays_list = [str(date[0]) for date in holiday_dates]
    
    return holidays_list

# Calculating a list of holidays from 1900 to 2100
list_of_holidays = []
for i in range(1900,2100):
    list_of_holidays.extend(get_holidays(i))






offset = BMonthBegin()



# Claculatig the first working day of every month if the fifth working day is a holiday then return the preceding working day
def first_working_day(start_date):
    offset = BMonthBegin()
    day_ = offset.rollback(start_date).date()
    if day_ in list_of_holidays:
        return day_ + BDay(1)
    else:
        return day_
        



# Claculatig the second working day of every month if the fifth working day is a holiday then return the preceding working day
def second_working_day(start_date):
    offset = BMonthBegin()
    day_ = offset.rollback(start_date).date() + BDay(1)
    if day_ in list_of_holidays:
        return day_ + BDay(2)
    else:
        return day_
        



# Claculatig the third working day of every month if the fifth working day is a holiday then return the preceding working day
def third_working_day(start_date):
    offset = BMonthBegin()
    day_ = offset.rollback(start_date).date() + BDay(2)
    if day_ in list_of_holidays:
        return day_ + BDay(3)
    else:
        return day_
        


# Claculatig the fourth working day of every month if the fifth working day is a holiday then return the preceding working day
def fourth_working_day(start_date):
    offset = BMonthBegin()
    day_ = offset.rollback(start_date).date() + BDay(3)
    if day_ in list_of_holidays:
        return day_ + BDay(4)
    else:
        return day_
        



# Claculatig the fifth working day of every month if the fifth working day is a holiday then return the preceding working day
def fifth_working_day(start_date):
    offset = BMonthBegin()
    day_ = offset.rollback(start_date).date() + BDay(4)
    if day_ in list_of_holidays:
        return day_ + BDay(5)
    else:
        return day_
        


# Claculatig the n-th working day of every month if the fifth working day is a holiday then return the preceding working day
def nth_working_day(start_date,n):
    """
    start_date: in datetime format
    n: the n-th business day
    """
    offset = BMonthBegin()
    day_ = offset.rollback(start_date).date() + BDay(n-1)
    if day_ in list_of_holidays:
        return day_ - BDay(n)
    else:
        return day_
        








