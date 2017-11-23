################################################################################################################
######################################################## NEW
## functions [Functions_table.txt]
#####  type (Text); name(Text); an(Text); definition(Text)
#####  type (Text); name(Text); an(Text, index-column); definition(Text)
| type | name | an | definition |
|:---:|:---:|:---:|
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

## protein_2_function [Protein_2_Function_table.txt] (only one that can't be in memory)
##### an(Text, index); function(Text Array) 
| an | func_array |
|:---:|:---:|
| P31946 | {"UPK:0002", "GO:0019899", "KEGG:04110"} |
| O9O21O | {"UPK:0002", "GO:0019899", "KEGG:04110"} |

## protein_secondary_2_primary_an [Protein_Secondary_2_Primary_AN_table.txt]
##### Secondary (Text); Prim(Text) ("Primary" is a reserved PostgreSQL word)
##### Secondary (Text, index-column); Prim(Text) ("Primary" is a reserved PostgreSQL word)
| sec | pri |
|:---:|:---:|
| A0A021WW06 | P40417 |

## go_2_slim [GO_2_Slim_table.txt]
##### an(Text); slim(Boolean)
##### an(Text, index-column); slim(Boolean)
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
##### an(Text); og(Text)
##### an(Text, index-column); og(Text)
| an | og |
|:---:|:---:|
| belk_c_455_5138 | ENOG4107WHC |
| KFI94664.1 | ENOG4105CJD |

## OGs [OGs_table.txt]
##### og(Text; index-column); taxid(Integer); description(Text)
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

################################################################################################################
######################################################## Intermediate
## protein_2_function (Protein_2_Function_table.txt) (only one that can't be in memory)
##### an(Text, index); function(Integer Array) 
##### GO terms from (math.pow(2, 63))*-1) to (math.pow(2, 63))*-1 + 47046) ((((wc -l Functions_table_GO.txt --> 47046)))) 
##### UPK from (math.pow(2, 63))*-1 + 47046 + 1) to (math.pow(2, 63))*-1 + 47046 + 1 + 1196)  ((((wc -l Functions_table_UPK.txt --> 1196)))
##### KEGG from (math.pow(2, 63))*-1 + 47046 + 1 + 1196 + 1) to (math.pow(2, 63))*-1 + 47046 + 1 + 1196 + 1 + 395) (((wc -l Functions_table_KEGG.txt --> 395)))
##### DOM from (math.pow(2, 63))*-1 + 47046 + 1 + 1196 + 1 + 395 + 1) to (math.pow(2, 63))*-1 + 47046 + 1 + 1196 + 1 + 395 + 1 + ) (((wc -l Functions_table_DOM.txt --> 6802)))
| an | func_enum_array |
|:---:|:---:|
| P31946 | {-9223372036854775808, 9223372036854728762, 98765} |
| O9O21O | {-9223372036854775808, 9223372036854728762, 98765} |

## protein_secondary_2_primary_an (Protein_Secondary_2_Primary_AN_table.txt) (keep in memory)
##### Secondary (Text, index-column); Prim(Text) ("Primary" is a reserved PostgreSQL word)
| sec | pri |
|:---:|:---:|
| A0A021WW06 | P40417 |

## Functions
#####  type (?Text or Integer see Ontologies?); an (64bit Integer, leading zeroes inferred from type, index-column); func_enum (64bit Integer index-column); name (Text, index-column)
| type | an | func_enum | name | definition |
|:---:|:---:|:---:|:---:|:---:|
| UPK | 0002 | -9223372036854775808 | 3D-structure | Protein, or part of a protein, whose three-dimensional structure has been resolved experimentally (for example by X-ray crystallography or NMR spectroscopy) and whose coordinates are available in the PDB database. Can also be used for theoretical models. |
| GO | 0019899 | 9223372036854728762 | enzyme binding | Interacting selectively and non-covalently with any enzyme. Source: GOC:jl |
| KEGG | 04110 | 98765 | Cell cycle | Mitotic cell cycle progression is accomplished through a reproducible sequence of events, DNA replication (S phase) and mitosis (M phase) separated temporally by gaps known as G1 and G2 phases. Cyclin-dependent kinases (CDKs) are key regulatory enzymes, each consisting of a catalytic CDK subunit and an activating cyclin subunit. ... etc. ... |

