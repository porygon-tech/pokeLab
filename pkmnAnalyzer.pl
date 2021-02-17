use LWP::Simple;
use lib ".";
#use pkmod;
=storage
open(DATASET, '>glance.txt');
	$data = get "https://www.smogon.com/dex/sm/pokemon/";
	$data =~ s/<[^>]*>//g;
	print DATASET $data;
close(DATASET);
=cut

open(DATASET, '>pkmnDB.csv');
print DATASET ("NAME;Type 1;Type 2;Ability 1;Ability 2;Ability 3;Ability 4;HP;Atk;Def;SpA;SpD;Spe\n");

	$data = get "https://www.smogon.com/dex/sm/pokemon/";
	$data =~ s/<[^>]*>//g;

	#my $pattern = qr/"\^\w*\$"/;

$init = index($data, "pokemon"); #desde la posición init se iniciará la próxima búsqueda de index

while ($dexID < 895) {	#Gen7: 895
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
		while ($rawDat =~ /(\d+)/g and $statID < 6) { #lo que queda entre paréntesis estará almacenado en $1
			#print "Word is $1, ends at position ", pos $rawDat, "\n";
			push @stats, $1;
			$statID++;
		}

	#typing
		my @types;
		if ($rawDat =~ /\"types\":\[\"(\w+)\"(,\"(\w+)\")?\]/g) {
			#print "$name - $1 $3\n";
			@types = ($1, $3);
		}

	#abilities
		my @abilities;
		if ($rawDat =~ /\"abilities\":\[\"((\w+\s?)+)\"(,\"((\w+\s?)+)\")?(,\"((\w+\s?)+)\")?(,\"((\w+\s?)+)\")?\]/g) {
			#print "$name - $1 $3\n";
			@abilities = ($1, $4, $7, $10);
		}
			if ($name eq "Magearna") {
				@abilities = ("Soul-Heart","","","");
			}

#debugging console output
		#print $name . ":   @stats" . "\n";
		$statFormat = join(";", @stats);
		$typeFormat = join(";", @types);
		$abltFormat = join(";", @abilities);
		print DATASET ("$name;$typeFormat;$abltFormat;$statFormat\n");
#		print "$name - ". "@types ".":   "."@stats "."\n";
		print "$name - ". "@abilities "."\n";
#		print $rawDat."\n\n";
	

	$dexID++;
}

close(DATASET);


=query
while ($query ne "STOP") {
	$query = <STDIN>;
	chomp $query;
	$finding = index($data, "\"name\":\"".$query);
	$result = substr($data, $finding, index($data, "},", $finding)-$finding+2);
	#$result =~ s/\],/\n/g;
	#$result =~ s/\]//g;
	print $result."\n";
}
=cut

=wfasvzx
		$strL = length($rawDat);
		$ndx = 0;
		while ($ndx < $strL) {
			$ndx = index($rawDat, "\"", $ndx);
			if ($ndx != -1) {
				print(substr($rawDat, $ndx+1, index($rawDat, "\"", $ndx)-$ndx-1));
				$ndx++;
			}else{
				last;
			}


		}
=cut