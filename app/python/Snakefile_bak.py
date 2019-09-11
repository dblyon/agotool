import os, sys
# sys.path.insert(0, os.path.join(os.getcwd(), "python"))
# import variables_snakemake as variables
import variables
import create_SQL_tables_snakemake as cst
import download_resources_snakemake as drs
import tools
from importlib import reload
reload(cst)
reload(drs)
reload(tools)

import socket
hostname = socket.gethostname()

DOWNLOADS_DIR = variables.DOWNLOADS_DIR
TABLES_DIR = variables.TABLES_DIR
PYTHON_DIR = variables.PYTHON_DIR
NUMBER_OF_PROCESSES = variables.NUMBER_OF_PROCESSES
if NUMBER_OF_PROCESSES > 10:
    NUMBER_OF_PROCESSES_sorting = 10
else:
    NUMBER_OF_PROCESSES_sorting = NUMBER_OF_PROCESSES
verbose = variables.VERBOSE
### files that need to be created for DB
# - Functions_table_FIN.txt
# - Protein_2_FunctionEnum_table_FIN.txt
# - Entity_types_table_STRING.txt
# - Taxid_2_Proteins_table_FIN.txt
# - Taxid_2_FunctionCountArray_table_FIN.txt
# - Lineage_table_FIN.txt

### notes temp
# from UniProt dumps: UPK, GO, InterPro, Pfam, Reactome, KEGG (in combination with KEGG dump)
# missing: BTO, DOID, PMID, SMART, WikiPathways
# BTO, DOID, PMID --> are in STRING name space, map to UniProt via UniProt_2_STRING_2_KEGG
# omit SMART ?
# WikiPathways

### File nomenclature logic
# from_2_to_etype_searchspace (e.g. Protein_2_Function_UPK_STS.txt Function_2_Proteins_table_UPS.txt)
# FIN --> FINal table used for agotool
# UPS UniProt search space
# STS STRING search space


### Parameters
max_len_description = 250
min_count = 1 # Function_2_ENSP_table: minimum number of ENSPs per TaxID for a each functional_association
### scripts
parallel_parse_textmining_pmc_medline = os.path.join(PYTHON_DIR, "parallel_parse_textmining_pmc_medline.py")
################################################## URLs & Downloads
URL_GO_obo = r"http://purl.obolibrary.org/obo/go/go-basic.obo"
GO_obo = os.path.join(DOWNLOADS_DIR, "go-basic.obo")
URL_GO_slim_obo = r"http://purl.obolibrary.org/obo/go/subsets/goslim_generic.obo"
GO_slim_obo = os.path.join(DOWNLOADS_DIR, "goslim_generic.obo")
URL_UPK_obo = r"http://www.uniprot.org/keywords/?query=&format=obo"
UPK_obo = os.path.join(DOWNLOADS_DIR, "keywords-all.obo")
URL_SwissProt_dump = r"ftp://ftp.expasy.org/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz"
SwissProt_dump = os.path.join(DOWNLOADS_DIR, "uniprot_sprot.dat.gz")
URL_TrEMBL_dump = r"ftp://ftp.expasy.org/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.dat.gz"
TrEMBL_dump = os.path.join(DOWNLOADS_DIR, "uniprot_trembl.dat.gz")
UniProt_reference_proteomes_dir = os.path.join(DOWNLOADS_DIR, "UniProt_ref_prots")
### Jensenlab
URL_blacklisted_terms_Jensenlab = r"http://download.jensenlab.org/aGOtool/all_hidden.tsv"
URL_doid_obo = r"http://download.jensenlab.org/aGOtool/doid.obo"
URL_go_obo_Jensenlab = r"http://download.jensenlab.org/aGOtool/go.obo"
URL_function_2_description_PMID = r"http://download.jensenlab.org/aGOtool/documents_function2description.tsv.gz"
Function_2_Description_PMID = os.path.join(DOWNLOADS_DIR, "Function_2_Description_PMID.txt.gz")
URL_integrated_function_2_description_Jensenlab = r"http://download.jensenlab.org/aGOtool/integrated_function2description.tsv.gz"
Function_2_Description_DOID_BTO_GO_down = os.path.join(DOWNLOADS_DIR, "Function_2_Description_DOID_BTO_GO.txt.gz")
URL_protein_2_function_PMID = r"http://download.jensenlab.org/aGOtool/documents_protein2function.tsv.gz"
Protein_2_Function_table_PMID_abstracts = os.path.join(DOWNLOADS_DIR, "Protein_2_Function_table_PMID_abstracts.txt")
URL_integrated_protein_2_function_Jensenlab = r"http://download.jensenlab.org/aGOtool/integrated_protein2function.tsv.gz"
Protein_2_Function_and_Score_DOID_BTO_GOCC = os.path.join(DOWNLOADS_DIR, "Protein_2_Function_and_Score_DOID_BTO_GOCC.txt.gz")
Blacklisted_terms_Jensenlab = os.path.join(DOWNLOADS_DIR, "blacklisted_terms_Jensenlab.txt")
DOID_obo_Jensenlab = os.path.join(DOWNLOADS_DIR, "doid_Jensenlab.obo")
GO_obo_Jensenlab = os.path.join(DOWNLOADS_DIR, "go_Jensenlab.obo")
BTO_obo_Jensenlab = os.path.join(DOWNLOADS_DIR, "bto_Jensenlab.obo") # static file
### Reactome
RCTM_hierarchy = os.path.join(DOWNLOADS_DIR, "RCTM_hierarchy.tsv") # https://reactome.org/download/current/ReactomePathwaysRelation.txt
RCTM_associations = os.path.join(DOWNLOADS_DIR, "RCTM_associations.tsv") # #!!! missing ask Damian he probably did some kind of mapping
RCTM_descriptions = os.path.join(DOWNLOADS_DIR, "RCTM_descriptions.tsv") # https://reactome.org/download/current/ReactomePathways.txt # --> there is an "R-" as prefix everywhere which Damian probably took out
# pmc_medline = r"/mnt/mnemo5/dblyon/agotool/data/PostgreSQL/downloads/pmc_medline.tsv" # deprecated ?
GO_knowledge_Lars = os.path.join(DOWNLOADS_DIR, "knowledge.tsv.gz") # version10="string_go.tsv.gz" new_version="knowledge.tsv.gz" # Lars
Protein_shorthands = os.path.join(DOWNLOADS_DIR, "protein.shorthands.v11.txt")
all_entities = os.path.join(DOWNLOADS_DIR, "all_entities.tsv.gz") # Lars mapping
if hostname == "ody":
    string_matches = r"/Users/dblyon/modules/cpr/agotool/data/PostgreSQL/downloads/string_matches.tsv"
    KEGG_dir = DOWNLOADS_DIR # fake mock
    KEGG_taxonomic_rank_file = os.path.join(DOWNLOADS_DIR, "taxonomic_rank")
elif hostname == "atlas":
    string_matches = r"/mnt/mnemo5/dblyon/agotool/data/PostgreSQL/downloads/string_matches.tsv"
    KEGG_dir = r"/mnt/mnemo5/dblyon/STRING_freeze_v11/kegg/pathway/organisms"
    KEGG_taxonomic_rank_file = r"/mnt/mnemo5/dblyon/STRING_freeze_v11/kegg/genes/misc/taxonomic_rank"
