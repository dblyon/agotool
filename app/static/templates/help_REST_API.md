| Name | DataType | Required/Optional | Default | Description | Example |
| :---: |  :---: |  :---: |  :---: | :---: | :---: |
| foreground | string | required | None | STRING identifier(s) for all proteins in the test group (the foreground, the sample, the group you want to examine for GO term enrichment) | "4932.YAR019C%04932.YFR028C" |
| taxid | integer | only required if enrichment_method is "genome" | None | NCBI taxon identifiers (e.g. Human is 9606, see: STRING organisms) | 9606 |
| output_format | string | optional | json | The desired format of the output, one of {tsv, tsv-no-header, json, xml} | tsv |
| limit_2_entity_type | string | optional | "-21;-22;-23;-51;-52;-53;-54;-55" (all available) | Limit the enrichment analysis to a specific or multiple entity types | '-21' (for GO molecular function) or '-21;-22;-23;-51' (for all GO terms as well as UniProt Keywords" |
| enrichment_method | string | required | genome | one of {genome, abundance_correction, compare_samples, compare_groups}. abundance_correction: Foreground vs Background abundance corrected; genome: provided foreground vs genome; compare_samples: Foreground vs Background (no abundance correction); compare_groups: Foreground(replicates) vs Background(replicates), --> foreground_n and background_n need to be set; characterize_foreground: Foreground only | genome |
| background | string | optional (not required for 'enrichment_method' 'genome') | None | STRING identifier(s) for all proteins in the background (the population, the group you want to compare your foreground to) | "4932.YAR019C%04932.YFR028C" |
| intensity | string | optional (only required for 'enrichment_method' 'abundance_correction') | None | Protein abundance (intensity) for all proteins (copy number, iBAQ, or any other measure of abundance). Separate the list using '%0d'. The number of items should correspond to the number of Accession Numbers of the 'background' | '12.3%0d3.4' |
| FDR_cutoff | float | optional | None | False Discovery Rate cutoff (threshold for multiple testing corrected p-values), 0 or not passing the parameter means no cutoff applied. | 0.001
| caller_identity | string | optional | None | Your identifier for us | www.my_awesome_app.com |
| species | string | deprecated | None | deprecated, please use 'taxid' instead | |
| organism | string | deprecated | None | deprecated, please use 'taxid' instead | |
| method | string | deprecated | None | deprecated | |
| enrichment | string | deprecated | None | deprecated | |
| identifiers | string | deprecated | None | Please use 'foreground' instead. Required parameter for multiple items | "DRD1_HUMAN%0dDRD2_HUMAN" |


| entity_type | description |
|:---:|:---:|
| -21 | GO biological process |
| -22 | GO cellular component |
| -23 | GO molecular function |
| -51 | UniProt keyword |
| -52 | KEGG |
| -53 | SMART |
| -54 | Interpro |
| -55 | PFAM |
| -56 | PMID |
