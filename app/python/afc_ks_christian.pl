#! /usr/bin/perl -w

use strict;
use warnings;
use Encode;
use POSIX;
use Sys::Hostname;

## constants / parameters

my $max_size_of_neighborhood_cluster = 200;

## main items;

my %terms = ();
my %species = ();
my %proteins = ();

## shorthands

my %shorthand_of_protein = ();
my %protein_of_shorthand = ();
my %shorthand_of_term = ();
my %term_of_shorthand = ();
my %description_of_term = ();

## features, connections:

my %proteins_per_species_per_term = ();
my %proteins_per_species = ();
my %species_of_protein = ();
my %genes_per_protein = ();
my %preferred_name_of_protein = ();
my %aliases_per_protein = ();
my %proteins_per_alias = ();
my %annotation_of_protein = ();
my %description_lines_per_protein = ();
my %function_line_of_protein = ();
my %official_name_of_species = ();
my %compact_name_of_species = ();
my %type_of_species = ();
my %kingdom_of_species = ();
my %size_of_protein = ();
my %sequence_of_protein = ();
my %end_position_of_gene = ();
my %orientation_of_gene = ();
my %counts_per_species_per_orthgroup = ();

###############################################################################################
## get the organisms we are to work with
###############################################################################################

print STDERR "learning about the organisms ...";
open (FH, "species.names.txt") or die "cannot read file 'species.names.txt'!\n";
while (<FH>) {
 chomp;
 next if /\A\#/;
 my ($taxon, $type, $name_official, $name_compact) = split /\t/;
 my $type_compact = "periphery";
 $type_compact = "core" if $type =~ /core/;
 $type_compact = "adherent" if $type =~ /adherent/;
 $official_name_of_species{$taxon} = $name_official;
 $compact_name_of_species{$taxon} = $name_compact;
 $type_of_species{$taxon} = $type_compact;
 $species{$taxon} = 1;
}
print STDERR "done.\n";

##############################################################################################
## next learn about protein identifiers, and shorthands
##############################################################################################

print STDERR "now processing 'species.lookup' ... ";
open (FH, "species.lookup") or die "cannot open inputfile 'species.lookup'\n";
while (<FH>) {
 chomp;
 next if /\A\#/;
 my ($identifier, $species) = split;
 my $protein = "$species.$identifier";
 $proteins{$protein} = 1;
 $species_of_protein{$protein} = $species;
 $proteins_per_species{$species}{$protein} = 1;
 print STDERR " warning: unclear species '$species' in species.lookup!\n" unless exists $species{$species};
}
close FH;
print STDERR "done.\n";

print STDERR "now reading protein-shorthands ...";
open (FH, "protein.shorthands.txt") or die "cannot read file 'protein.shorthands.txt'!\n";
while (<FH>) {
 chomp;
 next if /\A\#/;
 my ($protein, $shorthand) = split;
 unless (exists $proteins{$protein}) {
     warn "WARNING: unknown protein '$protein' in file 'protein.shorthands.txt'!\n";
 }
 $shorthand_of_protein{$protein} = $shorthand;
}
print STDERR "done.\n";

##############################################################################################
## next, learn about terms and their memberships, and print to stdout.
##############################################################################################

mkdir "$ENV{OUTPUT_DIR}/global_enrichment_data/";

my $term_shorthand = 1;

