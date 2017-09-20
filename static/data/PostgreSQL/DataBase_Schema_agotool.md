################################################################################################################
######################################################## CURRENT
## functions [Functions_table.txt]
##### type(Text); name(Text); an(Text, index-column)
| type | name | an |
|:---:|:---:|:---:|
| GO | dipeptidyl-peptidase activity | GO:0008239 |
| GO | sulfuric ester hydrolase activity | GO:0008484 |
| GO | biological process | GO:0008150 |
| GO | metabolic process | GO:0008152 |
| UPK | Aminopeptidase | UPK:0031 |
| UPK | 3D-structure | UPK:0002 |
| UPK | Technical term | UPK:9990 |
| UPK | Biological process | UKW:9999 |
| UPK | Domain | UPK:9994 |
| DOM | Sulfatase | DOM:Sulfatase |
| KEGG | D-Glutamine and D-glutamate metabolism | KEGG:00471 |
| KEGG | Steroid hormone biosynthesis | KEGG:00140 |
| KEGG | Metabolic pathways | KEGG:01100 |
| KEGG | Pentose phosphate pathway | KEGG:00030 |
| KEGG | Cell cycle | KEGG:04110 |
--> kick out DOID
| DOID | angiosarcoma | DOID:0001816 |
| DOID | pterygium | DOID:0002116 |

## function_2_definition [Function_2_definition_table.txt]
##### an(Text, index-column); definition(Text)
| an | definition |
|:---:|:---:|
| UPK:0002 | Protein, or part of a protein, whose three-dimensional structure has been resolved experimentally (for example by X-ray crystallography or NMR spectroscopy) and whose coordinates are available in the PDB database. Can also be used for theoretical models. |
| GO:0008239 | "Catalysis of the hydrolysis of N-terminal dipeptides from a polypeptide chain." [GOC:mb] |
--> kick out DOID
| DOID:0001816 | "A malignant Vascular tumor that results_in rapidly proliferating, extensively infiltrating anaplastic cells derived_from blood vessels and derived_from the lining of irregular blood-filled spaces." urls omitted due to formatting and length] |

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
--> kick out TaxIDs 
--> kick out DOID
| 9606 | 9605 | 1 | -3 |
| 9606 | 9604 | 0 | -3 |
| DOID:0001816 | DOID:4 | 0 | -26 |
| DOID:0001816 | DOID:0050687 | 0 | -26 |
| DOID:0001816 | DOID:162 | 0 | -26 |
| DOID:0001816 | DOID:14566 | 0 | -26 |
| DOID:0001816 | DOID:1115 | 1 | -26 |
| DOID:1115 | DOID:0050687 | 1 | -26 |
| DOID:0050687 | DOID:162 | 1 | -26 |
| DOID:162 | DOID:14566 | 1 | -26 |
| DOID:14566 | DOID:4 | 1 | -26 |

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

[('function_2_definition', 'an'),
 ('functions', 'an', 'type'),
 ('go_2_slim', 'an'),
 ('og_2_function', 'og', 'function'),
 ('ogs', 'og'),
 ('ontologies', 'child', 'parent', 'direct', 'type'),
 ('protein_2_function', 'an', 'function'),
 ('protein_2_og', 'an', 'og'),
 ('protein_secondary_2_primary_an', 'sec', 'pri')]
################################################################################################################
######################################################## NEW
## protein_2_function (Protein_2_Function_table.txt)
##### an(Text, index); function(Integer Array) 
##### GO terms from (math.pow(2, 63))*-1) to (math.pow(2, 63))*-1 + 47046) ((((wc -l Functions_table_GO.txt --> 47046)))) 
##### UPK from (math.pow(2, 63))*-1 + 47046 + 1) to (math.pow(2, 63))*-1 + 47046 + 1 + 1196)  ((((wc -l Functions_table_UPK.txt --> 1196)))
##### KEGG from (math.pow(2, 63))*-1 + 47046 + 1 + 1196 + 1) to (math.pow(2, 63))*-1 + 47046 + 1 + 1196 + 1 + 395) (((wc -l Functions_table_KEGG.txt --> 395)))
##### DOM from (math.pow(2, 63))*-1 + 47046 + 1 + 1196 + 1 + 395 + 1) to (math.pow(2, 63))*-1 + 47046 + 1 + 1196 + 1 + 395 + 1 + ) (((wc -l Functions_table_DOM.txt --> 6802)))
| an | function_array |
|:---:|:---:|
| P31946 | {-9223372036854775808, 9223372036854728762, 98765} |
| O9O21O | {-9223372036854775808, 9223372036854728762, 98765} |

## protein_secondary_2_primary_an (Protein_Secondary_2_Primary_AN_table.txt)
##### Secondary (Text, index-column); Prim(Text) ("Primary" is a reserved PostgreSQL word)
| sec | pri |
|:---:|:---:|
| A0A021WW06 | P40417 |

## Functions (GO_2_Slim_table.txt can be omitted)
##### "an" could be integer instead of text (but leading zeros need to be considered)
##### "slim" ToDo: why not drop and simply have txt file to parse and keep in memory
| an | func_enum | name | type | slim | definition | 
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0002 | -9223372036854775808 | 3D-structure | UPK | 0 | Protein, or part of a protein, whose three-dimensional structure has been resolved experimentally (for example by X-ray crystallography or NMR spectroscopy) and whose coordinates are available in the PDB database. Can also be used for theoretical models. |
| 0019899 | 9223372036854728762 | enzyme binding | GO | 1| Interacting selectively and non-covalently with any enzyme. Source: GOC:jl |
| 04110 | 98765 | Cell cycle | KEGG | 0 | Mitotic cell cycle progression is accomplished through a reproducible sequence of events, DNA replication (S phase) and mitosis (M phase) separated temporally by gaps known as G1 and G2 phases. Cyclin-dependent kinases (CDKs) are key regulatory enzymes, each consisting of a catalytic CDK subunit and an activating cyclin subunit. ... etc. ... |
 
##### an(Text, index-column); slim(Boolean)
| an | slim |
|:---:|:---:|
| GO:0000003 | 1 |

## Ontologies
##### child(Integer-with leading zeros, index-column); parent(same as child); direct(Integer, index-column); type(Integer, index-column)
| child | parent | direct | type |
|:---:|:---:|:---:|:---:|
| 0008152 | 0008150 | 1 | -21 |
| 0032259 | 0008152 | 1 | -21 |
| 0032259 | 0008150 | 0 | -21 |
| 0072591 | 0003674 | 0 | -23 |
| 0097042 | 0005575 | 0 | -22 |
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