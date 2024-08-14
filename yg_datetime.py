import datetime as dt
from legacy_constant import *
from typing import Union


class YgDatetime:
    # TODO: Change __init__ after python version up to 3.10
    # def __init__(self, datetime: dt.datetime | str = None):
    def __init_(self, datetime: Union[dt.datetime, str, None] = None):
        if isinstance(datetime, dt.datetime):
            self.stamp = datetime
        elif isinstance(datetime, str):
            try:
                temp = dt.datetime.strptime(datetime, Constant.TAG_VALUE_SYSTEM_DATE_FORMAT)
                self.stamp = temp
            except ValueError:
                print(f"Unsupported date format for: {datetime}")
        else:
            self.stamp = self.now()

    def __str__(self):
        return self.stamp.strftime(format=Constant.TAG_VALUE_SYSTEM_DATE_FORMAT)

    def now(self) -> dt.datetime:
        return dt.datetime.now(tz=dt.datetime.now().astimezone().tzinfo)