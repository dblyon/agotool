# Data Base Schema
## peptidehash_2_proteinsetenum (PeptideHash_2_ProteinSetEnum_table.txt)
###### peptide_hash (64bit, 'I' converted to 'L', index-column, redundant); protein_set_enumeration (32bit, redundant, positive numbers for target and negative for decoys)
| peptidehash | proteinsetenum |
|:---:|:---:|
| -9223361607465212318 | 1 | # 2 peptides map to the same protein group
| -8246361607465216987 | 1 | # 2 peptides map to the same protein group
| -9223355673387539936 | 2 | # anagram sequence target
| -9223355673387539936 | -1 | # anagram sequence decoy
| -1234567891234567891 | 3 |
| -4566892233337892555 | 4 |

## proteinsetenum_2_taxidlca_2_proteinenumarray (ProteinSetEnum_2_TaxIDLCA_2_ProteinEnumArray_table.txt)
###### ProteinSetEnumeration (32bit, index-column, unique, sort before import); TaxID_LCA (32bit, redundant); ProteinEnumerationArray (IntegerArray, redundant);
| proteinsetenum | taxid_lca | proteinenum_arr |
|:---:|:---:|:---:|
| 1 | 314146 | {1, 2} | # Euarchontoglires (Mouse and Human --> Placentales LCA)
| 2 | 837 | {3} | # Porphyromonas gingivalis anagram sequence
| -1 | 837 | {3} | # Porphyromonas gingivalis anagram sequence
| 3 | -2 | {837, -12345, 0, 4, 5} | # -2 is the placeholder symbolizing that Integers before are LCAs TaxIDs, and after are ProteinEnums 
| 3 | 1 | {4, 5} | # how is this different from row above
| 4 | -2 | {837, -6789, -5938, 0, 6, 7, 8} | # old
| 4 | 1 | {6, 7, 8} | # new
| 5 | -2 | {1437010, -55, -66, 0, 9, 10, 11, 12, 13} | # old 
| 5 | 1 | {9, 10, 11, 12, 13} | # new
###### TaxIDs of Proteins 4 and 5: 837 and -12345 --> -2; Porphyromonas 
###### gingivalis AND made up species -12345 
###### 837, -6789, and -5938 --> -2; Porphyromonas gingivalis AND
###### made up species -6789 AND made up species -5938 

## proteinenum_2_an_2_taxid (ProteinEnum_2_AN_2_TaxID_table.txt)
###### ProteinEnumeration (32bit Integer, unique, ?index-column?); AccessionNumber (String, unique, index-column); NCBI_TaxID (32bit Integer, unique)
| protenum | an | taxid |
|:---:|:---:|:---:|
| 1 | P84243 | 9606 |
| 2 | P84228 | 10090 |
| 3 | B2RID1 | 837 |
| 4 | B2RID1-98 | 837 |
| 5 | A1 | -12345 |
| 6 | B2RID1-99 | 837 |
| 7 | B1 | -6789 |
| 8 | C1 | -5938 |
| 9 | D | 9606 |
| 10 | E | 9913 |
| 11 | F | 10090 |
| 12 | G | -55 |
| 13 | H | -66 |

## child_2_parent (Child_2_Parent_table.txt)
###### Child (32bit Integer, redundant, index-column, sort before import); Parent (32bit Integer, redundant); Direct (Bool)
| child | parent | direct |
|:---:|:---:|:---:|
| 9606 | 9605 | True |
| 9606 | 9604 | False |
| -2 | 1 | True | # always add
| -1 | 1 | True | # always add

## taxa (Taxa_table.txt)
###### TaxID (32bit Integer, redundant, made up TaxIDs should be < -2, index-column); TaxName (String); Scientific (Boolean)
| taxid | taxname | scientific |
|:---:|:---:|:---:|
| -2 | root for negative TaxIDs if missing connection to root in tree | True | 
| -1| no TaxID or TaxID_LCA could be found | True |
| 0 | doesn't exist and should not be used at all | True |
| 1 | NCBI root node | True |
| 131567 | cellular organisms | True |
| 9606 | Homo sapiens | True |
| 207598 | Homininae | True |
| 207598 | Homo/Pan/Gorilla group | False |
| 9443 | primates | False |
| 1437010| Boreoeutheria | True |
| 1437010| Boreotheria | False |
| 10380 | Herpesvirus ateles | False |
| 10380 | Ateline herpesvirus 2 | True |

## taxid_2_rank (TaxID_2_rank_table.txt)
###### TaxID (32bit Integer, unique, index-column); Rank (String)
| taxid | rank |
|:---:|:---:|
| 1 | null/None |
| 9606 | species |
| 207598 | subfamily |
| 9443 | subfamily |
| 1437010 | null/None |
| 10380 | species |

## taxid_merged (TaxID_merged_table.txt)
| old | new |
|:---:|:---:|
| 9478 | 1868482 |
| 12 | 74109 |
| 30 | 29 |
| 36 | 184914 |
