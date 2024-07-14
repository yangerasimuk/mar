from yg_actor import *
from yg_file_system_iterator_filter import *
from sys import platform
if platform.startswith('win'):
    from pyads import *


class YgActorADSCleaner(YgActor):

    def __init__(self):
        print("YgActorADSCleaner")

    def clean(self, files: [YgFileSystemObject]):
        for file in files:
            ads = ADS(filename=file.full_name())
            print("***")
            print(file.full_name())
            print(ads.streams)
            for stream in ads.streams:
                stream = ads.get_stream_content(stream=stream)
                result = ads.delete_stream(stream=stream)
                print(f"stream deleted? {result}")


class YgIteratorFilterADSFiles(YgFileSystemIteratorFilter):
    def __init__(self):
        print("YgIteratorFilterADSFiles()")

    def __str__(self):
        return "YgIteratorFilterADSFiles"

    def is_match(self, file_system_object: YgFileSystemObject) -> bool:
        if not file_system_object.is_file():
            return False

        ads = ADS(file_system_object.full_name())
        if not ads.has_streams():
            return False

        return True
