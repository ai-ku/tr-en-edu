#!/usr/bin/perl -w
use strict;

# first count
warn "Counting...\n";
my %cnt;
for my $enfile (glob '*.alcmc.en') {
    my $trfile = $enfile; $trfile =~ s/en$/tr/;
    open(EN, $enfile); open(TR, $trfile);
    while(<EN>) {
	my $en = $_;
	my $tr = <TR>;
	chop $en;
	chop $tr;
	$cnt{"$_\t$tr"}++;
    }
    close(EN); close(TR);
}

# then randomly pick dev/test from one counts, 500+500 from each school except itu
my %dev;
my %tst;

warn "Picking...\n";
for my $enfile (glob '*.alcmc.en') {
    next if $enfile =~ /^itu/;
    my $trfile = $enfile; $trfile =~ s/en$/tr/;
    my @devtst; my $cnt;
    open(EN, $enfile); open(TR, $trfile);
    while(<EN>) {
	my $en = $_;
	my $tr = <TR>;
	chop $en;
	chop $tr;
	my $key = "$_\t$tr";
	next if $cnt{$key} > 1;
	$cnt++;
	my $idx = int(rand($cnt));
	if ($idx < 1000) {
	    if (@devtst < 1000) {
		push @devtst, $key;
	    } else {
		# Attempt to replace with existing entry 
		# But make shorter sentences more likely
		my $keylen = scalar(split(' ', $key));
		my $idxlen = scalar(split(' ', $devtst[$idx]));
		if (rand($idxlen**2 + $keylen**2) < $idxlen**2) {
		    $devtst[$idx] = $key;
		}
	    }
	}
    }
    close(EN); close(TR);
    die unless @devtst == 1000;
    for (my $i = 0; $i <= $#devtst; $i++) {
	my $key = $devtst[$i];
	$i % 2 ? $dev{$key}++ : $tst{$key}++;
    }
}

# finally print the trn dev tst files:
warn "Writing...\n";
open(TRNEN, '>trn.en') or die $!;
open(TRNTR, '>trn.tr') or die $!;
open(TSTEN, '>tst.en') or die $!;
open(TSTTR, '>tst.tr') or die $!;
open(DEVEN, '>dev.en') or die $!;
open(DEVTR, '>dev.tr') or die $!;
for my $enfile (glob '*.alcmc.en') {
    my $trfile = $enfile; $trfile =~ s/en$/tr/;
    open(EN, $enfile); open(TR, $trfile);
    while(<EN>) {
	my $en = $_;
	my $tr = <TR>;
	chop $en;
	chop $tr;
	my $key = "$_\t$tr";
	if ($tst{$key}) {
	    print TSTEN "$en\n";
	    print TSTTR "$tr\n";
	} elsif ($dev{$key}) {
	    print DEVEN "$en\n";
	    print DEVTR "$tr\n";
	} else {
	    print TRNEN "$en\n";
	    print TRNTR "$tr\n";
	}
    }
    close(EN); close(TR);
}
close(TRNEN);
close(TRNTR);
close(DEVEN);
close(DEVTR);
close(TSTEN);
close(TSTTR);
