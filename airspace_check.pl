#!/usr/bin/perl
#
# Check to see if a track violates airspace
#
# Needs to be quick/pruned somehow?
# Only check if 'nearby' / every 30 seconds?
# 
# Geoff Wong 2008
#

require DBD::mysql;

use Airspace qw(:all);
use Data::Dumper;

use strict;

#
# Verify an entire task ...
#

if ($#ARGV < 0)
{
    print "airspace_check <tasPk> [<traPk>]\n";
    exit 1;
}

my $traPk;
my $tasPk = 0 + $ARGV[0];

if ($#ARGV == 1)
{
    $traPk = 0 + $ARGV[1];
}

my $tracks;
my $airspace;
my $dist;
my $name;
my $space;

$Airspace::dbh = db_connect();

if ($traPk > 0)
{
    $tracks = get_one_track($traPk);
}
else
{
    $tracks = get_all_tracks($tasPk);
}
#$tracks = [ 13010 ];
#$airspace = find_nearby_airspace($regPk, 100000.0);
$airspace = find_task_airspace($tasPk);
print "Airspaces checked:\n";
foreach $space (@$airspace)
{
    print "   ", cln($space->{'name'}), " with base=", cln($space->{'base'}), "\n";
}

#print Dumper($airspace);
# Go through all the tracks ..
# might be more useful to print the names :-)

for my $track (keys %$tracks)
{
    $dist = 0;
    $name = $tracks->{$track}->{'pilFirstName'} . " " . $tracks->{$track}->{'pilLastName'};
    print "\n$name ($track): ";
    if (($dist = airspace_check($track,$airspace)) > 0)
    {
        print "\n    Maximum violation of $dist metres ($name).";
    }
    else
    {
        print "No violation.";
    }
}
print "\n";



