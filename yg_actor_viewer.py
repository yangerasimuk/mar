import os
import pathlib
import webbrowser
import datetime
from yg_finder import *
from yg_mared_file import *


def sort_file(file: YgFileSystemObject):
    return file.created_datetime()


class YgViewer:
    """
    Класс отвечающий за просмотр информации по тегам.

    Возможно два пути:
    1. Всё делает вьюер
    2. Ему передатся какая-то инфа от других модулей
    """


    def view_with_finder(self, finder: YgFinder):
        files = finder.mared_files()
        files.sort(key=sort_file, reverse=True)
        html = self.html_header()
        if len(files) > 0:
            for file in files:
                mared = YgMaredFile(file)
                html += mared.as_html()
        else:
            html += self.html_no_data()
        html += self.html_footer()

        # Сохраняем html-строку
        fso = YgFileSystemObject(self.view_file_name(), self.view_file_path())
        self.save_html(html, file=fso)

        print(fso.created_datetime())

        # Открыть в браузере
        self.open_file(file=fso)


    def open_file(self, file: YgFileSystemObject):
        webUrl = pathlib.Path(file.fullName()).as_uri()
        webbrowser.open_new(webUrl)


    def save_html(self, html: str, file: YgFileSystemObject):
        # Записать html-строку в файл
        f = open(file.name, "w")
        f.write(html + "\n")
        f.close()


    def html_header(self) -> str:
        html = "<html>"
        html += "<head><meta http-equiv='content-type' content='text/html; charset=utf-8'></head>"
        html += "<body"
        return html


    def html_footer(self) -> str:
        return "</body></html>"

    def html_no_data(self) -> str:
        html = "<h1>Нет данных</h1>"
        html += "<p>Возможно стоит изменить фильтр?</p>"
        return html


    def print_help(self):
        print("Представление замаранных файлов найденные finder'ом в виде html-странички")
        print("\tmar.py view [f]")
        print("\t\t" + "-f или --finder Отобразить список файлов, найденный при помощи finder'a")


    def view_file_name(self) -> str:
        date_time = datetime.datetime.now()
        timestamp = date_time.strftime('%Y-%m-%d_%H-%M-%S')
        return timestamp + "_finder.mar.html"


    def view_file_path(self) -> str:
        fs = YgFileSystem()
        return fs.cur_folder().fullpath
