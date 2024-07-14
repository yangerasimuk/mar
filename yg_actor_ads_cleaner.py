from yg_actor import *
from yg_file_system_iterator_filter import *
from legacy_color import *
from legacy_constant import *
from sys import platform
if platform.startswith('win'):
    from pyads import *


class YgActorADSCleaner(YgActor):

    def print(self, files: [YgFileSystemObject]):
        for file in files:
            print("***")
            print(file.full_name())
            ads = ADS(filename=file.full_name())
            for stream in ads.streams:
                stream = ads.get_stream_content(stream)
                print(stream)

    def erase(self, files: [YgFileSystemObject]):
        success_count = 0
        failure_files = []
        for file in files:
            ads = ADS(filename=file.full_name())
            for stream in ads.streams:
                result = ads.delete_stream(stream=stream)
                if result:
                    success_count += 1
                else:
                    failure_files.append(file)

        if success_count > 0:
            print(Color().GREEN)
            print(f"Success ADS removed: {success_count}")
            print(Color.ENDCOLOR)
        if len(failure_files) > 0:
            print(Color().RED)
            print(f"Failure ADS removed: {len(failure_files)}")
            for file in failure_files:
                print("\n" + file.full_name())
            print(Color.ENDCOLOR)


class YgIteratorFilterADSFiles(YgFileSystemIteratorFilter):
    def is_match(self, file_system_object: YgFileSystemObject) -> bool:
        if not file_system_object.is_file():
            return False

        ads = ADS(file_system_object.full_name())
        if not ads.has_streams():
            return False

        return True