## go_2_slim [GO_2_Slim_table.txt] (keep in memory)
##### an(Text, index-column); slim(Boolean)
| an | slim |
|:---:|:---:|
| GO:0000003 | 1 |

## Ontologies (keep in memory)
##### child(Integer-with leading zeros or leading zeroes inferred from 'type', index-column); parent(same as child); direct(Integer, index-column); type(Integer, index-column)
| child | parent | direct | type |
|:---:|:---:|:---:|:---:|
| 0008152 | 0008150 | 1 | -21 |
| 0032259 | 0008152 | 1 | -21 |
| 0032259 | 0008150 | 0 | -21 |
| 0097042 | 0005575 | 0 | -22 |
| 0072591 | 0003674 | 0 | -23 |
| 0440 | 9993 | 0 | -51 |
| 0440 | 9994 | 1 | -51 |

## Protein_2_OG
##### an(Text, index-column); og(Text)
| an | og |
|:---:|:---:|
| belk_c_455_5138 | ENOG4107WHC |
| KFI94664.1 | ENOG4105CJD |

## OGs
| og | TaxID (rank superkingdom) | description |
|:---:|:---:|:---:|
| ENOG4105CZH | 2 | peptidase |
| ENOG4107QRH | 2 | Arylsulfatase (Ec 3.1.6.1) |

## OG_2_Function
##### og(Text, index-column); function(Text) --> BREAKS since function(needs to be Text e.g. DOM:Sulfatase)
| og | function |
|:---:|:---:|
|ENOG4107QRH | KEGG:00140 |
|ENOG4107QRH | GO:0008484 |
|ENOG4107QRH | DOM:Sulfatase |

################################################################################################################
######################################################## CURRENT/OLD
## functions [Functions_table.txt]
##### type(Text); name(Text); an(Text, index-column); definition(Text)
| type | name | an | definition |
|:---:|:---:|:---:|
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

## function_2_definition [Function_2_definition_table.txt]
##### an(Text, index-column); definition(Text)
--> removed

## go_2_slim [GO_2_Slim_table.txt]
##### an(Text, index-column); slim(Boolean)
| an | slim |
|:---:|:---:|
| GO:0000003 | 1 |

## ogs [OGs_table.txt]
##### og(Text, index-column); taxid(integer); description(text)
| og | TaxID (rank superkingdom) | description |
|:---:|:---:|:---:|
| ENOG4105CZH | 2 | peptidase |
| ENOG4107QRH | 2 | Arylsulfatase (Ec 3.1.6.1) |

## og_2_function [OG_2_Function_table.txt]
##### og(Text, index-column); function(Text)
| og | function |
|:---:|:---:|
|ENOG4107QRH | KEGG:00140 |
|ENOG4107QRH | GO:0008484 |
|ENOG4107QRH | DOM:Sulfatase |

## ontologies [Ontologies_table.txt]
##### child(Text, index-column); parent(Text); direct(Integer, index-column); type(Integer, index-column)
| child | parent | direct | type |
|:---:|:---:|:---:|:---:|
| GO:0008152 | GO:0008150 | 1 | -21 |
| GO:0032259 | GO:0008152 | 1 | -21 |
| GO:0032259 | GO:0008150 | 0 | -21 |
| GO:0072591 | GO:0003674 | 0 | -23 |
| GO:0097042 | GO:0005575 | 0 | -22 |
| UPK:0440 | UPK:9993 | 0 | -51 |
| UPK:0440 | UPK:9994 | 1 | -51 |

## protein_2_function [Protein_2_Function_table.txt]
##### an(Text, index-column); function(Text)
| an | function |
|:---:|:---:|
| P31946 | UPK:0002 |
| P31946 | GO:0019899 |
| P31946 | KEGG:04110 |

## protein_secondary_2_primary_an [Protein_Secondary_2_Primary_AN_table.txt]
##### Secondary (Text, index-column); Prim(Text) ("Primary" is a reserved PostgreSQL word)
| sec | pri |
|:---:|:---:|
| A0A021WW06 | P40417 |

 ## protein_2_og [Protein_2_OG_table.txt]
 ##### an(Text, index-column); og(Text)
| an | og |
|:---:|:---:|
| belk_c_455_5138 | ENOG4107WHC |
| KFI94664.1 | ENOG4105CJD |
     