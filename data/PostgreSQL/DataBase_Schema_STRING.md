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


### functions [Functions_table_FIN.txt]
| enum | etype | an | description | year | level |
|:---:|:---:|:---:|:---:|:---:|:--:|
| 0 | -21 | GO:0000001 | mitochondrion inheritance | -1 | 5 |
| 1 | -21 | GO:0000002 | mitochondrial genome maintenance | -1 | 5 |
| 2 | -21 | GO:0000003 | reproduction | -1 | 1 |
| 47234 | -51 | KW-0001 | 2Fe-2S | -1 | 2 |
| 47235 | -51 | KW-0002 | 3D-structure | -1 | 1 |
| 48432 | -52 | map00010 | Glycolysis Gluconeogenesis | -1 | -1 |
| 48433 | -52 | map00020 | Citrate cycle (TCA cycle) | -1 | -1 |
| 48961 | -53 | SM00006 | amyloid A4 | -1 | -1 |
| 791705 | -56 | PMID:12926249 | (2003) QMMM calculations of kinetic isotope effects in the chorismate mutase active site. | 2003 | -1 |


### function_2_ENSP [Function_2_ENSP_table_FIN.txt]
| taxid | etype | association | background_count | background_n | an_array |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 9606 | -21 | 'GO:0006810' | 3 | 3919 | {'9606.ENSP00000000233', '9606.ENSP00000000412', ... } |
| 9606 | -21 | 'GO:0006897' | 2 | 3919 | {'9606.ENSP00000000412', ...} |
| 9606 | -21 | 'GO:0006898' | 1 | 3919 | {'9606.ENSP00000000412'} |


### protein_2_function [Protein_2_Function_table_FIN.txt]
| an | func_array | etype |
|:---:|:---:|:---:|
| 9606.ENSP00000000233 | {"GO:0006810","GO:0007154","GO:0007165","GO:0007264","GO:0008104","GO:0008150","GO:0008150","GO:0008152","GO:0009987","GO:0015031","GO:0015833","GO:0016192","GO:0023052","GO:0033036","GO:0035556","GO:0042886","GO:0044700","GO:0044763","GO:0045184","GO:0050789","GO:0050794","GO:0050896","GO:0051179","GO:0051234","GO:0051716","GO:0065007","GO:0071702","GO:0071705"} | -21 |
| 9606.ENSP00000000233 | {"GO:0005575","GO:0005576","GO:0005622","GO:0005623","GO:0005737","GO:0005794","GO:0005886","GO:0012505","GO:0016020","GO:0031982","GO:0031988","GO:0043226","GO:0043227","GO:0043229","GO:0043230","GO:0043231","GO:0044421","GO:0044424","GO:0044444","GO:0044464","GO:0048471","GO:0065010","GO:0070062","GO:0071944","GO:1903561"} | -22 |
| 9606.ENSP00000000233 | {"GO:0000166","GO:0001882","GO:0001883","GO:0003674","GO:0003824","GO:0003924","GO:0005488","GO:0005525","GO:0016462","GO:0016787","GO:0016817","GO:0016818","GO:0017076","GO:0017111","GO:0019001","GO:0032549","GO:0032550","GO:0032553","GO:0032555","GO:0032561","GO:0035639","GO:0036094","GO:0043167","GO:0043168","GO:0097159","GO:0097367","GO:1901265","GO:1901363"} | -23 |
| 9606.ENSP00000000233 | {"KW-0002","KW-0181","KW-0333","KW-0342","KW-0449","KW-0472","KW-0519","KW-0547","KW-0653","KW-0813","KW-0931","KW-0963","KW-1185","KW-9990","KW-9991","KW-9993","KW-9998","KW-9999"} | -51 |
| 9606.ENSP00000000233 | {"map04144"} | -52 |
| 9606.ENSP00000000233 | {"Arf","Gtr1_RagA","MMR_HSR1","Ras","Roc","SRPRB"}" | -53 |
| 9606.ENSP00000005587 | {"SM00233","SM00326"} | -53 |
| 9606.ENSP00000000233 | {"IPR005225","IPR006689","IPR024156","IPR027417"} | -54 |
| 9606.ENSP00000000412 | {"PF09451","PF02157"} | -55 |


