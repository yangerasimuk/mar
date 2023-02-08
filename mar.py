#!/usr/bin/env python3

import sys
import os
import hashlib
from typing import List
from file_system import *
from finder import *

class Constant:
	META_FILE_SUFFIX = ".mar.txt"
	MAR_DIRECTORY_NAME = "./.mar"
	TAGS_PATH_FILE_NAME = "./.mar/tags.path.mar.txt"

	# Поменять на MAR_DIRECTORY_NAME
	INDEX_DIRECTORY_NAME = "./.mar"
	INDEX_FILE_NAME = "./.mar/index.mar.txt"
	SYSTEM_FILE_PREFIX = "."
	CURRENT_DIRECTORY_NAME = "."
	PARENT_DIRECTORY_NAME = ".."
	SYSTEM_DIRECTORY_PREFIX = "."
	PYTHON_DIRECTORY_PREFIX = "_"

class Version:
	major = "0"
	minor = "1"
	patch = "0"
	build = "Febrary 8, 2023"
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

class Directory:
	def __init__(self, name = None, rootPathAbs = None):
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

	def checkDirectory(self, path):
		if self.isExistDirectory(path) == False:
			self.makeDirectory(path)

#	def currentDir(self):
		

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

	def hasMeta(self):
		metaFileName = self.fileName + Constant.META_FILE_SUFFIX
		if self.fileSystem.isExistFile(metaFileName) == True:
			return True
		else:
			return False
		


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

	def printHash(self):
		files = self.files()
		for file in files:
			fileHashRaw = file.encode('utf-8')
			fileHash = hashlib.sha1(fileHashRaw).hexdigest()
			if file in self.index.fileNamesInIndex:
				print(Color().fileNameInIndex() + fileHash + "\t" + file + Color.ENDCOLOR)
			else:
				print(fileHash + "\t" + file)

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


class Lister:

	def __init__(self):
		self.fileSystem = FileSystem()
		if self.fileSystem.isExistDirectory(Constant.MAR_DIRECTORY_NAME) == True:
			self.tagsInPath = self.readTagsPath()
		else:
			self.tagsInPath = []
			self.fileSystem.checkDirectory(Constant.MAR_DIRECTORY_NAME)

	def addTags(self, tags):
		for tag in tags:
			if (tag in self.tagsInPath) == False:
				self.tagsInPath.append(tag)
				f = open(Constant.TAGS_PATH_FILE_NAME, "a+")
				f.write(tag + "\n")
				f.close()

	def deleteTags(self, tags):
		needSync = False
		for tag in tags:
			if (tag in self.tagsInPath) == True:
				self.tagsInPath.remove(tag)
				needSync = True

		if needSync == True:
			self.fileSystem.writeLinesFile(Constant.TAGS_PATH_FILE_NAME, self.tagsInPath)


	def printTagsInPath(self):
		if len(self.tagsInPath) > 0:
			print("Tags in path:")
			for tag in self.tagsInPath:
				print("\t" + tag)
		else:
			print("Path is not consists any tag")

	def printFiles(self):
		self.printTagsInPath()
		rawFiles = os.listdir()
		sortedFiles = sorted(rawFiles)
		maredFiles = []
		for file in sortedFiles:
			nameResolver = NameResolver(file)
			if nameResolver.isValid() and nameResolver.hasMeta():
				maredFiles.append(file)

		matchedFiles = []
		for file in maredFiles:
			meta = Meta(file)
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

		if len(matchedFiles) > 0:
			innerTags = []
			print("Files for path:")
			for file in matchedFiles:
				print("\t" + file)
				meta = Meta(file)
				#innerTags.extend(meta.tags)
				for tag in meta.tags:
					if not (tag in innerTags):
						innerTags.append(tag)
			if len(innerTags) > 0:
				sortedInnerTags = sorted(innerTags)
				print("InnerTags: ")
				for tag1 in sortedInnerTags:
					print("\t" + tag1)
		else:
			print("Nothing matches for path tags")



	def printFilesRecursive(self):

		self.printTagsInPath()
		rawFiles = os.listdir()
		sortedFiles = sorted(rawFiles)
		maredFiles = []
		for file in sortedFiles:
			nameResolver = NameResolver(file)
			if nameResolver.isValid() and nameResolver.hasMeta():
				maredFiles.append(file)

		matchedFiles = []
		for file in maredFiles:
			meta = Meta(file)
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

		if len(matchedFiles) > 0:
			innerTags = []
			print("Files for path:")
			for file in matchedFiles:
				print("\t" + file)
				meta = Meta(file)
				#innerTags.extend(meta.tags)
				for tag in meta.tags:
					if not (tag in innerTags):
						innerTags.append(tag)
			if len(innerTags) > 0:
				sortedInnerTags = sorted(innerTags)
				print("InnerTags: ")
				for tag1 in sortedInnerTags:
					print("\t" + tag1)
		else:
			print("Nothing matches for path tags")


	def printAllTags(self):
		print("lister.printAllTags()")
		rawFiles = os.listdir()
		sortedFiles = sorted(rawFiles)
		maredFiles = []
		for file in sortedFiles:
			nameResolver = NameResolver(file)
			if nameResolver.isValid() and nameResolver.hasMeta():
				maredFiles.append(file)
			
		allTags = []
		for file in maredFiles:
			meta = Meta(file)
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

	def eraseTags(self):
		if self.fileSystem.isExistFile(Constant.TAGS_PATH_FILE_NAME) == True:
			self.fileSystem.deleteFile(Constant.TAGS_PATH_FILE_NAME)

	def readTagsPath(self):
		if self.fileSystem.isExistFile(Constant.TAGS_PATH_FILE_NAME) == True:
			return self.fileSystem.readLinesFile(Constant.TAGS_PATH_FILE_NAME)
		else:
			return []
	

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
	print("Option: ", option)
	file = argv[3]
	print("File: ", file)

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

def fast_scandir(dirname):
	subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
	for dirname in list(subfolders):
		subfolders.extend(fast_scandir(dirname))
	return subfolders

def finder(argv):
	print("finder(argv)")
	for arg in argv:
		print(arg)

	option = argv[2]
	keys = []

	if len(argv) > 2:
		option = argv[2]
		print("Option: ", option)
		counter = 3
		while counter < len(argv):
			key = argv[counter]
			keys.append(key)
			counter = counter + 1
	
	filesystem = YgFileSystem()
	finder = YgFinder(filesystem)

	if option == "-p" or option == "--print":
		finder.print()
	elif option == "-r" or option == "--print-recursive":
		finder.printRecursive()
	elif option == "-a" or option == "--add":
		finder.addTags(keys)
	elif option == "-d" or option == "--delete":
		finder.deleteTags(keys)
	elif option == "-e" or option == "--erase":
		finder.eraseTags()
	elif option == "-g" or option == "--goto":
		hash = keys.pop()
		finder.goToFolder(hash)
	elif option == "-o" or option == "--open":
		hash = keys.pop()
		finder.openFile(hash)

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
	else:
		error(sys.argv)

# Точка входа	
if __name__ == "__main__":
	main()
