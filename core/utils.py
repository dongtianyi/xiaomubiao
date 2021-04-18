import datetime


def get_first_day_week(m_data):
    """获取当前周的第一天"""""
    monday = m_data
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    return monday.date()


def get_last_day_week(m_data):
    """获取当前周的最后一天"""""
    monday = m_data
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 6:
        monday += one_day
    return monday.date()
