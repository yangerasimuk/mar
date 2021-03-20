# mar

## Главное
Программа описания других файлов при помощи тегов.

Способ добавления и хранения мета-информации - отдельный файл с названием описываемого файла плюс суффикс *.mar.txt*. Метафайл, должен быть размещен в одноной и той же папке с описываемым файлом.

Пример:
```
IMG_0001.JPG
IMG_0001.JPG.mar.txt
```
## Предусловие
Наличие интерпретатора python.

## Установка
Разместить файл в одной из папок с правами на исполнение.

### Удобства
Скрипт проще всего использовать с алиасами командного интерпретатора, определенными в файле настроек, например, `.zshrc`.

```
# Вывести версию программы
alias marVersion="python3 ~/bin/mar.py version"
# Установить теги для файла
alias marTagSet="python3 ~/bin/mar.py tag -s"
# Добавить теги для файла
alias marTagAdd="python3 ~/bin/mar.py tag -a"
# Удалить тег для файла
alias marTagDelete="python3 ~/bin/mar.py tag -d"
# Удалить все теги для файла
alias marTagErase="python3 ~/bin/mar.py tag -e"
# Вывести теги для файла
alias marTagPrint="python3 ~/bin/mar.py tag -p"

# Установить для всех файлов в индексе теги
alias marTagIndexSet="python3 ~/bin/mar.py tag-index -s"
# Добавить для всех файлов в индексе теги
alias marTagIndexAdd="python3 ~/bin/mar.py tag-index -a"
# Удалить для всех файлов в индексе теги
alias marTagIndexDelete="python3 ~/bin/mar.py tag-index -d"
# Удалить для всех файлов в индексе все теги
alias marTagIndexErase="python3 ~/bin/mar.py tag-index -e"

# Установить в индекс файл
alias marIndexSet="python3 ~/bin/mar.py index -s"
# Добавить в индекс файл
alias marIndexAdd="python3 ~/bin/mar.py index -a"
# Добавить все файлы в текущей папки в индекс
alias marIndexAddAll="python3 ~/bin/mar.py index -f"
# Удалить файл из индекса
alias marIndexDelete="python3 ~/bin/mar.py index -d"
# Удалить индекс
alias marIndexErase="python3 ~/bin/mar.py index -e"
# Вывести все файлы из индексы 
alias marIndexPrint="python3 ~/bin/mar.py index -p"

# Вывести все файлы в текущей папке и присвоить им индекс
alias marFolderPrint="python3 ~/bin/mar.py folder -p"
# Добавить файлы с номерами в индекс
alias marFolderAdd="python3 ~/bin/mar.py folder -a"
# Удалить файлы с номерами из индекса
alias marFolderDelete="python3 ~/bin/mar.py folder -d"
# Открыть файл с номером
alias marFolderOpen="python3 ~/bin/mar.py folder -o"
```
