#!/usr/bin/perl 


use strict;
use Data::Dumper;

my $thr = $ARGV[0];
while(<STDIN>){
    chomp;
    my @l = split("\t");
    $l[0] = $thr if($l[0] > 10);
    for(my $i = 0 ; $i < $l[0] ; $i++){
	print "$l[1]\t$l[2]\n";
    }
}
