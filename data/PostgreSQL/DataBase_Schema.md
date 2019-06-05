## go_2_slim [GO_2_Slim_table.txt]
##### an(Text); slim(Boolean)
| an | slim |
|:---:|:---:|
| GO:0000003 | 1 |


## protein_secondary_2_primary_an [Protein_Secondary_2_Primary_AN_table.txt] merge with ### uniprot_ac_2_id [UniProt_AC_2_ID.txt] # accession to entry name
##### Secondary (Text); Prim(Text) ("Primary" is a reserved PostgreSQL word)
| sec | pri |
|:---:|:---:|
| A0A021WW06 | P40417 | --> replace with translation of AC_old to UniProtID
| ENSPsomethingsomething | UniProtID |
| Q6GZX4 | 001R_FRG3G |
| Q6GZX3 | 002L_FRG3G |
| Q197F8 | 002R_IIV3 |

to map Jensenlab Score data to UniProt
 ENSP 2 UniProtID mapping needed

given:
- secondary 2 primary UniProt AC (URL_UNIPROT_SECONDARY_2_PRIMARY_AN = r"ftp://ftp.uniprot.org/pub/databases/uniprot/knowledgebase/docs/sec_ac.txt")
- UniProt AC 2 ID (from UniProt dump or URL_UniProt_ID_mapping = r"ftp://ftp.expasy.org/databases/uniprot/current_release/knowledgebase/idmapping/idmapping_selected.tab.gz")
 ftp://ftp.expasy.org/databases/uniprot/current_release/knowledgebase/idmapping/idmapping.dat.gz
- UniProtAC/ID 2 ENSP (UniProt_2_STRING_2_KEGG.txt from UniProt dump)
- UniProtAC 2 ENSP (uniprot_2_string_v11 "full_uniprot_2_string.jan_2018.clean.tsv") # ENSP 2 UniProtID is a one 2 one mapping :)

wanted:
- ENSP 2 UniProtID
- UniProtAC 2 UniProtID
- secondary AC 2 UniProtID
? - synonym ID 2 UniProtID ? --> not needed for now (would have to parse "ID   ADAM9_HUMAN             Reviewed;         819 AA." and 
"GN   Name=ADAM9; Synonyms=KIAA0021, MCMP, MDC9, MLTNG;" from UniProt dump)


query using:
- UniProt AC
- UniProt ID
- ENSP
--> maps to UniProt ID


URL_UniProt_ID_mapping = r"ftp://ftp.expasy.org/databases/uniprot/current_release/knowledgebase/idmapping/idmapping_selected.tab.gz"


### entity_types [Entity_types_table_FIN.txt]
| an | etype | name |
|:---:|:---:|:---:|
| GO:0008150 | -21 | GO biological process |
| GO:0005575 | -22 | GO cellular component |
| GO:0005575 | -20 | GO cellular component Textmining |
| GO:0003674 | -23 | GO molecular function |
| GO:OBSOLETE | -24 | GO obsolete |
| KW-9990 | -51 | UniProt keyword Technical term |
| KW-9991 | -51 | UniProt keyword PTM |
| KW-9992 | -51 | UniProt keyword Molecular function |
| KW-9993 | -51 | UniProt keyword Ligand |
| KW-9994 | -51 | UniProt keyword Domain |
| KW-9995 | -51 | UniProt keyword Disease |
| KW-9996 | -51 | UniProt keyword Developmental stage |
| KW-9997 | -51 | UniProt keyword Coding sequence diversity |
| KW-9998 | -51 | UniProt keyword Cellular component |
| KW-9999 | -51 | UniProt keyword Biological process |
| KEGG | -52 | KEGG |
| SMART | -53 | SMART |
| INTERPRO | -54 | Interpro |
| PFAM | -55 | Pfam |
| PMID | -56 | PMID |
| RCTM | -57 | REACTOME |
| chemicals | -1 | chemicals |
| NCBI species taxonomy id (tagging species) | -2 | NCBI species taxonomy id (tagging species) |
| NCBI species taxonomy id (tagging proteins) | -3 | NCBI species taxonomy id (tagging proteins) |
| Wikipedia | -11 | Wikipedia |
| BTO tissues | -25 | BTO tissues|
| DOID diseases | -26 | DOID diseases |
| ENVO environments | -27 | ENVO environments |
| APO phenotypes | -28 | APO phenotypes |
| FYPO phenotypes | -29 | FYPO phenotypes |
| MPheno phenotypes| -30 | MPheno phenotypes |
| NBO behaviors | -31 | NBO behaviors |
| mammalian phenotypes | -36 | mammalian phenotypes |
| DSD clusters | -77 | DSD based STRING clusters |
| clusters | -78 | STRING clusters |


