import hashlib
import os

from legacy_index import *
from legacy_name_resolver import *
from mar import Color


class LegacyFolder:

    def __init__(self):
        self.index = LegacyIndex()

    def print(self):
        files = self.files()
        counter = 0
        for file in files:
            if file in self.index.fileNamesInIndex:
                print(Color().fileNameInIndex() + str(counter) + "\t" + file + Color.ENDCOLOR)
            else:
                print(str(counter) + "\t" + file)
            counter = counter + 1

    def printHash(self):
        files = self.files()
        for file in files:
            fileHashRaw = file.encode('utf-8')
            fileHash = hashlib.sha1(fileHashRaw).hexdigest()
            if file in self.index.fileNamesInIndex:
                print(Color().fileNameInIndex() + fileHash + "\t" + file + Color.ENDCOLOR)
            else:
                print(fileHash + "\t" + file)

    def addFilesWithIndexes(self, fileIndexes):
        if len(fileIndexes) == 0:
            print("Index(es) not passed.")
            return

        files = self.files()
        counter = 0
        for file in files:
            counterStr = str(counter)
            if counterStr in fileIndexes:
                print(Color().fileAddedToIndex() + str(counterStr) + "\t" + file + Color.ENDCOLOR)
                self.index.addFile(file)
            counter = counter + 1

    def removeFilesWithIndexes(self, fileIndexes):
        files = self.files()
        counter = 0
        for file in files:
            counterStr = str(counter)
            if counterStr in fileIndexes:
                print(Color().fileRemovedFromIndex() + str(counterStr) + "\t" + file + Color.ENDCOLOR)
                self.index.deleteFile(file)
            counter = counter + 1

    def openFileWithIndex(self, index):
        files = self.files()
        counter = 0
        for file in files:
            counterStr = str(counter)
            if index == counterStr:
                os.system("open " + file)
            counter = counter + 1

    # Private

    def files(self):
        rawFiles = os.listdir()
        sortedFiles = sorted(rawFiles)
        validFiles = []
        for file in sortedFiles:
            nameResolver = LegacyNameResolver(file)
            if nameResolver.isValid():
                validFiles.append(file)
        return validFiles
