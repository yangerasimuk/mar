import datetime
import yg_file_system_object

import os

from spinner import *
from yg_file_system import *
from yg_file_system_object import *
from legacy_constant import *
from legacy_name_resolver import *
from legacy_color import *

from legacy_file_system import *
from legacy_meta import *
from yg_global_funcs import *


class YgFinder:
    def __init__(self, filesystem: YgFileSystem):
        print("ygFinder.init(filesystem:)")
        self.filesystem = filesystem
        self.oldFileSystem = LegacyFileSystem()

        if self.oldFileSystem.isExistDirectory(Constant.MAR_DIRECTORY_NAME) == True:
            self.tagsInPath = self.readTagsPath()
        else:
            self.tagsInPath = []
            self.oldFileSystem.checkDirectory(Constant.MAR_DIRECTORY_NAME)

    def addTags(self, tags):
        print("finder.addTags()")
        for tag in tags:
            if (tag in self.tagsInPath) == False:
                self.tagsInPath.append(tag)
                f = open(Constant.TAGS_PATH_FILE_NAME, "a+")
                f.write(tag + "\n")
                f.close()

    def deleteTags(self, tags):
        print("finder.deleteTags()")
        needSync = False
        for tag in tags:
            if (tag in self.tagsInPath) == True:
                self.tagsInPath.remove(tag)
                needSync = True

        if needSync == True:
            self.oldFileSystem.writeLinesFile(Constant.TAGS_PATH_FILE_NAME, self.tagsInPath)

    def eraseTags(self):
        print("finder.eraseTags()")

    def print(self):
        print("finder.print()")
        self.printAllTags()

    #	@spinner(msg="Elapsed Time")
    def getSubfoldersV2(self, searchPath):
        # Pass dirs with problems, for example, without permissions to read
        try:
            folderNames = [name for name in os.listdir(searchPath) if os.path.isdir(os.path.join(searchPath, name))]

            folders = []
            for name in os.listdir(searchPath):
                fso = YgFileSystemObject(name, searchPath)
                if fso.isDir() and not fso.is_mar_ignore():
                    folders.append(fso)
        except:
            print("Exception of os.listdir in YgFinder.getSubfoldersV2()")
            return

        if len(folderNames) <= 0:
            return []

        subfolders = []
        for folderName in folderNames:
            if folderName not in [".git", ".mar", "Trash"]:
                subfolder = YgFileSystemObject(folderName, searchPath)
                subfolders.append(subfolder)
                tempSubfolders = self.getSubfoldersV2(os.path.join(searchPath, subfolder.name))
                if tempSubfolders is not None:
                    subfolders += tempSubfolders
        return subfolders

    def get_subfolders(self, folder: YgFileSystemObject, is_recursive: bool) -> [YgFileSystemObject]:
        # Проверка на директорию и отстуствию .marignore
        if folder.is_mar_ignore():
            return []

        subfolders = []
        # Pass dirs with problems, for example, without permissions to read
        try:
            for name in os.listdir(folder.fullName()):
                fso = YgFileSystemObject(name, folder.path)
                if fso.isDir() and not fso.is_mar_ignore() and name not in Constant.MAR_IGNORE_DIRECTORY_NAMES:
                    subfolders.append(fso)
        except:
            print("Exception of os.listdir in YgFinder.getSubfoldersV2()")
            return []

        if len(subfolders) <= 0 and not is_recursive:
            return subfolders

        inner_subfolders = []
        for subfolder in subfolders:
            inners = self.get_subfolders(folder=subfolder, is_recursive=True)
            if len(inners) > 0:
                inner_subfolders += inners

        return subfolders + inner_subfolders


    @spinner(msg="Elapsed time")
    def getAllFolders(self, curFolderPath):
        currentFolder = YgFileSystemObject(os.path.basename(curFolderPath), os.path.dirname(curFolderPath))
        if currentFolder.is_mar_ignore():
            return []
        allFolders = [currentFolder]
        subFolders = self.getSubfoldersV2(curFolderPath)
        if subFolders is not None:
            allFolders += subFolders
        return allFolders

    @spinner(msg="Elapsed time")
    def getNonEmptyFolders(self, rawFolders):
        nonEmptyFolders = []
        for folder in rawFolders:
            if folder.hasFiles() == True:
                nonEmptyFolders.append(folder)
        return nonEmptyFolders

    def printRecursive(self):
        print("*")
        print("finder.printRecursive()")
        print("Start:", datetime.datetime.now())

        curFolderPath = os.getcwd()
        print("Current folder:")
        print(curFolderPath)
        #		currentFolder = YgFileSystemObject(os.path.basename(curFolderPath), os.path.dirname(curFolderPath))
        #		folders = self.getSubfoldersV2(curFolderPath)
        #		if folders is not None:
        #			allfolders = [currentFolder] + folders

        print("1. Walking folders tree...")
        allfolders = self.getAllFolders(curFolderPath)

        print("2. Filter non empty folders...")
        nonEmptyFolders = self.getNonEmptyFolders(allfolders)

        if len(nonEmptyFolders) > 0:
            print("Non empty folders count:", len(nonEmptyFolders))
        # print("Folders with files:")
        # for folder in nonEmptyFolders:
        # 	print(folder.fullName(), "-", len(folder.getFiles()), "files")
        else:
            print("Not folders with files.")
            print("Finish:", datetime.datetime.now())
            return

        maredFiles = []
        for i in progressbar(range(len(nonEmptyFolders)), "Computing: ", 40):
            #		for folder in nonEmptyFolders:
            folder = nonEmptyFolders[i]
            files = folder.getFiles()
            for file in files:
                # print("")
                # print("*")
                # print("$", file.fullName())
                # fileName = file.fullName()
                nameResolver = LegacyNameResolver(file.fullName())
                if nameResolver.isValid() and nameResolver.hasMeta():
                    # if nameResolver.isValid():
                    # marFileName = fileName + Constant.META_FILE_SUFFIX
                    # print("meta -", marFileName)
                    # lines = FileSystem().readLinesFile(marFileName)
                    # print(lines)

                    # if os.path.exists(marFileName):
                    # 	print("!!!")
                    maredFiles.append(file)
                # else:
                # 	print("&&&")

        # Отображаем уже выбранные теги
        if len(self.tagsInPath) > 0:
            print("")
            print("Selected tags:")
            print(self.tagsInPath)

        # Применяем фильтр если он есть
        matchedFiles = []
        if len(self.tagsInPath) > 0:
            for file in maredFiles:
                meta = LegacyMeta(file.fullName())
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

        selectedFiles = []
        if len(matchedFiles) > 0:
            selectedFiles = matchedFiles
        elif len(maredFiles) > 0:
            selectedFiles = maredFiles
        else:
            print("Not files for operate")
            print("Finish:", datetime.datetime.now())
            return

        # Собираем все теги с помеченных файлов
        allTags = []
        for file in selectedFiles:
            meta = LegacyMeta(file.fullName())
            tags = meta.readTags()
            for tag in tags:
                if (tag in allTags) == False:
                    allTags.append(tag)
        sortedAllTags = sorted(allTags)

        print("")
        print("Available tags:")
        print(sortedAllTags)

        if len(selectedFiles) > 0:
            print("")
            print("Mared files:")
            for file in selectedFiles:
                print("")
                print(file.name)
                print(file.path)
            # print("\t", file.fullName())
        else:
            print("No mared files.")
            print("Finish:", datetime.datetime.now())
            return

        print("")
        print("Finish:", datetime.datetime.now())

    def goToFolder(self, hash):
        print("finder.goToFolder()")

    def openFile(self, hash):
        print("finder.openFile")

    # private

    def eraseTags(self):
        if self.oldFileSystem.isExistFile(Constant.TAGS_PATH_FILE_NAME) == True:
            self.oldFileSystem.removeFile(Constant.TAGS_PATH_FILE_NAME)

    def readTagsPath(self):
        if self.oldFileSystem.isExistFile(Constant.TAGS_PATH_FILE_NAME) == True:
            return self.oldFileSystem.readLinesFile(Constant.TAGS_PATH_FILE_NAME)
        else:
            return []

    def printTagsInPath(self):
        if len(self.tagsInPath) > 0:
            print("Tags in path:")
            for tag in self.tagsInPath:
                print("\t" + tag)
        else:
            print("Path is not consists any tag")

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

    def mared_files(self, is_recurcive: bool = True):
        print("*")
        start_datetime = datetime.datetime.now()
        print("Start: ", start_datetime)

        curFolderPath = os.getcwd()
        print("Current folder:")
        print(curFolderPath)

        print("1. Walking folders tree...")
        all_folders = self.getAllFolders(curFolderPath)

        print("2. Filter non empty folders...")
        nonEmptyFolders = self.getNonEmptyFolders(all_folders)

        if len(nonEmptyFolders) > 0:
            print("Non empty folders count:", len(nonEmptyFolders))
        # print("Folders with files:")
        # for folder in nonEmptyFolders:
        # 	print(folder.fullName(), "-", len(folder.getFiles()), "files")
        else:
            print("Not folders with files.")
            print("Finish:", datetime.datetime.now())
            return []

        mared_files = []
        for i in progressbar(range(len(nonEmptyFolders)), "Computing: ", 40):
            folder = nonEmptyFolders[i]
            files = folder.getFiles()
            for file in files:
                # print("")
                # print("*")
                # print("$", file.fullName())
                # fileName = file.fullName()
                nameResolver = LegacyNameResolver(file.fullName())
                if nameResolver.isValid() and nameResolver.hasMeta():
                    mared_files.append(file)

        # Отображаем уже выбранные теги
        if len(self.tagsInPath) > 0:
            print("")
            print(Color().GREEN + "Selected tags:" + Color.ENDCOLOR)
            selected_tags = ' '.join(self.tagsInPath)
            print(Color().GREEN + selected_tags + Color.ENDCOLOR)
        else:
            print(Color().GREEN + "No selected tags" + Color.ENDCOLOR)

        # Применяем фильтр если он есть
        matched_files = []
        if len(self.tagsInPath) > 0:
            for file in mared_files:
                file_meta = LegacyMeta(file.fullName())
                file_tags = file_meta.readTags()
                is_match = False
                for tag in self.tagsInPath:
                    if tag in file_tags:
                        is_match = True
                        break
                    else:
                        is_match = False

                if is_match:
                    matched_files.append(file)

        count_of_matched = len(matched_files)
        print(f"Count of matched files: {count_of_matched}")
        selected_files = []
        if len(matched_files) > 0:
            selected_files = matched_files
        elif len(mared_files) > 0 and len(self.tagsInPath) == 0:
            selected_files = mared_files
        else:
            print("No files for operate")
            finish_datetime = datetime.datetime.now()
            delta = finish_datetime - start_datetime
            print(f"Time: {delta.seconds} sec(s)")
            return []

        print("")
        finish_datetime = datetime.datetime.now()
        print("Finish: ", finish_datetime)
        self.print_execution_time(start_datetime, finish_datetime)

        return selected_files

    def print_execution_time(self, start: datetime, finish: datetime):
        delta = finish - start
        if delta.seconds > 0:
            print(Color().PURPLE + f"Execution time: {delta.seconds} sec(s)" + Color.ENDCOLOR)
        else:
            print(Color().PURPLE + f"Execution time: {delta.microseconds} microsec(s)" + Color.ENDCOLOR)
