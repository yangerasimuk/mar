from file_system import *

from mar import Constant
from mar import FileSystem
from mar import NameResolver
from mar import Meta

class YgFinder:
	def __init__(self, filesystem: YgFileSystem):
		print("ygFinder.init(filesystem:)")
		self.filesystem = filesystem
		self.oldFileSystem = FileSystem()
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
		#if len(self.tagsInPath) > 0:
		#	self.printTagsInPath()
		#	self.printFiles()
		#else:
		self.printAllTags()



	def printRecursive(self):
		print("finder.printRecursive()")

	def goToFolder(self, hash):
		print("finder.goToFolder()")

	def openFile(self, hash):
		print("finder.openFile")

	# private

	def eraseTags(self):
		if self.oldFileSystem.isExistFile(Constant.TAGS_PATH_FILE_NAME) == True:
			self.oldFileSystem.deleteFile(Constant.TAGS_PATH_FILE_NAME)

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
