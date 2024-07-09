from legacy_meta import *
from yg_file_system_object import *
import pathlib


class YgMaredFile:
    def __init__(self, fso: YgFileSystemObject):
        self.file = fso
        self.meta = LegacyMeta(self.file.full_name())

    def as_html(self) -> str:
        path = self.file.full_name()
        url = pathlib.Path(self.file.full_name()).as_uri()
        result = "<br />"
        result += "<hr />"
        result += "<br />"
        result += "<h2>" + self.file.name + "</h2>"
        extension = self.file.extension().lower()
        if extension is not None:
            if extension == "jpg" or extension == "jpeg" or extension == "png":
                result += f"<img src='{url}' alt='' height='600' />"
        result += "<p><a href='" + url + "'>" + path + "</a></p>"
        result += "<p>" + "<a href='" + self.file.path + "'>" + self.file.path + "</a></p>"
        result += "<p>" + ''.join(" " + str(x) for x in self.meta.tags) + "</p>"
        # result += "<p>" + self.meta.tags + "</p>"
        return result
