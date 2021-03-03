import sys
import os

class Constant:
	META_FILE_SUFFIX = ".mar.txt"
	INDEX_DIRECTORY_NAME = "./.mar"
	INDEX_FILE_NAME = "./.mar/index.mar.txt"
	SYSTEM_FILE_PREFIX = "."
	CURRENT_DIRECTORY_NAME = "."
	PARENT_DIRECTORY_NAME = ".."

	# "./.mar/index.mar.txt"

class Version:
	major = "0"
	minor = "0"
	patch = "6"
	build = "Mar 3, 2021"

	def fullVersion(self):
		return "Mar v" + self.major + "." + self.minor + "." + self.patch + ", " + self.build

	def shortVersion(self):
		return "Mar v" + self.major + "." + self.minor + "." + self.patch

	def print(self):
		print(self.fullVersion())

class FileSystem:
	def isExistFile(self, path):
		if os.path.isfile(path):
			return True
		else:
			return False
	
	def isExistDirectory(self, path):
		# print("fileSystem.isExistDirectory()")
		# print("\t" + path)
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
			print("File removed")
		else:
			print("File not exists")

	def makeDirectory(self, path):
		try:
			os.mkdir(path)
		except OSError:
			print("Creation of the directory failed" & path)
		
	def currentDirectory(self):
		return os.getcwd()


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

		return True

class Meta:

	def __init__(self, fileName):
		self.fileName = fileName
		self.metaFileName = fileName + Constant.META_FILE_SUFFIX
		self.fileSystem = FileSystem()
		self.syncTags()

# Public API

	def setTags(self, tags):
		# print("meta.setTags()")
		self.tags = tags
		self.writeTags()

	def addTags(self, tags):
		# print("meta.addTags()")
		self.tags = self.tags + tags
		self.writeTags()

	def deleteTags(self, tags):
		# print("meta.deleteTags()")
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
			print("Meta file removed")
		else:
			print("Meta file not exists")

	def printTags(self):
		if len(self.tags) > 0:
			print("Tags")
			for tag in self.tags:
				print("\t", tag)
		else:
			print("Tags not exists")

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
	indexDirectoryName = "./.mar"
	indexFileName = "./.mar/index.mar.txt"
	#systemFilePrefix = "."
	#metaFileSuffix = ".mar.txt"

	def __init__(self):
		self.fileSystem = FileSystem()

		if self.fileSystem.isExistDirectory(self.indexDirectoryName) == True:
			self.fileNamesInIndex = self.readIndex()
		else:
			self.fileNamesInIndex = []
			self.checkIndexDirectory()

	def setFile(self, name):
		# print("index.setFile()")
		self.fileNamesInIndex = [name]
		self.fileSystem.writeLinesFile(self.indexFileName, self.fileNamesInIndex)

	def addFile(self, name):
		# print("index.addFile()")
		if name not in self.fileNamesInIndex:
			# print(name + " not in index")
			f = open(self.indexFileName, "a+")
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
		# print("index.deleteFile()")
		if name in self.fileNamesInIndex:
			self.fileNamesInIndex.remove(name)

			if len(self.indexFileName) > 0:
				self.fileSystem.writeLinesFile(self.indexFileName, self.fileNamesInIndex)
			else:
				self.fileSystem.removeFile(self.indexFileName)
		else:
			print("File not exists in index")

	def eraseIndex(self):
		# print("index.eraseIndex()")
		self.fileSystem.removeFile(self.indexFileName)

	def readIndex(self):
		if self.fileSystem.isExistFile(self.indexFileName) == True:
			return self.fileSystem.readLinesFile(self.indexFileName)
		else:
			return []

	def checkIndexDirectory(self):
		# print("index.checkIndexDirectory()")
		if self.fileSystem.isExistDirectory(self.indexDirectoryName) == False:
			# print("make index directory")
			self.fileSystem.makeDirectory(self.indexDirectoryName)
		else:
			print("index directory exists yet")

	def isExistIndex(self):
		if self.fileSystem.isExistFile(self.indexFileName):
			return True
		else:
			return False

class MetaIndex:

	def __init__(self):
		self.index = Index()

	def setTags(self, tags):
		print("metaIndex.setTags()")
		if not self.index.isExistIndex():
			print("Index not exists")
			return

		for fileName in self.index.listFiles():
			meta = Meta(fileName)
			meta.setTags(tags)

	def addTags(self, tags):
		print("metaIndex.addTags()")
		if not self.index.isExistIndex():
			print("Index not exists")
			return

		for fileName in self.index.listFiles():
			meta = Meta(fileName)
			meta.addTags(tags)

	def deleteTags(self, tags):
		print("metaIndex.deleteTags()")
		if not self.index.isExistIndex():
			print("Index not exists")
			return

		for fileName in self.index.listFiles():
			meta = Meta(fileName)
			meta.deleteTags(tags)

	def eraseTags(self):
		print("metaIndex.eraseTags()")
		if not self.index.isExistIndex():
			print("Index not exists")
			return

		for fileName in self.index.listFiles():
			meta = Meta(fileName)
			meta.eraseTags()

class Folder:

	def __init__(self):
		self.index = Index()

	def list(self):
		print("folder.list()")
		files = self.files()
		counter = 0
		for file in files:
			print(counter, "\t", file)
			counter = counter + 1

	def addFilesWithIndexes(self, fileIndexes):
		print("folder.addFilesWithIndexes()")
		files = self.files()
		print("count of files ", len(files))
		counter = 0
		for file in files:
			counterStr = str(counter)
			if counterStr in fileIndexes:
				print(counterStr, "\t", file)
				self.index.addFile(file)
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
	print("Option: ", option)

	print("Tags: ")
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
	'''
	if len(tags) > 0:
		print("Tags:")
		for tag in tags:
			print("	", tag)
	else:
		print("Tags: - ")
	'''

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
	print("folder()")

	option = argv[2]
	print("Option: ", option)

	indexes = []
	counter = 3
	while counter < len(argv):
		index = argv[counter]
		# nameResolver = NameResolver()
		indexes.append(index)
		counter = counter + 1

	folder = Folder()
	if option == "-l" or option == "--list":
		folder.list()
	elif option == "-a" or option == "--add":
		folder.addFilesWithIndexes(indexes)


def main():
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
	else:
		error()

if __name__ == "__main__":
	main()
