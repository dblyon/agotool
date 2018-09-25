from celery import Celery
from celery import group
from collections import defaultdict
import pandas as pd
# import numpy as np
import os, sys
from fisher import pvalue
sys.path.insert(0, os.path.abspath(os.path.realpath('./python')))
import ratio, query, variables
from multiple_testing import Bonferroni, Sidak, HolmBonferroni, BenjaminiHochberg
from io import StringIO
# from lxml import etree

# app = Celery('tasks', broker='pyamqp://guest@localhost//')
# celery = Celery('tasks', backend='rpc://', broker='pyamqp://')

# broker_url = 'amqp://myuser:mypassword@localhost:5672/myvhost'
broker_url = 'amqp://agotool:lightspeed@localhost:5672/agotool'
# amqp://agotool:**@localhost:5672/agotool
result_backend = 'rpc://'
# broker_url = 'amqp://agotool:lightspeed@localhost:5672/agotool'
# app = Celery('tasks', backend='rpc://', broker='pyamqp://')
celery = Celery("tasks", backend=result_backend, broker=broker_url)
def make_celery_v2():
    return Celery("tasks", backend=result_backend, broker=broker_url)
### setting up rabbitmq on Atlas
## http://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html#broker-rabbitmq
# sudo rabbitmqctl add_user agotool lightspeed
# sudo rabbitmqctl add_vhost agotool
# sudo rabbitmqctl set_user_tags agotool agotool
# sudo rabbitmqctl set_permissions -p agotool agotool ".*" ".*" ".*"

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

@celery.task()
def add_together(a, b):
    return a + b

# @celery.task(name="tasks.run_enrichment_genome")
def run_enrichment_genome(protein_ans_list, taxid, background_n, FDR_cutoff):
    df_list = []
    args_dict = {}
    etype_2_association_2_count_dict_background = query.from_taxid_get_association_2_count_split_by_entity(taxid)
    # for entity_type in variables.entity_types_with_data_in_functions_table:
    #     association_2_count_dict_background = etype_2_association_2_count_dict_background[entity_type]
    #     result_df, args_dict_temp = enrichmentstudy_genome.delay(protein_ans_list, entity_type, association_2_count_dict_background, background_n, FDR_cutoff).get()

    jobs = group(enrichmentstudy_genome.s(protein_ans_list, entity_type, etype_2_association_2_count_dict_background[entity_type], background_n, FDR_cutoff) for entity_type in variables.entity_types_with_data_in_functions_table)
    result = jobs.apply_async()
    for result_df_args_dict in result.join():
        result_df, args_dict_temp = result_df_args_dict

        args_dict.update(args_dict_temp)
        result_df = pd.read_csv(StringIO(result_df), sep='\t')
        if result_df is None:
            return None, args_dict
        if not result_df.empty:
            # result_df["etype"] = entity_type
            # result_df["category"] = variables.entityType_2_functionType_dict[entity_type]
            df_list.append(result_df)
    try:
        df = pd.concat(df_list)
    except ValueError:  # empty list
        args_dict["ERROR_Empty_Results"] = "Unfortunately no results to display or download. This could be due to e.g. FDR_threshold being set too stringent, identifiers not being present in our system or not having any functional annotations, as well as others. Please check your input and try again."
        return None, args_dict
    return df.to_csv(header=True, index=False, sep="\t"), args_dict

@celery.task(name="tasks.enrichmentstudy_genome")
def enrichmentstudy_genome(protein_ans_list, entity_type, association_2_count_dict_background, background_n,
        FDR_cutoff=None):
    assoc_dict = query.get_association_dict_from_etype_and_proteins_list(protein_ans_list, entity_type)
    association_2_count_dict_foreground, association_2_ANs_dict_foreground, foreground_n = count_terms_v3(protein_ans_list, assoc_dict)
    fisher_dict, args_dict = {}, {}
    term_list, description_list, p_value_list, foreground_ids_list, foreground_count_list = [], [], [], [], []
    for association, foreground_count in association_2_count_dict_foreground.items():
        try:
            background_count = association_2_count_dict_background[association]
        except KeyError:
            args_dict["ERROR_association_2_count"] = "ERROR retrieving counts for association {} please contact david.lyon@uzh.ch with this error message".format(association)
            return None, args_dict
        a = foreground_count # number of proteins associated with given GO-term
        b = foreground_n - foreground_count # number of proteins not associated with GO-term
        c = background_count
        d = background_n - background_count
        if d < 0:
            d = 0
        try:
            p_val_uncorrected = fisher_dict[(a, b, c, d)]
        except KeyError:
            p_val_uncorrected = pvalue(a, b, c, d).right_tail
            fisher_dict[(a, b, c, d)] = p_val_uncorrected
        term_list.append(association)
        p_value_list.append(p_val_uncorrected)
        foreground_ids_list.append(';'.join(association_2_ANs_dict_foreground[association]))
        foreground_count_list.append(foreground_count)
    df = pd.DataFrame({"term": term_list,
                      "p_value": p_value_list,
                      "foreground_ids": foreground_ids_list,
                      "foreground_count": foreground_count_list})
    df["FDR"] = BenjaminiHochberg(df["p_value"].values, df.shape[0], array=True)
    df["etype"] = entity_type
    # df["category"] = variables.entityType_2_functionType_dict[entity_type]
    if FDR_cutoff is not None:
        df = df[df["FDR"] <= FDR_cutoff]
    return df.to_csv(header=True, index=False, sep="\t"), args_dict

def count_terms_v3(ans_set, assoc_dict):
    association_2_ANs_dict = {}
    association_2_count_dict = defaultdict(int)
    for an in (AN for AN in ans_set if AN in assoc_dict):
        for association in assoc_dict[an]:
            association_2_count_dict[association] += 1
            if not association in association_2_ANs_dict:
                association_2_ANs_dict[association] = {an}
            else:
                association_2_ANs_dict[association] |= {an} # update dict
    return association_2_count_dict, association_2_ANs_dict, len(ans_set)


