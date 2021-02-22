import argparse
import sys
import os

class Version:
	major = "0"
	minor = "0"
	patch = "4"
	build = "Feb 23 2021"

	def fullVersion(self):
		return "Mar {self.major}.{self.minor}.{self.patch}, {self.build}"

	def shortVersion(self):
		return "Mar {self.major}.{self.minor}.{self.patch}"

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
		os.remove(path)

	def makeDirectory(self, path):
		try:
			os.mkdir(path)
		except OSError:
			print("Creation of the directory failed" & path)
		
	def currentDirectory(self):
		return os.getcwd()

class Meta:
	metaSuffix = ".plain.mar"

	def __init__(self, fileName):
		self.fileName = fileName
		self.metaFileName = fileName + self.metaSuffix
		self.fileSystem = FileSystem()
		self.syncTags()

# Public API
	def setTags(self, tags):
		print("meta.setTags()")
		self.tags = tags
		self.writeTags()

	def addTags(self, tags):
		print("meta.addTags()")
		self.tags = self.tags + tags
		self.writeTags()

	def listTags(self):
		print("meta.listTags()")
		print("Tags")
		for tag in self.tags:
			print("\t", tag)

# Private

	def writeTags(self):
		print("meta.writeTags()")
		self.fileSystem.writeLinesFile(self.metaFileName, self.tags)

	def readTags(self):
		print("meta.readTags()")
		return self.fileSystem.readLinesFile(self.metaFileName)

	def syncTags(self):
		print("meta.syncTags()")
		if self.fileSystem.isExistFile(self.metaFileName):
			self.tags = self.readTags()
		else:
			self.tags = []


def test():
	fs = FileSystem()
	print("current dir: ", fs.currentDirectory())


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--version", action="version", version="%(prog)s {version}".format(version=__version__))	
	parser.add_argument("command", help="Command: tag, file or index")
	parser.add_argument("-s", "--set", help="Установить теги для файла, файлы в индекс или теги для индекса")
	parser.add_argument("-a", "--add", help="Добавить тег, файл в индекс или теги для индекса")
	parser.add_argument("-d", "--delete", help="Удалить теги, файл из индекса или теги из индекса")
	parser.add_argument("-e", "--erase", help="Удалить все теги, файлы из индекса или теги из индекса")
	parser.add_argument("-l", "--list", help="Получить список тегов, файлов в индексе")
	parser.add_argument("file", help="File name or .")
	return parser.parse_args()

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
	if len(tags) > 0:
		print("Tags:")
		for tag in tags:
			print("	", tag)
	else:
		print("Tags: - ")

	if option == "-s" or option == "--set":
		meta = Meta(file)
		meta.setTags(tags)
	elif option == "-a" or option == "--add":
		meta = Meta(file)
		meta.addTags(tags)
	elif option == "-l" or option == "--list":
		meta = Meta(file)
		meta.listTags()




def main():
	'''
	args = parse_args()
	print(args)
	if args.command == "tag":
		tag()
	elif args.command == "file":
		file()
	elif args.command == "index":
		index()
	else:
		test()
	'''
	
	'''
	if len(sys.argv) < 3:
		raise ValueError('Please, provide valid args')
	'''

	print("Args: ")
	for arg in sys.argv:
		print("	", arg)

	firstArg = sys.argv[1]
	if firstArg == "tag":
		tag(sys.argv)
	elif firstArg == "index":
		index()
	elif firstArg == "version":
		version = Version()
		version.print()
	else:
		error()

if __name__ == "__main__":
	main()

def index():
	print("index()")
