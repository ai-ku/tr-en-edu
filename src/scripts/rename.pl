#!/usr/bin/perl

use strict;

my $dirname = $ARGV[0];
opendir my($dh), $dirname or die "Couldn't open dir '$dirname': $!";
my @files = readdir $dh;
closedir $dh;

foreach(@files){
    if (-f $_ ){
	print STDERR "$_\n";
	$_ =~ /^(.*?)_(\w{2}).txt$/;
	`mv $_ $1.txt.$2`;
    }
}
