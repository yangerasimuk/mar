from legacy_constant import *
from legacy_file_system import *

class LegacyMeta:

    def __init__(self, fileName):
        self.fileName = fileName
        self.metaFileName = fileName + Constant.META_FILE_SUFFIX
        self.fileSystem = LegacyFileSystem()
        self.syncTags()

    def setTags(self, tags):
        self.tags = tags
        self.writeTags()

    def addTags(self, tags):
        self.tags = self.tags + tags
        self.writeTags()

    def deleteTags(self, tags):
        needSync = None
        for tag in tags:
            if tag in self.tags:
                needSync = True
                self.tags.remove(tag)

        if needSync and len(self.tags) != 0:
            self.writeTags()
        elif len(self.tags) == 0:
            self.fileSystem.removeFile(self.metaFileName)

    def eraseTags(self):
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

    def writeTags(self):
        self.fileSystem.writeLinesFile(self.metaFileName, self.tags)

    def readTags(self):
        return self.fileSystem.readLinesFile(self.metaFileName)

    def syncTags(self):
        if self.fileSystem.isExistFile(self.metaFileName):
            self.tags = self.readTags()
        else:
            self.tags = []
