#!/usr/bin/env python3

import sys
import os
from typing import List

class Constant:
	META_FILE_SUFFIX = ".mar.txt"
	INDEX_DIRECTORY_NAME = "./.mar"
	INDEX_FILE_NAME = "./.mar/index.mar.txt"
	SYSTEM_FILE_PREFIX = "."
	CURRENT_DIRECTORY_NAME = "."
	PARENT_DIRECTORY_NAME = ".."
	SYSTEM_DIRECTORY_PREFIX = "."
	PYTHON_DIRECTORY_PREFIX = "_"

class Version:
	major = "0"
	minor = "0"
	patch = "10"
	build = "April 4, 2021"
	author = "Yan Gerasimuk"

	def fullVersion(self):
		return "v" + self.major + "." + self.minor + "." + self.patch + " (" + self.build + ")"

	def shortVersion(self):
		return "v" + self.major + "." + self.minor + "." + self.patch

	def print(self):
		print("mar " + self.fullVersion() + ", " + self.author)

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

# class Directory:

# 	def __init__(self, name = None, baseDirectory: Directory = None):
# 		if name is None and baseDirectory is None:
# 			currentDirectory = FileSystem.currentDirectory()
# 			self.name = currentDirectory.name()
# 			self.baseDirectory = currentDirectory.baseDirectory()
# 		elif directory is None:
# 			self.name = name
# 			currentDirectory = FileSystem.currentDirectory()
# 			self.baseDirectory = currentDirectory
# 		else:
# 			self.name = name
# 			self.baseDirectory = baseDirectory

# 		self.fullPath = self.baseDirectory.fullPath + "/" + self.name

# class File:

# 	def __init__(self, name, directory: Directory = None):
# 		self.name = name
# 		if directory is None:
# 			self.directory = FileSystem().currentDirectory()
# 		else:
# 			self.directory = directory
# 		self.fullPath = self.directory.fullPath + "/" + self.name

class FileSystem:
	def isExistFile(self, path):
		if os.path.isfile(path):
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
			print("Creation of the directory failed" & path)


class NameResolver:

	def __init__(self, fileName):
		self.fileSystem = FileSystem()
		self.index = Index()
		self.fileName = fileName

	def names():
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
		if len(self.fileName) == 0:
			return False

		if self.fileSystem.isExistDirectory(self.fileName):
			return False

		if self.fileName == Constant.CURRENT_DIRECTORY_NAME:
			return False

		if self.fileName == Constant.PARENT_DIRECTORY_NAME:
			return False

		if self.fileName.startswith(Constant.SYSTEM_FILE_PREFIX):
			return False

		if self.fileName.endswith(Constant.META_FILE_SUFFIX):
			return False

		if os.path.islink(self.fileName):
			return False
		
		if os.path.ismount(self.fileName):
			return False

		return True

class Meta:

	def __init__(self, fileName):
		self.fileName = fileName
		self.metaFileName = fileName + Constant.META_FILE_SUFFIX
		self.fileSystem = FileSystem()
		self.syncTags()

	def setTags(self, tags):
		self.tags = tags
		self.writeTags()

	def addTags(self, tags):
		self.tags = self.tags + tags
		self.writeTags()

	def deleteTags(self, tags):
		needSync = None
		for tag in tags:
			if tag in self.tags:
				needSync = True
				self.tags.remove(tag)

		if needSync and len(self.tags) != 0:
			self.writeTags()
		elif len(self.tags) == 0:
			self.fileSystem.removeFile(self.metaFileName)

	def eraseTags(self):
		if self.fileSystem.isExistFile(self.metaFileName):
			self.fileSystem.removeFile(self.metaFileName)
			print("Meta file removed.")
		else:
			print("Meta file not exists.")

	def printTags(self):
		if len(self.tags) > 0:
			print("Tags:")
			for tag in self.tags:
				print("\t", tag)
		else:
			print("Tags not exists.")

	def metaFileSuffix(self):
		return Constant.META_FILE_SUFFIX

	def writeTags(self):
		self.fileSystem.writeLinesFile(self.metaFileName, self.tags)

	def readTags(self):
		return self.fileSystem.readLinesFile(self.metaFileName)

	def syncTags(self):
		if self.fileSystem.isExistFile(self.metaFileName):
			self.tags = self.readTags()
		else:
			self.tags = []


