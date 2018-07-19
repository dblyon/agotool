## functions [Functions_table.txt]
##### UPK --> DONE
##### GO --> DONE
##### KEGG --> DONE but might need an additional tab (empty string)
##### Domains ToDo missing
#####  type (Text); name(Text); an(Text);  definition(Text)
#####  type (Text); name(Text); an(Text) --> STRING?
| type | name | an | definition |
|:---:|:---:|:---:|:---:|
| GO | dipeptidyl-peptidase activity | GO:0008239 | blabla definition |
| GO | sulfuric ester hydrolase activity | GO:0008484 | blabla definition |
| GO | biological process | GO:0008150 | blabla definition |
| GO | metabolic process | GO:0008152 | blabla definition |
| UPK | Aminopeptidase | UPK:0031 | blabla definition |
| UPK | 3D-structure | UPK:0002 | blabla definition |
| UPK | Technical term | UPK:9990 | blabla definition |
| UPK | Biological process | UKW:9999 | blabla definition |
| UPK | Domain | UPK:9994 | blabla definition |
| DOM | Sulfatase | DOM:Sulfatase | blabla definition |
| KEGG | D-Glutamine and D-glutamate metabolism | KEGG:00471 | blabla definition |
| KEGG | Steroid hormone biosynthesis | KEGG:00140 | blabla definition |
| KEGG | Metabolic pathways | KEGG:01100 | blabla definition |
| KEGG | Pentose phosphate pathway | KEGG:00030 | blabla definition |
| KEGG | Cell cycle | KEGG:04110 | blabla definition |

## protein_2_function [Protein_2_Function_table.txt] (the only one that can't be in memory)
##### ToDO concatenate files and sort
##### PMID missing
##### ? ENSP with or without TaxID prefix ? --> with
##### ? add column with TaxID --> 1. to cluster DB   2. TaxID 2 proteins becomes superfluous (but probably faster) ? --> no
##### ? if ENSP have TaxID as prefix then clustering according to "TaxID" column becomes unnecessary
##### AccessionNumber(Text); function_array(Text Array); EntityType(Integer)
| an | func_array | etype |
|:---:|:---:|:---:|
| P31946 | {"UPK:0002", "UPK:0003"} | -51 |
| P31946 | {"GO:0019899"} | -23 |
| P31946 | {"GO:0051220"} | -21 |
| P31946 | {"KEGG:04110"} | -52 |

## entity_types [Entity_types_table.txt] --> DONE
##### AccessionNumber(Text); EntityType(Integer); Name(Text)
| an | etype | name |
|:---:|:---:|:---:|
| GO:0003674 | -23 | GO molecular function |
| GO:0005575 | -22 | GO cellular component |
| GO:0008150 | -21 | GO biological process |
| GO:OBSOLETE | -24 | GO obsolete |
| UPK:9990 | -51 | UniProt keyword Technical term |
| UPK:9991 | -51 | UniProt keyword PTM |
| UPK:9992 | -51 | UniProt keyword Molecular function |
| UPK:9993 | -51 | UniProt keyword Ligand |
| UPK:9994 | -51 | UniProt keyword Domain |
| UPK:9995 | -51 | UniProt keyword Disease |
| UPK:9996 | -51 | UniProt keyword Developmental stage |
| UPK:9997 | -51 | UniProt keyword Coding sequence diversity |
| UPK:9998 | -51 | UniProt keyword Cellular component |
| UPK:9999 | -51 | UniProt keyword Biological process |
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


## taxid_2_proteins [TaxID_2_Proteins_table.txt] --> DONE
##### TaxID (Integer); AccessionNumber_Array (Text Array)
| taxid | an_array |
|:---:|:---:|
| 9606 | {"P31946", "P04637", ...} |
| 10090 | {"P02340", ...} |

## go_2_slim [GO_2_Slim_table.txt] --> DONE
##### an(Text); slim(Boolean)
| an | slim |
|:---:|:---:|
| GO:0000003 | 1 |

# ? deprecated ?
## ontologies [Ontologies_table.txt] --> DONE
##### child(Text); parent(Text); direct(Integer); type(Integer)
| child | parent | direct | type |
|:---:|:---:|:---:|:---:|
| GO:0008152 | GO:0008150 | 1 | -21 |
| GO:0032259 | GO:0008152 | 1 | -21 |
| GO:0032259 | GO:0008150 | 0 | -21 |
| GO:0097042 | GO:0005575 | 0 | -22 |
| GO:0072591 | GO:0003674 | 0 | -23 |
| UPK:0440 | UPK:9993 | 0 | -51 |
| UPK:0440 | UPK:9994 | 1 | -51 |




# ?! Deprecated !?
## protein_secondary_2_primary_an [Protein_Secondary_2_Primary_AN_table.txt]
##### Secondary (Text); Prim(Text) ("Primary" is a reserved PostgreSQL word)
| sec | pri |
|:---:|:---:|
| A0A021WW06 | P40417 |
