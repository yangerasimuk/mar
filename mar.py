import argparse
import os
from version import __version__

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
		with open(path) as f:
    			lines = [line.rstrip() for line in f]
		return lines

	def writeLinesFile(self, path, lines):
		print("todo")

	def removeFile(self, path):
		os.remove(path)

	def makeDirectory(self, path):
		try:
			os.mkdir(path)
		except OSError:
			print("Creation of the directory failed" & path)
		
	def currentDirectory(self):
		return os.getcwd()

def test():
	fs = FileSystem()
	print("current dir: ", fs.currentDirectory())

def tag():
	print("tag")
def file():
	print("file")
def index():
	print("index")

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--version", action="version", version="%(prog)s {version}".format(version=__version__))	
	parser.add_argument("command", help="Command: tag, file or index")
	parser.add_argument("file", help="File name or .")
	return parser.parse_args()

def main():
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

if __name__ == "__main__":
	main()

