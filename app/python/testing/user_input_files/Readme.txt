# Description of example_*.txt content

## positive examples
- example_1.txt: foreground is a proper subset of the background, everything has an abundance value, one row of NaNs
- example_2.txt: same as example_1.txt with "," instead of "." as decimal delimiter
- example_3.txt: foreground is not a proper subset of the background, not everything has an abundance value
- example_4.txt: foreground and background don't intersect at all

## negative examples
- negative_1.txt: nonesense AccessionNumbers, foreground is a proper subset of the background, everything has an abundance value
- negative_2.txt: nonesense AccessionNumbers, foreground is a proper subset of the background, without intensity values
- negative_3.txt: empty file
- negative_4.txt: full of NaNs


- example_5.txt: protein-groups, foreground is a proper subset of the background, everything has an abundance value
- example_6.txt: foreground equals background, with abundance values
- example_7.txt: foreground equals background, without abundance values


## unfinished
- example_9.txt: protein-groups, --> check protein-group consensus methods #!!!

check all 4 methods for doing enrichment
- example_8.txt: redundancy of foreground proteins

################################ UniProt AN examples above
################################ ENSPs below
# Description of example_*.txt content

## positive examples
- example_1_STRING.txt: foreground is a proper subset of the background, everything has an abundance value, one row of NaNs
- example_2_STRING.txt: same as example_1_STRING.txt with "," instead of "." as decimal delimiter
- example_3_STRING.txt: foreground is not a proper subset of the background, not everything has an abundance value
- example_4_STRING.txt: foreground and background don't intersect at all
- example_6_STRING.txt: foreground equals background, with abundance values
- example_7_STRING.txt: foreground equals background, without abundance values
- example_8_STRING.txt: redundancy of foreground proteins, with abundance values
- example_10_STRING.txt: foreground 2000 proteins, background complete proteome, no abundance data
- example_11_STRING.txt: foreground is a proper subset of the background, not everything has an abundance value

## negative examples
- negative_1.txt: nonesense AccessionNumbers, foreground is a proper subset of the background, everything has an abundance value
- negative_2.txt: nonesense AccessionNumbers, foreground is a proper subset of the background, without intensity values
- negative_3.txt: empty file
- negative_4.txt: full of NaNs
- negative_5_STRING.txt: foreground AccessionNumbers from different TaxID as background, no intensity values
