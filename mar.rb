#require 'pry'; binding.pry
require 'io/console'

USAGE = <<-ENDUSAGE
Usage:
	mar [-h] [-v] [-t] [-s] [-d] file

ENDUSAGE

HELP = <<-ENDHELP
	-h, --help		Show this help.
	-v, --version	Show the version number.
	-t, --tag		Mark with tags.
	-s, --show		Show tags of file.
	-d, --delete	Delete tags.

ENDHELP

TAGS = []
ARGS = { } # Setting default values
UNFLAGGED_ARGS = [ :file ]              # Bare arguments (no flag)
next_arg = UNFLAGGED_ARGS.first
ARGV.each do |arg|
	case arg
		when '-h','--help'		then ARGS[:help]		= true
		when '-v','--version'	then ARGS[:version]		= true
		when '-t','--tag'		then ARGS[:tag]			= true
		when '-s','--show'		then ARGS[:show]		= true
		when '-d','--delete'	then ARGS[:delete]		= true
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

if ARGS[:tag]
	puts "mark file '" + ARGS[:file] +"' with tags:"

	File.open(ARGS[:file] + ".plain.mar", "w+") do |f|
		TAGS.each { |element| f.puts(element) }
	end
end

if ARGS[:show]
	puts "tags of file '" + ARGS[:file] + "'"
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
end
