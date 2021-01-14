#require 'pry'; binding.pry

USAGE = <<-ENDUSAGE
Usage:
    mar [-h] [-v] [-t]

ENDUSAGE

HELP = <<-ENDHELP
   -h, --help       Show this help.
   -v, --version    Show the version number.
   -t, --tag		Mark with tags.

ENDHELP

ARGS = { } # Setting default values
UNFLAGGED_ARGS = []              # Bare arguments (no flag)
next_arg = UNFLAGGED_ARGS.first
ARGV.each do |arg|
  case arg
    when '-h','--help'      then ARGS[:help]      = true
    when '-v','--version'   then ARGS[:version]   = true
    when '-t','--tag'	then ARGS[:tag] = true
    else
      if next_arg
        ARGS[next_arg] = arg
        UNFLAGGED_ARGS.delete( next_arg )
      end
      next_arg = UNFLAGGED_ARGS.first
  end
end

if ARGS[:help]
  puts USAGE unless ARGS[:version]
  puts HELP if ARGS[:help]
  exit
end

if ARGS[:version]
  puts "mar version v0.0.1"
end

if ARGS[:tag]
  puts "mark with tags:"
end