KEGG_pathway = os.path.join(DOWNLOADS_DIR, "pathway.list") # Damian script --> running on cluster
KEGG_benchmarking = os.path.join(DOWNLOADS_DIR, "kegg_benchmarking.CONN_maps_in.v11.nothing_blacklisted.tsv")
URL_interpro_parent_2_child_tree = r"ftp://ftp.ebi.ac.uk/pub/databases/interpro/ParentChildTreeFile.txt"
interpro_parent_2_child_tree = os.path.join(DOWNLOADS_DIR, "interpro_parent_2_child_tree.txt")
string_2_interpro = os.path.join(DOWNLOADS_DIR, "string_2_interpro.dat.gz") # Davide
URL_uniprot_2_interpro = r"ftp://ftp.ebi.ac.uk/pub/databases/interpro/protein2ipr.dat.gz"
uniprot_2_interpro = os.path.join(DOWNLOADS_DIR, "protein2ipr.dat.gz")
URL_interpro_AN_2_name = r"ftp://ftp.ebi.ac.uk/pub/databases/interpro/entry.list"
interpro_AN_2_name = os.path.join(DOWNLOADS_DIR, "interpro_AN_2_name.txt") # InterPro_name_2_AN
uniprot_2_string_v11 = os.path.join(DOWNLOADS_DIR, "full_uniprot_2_string.jan_2018.clean.tsv") # Damain script --> run on cluster
protein_domain_annotations = os.path.join(DOWNLOADS_DIR, "string11_dom_prot_full_v3.sql") # Ivica --> static
SMART_domain_descriptions = os.path.join(DOWNLOADS_DIR, "SMART_domain_descriptions.txt")
PFAM_clans = os.path.join(DOWNLOADS_DIR, "Pfam-A.clans.tsv")
### WikiPathways
URL_WikiPathways_GMT = r"http://data.wikipathways.org/current/gmt" # monthly on the 11th
URL_UniProt_ID_mapping = r"ftp://ftp.expasy.org/databases/uniprot/current_release/knowledgebase/idmapping/idmapping_selected.tab.gz" # monthly download?
UniProt_ID_mapping = os.path.join(DOWNLOADS_DIR, "UniProt_ID_mapping_selected.tab.gz")
WikiPathways_organisms_metadata = os.path.join(DOWNLOADS_DIR, "WikiPathways_organisms_metadata.tsv") # static
WikiPathways_not_a_gmt_file = os.path.join(DOWNLOADS_DIR, "WikiPathways_not_a_gmt_file.txt")
STRING_EntrezGeneID_2_STRING = os.path.join(DOWNLOADS_DIR, "STRING_v11_all_organisms_entrez_2_string_2018.tsv.gz") # https://string-db.org/mapping_files/entrez/all_organisms.entrez_2_string.2018.tsv.gz

################################################## Tables
Protein_2_Function_table_UniProtDump_UPS = os.path.join(TABLES_DIR, "Protein_2_Function_table_UniProtDump_UPS.txt")
UniProt_2_STRING_2_KEGG = os.path.join(TABLES_DIR, "UniProt_2_STRING_2_KEGG.txt")
Protein_2_Function_table_KEGG_UPS = os.path.join(TABLES_DIR, "Protein_2_Function_table_KEGG_UPS.txt")
Protein_2_Function_table_KEGG_UPS_ENSP_benchmark = os.path.join(TABLES_DIR, "Protein_2_Function_table_KEGG_UPS_ENSP_benchmark.txt") # ENSP 2 KEGG benchmark coming from UniProt 2 KEGG and mapping STRING 2 UniProt
KEGG_entry_no_pathway_annotation = os.path.join(TABLES_DIR, "KEGG_entry_no_pathway_annotation.txt")
Functions_table_DOID_BTO_GOCC = os.path.join(TABLES_DIR, "Functions_table_DOID_BTO_GOCC.txt")
Protein_2_Function_table_PMID_STS = os.path.join(TABLES_DIR, "Protein_2_Function_table_PMID_STS.txt")
DOID_GO_BTO_an_without_translation = os.path.join(TABLES_DIR, "DOID_GO_BTO_an_without_translation.txt")
Protein_2_Function_table_PMID_fulltexts = os.path.join(TABLES_DIR, "Protein_2_Function_table_PMID_fulltexts.txt")
KEGG_Taxid_2_acronym_table_STRING = os.path.join(TABLES_DIR, "KEGG_Taxid_2_acronym_table_STRING.txt")
KEGG_Taxid_2_acronym_table_UP = os.path.join(TABLES_DIR, "KEGG_Taxid_2_acronym_table_UP.txt")
KEGG_Taxid_2_acronym_ambiguous_table = os.path.join(TABLES_DIR, "KEGG_Taxid_2_acronym_ambiguous_table.txt")
KEGG_Taxid_2_acronym_table_FIN = variables.tables_dict["KEGG_Taxid_2_acronym_table"]

Function_2_ENSP_table = os.path.join(TABLES_DIR, "Function_2_ENSP_table.txt")
Function_2_ENSP_table_reduced = os.path.join(TABLES_DIR, "Function_2_ENSP_table_reduced.txt")
Function_2_ENSP_table_removed = os.path.join(TABLES_DIR, "Function_2_ENSP_table_removed.txt")
Function_2_Proteins_table_UPS = os.path.join(TABLES_DIR, "Function_2_Proteins_table_UPS.txt")
Function_2_Proteins_table_UPS_reduced = os.path.join(TABLES_DIR, "Function_2_Proteins_table_UPS_reduced.txt")
Function_2_Proteins_table_UPS_removed = os.path.join(TABLES_DIR, "Function_2_Proteins_table_UPS_removed.txt")
Function_2_Proteins_table_FIN = os.path.join(TABLES_DIR, "Function_2_Proteins_table_FIN.txt")

