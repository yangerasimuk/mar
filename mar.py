import sys

from urler import *
from legacy_folder import *
from legacy_meta_index import *
from legacy_lister import *
from legacy_constant import *
from yg_actor_viewer import *
from yg_actor_ads_cleaner import *
from yg_garbage_collector import *

from yg_tag import *
from uuid import *

class Version:
    major = "0"
    minor = "3"
    patch = "1"
    build = "July 14, 2024"
    author = "Yan Gerasimuk"

    def fullVersion(self):
        return "v" + self.major + "." + self.minor + "." + self.patch + " (" + self.build + ")"

    def shortVersion(self):
        return "v" + self.major + "." + self.minor + "." + self.patch

    def print(self):
        print("mar " + self.fullVersion() + ", (c) " + self.author)


class Environment:
    def print(self):
        print(sys.version)


class Helper:

    def print(self):
        print("\tРабота с тегами одного файла")
        print("\tmar.py tag [sadep] FILE [tag...]")
        print("\tmar.py tag --set text.txt firstTag secondTag")
        print("\t\t" + "-s или --set Установить теги")
        print("\t\t" + "-a или --add Добавить теги")
        print("\t\t" + "-d или --delete Удалить теги")
        print("\t\t" + "-e или --erase Удалить все теги (файл с тегами")
        print("\t\t" + "-p или --print Напечатать теги файла")

def tagIndex(argv):
    option = argv[2]
    # print("Option: ", option)

    # print("Tags: ")
    tags = []
    counter = 3
    while counter < len(argv):
        print("\t", argv[counter])
        tags.append(argv[counter])
        counter = counter + 1

    metaIndex = LegacyMetaIndex()
    if option == "-s" or option == "--set":
        metaIndex.setTags(tags)
    elif option == "-a" or option == "--add":
        metaIndex.addTags(tags)
    elif option == "-d" or option == "--delete":
        metaIndex.deleteTags(tags)
    elif option == "-e" or option == "--erase":
        metaIndex.eraseTags()


def tag(argv):
    option = argv[2]
    # print("Option: ", option)
    file = argv[3]
    print("File: ", file)

    tags = []
    counter = 4
    while counter < len(argv):
        tags.append(argv[counter])
        counter = counter + 1

    meta = LegacyMeta(file)

    if option == "-s" or option == "--set":
        meta.set_tags(tags)
    elif option == "-a" or option == "--add":
        meta.add_tags(tags)
    elif option == "-d" or option == "--delete":
        meta.delete_tags(tags)
    elif option == "-e" or option == "--erase":
        meta.erase_tags()
    elif option == "-p" or option == "--print":
        meta.printTags()


def tagList(argv):
    print("tagList()")

    for arg in argv:
        print(arg)

    fs = YgFileSystem()
    fs.cur_folder()
    #fs.fast_scandir(os.curdir)
    curdir = os.path.abspath(os.curdir)
    folder = YgFolder(curdir)

    print("#1")
    folders = fs.folders(folder, False)
    for item in folders:
        item.print()

    print("#2")
    folders2 = fs.folders(folder)
    for item in folders2:
        item.print()


def index(argv):
    option = argv[2]
    # print("Option: ", option)
    file = ""
    if len(argv) >= 4:
        file = argv[3]
    # print("File: ", file)

    index = LegacyIndex()
    if option == "-s" or option == "--set":
        index.setFile(file)
    elif option == "-a" or option == "--add":
        index.addFile(file)
    elif option == "-f" or option == "--add-folder":
        index.addFolder()
    elif option == "-d" or option == "--delete":
        index.deleteFile(file)
    elif option == "-e" or option == "--erase":
        index.eraseIndex()
    elif option == "-l" or option == "--list":
        index.listFiles()
    elif option == "-p" or option == "--print":
        index.printFiles()


def folder(argv):
    option = argv[2]
    # print("Option: ", option)

    indexes = []
    counter = 3
    while counter < len(argv):
        index = argv[counter]
        # nameResolver = NameResolver()
        indexes.append(index)
        counter = counter + 1

    folder = LegacyFolder()
    if option == "-p" or option == "--print":
        folder.print()
    elif option == "-a" or option == "--add":
        folder.addFilesWithIndexes(indexes)
    elif option == "-d" or option == "--delete":
        folder.removeFilesWithIndexes(indexes)
    elif option == "-o" or option == "--open":
        folder.openFileWithIndex(index)
    elif option == "-h" or option == "--hash":
        folder.printHash()


def listTag(argv):
    # mar.py list --add someTag

    tags = []

    if len(argv) > 2:
        option = argv[2]
        print("Option: ", option)
        counter = 3
        while counter < len(argv):
            tag = argv[counter]
            tags.append(tag)
            counter = counter + 1
            print("\t" + tag)
    elif len(argv) == 2:
        print("List of current tags")

    #assert False, "Объект lister не реализован"
    lister = Lister()
    if option == "-a" or option == "--add":
        lister.addTags(tags)
    elif option == "-d" or option == "--delete":
        lister.deleteTags(tags)
    elif option == "-p" or option == "--print":
        lister.printTagsInPath()
    elif option == "-f" or option == "--files":
        lister.printFiles()
    elif option == "-t" or option == "--tags":
        lister.printAllTags()
    elif option == "-e" or option == "--erase":
        lister.eraseTags()
    elif option == "-r" or option == "--files-recursive":
        lister.printFilesRecurcive()


