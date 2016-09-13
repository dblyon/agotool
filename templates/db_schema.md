1. [Functions](#functions)
2. [Function_2_definition](#function_2_definition)
3. [GO_2_Slim](#go_2_slim)
4. [OGs](#ogs)
5. [OG_2_Function](#og_2_function)
6. [Ontologies](#ontologies)
7. [Peptides](#peptides)
8. [Proteins](#proteins)
9. [Protein_2_Function](#protein_2_function)
10. [Protein_2_Gene](#protein_2_gene)
11. [Protein_2_OG](#protein_2_og)
12. [Protein_2_TaxID](#protein_2_taxid)
13. [Protein_2_version](#protein_2_version)
14. [Taxa](#taxa)
15. [TaxID_2_rank](#taxid_2_rank)

## Functions
| type | name | an |
|:---:|:---:|:---:|:---:|
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

## Function_2_definition
| an | definition |
|:---:|:---:|
| UPK:0002 | Protein, or part of a protein, whose three-dimensional structure has been resolved experimentally (for example by X-ray crystallography or NMR spectroscopy) and whose coordinates are available in the PDB database. Can also be used for theoretical models. |
| GO:0008239 | "Catalysis of the hydrolysis of N-terminal dipeptides from a polypeptide chain." [GOC:mb] |

## GO_2_Slim
| an | slim |
|:---:|:---:|
| GO:0000003 | 1 |

## OGs
| og | TaxID (rank superkingdom) | description |
|:---:|:---:|:---:|:---:|
| ENOG4105CZH | 2 | peptidase |
| ENOG4107QRH | 2 | Arylsulfatase (Ec 3.1.6.1) |

## OG_2_Function
| og | function |
|:---:|:---:|
|ENOG4107QRH | KEGG:00140 |
|ENOG4107QRH | GO:0008484 |
|ENOG4107QRH | DOM:Sulfatase |

## Ontologies
| child | parent | direct |
|:---:|:---:|:---:|
| GO:0008152 | GO:0008150 | 1 |
| GO:0032259 | GO:0008152 | 1 |
| GO:0032259 | GO:0008150 | 0 |
| UPK:0440 | UPK:9993 | 0 |
| UPK:0440 | UPK:9994 | 1 |
| 9606 | 9605 | 1 |
| 9606 | 9604 | 0 |

## Peptides
##### ('I' converted to 'L')
| aaseq | an | missedCleavages | length |
|:---:|:---:|:---:|:---:|
| LLLPLFAALCLSQIAHADEGMWLMQQLGR | B2RID1 | 0 | 29 |
| LLLPLFAALCLSQIAHADEGMWLMQQLGRK | B2RID1 | 1 | 30 |
| PEPTIDER | ABC123 | 0 | 8 |
| PEPTIDER | DEF456 | 0 | 8 |

## Proteins
| an | header | aaseq |
|:---:|:---:|:---:|
| B2RID1 | >sp\|B2RID1\|DPP11_PORG3 Asp/Glu-specific dipeptidyl-peptidase GN=dpp11 PE=1 SV=1 OS=Porphyromonas gingivalis (strain ATCC 33277 / DSM 20709 / CIP 103683 / JCM 12257 / NCTC 11834 / 2561) NCBI_TaxID=431947 | MKKRLLLPLFAALCLSQIAHADEGMWLMQQLGRKYAQMKERGLKMKEYDL... |
| P31946 | >sp\|P31946\|1433B_HUMAN 14-3-3 protein beta/alpha GN=YWHAB PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606 | MTMDKSELVQKAKLAEQAERYDDMAAAMKAVTEQGHELSNEERNLLSVAY... |

## Protein_2_Function
| an | function |
|:---:|:---:|
| P31946 | UPK:0002 |
| P31946 | GO:0019899 |
| P31946 | KEGG:04110 |
use for UniProt AccessionNumbers to retrieve UniProt-Keywords and GO-terms, also map UniProt ANs to KEGG ANs
HOMD ANs are mapped via OGs

## Protein_2_Gene
| prot | gene |
|:---:|:---:|
|  | ADAM6 |


## Protein_2_OG
| an | og |
|:---:|:---:|
| belk_c_455_5138 | ENOG4107WHC |
| KFI94664.1 | ENOG4105CJD |

## Protein_2_TaxID
| an | taxid |
|:---:|:---:|
| belk_c_455_5138 | 1156987 |
| B2RID1 | 837 |
| P31946 | 9606 |

## Protein_2_version
| an | version |
|:---:|:---:|
| AFN76050.1 | 201607 |
| EKD75160.1 | 201607 |
| EEI83299.1 | 201508 |
| CAR86915.1 | 201508 |
| belk_c_455_5138 | 201607 |
| belk_c_455_5138 | 201508 |
| KFI94664.1 | 201607 |
| KFI94664.1 | 201508 |
| belk_c_455_5138 | 201607 |
| belk_c_455_5138 | 201508 |

## Taxa
| TaxID | TaxName | scientific
|:---:|:---:|:---:|
| 9606 | Homo sapiens | 1 |
| 207598 | Homininae | 1 |
| 207598 | Homo/Pan/Gorilla group | 0 |
| 9443 | primates | 0 |
| 1437010| Boreoeutheria | 1 |
| 1437010| Boreotheria | 0 |
| 10380 | Herpesvirus ateles | 0 |
| 10380 | Ateline herpesvirus 2 | 1 |
from taxonomy class, parsing NCBI taxonomy dump files

## TaxID_2_rank
| TaxID | rank |
|:---:|:---:|
| 9606 | species |
| 207598 | subfamily |
| 9443 | subfamily |
| 1437010 | null/None |
| 10380 | species |
