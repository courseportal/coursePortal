#!/usr/bin/perl


#=== Instructions ===
# There are 3 possible tags, any other tags will be ignored.  You need at least
# one of -setup and -migrate.  Order does not matter
#
# -setup
# This tag sets up a new app(s) for migration if you haven't migrated it before
# It can be used in conjunction with -migrate.
#
# -migrate
# This tag migrates the database for the selected apps.  It can be used in
# conjunction with -setup, in that case it will setup the database then migrate
#
# -print
# When you use this tag the script just prints out the commands to run
# instead of actually running them.
#
# After you select you tags you select the apps that you wish to migrate by
# inputting them as agruments to the script.
#
# Here are a few examples of the command line input:
# ./south -print -setup myapp myapp2
# ./south -setup myapp myapp2
# ./south -setup -migrate myapp myapp2
# ./south -migrate -print myapp
# ./south -migrate -setup -print myapp myapp2 myapp3
# ./south -setup -print -migrate myapp

$echo = "";

foreach $argnum (0 .. $#ARGV)
{
    if (@ARGV[$argnum] eq "-print")
    {
        $echo = "echo ";
        splice(@ARGV, $argnum, 1);
        last;
    }
}

foreach $argnum (0 .. $#ARGV)
{
    if (@ARGV[$argnum] eq "-setup")
    {
        splice(@ARGV, $argnum, 1);
        $command_0 = "$echo" . "./manage.py syncdb";
        print `$command_0`;
        for $arg (0 .. $#ARGV)
        {
            next if (@ARGV[$arg] =~ /^-/); #Skip all tags (beginning w/ '-')
            
            $command_1 = "$echo" . "./manage.py schemamigration " . "@ARGV[$arg]" . " --initial";
            $command_2 = "$echo" . "./manage.py migrate " . "@ARGV[$arg]" . " --fake";
            print `$command_1`;
            print `$command_2`;
        }
        last;
    }
    if (@ARGV[$argnum] ne "-migrate")
    {
        last;
    }
}

if (@ARGV[0] eq "-migrate")
{
    splice(@ARGV, 0, 1);
    for $arg (0 .. $#ARGV)
    {
        next if (@ARGV[$arg] =~ /^-/); #Skip all tags (beginning w/ '-')
        
        $command_1 = "$echo" . "./manage.py schemamigration " . "@ARGV[$arg]" . " --auto";
        $command_2 = "$echo" . "./manage.py migrate " . "@ARGV[$arg]";
        print `$command_1`;
        print `$command_2`;
    }
}