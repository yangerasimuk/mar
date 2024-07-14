from yg_file_system_iterator_filter import *
from legacy_color import *
from yg_file_system import *


class YgGarbageCollector:
    def __init__(self, file_system: YgFileSystem):
        self.file_system = file_system

    def print(self, files: [YgFileSystemObject]):
        print(Color().RED)
        print("Garbage files:")
        for file in files:
            print(f"\n{file.full_name()}")
        print(Color.ENDCOLOR)

    def erase(self, files: [YgFileSystemObject]):
        success_count = 0
        failure_count = 0
        print(Color().RED)
        print("Garbage collect...")
        for file in files:
            print(f"\n{file.full_name()}")
            try:
                self.file_system.remove_file(file.full_name())
                success_count += 1
            except:
                print("Error during remove file.")
                failure_count += 1
                continue
        print(Color.ENDCOLOR)

        if success_count > 0:
            print(Color().GREEN)
            print(f"Success removed: {success_count}")
            print(Color.ENDCOLOR)
            print(Color().RED)
            print(f"Failure removed: {failure_count}")
            print(Color.ENDCOLOR)


class YgIteratorFilterGarbageFiles(YgFileSystemIteratorFilter):
    def is_match(self, file_system_object: YgFileSystemObject) -> bool:
        # file:///Users/UserName/Downloads/2024-07-14_16-12-48_finder.mar.html
        if file_system_object.is_file() and len(file_system_object.name) >= 19 and file_system_object.name.endswith("_finder.mar.html"):
            name = file_system_object.name[:19]
            try:
                result = file_system_object.convert(date_time=name, format='%Y-%m-%d_%H-%M-%S')
                return True
            except:
                pass

        if file_system_object.is_dir() and file_system_object.name == "@eaDir":
            return True

        if file_system_object.is_file() and file_system_object.name.endswith("@SynoResource"):
            return True

        if file_system_object.is_file() and file_system_object.name.endswith("@SynoEAStream"):
            return True

        if file_system_object.is_file() and file_system_object.name.startswith("SYNOPHOTO_"):
            return True

        return False
    