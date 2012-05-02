#!/usr/bin/perl

use strict;
use DBI;

my $dbh = DBI->connect("DBI:mysql:eqitems", "eqitems", "password") || die "Could not create db handle\n";

open(FILE, "< items.txt") or die "Could not open file: $!";
$_ = <FILE>;
chomp;
my @headers = split("(?<!\\\\)\\|", $_);

while (<FILE>) {
  chomp;
  my @field = split("(?<!\\\\)\\|", $_);

  my $statement = 'INSERT INTO items (';

  $statement .= join(',', @headers) .')';

  $statement .= ' VALUES(';

  for (@field) {
    s/\\\|/\|/g;
    $statement .= '"'. $dbh->quote($_) .'",';
    #$statement .= '"'. $_ .'",';
  }

  $statement = substr($statement, 0, -1);
  $statement .= ')';

  $dbh->do($statement);
  #print $statement ."\n";
} 
