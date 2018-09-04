### entity_types [Entity_types_table_STRING.txt]
| an | etype | name |
|:---:|:---:|:---:|
| GO:0008150 | -21 | GO biological process |
| GO:0005575 | -22 | GO cellular component |
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

### functions [Functions_table_STRING.txt]
| etype | name | an | definition |
|:---:|:---:|:---:|:---:|
| -21 | mitochondrion inheritance | GO:0000001 | "The distribution of mitochondria, including the mitochondrial genome, into daughter cells after mitosis or meiosis, mediated by interactions between mitochondria and the cytoskeleton." [GOC:mcc, PMID:10873824, PMID:11389764] |
| -21 | mitochondrial genome maintenance | GO:0000002 | "The maintenance of the structure and integrity of the mitochondrial genome; includes replication and segregation of the mitochondrial chromosome." [GOC:ai, GOC:vw] |
| -51 | 2Fe-2S | KW-0001 | "Protein which contains at least one 2Fe-2S iron-sulfur cluster: 2 iron atoms complexed to 2 inorganic sulfides and 4 sulfur atoms of cysteines from the protein." [] |
| -51 | 3D-structure | KW-0002 | "Protein, or part of a protein, whose three-dimensional structure has been resolved experimentally (for example by X-ray crystallography or NMR spectroscopy) and whose coordinates are available in the PDB database. Can also be used for theoretical models." [] |
| -51 | 4Fe-4S | KW-0004 | "Protein which contains at least one 4Fe-4S iron-sulfur cluster: 4 iron atoms complexed to 4 inorganic sulfides and 4 sulfur atoms of cysteines from the protein. In a number of iron-sulfur proteins, the 4Fe-4S cluster can be reversibly converted by oxidation and loss of one iron ion to a 3Fe-4S cluster." [] |
| -51 | Abscisic acid biosynthesis | KW-0937 | "Protein involved in the synthesis of abscisic acid (ABA) (5-(1-hydroxy-2,6,6,trimethyl-4-oxocyclohex-2-en-1-y1)-3-methylpenta-2,4-dienoic acid). ABA is a plant hormone which play a role in many aspects of plant growth, development and cellular signaling (e.g. seed dormancy, seed maturation, vegetative growth and responses to various environmental stimuli such as stomatal closure during drought). This phytohormone can be synthesized from farnesyl diphosphate (direct C15 pathway) or from 9-cis-violaxanthine (indirect C40 pathway)." [] |
| -52 | Metabolic pathways | KEGG:01100 |
| -52 | Biosynthesis of secondary metabolites | KEGG:01110 | |
| -52 | Microbial metabolism in diverse environments | KEGG:01120 |
| -53 | 14_3_3 | SM00101 | 14-3-3 homologues; 14-3-3 homologues mediates signal transduction... |
| -53 | 35EXOc | SM00474 | 3'-5' exonuclease; 3\' -5' exonuclease proofreading domain presen... |
| -54 | Kringle | IPR000001 | |
| -54 | Retinoid X receptor/HNF4 | IPR000003 | |
| -55 | 7tm_1 | PF00001 | 7 transmembrane receptor (rhodopsin family) |
| -55 | 7tm_2 | PF00002 | 7 transmembrane receptor (Secretin family) |


### function_2_ENSP [Function_2_ENSP_table_STRING.txt]
| taxid | etype | association | background_count | background_n | an_array |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 9606 | -21 | 'GO:0006810' | 3 | 3919 | {'9606.ENSP00000000233', '9606.ENSP00000000412', ... } |
| 9606 | -21 | 'GO:0006897' | 2 | 3919 | {'9606.ENSP00000000412', ...} |
| 9606 | -21 | 'GO:0006898' | 1 | 3919 | {'9606.ENSP00000000412'} |

### go_2_slim [GO_2_Slim_table_STRING.txt]
| an | slim |
|:---:|:---:|
| GO:0000003 | 1 |


### ontologies [Ontologies_table_STRING.txt]
| child | parent | direct | etype |
|:---:|:---:|:---:|:---:|
| GO:0008152 | GO:0008150 | 1 | -21 |
| GO:0032259 | GO:0008152 | 1 | -21 |
| GO:0032259 | GO:0008150 | 0 | -21 |
| GO:0097042 | GO:0005575 | 0 | -22 |
| GO:0072591 | GO:0003674 | 0 | -23 |
| KW-0440 | KW-9993 | 0 | -51 |
| KW-0440 | KW-9994 | 1 | -51 |


### protein_2_function [Protein_2_Function_table_STRING.txt]
| etype | an | func_array |
|:---:|:---:|:---:|
| -21 | 9606.ENSP00000000233 | {"GO:0006810","GO:0007154","GO:0007165","GO:0007264","GO:0008104","GO:0008150","GO:0008150","GO:0008152","GO:0009987","GO:0015031","GO:0015833","GO:0016192","GO:0023052","GO:0033036","GO:0035556","GO:0042886","GO:0044700","GO:0044763","GO:0045184","GO:0050789","GO:0050794","GO:0050896","GO:0051179","GO:0051234","GO:0051716","GO:0065007","GO:0071702","GO:0071705"} |
| -22 | 9606.ENSP00000000233 | {"GO:0005575","GO:0005576","GO:0005622","GO:0005623","GO:0005737","GO:0005794","GO:0005886","GO:0012505","GO:0016020","GO:0031982","GO:0031988","GO:0043226","GO:0043227","GO:0043229","GO:0043230","GO:0043231","GO:0044421","GO:0044424","GO:0044444","GO:0044464","GO:0048471","GO:0065010","GO:0070062","GO:0071944","GO:1903561"} |
| -23 | 9606.ENSP00000000233 | {"GO:0000166","GO:0001882","GO:0001883","GO:0003674","GO:0003824","GO:0003924","GO:0005488","GO:0005525","GO:0016462","GO:0016787","GO:0016817","GO:0016818","GO:0017076","GO:0017111","GO:0019001","GO:0032549","GO:0032550","GO:0032553","GO:0032555","GO:0032561","GO:0035639","GO:0036094","GO:0043167","GO:0043168","GO:0097159","GO:0097367","GO:1901265","GO:1901363"} |
| -51 | 9606.ENSP00000000233 | {"KW-0002","KW-0181","KW-0333","KW-0342","KW-0449","KW-0472","KW-0519","KW-0547","KW-0653","KW-0813","KW-0931","KW-0963","KW-1185","KW-9990","KW-9991","KW-9993","KW-9998","KW-9999"} |
| -52 | 9606.ENSP00000000233 | {"KEGG:04144"} |
| -53 | 9606.ENSP00000000233 | {"Arf","Gtr1_RagA","MMR_HSR1","Ras","Roc","SRPRB"}" |
| -53 | 9606.ENSP00000005587 | {"SM00233","SM00326"} |
| -54 | 9606.ENSP00000000233 | {"IPR005225","IPR006689","IPR024156","IPR027417"} |
| -55 | 9606.ENSP00000000412 | {"PF09451","PF02157"} |


### taxid_2_protein [TaxID_2_Protein_table_STRING.txt]
| taxid | count | an_array |
|:---:|:---:|:---:|
| 9606 | 19566 | {"9606.ENSP00000000233","9606.ENSP00000000412","9606.ENSP00000001008","9606.ENSP00000001146", ...} |
| 1000565 | 12345 | {"1000565.METUNv1_00006","1000565.METUNv1_00011","1000565.METUNv1_00018","1000565.METUNv1_00019", ...} |
