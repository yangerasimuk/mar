import os
import datetime
from spinner import *
from yg_file_system import *
from yg_file_system_object import *
from yg_file_system_iterator_filter import *
from legacy_name_resolver import *
from legacy_meta import *


class YgFileSystemIterator:
    def __init__(self, file_system: YgFileSystem, root_folder: YgFileSystemObject):
        self.file_system = file_system
        self.current_folder = root_folder

    def go(
            self,
            current_folder: YgFileSystemObject,
            include_filter: YgFileSystemIteratorFilter,
            is_recursive: bool = True,
            is_spinnered: bool = True
    ) -> ([YgFileSystemObject], [YgFileSystemObject]):
        if is_spinnered:
            folders, included_objects = self.iterate_with_spinner(
                self,
                current_folder=current_folder,
                include_filter=include_filter,
                is_recursive=is_recursive
            )
            return folders, included_objects
        else:
            folders, included_objects = self.iterate_without_spinner(
                self,
                current_folder=current_folder,
                include_filter=include_filter,
                is_recursive=is_recursive
            )
            return folders, included_objects

    @spinner(msg="Elapsed time")
    def iterate_with_spinner(
            self,
            current_folder: YgFileSystemObject,
            include_filter: YgFileSystemIteratorFilter,
            is_recursive: bool = True
    ) -> ([YgFileSystemObject], [YgFileSystemObject]):
        folders, included_objects = self.iterate(
            current_folder=current_folder,
            include_filter=include_filter,
            is_recursive=is_recursive
        )
        return folders, included_objects

    def iterate_without_spinner(
            self,
            current_folder: YgFileSystemObject,
            include_filter: YgFileSystemIteratorFilter,
            is_recursive: bool = True
    ) -> ([YgFileSystemObject], [YgFileSystemObject]):
        folders, included_objects = self.iterate(
            current_folder=current_folder,
            include_filter=include_filter,
            is_recursive=is_recursive
        )
        return folders, included_objects

    def iterate(
            self,
            current_folder: YgFileSystemObject,
            include_filter: YgFileSystemIteratorFilter,
            is_recursive: bool = True
    ) -> ([YgFileSystemObject], [YgFileSystemObject]):
        # Result
        subfolders = []
        include_objects = []

        # Check file system object is directory and not ignored
        if not current_folder.is_dir() and current_folder.is_mar_ignore():
            return []

        # Pass dirs with problems, for example, without permissions to read
        try:
            for name in os.listdir(current_folder.full_name()):
                fso = YgFileSystemObject(name, current_folder.full_name())

                if include_filter.is_match(fso):
                    include_objects.append(fso)

                # print(f"\t\tpath: {fso.full_name()}")
                if not fso.is_dir():
                    # print("\t\tpass is NOT dir")
                    has_files = True
                    continue
                if fso.is_mar_ignore():
                    # print("\t\tpass is mar_ignore")
                    continue
                if name in Constant.MAR_IGNORE_DIRECTORY_NAMES:
                    # print("\t\tpass name in ignore mames")
                    continue
                # print("\tfso append!")
                subfolders.append(fso)
                # if fso.is_dir() and not fso.is_mar_ignore() and name not in Constant.MAR_IGNORE_DIRECTORY_NAMES:
                #     print(" - append")
                #     subfolders.append(fso)
                # else:
                #     print(" - no append!")
        except:
            # print("Exception of os.listdir in YgFinder.getSubfoldersV2()")
            return [], []

        if not is_recursive:
            return subfolders, include_objects

        inner_subfolders = []
        for subfolder in subfolders:
            tuple_subfolders, tuple_include_objects = self.iterate(
                current_folder=subfolder,
                include_filter=include_filter,
                is_recursive=True
            )
            if len(tuple_subfolders) > 0:
                inner_subfolders += tuple_subfolders
            if len(tuple_include_objects) > 0:
                include_objects += tuple_include_objects

        return subfolders + inner_subfolders, include_objects
