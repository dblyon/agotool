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
r"ftp://ftp.expasy.org/databases/uniprot/current_release/knowledgebase/complete/docs/sec_ac.txt"
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

### secondary_2_primary_id [Secondary_2_Primary_ID_UPS_FIN.txt]
| taxid | type | sec | uniprotid |
|:---:|:---:|:---:|:---:|
| 1028729 | ENSP_2_ID | 101028.EKJ70075 | K3VY58_FUSPC |
| 2026739 | AC_2_ID | A0A2E5VZF0 | A0A2E5VZF0_9EURY |


### taxid_uniprot_ac_2_id [Taxid_UniProt_AC_2_ID.txt]
| taxid | uniprotan | uniprotid |
|:---:|:---:|:---:|
| 654924 | Q6GZX4 | 001R_FRG3G |
| 654924 | Q6GZX3 | 002L_FRG3G |
| 345201 | Q197F8 | 002R_IIV3 |


### taxid_uniprotid_2_ensps_2_keggs [Taxid_UniProtID_2_ENSPs_2_KEGGs.txt]
| taxid | uniprotid | ensps | keggs |  
|:---:|:---:|:---:|:---:|
| 176652 | 127L_IIV6 |  | vg:1733363 |
| 272626 | 12OLP_LISIN | 272626.lin1839 | lin:lin1839 |
| 83332 | 35KD_MYCTU | 83332.Rv2744c;83332.ABC123   mtu:Rv2744c;mtv:RVBD_2744c |


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
| RCTM | -57 | Reactome |
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


### functions [Functions_table_UPS_FIN.txt] # ToDo check RCTM terms
| enum | etype | an | description | year | level |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | -21 | GO:0000001 | mitochondrion inheritance | -1 | 5 |
| 1 | -21 | GO:0000002 | mitochondrial genome maintenance | -1 | 5 |
| 2 | -21 | GO:0000003 | reproduction | -1 | 1 |
| 47234 | -51 | KW-0001 | 2Fe-2S | -1 | 2 |
| 47235 | -51 | KW-0002 | 3D-structure | -1 | 1 |
| 48432 | -52 | map00010 | Glycolysis Gluconeogenesis | -1 | -1 |
| 48433 | -52 | map00020 | Citrate cycle (TCA cycle) | -1 | -1 |
| 48961 | -53 | SM00006 | amyloid A4 | -1 | -1 |
| 791705 | -56 | PMID:12926249 | (2003) QMMM calculations of kinetic isotope effects in the chorismate mutase active site. | 2003 | -1 |


### function_2_Protein [Function_2_Protein_table_UPS.txt]
| taxid | etype | association | background_count | background_n | uniprotid_array |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 654924 | -51 | KW-9990 | 2 | -1 | 001R_FRG3G;002L_FRG3G |
| 654924 | -51 | KW-1185 | 2 | -1 | 001R_FRG3G;002L_FRG3G |
| 1228191 | -21 | GO:0051806 | 1 | -1 | J7MAC7_9INFA |
| 1797973 | -21 | GO:0072521 | 43 | -1 | A0A1F9YTV2_9BACT;A0A1F9YUJ4_9BACT;A0A1F9YUQ8_9BACT;... |
| 2320103 | -21 | GO:2001295 | 3 | 3860 | A0A3A8U194_9BACT;A0A3A8UNX3_9BACT;A0A3A8UWE3_9BACT |


### lineage [Lineage_table_UPS_FIN.txt]
| func_enum | func_enum_array |
|:---:|:---:|
| 0 | {2803, 2809, 3348, 4057, 5420, 14355, 14358, 15352, 15697, 15698, 15703, 19423} |
| 1 | {2803, 2809, 3348, 4057, 5420, 9249, 19423} |
| 2 | {255, 402, 2890, 2895, 2896, 3348, 6754, 6755, 7520, ... } |


### lineage_hr [Lineage_table_UPS_hr.txt]
| func | func_array |
|:---:|:---:|
| GO:0000001 | {"GO:0006996", "GO:0007005", "GO:0008150", "GO:0009987", "GO:0016043", "GO:0048308", "GO:0048311", "GO:0051179", "GO:0051640", "GO:0051641", "GO:0051646", "GO:0071840"} |
| GO:0000002 | {"GO:0006996", "GO:0007005", "GO:0008150", "GO:0009987", "GO:0016043", "GO:0071840"} |
| GO:0000003 | {"GO:0008150"} |
| GO:0000005 | {} |


