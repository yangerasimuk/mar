import os
from datetime import datetime as dt, timezone as tz
from legacy_constant import *


class YgFileSystemObject:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def __str__(self) -> str:
        return f"FSO: {self.full_name()}"

    def full_name(self):
        return os.path.join(self.path, self.name)

    def extension(self) -> str:
        last = self.name.split(".")[-1]
        if last:
            return last
        else:
            return None

    def is_dir(self):
        return os.path.isdir(self.full_name())

    def is_file(self):
        return os.path.isfile(self.full_name())

    def is_mar_ignore(self) -> bool:
        mar_ignore_file = os.path.join(self.path, Constant.MAR_IGNORE_FILE_NAME)
        return os.path.isfile(mar_ignore_file)

    def has_files(self):
        if self.is_file():
            return False

        files = self.get_files()
        for file in files:
            if file in Constant.SYSTEM_FILES:
                continue
            else:
                return True
        return False

    def get_files(self):
        if self.is_file():
            return False
        file_names = [name for name in os.listdir(self.full_name()) if
                     os.path.isfile(os.path.join(self.full_name(), name))]
        result_files = []
        for file_name in file_names:
            file = YgFileSystemObject(file_name, self.full_name())
            result_files.append(file)
        return result_files

    def created_datetime(self) -> dt:
        stat = os.stat(self.full_name())
        birth_time = stat.st_birthtime
        birth = dt.fromtimestamp(birth_time)

        # for "2018-10-08_12-55-25_20181008_125525.jpg" file name
        if len(self.name) >= 19:
            name = self.name[:19]
            try:
                result = self.convert(date_time=name, date_format='%Y-%m-%d_%H-%M-%S')
                return result
            except:
                pass

        # for "2021-08-31, Order HT.pdf" file name
        if len(self.name) >= 10:
            name = self.name[:10]
            try:
                result = self.convert(date_time=name, date_format='%Y-%m-%d')
                return result
            except:
                pass

        # print(f"#3 birth: {birth}")
        return birth

    def created_timestamp(self) -> dt:
        stat = os.stat(self.full_name())
        birth = dt.fromtimestamp(stat.st_birthtime, tz=dt.now().astimezone().tzinfo)

        # for "2018-10-08_12-55-25_20181008_125525.jpg" file name
        if len(self.name) >= 19:
            name = self.name[:19]
            try:
                result = self.convert(date_time=name, date_format='%Y-%m-%d_%H-%M-%S')
                diff = birth - result

                # if diff between file system and file name is less than 1 day - use system one
                if diff.days > 1:
                    return result
            except:
                pass

        # for "2021-08-31, Order HT.pdf" file name
        if len(self.name) >= 10:
            name = self.name[:10]
            try:
                result = self.convert(
                    date_time=name,
                    date_format='%Y-%m-%d',
                    time_zone=tz.utc
                )
                diff = birth - result

                # if diff between file system and file name is less than 1 day - use system one
                if diff.days > 1:
                    return result
            except:
                pass

        return birth

    def convert(self, date_time: str, date_format: str, time_zone: dt.tzinfo = None) -> dt:
        result = dt.strptime(date_time, date_format)

        if time_zone:
            result = result.replace(tzinfo=time_zone)
        else:
            result = result.replace(tzinfo=dt.now().astimezone().tzinfo)

        return result