Functions_table_GO = os.path.join(TABLES_DIR, "Functions_table_GO.txt")
Functions_table_InterPro = os.path.join(TABLES_DIR, "Functions_table_InterPro.txt")
Functions_table_KEGG = os.path.join(TABLES_DIR, "Functions_table_KEGG.txt")
Functions_table_PFAM = os.path.join(TABLES_DIR, "Functions_table_PFAM.txt")
Functions_table_PFAM_no_mapping = os.path.join(TABLES_DIR, "Functions_table_PFAM_no_mapping.txt")
Functions_table_PMID = os.path.join(TABLES_DIR, "Functions_table_PMID.txt") # unfiltered since filtering happens at Functions_table_FIN step via Function_2_ENSP_table
# deprecated Functions_table_GOCC_textmining = os.path.join(TABLES_DIR, "Functions_table_GOCC_textmining.txt") # redundant with GOCC but keeping this to keep a cleaner separation of textmining results with the rest, also obo file versions might differ
# Functions_table_PMID_temp = os.path.join(TABLES_DIR, "Functions_table_PMID_temp.txt") # deprecated
Functions_table_RCTM = os.path.join(TABLES_DIR, "Functions_table_RCTM.txt")
Functions_table_SMART = os.path.join(TABLES_DIR, "Functions_table_SMART.txt")
Functions_table_SMART_no_mapping = os.path.join(TABLES_DIR, "Functions_table_SMART_no_mapping.txt")
Functions_table_all = os.path.join(TABLES_DIR, "Functions_table_all.txt")
Functions_table_STRING = os.path.join(TABLES_DIR, "Functions_table_STRING.txt")
Functions_table_UniProt = os.path.join(TABLES_DIR, "Functions_table_UniProt.txt")
Functions_table_FIN = variables.tables_dict["Functions_table"]
Functions_table_removed = os.path.join(TABLES_DIR, "Functions_table_removed.txt")
Functions_table_UPK = os.path.join(TABLES_DIR, "Functions_table_UPK.txt")
Lineage_table_FIN = variables.tables_dict["Lineage_table"]
Lineage_table_no_translation = os.path.join(TABLES_DIR, "Lineage_table_no_translation.txt")
Lineage_table_hr = os.path.join(TABLES_DIR, "Lineage_table_hr.txt") # Human Readable
# Protein_2_FunctionEnum_table_FIN = os.path.join(TABLES_DIR, "Protein_2_FunctionEnum_table_FIN.txt")
Protein_2_FunctionEnum_table_FIN = variables.tables_dict["Protein_2_FunctionEnum_table"]
Protein_2_Function_table_PMID_combi = os.path.join(TABLES_DIR, "Protein_2_Function_table_PMID_combi.txt")
Protein_2_Function_table_DOID_BTO = os.path.join(TABLES_DIR, "Protein_2_Function_table_DOID_BTO.txt")
Protein_2_Function_table_GO_STS = os.path.join(TABLES_DIR, "Protein_2_Function_table_GO_STS.txt")
Protein_2_Function_table_InterPro_STS = os.path.join(TABLES_DIR, "Protein_2_Function_table_InterPro_STS.txt")
Protein_2_Function_table_KEGG_STS = os.path.join(TABLES_DIR, "Protein_2_Function_table_KEGG_STS.txt")
Protein_2_Function_table_PFAM_STS = os.path.join(TABLES_DIR, "Protein_2_Function_table_PFAM_STS.txt")
Protein_2_Function_table_RCTM_STS = os.path.join(TABLES_DIR, "Protein_2_Function_table_RCTM_STS.txt")
Protein_2_Function_table_SMART_STS = os.path.join(TABLES_DIR, "Protein_2_Function_table_SMART_STS.txt")
Protein_2_Function_table = os.path.join(TABLES_DIR, "Protein_2_Function_table.txt")
Protein_2_Function_table_reduced = os.path.join(TABLES_DIR, "Protein_2_Function_table_reduced.txt")
Protein_2_Function_table_removed = os.path.join(TABLES_DIR, "Protein_2_Function_table_removed.txt")
Protein_2_Function_table_UPK_STS = os.path.join(TABLES_DIR, "Protein_2_Function_table_UPK_STS.txt")
Protein_2_FunctionEnum_and_Score_table_FIN = os.path.join(TABLES_DIR, "Protein_2_FunctionEnum_and_Score_table_FIN.txt")
# Taxid_2_Proteins_table_STS = os.path.join(TABLES_DIR, "Taxid_2_Proteins_table_STS.txt")
Taxid_2_Proteins_table_UPS = os.path.join(TABLES_DIR, "Taxid_2_Proteins_table_UPS.txt")
# Taxid_2_Proteins_table_FIN = os.path.join(TABLES_DIR, "Taxid_2_Proteins_table_FIN.txt")
# Taxid_2_Proteins_table_FIN = variables.tables_dict["Taxid_2_Proteins_table_UPS_FIN"]
Taxid_2_FunctionCountArray_table_temp = os.path.join(TABLES_DIR, "Taxid_2_FunctionCountArray_table_temp.txt")
# Taxid_2_FunctionCountArray_table_FIN = os.path.join(TABLES_DIR, "Taxid_2_FunctionCountArray_table_FIN.txt")
Taxid_2_FunctionCountArray_table_FIN = variables.tables_dict["Taxid_2_FunctionCountArray_table"]
Taxid_2_FunctionCountArray_table_BTO_DOID_GOCC = os.path.join(TABLES_DIR, "Taxid_2_FunctionCountArray_table_BTO_DOID_GOCC.txt") # Taxid_2_FunctionCountArray_2_merge_BTO_DOID
Taxid_2_funcEnum_2_scores_table_FIN = os.path.join(TABLES_DIR, "Taxid_2_funcEnum_2_scores_table_FIN.txt")
map_name_2_an_PFAM = os.path.join(TABLES_DIR, "map_name_2_an_PFAM.txt")
map_name_2_an_SMART = os.path.join(TABLES_DIR, "map_name_2_an_SMART.txt")
AFC_KS_DIR = directory(os.path.join(TABLES_DIR, "afc_ks/"))
### temp files
Protein_2_Function_table_SMART_temp = os.path.join(TABLES_DIR, "Protein_2_Function_table_SMART_temp.txt")
Protein_2_Function_table_PFAM_temp = os.path.join(TABLES_DIR, "Protein_2_Function_table_PFAM_temp.txt")
# Functions_tables_temp = temp(os.path.join(TABLES_DIR, "Functions_tables_temp.txt")) # deprecated
# temp_dir = directory(os.path.join(TABLES_DIR, "temp"))
Protein_2_Function_table_WikiPathways = os.path.join(TABLES_DIR, "Protein_2_Function_table_WikiPathways.txt")
Functions_table_WikiPathways = os.path.join(TABLES_DIR, "Functions_table_WikiPathways.txt")
UniProt_AC_2_ID = os.path.join(TABLES_DIR, "UniProt_AC_2_ID.txt")

# TODO:
# AC 2 ID exits, but here it's AC 2 AC
# ftp://ftp.expasy.org/databases/uniprot/current_release/knowledgebase/complete/docs/sec_ac.txt
###################################################################################################
### download resources
rule download_GO_obo:
    output:
        GO_obo = GO_obo
    params:
        URL_GO_obo = URL_GO_obo,
        verbose = verbose
    run:
        drs.download_requests(params.URL_GO_obo, output.GO_obo, params.verbose)

rule download_UPK_obo:
    output:
        UPK_obo = UPK_obo
    params:
        URL_UPK_obo = URL_UPK_obo,
        verbose = verbose
    run:
        drs.download_requests(params.URL_UPK_obo, output.UPK_obo, params.verbose)

rule download_SwissProt_dump:
    output:
        SwissProt_dump = SwissProt_dump
    params:
        URL_SwissProt_dump = URL_SwissProt_dump,
        verbose = verbose
    run:
        drs.download_gzip_file(params.URL_SwissProt_dump, output.SwissProt_dump, params.verbose)

rule download_TrEMBL_dump:
    output:
        TrEMBL_dump = TrEMBL_dump
    params:
        URL_TrEMBL_dump = URL_TrEMBL_dump,
        verbose = verbose
    run:
        drs.download_gzip_file(params.URL_TrEMBL_dump, output.TrEMBL_dump, params.verbose)

rule download_Protein_2_Function_Interpro: # update cycle? InterPro is updated approximately every 8 weeks
    output:
        uniprot_2_interpro = uniprot_2_interpro
    params:
        URL_uniprot_2_interpro = URL_uniprot_2_interpro,
        verbose = verbose
    run:
        drs.download_gzip_file(params.URL_uniprot_2_interpro, output.uniprot_2_interpro, params.verbose)

rule download_descriptions_Interpro:
    output:
        interpro_AN_2_name = interpro_AN_2_name
    params:
        URL_interpro_AN_2_name = URL_interpro_AN_2_name,
        verbose = verbose
    run:
        drs.download_gzip_file(params.URL_interpro_AN_2_name, output.interpro_AN_2_name, params.verbose)

rule download_ontology_Interpro:
    output:
        interpro_parent_2_child_tree = interpro_parent_2_child_tree
    params:
        URL_interpro_parent_2_child_tree = URL_interpro_parent_2_child_tree,
        verbose = verbose
    run:
        drs.download_gzip_file(params.URL_interpro_parent_2_child_tree, output.interpro_parent_2_child_tree, verbose=params.verbose)

rule download_descriptions_PMID:
    output:
        # Function_2_Description_PMID_gz = Functions_table_PMID + ".gz",
        Function_2_Description_PMID = Function_2_Description_PMID
    params:
        URL_function_2_description_PMID = URL_function_2_description_PMID,
        verbose = verbose
    run:
        # drs.download_requests(params.URL_function_2_description_PMID, output.Function_2_Description_PMID_gz, params.verbose)
        # tools.gunzip_file(output.Function_2_Description_PMID_gz, output.Function_2_Description_PMID)
        drs.download_requests(params.URL_function_2_description_PMID, output.Function_2_Description_PMID, params.verbose)

