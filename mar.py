import sys
import os

class Version:
	major = "0"
	minor = "0"
	patch = "4"
	build = "Feb 23 2021"

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
		os.remove(path)

	def makeDirectory(self, path):
		try:
			os.mkdir(path)
		except OSError:
			print("Creation of the directory failed" & path)
		
	def currentDirectory(self):
		return os.getcwd()

class Meta:
	metaSuffix = ".mar.txt"

	def __init__(self, fileName):
		self.fileName = fileName
		self.metaFileName = fileName + self.metaSuffix
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

		if needSync:
			# print("needSync")
			self.writeTags()

	def eraseTags(self):
		# print("meta.eraseTags()")
		if self.fileSystem.isExistFile(self.metaFileName):
			self.fileSystem.removeFile(self.metaFileName)

	def listTags(self):
		# print("meta.listTags()")
		# print("Tags")
		for tag in self.tags:
			print("\t", tag)

	def metaFileSuffix(self):
		return self.metaSuffix

	def writeTags(self):
		# print("meta.writeTags()")
		self.fileSystem.writeLinesFile(self.metaFileName, self.tags)

	def readTags(self):
		# print("meta.readTags()")
		return self.fileSystem.readLinesFile(self.metaFileName)

	def syncTags(self):
		# print("meta.syncTags()")
		if self.fileSystem.isExistFile(self.metaFileName):
			self.tags = self.readTags()
		else:
			self.tags = []


class Index:
	indexDirectoryName = "./.mar"
	indexFileName = "./.mar/index.mar.txt"
	systemFilePrefix = "."
	metaFileSuffix = ".mar.txt"

	def __init__(self, fileName):
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
			print("file not in index")

	def listFiles(self):
		return self.fileNamesInIndex

	def printFiles(self):
		if len(self.fileNamesInIndex) > 0:
			print("Files in index:")
			for name in self.fileNamesInIndex:
				print("\t" + name)

	def deleteFile(self, name):
		# print("index.deleteFile()")
		if name in self.fileNamesInIndex:
			self.fileNamesInIndex.remove(name)

			if len(self.indexFileName) > 0:
				self.fileSystem.writeLinesFile(self.indexFileName, self.fileNamesInIndex)
			else:
				self.fileSystem.removeFile(self.indexFileName)
		else:
			print("file not in index")

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

class NameResolver:

	def __init__(self, fileName):
		self.fileSystem = FileSystem()
		self.index = Index(fileName)
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
			return NO

		if self.fileName == "." or self.fileName == "..":
			return NO

		if self.fileSystem.isExistDirectory(self.fileName):
			return NO

		if self.fileName.endswith(self.fileSystem.metaFileSuffix):
			return NO

		return YES

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
	elif option == "-l" or option == "--list":
		meta.listTags()

	'''
	elif option == "-p" or option == "--print":
		meta.listTags()
	'''

def index(argv):

	option = argv[2]
	# print("Option: ", option)
	file = ""
	if len(argv) >= 4:
		file = argv[3]
	# print("File: ", file)

	index = Index(file)
	if option == "-s" or option == "--set":
		index.setFile(file)
	elif option == "-a" or option == "--add":
		index.addFile(file)
	elif option == "-d" or option == "--delete":
		index.deleteFile(file)
	elif option == "-e" or option == "--erase":
		index.eraseIndex()
	elif option == "-l" or option == "--list":
		index.listFiles()
	elif option == "-p" or option == "--print":
		index.printFiles()

def main():
	'''
	print("Args: ")
	for arg in sys.argv:
		print("	", arg)
	'''
	firstArg = sys.argv[1]
	if firstArg == "tag":
		tag(sys.argv)
	elif firstArg == "index":
		index(sys.argv)
	elif firstArg == "version":
		version = Version()
		version.print()
	else:
		error()

if __name__ == "__main__":
	main()
