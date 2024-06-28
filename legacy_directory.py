import os

# Не используется?

class Directory:
    def __init__(self, name=None, rootPathAbs=None):
        currentDir = os.curdir
        absCurrentDir = os.path.abspath(currentDir)
        print(absCurrentDir)

        if name is None and rootPathAbs is None:
            currentDir = os.curdir
            absCurrentDir = os.path.abspath(currentDir)
            print(absCurrentDir)
        elif rootPathAbs is None:
            self.name = "/"
        else:
            self.name = name
            self.rootPathAbs = rootPathAbs

    def fullPath(self):
        if self.rootPathAbs is None:
            return self.name
        else:
            return self.rootPathAbs + "/" + self.name