foreach my $taxon (sort {$a <=> $b} keys %species) {

 print STDERR "now trying organism '$taxon' ...\n";

 mkdir "$ENV{OUTPUT_DIR}/global_enrichment_data/";
 my $output_filename_term_members = "$ENV{OUTPUT_DIR}/global_enrichment_data/$taxon.terms_members.tsv";
 open (FH_OUT_MEMBERS, "> $output_filename_term_members") or die "cannot write to file '$output_filename_term_members'\n";
 my $output_filename_term_descriptions = "$ENV{OUTPUT_DIR}/global_enrichment_data/$taxon.terms_descriptions.tsv";
 open (FH_OUT_DESCRIPTIONS, "> $output_filename_term_descriptions") or die "cannot write to file '$output_filename_term_descriptions'\n";
 my $output_filename_term_children = "$ENV{OUTPUT_DIR}/global_enrichment_data/$taxon.terms_children.tsv";
 open (FH_OUT_CHILDREN, "> $output_filename_term_children") or die "cannot write to file '$output_filename_term_children'\n";

 my $terms_filename = "classification/agotool_annotations/$taxon"."_AFC_KS_all_terms.tsv";
 unless (-e $terms_filename) {
     print STDERR "   file not found: '$terms_filename' - skipping taxon.\n";
     next;
 }

 my $terms_lineage_filename = "classification/agotool_annotations/$taxon"."_AFC_KS_all_terms_lineage.tsv";
 unless (-e $terms_lineage_filename) {
     print STDERR "   file not found: '$terms_lineage_filename' - skipping taxon.\n";
     next;
 }

 my $clusters_filename = "classification/string_neighborhood_clusters/$taxon.al.simpLeafs5.named.F1.forEnrich";
 unless (-e $clusters_filename) {
     print STDERR "   file not found: '$clusters_filename' - skipping taxon.\n";
     next;
 }

 my $clusters_lineage_filename = "classification/string_neighborhood_clusters/$taxon.al.simpChild5";
 unless (-e $clusters_lineage_filename) {
     print STDERR "   file not found: '$clusters_lineage_filename' - skipping taxon.\n";
     next;
 }

 print STDERR "now reading agotool file '$terms_filename' ...";
 open (FH, $terms_filename) or die "cannot read file '$terms_filename'!\n";
 while (<FH>) {
     chomp; next if /\A\#/;
     my ($term, $category_id, $description, $nr_of_proteins, $shorthands_concatenated) = split /\t/;
     my @shorthands = split /\s/, $shorthands_concatenated;
     next unless $nr_of_proteins > 1;
     $terms{$term} = 1;
     unless (exists $shorthand_of_term{$term}) {
         $shorthand_of_term{$term} = $term_shorthand;
         $term_of_shorthand{$term_shorthand} = $term;
         $description_of_term{$term} = $description;
         $term_shorthand += 1;
     }
     foreach my $shorthand (@shorthands) {
         $proteins_per_species_per_term{$term}{$taxon}{$shorthand} = 1;
     }
     print FH_OUT_MEMBERS "$shorthand_of_term{$term}\t$category_id\t$nr_of_proteins\t";
     print FH_OUT_MEMBERS join "\t", @shorthands;
     print FH_OUT_MEMBERS "\n";
     print FH_OUT_DESCRIPTIONS "$shorthand_of_term{$term}\t$term\t$description\n";
 }
 print STDERR "done.\n";

 print STDERR "now reading string cluster file '$clusters_filename' ...";
 open (FH, $clusters_filename) or die "cannot read file '$clusters_filename'!\n";
 while (<FH>) {
     chomp; next if /\A\#/;
     my ($term_raw, $category_id, $description, $nr_of_proteins, @shorthands) = split /\t/;
     next unless $nr_of_proteins > 1;
     next unless $nr_of_proteins <= $max_size_of_neighborhood_cluster;
     my $term = $taxon . ":" . $term_raw;    ## Annika clusters re-use IDs across organisms, but annotations do not match !
     $terms{$term} = 1;
     unless (exists $shorthand_of_term{$term}) {
         $shorthand_of_term{$term} = $term_shorthand;
         $term_of_shorthand{$term_shorthand} = $term;
         $description_of_term{$term} = $description;
         $term_shorthand += 1;
     }
     foreach my $shorthand (@shorthands) {
         $proteins_per_species_per_term{$term}{$taxon}{$shorthand} = 1;
     }
     print FH_OUT_MEMBERS "$shorthand_of_term{$term}\t$category_id\t$nr_of_proteins\t";
     print FH_OUT_MEMBERS join "\t", @shorthands;
     print FH_OUT_MEMBERS "\n";
     print FH_OUT_DESCRIPTIONS "$shorthand_of_term{$term}\t$term\t$description\n";
 }
 print STDERR "done.\n";

 print STDERR "now reading lineage filename '$terms_lineage_filename' ...";
 open (FH, $terms_lineage_filename) or die "cannot read file '$terms_lineage_filename'!\n";
 while (<FH>) {
     chomp; next if /\A\#/;
     my ($term, @children) = split /\t/;
     next unless exists $shorthand_of_term{$term};
     my $nr_of_children = scalar @children;
     next unless $nr_of_children > 0;
     my @children_shorthands = ();
     foreach my $child (@children) {
         next unless exists $shorthand_of_term{$child};
         push @children_shorthands, $shorthand_of_term{$child};
     }
     $nr_of_children = scalar @children_shorthands;
     next unless $nr_of_children > 0;
     print FH_OUT_CHILDREN "$shorthand_of_term{$term}\t$nr_of_children\t";
     print FH_OUT_CHILDREN join "\t", @children_shorthands;
     print FH_OUT_CHILDREN "\n";
 }
 print STDERR "done.\n";

 print STDERR "now reading lineage filename '$clusters_lineage_filename' ...";
 open (FH, $clusters_lineage_filename) or die "cannot read file '$clusters_lineage_filename'!\n";
 while (<FH>) {
     chomp; next if /\A\#/;
     my ($term_raw, @children) = split /\t/;
     my $term = $taxon . ":" . $term_raw;    ## Annika clusters re-use IDs across organisms, but annotations do not match !
     next unless exists $shorthand_of_term{$term};
     my $nr_of_children = scalar @children;
     next unless $nr_of_children > 0;
     my @children_shorthands = ();
     foreach my $child_raw (@children) {
         my $child = $taxon . ":" . $child_raw;    ## Annika clusters re-use IDs across organisms, but annotations do not match !
         next unless exists $shorthand_of_term{$child};
         push @children_shorthands, $shorthand_of_term{$child};
     }
     $nr_of_children = scalar @children_shorthands;
     next unless $nr_of_children > 0;
     print FH_OUT_CHILDREN "$shorthand_of_term{$term}\t$nr_of_children\t";
     print FH_OUT_CHILDREN join "\t", @children_shorthands;
     print FH_OUT_CHILDREN "\n";
 }

 close FH_OUT_MEMBERS;
 close FH_OUT_DESCRIPTIONS;
 close FH_OUT_CHILDREN;

 print STDERR "done.\n";
}

