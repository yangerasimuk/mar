

USAGE = <<-ENDUSAGE
Usage:
	mar [-h] [-v] [-mt] [-ut] [-dt] [-et] [-lt] [-af] [-df] [-ef] [-sf] [-mi] [-ui] [-di] [-ei] file [tags...]

ENDUSAGE

HELP = <<-ENDHELP
	-h, --help			Show this help.
	-v, --version		Show the version number.

	-mt, --mark			Mark file with tags.
	-ut, --update		Mark file with tag, in additional with exist tags.
	-dt, --delete		Delete tag of file.
	-et, --erase		Erase file from all tags.
	-lt, --list			List tags of file.

	-af, --add-file		Add file(-s) to index.
	-df, --delete-file	Delete file from index
	-ef, --erase-file	Erase index.
	-sf, --status		Status of index.

	-mi, --mark-index	Mark files in index with tags.
	-ui, --update-index	Mark files in index with tag, in addtional with exist tags
	-di, --delete-index	Delete tags from files in index.
	-ei, --erase-index	Erase all tags from files in index.

ENDHELP

TAGS = []
ARGS = { } # Setting default values
UNFLAGGED_ARGS = [ :file ]              # Bare arguments (no flag)
next_arg = UNFLAGGED_ARGS.first
ARGV.each do |arg|
	case arg
		when '-h','--help'			then ARGS[:help]			= true
		when '-v','--version'		then ARGS[:version]			= true
		when '-mt','--mark'			then ARGS[:mark]			= true
		when '-ut','--update'		then ARGS[:update]			= true
		when '-dt','--delete'		then ARGS[:delete]			= true
		when '-et','--erase'		then ARGS[:erase]			= true
		when '-lt','--list'			then ARGS[:list]			= true
		when '-af','--add-file'		then ARGS[:add_file]		= true
		when '-df','--delete-file'	then ARGS[:delete_file]		= true
		when '-ef','--erase-file'	then ARGS[:erase_file]		= true
		when '-sf','--status'		then ARGS[:status]			= true
		when '-mi','--mark-index'	then ARGS[:mark_index]		= true
		when '-ui','--update-index'	then ARGS[:update_index]	= true
		when '-di','--delete-index' then ARGS[:delete_index]	= true
		when '-ei','--erase-index'	then ARGS[:erase_index]		= true
	else
		if next_arg
			ARGS[next_arg] = arg
			UNFLAGGED_ARGS.delete( next_arg )
			next_arg = UNFLAGGED_ARGS.first
		else
			TAGS << arg
		end
#		next_arg = UNFLAGGED_ARGS.first
	end
end

class MarMeta
	META_SUFFIX = ".plain.mar"

	@@target_file_name
	@@file_system
	@@tags

	def initialize(target_file_name)
		@@target_file_name = target_file_name
		@@file_system = FileSystem.new()
		@@tags = tags_in_meta_file()
	end

	def mark_tags(tags)
		if tags.count == 0
			return
		end
		@@tags = tags
		sync_tags()
	end

	def update_tags(tags)
		need_sync = false
		tags.each do |tag|
			if !@@tags.include?(tag)
				@@tags.push(tag)
				need_sync = true
			end
		end

		if need_sync
			sync_tags()
		end
	end

	def delete_tags(tags)
		need_sync = false
		tags.each do |tag|
			if @@tags.include?(tag)
				@@tags.delete(tag)
				need_sync = true
			end
		end

		if need_sync
			sync_tags()
		end
	end

	def erase_tags
		if @@file_system.is_exists_file(meta_file_name())
			file_system.remove_file(meta_file_name())
		end
	end

	def tags
		return @@tags
	end

	private

	def meta_file_name
		@@target_file_name + ".plain.mar"
	end

	def sync_tags
		@@file_system.write_lines_file(meta_file_name(), @@tags)
	end

	def tags_in_meta_file
		if @@file_system.is_exists_file(meta_file_name())
			return File.readlines(meta_file_name(), chomp: true)
			# File.readlines("/path/to/file", chomp: true)
		else
			return Array.new()
		end
	end
end

class MarIndex

	INDEX_DIRECTORY_NAME = "./.mar"
	INDEX_FILE_NAME = INDEX_DIRECTORY_NAME + "/index.plain.mar"
	SYSTEM_FILE_PREFIX = "."
	META_FILE_SUFFIX = ".plain.mar"

	@@file_system

	def initialize
		@@file_system = FileSystem.new()
		check_index()
	end

	def add_all
		file_names = @@file_system.files_in_dir(".")
		file_names.each do |name|
			puts "	" + name
			add_file(name)
		end
	end

	def add_file(name)
		puts "#1"
		if !is_exists_in_index_file?(name)
			"#2"
			File.open(INDEX_FILE_NAME, "a") do |f|
				f.puts(name)
			end
		end
	end

	def delete_file(name)
		if is_exists_in_index_file(name)
			file_names = file_names_in_index()
			puts "#1"
			file_names.each do |name|
				puts "	" + name
			end
			file_names.delete(name)
			puts "#2"
			file_names.each do |name|
				puts "	" + name
			end

			if file_names.empty?
				@@file_system.truncate_file(INDEX_FILE_NAME)
			else
				file_names.each do |name|
					add_file(name)
				end
			end
		else
			puts "no this file in index"
		end
	end

	def status
		file_names = file_names_in_index()
		if !file_names.empty?
			file_names.each do |name|
				puts "	" + name
			end
		else
			puts "	no files"
		end
	end

	def erase
		# добавить подтверждение действия
		@@file_system.remove_file(INDEX_FILE_NAME)
	end

	def file_names
		names = file_names_in_index()
		names.each do |name|
			puts "		#" + name
		end
		return names
	end

	private

	def is_exists_in_index_file?(name)
		puts "marIndex.is_exists_in_index_file()"
		file_names = file_names_in_index()
		return file_names.include?(name)
	end

	def file_names_in_index
		puts "marIndex.file_names_in_index()"
		if @@file_system.is_exists_file(INDEX_FILE_NAME)
			return File.readlines(INDEX_FILE_NAME, chomp: true)
			# chomp: true
		else
			return Array.new()
		end
	end

	def check_index
		if !@@file_system.is_exists_directory?(INDEX_DIRECTORY_NAME)
			@@file_system.make_directory(INDEX_DIRECTORY_NAME)
		end
	end