### functions [Functions_table_UPS_FIN.txt]
| enum | etype | an | description | year | level |
|:---:|:---:|:---:|:---:|:---:|:--:|
| 0 | -21 | GO:0000001 | mitochondrion inheritance | -1 | 5 |
| 1 | -21 | GO:0000002 | mitochondrial genome maintenance | -1 | 5 |
| 2 | -21 | GO:0000003 | reproduction | -1 | 1 |
| 47234 | -51 | KW-0001 | 2Fe-2S | -1 | 2 |``
| 47235 | -51 | KW-0002 | 3D-structure | -1 | 1 |
| 48432 | -52 | map00010 | Glycolysis Gluconeogenesis | -1 | -1 |
| 48433 | -52 | map00020 | Citrate cycle (TCA cycle) | -1 | -1 |
| 48961 | -53 | SM00006 | amyloid A4 | -1 | -1 |
| 791705 | -56 | PMID:12926249 | (2003) QMMM calculations of kinetic isotope effects in the chorismate mutase active site. | 2003 | -1 |


### function_2_Protein [Function_2_Protein_table_UPS.txt]  
| taxid | etype | association | background_count | background_n | uniprotid_array |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 9606 | -21 | 'GO:0006810' | 3 | 3919 | {'9606.ENSP00000000233', '9606.ENSP00000000412', ... } |
| 9606 | -21 | 'GO:0006897' | 2 | 3919 | {'9606.ENSP00000000412', ...} |
| 9606 | -21 | 'GO:0006898' | 1 | 3919 | {'9606.ENSP00000000412'} |
| 9606 | -21 | 'GO:0006810' | 3 | 3919 | {'UniProtID1', 'UniProtID2', ... } |
| 9606 | -21 | 'GO:0006897' | 2 | 3919 | {'UniProtID3', ...} |
| 9606 | -21 | 'GO:0006898' | 1 | 3919 | {'UniProtID3'} |
| 654924 | -51 | KW-0181 | 2 | -1 | {"001R_FRG3G","002L_FRG3G"} |
| 9606 | -22 | GO:0044444 | 2 | 20874 | {"1433B_HUMAN","1433B_HUMAN"} |
| 9606 | -22 | GO:0005774 | 2 | 20874 | {"1433B_HUMAN","1433B_HUMAN"} |


### lineage [Lineage_table_FIN.txt]
| func_enum | func_enum_array |
|:---:|:---:|
| 0 | {2803, 2809, 3348, 4057, 5420, 14355, 14358, 15352, 15697, 15698, 15703, 19423} |
| 1 | {2803, 2809, 3348, 4057, 5420, 9249, 19423} |
| 2 | {255, 402, 2890, 2895, 2896, 3348, 6754, 6755, 7520, ... } |


### protein_2_function [Protein_2_Function_table_UPS.txt]
| uniprotid | func_array | etype | taxid | 
|:---:|:---:|:---:|:---:|
| 001R_FRG3G | {"KW-0010","KW-0181","KW-0804","KW-0805","KW-1185","KW-9990","KW-9992","KW-9999"} | -51 | 654924 | 
| 001R_FRG3G | {"GO:0008150","GO:0043900","GO:0043903","GO:0046782","GO:0050789","GO:0050792","GO:0065007"} | -21 | 654924 |
| 001R_FRG3G | {"IPR007031"} |-54 | 654924 |
| 001R_FRG3G | {"PF04947"} | -55 | 654924 |
| 002L_FRG3G | {"KW-0181","KW-0472","KW-0812","KW-1043","KW-1133","KW-1185","KW-9990","KW-9994","KW-9998"} | -51 | 654924 |


