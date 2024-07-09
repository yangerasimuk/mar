from yg_file_system_object import *
from legacy_meta import *
from legacy_name_resolver import *


class YgFileSystemIteratorFilter:
    def is_match(self, file_system_object: YgFileSystemObject) -> bool:
        return False


class YgIteratorFilterMarFiles(YgFileSystemIteratorFilter):
    def is_match(self, file_system_object: YgFileSystemObject) -> bool:
        if not file_system_object.is_file():
            return False
        if file_system_object.is_mar_ignore():
            return False

        name_resolver = LegacyNameResolver(file_system_object.full_name())
        if not name_resolver.isValid() or not name_resolver.hasMeta():
            return False

        return True


class YgIteratorFilterMarSelectedFiles(YgFileSystemIteratorFilter):
    def __init__(self, tags: [str]):
        self.tags = tags

    def __str__(self):
        selected_tags = ' '.join(self.tags)
        return "YgIteratorFilterMarSelectedFiles. Selected tags: " + selected_tags

    def is_match(self, file_system_object: YgFileSystemObject) -> bool:
        if not file_system_object.is_file():
            return False

        if file_system_object.is_mar_ignore():
            return False

        name_resolver = LegacyNameResolver(file_system_object.full_name())
        if not name_resolver.isValid() or not name_resolver.hasMeta():
            return False

        meta = LegacyMeta(file_system_object.full_name())
        if len(meta.tags) == 0:
            return False

        intersection = set(meta.tags).intersection(self.tags)
        if list(intersection) != self.tags:
            return False

        return True
