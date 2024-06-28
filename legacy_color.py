class Color:
    # https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    ENDCOLOR = '\033[0m'

    def fileNameInIndex(self):
        return self.YELLOW

    def fileAddedToIndex(self):
        return self.GREEN

    def fileRemovedFromIndex(self):
        return self.RED