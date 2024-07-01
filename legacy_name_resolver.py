from legacy_file_system import *
#from legacy_index import *
from legacy_constant import *


class LegacyNameResolver:

	def __init__(self, fileName):
		self.fileSystem = LegacyFileSystem()
		#self.index = LegacyIndex()
		self.fileName = fileName

	def names(self):
		names = []
		if self.fileName == ".":
			print("nameResolver.names() with .")
		elif self.fileName == "":
			print("nameResolver.names() with index")
		elif self.isValid(self.fileName):
			return [self.fileName]
		else:
			return []

	def isValid(self):
		# print("isValid()")
		if len(self.fileName) == 0:
			# print("nonValid - null name")
			return False

		# Warning! Не срабатывает для кейса finder'а
		#if self.fileSystem.isExistDirectory(self.fileName):
		#	return False

		if self.fileName == Constant.CURRENT_DIRECTORY_NAME:
			# print("nonValid - current directory name")
			return False

		if self.fileName == Constant.PARENT_DIRECTORY_NAME:
			# print("nonValid - parent directory name")
			return False

		if self.fileName.startswith(Constant.SYSTEM_FILE_PREFIX):
			# print("nonValid - startswith(prefix)")
			return False

		if self.fileName.endswith(Constant.META_FILE_SUFFIX):
			# print("nonValid - endswith(suffix)")
			return False

		if os.path.islink(self.fileName):
#			print("nonValid - islink")
			# return False
			return False

		if os.path.ismount(self.fileName):
			# print("nonValid - ismount")
			return False

		# print("File is valid!")
		return True

	def hasMeta(self):
		metaFileName = self.fileName + Constant.META_FILE_SUFFIX
		if self.fileSystem.isExistFile(metaFileName) == True:
			return True
		else:
			return False