rule download_Protein_2_Function_table_PMID_abstracts:
    output:
        Protein_2_Function_table_PMID_abstracts_gz = Protein_2_Function_table_PMID_abstracts + ".gz",
        Protein_2_Function_table_PMID_abstracts = Protein_2_Function_table_PMID_abstracts
    params:
        URL_protein_2_function_PMID = URL_protein_2_function_PMID,
        verbose = verbose
    run:
        drs.download_requests(params.URL_protein_2_function_PMID, output.Protein_2_Function_table_PMID_abstracts_gz, params.verbose)
        tools.gunzip_file(output.Protein_2_Function_table_PMID_abstracts_gz, output.Protein_2_Function_table_PMID_abstracts)

rule download_Protein_2_Function_and_Score_DOID_BTO_GOCC:
    output:
        Protein_2_Function_and_Score_DOID_BTO_GOCC = Protein_2_Function_and_Score_DOID_BTO_GOCC
    params:
        URL_integrated_protein_2_function_Jensenlab = URL_integrated_protein_2_function_Jensenlab,
        verbose = verbose
    run:
        drs.download_requests(params.URL_integrated_protein_2_function_Jensenlab, output.Protein_2_Function_and_Score_DOID_BTO_GOCC, params.verbose)

rule download_Descriptions_DOID_BTO_GO:
    output:
        Function_2_Description_DOID_BTO_GO_down = Function_2_Description_DOID_BTO_GO_down
    params:
        URL_integrated_function_2_description_Jensenlab = URL_integrated_function_2_description_Jensenlab,
        verbose = verbose
    run:
        drs.download_requests(params.URL_integrated_function_2_description_Jensenlab, output.Function_2_Description_DOID_BTO_GO_down, params.verbose)

rule download_Blacklist_Jensenlab:
    output:
        Blacklisted_terms_Jensenlab = Blacklisted_terms_Jensenlab
    params:
        URL_blacklisted_terms_Jensenlab = URL_blacklisted_terms_Jensenlab,
        verbose = verbose
    run:
        drs.download_requests(params.URL_blacklisted_terms_Jensenlab, output.Blacklisted_terms_Jensenlab, params.verbose)

rule download_DOID_obo_Jensenlab:
    output:
        DOID_obo_Jensenlab = DOID_obo_Jensenlab
    params:
        URL_doid_obo = URL_doid_obo,
        verbose = verbose
    run:
        drs.download_requests(params.URL_doid_obo, output.DOID_obo_Jensenlab, params.verbose)

rule download_GO_obo_Jensenlab:
    output:
        GO_obo_Jensenlab = GO_obo_Jensenlab
    params:
        URL_go_obo_Jensenlab = URL_go_obo_Jensenlab,
        verbose = verbose
    run:
        drs.download_requests(params.URL_go_obo_Jensenlab, output.GO_obo_Jensenlab, params.verbose)

rule download_WikiPathways:
    input:
        DOWNLOADS_DIR = DOWNLOADS_DIR
    params:
        URL_WikiPathways_GMT = URL_WikiPathways_GMT,
        verbose = verbose
    output:
        WikiPathways_not_a_gmt_file = WikiPathways_not_a_gmt_file
    run:
        drs.download_WikiPathways(params.URL_WikiPathways_GMT, input.DOWNLOADS_DIR, output.WikiPathways_not_a_gmt_file, params.verbose)

rule download_UniProt_ID_mapping:
    output:
        UniProt_ID_mapping = UniProt_ID_mapping
    params:
        URL_UniProt_ID_mapping = URL_UniProt_ID_mapping,
        verbose = verbose
    run:
        drs.download_gzip_file(params.URL_UniProt_ID_mapping, output.UniProt_ID_mapping, params.verbose)

###################################################################################################
### create tables
rule string_2_interpro:
    input: # relative path to working dir
        uniprot_2_string_v11 = uniprot_2_string_v11,
        uniprot_2_interpro = uniprot_2_interpro
    output: # relative path to working dir
        string_2_interpro = string_2_interpro
    run:
        cst.string_2_interpro(input.uniprot_2_string_v11, input.uniprot_2_interpro, output.string_2_interpro)

rule Protein_2_Function_table_InterPro_STS:
    input:
        string_2_interpro = string_2_interpro,
        Functions_table_INTERPRO = Functions_table_INTERPRO,
        interpro_parent_2_child_tree = interpro_parent_2_child_tree
    output:
        Protein_2_Function_table_InterPro_STS = Protein_2_Function_table_InterPro_STS,
    params:
        verbose = verbose
    threads: NUMBER_OF_PROCESSES_sorting
    run:
        cst.Protein_2_Function_table_InterPro_STS(input.string_2_interpro, input.Functions_table_INTERPRO, input.interpro_parent_2_child_tree, output.Protein_2_Function_table_InterPro_STS, number_of_processes=threads, verbose=params.verbose)

rule Functions_table_InterPro:
    input:
        interpro_AN_2_name = interpro_AN_2_name,
        interpro_parent_2_child_tree = interpro_parent_2_child_tree
    output:
        Functions_table_InterPro = Functions_table_InterPro
    run:
        cst.Functions_table_InterPro(input.interpro_AN_2_name, input.interpro_parent_2_child_tree, output.Functions_table_INTERPRO)

rule Functions_table_KEGG:
    input:
        KEGG_pathway = KEGG_pathway
    output:
        Functions_table_KEGG = Functions_table_KEGG
    params:
        verbose = verbose
    run:
        cst.Functions_table_KEGG(input.KEGG_pathway, output.Functions_table_KEGG, params.verbose)

rule Functions_table_SMART:
    input:
        SMART_domain_descriptions = SMART_domain_descriptions
    output:
        Functions_table_SMART = Functions_table_SMART,
        map_name_2_an_SMART = map_name_2_an_SMART
    params:
        max_len_description = max_len_description
    run:
        cst.Functions_table_SMART(input.SMART_domain_descriptions, output.Functions_table_SMART, params.max_len_description, output.map_name_2_an_SMART)

rule Functions_table_PFAM:
    input:
        PFAM_clans = PFAM_clans
    output:
        Functions_table_PFAM = Functions_table_PFAM,
        map_name_2_an_PFAM = map_name_2_an_PFAM
    run:
        cst.Functions_table_PFAM(input.PFAM_clans, output.Functions_table_PFAM, output.map_name_2_an_PFAM)

rule Functions_table_GO:
    input:
        GO_obo_Jensenlab = GO_obo_Jensenlab
    output:
        Functions_table_GO = Functions_table_GO
    params:
        is_upk = False
    run:
        cst.Functions_table_GO_or_UPK(input.GO_obo_Jensenlab, output.Functions_table_GO, params.is_upk)

rule Functions_table_UPK:
    input:
        UPK_obo = UPK_obo
    output:
        Functions_table_UPK = Functions_table_UPK
    params:
        is_upk = True
    run:
        cst.Functions_table_GO_or_UPK(input.UPK_obo, output.Functions_table_UPK, params.is_upk)

rule Protein_2_Function_table_RCTM__and__Functions_table_RCTM: # STRING space
    input:
        RCTM_associations = RCTM_associations,
        RCTM_descriptions = RCTM_descriptions,
        RCTM_hierarchy = RCTM_hierarchy
    output:
        Protein_2_Function_table_RCTM_STS = Protein_2_Function_table_RCTM_STS,
        Functions_table_RCTM = Functions_table_RCTM
    threads: NUMBER_OF_PROCESSES_sorting
    run:
        cst.Protein_2_Function_table_RCTM__and__Function_table_RCTM(input.RCTM_associations, input.RCTM_descriptions, input.RCTM_hierarchy, output.Protein_2_Function_table_RCTM_STS, output.Functions_table_RCTM, threads)

rule Functions_table_PMID:
    input:
        Function_2_Description_PMID = Function_2_Description_PMID
    output:
        Functions_table_PMID = Functions_table_PMID
    run:
        cst.Functions_table_PMID(input.Function_2_Description_PMID, output.Functions_table_PMID, max_len_description)