print "CREATE TABLE classification.terms_proteins_temp (\n";
print "       term_id integer,\n";
print "       species_id integer,\n";
print "       protein_id integer\n";
print ") WITHOUT OIDS;\n";

print "CREATE TABLE classification.terms_counts_temp (\n";
print "       term_id integer,\n";
print "       species_id integer,\n";
print "       member_count integer\n";
print ") WITHOUT OIDS;\n";

print "CREATE TABLE classification.terms_temp (\n";
print "       term_id integer,\n";
print "       term_external_id_full character varying (100),\n";
print "       term_external_id_compact character varying (100),\n";
print "       description character varying\n";
print ") WITHOUT OIDS;\n";

print STDERR "COPY classification.terms_proteins_temp FROM stdin;\n";
print "COPY classification.terms_proteins_temp FROM stdin;\n";
foreach my $term (sort { $shorthand_of_term{$a} <=> $shorthand_of_term{$b} } keys %proteins_per_species_per_term) {
 my $term_shorthand = $shorthand_of_term{$term};
 foreach my $species (keys %{$proteins_per_species_per_term{$term}}) {
     my $nr_of_proteins = scalar keys %{$proteins_per_species_per_term{$term}{$species}};
     foreach my $protein (keys %{$proteins_per_species_per_term{$term}{$species}}) {
         print "$term_shorthand\t" .
             "$species\t" .
             "$protein\n";
     }
 }
}
print "\\.\n";

print STDERR "COPY classification.terms_counts_temp FROM stdin;\n";
print "COPY classification.terms_counts_temp FROM stdin;\n";
foreach my $term (sort { $shorthand_of_term{$a} <=> $shorthand_of_term{$b} } keys %terms) {
 my $term_shorthand = $shorthand_of_term{$term};
 foreach my $taxon (sort {$a <=> $b} keys %{$proteins_per_species_per_term{$term}}) {
     my $nr_of_proteins = scalar keys %{$proteins_per_species_per_term{$term}{$taxon}};
     print "$term_shorthand\t" .
         "$taxon\t" .
         "$nr_of_proteins\n";
 }
}
print "\\.\n";

print STDERR "COPY classification.terms_temp FROM stdin;\n";
print "COPY classification.terms_temp FROM stdin;\n";
foreach my $term (sort { $shorthand_of_term{$a} <=> $shorthand_of_term{$b} } keys %terms) {
 my $term_shorthand = $shorthand_of_term{$term};
 my $description = $description_of_term{$term};
 my $compact_term = $term;
 if ($term =~ /\A(\d+)\:(C.+)\z/) {        ## Annika clusters re-use IDs across organisms, but annotations do not match !
     $compact_term = $2;
 }
 print "$term_shorthand\t" .
     "$term\t" .
     "$compact_term\t" .
     "$description\n";
}
print "\\.\n";

print "CREATE INDEX pi_terms_term_id_temp ON classification.terms_temp (term_id);\n";
print "CREATE INDEX si_terms_term_external_id_temp ON classification.terms_temp (term_external_id_full);\n";
print "CLUSTER pi_terms_term_id_temp ON classification.terms_temp;\n";
print "VACUUM ANALYZE classification.terms_temp;\n";

print "CREATE INDEX pi_terms_proteins_term_id_species_id_temp ON classification.terms_proteins_temp (term_id, species_id);\n";
print "CLUSTER pi_terms_proteins_term_id_species_id_temp ON classification.terms_proteins_temp;\n";
print "VACUUM ANALYZE classification.terms_proteins_temp;\n";

print "CREATE INDEX pi_terms_counts_term_id_species_id_temp ON classification.terms_counts_temp (term_id, species_id);\n";
print "CLUSTER pi_terms_counts_term_id_species_id_temp ON classification.terms_counts_temp;\n";
print "VACUUM ANALYZE classification.terms_counts_temp;\n";

print STDERR "\nall done.\n";

## that's it.

close STDERR;
close STDOUT;

POSIX::_exit(0);    ## this line: to prevent Perl from going through all its clean-up code.
                 ##            [this exits the script the hard way. Destructors etc. will not be called,
                 ##             file handles may not be closed, memory not garbage-collected, buffers not flushed. Beware ...]
                 ##
                 ## But: cleaning up does not help anyone, and is darn slow when you have large data structures, so ...