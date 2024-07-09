import os
import datetime
from spinner import *
from yg_file_system import *
from legacy_constant import *


class YgFileSystemObject:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def __str__(self) -> str:
        return f"fso: full_name: {self.full_name()}"

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
        # print("is_mar_ignored()...")
        mar_ignore_file = os.path.join(self.path, Constant.MAR_IGNORE_FILE_NAME)
        # print(f"\t.marignore file: {mar_ignore_file}")
        is_exist = os.path.isfile(mar_ignore_file)
        # if #s_exist:
            # print("\tis_mar_ignore == true")
        # else:
            # print("\tis_mar_ignore == false")
        return is_exist

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
        fileNames = [name for name in os.listdir(self.full_name()) if
                     os.path.isfile(os.path.join(self.full_name(), name))]
        objFiles = []
        for fileName in fileNames:
            objFile = YgFileSystemObject(fileName, self.full_name())
            objFiles.append(objFile)
        return objFiles

    def created_datetime(self) -> datetime:
        stat = os.stat(self.full_name())
        birthtime = stat.st_birthtime
        birth = datetime.datetime.fromtimestamp(birthtime)

        # for "2018-10-08_12-55-25_20181008_125525.jpg" file name
        if len(self.name) >= 19:
            name = self.name[:19]
            try:
                result = self.convert(date_time=name, format='%Y-%m-%d_%H-%M-%S')
                return result
            except:
                pass

        # for "2021-08-31, Order HT.pdf" file name
        if len(self.name) >= 10:
            name = self.name[:10]
            try:
                result = self.convert(date_time=name, format='%Y-%m-%d')
                return result
            except:
                pass

        print(f"#3 birth: {birth}")
        return birth

    def convert(self, date_time: str, format: str) -> datetime:
        return datetime.datetime.strptime(date_time, format)
