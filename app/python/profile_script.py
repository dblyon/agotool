import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
import seaborn as sns
import os, sys, math

def rescale_scores(df, alpha=0.5, max_score=5):
    df = df.sort_values(["DOID", "Score"], ascending=[True, True])
    df = df.reset_index(drop=True)
    df["Rescaled_score_orig"] = np.nan
    df["Rescaled_score"] = np.nan
    indices_score_orig, rescaled_score_orig_list, rescaled_score_equal_ranks_list = [], [], []
    for DOID, group in df.groupby("DOID"):
        rescaled_score_group = []
        index_group = group.index
        for gene_rank, score in enumerate(group.Score, 1):         
            rescaled_score_group.append(math.pow(gene_rank, alpha) * math.pow((1 - score / max_score), (1 - alpha))) # version 2
        rescaled_score_orig_list += rescaled_score_group
        
        vals, idx_start, count = np.unique(group.Score, return_counts=True, return_index=True)
        start_stop_index_list = list(zip(idx_start, idx_start[1:])) + [(idx_start[-1], None)]
        for start_stop, num_genes in zip(start_stop_index_list, count):
            start, stop = start_stop
            if num_genes > 1:                
                rescaled_score_equal_ranks_list += [np.median(rescaled_score_group[start:stop])]*num_genes
            else:
                rescaled_score_equal_ranks_list.append(rescaled_score_group[start])
        
    df["Rescaled_score_orig"] = rescaled_score_orig_list
    df["Rescaled_score"] = rescaled_score_equal_ranks_list    
    return df

# for each functional term (per genome): sort by score in descending order, and thereby rank the ENSPs.
fn_textmining_channel = r"/mnt/mnemo5/dblyon/agotool/data/PostgreSQL/downloads/human_disease_textmining_full.tsv"
df_tm = pd.read_csv(fn_textmining_channel, sep='\t', names=["ENSP", "gene", "DOID", "description", "z_score", "Score", "url"]) # confidence_score == Score
df_tm = df_tm[["ENSP", "DOID", "Score"]]
cond_is_ENSP = df_tm["ENSP"].apply(lambda x: x.startswith("ENSP"))
cond_is_DOID = df_tm["DOID"].apply(lambda x: x.startswith("DOID:"))
df_tm = df_tm[cond_is_ENSP & cond_is_DOID]
df_tm = rescale_scores(df_tm, alpha=0.5, max_score=5)
fn_textmining_channel_rescaled = r"/mnt/mnemo5/dblyon/agotool/data/PostgreSQL/downloads/human_disease_textmining_full_rescored_benchmark_v3.tsv"
df_tm.to_csv(fn_textmining_channel_rescaled, sep='\t', header=True, index=False)

