import argparse
import sys
import os

class Version:
	major = "0"
	minor = "0"
	patch = "3"
	build = "Feb 19 2021"

	def print(self):
		print(f"Mar {self.major}.{self.minor}.{self.patch}, {self.build}")

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
		self.fileSystem = FileSystem()
		self.metaFileName = fileName + self.metaSuffix
		self.tags = []

	def mark(self, tags):
		self.tags = tags
		self.syncTags()

	def syncTags(self):
		print("syncTags()")
		self.fileSystem.writeLinesFile(self.metaFileName, self.tags)

def test():
	fs = FileSystem()
	print("current dir: ", fs.currentDirectory())

'''
def tag():
	print("tag")
def file():
	print("file")
def index():
	print("index")
'''

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

	file = argv[2]
	print("File: ", file)

	tags = []
	counter = 3
	while counter < len(argv):
		tags.append(argv[counter])
		counter = counter + 1

	print("Tags:")
	for tag in tags:
		print("	", tag)

	meta = Meta(file)
	meta.mark(tags)

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

