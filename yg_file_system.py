import os
from yg_file_system_object import *


class YgFolder:
	def __init__(self, fullpath):
		self.fullpath = fullpath
		self.name = os.path.basename(self.fullpath)

	def print(self):
		print(self.fullpath)


class YgFileSystem:

	IGNORE_DIR_SUFFIX = [".xcassets", ".lproj", ".xcodeproj", ".xcworkspace"]
	IGNORE_DIR_NAMES = [".git", ".mar", "__pycache__"]

	def cur_folder(self):
		cur_dir = os.curdir
		# print(type(cur_dir))
		# print("cur_dir: " + cur_dir)
		# print("os.path.dirname():" + os.path.dirname(cur_dir))
		# print("os.path.abspath(): " + os.path.abspath(cur_dir))
		# return YgFolder(cur_dir)
		# return YgFolder(os.path.abspath(cur_dir))

		try:
			abspath = os.path.abspath(cur_dir)
			return YgFolder(abspath)
		except PermissionError:
			print("Error. Operation non permited.")
			return None

	def current_folder(self) -> YgFileSystemObject:
		path, name = os.path.split(os.getcwd())
		return YgFileSystemObject(name=name, path=path)

	def fast_scandir(self, dirname):
		subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]

		#print(type(subfolders))
		for dirname in list(subfolders):
			print(dirname)
			subfolders.extend(self.fast_scandir(dirname))
		return subfolders

	def folders(self, folder: YgFolder, recursive: bool = True):
		pathes = [f.path for f in os.scandir(folder.fullpath) if f.is_dir()]

		subfolders = []
		for path in list(pathes):
			newItem = YgFolder(path)
			must_ignored = False
			for ignor_name in YgFileSystem.IGNORE_DIR_NAMES:
				if newItem.name == ignor_name:
					must_ignored = True
					break
			for ignor_suffix in YgFileSystem.IGNORE_DIR_SUFFIX:
				if newItem.name.endswith(ignor_suffix) == True:
					must_ignored = True
					break

			if must_ignored == False:
				subfolders.append(newItem)

		if recursive == True:
			result = subfolders.copy()
			for subfolder in subfolders:
				result.extend(self.folders(subfolder))
			subfolders = result

		return subfolders

	def remove_file(self, path):
		os.remove(path)

	def remove_folder(self, path: str):
		os.rmdir(path=path)

	def is_exist_file(self, file_name: str) -> bool:
		if os.path.isfile(file_name):
			return True
		else:
			return False

	def file_system_object(self, file_name: str):
		"""
		File object from full name.
		:param file_name: full name of file system object
		:return: None or YgFileSystemObject
		"""
		if not self.is_exist_file(file_name=file_name):
			return None

		name = os.path.basename(file_name)
		path = os.path.dirname(file_name)
		return YgFileSystemObject(name=name, path=path)

