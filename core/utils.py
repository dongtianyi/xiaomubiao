import datetime


def get_first_day_week(m_data):
    """获取当前周的第一天0点"""""
    monday = m_data
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    return monday.replace(hour=0, minute=0, second=0, microsecond=0)


def get_last_day_week(m_data):
    """获取当前周的最后一天23:59:59:999"""""
    monday = m_data
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 6:
        monday += one_day
    return monday.replace(hour=23, minute=59, second=59, microsecond=999)
