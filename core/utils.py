import datetime


def get_current_week():
    """后去当前周的第一天"""""
    monday = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    return monday