rule Functions_table_DOID_BTO_GOCC: # these are not being filtered to relevant ones, but since number is small (~20k), the impact should be negligible
    input:
        Function_2_Description_DOID_BTO_GO_down = Function_2_Description_DOID_BTO_GO_down,
        BTO_obo_Jensenlab = BTO_obo_Jensenlab,
        DOID_obo_Jensenlab = DOID_obo_Jensenlab,
        GO_obo_Jensenlab = GO_obo_Jensenlab,
        Blacklisted_terms_Jensenlab = Blacklisted_terms_Jensenlab
    output:
        Functions_table_DOID_BTO_GOCC = Functions_table_DOID_BTO_GOCC
    params:
        GO_CC_textmining_additional_etype = True,
        verbose = verbose
    threads: NUMBER_OF_PROCESSES_sorting
    run:
        cst.Functions_table_DOID_BTO_GOCC(input.Function_2_Description_DOID_BTO_GO_down, input.BTO_obo_Jensenlab, input.DOID_obo_Jensenlab, input.GO_obo_Jensenlab, input.Blacklisted_terms_Jensenlab, output.Functions_table_DOID_BTO_GOCC, params.GO_CC_textmining_additional_etype, threads, params.verbose)

rule Functions_table_all:
    input:
        fn_list_str = [Functions_table_InterPro,
                       Functions_table_KEGG,
                       Functions_table_SMART,
                       Functions_table_PFAM,
                       Functions_table_GO,
                       Functions_table_UPK,
                       Functions_table_PMID,
                       Functions_table_RCTM,
                       Functions_table_DOID_BTO_GOCC,
                       Functions_table_WikiPathways]
    output:
        Functions_table_all = Functions_table_all,
        # Functions_tables_temp = Functions_tables_temp
    threads: NUMBER_OF_PROCESSES_sorting
    run:
        cst.concatenate_Functions_tables(input.fn_list_str, output.Functions_tables_temp, output.Functions_table_all, threads)

# rule Taxid_2_Proteins_table_STS:
#     input:
#         Protein_shorthands = Protein_shorthands
#     output:
#         Taxid_2_Proteins_table_STS = Taxid_2_Proteins_table_STS
#     threads: NUMBER_OF_PROCESSES_sorting
#     params:
#         verbose = verbose
#     run:
#         cst.Taxid_2_Proteins_table_STS(input.Protein_shorthands, output.Taxid_2_Proteins_table_STS, threads, params.verbose)

rule download_UniProt_reference_proteomes:
    output:
        UniProt_reference_proteomes_dir = directory(UniProt_reference_proteomes_dir)
    params:
        verbose = verbose
    run:
        drs.download_UniProt_reference_proteomes(output.UniProt_reference_proteomes_dir, params.verbose)

rule Taxid_2_Proteins_table_UPS:
    input:
        UniProt_reference_proteomes_dir = UniProt_reference_proteomes_dir
    output:
        Taxid_2_Proteins_table_UPS = Taxid_2_Proteins_table_UPS
    run:
        cst.Taxid_2_Proteins_table_UPS(input.UniProt_reference_proteomes_dir, output.Taxid_2_Proteins_table_UPS)

# rule Taxid_2_Proteins_table_FIN: #  --> Snakemake_STRING
#     input:
#         Taxid_2_Proteins_table_STS = Taxid_2_Proteins_table_STS,
#         Taxid_2_Proteins_table_UPS = Taxid_2_Proteins_table_UPS
#     output:
#         Taxid_2_Proteins_table_FIN = Taxid_2_Proteins_table_FIN
#     threads: NUMBER_OF_PROCESSES_sorting
#     params:
#         verbose = verbose
#     run:
#         cst.Taxid_2_Proteins_table_FIN(input.Taxid_2_Proteins_table_STS, input.Taxid_2_Proteins_table_UPS, output.Taxid_2_Proteins_table_FIN, threads, params.verbose)

rule Taxid_2_funcEnum_2_scores_table_FIN:
    input:
        Protein_2_FunctionEnum_and_Score_table_FIN = Protein_2_FunctionEnum_and_Score_table_FIN
    output:
        Taxid_2_funcEnum_2_scores_table_FIN = Taxid_2_funcEnum_2_scores_table_FIN
    run:
        cst.Taxid_2_funcEnum_2_scores_table_FIN(input.Protein_2_FunctionEnum_and_Score_table_FIN, output.Taxid_2_funcEnum_2_scores_table_FIN)

rule Protein_2_Function_table_SMART__and__PFAM_helper: # STRING space
    input:
        protein_domain_annotations = protein_domain_annotations
    output:
        Protein_2_Function_table_SMART_temp = Protein_2_Function_table_SMART_temp,
        Protein_2_Function_table_PFAM_temp = Protein_2_Function_table_PFAM_temp
    threads: NUMBER_OF_PROCESSES_sorting
    params:
        verbose = verbose
    run:
        cst.Protein_2_Function_table_SMART_and_PFAM_temp(input.protein_domain_annotations, output.Protein_2_Function_table_SMART_temp, output.Protein_2_Function_table_PFAM_temp, threads, params.verbose)

rule Protein_2_Function_table_SMART_STS:
    input:
        Protein_2_Function_table_SMART_temp = Protein_2_Function_table_SMART_temp,
        map_name_2_an_SMART = map_name_2_an_SMART
    output:
        Protein_2_Function_table_SMART_STS = Protein_2_Function_table_SMART_STS,
        Functions_table_SMART_no_mapping = Functions_table_SMART_no_mapping
    run:
        cst.map_Name_2_AN(input.Protein_2_Function_table_SMART_temp, output.Protein_2_Function_table_SMART_STS, input.map_name_2_an_SMART, output.Functions_table_SMART_no_mapping)

rule Protein_2_Function_table_PFAM_STS:
    input:
        Protein_2_Function_table_PFAM_temp = Protein_2_Function_table_PFAM_temp,
        map_name_2_an_PFAM = map_name_2_an_PFAM
    output:
        Protein_2_Function_table_PFAM_STS = Protein_2_Function_table_PFAM_STS,
        Functions_table_PFAM_no_mapping = Functions_table_PFAM_no_mapping
    run:
        cst.map_Name_2_AN(input.Protein_2_Function_table_PFAM_temp, output.Protein_2_Function_table_PFAM_STS, input.map_name_2_an_PFAM, output.Functions_table_PFAM_no_mapping)

rule Protein_2_Function_table_GO_STS:
    input:
        GO_knowledge_Lars = GO_knowledge_Lars,
        GO_obo_Jensenlab = GO_obo_Jensenlab
    output:
        Protein_2_Function_table_GO_STS = Protein_2_Function_table_GO_STS
    threads: NUMBER_OF_PROCESSES_sorting
    params:
        verbose = verbose
    run:
        cst.Protein_2_Function_table_GO_STS(input.GO_obo_Jensenlab, input.GO_knowledge_Lars, output.Protein_2_Function_table_GO_STS, threads, params.verbose)

rule Protein_2_Function_table_UPK_STS: # STRING Space
    input:
        Functions_table_UPK = Functions_table_UPK,
        UPK_obo = UPK_obo,
        SwissProt_dump = SwissProt_dump,
        TrEMBL_dump = TrEMBL_dump,
        uniprot_2_string_v11 = uniprot_2_string_v11
    output:
        Protein_2_Function_table_UPK_STS = Protein_2_Function_table_UPK_STS
    threads: NUMBER_OF_PROCESSES_sorting
    params:
        verbose = verbose
    run:
        cst.Protein_2_Function_table_UPK_STS(input.Functions_table_UPK, input.UPK_obo, input.SwissProt_dump, input.TrEMBL_dump, input.uniprot_2_string_v11, output.Protein_2_Function_table_UPK_STS, threads, params.verbose)

