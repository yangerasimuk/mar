#!/usr/bin/env python3

import json
import uuid
import hashlib
from datetime import datetime
from urllib.parse import urlparse

class URLer:
	def __init__(self, argv = None):
		if argv is None:
			print("argv is None")
		print(argv)
		for arg in argv:
			print(arg)
		# print(url, text, fileName)

	def start(self):
		print("urler.start()")
		url = input("Enter URL:")
		if len(url) == 0:
			return
		text = input("Enter text: ")
		if len(text) == 0:
			text = url
		fileName = input("Enter file name: ")
		if fileName is None:
			o = urlparse(url)
			fileName = o.hostname
			print(fileName) 
		urlO = YgURL(url, text)

		# string1 = json.JSONEncoder().encode(urlO)
		# print(string1)

		# jsonObj = json.dump(urlO.toJSON())

		# print(jsonObj)
		# jsonFormatted = json.loads(jsonString)
		# print(jsonFormatted)
		# jsonV2 = json.dumps(jsonFormatted)
		
		name = YgFileName(fileName, "URL", "json")

		with open(name.name(), 'w') as fp:
			# fp.write(eval)
			json.dump(urlO.toJSON(), fp)

		with open(name.name(), 'r') as fp1:
			jsonX = json.load(fp1)
			print(type(jsonX))
			print(jsonX)
			# jsonX1 = json.loads(jsonX)
			# print(jsonX1)

		

class YgURL:
	def __init__(self, url, text):
		self.url = url
		self.text = text
		self.uid = YgUniqueIdentificator(url)

	def toJSON(self):
		"""Конвертация объекта в JSON-словарь.
		Именно словарь, а не python-строку. Так красивее будет смотреться в файле на диске."""
		jsonString = json.dumps(self, default=lambda o: o.__dict__)
		return json.loads(jsonString)

class YgUniqueIdentificator:
	def __init__(self, text):
		self.text = text
		self.uuid = str(uuid.uuid4())
		self.timestamp = str(datetime.now())
		self.hash = hashlib.md5((self.text+self.uuid+self.timestamp).encode('utf')).hexdigest()

class YgFileName:
	def __init__(self, text, suffix, extension):
		self.text = text
		self.suffix = suffix
		self.extension = extension
		self.prefix = datetime.now().strftime("%Y-%m-%d")

	def name(self):
		return self.prefix + ", " + self.text + ", " + self.suffix + "." + self.extension
