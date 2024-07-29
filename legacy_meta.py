import uuid
from legacy_file_system import *
from yg_tag import *

class LegacyMeta:

    def __init__(self, fileName):
        self.fileName = fileName
        self.metaFileName = fileName + Constant.META_FILE_SUFFIX
        self.fileSystem = LegacyFileSystem()

        if self.fileSystem.isExistFile(self.metaFileName):
            self.tags = self.readTags()
        else:
            self.tags = []

        self.source_tags = self.tags.copy()

    def set_tags(self, tags):
        if len(tags) == 0:
            print("Can not set empty tags.")
            return
        if not self.fileSystem.isExistFile(self.fileName):
            print("Target file is not exists.")
            return

        # save all kvo tags
        kvo_tags = []
        is_identifiable = False
        for tag in self.tags:
            target = YgTag(string=tag)
            if target.is_key_value():
                kvo_tags.append(str(target))
                if target.identifiable_by_uuid():
                    is_identifiable = True

        # if meta is not identifiable by uuid, add one
        if not is_identifiable:
            string = "[" + Constant.TAG_KEY_SYSTEM_UUID + "]:" + str(uuid.uuid4())
            uuid_tag = YgTag(string=string)
            kvo_tags.append(str(uuid_tag))

        # prepare income tags
        income_tags = []
        for source in tags:
            target = YgTag(string=source)
            income_tags.append(str(target))

        self.tags = kvo_tags + income_tags
        self.write_tags()

    def add_tags(self, tags):
        if len(tags) == 0:
            print("Can not set empty tags.")
            return
        if not self.fileSystem.isExistFile(self.fileName):
            print("Target file is not exists.")
            return

        # check is identifiable
        is_identifiable = False
        for tag in self.tags:
            target = YgTag(string=tag)
            if target.identifiable_by_uuid():
                is_identifiable = True

        # if meta is not identifiable by uuid, add one
        if not is_identifiable:
            string = "[" + Constant.TAG_KEY_SYSTEM_UUID + "]:" + str(uuid.uuid4())
            uuid_tag = YgTag(string=string)
            self.add_tag(uuid_tag)

        # add tags
        for el in tags:
            my_tag = YgTag(string=el)
            self.add_tag(my_tag)

        self.write_tags()

    def delete_tag(self, tag: YgTag, needs_write_to_storage: bool = False):
        key = tag.key_if_kvo()
        result_tags = []
        if key:
            prefix = "[" + key + "]:"
            for el in self.tags:
                if not el.startswith(prefix):
                    result_tags.append(el)
        else:
            string_tag = str(tag)
            for el in self.tags:
                if el != string_tag:
                    result_tags.append(el)

        self.tags = result_tags

        if needs_write_to_storage:
            self.write_tags()

    def delete_tags(self, tags):
        for string_tag in tags:
            obj_tag = YgTag(string=string_tag)
            self.delete_tag(tag=obj_tag)

        if len(self.tags) > 0:
            self.write_tags()
        else:
            self.erase_tags()

    def erase_tags(self):
        if self.fileSystem.isExistFile(self.metaFileName):
            self.fileSystem.removeFile(self.metaFileName)
            print("Meta file removed.")
        else:
            print("Meta file not exists.")

    def printTags(self):
        if len(self.tags) > 0:
            print("Tags:")
            for tag in self.tags:
                print("\t", tag)
        else:
            print("Tags not exists.")

    def metaFileSuffix(self):
        return Constant.META_FILE_SUFFIX

    def write_tags(self):
        if self.source_tags == self.tags:
            print("No changes - no writes.")
            return
        # remove duplicates
        self.tags = list(set(self.tags))
        # sort
        self.tags.sort()
        # write
        self.fileSystem.writeLinesFile(self.metaFileName, self.tags)
        # sync
        self.source_tags = self.tags.copy()

    def readTags(self):
        return self.fileSystem.readLinesFile(self.metaFileName)

    def add_tag(self, tag: YgTag, needs_write_to_storage: bool = False):
        key = tag.key_if_kvo()
        if key:
            prefix = "[" + key + "]:"
            result_tags = []
            for source_tag in self.tags:
                if not source_tag.startswith(prefix):
                    result_tags.append(source_tag)
            result_tags.append(str(tag))
            self.tags = result_tags #.append(str(tag))
        else:
            string_tag = str(tag)
            is_exists = False
            for el in self.tags:
                if el == string_tag:
                    is_exists = True
                    break
            if not is_exists:
                self.tags.append(string_tag)

        if needs_write_to_storage:
            self.write_tags()
