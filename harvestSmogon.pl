#!/usr/bin/perl
#use LWP::Simple;
#use lib ".";
#http://jkorpela.fi/perl/regexp.html
#https://stackoverflow.com/questions/7047790/how-can-i-input-data-into-a-webpage-to-scrape-the-resulting-output-using-python





open(HARVEST, '<tmpFile');
open(RAWCOUNT, '>Rawcount.tsv');
open(ABILITIES, '>Abilities.tsv');
open(ITEMS, '>Items.tsv');
open(SPREADS, '>Spreads.tsv');
open(MOVES, '>Moves.tsv');
open(TEAMMATES, '>Teammates.tsv');
open(CHECKSANDCOUNTERS, '>Checks.tsv');

my $separatorCount = 0;
my $k = 0;
my $modeAbilities = 0;
my $modeItems = 0;
my $modeSpreads = 0;
my $modeMoves = 0;
my $modeTeammates = 0;
my $modeChecks = 0;

sub exitAllModes {
	$modeAbilities = 0;
	$modeItems = 0;
	$modeSpreads = 0;
	$modeMoves = 0;
	$modeTeammates = 0;
	$modeChecks = 0;
	#print CHECKSANDCOUNTERS ("\n");
	return();
}

while (<HARVEST>) {
	$k++;
	my $line = $_;
	if ($line =~ /^\s\+/) { 
		$separatorCount++;
		exitAllModes;
	}else{
		chomp $line;
		$line =~ s/\|//g;
		$line =~ s/\s{3,}//g;

		if ($separatorCount >= 2 || $k == 2) { #new dex entry
			print "\n\n\n\n";
			if ($line =~ /(\w+)/) {
				print $1;
				print RAWCOUNT ($1);
				print CHECKSANDCOUNTERS ("-> " . $1 . "\n");
			}
		}else{
		
			if ($modeChecks == 1) {
				print CHECKSANDCOUNTERS ($line . "\n");
				print "\n" . $line;
			}

			#~~~~~~~~~~~~
			if ($line =~ /Raw count: (\d+)/) {
				print RAWCOUNT ("\t" . $1 ."\n");
			}
			if ($line =~ /Abilities/) {
				$modeAbilities = 1;
			}
			if ($line =~ /Spreads/) {
				$modeSpreads = 1;
			}
			if ($line =~ /Moves/) {
				$modeMoves = 1;
			}
			if ($line =~ /Teammates/) {
				$modeTeammates = 1;
			}
			if ($line =~ /Checks and Counters/) {
				$modeChecks = 1;
			}
		}

		#print $line;


		$separatorCount = 0;

	}
=test
	if ($k > 200) {
		exit;
	}
=cut
}







=d
while (<HARVEST>) {
	my $line = $_;
	chomp $line;

	$k++;
	print ($k . "\t");
	#$line =~ s/<[^>]*>//g;
	#print $line . "\n"

	if ($line =~ /^\+-+/) { 
		$separatorCount++;
		#next;

	}else{
		$line =~ s/\|//g;

		print $line;
		if ($separatorCount > 2 or $k = 2) { #new dex entry
			print "\n";
		}else{
			print "\t";
		}
		$separatorCount = 0;
	}

	if ($k >= 100) {
		exit;
	}

}
close HARVEST;
=cut


















=storage
open(DATASET, '>webData.txt');
	$data = get "https://www.smogon.com/stats/";
	$data =~ s/<[^>]*>//g;
	print DATASET $data;
close(DATASET);
#=cut
=r
open(DATASET, '>pkmnDB.csv');
print DATASET ("NAME;Type 1;Type 2;Ability 1;Ability 2;Ability 3;Ability 4;HP;Atk;Def;SpA;SpD;Spe\n");

	$data = get "https://www.smogon.com/dex/sm/pokemon/";
	$data =~ s/<[^>]*>//g;
=cut