#!/usr/bin/env python3

import argparse
from version import __version__

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

if __name__ == "__main__":
	main()