class Index:
	indexFileName = "./.mar/index.mar.txt"
	#systemFilePrefix = "."
	#metaFileSuffix = ".mar.txt"

	def __init__(self):
		self.fileSystem = FileSystem()

		if self.fileSystem.isExistDirectory(Constant.INDEX_DIRECTORY_NAME) == True:
			self.fileNamesInIndex = self.readIndex()
		else:
			self.fileNamesInIndex = []
			self.checkIndexDirectory()

	def setFile(self, name):
		# print("index.setFile()")
		self.fileNamesInIndex = [name]
		self.fileSystem.writeLinesFile(Constant.INDEX_FILE_NAME, self.fileNamesInIndex)

	def addFile(self, name):
		# print("index.addFile()")
		if name not in self.fileNamesInIndex:
			# print(name + " not in index")
			f = open(Constant.INDEX_FILE_NAME, "a+")
			f.write(name + "\n")
			f.close()
		else:
			print("File exists in index yet")

	def addFolder(self):
		elements = os.listdir()
		validFiles = []

		print("index.addFolder()")
		print("elements before:")
		for el in elements:
			print("\t" + el)
			resolver = NameResolver(el)
			if resolver.isValid():
				validFiles.append(el)

		print("elements after:")
		for file in validFiles:
			print("\t" + file)
			self.addFile(file)

	def listFiles(self):
		return self.fileNamesInIndex

	def printFiles(self):
		if len(self.fileNamesInIndex) > 0:
			print("File(s) in index:")
			for name in self.fileNamesInIndex:
				print("\t" + name)
		else:
			print("Index is empty")

	def deleteFile(self, name):
		if name in self.fileNamesInIndex:
			self.fileNamesInIndex.remove(name)
			if self.fileNamesInIndex.count > 0:
				self.fileSystem.writeLinesFile(Constant.INDEX_FILE_NAME, self.fileNamesInIndex)
			else:
				self.fileSystem.removeFile(Constant.INDEX_FILE_NAME)
		else:
			print("File not exists in index")

	def eraseIndex(self):
		self.fileSystem.removeFile(Constant.INDEX_FILE_NAME)

	def readIndex(self):
		if self.fileSystem.isExistFile(Constant.INDEX_FILE_NAME) == True:
			return self.fileSystem.readLinesFile(Constant.INDEX_FILE_NAME)
		else:
			return []

	def checkIndexDirectory(self):
		if self.fileSystem.isExistDirectory(Constant.INDEX_DIRECTORY_NAME) == False:
			self.fileSystem.makeDirectory(Constant.INDEX_DIRECTORY_NAME)
		else:
			print("Index directory exists yet.")

	def isExistIndex(self):
		if self.fileSystem.isExistFile(Constant.INDEX_FILE_NAME):
			return True
		else:
			return False

class MetaIndex:

	def __init__(self):
		self.index = Index()

	def setTags(self, tags):
		if not self.index.isExistIndex():
			print("Index not exists.")
			return

		for fileName in self.index.listFiles():
			meta = Meta(fileName)
			meta.setTags(tags)

	def addTags(self, tags):
		if not self.index.isExistIndex():
			print("Index not exists.")
			return

		for fileName in self.index.listFiles():
			meta = Meta(fileName)
			meta.addTags(tags)

	def deleteTags(self, tags):
		if not self.index.isExistIndex():
			print("Index not exists.")
			return

		for fileName in self.index.listFiles():
			meta = Meta(fileName)
			meta.deleteTags(tags)

	def eraseTags(self):
		if not self.index.isExistIndex():
			print("Index not exists.")
			return

		for fileName in self.index.listFiles():
			meta = Meta(fileName)
			meta.eraseTags()

class Folder:

	def __init__(self):
		self.index = Index()

	def print(self):
		files = self.files()
		counter = 0
		for file in files:
			if file in self.index.fileNamesInIndex:
				print(Color().fileNameInIndex() + str(counter) + "\t" + file + Color.ENDCOLOR)
			else:
				print(str(counter) + "\t" + file)
			counter = counter + 1

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
			nameResolver = NameResolver(file)
			if nameResolver.isValid():
				validFiles.append(file)
		return validFiles

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

	metaIndex = MetaIndex()
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
	# print("File: ", file)

	tags = []
	counter = 4
	while counter < len(argv):
		tags.append(argv[counter])
		counter = counter + 1

	meta = Meta(file)

	if option == "-s" or option == "--set":
		meta.setTags(tags)
	elif option == "-a" or option == "--add":
		meta.addTags(tags)
	elif option == "-d" or option == "--delete":
		meta.deleteTags(tags)
	elif option == "-e" or option == "--erase":
		meta.eraseTags()
	elif option == "-p" or option == "--print":
		meta.printTags()

def index(argv):

	option = argv[2]
	# print("Option: ", option)
	file = ""
	if len(argv) >= 4:
		file = argv[3]
	# print("File: ", file)

	index = Index()
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

	folder = Folder()
	if option == "-p" or option == "--print":
		folder.print()
	elif option == "-a" or option == "--add":
		folder.addFilesWithIndexes(indexes)
	elif option == "-d" or option == "--delete":
		folder.removeFilesWithIndexes(indexes)
	elif option == "-o" or option == "--open":
		folder.openFileWithIndex(index)

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

	assert False, "Объект lister не реализован"

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
	elif firstArg == "folder":
		folder(sys.argv)
	elif firstArg == "help":
		helper = Helper()
		helper.print()
	elif firstArg == "list":
		listTag(sys.argv)
	else:
		error()

if __name__ == "__main__":
	main()