# rule Protein_2_Function_table_PMID_fulltexts: # STRING space
#     input:
#         all_entities = all_entities,
#         string_matches = string_matches,
#         Taxid_2_Proteins_table_STS = Taxid_2_Proteins_table_STS,
#     output:
#         Protein_2_Function_table_PMID_fulltexts = Protein_2_Function_table_PMID_fulltexts
#     run:
#         cst.Protein_2_Function_table_PMID_fulltexts(input.all_entities, input.string_matches, input.Taxid_2_Proteins_table_STS, output.Protein_2_Function_table_PMID_fulltexts)

rule Protein_2_Function_table_PMID_STS: # STRING space
    input:
        Taxid_2_Proteins_table_STS = Taxid_2_Proteins_table_STS,
        Protein_2_Function_table_PMID_abstracts = Protein_2_Function_table_PMID_abstracts,
        Protein_2_Function_table_PMID_fulltexts = Protein_2_Function_table_PMID_fulltexts
    output:
        Protein_2_Function_table_PMID_combi = Protein_2_Function_table_PMID_combi,
        Protein_2_Function_table_PMID_STS = Protein_2_Function_table_PMID_STS
    threads: NUMBER_OF_PROCESSES_sorting
    params:
        verbose = verbose
    run:
        cst.Protein_2_Function_table_PMID_STS(input.Taxid_2_Proteins_table_STS, input.Protein_2_Function_table_PMID_abstracts, input.Protein_2_Function_table_PMID_fulltexts, output.Protein_2_Function_table_PMID_combi, output.Protein_2_Function_table_PMID_STS, threads, params.verbose)

rule Protein_2_Function__and__Functions_table_WikiPathways: # ENSPs and UniProt AC/ID
    input:
        WikiPathways_organisms_metadata = WikiPathways_organisms_metadata,
        UniProt_ID_mapping = UniProt_ID_mapping,
        STRING_EntrezGeneID_2_STRING = STRING_EntrezGeneID_2_STRING,
        Taxid_2_Proteins_table_STS = Taxid_2_Proteins_table_STS,
        WikiPathways_not_a_gmt_file = WikiPathways_not_a_gmt_file
    output:
        Protein_2_Function_table_WikiPathways = Protein_2_Function_table_WikiPathways,
        Functions_table_WikiPathways = Functions_table_WikiPathways
    params:
        verbose = verbose
    run:
        cst.Protein_2_Function__and__Functions_table_WikiPathways(input.WikiPathways_organisms_metadata, input.UniProt_ID_mapping, input.STRING_EntrezGeneID_2_STRING, input.Taxid_2_Proteins_table_STS, input.WikiPathways_not_a_gmt_file, output.Functions_table_WikiPathways, output.Protein_2_Function_table_WikiPathways, params.verbose)

rule Protein_2_Function_table:
    input:
        Taxid_2_Proteins_table_FIN = Taxid_2_Proteins_table_FIN,
        fn_list_str = [Protein_2_Function_table_InterPro_STS,
                       Protein_2_Function_table_KEGG_STS,
                       Protein_2_Function_table_SMART_STS,
                       Protein_2_Function_table_PFAM_STS,
                       Protein_2_Function_table_GO_STS,
                       Protein_2_Function_table_UPK_STS,
                       Protein_2_Function_table_PMID_STS,
                       Protein_2_Function_table_RCTM_STS,
                       Protein_2_Function_table_WikiPathways, # STS & UPS
                       Protein_2_Function_table_UniProtDump_UPS] # UPK, GO, RCTM, Interpro, PFam
                       # Protein_2_Function_table_DOID_BTO
    output:
        Protein_2_Function_table = Protein_2_Function_table
    threads: NUMBER_OF_PROCESSES_sorting
    run:
        cst.Protein_2_Function_table(input.fn_list_str, input.Taxid_2_Proteins_table_FIN, output.Protein_2_Function_table, threads)

rule Function_2_ENSP_table:
    input:
        Protein_2_Function_table = Protein_2_Function_table,
        Taxid_2_Proteins_table_STS = Taxid_2_Proteins_table_STS,
        Functions_table_all = Functions_table_all,
    output:
        Function_2_ENSP_table = Function_2_ENSP_table,
        Function_2_ENSP_table_reduced = Function_2_ENSP_table_reduced,
        Function_2_ENSP_table_removed = Function_2_ENSP_table_removed
    params:
        min_count = min_count,
        verbose = verbose
    run:
        cst.Function_2_ENSP_table(input.Protein_2_Function_table, input.Taxid_2_Proteins_table_STS, input.Functions_table_all, output.Function_2_ENSP_table, output.Function_2_ENSP_table_reduced, output.Function_2_ENSP_table_removed, min_count=params.min_count, verbose=params.verbose)

rule Function_2_Proteins_table_UPS: # NotImplementedFunction
    input:
        Protein_2_Function_table_UniProtDump_UPS = Protein_2_Function_table_UniProtDump_UPS,
        Taxid_2_Proteins_table_UPS = Taxid_2_Proteins_table_UPS
    output:
        Function_2_Proteins_table_UPS = Function_2_Proteins_table_UPS,
        Function_2_Proteins_table_UPS_reduced = Function_2_Proteins_table_UPS_reduced,
        Function_2_Proteins_table_UPS_removed = Function_2_Proteins_table_UPS_removed
    run:
        cst.NotImplementedFunction()


rule Function_2_Proteins_table_FIN:
    input:
        Function_2_ENSP_table_reduced = Function_2_ENSP_table_reduced,
        Function_2_Proteins_table_UniProt_reduced = Function_2_Proteins_table_UniProt_reduced
    output:
        Function_2_Proteins_table_FIN = Function_2_Proteins_table_FIN
    run:
        cst.NotImplementedFunction(input.Function_2_ENSP_table_reduced, input.Function_2_Proteins_table_UniProt_reduced, output.Function_2_Proteins_table_FIN)

rule Functions_table_STRING: # sort before ?
    input:
        Functions_table_all = Functions_table_all,
        Function_2_ENSP_table_reduced = Function_2_ENSP_table_reduced,
    output:
        Functions_table_removed = Functions_table_removed,
        Functions_table_STRING = Functions_table_STRING
    run:
        cst.Functions_table_STRING(input.Functions_table_all, input.Function_2_ENSP_table_reduced, output.Functions_table_removed, output.Functions_table_STRING)

rule Protein_2_Function_table_reduced:
    input:
        Protein_2_Function_table = Protein_2_Function_table,
        Function_2_ENSP_table_removed = Function_2_ENSP_table_removed,
        Functions_table_STRING = Functions_table_STRING
    output:
        Protein_2_Function_table_reduced = Protein_2_Function_table_reduced,
        Protein_2_Function_table_removed = Protein_2_Function_table_removed
    run:
        cst.Protein_2_Function_table_reduced(input.Protein_2_Function_table, input.Function_2_ENSP_table_removed, input.Functions_table_STRING, output.Protein_2_Function_table_reduced, output.Protein_2_Function_table_removed)

rule Protein_2_FunctionEnum_table_FIN:
    input:
        Protein_2_Function_table_reduced = Protein_2_Function_table_reduced,
        Functions_table_STRING = Functions_table_STRING
    output:
        Protein_2_FunctionEnum_table_FIN = Protein_2_FunctionEnum_table_FIN
    threads: NUMBER_OF_PROCESSES_sorting
    run:
        cst.Protein_2_FunctionEnum_table_FIN(input.Functions_table_STRING, input.Protein_2_Function_table_reduced, output.Protein_2_FunctionEnum_table_FIN, threads)

