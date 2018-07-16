## functions [Functions_table.txt]
#####  type (Text); name(Text); an(Text); definition(Text)
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
##### an(Text, index); function(Text Array) 
| an | func_array |
|:---:|:---:|
| P31946 | {"UPK:0002", "GO:0019899", "KEGG:04110"} |
| O9O21O | {"UPK:0002", "GO:0019899", "KEGG:04110"} |

#!!!
- cluster the DB #!!!
- array of arrays



## protein_2_function_long #!!! ? for STRING
## STRING version might require long format for speed?
##### AccessionNumber(Text); function_array(Text Array); Type(Integer)
| an | func_array | type |
|:---:|:---:|:---:|
| P31946 | {"UPK:0002", "UPK:0003"} | -51 |
| P31946 | {"GO:0019899"} | -23 |
| P31946 | {"GO:0051220"} | -21 |
| P31946 | {"KEGG:04110"} | -52 |

## entity_types [entity_types_table.txt]
##### AccessionNumber(Text); ID(Integer); Name(Text)
| an | id | name |
|:---:|:---:|:---:|
| GO:0003674 | -23 | Molecular Function |
| GO:0005575 | -22 | Cellular Component |
| GO:0008150 | -21 | Biological Process |
| UPK:9990 | -51 | Technical term |
| UPK:9991 | -51 | PTM |
| UPK:9992 | -51 | Molecular function |
| UPK:9993 | -51 | Ligand |
| UPK:9994 | -51 | Domain |
| UPK:9995 | -51 | Disease |
| UPK:9996 | -51 | Developmental stage |
| UPK:9997 | -51 | Coding sequence diversity |
| UPK:9998 | -51 | Cellular component |
| UPK:9999 | -51 | Biological process |
| KEGG | -52 | KEGG |
| SMART | -53 | SMART |
| Interpro | -54 | Interpro |
| Pfam | -55 | Pfam |
| PMID | -56 | PMID |


## taxid_2_proteins [TaxID_2_Proteins_table.txt] #!!! ? for STRING in order to have "genome" as available enrichment
#####
| taxid | an_array |
|:---:|:---:|
| 9606 | {"P31946", "P04637", ...} |
| 10090 | {"P02340", ...} |

## protein_secondary_2_primary_an [Protein_Secondary_2_Primary_AN_table.txt]
##### Secondary (Text); Prim(Text) ("Primary" is a reserved PostgreSQL word)
| sec | pri |
|:---:|:---:|
| A0A021WW06 | P40417 |

## go_2_slim [GO_2_Slim_table.txt]
##### an(Text); slim(Boolean)
| an | slim |
|:---:|:---:|
| GO:0000003 | 1 |

## ontologies [Ontologies_table.txt]
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

## Protein_2_OG [Protein_2_OG_table.txt]
##### an(Text, index-column); og(Text)
| an | og |
|:---:|:---:|
| belk_c_455_5138 | ENOG4107WHC |
| KFI94664.1 | ENOG4105CJD |

## OGs [OGs_table.txt]
##### og(Text; index-column); description(Text)
| og | description |
|:---:|:---:|
| ENOG4105CZH | peptidase |
| ENOG4107QRH | Arylsulfatase (Ec 3.1.6.1) |

## OG_2_Function [OG_2_Function_table.txt]
##### og(Text, index-column); function(Text)
| og | function |
|:---:|:---:|
|ENOG4107QRH | KEGG:00140 |
|ENOG4107QRH | GO:0008484 |
|ENOG4107QRH | DOM:Sulfatase |