### protein_2_function [Protein_2_Function_table_UPS.txt]
| taxid | uniprotid | func_array | etype | 
|:---:|:---:|:---:|:---:|
| 1160091 | A0A1Y2T2E3_9BIFI | {"IPR000362","IPR008948","IPR013539","IPR020557","IPR022761","IPR024083"} | -54 |
| 1813946 | A0A165J5C1_9BURK | {"KW-0181","KW-9990"} | -51 |
| 2039283 | A0A397FNG6_9MOLU | {"GO:0005575","GO:0005622","GO:0005623","GO:0005737","GO:0044424","GO:0044464"} | -22 |


### Protein_2_Function_withoutScore_DOID_BTO_GOCC_UPS [Protein_2_Function_withoutScore_DOID_BTO_GOCC_UPS.txt]
| taxid | uniprotid | func_array | etype | 
|:---:|:---:|:---:|:---:|
| 10090 | G3XA30_MOUSE | {"GO:0005622","GO:0005886","GO:0016020","GO:0044424","GO:0044464","GO:0043231","GO:0005856","GO:0044444","GO:0043228","GO:0043226","GO:0005737","GO:0043227","GO:0043232","GO:0005634","GO:0005576","GO:0005829","GO:0071944","GO:0005575","GO:0005623","GO:0043229"} | -22 |
| 10116 | PCOC1_RAT | {"GO:0005886","GO:0043227","GO:0044464","GO:0043229","GO:0044424","GO:0016020","GO:0016942","GO:0005576","GO:0005622","GO:0043226","GO:0005615","GO:0043231","GO:0044421","GO:0036454","GO:0071944","GO:0005575","GO:0005634","GO:0005623"} | -22 |


### protein_2_functionenum [Protein_2_FunctionEnum_table_UPS_FIN.txt]
| taxid | uniprotid | func_enum_array |
|:---:|:---:|:---:|
| 157072 | A0A024TED2_9STRA | {44491,45368,45450} |
| 1945579 | A0A328S5B5_9EURY | {44491,45368,45450} |
| 1978231 | A0A2V2RNV7_9BACT | {55397,57018,58330,89447} |


### protein_2_functionenum_and_score [Protein_2_FunctionEnum_and_Score_table_UPS_FIN.txt] ? reduce to primary UniProtIDs ?
| taxid | uniprotid | funcenum_score_arr |
|:---:|:---:|:---:|
| 3702 | NAC1_ARATH | {{211,4.2},{252,4.166357},{253,4.195121},{259,3.257143},{323,1.234689}, ...} |
| 3702 | NGA3_ARATH | {{211,4.2},{212,0.214286},{252,4.2},{253,4.2}, ...} |


### taxid_2_proteins [Taxid_2_Proteins_table_UPS_FIN.txt]
| taxid | count | an_array | 
|:---:|:---:|:---:|
| 9606 | 20874 | {"1433B_HUMAN","1433E_HUMAN","1433F_HUMAN","1433G_HUMAN", ...} |
| 10090 | 22287 | {"1433B_MOUSE","1433E_MOUSE","1433F_MOUSE", ...} |


### taxid_2_functioncountarray [Taxid_2_FunctionCountArray_table_UPS_FIN.txt]
| taxid | background_n | background_count_array |
|:---:|:---:|:---:|
| 9606 | 19566 | {{1,22},{100,10},{1000001,2},{1000002,4},{100001,8},{1000011,2}, ... |
| 100901 | 647 | {{3328085,2},{3635192,6},{4454829,2},{47234,4}, ... |
| 7230 | 14594 | {{100001,2},{1000164,6},{100046,2},{100058,9}, ... |


### taxid_2_functionenum_2_scores [Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN.txt]
| taxid | func_enum | score_array |
|:---:|:---:|:---:|
| 9606 | 0 | {0.611452,1.67871,1.21, ...} |
| 9606 | 1 | {5.0,0.69, ...} |
| 10090 | 0 | {1.45,0.5744,...} |
| 10090 | 1 | {0.5,0.7477,...} |