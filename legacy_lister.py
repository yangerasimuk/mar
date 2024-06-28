from legacy_file_system import *
from legacy_meta import *
from legacy_name_resolver import *
from mar import Constant

class Lister:

    def __init__(self):
        self.fileSystem = LegacyFileSystem()
        if self.fileSystem.isExistDirectory(Constant.MAR_DIRECTORY_NAME) == True:
            self.tagsInPath = self.readTagsPath()
        else:
            self.tagsInPath = []
            self.fileSystem.checkDirectory(Constant.MAR_DIRECTORY_NAME)

    def addTags(self, tags):
        for tag in tags:
            if (tag in self.tagsInPath) == False:
                self.tagsInPath.append(tag)
                f = open(Constant.TAGS_PATH_FILE_NAME, "a+")
                f.write(tag + "\n")
                f.close()

    def deleteTags(self, tags):
        needSync = False
        for tag in tags:
            if (tag in self.tagsInPath) == True:
                self.tagsInPath.remove(tag)
                needSync = True

        if needSync == True:
            self.fileSystem.writeLinesFile(Constant.TAGS_PATH_FILE_NAME, self.tagsInPath)

    def printTagsInPath(self):
        if len(self.tagsInPath) > 0:
            print("Tags in path:")
            for tag in self.tagsInPath:
                print("\t" + tag)
        else:
            print("Path is not consists any tag")

    def printFiles(self):
        self.printTagsInPath()
        rawFiles = os.listdir()
        sortedFiles = sorted(rawFiles)
        maredFiles = []
        for file in sortedFiles:
            nameResolver = LegacyNameResolver(file)
            if nameResolver.isValid() and nameResolver.hasMeta():
                maredFiles.append(file)

        matchedFiles = []
        for file in maredFiles:
            meta = LegacyMeta(file)
            tags = meta.readTags()
            isMatch = False
            for tag in self.tagsInPath:
                if (tag in tags):
                    isMatch = True
                else:
                    isMatch = False
                    break

            if isMatch == True:
                matchedFiles.append(file)

        if len(matchedFiles) > 0:
            innerTags = []
            print("Files for path:")
            for file in matchedFiles:
                print("\t" + file)
                meta = LegacyMeta(file)
                #innerTags.extend(meta.tags)
                for tag in meta.tags:
                    if not (tag in innerTags):
                        innerTags.append(tag)
            if len(innerTags) > 0:
                sortedInnerTags = sorted(innerTags)
                print("InnerTags: ")
                for tag1 in sortedInnerTags:
                    print("\t" + tag1)
        else:
            print("Nothing matches for path tags")

    def printFilesRecursive(self):

        self.printTagsInPath()
        rawFiles = os.listdir()
        sortedFiles = sorted(rawFiles)
        maredFiles = []
        for file in sortedFiles:
            nameResolver = LegacyNameResolver(file)
            if nameResolver.isValid() and nameResolver.hasMeta():
                maredFiles.append(file)

        matchedFiles = []
        for file in maredFiles:
            meta = LegacyMeta(file)
            tags = meta.readTags()
            isMatch = False
            for tag in self.tagsInPath:
                if (tag in tags):
                    isMatch = True
                else:
                    isMatch = False
                    break

            if isMatch == True:
                matchedFiles.append(file)

        if len(matchedFiles) > 0:
            innerTags = []
            print("Files for path:")
            for file in matchedFiles:
                print("\t" + file)
                meta = LegacyMeta(file)
                #innerTags.extend(meta.tags)
                for tag in meta.tags:
                    if not (tag in innerTags):
                        innerTags.append(tag)
            if len(innerTags) > 0:
                sortedInnerTags = sorted(innerTags)
                print("InnerTags: ")
                for tag1 in sortedInnerTags:
                    print("\t" + tag1)
        else:
            print("Nothing matches for path tags")

    def printAllTags(self):
        print("lister.printAllTags()")
        rawFiles = os.listdir()
        sortedFiles = sorted(rawFiles)
        maredFiles = []
        for file in sortedFiles:
            nameResolver = LegacyNameResolver(file)
            if nameResolver.isValid() and nameResolver.hasMeta():
                maredFiles.append(file)

        allTags = []
        for file in maredFiles:
            meta = LegacyMeta(file)
            tags = meta.readTags()
            for tag in tags:
                if (tag in allTags) == False:
                    allTags.append(tag)
        sortedAllTags = sorted(allTags)

        if len(sortedAllTags) > 0:
            print("All tags of directory:")
            for tag in sortedAllTags:
                print("\t" + tag)
        else:
            print("Files in directory have not any tags")

    def eraseTags(self):
        if self.fileSystem.isExistFile(Constant.TAGS_PATH_FILE_NAME) == True:
            self.fileSystem.deleteFile(Constant.TAGS_PATH_FILE_NAME)

    def readTagsPath(self):
        if self.fileSystem.isExistFile(Constant.TAGS_PATH_FILE_NAME) == True:
            return self.fileSystem.readLinesFile(Constant.TAGS_PATH_FILE_NAME)
        else:
            return []

