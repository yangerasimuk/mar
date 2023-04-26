import os
import datetime
from file_system import *
from mar import Constant
from mar import FileSystem
from mar import NameResolver
from mar import Meta

class YgFileSystemObject:
	def __init__(self, name, path):
		self.name = name
		self.path = path

	def fullName(self):
		return os.path.join(self.path, self.name)

	def isDir(self):
		return os.path.isdir(self.fullName())

	def isFile(self):
		return os.path.isfile(self.fullName())

	def hasFiles(self):
		if self.isFile():
			return False

		files = self.getFiles()
		for file in files:
			if file in Constant.SYSTEM_FILES:
				continue
			else:
				return True
		return False

	def getFiles(self):
		if self.isFile():
			return False
		fileNames = [name for name in os.listdir(self.fullName()) if os.path.isfile(os.path.join(self.fullName(), name))]
		objFiles = []
		for fileName in fileNames:
			objFile = YgFileSystemObject(fileName, self.fullName())
			objFiles.append(objFile)
		return objFiles

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
		self.printAllTags()

	def getSubfoldersV2(self, searchPath):
		# Pass dirs with problems, for example, without permissions to read
		try:
			folderNames = [name for name in os.listdir(searchPath) if os.path.isdir(os.path.join(searchPath, name))]
		except:
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

	def printRecursive(self):
		print("*")
		print("finder.printRecursive()")
		print("Start:", datetime.datetime.now())

		curFolderPath = os.getcwd()
		print("Current folder:")
		print(curFolderPath)
		currentFolder = YgFileSystemObject(os.path.basename(curFolderPath), os.path.dirname(curFolderPath))
		folders = self.getSubfoldersV2(curFolderPath)
		if folders is not None:
			allfolders = [currentFolder] + folders

		nonEmptyFolders = []
		for folder in allfolders:
			if folder.hasFiles() == True:
				nonEmptyFolders.append(folder)
				# print("\t", folder.fullName(), "-", len(folder.getFiles()))
		if len(nonEmptyFolders) > 0:
			print("")
			print("Всего непустых папок:", len(nonEmptyFolders))
			# print("Folders with files:")
			# for folder in nonEmptyFolders:
			# 	print(folder.fullName(), "-", len(folder.getFiles()), "files")
		else:
			print("Not folders with files.")
			print("Finish:", datetime.datetime.now())
			return

		maredFiles = []
		for folder in nonEmptyFolders:
			files = folder.getFiles()
			for file in files:
				# print("")
				# print("*")
				# print("$", file.fullName())
				# fileName = file.fullName()
				nameResolver = NameResolver(file.fullName())
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
				meta = Meta(file.fullName())
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
			meta = Meta(file.fullName())
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
