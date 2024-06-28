import os
import datetime
from spinner import *
from yg_file_system import *
from legacy_constant import *

class YgFileSystemObject:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        # print(type(self.name))
        # print(type(self.path))

    def fullName(self):
        return os.path.join(self.path, self.name)

    def extension(self) -> str:
        last = self.name.split(".")[-1]
        if last:
            return last
        else:
            return None

    def isDir(self):
        return os.path.isdir(self.fullName())

    def isFile(self):
        return os.path.isfile(self.fullName())

    def hasFiles(self):
        if self.isFile():
            return False

        files = self.getFiles()
        for file in files:
            if file in Constant.SYSTEM_FILES:
                continue
            else:
                return True
        return False

    def getFiles(self):
        if self.isFile():
            return False
        fileNames = [name for name in os.listdir(self.fullName()) if
                     os.path.isfile(os.path.join(self.fullName(), name))]
        objFiles = []
        for fileName in fileNames:
            objFile = YgFileSystemObject(fileName, self.fullName())
            objFiles.append(objFile)
        return objFiles

    def created_datetime(self) -> datetime:
        stat = os.stat(self.fullName())
        birthtime = stat.st_birthtime
        # print(f"birthtime: {birthtime}")
        birth = datetime.datetime.fromtimestamp(birthtime)
        # print(f"birthtime: {birth}")

        if len(self.name) >= 19:
            name = self.name[:19]
            # print(f"#2 name: {name}")

            try:
                result = self.convert(date_time=str(name), format='%Y-%m-%d_%H-%M-%S')
                return result
            except: pass

        if len(self.name) >= 12:
            name = self.name[:12]
            # print(f"#1 name: {name}")

            try:
                result = self.convert(date_time=name, format='%Y-%m-%d')
                return result
            except: pass

        return birth


    def convert(self, date_time: str, format: str) -> datetime:
        return datetime.datetime.strptime(date_time, format)