rule Lineage_table_FIN:
    input:
        GO_obo_Jensenlab = GO_obo_Jensenlab,
        UPK_obo = UPK_obo,
        RCTM_hierarchy = RCTM_hierarchy,
        interpro_parent_2_child_tree = interpro_parent_2_child_tree,
        Functions_table_STRING = Functions_table_STRING,
        DOID_obo_Jensenlab = DOID_obo_Jensenlab,
        BTO_obo_Jensenlab = BTO_obo_Jensenlab
    output:
        Lineage_table_FIN = Lineage_table_FIN,
        Lineage_table_no_translation = Lineage_table_no_translation,
        Lineage_table_hr = Lineage_table_hr
    params:
        GO_CC_textmining_additional_etype = True
    run:
        cst.Lineage_table_FIN(input.GO_obo_Jensenlab, input.UPK_obo, input.RCTM_hierarchy, input.interpro_parent_2_child_tree, input.Functions_table_STRING, input.DOID_obo_Jensenlab, input.BTO_obo_Jensenlab, output.Lineage_table_FIN, output.Lineage_table_no_translation, output.Lineage_table_hr, params.GO_CC_textmining_additional_etype)

rule Taxid_2_FunctionCountArray_table_FIN:
    input:
        Protein_2_FunctionEnum_table_FIN = Protein_2_FunctionEnum_table_FIN,
        Functions_table_STRING = Functions_table_STRING,
        Taxid_2_Proteins_table_FIN = Taxid_2_Proteins_table_FIN
        # Taxid_2_FunctionCountArray_table_BTO_DOID = Taxid_2_FunctionCountArray_table_BTO_DOID
        # tables could be merged at some later point #!!!
    output:
        # Taxid_2_FunctionCountArray_table_temp = Taxid_2_FunctionCountArray_table_temp,
        Taxid_2_FunctionCountArray_table_FIN = Taxid_2_FunctionCountArray_table_FIN
    threads: NUMBER_OF_PROCESSES_sorting
    params:
        verbose = verbose
    run:
        cst.Taxid_2_FunctionCountArray_table_FIN(input.Protein_2_FunctionEnum_table_FIN, input.Functions_table_STRING, input.Taxid_2_Proteins_table_FIN, output.Taxid_2_FunctionCountArray_table_FIN, threads, params.verbose)

rule AFC_KS_enrichment_terms_flat_files:
    input:
        Protein_shorthands = Protein_shorthands,
        Functions_table_STRING = Functions_table_STRING,
        Function_2_ENSP_table_reduced = Function_2_ENSP_table_reduced,
        KEGG_Taxid_2_acronym_table_STRING = KEGG_Taxid_2_acronym_table_STRING
    output:
        AFC_KS_DIR = AFC_KS_DIR
    params:
        verbose = verbose
    run:
        cst.AFC_KS_enrichment_terms_flat_files(input.Protein_shorthands, input.Functions_table_STRING, input.Function_2_ENSP_table_reduced, input.KEGG_Taxid_2_acronym_table_STRING, output.AFC_KS_DIR, params.verbose)

rule KEGG_Taxid_2_acronym_table_UP:
    input:
        KEGG_taxonomic_rank_file = KEGG_taxonomic_rank_file
    output:
        KEGG_Taxid_2_acronym_table_UP = KEGG_Taxid_2_acronym_table_UP
    run:
        cst.KEGG_Taxid_2_acronym_table_UP(input.KEGG_taxonomic_rank_file, output.KEGG_Taxid_2_acronym_table_UP)

rule KEGG_Taxid_2_acronym_table_FIN:
    input:
        KEGG_Taxid_2_acronym_table_STRING = KEGG_Taxid_2_acronym_table_STRING,
        KEGG_Taxid_2_acronym_table_UP = KEGG_Taxid_2_acronym_table_UP
    output:
        KEGG_Taxid_2_acronym_table_FIN = KEGG_Taxid_2_acronym_table_FIN,
        KEGG_Taxid_2_acronym_ambiguous_table = KEGG_Taxid_2_acronym_ambiguous_table
    run:
        cst.KEGG_Taxid_2_acronym_table_FIN(input.KEGG_Taxid_2_acronym_table_STRING, input.KEGG_Taxid_2_acronym_table_UP, output.KEGG_Taxid_2_acronym_table_FIN, output.KEGG_Taxid_2_acronym_ambiguous_table)

rule Protein_2_FunctionEnum_and_Score_table_FIN: # retain_scores
    input:
        Protein_2_Function_and_Score_DOID_BTO_GOCC = Protein_2_Function_and_Score_DOID_BTO_GOCC,
        Functions_table_STRING = Functions_table_STRING,
        Taxid_2_Proteins_table_FIN = Taxid_2_Proteins_table_FIN
    output:
        Protein_2_FunctionEnum_and_Score_table_FIN = Protein_2_FunctionEnum_and_Score_table_FIN,
        DOID_GO_BTO_an_without_translation = DOID_GO_BTO_an_without_translation
    params:
        GO_CC_textmining_additional_etype = True
    run:
        cst.Protein_2_FunctionEnum_and_Score_table_FIN(input.Protein_2_Function_and_Score_DOID_BTO_GOCC, input.Functions_table_STRING, input.Taxid_2_Proteins_table_FIN, output.Protein_2_FunctionEnum_and_Score_table_FIN, output.DOID_GO_BTO_an_without_translation, params.GO_CC_textmining_additional_etype)

rule Protein_2_Function_table_KEGG_STS:
    input:
        KEGG_benchmarking = KEGG_benchmarking
    output:
        Protein_2_Function_table_KEGG_STS = Protein_2_Function_table_KEGG_STS,
        KEGG_Taxid_2_acronym_table_STRING = KEGG_Taxid_2_acronym_table_STRING
    threads: NUMBER_OF_PROCESSES_sorting
    run:
        cst.Protein_2_Function_table_KEGG_STS(input.KEGG_benchmarking, output.Protein_2_Function_table_KEGG_STS, output.KEGG_Taxid_2_acronym_table_STRING, threads)

rule Protein_2_Function_table_KEGG_UPS: # and Protein_2_Function_table_KEGG_UP_ENSP_benchmark
    input:
        KEGG_dir = KEGG_dir,
        UniProt_2_STRING_2_KEGG = UniProt_2_STRING_2_KEGG
    output:
        Protein_2_Function_table_KEGG_UPS = Protein_2_Function_table_KEGG_UPS,
        Protein_2_Function_table_KEGG_UPS_ENSP_benchmark = Protein_2_Function_table_KEGG_UPS_ENSP_benchmark,
        KEGG_entry_no_pathway_annotation = KEGG_entry_no_pathway_annotation
    run:
        cst.Protein_2_Function_table_KEGG_UPS_and_ENSP_2_KEGG_benchmark(input.KEGG_dir, input.UniProt_2_STRING_2_KEGG, output.Protein_2_Function_table_KEGG_UPS, output.Protein_2_Function_table_KEGG_UPS_ENSP_benchmark, output.KEGG_entry_no_pathway_annotation)

rule Protein_2_Function_table_UniProtDump_UPS: # Protein_2_Function_table_UniProtDump_UPS
    input:
        Functions_table_UPK = Functions_table_UPK,
        GO_obo = GO_obo, # not Jensenlab obo
        UPK_obo = UPK_obo,
        SwissProt_dump = SwissProt_dump,
        TrEMBL_dump = TrEMBL_dump,
        interpro_parent_2_child_tree = interpro_parent_2_child_tree,
        RCTM_hierarchy = RCTM_hierarchy
    output:
        Protein_2_Function_table_UniProtDump_UPS = Protein_2_Function_table_UniProtDump_UPS, # UPK, GO, RCTM, Interpro, PFam
        UniProt_2_STRING_2_KEGG = UniProt_2_STRING_2_KEGG,
        UniProt_AC_2_ID = UniProt_AC_2_ID
    params:
        verbose = verbose
    run:
        cst.Protein_2_Function_table_UniProtDump_UPS(input.Functions_table_UPK, input.GO_obo, input.UPK_obo, [input.SwissProt_dump, input.TrEMBL_dump], input.interpro_parent_2_child_tree, input.RCTM_hierarchy,  output.Protein_2_Function_table_UniProtDump_UPS, output.UniProt_2_STRING_2_KEGG, output.UniProt_AC_2_ID, params.verbose)

