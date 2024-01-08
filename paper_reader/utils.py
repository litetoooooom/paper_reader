
from datetime import datetime

def format_date(datetime_obj: datetime):
    """ 格式化日期格式
    """
    return datetime_obj.strftime("%Y%m%d")