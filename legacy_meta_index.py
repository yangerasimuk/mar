from legacy_meta import *
from legacy_index import *


class LegacyMetaIndex:

	def __init__(self):
		self.index = LegacyIndex()

	def setTags(self, tags):
		if not self.index.isExistIndex():
			print("Index not exists.")
			return

		for fileName in self.index.listFiles():
			meta = LegacyMeta(fileName)
			meta.set_tags(tags)

	def addTags(self, tags):
		if not self.index.isExistIndex():
			print("Index not exists.")
			return

		for fileName in self.index.listFiles():
			meta = LegacyMeta(fileName)
			meta.add_tags(tags)

	def deleteTags(self, tags):
		if not self.index.isExistIndex():
			print("Index not exists.")
			return

		for fileName in self.index.listFiles():
			meta = LegacyMeta(fileName)
			meta.delete_tags(tags)

	def eraseTags(self):
		if not self.index.isExistIndex():
			print("Index not exists.")
			return

		for fileName in self.index.listFiles():
			meta = LegacyMeta(fileName)
			meta.erase_tags()
