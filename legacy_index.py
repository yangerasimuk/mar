import os
from legacy_constant import *
from legacy_name_resolver import *
from legacy_file_system import *


class LegacyIndex:
    indexFileName = "./.mar/index.mar.txt"

    def __init__(self):
        self.fileSystem = LegacyFileSystem()

        if self.fileSystem.isExistDirectory(Constant.INDEX_DIRECTORY_NAME) == True:
            self.fileNamesInIndex = self.readIndex()
        else:
            self.fileNamesInIndex = []
            self.checkIndexDirectory()

    def setFile(self, name):
        # print("index.setFile()")
        self.fileNamesInIndex = [name]
        self.fileSystem.writeLinesFile(Constant.INDEX_FILE_NAME, self.fileNamesInIndex)

    def addFile(self, name):
        # print("index.addFile()")
        if name not in self.fileNamesInIndex:
            # print(name + " not in index")
            f = open(Constant.INDEX_FILE_NAME, "a+")
            f.write(name + "\n")
            f.close()
        else:
            print("File exists in index yet")

    def addFolder(self):
        elements = os.listdir()
        validFiles = []

        print("index.addFolder()")
        print("elements before:")
        for el in elements:
            print("\t" + el)
            resolver = LegacyNameResolver(el)
            if resolver.isValid():
                validFiles.append(el)

        print("elements after:")
        for file in validFiles:
            print("\t" + file)
            self.addFile(file)

    def listFiles(self):
        return self.fileNamesInIndex

    def printFiles(self):
        if len(self.fileNamesInIndex) > 0:
            print("File(s) in index:")
            for name in self.fileNamesInIndex:
                print("\t" + name)
        else:
            print("Index is empty")

    def deleteFile(self, name):
        if name in self.fileNamesInIndex:
            self.fileNamesInIndex.remove(name)
            if self.fileNamesInIndex.count > 0:
                self.fileSystem.writeLinesFile(Constant.INDEX_FILE_NAME, self.fileNamesInIndex)
            else:
                self.fileSystem.removeFile(Constant.INDEX_FILE_NAME)
        else:
            print("File not exists in index")

    def eraseIndex(self):
        self.fileSystem.removeFile(Constant.INDEX_FILE_NAME)

    def readIndex(self):
        if self.fileSystem.isExistFile(Constant.INDEX_FILE_NAME) == True:
            return self.fileSystem.readLinesFile(Constant.INDEX_FILE_NAME)
        else:
            return []

    def checkIndexDirectory(self):
        if self.fileSystem.isExistDirectory(Constant.INDEX_DIRECTORY_NAME) == False:
            self.fileSystem.makeDirectory(Constant.INDEX_DIRECTORY_NAME)
        else:
            print("Index directory exists yet.")

    def isExistIndex(self):
        if self.fileSystem.isExistFile(Constant.INDEX_FILE_NAME):
            return True
        else:
            return False