##########################################################################################
##########################################################################################
### archive code might be deprecated | RIP code
# rule Protein_2_Function_table_DOID_BTO: # hard_cutoff
#     input:
#         Protein_2_Function_and_Score_DOID_BTO_GOCC = Protein_2_Function_and_Score_DOID_BTO_GOCC,
#         Taxid_2_Proteins_table_FIN = Taxid_2_Proteins_table_FIN
#     output:
#         Protein_2_Function_table_DOID_BTO = Protein_2_Function_table_DOID_BTO,
#     params:
#         score_cutoff = 3.0
#     run:
#         cst.Protein_2_Function_table_DOID_BTO(input.Protein_2_Function_and_Score_DOID_BTO_GOCC, input.Taxid_2_Proteins_table_FIN, params.score_cutoff, output.Protein_2_Function_table_DOID_BTO)

# rule UniProt_2_STRING_2_KEGG:
#     input:
#         SwissProt_dump = SwissProt_dump,
#         TrEMBL_dump = TrEMBL_dump
#     output:
#         UniProt_2_STRING_2_KEGG = UniProt_2_STRING_2_KEGG
#     run:
#         cst.UniProt_2_STRING_2_KEGG_from_dump(fn_in_list_uniprot_dumps=[input.SwissProt_dump, input.TrEMBL_dump], fn_out_UniProt_2_STRING_2_KEGG=output.UniProt_2_STRING_2_KEGG)
# rule Taxid_2_FunctionCountArray_table_BTO_DOID_GOCC: # retain_score
#     input:
#         Taxid_2_Proteins_table_FIN = Taxid_2_Proteins_table_FIN,
#         Functions_table_STRING = Functions_table_STRING,
#         Protein_2_FunctionEnum_and_Score_table_STRING = Protein_2_FunctionEnum_and_Score_table_STRING
#     output:
#         Taxid_2_FunctionCountArray_table_BTO_DOID_GOCC = Taxid_2_FunctionCountArray_table_BTO_DOID_GOCC
#     threads: NUMBER_OF_PROCESSES_sorting
#     params:
#         verbose = verbose
#     run:
#         cst.Taxid_2_FunctionCountArray_table_BTO_DOID_GOCC(input.Taxid_2_Proteins_table_FIN, input.Functions_table_STRING, input.Protein_2_FunctionEnum_and_Score_table_STRING, output.Taxid_2_FunctionCountArray_table_BTO_DOID_GOCC, threads, params.verbose)

# rule Functions_table_GOCC_textmining: # using Functions_table_DOID_BTO_GOCC instead
#     input:
#         GO_obo_Jensenlab = GO_obo_Jensenlab
#     output:
#         Functions_table_GOCC_textmining = Functions_table_GOCC_textmining
#     params:
#         is_upk = False
#         GO_CC_textmining_additional_etype = True
#     run:
#         cst.Functions_table_GO_or_UPK(input.GO_obo_Jensenlab, output.Functions_table_GO, params.is_upk, param.GO_CC_textmining_additional_etype)

### deprecated since using Lars' DB dump
# rule Functions_table_PMID_temp: # textmining pmc medline --> using gnu parallel
#     input:
#         pmc_medline = pmc_medline,
#         parallel_parse_textmining_pmc_medline = parallel_parse_textmining_pmc_medline
#     output:
#         Functions_table_PMID_temp = Functions_table_PMID_temp,
#         temp_dir = temp_dir
#     threads: NUMBER_OF_PROCESSES
#     shell:
#         """python -c 'import parallel_parse; parallel_parse.parallel_script(r"{input.pmc_medline}", r"{input.parallel_parse_textmining_pmc_medline}", r"{output.Functions_table_PMID_temp}", temp_dir=r"{output.temp_dir}", cpu_number={threads})'"""

# rule string_2_interpro: # example of various styles of calling python function/script
#     input: # relative path to working dir
#         uniprot_2_string_v11 = uniprot_2_string_v11,
#         uniprot_2_interpro = uniprot_2_interpro
#     output: # relative path to working dir
#         string_2_interpro = string_2_interpro
#     #script: # relative path to Snakefile
#     #    "python/map_string_2_interpro.py"
#     # shell:
#     #     """python -c 'import create_SQL_tables_snakemake; create_SQL_tables_snakemake.map_string_2_interpro(r"{input.uniprot_2_string_v11}", r"{input.uniprot_2_interpro}", r"{output.string_2_interpro}")'"""
#     run:
#         cst.string_2_interpro(input.uniprot_2_string_v11, input.uniprot_2_interpro, output.string_2_interpro)
##########################################################################################
##########################################################################################

### logic
# assemble all annotations into Protein_2_Function_table.txt limit to minimum number of > 1 function per protein
# --> Function_2_ENSP_table.txt
#      includes reduction step
#       - limit to relevant ENSPs
#       - limit to functions with proper descriptions and information in Functions_table_STRING.txt
#       - remove if only a single function per genome of given TaxID
# limit Functions_table_STRING.txt to relevant functions appearing in Function_2_ENSP_table_reduced.txt
# Function_2_ENSP_table_reduced.txt again serves as the basis to reduce
#   - Protein_2_Function_table.txt
#   - Protein_2_FuncEnum_table_STRING.txt
#   - Taxid_2_FunctionCountArray_table_FIN.txt
# reduce Functions_table_STRING.txt by removing varibles.blacklisted_terms --> therefore removing them from final Protein_2_Function/Enum table


# FAQ
# Why are annotations removed in Protein_2_Function_table_removed.txt ?
#  - check function in Function_2_ENSP_table.txt --> exists only once per genome
#  - check ENSP in shorthands --> maybe not in relevant ENSPs
# Why are functions removed from Functions_table_STRING.txt ?
#  - check if present at all in Protein_2_Function_table.txt


##########################################################################################
##########################################################################################
##### some stuff below
##### ToDo
# add UniProt AC and ID to Taxid_2_Proteins_table_FIN
# otherwise it gets filtered

# map PMID data from ENSP to UniProt --> Protein_2_Function_table_PMID_UP.txt --> question Damian/Christian ???


# parse proteome information as well
# DR   Proteomes; UP000008770; Genome.


### ToDo:
# - Taxid_2_Proteins_table_FIN --> Taxid_2_Proteins_table_STS for all
# - KEGG_Taxid_2_acronym_table_STRING aus KEGG dump neu erstellen --> merge with UniProt dump
# - Protein_2_FunctionEnum_and_Score_table_FIN --> map to UniProt AC and ID

# Isoforms e.g. from uniprot dump:
# "CC         IsoId=P07806-2; Sequence=VSP_018910;"
# --> add P07806-2 to secondary to primary IDs ? P07806-2 --> P07806

# This would mean that if a user provides isoform information such as "P16157-4"
### CronJobs or something similar for the automatic updates
# - WikiPathways, update on the 11th of each month
# - UniProt ???
# - Jensenlab on Monday each week
# - Reactome
# - InterPro

# 5.) ? How to count Jensenlab Scores?
# bin into 5 categories, like using a hard-cutoff, and merge results (correcting p-values * number_of_bins), duplicate terms --> select best p-value?
# bins: 0-5, 1-5, 2-5, 3-5, 4-5

# parse UniProtAN to other functional annotations apart from keywords (which are)

# ask Lars about the differences of annotation information/quality
### ToDo compare GO annotations from Lars to UniProt-retrieved

# # TODO:
# dtype warning Taxid_2_Proteins_table_UPS_FIN/mnt/mnemo5/dblyon/install/anaconda3/envs/snake/lib/python3.6/importlib/_bootstrap.py:219: RuntimeWarning: numpy.dtype size changed, may indicate binary incompatibility
#  Wikipathways extra download dir
# wiki tqdm for all don't show individual files
