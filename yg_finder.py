import os
import datetime
from yg_file_system_iterator import *
from yg_file_system_iterator_filter import *
from legacy_name_resolver import *
from legacy_color import *
from legacy_meta import *


class YgFinder:
    def __init__(self, filesystem: YgFileSystem):
        # print("ygFinder.init(filesystem:)")
        self.filesystem = filesystem
        self.oldFileSystem = LegacyFileSystem()

        if self.oldFileSystem.isExistDirectory(Constant.MAR_DIRECTORY_NAME):
            self.tags_in_path = self.read_tags_in_path()
        else:
            self.tags_in_path = []
            self.oldFileSystem.checkDirectory(Constant.MAR_DIRECTORY_NAME)

    def read_tags_in_path(self):
        if self.oldFileSystem.isExistFile(Constant.TAGS_PATH_FILE_NAME):
            return self.oldFileSystem.readLinesFile(Constant.TAGS_PATH_FILE_NAME)
        else:
            return []

    def add_tags(self, tags):
        if not type(tags) is list and len(tags) == 0:
            print("Tags in wrong format or empty.")
            return

        f = open(Constant.TAGS_PATH_FILE_NAME, "a+")
        for tag in tags:
            if (tag in self.tags_in_path) == False:
                self.tags_in_path.append(tag)
                f.write(tag + "\n")
        f.close()

    def delete_tags(self, tags):
        need_sync = False
        for tag in tags:
            if tag in self.tags_in_path:
                self.tags_in_path.remove(tag)
                need_sync = True

        if need_sync:
            self.oldFileSystem.writeLinesFile(Constant.TAGS_PATH_FILE_NAME, self.tags_in_path)

    def erase_all_tags(self):
        if self.oldFileSystem.isExistFile(Constant.TAGS_PATH_FILE_NAME):
            self.oldFileSystem.removeFile(Constant.TAGS_PATH_FILE_NAME)

    def tags_from_mared_files(self, mared_files: [YgFileSystemObject]) -> list[str]:
        tags = set()
        for file in mared_files:
            meta = LegacyMeta(file.full_name())
            tags.update(meta.tags)
        result = list(tags)
        result.sort()
        return result

    def mared_files(self, is_recursive: bool = False) -> [YgFileSystemObject]:
        current_folder = YgFileSystem().current_folder()
        iterator = YgFileSystemIterator(
            file_system=YgFileSystem(),
            root_folder=current_folder
        )

        include_filter = None
        if len(self.tags_in_path) > 0:
            include_filter = YgIteratorFilterMarSelectedFiles(tags=self.tags_in_path)
        else:
            include_filter = YgIteratorFilterMarFiles()

        folders, mared_files = iterator.iterate_without_spinner(
            current_folder=current_folder,
            include_filter=include_filter,
            is_recursive=is_recursive
        )

        return mared_files

    def print(self, is_recursive: bool = False):
        # Estimate time of execute
        start_datetime = datetime.datetime.now()

        current_folder = YgFileSystem().current_folder()
        iterator = YgFileSystemIterator(
            file_system=YgFileSystem(),
            root_folder=current_folder
        )

        self.print_selected_tags()

        # Form include filter
        include_filter = None
        if len(self.tags_in_path) > 0:
            include_filter = YgIteratorFilterMarSelectedFiles(tags=self.tags_in_path)
        else:
            include_filter = YgIteratorFilterMarFiles()

        print("")
        print("Folder tree walk...")
        folders, mared_files = iterator.iterate_with_spinner(
            current_folder=current_folder,
            include_filter=include_filter,
            is_recursive=is_recursive
        )

        # Print tags of mared files with filter or all
        available_tags = self.tags_from_mared_files(mared_files=mared_files)
        self.print_tags_of_mared_files(include_tags=available_tags, exclude_tags=self.tags_in_path)

        # Print mared files
        self.print_mared_files(mared_files=mared_files)

        # Print elapsed time
        self.print_execution_time(start=start_datetime, finish=datetime.datetime.now())

    def print_execution_time(self, start: datetime, finish: datetime):
        print("")
        print(f"Start:  {start}")
        print(f"Finish: {finish}")

        delta = finish - start
        if delta.seconds > 0:
            print(Color().PURPLE + f"Elapsed time: {delta.seconds} sec(s)" + Color.ENDCOLOR)
        elif delta.microseconds:
            print(Color().PURPLE + f"Elapsed time: {delta.microseconds} microsec(s)" + Color.ENDCOLOR)

    def print_selected_tags(self):
        print(Color().GREEN)
        print("")
        if len(self.tags_in_path) > 0:
            print("Selected tags:")
            print(self.tags_in_path)
        else:
            print("No selected tags.")
        print(Color.ENDCOLOR)

    def print_tags_of_mared_files(self, include_tags: list[str], exclude_tags: list[str]):
        print(Color().GREEN)
        if len(include_tags) > 0:
            selected = set()
            for tag in include_tags:
                if tag not in exclude_tags:
                    selected.add(tag)
            result = list(selected)
            result.sort()
            print("Available tags:")
            print(result)

        else:
            print("No available tags.")
        print(Color.ENDCOLOR)

    def print_mared_files(self, mared_files: [YgFileSystemObject]):
        print(Color().BLUE)
        if len(mared_files) > 0:
            print("Mared files:")
            counter = 0
            for file in mared_files:
                if counter != 0:
                    print("")
                print(file.name)
                print(file.path)
                counter += 1
        else:
            print("No mared files.")
        print(Color.ENDCOLOR)
