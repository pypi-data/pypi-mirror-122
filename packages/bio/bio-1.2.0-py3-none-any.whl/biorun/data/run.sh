# No difference between outputs.
diff all_1.fa all_2.fa > nodiff.txt
bio align GATTACA GATCA --diff  > gattaca.diff
# Format to diff
bio format mafft.fa --diff > mafft.diff