def view(argv):
    print(argv)
    terminal_path = ' '.join(argv)
    print("Call " + terminal_path)

    filesystem = YgFileSystem()
    find = YgFinder(filesystem)
    viewer = YgViewer()
    if len(argv) == 3 and argv[2] in ("-r", "--recursive"):
        viewer.view_with_finder(find, is_recursive=True)
    else:
        viewer.view_with_finder(find)

    print(filesystem.desktop_folder())

def garbage_collector(argv):
    file_system = YgFileSystem()
    find = YgFinder(filesystem=file_system)
    garbage_collector = YgGarbageCollector(file_system=file_system)

    option = None
    if len(argv) > 2:
        option = argv[2]
    else:
        print("Command line error.")
        return

    if option == "-e" or option == "--erase":
        objects = find.files_with_filter(YgIteratorFilterGarbageFiles())
        garbage_collector.erase(objects=objects)
    elif option == "-er" or option == "--erase-recursive":
        objects = find.files_with_filter(YgIteratorFilterGarbageFiles(), is_recursive=True)
        garbage_collector.erase(objects=objects)
    elif option == "-p" or option == "--print":
        objects = find.files_with_filter(YgIteratorFilterGarbageFiles())
        garbage_collector.print(objects=objects)
    elif option == "-pr" or option == "--print-recursive":
        objects = find.files_with_filter(YgIteratorFilterGarbageFiles(), is_recursive=True)
        garbage_collector.print(objects=objects)
    else:
        error(argv)

def ads_cleaner(argv):
    terminal_path = ' '.join(argv)
    print("Call " + terminal_path)

    if not platform.startswith('win'):
        print("Manipulating with ntfs streams (ADS) available only on windows platform.")
        return

    option = None
    if len(argv) > 2:
        option = argv[2]
    else:
        print("Command line error.")
        return

    filesystem = YgFileSystem()
    find = YgFinder(filesystem)
    cleaner = YgActorADSCleaner()

    if option == "-e" or option == "--erase":
        files = find.files_with_filter(YgIteratorFilterADSFiles())
        if len(files) == 0:
            print(Color().GREEN + Constant.MESSAGE_NO_ADS_FILES + Color.ENDCOLOR)
        else:
            cleaner.erase(files=files)
    elif option == "-er" or option == "--erase-recursive":
        files = find.files_with_filter(YgIteratorFilterADSFiles(), is_recursive=True)
        if len(files) == 0:
            print(Color().GREEN + Constant.MESSAGE_NO_ADS_FILES + Color.ENDCOLOR)
        else:
            cleaner.erase(files=files)
    elif option == "-p" or option == "--print":
        files = find.files_with_filter(YgIteratorFilterADSFiles())
        if len(files) == 0:
            print(Color().GREEN + Constant.MESSAGE_NO_ADS_FILES + Color.ENDCOLOR)
        else:
            cleaner.print(files=files)
    elif option == "-pr" or option == "--print-recursive":
        files = find.files_with_filter(YgIteratorFilterADSFiles(), is_recursive=True)
        if len(files) == 0:
            print(Color().GREEN + Constant.MESSAGE_NO_ADS_FILES + Color.ENDCOLOR)
        else:
            cleaner.print(files=files)
    else:
        error(argv)


def finder(argv):
    terminal_path = ' '.join(argv)
    print("Call " + terminal_path)

    option = argv[2]
    keys = []

    if len(argv) > 2:
        option = argv[2]
        # print("Option: ", option)
        counter = 3
        while counter < len(argv):
            key = argv[counter]
            keys.append(key)
            counter = counter + 1

    filesystem = YgFileSystem()
    find = YgFinder(filesystem)

    if option == "-a" or option == "--add":
        find.add_tags(keys)
    elif option == "-d" or option == "--delete":
        find.delete_tags(keys)
    elif option == "-e" or option == "--erase":
        find.erase_all_tags()
    elif option == "-p" or option == "--print":
        find.print(is_recursive=False)
    elif option == "-pr" or option == "--print-recursive":
        find.print(is_recursive=True)
    else:
        error(argv)


def error(argv):
    print("Command line is not correct")
    for arg in argv:
        print(arg)


def main():
    if len(sys.argv) == 1:
        helper = Helper()
        helper.print()
        exit()
    firstArg = sys.argv[1]
    if firstArg == "tag":
        tag(sys.argv)
    elif firstArg == "tag-index":
        tagIndex(sys.argv)
    elif firstArg == "index":
        index(sys.argv)
    elif firstArg == "version":
        version = Version()
        version.print()
    elif firstArg == "environment":
        env = Environment()
        env.print()
    elif firstArg == "folder":
        folder(sys.argv)
    elif firstArg == "help":
        helper = Helper()
        helper.print()
    elif firstArg == "list":
        listTag(sys.argv)
    elif firstArg == "finder":
        finder(sys.argv)
    elif firstArg == "tag-list":
        tagList(sys.argv)
    elif firstArg == "url":
        urler = URLer(sys.argv)
        urler.start()
    elif firstArg == "view":
        view(sys.argv)
    elif firstArg == "ads":
        ads_cleaner(sys.argv)
    elif firstArg == "gc":
        garbage_collector(sys.argv)
    else:
        error(sys.argv)


# Entry point
if __name__ == "__main__":
    main()