### Protein_2_Function_withoutScore_DOID_BTO_GOCC_UPS [Protein_2_Function_withoutScore_DOID_BTO_GOCC_UPS.txt]
| uniprotid | func_array | etype | taxid | 
|:---:|:---:|:---:|:---:|
| G3XA30_MOUSE | {"GO:0005622","GO:0005886","GO:0016020","GO:0044424","GO:0044464","GO:0043231","GO:0005856","GO:0044444","GO:0043228","GO:0043226","GO:0005737","GO:0043227","GO:0043232","GO:0005634","GO:0005576","GO:0005829","GO:0071944","GO:0005575","GO:0005623","GO:0043229"} | -22 | 10090 |
| PCOC1_RAT | {"GO:0005886","GO:0043227","GO:0044464","GO:0043229","GO:0044424","GO:0016020","GO:0016942","GO:0005576","GO:0005622","GO:0043226","GO:0005615","GO:0043231","GO:0044421","GO:0036454","GO:0071944","GO:0005575","GO:0005634","GO:0005623"} | -22 | 10116 |


### protein_2_functionenum [Protein_2_FunctionEnum_table_UPS_FIN.txt]
| uniprotid | func_enum_array | taxid |
|:---:|:---:|:---:|
| 1000565.METUNv1_00006 | {47403, 48329, 48422, 52375, 86134, 97354, 97505} | 1000565 | 
| 1193181.BN10_100007 | {47403, 47665, 47963, 48277, 48329, 48422, 48426, 48430, 52979, 61216, 86802} | 1193181 |
| 1230343.CANP01000023_gene1527 | {47403, 47665, 47963, 48277, 48422, 48426, 48430} | 1230343 |


### protein_2_functionenum_and_score [Protein_2_FunctionEnum_and_Score_table_UPS_FIN.txt] ? reduce to primary UniProtIDs ?
| uniprotid | funcenum_score_arr | taxid |
|:---:|:---:|
| 9606.ENSP00000000233 | {{33885,1.00616},{34752,0.709055},{35541,1.297117},{35543,1.296111},{35907,0.600582},{36031,0.670014},{36271,0.527888},{36276,0.552587}, ... } | 9606 |


### taxid_2_proteins [Taxid_2_Proteins_table_UPS_FIN.txt]
| taxid | an_array | count |
|:---:|:---:|:---:|
| 9606 | {"1433B_HUMAN","1433E_HUMAN","1433F_HUMAN","1433G_HUMAN", ...} | 20874 |
| 10090 | {"1433B_MOUSE","1433E_MOUSE","1433F_MOUSE", ...} | 22287 |


### taxid_2_functioncountarray [Taxid_2_FunctionCountArray_table_FIN.txt]
| taxid | background_n | background_count_array | dbtype |
|:---:|:---:|:---:|:---:|
| 9606 | 19566 | {{1,22},{100,10},{1000001,2},{1000002,4},{100001,8},{1000011,2}, ... | 1 |
| 100901 | 647 | {{3328085,2},{3635192,6},{4454829,2},{47234,4}, ... | 1 |
| 7230 | 14594 | {{100001,2},{1000164,6},{100046,2},{100058,9}, ... | 1 |
| 9606 | 19566 | {{1,22},{100,10},{1000001,2},{1000002,4},{100001,8},{1000011,2}, ... | 2 |
| 100901 | 647 | {{3328085,2},{3635192,6},{4454829,2},{47234,4}, ... | 2 |
| 7230 | 14594 | {{100001,2},{1000164,6},{100046,2},{100058,9}, ... | 2 |


### taxid_2_funcenum_2_scores [Taxid_2_funcEnum_2_scores_table_FIN.txt]
| taxid | func_enum | score_array |
|:---:|:---:|:---:|
| 9606 | 0 | {0.611452,1.67871,1.21, ...} |
| 9606 | 1 | {5.0,0.69, ...} |
| 10090 | 0 | {1.45,0.5744,...} |
| 10090 | 1 | {0.5,0.7477,...} |
