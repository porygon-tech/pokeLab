#!/usr/bin/perl
#PokéLab v1.2 4/1/2019
#Credits: Miguel Roman
use LWP::Simple;
#use lib ".";

=storage
open(DATASET, '>webData.txt');
	$data = get "https://www.smogon.com/dex/sm/pokemon/";
	$data =~ s/<[^>]*>//g;
	print DATASET $data;
close(DATASET);
=cut

open(DATASET, '>pkmnDB.csv');
print DATASET ("NAME;Type 1;Type 2;Ability 1;Ability 2;Ability 3;Ability 4;HP;Atk;Def;SpA;SpD;Spe\n");

	$data = get "https://www.smogon.com/dex/ss/pokemon/";
	$data =~ s/<[^>]*>//g;
#	print $data;





$init = index($data, "pokemon"); #desde la posición init se iniciará la próxima búsqueda de index

while ($init != -1) {
	$init = index($data, "name", $init);
	if ($init != 5) {
		$init +=6;
		$rawDat = substr($data, $init, index($data, "name", $init)-$init);
	}
#processing raw data
	#name
		my @prsDat = split "\"", $rawDat;
		my $name = $prsDat[1];

	#stats
		my @stats;
		my $statID;
		while ($rawDat =~ /(\d+)/g and $statID < 6) {
			push @stats, $1;
			$statID++;
		}

	#typing
		my @types;
		if ($rawDat =~ /\"types\":\[\"(\w+)\"(,\"(\w+)\")?\]/g) {
			@types = ($1, $3);
		}

	#abilities
		my @abilities;
		if ($rawDat =~ /\"abilities\":\[\"((\w+\s?)+)\"(,\"((\w+\s?)+)\")?(,\"((\w+\s?)+)\")?(,\"((\w+\s?)+)\")?\]/g) {
			@abilities = ($1, $4, $7, $10);
		}
			if ($name eq "Magearna") {
				@abilities = ("Soul-Heart","","","");
			}

#debugging console output
#		print $name . ":   @stats" . "\n";
#		print "$name - ". "@types ".":   "."@stats "."\n";
#		print "$name - ". "@abilities "."\n";
#		print $rawDat."\n\n";

#output formatting
		$statFormat = join("\t", @stats);
		$typeFormat = join("\t", @types);
		$abltFormat = join("\t", @abilities);
		print DATASET ("$name\t$typeFormat\t$abltFormat\t$statFormat\n");

	#$dexID++;
}
=cut
close(DATASET);
