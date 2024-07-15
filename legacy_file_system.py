import os


class LegacyFileSystem:
    def isExistFile(self, fileName):
        if os.path.isfile(fileName):
            return True
        else:
            return False

    def isExistDirectory(self, path):
        if os.path.isdir(path):
            return True
        else:
            return False

    def readLinesFile(self, path):
        lines = []
        with open(path) as f:
            lines = [line.rstrip() for line in f]
        return lines

    def writeLinesFile(self, path, lines):
        with open(path, "w") as f:
            for line in lines:
                f.write(line + "\n")

    def removeFile(self, path):
        if self.isExistFile(path):
            os.remove(path)
            print("File '" + path + "' removed")
        else:
            print("File '" + path + "' not exists.")

    def makeDirectory(self, path):
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory failed. Path: " + path)

    def checkDirectory(self, path):
        if self.isExistDirectory(path) == False:
            self.makeDirectory(path)
