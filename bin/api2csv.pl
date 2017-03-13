#!/usr/bin/env perl
use 5.010;
use strict;
use warnings;
use autodie;
use WWW::Mechanize;
use JSON qw(decode_json);
use Text::CSV_XS qw(csv);

# Quick'n'dirty script that scrapes an API and produces a CSV file.
# Eg: api2csv https://www.humanitarianresponse.info/en/api/v1.0/organizations
# The resulting filename is automatically generated from the endpoint.

my $VERBOSE = 1;

# Argument handling
my ($url) = @ARGV;
$url or die "Usage: $0 url";

# Figure out what we're connecting to.
if ($url !~ /(?<endpoint>\w+)$/) {
    die "Cannot determine API endpoint";
}

# Create a filename and open it for writing.
my $out_file = "$+{endpoint}.csv";
say "Writing to $out_file";
open(my $out_fh, '>', $out_file);

# Let's get ready to scrape.
my $mech = WWW::Mechanize->new( autocheck => 1 );

# @data is where we store each $result.
my (@data, $result);

# Collect all our results
do {
    print STDERR "$url\n" if $VERBOSE;
    $mech->get($url);
    $result = decode_json($mech->content);
    
    push(@data, @{$result->{data}});

    $url = $result->{next}{href};

} while ($url);

# Flatten one layer of sub-keys
# Eg type{id} -> type.id

foreach my $entry (@data) {
    foreach my $key (keys %$entry) {
        if (ref $entry->{$key} eq "HASH") {
            my $sub_entry = delete $entry->{$key};
            foreach my $subkey (keys %$sub_entry) {
                $entry->{"$key.$subkey"} = $sub_entry->{$subkey};
            }
        }
    }
}

# Write our CSV!
csv( in => \@data, out => $out_fh);

say "Done!";
