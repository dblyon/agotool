import os, sys
import numpy as np
import pandas as pd
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
import variables, tools
import create_SQL_tables_snakemake as cst
# etype = "-58"
etype = variables.id_2_entityTypeNumber_dict["STRING_clusters"] = "-58"


# dirs
DOWNLOADS_DIR = r"/mnt/mnemo5/dblyon/agotool_PMID_autoupdate/agotool/data/PostgreSQL/downloads"
TABLES_DIR = r"/mnt/mnemo5/dblyon/agotool_PMID_autoupdate/agotool/data/PostgreSQL/tables"

# input
fn_clusters_proteins = os.path.join(DOWNLOADS_DIR, "clusters.proteins.v11.0.txt.gz")
fn_descriptions = os.path.join(DOWNLOADS_DIR, "clusters.info.v11.0.txt.gz")
fn_tree = os.path.join(DOWNLOADS_DIR, "clusters.tree.v11.0.txt.gz")

# output
fn_Protein_2_Function_table_STRING_clusters = os.path.join(TABLES_DIR, "Protein_2_Function_table_STRING_clusters.txt")
fn_Functions_table_STRING_clusters = os.path.join(TABLES_DIR, "Functions_table_STRING_clusters.txt")



def Protein_2_Function_table_STRING_clusters(fn_clusters_proteins):
    protein_2_functionSet_dict = defaultdict(lambda: set())
    gen = tools.yield_line_uncompressed_or_gz_file(fn_clusters_proteins)
    _ = next(gen) # skip header: '#ncbi_taxid\tcluster_id\tprotein_id\n'
    for line in gen:
        ncbi_taxid, cluster_id, protein_id = line.split()
        cluster_id = ncbi_taxid + "_" + cluster_id
        protein_id = protein_id.strip()
        protein_2_functionSet_dict[protein_id].update({cluster_id})
    return protein_2_functionSet_dict

def get_cluster_id_set_max200(fn_descriptions): #, fn_Functions_table_STRING_clusters, term_2_level_dict):
    cluster_id_set_max200 = set()
    gen = tools.yield_line_uncompressed_or_gz_file(fn_descriptions)
    _ = next(gen) # skip header: #ncbi_taxid     cluster_id      cluster_size    best_described_by
    with open(fn_Functions_table_STRING_clusters, "w") as fh_out:
        for line in gen:
            ncbi_taxid, cluster_id, cluster_size, best_described_by = line.split("\t")
            if int(cluster_size) > 200:
                continue # exclude large clusters
            cluster_id = ncbi_taxid + "_" + cluster_id
            cluster_id_set_max200 |= {cluster_id}
    return cluster_id_set_max200 #, terms_without_hierarchy

def get_child_2_parent_dict_STRING_clusters(fn_tree):
    child_2_parent_dict = {}  # direct parents
    # ncbi_taxid     child_cluster_id        parent_cluster_id
    gen = tools.yield_line_uncompressed_or_gz_file(fn_tree)
    _ = next(gen)
    for line in gen:
        ncbi_taxid, child_cluster_id, parent_cluster_id = line.split()
        child = ncbi_taxid + "_" + child_cluster_id
        parent = ncbi_taxid + "_" + parent_cluster_id
        if child not in child_2_parent_dict:
            child_2_parent_dict[child] = {parent}
        else:
            child_2_parent_dict[child] |= {parent}
    return child_2_parent_dict


protein_2_functionSet_dict = Protein_2_Function_table_STRING_clusters(fn_clusters_proteins)
cluster_id_set_max200 = get_cluster_id_set_max200(fn_descriptions)

child_2_parent_dict = get_child_2_parent_dict_STRING_clusters(fn_tree)
term_2_level_dict = cst.get_term_2_level_dict(child_2_parent_dict)
# child_2_parent_dict_STRING_clusters = child_2_parent_dict


cluster_id_set_ocurring = set()
with open(fn_Protein_2_Function_table_STRING_clusters, "w") as fh_out:
    for protein_id in sorted(protein_2_functionSet_dict):
        functionSet = protein_2_functionSet_dict[protein_id]
        functionSet = functionSet.intersection(cluster_id_set_max200) # filter for clusters of size > 200
        if len(functionSet) > 1:
            cluster_id_set_ocurring |= functionSet
            fh_out.write(protein_id + "\t" + cst.format_list_of_string_2_postgres_array(functionSet) + "\t" + etype + "\n")

year = "-1"
etype = str(etype)
gen = tools.yield_line_uncompressed_or_gz_file(fn_descriptions)
_ = next(gen) # skip header: # ncbi_taxid     cluster_id      cluster_size    best_described_by
# terms_without_hierarchy = []
with open(fn_Functions_table_STRING_clusters, "w") as fh_out:
    for line in gen:
        ncbi_taxid, cluster_id, cluster_size, best_described_by = line.split("\t")
        if int(cluster_size) > 200:
            continue # exclude large clusters
        cluster_id = ncbi_taxid + "_" + cluster_id
        if cluster_id not in cluster_id_set_ocurring:
            continue
        best_described_by = best_described_by.strip()
        try:
            level = term_2_level_dict[cluster_id]
        except KeyError:
            level = "-1"
            # terms_without_hierarchy.append(cluster_id) # checked and written to file when creating Lineage_table
        fh_out.write(etype + "\t" + cluster_id + "\t" + best_described_by + "\t" + year +"\t" + str(level) + "\n")