end

class FileSystem

	def is_exists_file(name)
		begin
			f = File.open(name, 'r')
		ensure
			if !f.nil? && File.exist?(f)
				f.close unless f.closed?
				return true
			else
				return false
			end
		end
	end

	def is_exists_directory?(name)
		File.directory?(name)
	end

	def remove_file(name)
		begin
			f = File.open(name, "r")
		ensure
			if !f.nil? && File.exist?(f)
				f.close unless f.closed?
				File.delete(f)
			end
		end
	end

	def read_lines_file(name)
		File.readlines(name, chomp: true)
	end

	def write_lines_file(name, lines)
		File.open(name, "w+") do |f|
			lines.each { |line| f.puts(line) }
		end
	end

	def files_in_dir(name)
		file_names = Dir.entries(name)
		if file_names.empty?
			return Array.new()
		else
			valid_names = Array.new()
			file_names.each do |name|
				if !name.start_with? "."
					if !name.end_with? ".plain.mar"
						valid_names << name
					end
				end
			end
			return valid_names
		end
	end

	def make_directory(name)
		Dir.mkdir(name)
	end

	def truncate_file(name)
		File.open(name, 'w') { |file| file.truncate(0) }
	end
end

# Entry points

if ARGS[:help]
	puts USAGE unless ARGS[:version]
	puts HELP if ARGS[:help]
	exit
end

if ARGS[:version]
	puts "mar version v0.0.1"
	exit
end

if ARGS[:mark]
	puts "mark file '" + ARGS[:file] + "' with tags:"
	TAGS.each do |tag|
		puts "	" + tag
	end
	meta = MarMeta.new(ARGS[:file])
	meta.mark_tags(TAGS)
end

if ARGS[:update]
	puts "update file'" + ARGS[:file] + "' with tags:"
	meta = MarMeta.new(ARGS[:file])
	meta.update_tags(TAGS)
end

if ARGS[:delete]
	puts "delete tags for file '" + ARGS[:file] + "':"
	TAGS.each do |tag|
		puts "	" + tag
	end
	meta = MarMeta.new(ARGS[:file])
	meta.delete_tags(TAGS)
	exit
end

if ARGS[:erase]
	puts "erase all tags from file '" + ARGS[:file] + "'"
	meta = MarMeta.new(ARGS[:file]).erase_tags()
end

if ARGS[:list]
	# проверка на нулевое имя
	puts "list tags of file '" + ARGS[:file] + "'"
	meta = MarMeta.new(ARGS[:file])
	meta.tags.each do |tag|
		puts "	" + tag
	end
	exit
end

if ARGS[:status]
	puts "files in index:"
	MarIndex.new().status()
	exit
end

if ARGS[:add_file]
	index = MarIndex.new()
	if ARGS[:file] == "."
		puts "add all files in directory to index"
		index.add_all()
	else
		puts "add file '" + ARGS[:file] +"' to index"
		index.add_file(ARGS[:file])
	end
	exit
end

if ARGS[:delete_file]
	puts "delete file '" + ARGS[:file] + "' from index"
	MarIndex.new().delete_file(ARGS[:file])
	exit
end

if ARGS[:erase_file]
	puts "erase index"
	MarIndex.new().erase()
	exit
end

if ARGS[:status]
	index = mar_index.new()
	MarIndex.status()
	exit
end

if ARGS[:mark_index]
	TAGS.each do |tag|
		puts "	" + tag
	end

	# crutch - имя файла здесь тоже тег :)
	TAGS.push(ARGS[:file])

	index = MarIndex.new()
	file_names = index.file_names()
	file_names.each do |name|
		puts "		" + name
		meta = MarMeta.new(name)
		meta.mark_tags(TAGS)
	end
	exit
end

if ARGS[:update_index]
	index = MarIndex.new()
	index.file_names().each do |name|
		meta = MarMeta.new(name)
		meta.update_tags(TAGS)
	end
	exit
end

if ARGS[:delete_index]
	index = MarIndex.new()
	index.file_names().each do |name|
		meta = MarMeta.new(name)
		meta.delete_tags(TAGS)
	end
	exit
end

if ARGS[:erase_index]
	index = MarIndex.new()
	index.file_names().each do |name|
		meta = MarMeta.new(name)
		meta.erase_tags
	end
	exit
end
