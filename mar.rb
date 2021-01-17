

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

	-af, --add-index	Add file(-s) to index.
	-df, --delete-index	Delete file from index
	-ef, --erase-index	Erase index.
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
		when '-l','--list'			then ARGS[:list]			= true
		when '-af','--add-index'	then ARGS[:add_index]		= true
		when '-df','--delete-index'	then ARGS[:delete_index]	= true
		when '-ef','--erase-index'	then ARGS[:erase_index]		= true
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
	puts "mark file '" + ARGS[:file] +"' with tags:"

	TAGS.each do |tag|


	end

	File.open(ARGS[:file] + ".plain.mar", "w+") do |f|
		TAGS.each { |element| f.puts(element) }
	end
end

if ARGS[:list]
	puts "list tags of file '" + ARGS[:file] + "'"
	a = IO.readlines(ARGS[:file] + ".plain.mar")
	a.each do |tag|
		puts "		" + tag
	end
	exit
end

if ARGS[:delete]
	puts "delete tags for file '" + ARGS[:file] + "'"
	begin
		f = File.open(ARGS[:file] + ".plain.mar", 'r')
	ensure
		if !f.nil? && File.exist?(f)
			f.close unless f.closed?
			File.delete(f)
		end
	end
	exit
end

# Operations with index

if ARGS[:status]
	puts "index:"
	MapIndex.new().status()
	exit
end

if ARGS[:add]
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

if ARGS[:reset]
	puts "reset index"
	MarIndex.new().reset()
	exit
end

if ARGS[:tag-index]
	index = mar_index.new()

end

if ARGS[:delete-index]

end

class MarMeta
	META_SUFFIX = ".plain.mar"

	@@target_file_name
	@@file_system
	@@tags

	def initialize(target_file_name)
		@@target_file_name = target_file_name
		@@file_system = FileSystem.new()
		@@tags = @@file_system.read_lines_file(meta_file_name())
	end

	def mark_tag(tag)
		tags.set = tag
		sync_tags()
	end

	def update_tag(tag)
		if !tags.include?(tag)
			@@tags.add(tag)
			sync_tags()
		end
	end

	def delete(tag)
		if !tags.include?(tag)
			@@tags.delete(tag)
			sync_tags()
		end
	end

	def erase
		if @@file_system.is_exists_file(meta_file_name())
			file_system.remove_file(meta_file_name())
		end
	end

	def list
		tags = @@file_system.lines_file(meta_file_name())
		tags.each do |tag|
			puts "	" + tag
		end
	end

	private

	def meta_file_name
		@@target_file_name + ".plain.mar"
	end

	def sync_tags
		@@file_system.write_lines_file(meta_file_name(), @@tags)
	end
end

class MarIndex
	INDEX_DIRECTORY_NAME = "./.mar"
	INDEX_FILE_NAME = INDEX_DIRECTORY_NAME + "/index.plain.mar"
	file_system :FileSystem

	def initialize
		file_system = FileSystem.new()
		check_index()
	end

	def add_all
		file_names = file_system.files_in_dir()
		file_names.each do |name|
			add_file(name)
		end
	end

	def add_file(name)
		if !is_exists_in_index_file(name)
			File.open(INDEX_FILE_NAME, "w+") do |f|
				f.puts(name)
			end
		end
	end

	def status
		file_names = file_system.file_names_in_index()
		if file_names.count > 0
			file_names.each do |name|
				puts "	name"
			end
		else
			puts "no files"
		end
	end

	def reset
		# добавить подтверждение действия
		file_system.remove_file(INDEX_FILE_NAME)
	end

	private

	def is_exists_in_index_file(name)
		file_names = file_names_in_index()
		return file_names.include?(name)
	end

	def file_names_in_index
		if file_system.is_exists_file(INDEX_FILE_NAME)
			return File.readlines(INDEX_FILE_NAME)
		else
			return Array.new()
		end
	end

	def check_index
		if !file_system.is_exists_directory(INDEX_DIRECTORY_NAME)
			file_system.make_directory(INDEX_DIRECTORY_NAME)
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
		File.readlines(name)
	end

	def write_lines_file(name, lines)
		File.open(name, "w+") do |f|
			lines.each { |line| f.puts(line) }
		end
	end

	def files_in_dir?(name)
		Dir.entries?(name)
	end

	def make_directory(name)
		Dir.mkdir(name)
	end
end