### protein_2_functionEnum [Protein_2_FunctionEnum_table_FIN.txt]
| an | func_enum_array |
|:---:|:---:|
| 1000565.METUNv1_00006 | {47403, 48329, 48422, 52375, 86134, 97354, 97505} |
| 1193181.BN10_100007 | {47403, 47665, 47963, 48277, 48329, 48422, 48426, 48430, 52979, 61216, 86802} |
| 1230343.CANP01000023_gene1527 | {47403, 47665, 47963, 48277, 48422, 48426, 48430} |
| 1286170.RORB6_22675 | {47403, 47440, 47743, 48422, 48424, 53868, 75137, 82814, 85480} |
| 1537715.JQFJ01000002_gene718 | {49160} |
| 211165.AJLN01000153_gene695 | {100879} |
| 246196.MSMEI_2975 | {47397, 47403, 48329, 48422, 48426, 51824, 59740, 1812416, 1914629, 2064397, 2516845, 2542738, 2579066, 2787936, 3317676, 3378861, 3552644, 4064473, 4205464, 4398263, 5424544, 5522838} |
| 38833.XP_003059384.1 | {47403, 48329, 48422, 49005, 51951, 60573, 96979, 97269, 97582} |
| 794846.AJQU01000003_gene1109 | {47403, 48422, 53420, 69968, 87113} |
| 9606.ENSP00000298492 | {78, 93, 95, 1557, 2377, 2408, 2670, 2771, 2803, 2814, 2818, 2843, 2845, 2846, 2853, 3348, 3349, 3432, 4057, 5420, 5615, 6509, 7297, 7319, 10550, 11801, 11918, 12247, 12316, 12317, 12329, 12333, 14335, 15112, 15390, 15448, 18561, 18628, 18629, 18794, 19344, ... |
| 9986.ENSOCUP00000018664 | {47403, 48329, 48422} |


### lineage [Lineage_table_FIN.txt]
| func_enum | func_enum_array |
| 0 | {2803, 2809, 3348, 4057, 5420, 14355, 14358, 15352, 15697, 15698, 15703, 19423} |
| 1 | {2803, 2809, 3348, 4057, 5420, 9249, 19423} |
| 2 | {255, 402, 2890, 2895, 2896, 3348, 6754, 6755, 7520, ... } |


### taxid_2_proteins [TaxID_2_Proteins_table_FIN.txt]
| taxid | an_array | count |
|:---:|:---:|:---:|
| 9606 | {"9606.ENSP00000000233","9606.ENSP00000000412","9606.ENSP00000001008","9606.ENSP00000001146", ...} | 19566 |
| 1000565 | {"1000565.METUNv1_00006","1000565.METUNv1_00011","1000565.METUNv1_00018","1000565.METUNv1_00019", ...} | 12345 |


### Taxid_2_FunctionCountArray [Taxid_2_FunctionCountArray_table_FIN.txt]
| taxid | background_n | background_count_array |
|:---:|:---:|:---:|
| 9606 | 19566 | {{1,22},{100,10},{1000001,2},{1000002,4},{100001,8},{1000011,2}, ... |
| 100901 | 647 | {{3328085,2},{3635192,6},{4454829,2},{47234,4}, ... |
| 7230 | 14594 | {{100001,2},{1000164,6},{100046,2},{100058,9}, ... |

### Protein_2_FunctionEnum_and_Score_table_FIN.txt
|:---:|:---:|
| 9606.ENSP00000000233 | {{33885,1.00616},{34752,0.709055},{35541,1.297117},{35543,1.296111},{35907,0.600582},{36031,0.670014},{36271,0.527888},{36276,0.552587}, ... } |
