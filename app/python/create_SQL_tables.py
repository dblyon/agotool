import os, json, sys, re, fnmatch, subprocess, time, datetime #, shlex  #, multiprocessing
import pandas as pd
from subprocess import call
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
import ast

import tools, obo_parser, variables, query, ratio
from obo_parser import OBOReader_2_text


TYPEDEF_TAG, TERM_TAG = "[Typedef]", "[Term]"
BASH_LOCATION = r"/usr/bin/env bash"
PYTHON_DIR = variables.PYTHON_DIR
LOG_DIRECTORY = variables.LOG_DIRECTORY
POSTGRESQL_DIR = variables.POSTGRESQL_DIR
DOWNLOADS_DIR = variables.DOWNLOADS_DIR
STATIC_DIR = variables.STATIC_POSTGRES_DIR
TABLES_DIR = variables.TABLES_DIR
TEST_DIR = variables.TEST_DIR
FILES_NOT_2_DELETE = variables.FILES_NOT_2_DELETE
NUMBER_OF_PROCESSES = variables.NUMBER_OF_PROCESSES
VERSION_ = variables.VERSION_
PLATFORM = sys.platform


EMPTY_EGGNOG_JSON_DICT = {"KEGG": {"kegg_pathways": [], "kegg_header": ["Pathway", "SeqCount", "Frequency", "relative_fontsize"]}, "go_terms": {"go_terms": {}, "go_header": ["ID", "GO term", "Evidence", "SeqCount", "Frequency", "relative_fontsize"]}, "domains": {"domains": {}, "dom_header": ["Domain ID", "SeqCount", "Frequency", "relative_fontsize"]}}
id_2_entityTypeNumber_dict = {'GO:0003674': "-23",  # 'Molecular Function',
                              'GO:0005575': "-22",  # 'Cellular Component',
                              'GO:0008150': "-21",  # 'Biological Process',
                              "GO:OBSOLETE": "-24", # "GO obsolete
                              'UPK:9990': "-51",  # 'Technical term',
                              'UPK:9991': "-51",  # 'PTM',
                              'UPK:9992': "-51",  # 'Molecular function',
                              'UPK:9993': "-51",  # 'Ligand',
                              'UPK:9994': "-51",  # 'Domain',
                              'UPK:9995': "-51",  # 'Disease',
                              'UPK:9996': "-51",  # 'Developmental stage',
                              'UPK:9997': "-51",  # 'Coding sequence diversity',
                              'UPK:9998': "-51",  # 'Cellular component',
                              'UPK:9999': "-51",  # 'Biological process'
                              "UniProtKeywords": "-51",
                              'KEGG': "-52", # KEGG
                              "SMART": "-53", # SMART domains
                              "INTERPRO": "-54", # Interpro domains
                              "PFAM": "-55", # Pfam domains
                              "PMID": "-56"} # Pubmed identifiers

id_2_entityTypeNumber_dict_keys_set = set(id_2_entityTypeNumber_dict.keys())


def run_create_tables_for_PostgreSQL(debug=False, testing=False, verbose=True, version_="STRING"):
    if version_ == "STRING":
        run_create_tables_for_PostgreSQL_STRING(debug=debug, testing=testing, verbose=verbose)
    elif version_ == "aGOtool":
        run_create_tables_for_PostgreSQL_aGOtool(debug=debug, testing=testing, verbose=verbose)
    else:
        print("version: ", version_, " unknown")
        raise NotImplementedError

def run_create_tables_for_PostgreSQL_aGOtool(debug=False, testing=False, verbose=True):
    if debug:
        start_time = time.time()
        # remove_files(find_tables_to_remove())
        # print(find_tables_to_remove())
        ### PostgreSQL DB creation, copy from file and indexing
        create_test_tables(50000, TABLES_DIR, version_="aGOtool")
        fn_create_DB_copy_and_index_tables = create_psql_script_copy_from_file_and_index(testing=testing)
        print("PostgreSQL DB creation, copy from file, and indexing")
        call_script(BASH_LOCATION, fn_create_DB_copy_and_index_tables)
        tools.print_runtime(start_time)
    else:
        start_time = time.time()
        print("#"*80)
        print("Parsing downloaded content and writing tables for PostgreSQL import")
        create_tables(verbose=verbose)
        create_test_tables(50000, TABLES_DIR, version_="aGOtool")
        remove_files(find_tables_to_remove())

        ### PostgreSQL table file creation, (copy from file and indexing run from .psql script)
        print("PostgreSQL flat files created, ready to read from file and index")
        print("#" * 80)
        tools.print_runtime(start_time)

def run_create_tables_for_PostgreSQL_STRING(debug=False, testing=False, verbose=True, delete_temp_files=False):
    if debug:
        start_time = time.time()
        ### PostgreSQL DB creation, copy from file and indexing
        create_test_tables(50000, TABLES_DIR, version_="STRING")
        fn_create_DB_copy_and_index_tables = create_psql_script_copy_from_file_and_index(testing=testing)
        print("PostgreSQL DB creation, copy from file, and indexing")
        call_script(BASH_LOCATION, fn_create_DB_copy_and_index_tables)
        tools.print_runtime(start_time)
    else:
        start_time = time.time()
        print("#"*80)
        print("Parsing downloaded content and writing tables for PostgreSQL import")
        create_tables_STRING(verbose=verbose, delete_temp_files=delete_temp_files)
        create_test_tables(50000, TABLES_DIR, version_="STRING")
        if delete_temp_files:
            remove_files(find_tables_to_remove())

        ### PostgreSQL table file creation, (copy from file and indexing run from .psql script)
        print("PostgreSQL flat files created, ready to read from file and index")
        print("#" * 80)
        tools.print_runtime(start_time)

def create_tables(verbose=False):
    """
    :return: None
    """
    ### - OGs
    ### - OG_2_Function
    ### STATIC FILE simply provide the finished table
    ### create_OGs_table_and_OG_2_Function_table_and_Functions_table_DOM()

    ### - Functions
    # create_Child_2_Parent_table_GO__and__Functions_table_GO__and__Function_2_definition_GO()
    # create_Child_2_Parent_table_UPK__and__Functions_table_UPK__and__Function_2_definition_UPK()
    ### create_Functions_table_KEGG() # STATIC FILE simply provide the finished table
    # fn_list = [os.path.join(TABLES_DIR, fn) for fn in ["Functions_table_GO.txt", "Functions_table_UPK.txt"]]
    # fn_list += [os.path.join(STATIC_DIR, fn) for fn in ["Functions_table_KEGG_static.txt", "Functions_table_DOM_static.txt"]]
    # fn_out = os.path.join(TABLES_DIR, "Functions_table.txt")
    ### dependency on create_OGs_table_and_OG_2_Function_table_and_Functions_table_KEGG_DOM
    # concatenate_files(fn_list, fn_out)

    ### - Function_2_definition (obsolete, since definitions added to Functions_table as a column)
    #fn_list = [os.path.join(TABLES_DIR, fn) for fn in ["Function_2_definition_table_UPK.txt", "Function_2_definition_table_GO.txt"]]
    #fn_out = os.path.join(TABLES_DIR, "Function_2_definition_table.txt")
    #concatenate_files(fn_list, fn_out)


    ## - Ontologies (Child_2_Parent)
    # fn_list = [os.path.join(TABLES_DIR, fn) for fn in ["Child_2_Parent_table_GO.txt", "Child_2_Parent_table_UPK.txt"]]
    # fn_out = os.path.join(TABLES_DIR, "Ontologies_table.txt")
    # create_Ontologies_table(fn_list, fn_out)

    ### - Protein_2_OG
    ### STATIC FILE simply provide the finished table
    ### create_Protein_2_OG_table()

    ### - Protein_2_Function (updated, dependency on Ontologies since, only functions that are present in ontology should be assigned)
    # create_Protein_2_Function_table_wide_format(verbose=verbose)
    # create_Protein_Secondary_2_Primary_AN()

    ### - GO_2_Slim
    # create_GO_2_Slim_table()
    if verbose:
        print("#"*80, "\n", "### finished creating all tables")


    ### - Entity_types_table.txt
    # static table, edit manually

def create_tables_STRING(verbose=True, delete_temp_files=False, clear_log_files=False, number_of_processes=1):
     if NUMBER_OF_PROCESSES > 8:
         number_of_processes = 8

     # log_fn_list = [os.path.join(LOG_DIRECTORY, fn) for fn in os.listdir(LOG_DIRECTORY) if fn.startswith("create_SQL_tables_")]
     # if clear_log_files:
     #     for fn in log_fn_list:
     #         print("removing/clearing for new input {}".format(fn))
     #         os.remove(fn)
     # else:
     #     for fn in log_fn_list:
     #         with open(fn, "a+") as fh:
     #             fh.write("\n{}\n{}\n".format("######\n# Current Date and Time", datetime.datetime.now().isoformat()))
     #
     # GO_dag = obo_parser.GODag(obo_file=os.path.join(DOWNLOADS_DIR, "go-basic.obo"), upk=False)
     # UPK_dag = obo_parser.GODag(obo_file=os.path.join(DOWNLOADS_DIR, "keywords-all.obo"), upk=True)
     #
     # ### - Ontologies (Child_2_Parent)
     # create_Child_2_Parent_table_UPK__and__Functions_table_UPK__and__Function_2_definition_UPK()
     # create_Child_2_Parent_table_GO__and__Functions_table_GO__and__Function_2_definition_GO()
     # fn_list = [os.path.join(TABLES_DIR, fn) for fn in ["Child_2_Parent_table_GO.txt", "Child_2_Parent_table_UPK.txt"]]
     # fn_out = os.path.join(TABLES_DIR, "Ontologies_table_STRING.txt")
     # create_Ontologies_table(fn_list, fn_out)
     #
     # ### - GO_2_Slim_table
     # create_GO_2_Slim_table(fn_out=os.path.join(TABLES_DIR, "GO_2_Slim_table_STRING.txt"))

     # ### - Functions_table
     # create_Functions_table_KEGG(fn_in=os.path.join(DOWNLOADS_DIR, "pathway.list"), fn_out=os.path.join(TABLES_DIR, "Functions_table_KEGG.txt"))
     # create_Functions_table_SMART(fn_in=os.path.join(DOWNLOADS_DIR, "SMART_domain_descriptions.txt"), fn_out=os.path.join(TABLES_DIR, "Functions_table_SMART.txt"))
     # create_Functions_table_PFAM(fn_in=os.path.join(DOWNLOADS_DIR, "Pfam-A.clans.tsv"), fn_out=os.path.join(TABLES_DIR, "Functions_table_PFAM.txt"))
     # create_Functions_table_InterPro(fn_in=os.path.join(DOWNLOADS_DIR, "InterPro_name_2_AN.txt"), fn_out=os.path.join(TABLES_DIR, "Functions_table_InterPro.txt"))
     # fn_list = [os.path.join(TABLES_DIR, fn) for fn in ["Functions_table_GO.txt", "Functions_table_UPK.txt",
     #                                                    "Functions_table_KEGG.txt", "Functions_table_SMART.txt",
     #                                                    "Functions_table_PFAM.txt", "Functions_table_InterPro.txt"]]
     # fn_out = os.path.join(TABLES_DIR, "Functions_table_STRING.txt")
     # print("creating {} by concatenation and sorting".format(fn_out))
     # concatenate_files(fn_list, fn_out)
     # sort_file(fn_out, fn_out, columns="1", number_of_processes=number_of_processes)

     # ##### - Protein_2_Function_table
     # ### - Protein_2_Function_table_Interpro no map_Name_2_AN necessary since AN not names provided, but check that all ANs are also present in Functions_table_InterPro.txt
     # create_Protein_2_Function_table_InterPro(fn_in=os.path.join(DOWNLOADS_DIR, "string2interpro.dat.gz"),
     #     fn_in_temp=os.path.join(DOWNLOADS_DIR, "string2interpro.dat" + "_temp"),
     #     fn_out=os.path.join(TABLES_DIR, "Protein_2_Function_table_InterPro.txt"),
     #     fn_superset=os.path.join(TABLES_DIR, "Functions_table_InterPro.txt"),
     #     number_of_processes=number_of_processes, verbose=verbose)

     ### - Protein_2_Function_table_PFAM
     ### - Protein_2_Function_table_SMART
     # fn_out_SMART_temp = os.path.join(TABLES_DIR, "Protein_2_Function_table_SMART_temp.txt")
     # fn_out_SMART = os.path.join(TABLES_DIR, "Protein_2_Function_table_SMART.txt")
     # fn_out_PFAM_temp = os.path.join(TABLES_DIR, "Protein_2_Function_table_PFAM_temp.txt")
     # fn_out_PFAM = os.path.join(TABLES_DIR, "Protein_2_Function_table_PFAM.txt")
     # create_Protein_2_Function_table_SMART_and_PFAM(fn_in=os.path.join(DOWNLOADS_DIR, "string11_dom_prot_full.clean.sql"),
     #     fn_in_temp=os.path.join(DOWNLOADS_DIR, "string11_dom_prot_full.clean.sql" + "_temp"),
     #     fn_out_SMART_temp=fn_out_SMART_temp, fn_out_PFAM_temp=fn_out_PFAM_temp,
     #     number_of_processes=number_of_processes, verbose=verbose)
     # map_Name_2_AN(fn_in=fn_out_SMART_temp, fn_out=fn_out_SMART, fn_dict=os.path.join(TABLES_DIR, "Functions_table_SMART.txt"),
     #     fn_no_mapping=os.path.join(TABLES_DIR, "Functions_table_SMART_no_mapping.txt"))
     # map_Name_2_AN(fn_in=fn_out_PFAM_temp, fn_out=fn_out_PFAM, fn_dict=os.path.join(TABLES_DIR, "Functions_table_PFAM.txt"),
     #     fn_no_mapping=os.path.join(TABLES_DIR, "Functions_table_PFAM_no_mapping.txt"))

     # ### - Protein_2_Function_table_GO
     # fn_in = os.path.join(DOWNLOADS_DIR, "knowledge.tsv.gz") # version10="string_go.tsv.gz" new_version="knowledge.tsv.gz"
     # fn_in_temp = fn_in + "_temp"
     # fn_out = os.path.join(TABLES_DIR, "Protein_2_Function_table_GO.txt")
     # create_Protein_2_Function_table_GO(GO_dag, fn_in, fn_in_temp, fn_out, number_of_processes=number_of_processes, verbose=verbose)

     # ### - Protein_2_Function_table_UniProtKeyword
     # fn_in_uniprot_SwissProt_dat = os.path.join(DOWNLOADS_DIR, "uniprot_sprot.dat.gz")
     # fn_in_uniprot_TrEMBL_dat = os.path.join(DOWNLOADS_DIR, "uniprot_trembl.dat.gz")
     # fn_in_uniprot_2_string = os.path.join(DOWNLOADS_DIR, "full_uniprot_2_string.jan_2018.clean.tsv")
     # fn_out = os.path.join(TABLES_DIR, "Protein_2_Function_table_UniProtKeyword.txt")
     # UPK_Name_2_AN_dict = get_keyword_2_upkan_dict() # depends on create_Child_2_Parent_table_UPK__and__Functions_table_UPK__and__Function_2_definition_UPK
     # create_Protein_2_Function_table_UniProtKeyword(UPK_Name_2_AN_dict, UPK_dag, fn_in_uniprot_SwissProt_dat, fn_in_uniprot_TrEMBL_dat,
     #        fn_in_uniprot_2_string, fn_out, number_of_processes=number_of_processes, verbose=verbose)
     #
     # ### - Protein_2_Function_table_KEGG
     # fn_in = os.path.join(DOWNLOADS_DIR, "kegg_benchmarking.CONN_maps_in.v11.nothing_blacklisted.tsv")
     # fn_out_temp = os.path.join(TABLES_DIR, "Protein_2_Function_table_KEGG_temp.txt")
     # fn_out = os.path.join(TABLES_DIR, "Protein_2_Function_table_KEGG.txt")
     # create_Protein_2_Function_table_KEGG_STRING(fn_in=fn_in, fn_out_temp=fn_out_temp, fn_out=fn_out, number_of_processes=number_of_processes, verbose=verbose)
     # fn_list = [os.path.join(TABLES_DIR, fn) for fn in
     #            ["Protein_2_Function_table_GO.txt",
     #             "Protein_2_Function_table_UniProtKeyword.txt",
     #             "Protein_2_Function_table_KEGG.txt",
     #             "Protein_2_Function_table_InterPro.txt",
     #             "Protein_2_Function_table_PFAM.txt",
     #             "Protein_2_Function_table_SMART.txt"]]
     # fn_out = os.path.join(TABLES_DIR, "Protein_2_Function_table_STRING.txt")
     # concatenate_files(fn_list, fn_out)
     # sort_file(fn_out, fn_out, columns="1,3", fn_bash_script=None, number_of_processes=number_of_processes, verbose=True)

     # ### - TaxID_2_Proteins_table
     # fn_in = os.path.join(DOWNLOADS_DIR, "protein.shorthands.txt")
     # fn_out_temp = os.path.join(DOWNLOADS_DIR, "protein.shorthands.txt_sorted_temp.txt")
     # fn_out = os.path.join(TABLES_DIR, "TaxID_2_Proteins_table_STRING.txt")
     # create_TaxID_2_Proteins_table(fn_in, fn_out_temp, fn_out, number_of_processes=number_of_processes, verbose=verbose)

     ### - Functions_2_ENSP_table
     #### dependency on creating DB first #!!!
     fn_out = os.path.join(TABLES_DIR, "Function_2_ENSP_table_STRING.txt")
     pqo = query.PersistentQueryObject_STRING()
     create_functions_2_ENSP_table(pqo, fn_out, number_of_processes=number_of_processes, verbose=verbose)

     # if verbose:
     #     print("#"*80 + "\n##### " + "finished creating all tables")
     # if delete_temp_files:
     #     remove_files(find_tables_to_remove() + tables_to_remove_temp)
     #     print("#" * 80, "removing temp files and temp_tables")

def sort_file(fn_in, fn_out, columns="1", fn_bash_script=None, number_of_processes=1, verbose=True):
    if verbose:
        print("#sorting file\nfn_in:\n{}\nfn_out:\n{}".format(fn_in, fn_out))
    if fn_bash_script is None:
        fn_bash_script = "bash_script_sort_{}.sh".format(os.path.basename(fn_in))
    with open(fn_bash_script, "w") as fh:
        fh.write("#!/usr/bin/env bash\n")
        if PLATFORM == "linux":
            shellcmd = "sort --parallel {} -k {} {} -o {}".format(number_of_processes, columns, fn_in, fn_out)
        else:
            shellcmd = "LC_ALL=C gsort --parallel {} -k {} {} -o {}".format(number_of_processes, columns, fn_in, fn_out)
        fh.write(shellcmd)
    if verbose:
        print(shellcmd)
    subprocess.call("chmod 744 ./{}".format(fn_bash_script), shell=True)
    subprocess.call("./{}".format(fn_bash_script), shell=True)
    os.remove(fn_bash_script)

def gunzip_file(fn_in, fn_out=None):
    fn_bash_script = "bash_script_sort_{}.sh".format(os.path.basename(fn_in))
    with open(fn_bash_script, "w") as fh:
        fh.write("#!/usr/bin/env bash\n")
        if fn_out is None:
            fn_out = fn_in + "_temp"
        shellcmd_1 = "gunzip -c {} > {}".format(fn_in, fn_out)
        fh.write(shellcmd_1 + "\n")
    subprocess.call("chmod 744 ./{}".format(fn_bash_script), shell=True)
    subprocess.call("./{}".format(fn_bash_script), shell=True)
    os.remove(fn_bash_script)

def create_functions_2_ENSP_table(pqo, fn_out, number_of_processes=1, verbose=True):
    if verbose:
        print("creating functions_2_ENSP_table this will take a while")
    taxid_list = query.get_taxids()
    with open(fn_out, "w") as fh_out:
        for taxid in sorted(taxid_list):
            ans_list = sorted(query.get_proteins_of_taxid(taxid))
            etype_2_association_dict = pqo.get_association_dict_split_by_category(ans_list)
            for etype in sorted(variables.entity_types_with_data_in_functions_table):
                assoc_dict = etype_2_association_dict[etype]
                association_2_count_dict, association_2_ANs_dict, ans_counter = ratio.count_terms_manager(set(ans_list), assoc_dict)
                # ans_counter --> number of AccessionNumbers with any association = background_n
                # association_2_count_dict --> number of associations per given Association” = background_count
                for association, ans in association_2_ANs_dict.items():
                    assert ans_counter >= association_2_count_dict[association]
                    fh_out.write(str(taxid) + "\t" + str(etype) + "\t" + association + "\t" + str(association_2_count_dict[association]) + "\t" + str(ans_counter) + "\t" + format_list_of_string_2_postgres_array(ans) + "\n")
    sort_file(fn_out, fn_out, columns="1,2", number_of_processes=number_of_processes, verbose=verbose)
    if verbose:
        print("finished creating functions_2_ENSP_table")

def format_list_of_string_2_postgres_array(list_of_string):
    """
    removes internal spaces
    :param list_of_string: List of String
    :return: String
    """
    return "{" + str(list_of_string)[1:-1].replace(" ", "").replace("'", '"') + "}"

def create_TaxID_2_Proteins_table(fn_in, fn_out_temp, fn_out, number_of_processes=1, verbose=True):
    sort_file(fn_in, fn_out_temp, columns="1", fn_bash_script="bash_script_sort_Proteomes_input_table_temp.sh", number_of_processes=number_of_processes, verbose=verbose)
    # # sort by first column
    # bash_script_temp_fn = "bash_script_sort_Proteomes_input_table_temp.sh"
    # with open(bash_script_temp_fn, "w") as fh:
    #     fh.write("#!/usr/bin/env bash\n")
    #     if PLATFORM == "linux":
    #         shellcmd = "sort --parallel {} -k1 {} -o {}".format(number_of_processes, fn_in, fn_out_temp)
    #     else:
    #         shellcmd = "LC_ALL=C gsort --parallel {} -k1 {} -o {}".format(number_of_processes, fn_in, fn_out_temp)
    #     fh.write(shellcmd)
    # subprocess.call("chmod 744 ./{}".format(bash_script_temp_fn), shell=True)
    # subprocess.call("./{}".format(bash_script_temp_fn), shell=True)
    if verbose:
        print("Creating TaxID_2_Proteins_table.txt")
        print("Proteomes_input_table_temp.txt needs sorting, doing it now")

    if verbose:
        print("parsing Proteomes_input_table_temp.txt")
    # now parse and transform into wide format
    with open(fn_out_temp, "r") as fh_in:
        with open(fn_out, "w") as fh_out:
            ENSP_list = []
            did_first = False
            for line in fh_in:
                # 287.DR97_1012   6412
                # 287.DR97_1013   6413
                ENSP, *rest = line.strip().split()
                TaxID = ENSP[:ENSP.index(".")]
                if not did_first:
                    TaxID_previous = TaxID
                    did_first = True
                if TaxID == TaxID_previous:
                    ENSP_list.append(ENSP)
                else:
                    ENSPs_2_write = sorted(set(ENSP_list))
                    # fh_out.write(TaxID_previous + "\t" + "{" + str(ENSPs_2_write)[1:-1].replace(" ", "").replace("'", '"') + "}\t" + str(len(ENSPs_2_write)) + "\n")
                    fh_out.write(TaxID_previous + "\t" + format_list_of_string_2_postgres_array(ENSPs_2_write) + "\t" + str(len(ENSPs_2_write)) + "\n")
                    ENSP_list = [ENSP]
                    TaxID_previous = TaxID
            ENSPs_2_write = sorted(set(ENSP_list))
            fh_out.write(TaxID_previous + "\t" + format_list_of_string_2_postgres_array(ENSPs_2_write) + "\t" + str(len(ENSPs_2_write)) + "\n")

def create_Protein_2_Function_table_InterPro(fn_in, fn_in_temp, fn_out, fn_superset, number_of_processes=1, verbose=True):
    """
    :param fn_in: String (e.g. /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/downloads/string2interpro.dat.gz)
    :param fn_in_temp: String (Temp file to be deleted later e.g. /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/downloads/string2interpro.dat.gz_temp)
    :param fn_out: String (e.g. /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables/Protein_2_Function_table_InterPro.txt)
    :param fn_superset: String (/home/dblyon/agotool/data/PostgreSQL/tables/Functions_table_InterPro.txt) with InterPro ANs to verify
    :param number_of_processes: Integer (number of cores, shouldn't be too high since Disks are probably the bottleneck even with SSD, e.g. max 4)
    :param verbose: Bool (flag to print infos)
    :return: None
    """
    ### sort by fn_in first column (data is most probably already sorted, but we need to be certain for the parser that follows)
    ### unzip first, then sort to enable parallel sorting
    ### is the output is NOT zipped, but the
    ### e.g. of line "1298865.H978DRAFT_0001  A0A010P2C8      IPR011990       Tetratricopeptide-like helical domain superfamily       G3DSA:1.25.40.10        182     292"
    if verbose:
        print("\ncreate_Protein_2_Function_table_InterPro")

    # bash_script_temp_fn = "bash_script_gunzip_sort_InterPro.sh"
    gunzip_file(fn_in, fn_in_temp)
    sort_file(fn_in_temp, fn_in_temp, columns="1", number_of_processes=number_of_processes, verbose=verbose)

    # with open(bash_script_temp_fn, "w") as fh:
    #     fh.write("#!/usr/bin/env bash\n")
    #     shellcmd_1 = "gunzip -c {} > {}".format(fn_in, fn_in_temp)
    #     fh.write(shellcmd_1 + "\n")
    #     if PLATFORM == "linux":
    #         # this should be simpler but it works for and there were issues with the other versions (calling the shellcmds via subprocess.call or subprocess.Popen)
    #         # no error with first version but empty file produced, probably due to ">" not "-o"
    #         # shellcmd = "sort --parallel {} -k1 <(gunzip -c {}) > {}".format(number_of_processes, fn_in, fn_in_temp)
    #         shellcmd_2 = "sort --parallel {} -k1 {} -o {}".format(number_of_processes, fn_in_temp, fn_in_temp)
    #     else:
    #         # shellcmd_2 = "LC_ALL=C gsort --parallel {} -k1 <(gunzip -c {}) > {}".format(number_of_processes, fn_in, fn_in_temp)
    #         shellcmd_2 = "LC_ALL=C gsort --parallel {} -k1 {} -o {}".format(number_of_processes, fn_in_temp, fn_in_temp)
    #     fh.write(shellcmd_2)
    # if verbose:
    #     print("gunzip and sorting string2interpro.dat.gz")
    # subprocess.call("chmod 744 ./{}".format(bash_script_temp_fn), shell=True)
    # subprocess.call("./{}".format(bash_script_temp_fn), shell=True)

    df = pd.read_csv(fn_superset, sep='\t', names=["etype", "name", "AN", "description"])
    InterPro_AN_superset = set(df["AN"].values.tolist())
    if verbose:
        print("parsing previous result to produce Protein_2_Function_table_InterPro.txt")
    entityType_InterPro = id_2_entityTypeNumber_dict["INTERPRO"]
    with open(fn_out, "w") as fh_out:
        for ENSP, InterProID_list in parse_string2interpro_yield_entry(fn_in_temp):
            # ('1298865.H978DRAFT_0001', ['IPR011990', 'IPR011990', 'IPR011990', 'IPR013026', 'IPR019734', 'IPR019734', 'IPR019734', 'IPR019734', 'IPR019734', 'IPR019734', 'IPR019734', 'IPR019734', 'IPR019734', 'IPR019734'])
            # InterProID_list = sorted(set(InterProID_list))
            InterProID_list = sorted({id_ for id_ in InterProID_list if id_ in InterPro_AN_superset})
            if len(InterProID_list) >= 1:
                fh_out.write(ENSP + "\t" + "{" + str(InterProID_list)[1:-1].replace(" ", "").replace("'", '"') + "}\t" + entityType_InterPro + "\n")
    if verbose:
        print("done create_Protein_2_Function_table_InterPro\n")

def create_Protein_2_Function_table_SMART_and_PFAM(fn_in, fn_in_temp, fn_out_SMART_temp, fn_out_PFAM_temp, number_of_processes=1, verbose=True):
    """
    :param fn_in: String (e.g. /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/downloads/string11_dom_prot_full.sql)
    :param fn_in_temp: String (Temp file to be deleted later e.g. /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/downloads/string11_dom_prot_full.sql_temp)
    :param fn_out_SMART_temp: String (e.g. /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables/Protein_2_Function_table_SMART.txt)
    :param fn_out_PFAM_temp: String (e.g. /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables/Protein_2_Function_table_PFAM.txt)
    :param number_of_processes: Integer (number of cores, shouldn't be too high since Disks are probably the bottleneck even with SSD, e.g. max 8 !?)
    :param verbose: Bool (flag to print infos)
    :return: None
    """
    if verbose:
        print("\ncreate_Protein_2_Functions_table_SMART and PFAM")

    # sort_file(fn_in, fn_in_temp, columns="2,1", number_of_processes=number_of_processes)
    # bash_script_temp_fn = "bash_script_sort_SMART.sh"
    # with open(bash_script_temp_fn, "w") as fh:
    #     fh.write("#!/usr/bin/env bash\n")
    #     if PLATFORM == "linux":
    #         shellcmd_2 = "sort --parallel {} -k2,1 {} -o {}".format(number_of_processes, fn_in, fn_in_temp)
    #     else:
    #         shellcmd_2 = "LC_ALL=C gsort --parallel {} -k2,1 {} -o {}".format(number_of_processes, fn_in, fn_in_temp)
    #     fh.write(shellcmd_2)
    # if verbose:
    #     print("sorting {}".format(fn_in))
    # subprocess.call("chmod 744 ./{}".format(bash_script_temp_fn), shell=True)
    # subprocess.call("./{}".format(bash_script_temp_fn), shell=True)

    if verbose:
        print("parsing previous result to produce create_Protein_2_Function_table_SMART.txt and Protein_2_Function_table_PFAM.txt")
    entityType_SMART = id_2_entityTypeNumber_dict["SMART"]
    entityType_PFAM = id_2_entityTypeNumber_dict["PFAM"]
    with open(fn_out_PFAM_temp, "w") as fh_out_PFAM:
        with open(fn_out_SMART_temp, "w") as fh_out_SMART:
            for ENSP, PFAM_list_SMART_list in parse_string11_dom_prot_full_yield_entry(fn_in_temp):
                PFAM_list, SMART_list = PFAM_list_SMART_list
                if len(PFAM_list) >= 1:
                    fh_out_PFAM.write(ENSP + "\t" + "{" + str(PFAM_list)[1:-1].replace(" ", "").replace("'", '"') + "}\t" + entityType_PFAM + "\n")
                if len(SMART_list) >= 1:
                    fh_out_SMART.write(ENSP + "\t" + "{" + str(SMART_list)[1:-1].replace(" ", "").replace("'", '"') + "}\t" + entityType_SMART + "\n")
    if verbose:
        print("done create_Protein_2_Function_table_SMART\n")

def map_Name_2_AN(fn_in, fn_out, fn_dict, fn_no_mapping):
    """
    SMART and PFAM Protein_2_Function_table(s) contain names from parsing the
    orig source, convert names to accessions
    :param fn_in: String (Protein_2_Function_table_temp_SMART.txt)
    :param fn_out: String (Protein_2_Function_table_SMART.txt)
    :param fn_dict: String (Functions_table_SMART.txt
    :param fn_no_mapping: String (missing mapping)
    :return: NONE
    """
    df = pd.read_csv(fn_dict, sep="\t", names=["etype", "name", "an", "definition"])
    name_2_an_dict = pd.Series(df["an"].values, index=df["name"]).to_dict()
    df["name_v2"] = df["name"].apply(lambda x: x.replace("-", "_").lower())
    name_2_an_dict_v2 = pd.Series(df["an"].values, index=df["name_v2"]).to_dict()
    name_2_an_dict.update(name_2_an_dict_v2)
    name_no_mapping_list = []
    with open(fn_in, "r") as fh_in:
        with open(fn_out, "w") as fh_out:
            for line in fh_in:
                ENSP, name_array, etype_newline = line.split("\t")
                name_set = ast.literal_eval(name_array)
                an_list = []
                for name in name_set:
                    try:
                        an_list.append(name_2_an_dict[name])
                    except KeyError:
                        # not in the lookup, therefore should be skipped since most likely obsolete in current version
                        name_no_mapping_list.append(name)
                if an_list: # not empty
                    fh_out.write(ENSP + "\t{" + str(sorted(an_list))[1:-1].replace(" ", "").replace("'", '"') + "}\t" + etype_newline)
    with open(fn_no_mapping, "w") as fh_no_mapping:
        fh_no_mapping.write("\n".join(sorted(set(name_no_mapping_list))))

def create_Functions_table_SMART(fn_in, fn_out):
    # http://smart.embl-heidelberg.de/smart/descriptions.pl downloaded 20180808
    columns = ['DOMAIN', 'ACC', 'DEFINITION', 'DESCRIPTION']
    df = pd.read_csv(fn_in, sep="\t", skiprows=2, names=columns)
    # "etype" --> -53
    # "name" --> "DOMAIN"
    # "an" --> "ACC"
    # "definition" --> "DEFINITION; DESCRIPTION"
    entityType_SMART = id_2_entityTypeNumber_dict["SMART"]
    df["etype"] = entityType_SMART
    df = df[["etype", "DOMAIN", "ACC", "DEFINITION", "DESCRIPTION"]]
    df["definition"] = df["DEFINITION"].fillna("") + "; " + df["DESCRIPTION"].fillna("")
    df["definition"] = df["definition"].apply(lambda x: x.replace("\n", "").replace("\t", " "))
    df = df[["etype", "DOMAIN", "ACC", "definition"]]
    df.to_csv(fn_out, sep="\t", header=False, index=False)

def create_Functions_table_PFAM(fn_in, fn_out):
    # ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.clans.tsv.gz (from 24/02/2017 downloaded 20180808)
    # fn = r"/home/dblyon/agotool/data/PostgreSQL/downloads/Pfam-A.clans.tsv"
    columns = ['an', 'clan_an', 'HOMSTRAD', 'name', 'definition']
    df = pd.read_csv(fn_in, sep="\t", names=columns)
    df["etype"] = id_2_entityTypeNumber_dict["PFAM"]
    df = df[["etype", "name", "an", "definition"]]
    # fn_out = r"/home/dblyon/agotool/data/PostgreSQL/tables/Functions_table_PFAM.txt"
    df.to_csv(fn_out, sep="\t", header=False, index=False)

def create_Functions_table_InterPro(fn_in, fn_out):
    df = pd.read_csv(fn_in, sep='\t', names=["an", "name"])
    df["etype"] = id_2_entityTypeNumber_dict["INTERPRO"]
    df["definition"] = ""
    df = df[["etype", "name", "an", "definition"]]
    df.to_csv(fn_out, sep="\t", header=False, index=False)

def create_Protein_2_Function_table_GO(GO_dag, fn_in, fn_in_temp, fn_out, number_of_processes=1, verbose=True):
    """
    secondary GOids are converted to primary GOids
    e.g. goterm: 'GO:0007610' has secondary id 'GO:0044708', thus if 'GO:0044708' is associated it will be mapped to 'GO:0007610'
    :param GO_dag: Dict like object
    :param fn_in: String (e.g. /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/downloads/string_go.tsv.gz)
    :param fn_in_temp: String (Temp file to be deleted later e.g. /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/downloads/string_go.tsv.gz_temp)
    :param fn_out: String (e.g. /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables/Protein_2_Function_table_GO.txt)
    :param number_of_processes: Integer (number of cores, shouldn't be too high since Disks are probably the bottleneck even with SSD, e.g. max 4)
    :param verbose: Bool (flag to print infos)
    :return: None
    """
    ### e.g. of lines
    # 1001530 PMSV_1450       -21     GO:0000302      UniProtKB-EC    IEA     2       FALSE   http://www.uniprot.org/uniprot/SODF_PHOLE
    # 1000565 METUNv1_03599   -23     GO:0003824      UniProtKB-EC    IEA     2       FALSE   http://www.uniprot.org/uniprot/GMAS_METUF
    if verbose:
        print("\ncreate_Protein_2_Function_table_GO")

    # bash_script_temp_fn = "bash_script_gunzip_sort_GO.sh"
    gunzip_file(fn_in, fn_in_temp)
    sort_file(fn_in_temp, fn_in_temp, columns="1,2", number_of_processes=number_of_processes)
    # with open(bash_script_temp_fn, "w") as fh:
    #     fh.write("#!/usr/bin/env bash\n")
    #     shellcmd_1 = "gunzip -c {} > {}".format(fn_in, fn_in_temp)
    #     fh.write(shellcmd_1 + "\n")
    #     if PLATFORM == "linux":
    #         shellcmd_2 = "sort --parallel {} -k1,2 {} -o {}".format(number_of_processes, fn_in_temp, fn_in_temp)
    #     else:
    #         shellcmd_2 = "LC_ALL=C gsort --parallel {} -k1,2 {} -o {}".format(number_of_processes, fn_in_temp, fn_in_temp)
    #     fh.write(shellcmd_2)
    if verbose:
        print("gunzip and sorting string_go.tsv.gz")
    # subprocess.call("chmod 744 ./{}".format(bash_script_temp_fn), shell=True)
    # subprocess.call("./{}".format(bash_script_temp_fn), shell=True)

    GOterms_not_in_obo = []
    if verbose:
        print("parsing previous result to produce Protein_2_Function_table_GO.txt")
    with open(fn_out, "w") as fh_out:
        for ENSP, GOterm_list, _ in parse_string_go_yield_entry(fn_in_temp):
            # if entityType == "-24":
            #     continue
            # GOterm_list = sorted(set(GOterm_list))
            GOterm_list, GOterms_not_in_obo_temp = get_all_parent_terms(GOterm_list, GO_dag)
            GOterms_not_in_obo += GOterms_not_in_obo_temp
            if len(GOterm_list) >= 1:
                # fh_out.write(ENSP + "\t" + "{" + str(GOterm_list)[1:-1].replace(" ", "").replace("'", '"') + "}\t" + entityType + "\n")
                MFs, CPs, BPs, not_in_OBO = divide_into_categories(GOterm_list, GO_dag, [], [], [], [])
                GOterms_not_in_obo_temp += not_in_OBO
                if MFs:
                    fh_out.write(ENSP + "\t" + "{" + str(MFs)[1:-1].replace(" ", "").replace("'", '"') + "}\t" + id_2_entityTypeNumber_dict['GO:0003674'] + "\n")
                if CPs:
                    fh_out.write(ENSP + "\t" + "{" + str(CPs)[1:-1].replace(" ", "").replace("'", '"') + "}\t" + id_2_entityTypeNumber_dict['GO:0005575'] + "\n")
                if BPs:
                    fh_out.write(ENSP + "\t" + "{" + str(BPs)[1:-1].replace(" ", "").replace("'", '"') + "}\t" + id_2_entityTypeNumber_dict['GO:0008150'] + "\n")
    ### id_2_entityTypeNumber_dict = {'GO:0003674': "-23",  # 'Molecular Function',
    ###                               'GO:0005575': "-22",  # 'Cellular Component',
    ## #                              'GO:0008150': "-21",  # 'Biological Process',
    GOterms_not_in_obo = sorted(set(GOterms_not_in_obo))
    fn_log = os.path.join(LOG_DIRECTORY, "create_SQL_tables_GOterms_not_in_OBO.log")
    with open(fn_log, "w") as fh_out:
        fh_out.write(";".join(GOterms_not_in_obo))
    if verbose:
        print("Number of GO terms not in OBO: ", len(GOterms_not_in_obo))
        print("done create_Protein_2_Function_table_GO\n")

def create_Protein_2_Function_table_UniProtKeyword(UPK_Name_2_AN_dict, UPK_dag, fn_in_uniprot_SwissProt_dat, fn_in_uniprot_TrEMBL_dat, fn_in_uniprot_2_string, fn_out, number_of_processes=1,  verbose=True):
    if verbose:
        print("\ncreate_Protein_2_Function_table_UniProtKeywords")
    uniprot_2_string_missing_mapping = []
    uniprot_2_ENSPs_dict = parse_full_uniprot_2_string(fn_in_uniprot_2_string)
    entityType_UniProtKeywords = id_2_entityTypeNumber_dict["UniProtKeywords"]
    UPKs_not_in_obo_list = []

    with open(fn_out, "w") as fh_out:
        if verbose:
            print("parsing {}".format(fn_in_uniprot_SwissProt_dat))
        for UniProtAN_list, KeyWords_list in parse_uniprot_dat_dump_yield_entry(fn_in_uniprot_SwissProt_dat):
            for UniProtAN in UniProtAN_list:
                try:
                    ENSP_list = uniprot_2_ENSPs_dict[UniProtAN]
                except KeyError:
                    uniprot_2_string_missing_mapping.append(UniProtAN)
                    continue
                for ENSP in ENSP_list:
                    if len(KeyWords_list) >= 1:
                        UPK_ANs, UPKs_not_in_obo_temp = map_keyword_name_2_AN(UPK_Name_2_AN_dict, KeyWords_list)
                        UPKs_not_in_obo_list += UPKs_not_in_obo_temp
                        KeyWords_list, UPKs_not_in_obo_temp = get_all_parent_terms(UPK_ANs, UPK_dag)
                        UPKs_not_in_obo_list += UPKs_not_in_obo_temp
                        fh_out.write(ENSP + "\t" + "{" + str(KeyWords_list)[1:-1].replace(" ", "").replace("'", '"') + "}\t" + entityType_UniProtKeywords + "\n")

        if verbose:
            print("parsing {}".format(fn_in_uniprot_TrEMBL_dat))
        for UniProtAN_list, KeyWords_list in parse_uniprot_dat_dump_yield_entry(fn_in_uniprot_TrEMBL_dat):
            for UniProtAN in UniProtAN_list:
                try:
                    ENSP_list = uniprot_2_ENSPs_dict[UniProtAN]
                except KeyError:
                    uniprot_2_string_missing_mapping.append(UniProtAN)
                    continue
                for ENSP in ENSP_list:
                    if len(KeyWords_list) >= 1:
                        UPK_ANs, UPKs_not_in_obo_temp = map_keyword_name_2_AN(UPK_Name_2_AN_dict, KeyWords_list)
                        UPKs_not_in_obo_list += UPKs_not_in_obo_temp
                        KeyWords_list, UPKs_not_in_obo_temp = get_all_parent_terms(UPK_ANs, UPK_dag)
                        UPKs_not_in_obo_list += UPKs_not_in_obo_temp
                        fh_out.write(ENSP + "\t" + "{" + str(KeyWords_list)[1:-1].replace(" ", "").replace("'", '"') + "}\t" + entityType_UniProtKeywords + "\n")

    ### table Protein_2_Function_table_UniProtKeywords.txt needs sorting
    sort_file(fn_out, fn_out, columns="1", number_of_processes=number_of_processes, verbose=verbose)

    UPKs_not_in_obo_list = sorted(set(UPKs_not_in_obo_list))
    fn_log = os.path.join(LOG_DIRECTORY, "create_SQL_tables_UniProtKeywords_not_in_OBO.log")
    with open(fn_log, "w") as fh_out:
        fh_out.write(";".join(UPKs_not_in_obo_list))

    if len(uniprot_2_string_missing_mapping) > 0:
        print("#!$%^@"*80)
        print("writing uniprot_2_string_missing_mapping to log file\n", os.path.join(LOG_DIRECTORY, "create_SQL_tables_STRING.log"))
        print("number of uniprot_2_string_missing_mapping", len(uniprot_2_string_missing_mapping))
        print("number of uniprot_2_ENSPs_dict keys", len(uniprot_2_ENSPs_dict.keys()))
        print("#!$%^@" * 80)
        with open(os.path.join(LOG_DIRECTORY, "create_SQL_tables_STRING.log"), "a+") as fh:
            fh.write(";".join(uniprot_2_string_missing_mapping))

    if verbose:
        print("Number of UniProt Keywords not in OBO: ", len(UPKs_not_in_obo_list))
        print("done create_Protein_2_Function_table_UniProtKeywords\n")

def create_Protein_2_Function_table_KEGG_STRING(fn_in, fn_out_temp, fn_out, number_of_processes=1, verbose=True):
    # create long format of ENSP 2 KEGG table
    with open(fn_in, "r") as fh_in:
        with open(fn_out_temp, "w") as fh_out:
            for line in fh_in:
                TaxID, KEGG, num_ENSPs, *ENSPs = line.split()
                if KEGG.startswith("CONN_"):
                    continue
                else: # e.g. bced00190 or rhi00290
                    KEGG = KEGG[-5:]
                # add TaxID to complete the ENSP
                ENSPs = [TaxID + "." + ENSP for ENSP in ENSPs]
                for ENSP in ENSPs:
                    fh_out.write(ENSP + "\t" + "KEGG:" + KEGG + "\n")

    # sort by first column and transform to wide format
    bash_script_temp_fn = "bash_script_sort_Protein_2_Function_table_KEGG_temp.sh"
    with open(bash_script_temp_fn, "w") as fh:
        fh.write("#!/usr/bin/env bash\n")
        if PLATFORM == "linux":
            shellcmd = "sort --parallel {} -k1 {} -o {}".format(number_of_processes, fn_out_temp, fn_out_temp)
        else:
            shellcmd = "LC_ALL=C gsort --parallel {} -k1 {} -o {}".format(number_of_processes, fn_out_temp, fn_out_temp)
        fh.write(shellcmd)
    if verbose:
        print("Protein_2_Function_table_KEGG_temp.txt needs sorting, doing it now")
    subprocess.call("chmod 744 ./{}".format(bash_script_temp_fn), shell=True)
    subprocess.call("./{}".format(bash_script_temp_fn), shell=True)

    # convert long to wide format and add entity type
    entityType_UniProtKeywords = id_2_entityTypeNumber_dict["KEGG"]
    long_2_wide_format(fn_out_temp, fn_out, entityType_UniProtKeywords)

def get_all_parent_terms(GOterm_list, GO_dag):
    """
    backtracking to root INCLUDING given children
    :param GOterm_list: List of String
    :param GO_dag: Dict like object
    :return: List of String
    """
    parents = []
    not_in_obo = []
    for GOterm in GOterm_list:
        try:
            parents += GO_dag[GOterm].get_all_parents()
        except KeyError: # remove GOterm from DB since not in OBO #!!! ToDo check with the boss
            # parents += [GOterm]
            not_in_obo.append(GOterm)
    return sorted(set(parents).union(set(GOterm_list))), sorted(set(not_in_obo))

def map_keyword_name_2_AN(UPK_Name_2_AN_dict, KeyWords_list):
    UPK_ANs, UPKs_not_in_obo_temp = [], []
    for keyword in KeyWords_list:
        try:
            AN = UPK_Name_2_AN_dict[keyword]
        except KeyError:
            UPKs_not_in_obo_temp.append(keyword)
            continue
        UPK_ANs.append(AN)
    return UPK_ANs, UPKs_not_in_obo_temp

def divide_into_categories(GOterm_list, GO_dag,
                           MFs=[], CPs=[], BPs=[], not_in_OBO=[]):
    """
    split a list of GO-terms into the 3 parent categories in the following order MFs, CPs, BPs
    'GO:0003674': "-23",  # 'Molecular Function',
    'GO:0005575': "-22",  # 'Cellular Component',
    'GO:0008150': "-21",  # 'Biological Process',
    :param GOterm_list: List of String
    :param GO_dag: Dict like object
    :return: Tuple (List of String x 3)
    """
#     MFs, CPs, BPs, not_in_OBO = [], [], [], []
    for term in GOterm_list:
        if term == "GO:0003674" or GO_dag[term].has_parent("GO:0003674"):
            MFs.append(GO_dag[term].id)
        elif term == "GO:0005575" or GO_dag[term].has_parent("GO:0005575"):
            CPs.append(GO_dag[term].id)
        elif term == "GO:0008150" or GO_dag[term].has_parent("GO:0008150"):
            BPs.append(GO_dag[term].id)
        else:
            try:
                GO_id = GO_dag[term].id
            except KeyError:
                not_in_OBO.append(term)
                continue
            if GO_dag[GO_id].is_obsolete:
                not_in_OBO.append(term)
            else:
                MFs, CPs, BPs, not_in_OBO = divide_into_categories([GO_id], GO_dag, MFs, CPs, BPs, not_in_OBO)
    return sorted(MFs), sorted(CPs), sorted(BPs), sorted(not_in_OBO)

def get_entity_type_from_GO_term(term, GO_dag):
    if term == "GO:0003674" or GO_dag[term].has_parent("GO:0003674"):
        return "-23"
    elif term == "GO:0005575" or GO_dag[term].has_parent("GO:0005575"):
        return "-22"
    elif term == "GO:0008150" or GO_dag[term].has_parent("GO:0008150"):
        return "-21"
    else:
        return "-24"

def parse_uniprot_dat_dump_yield_entry(fn_in):
    """
    yield parsed entry from UniProt DB dump file
    :param fn_in:
    :return:
    """
    for entry in yield_entry_UniProt_dat_dump(fn_in):
        UniProtAN_list, UniProtAN, Keywords_string = [], "", ""
        for line in entry:
            line_code = line[:2]
            rest = line[2:].strip()
            if line_code == "AC":
                UniProtAN_list += [UniProtAN.strip() for UniProtAN in rest.split(";") if len(UniProtAN) > 0]
            elif line_code == "KW":
                Keywords_string += rest
        UniProtAN_list = sorted(set(UniProtAN_list))
        Keywords_list = sorted(set(Keywords_string.split(";")))
        # remove empty strings from keywords_list
        Keywords_list = [cleanup_Keyword(keyword) for keyword in Keywords_list if len(keyword) > 0]
        yield (UniProtAN_list, Keywords_list)

def cleanup_Keyword(keyword):
    """
    remove stuff after '{'
    remove '.' at last keyword
    remove last ',' in string
    "ATP-binding{ECO:0000256|HAMAP-Rule:MF_00175,","Chaperone{ECO:0000256|HAMAP-Rule:MF_00175,","Completeproteome{ECO:0000313|Proteomes:UP000005019}","ECO:0000256|SAAS:SAAS00645729}","ECO:0000256|SAAS:SAAS00645733}","ECO:0000256|SAAS:SAAS00645738}.","ECO:0000256|SAAS:SAAS00701776}","ECO:0000256|SAAS:SAAS00701780,ECO:0000313|EMBL:EGK73413.1}","Hydrolase{ECO:0000313|EMBL:EGK73413.1}","Metal-binding{ECO:0000256|HAMAP-Rule:MF_00175,","Nucleotide-binding{ECO:0000256|HAMAP-Rule:MF_00175,","Protease{ECO:0000313|EMBL:EGK73413.1}","Referenceproteome{ECO:0000313|Proteomes:UP000005019}","Zinc{ECO:0000256|HAMAP-Rule:MF_00175,ECO:0000256|SAAS:SAAS00645735}","Zinc-finger{ECO:0000256|HAMAP-Rule:MF_00175,"
    :param keyword:
    :return:
    """
    try:
        index_ = keyword.index("{")
    except ValueError:
        index_ = False
    if index_:
        keyword = keyword[:index_]
    return keyword.replace(".", "").strip()

def yield_entry_UniProt_dat_dump(fn_in):
    """
    yield a single entry, delimited by '//' at the end
    of UniProt DB dump files
    fn_in = "uniprot_sprot.dat.gz"
    '//         Terminator                        Once; ends an entry'
    # ID   D5EJT0_CORAD            Unreviewed;       296 AA.
    # AC   D5EJT0;
    # DT   15-JUN-2010, integrated into UniProtKB/TrEMBL.
    # DT   15-JUN-2010, sequence version 1.
    # DT   25-OCT-2017, entry version 53.
    # DE   SubName: Full=Binding-protein-dependent transport systems inner membrane component {ECO:0000313|EMBL:ADE54679.1};
    # GN   OrderedLocusNames=Caka_1660 {ECO:0000313|EMBL:ADE54679.1};
    # OS   Coraliomargarita akajimensis (strain DSM 45221 / IAM 15411 / JCM 23193
    # OS   / KCTC 12865 / 04OKA010-24).
    # OC   Bacteria; Verrucomicrobia; Opitutae; Puniceicoccales;
    # OC   Puniceicoccaceae; Coraliomargarita.
    # OX   NCBI_TaxID=583355 {ECO:0000313|EMBL:ADE54679.1, ECO:0000313|Proteomes:UP000000925};
    # RN   [1] {ECO:0000313|EMBL:ADE54679.1, ECO:0000313|Proteomes:UP000000925}
    # RP   NUCLEOTIDE SEQUENCE [LARGE SCALE GENOMIC DNA].
    # RC   STRAIN=DSM 45221 / IAM 15411 / JCM 23193 / KCTC 12865
    # RC   {ECO:0000313|Proteomes:UP000000925};
    # RX   PubMed=21304713; DOI=10.4056/sigs.952166;
    # RA   Mavromatis K., Abt B., Brambilla E., Lapidus A., Copeland A.,
    # RA   Deshpande S., Nolan M., Lucas S., Tice H., Cheng J.F., Han C.,
    # RA   Detter J.C., Woyke T., Goodwin L., Pitluck S., Held B., Brettin T.,
    # RA   Tapia R., Ivanova N., Mikhailova N., Pati A., Liolios K., Chen A.,
    # RA   Palaniappan K., Land M., Hauser L., Chang Y.J., Jeffries C.D.,
    # RA   Rohde M., Goker M., Bristow J., Eisen J.A., Markowitz V.,
    # RA   Hugenholtz P., Klenk H.P., Kyrpides N.C.;
    # RT   "Complete genome sequence of Coraliomargarita akajimensis type strain
    # RT   (04OKA010-24).";
    # RL   Stand. Genomic Sci. 2:290-299(2010).
    # CC   -!- SUBCELLULAR LOCATION: Cell membrane
    # CC       {ECO:0000256|RuleBase:RU363032}; Multi-pass membrane protein
    # CC       {ECO:0000256|RuleBase:RU363032}.
    # CC   -!- SIMILARITY: Belongs to the binding-protein-dependent transport
    # CC       system permease family. {ECO:0000256|RuleBase:RU363032,
    # CC       ECO:0000256|SAAS:SAAS00723689}.
    # CC   -----------------------------------------------------------------------
    # CC   Copyrighted by the UniProt Consortium, see http://www.uniprot.org/terms
    # CC   Distributed under the Creative Commons Attribution-NoDerivs License
    # CC   -----------------------------------------------------------------------
    # DR   EMBL; CP001998; ADE54679.1; -; Genomic_DNA.
    # DR   RefSeq; WP_013043401.1; NC_014008.1.
    # DR   STRING; 583355.Caka_1660; -.
    # DR   EnsemblBacteria; ADE54679; ADE54679; Caka_1660.
    # DR   KEGG; caa:Caka_1660; -.
    # DR   eggNOG; ENOG4105C2T; Bacteria.
    # DR   eggNOG; COG1173; LUCA.
    # DR   HOGENOM; HOG000171367; -.
    # DR   KO; K15582; -.
    # DR   OMA; PTGIWWT; -.
    # DR   OrthoDB; POG091H0048; -.
    # DR   Proteomes; UP000000925; Chromosome.
    # DR   GO; GO:0016021; C:integral component of membrane; IEA:UniProtKB-KW.
    # DR   GO; GO:0005886; C:plasma membrane; IEA:UniProtKB-SubCell.
    # DR   GO; GO:0006810; P:transport; IEA:UniProtKB-KW.
    # DR   CDD; cd06261; TM_PBP2; 1.
    # DR   Gene3D; 1.10.3720.10; -; 1.
    # DR   InterPro; IPR000515; MetI-like.
    # DR   InterPro; IPR035906; MetI-like_sf.
    # DR   InterPro; IPR025966; OppC_N.
    # DR   Pfam; PF00528; BPD_transp_1; 1.
    # DR   Pfam; PF12911; OppC_N; 1.
    # DR   SUPFAM; SSF161098; SSF161098; 1.
    # DR   PROSITE; PS50928; ABC_TM1; 1.
    # PE   3: Inferred from homology;
    # KW   Cell membrane {ECO:0000256|SAAS:SAAS00894688};
    # KW   Complete proteome {ECO:0000313|Proteomes:UP000000925};
    # KW   Membrane {ECO:0000256|RuleBase:RU363032,
    # KW   ECO:0000256|SAAS:SAAS00893669};
    # KW   Reference proteome {ECO:0000313|Proteomes:UP000000925};
    # KW   Transmembrane {ECO:0000256|RuleBase:RU363032,
    # KW   ECO:0000256|SAAS:SAAS00894237};
    # KW   Transmembrane helix {ECO:0000256|RuleBase:RU363032,
    # KW   ECO:0000256|SAAS:SAAS00894527};
    # KW   Transport {ECO:0000256|RuleBase:RU363032,
    # KW   ECO:0000256|SAAS:SAAS00723738}.
    # FT   TRANSMEM     34     53       Helical. {ECO:0000256|RuleBase:RU363032}.
    # FT   TRANSMEM     94    119       Helical. {ECO:0000256|RuleBase:RU363032}.
    # FT   TRANSMEM    131    150       Helical. {ECO:0000256|RuleBase:RU363032}.
    # FT   TRANSMEM    156    175       Helical. {ECO:0000256|RuleBase:RU363032}.
    # FT   TRANSMEM    214    239       Helical. {ECO:0000256|RuleBase:RU363032}.
    # FT   TRANSMEM    259    282       Helical. {ECO:0000256|RuleBase:RU363032}.
    # FT   DOMAIN       92    282       ABC transmembrane type-1.
    # FT                                {ECO:0000259|PROSITE:PS50928}.
    # SQ   SEQUENCE   296 AA;  32279 MW;  3DB3B060376AFDB5 CRC64;
    #      MIKQQREAKA VSVAATSLGQ DAWERLKRNN MARIGGTLFA IITALCIVGP WLLPHSYDAQ
    #      NLAYGAQGPS WQHLLGTDDL GRDLLVRILV GGRISIGVGF AASLVALIIG VSYGALAGYI
    #      GGRTESVMMR FVDAVYALPF TMIVIILTVT FDEKSIFLIF MAIGLVEWLT MARIVRGQTK
    #      ALRQLNYIDA ARTMGASHLS ILTRHILPNL LGPVIVFTTL TIPAVILLES ILSFLGLGVQ
    #      PPMSSWGILI NEGADKIDIY PWLLIFPALF FSLTIFALNF IGDGLRDALD PKESQH
    # //
    """
    lines_list = []
    for line in yield_line_uncompressed_or_gz_file(fn_in):
        line = line.strip()
        if not line.startswith("//"):
            lines_list.append(line)
        else:
            yield lines_list
            lines_list = []
    if lines_list:
        if len(lines_list[0]) == 0:
            return None
    else:
        yield lines_list

def parse_string2interpro_yield_entry(fn_in):
    # "1298865.H978DRAFT_0001  A0A010P2C8      IPR011990       Tetratricopeptide-like helical domain superfamily       G3DSA:1.25.40.10        182     292"
    InterProID_list = []
    did_first = False
    for line in yield_line_uncompressed_or_gz_file(fn_in):
        ENSP, UniProtAN, InterProID, *rest = line.split()
        if not did_first:
            ENSP_previous = ENSP
            did_first = True
        if ENSP == ENSP_previous:
            InterProID_list.append(InterProID)
        else:
            yield (ENSP_previous, InterProID_list)
            InterProID_list = [InterProID]
            ENSP_previous = ENSP
    yield (ENSP_previous, InterProID_list)

def parse_string11_dom_prot_full_yield_entry(fn_in):
    domain_list = []
    did_first = False
    ENSP_previous = ""
    counter = 0
    with open(fn_in, "r") as fh_in:
        for line in fh_in:
            counter += 1
            try:
                domain, ENSP, *rest = line.split()
            except ValueError:
                print("-" * 80)
                print(line)
                print(counter)
                print("-" * 80)
                continue
            if not did_first:
                ENSP_previous = ENSP
                did_first = True
            if ENSP == ENSP_previous:
                domain_list.append(domain)
            else:
                yield (ENSP_previous, sort_PFAM_and_SMART(domain_list))
                domain_list = [domain]
                ENSP_previous = ENSP
        yield (ENSP_previous, sort_PFAM_and_SMART(domain_list))

def sort_PFAM_and_SMART(list_of_domain_names):
    PFAM_list, SMART_list = [], []
    for domain in set(list_of_domain_names):
        if domain.startswith("Pfam:"):
            PFAM_list.append(domain.replace("Pfam:", ""))
        elif domain in {"TRANS", "COIL", "SIGNAL"}:
            continue
        else:
            SMART_list.append(domain)
    return sorted(PFAM_list), sorted(SMART_list)

def parse_string_go_yield_entry(fn_in):
    """
    careful the entity type will NOT (necessarily) be consistent as multiple annotations are given
    :param fn_in:
    :return:
    """
    # "9606    ENSP00000281154 -24     GO:0019861      UniProtKB       CURATED 5       TRUE    http://www.uniprot.org/uniprot/ADT4_HUMAN"
    GOterm_list = []
    did_first = False
    for line in yield_line_uncompressed_or_gz_file(fn_in):
        TaxID, ENSP_without_TaxID, EntityType, GOterm, *rest = line.split()
        if not GOterm.startswith("GO:"):
            continue
        ENSP = TaxID + "." + ENSP_without_TaxID
        if not did_first:
            ENSP_previous = ENSP
            did_first = True
        if ENSP == ENSP_previous:
            GOterm_list.append(GOterm)
        else:
            yield (ENSP_previous, GOterm_list, EntityType)
            GOterm_list = [GOterm]
            ENSP_previous = ENSP
    yield (ENSP_previous, GOterm_list, EntityType)

def parse_full_uniprot_2_string(fn_in):
    """
    #species   uniprot_ac|uniprot_id   string_id   identity   bit_score
    742765  G1WQX1|G1WQX1_9FIRM     742765.HMPREF9457_01522 100.0   211.0
    742765  G1WQX2|G1WQX2_9FIRM     742765.HMPREF9457_01523 100.0   70.5
    """
    uniprot_2_ENSPs_dict = {}
    with open(fn_in, "r") as fh:
        next(fh) # skip header line
        for line in fh:
            taxid, uniprot_ac_and_uniprot_id, ENSP, *rest= line.strip().split()
            uniprot = uniprot_ac_and_uniprot_id.split("|")[0]
            if not uniprot in uniprot_2_ENSPs_dict :
                uniprot_2_ENSPs_dict[uniprot] = [ENSP]
            else: # it can be a one to many mapping (1 UniProtAN to multiple ENSPs)
                uniprot_2_ENSPs_dict[uniprot].append(ENSP)
    return uniprot_2_ENSPs_dict

def yield_line_uncompressed_or_gz_file(fn):
    """
    adapted from
    https://codebright.wordpress.com/2011/03/25/139/
    and
    https://www.reddit.com/r/Python/comments/2olhrf/fast_gzip_in_python/
    http://pastebin.com/dcEJRs1i
    :param fn: String (absolute path)
    :return: GeneratorFunction (yields String)
    """
    if fn.endswith(".gz"):
        if PLATFORM == "darwin": # OSX: "Darwin"
            ph = subprocess.Popen(["gzcat", fn], stdout=subprocess.PIPE)
        elif PLATFORM == "linux": # Debian: "Linux"
            ph = subprocess.Popen(["zcat", fn], stdout=subprocess.PIPE)
        else:
            ph = subprocess.Popen(["cat", fn], stdout=subprocess.PIPE)

        for line in ph.stdout:
            yield line.decode("utf-8")
    else:
        with open(fn, "r") as fh:
            for line in fh:
                yield line

def get_table_name_2_absolute_path_dict(testing=False):
    global TABLES_DIR
    if testing:
        TABLES_DIR = TEST_DIR
    functions_table = os.path.join(TABLES_DIR, "Functions_table.txt")
    go_2_slim_table = os.path.join(TABLES_DIR, "GO_2_Slim_table.txt")
    og_2_function_table = os.path.join(STATIC_DIR, "OG_2_Function_table_static.txt")
    ogs_table = os.path.join(STATIC_DIR, "OGs_table_static.txt")
    ontologies_table = os.path.join(TABLES_DIR, "Ontologies_table.txt")
    protein_2_function_table = os.path.join(TABLES_DIR, "Protein_2_Function_table.txt")
    protein_2_og_table = os.path.join(STATIC_DIR, "Protein_2_OG_table_static.txt")
    protein_secondary_2_primary_an_table = os.path.join(TABLES_DIR, "Protein_Secondary_2_Primary_AN_table.txt")
    table_name_2_absolute_path_dict = {"functions_table": functions_table,
                                       "go_2_slim_table": go_2_slim_table,
                                       "og_2_function_table": og_2_function_table,
                                       "ogs_table": ogs_table,
                                       "ontologies_table": ontologies_table,
                                       "protein_2_function_table": protein_2_function_table,
                                       "protein_2_og_table": protein_2_og_table,
                                       "protein_secondary_2_primary_an_table": protein_secondary_2_primary_an_table}
    return table_name_2_absolute_path_dict

##### create test tables for import
def create_test_tables(num_lines=5000, TABLES_DIR_=None, version_="STRING"):
    if not os.path.exists(TEST_DIR):
        os.makedirs(TEST_DIR)
    if TABLES_DIR_ is None:
        TABLES_DIR_ = TABLES_DIR
    fn_list = [os.path.join(TABLES_DIR_, fn) for fn in os.listdir(TABLES_DIR_)]
    if version_ == "STRING":
        fn_list = [fn for fn in fn_list if fn.endswith("_table_STRING.txt")]
    elif version_ == "aGOtool":
        fn_list = [fn for fn in fn_list if fn.endswith("_table_aGOtool.txt")]
    else:
        print("Can't interpret version_ {} to create_test_tables".format(version_))
        raise NotImplementedError
    fn_list_static = [os.path.join(STATIC_DIR, fn) for fn in os.listdir(STATIC_DIR)]
    fn_list_static = [fn for fn in fn_list_static if fn.endswith("_table_static.txt")]
    fn_list += fn_list_static
    for fn in fn_list:
        counter = 0
        with open(fn, "r") as fh_in:
            fn_out = os.path.join(TEST_DIR, os.path.basename(fn))
            with open(fn_out, "w") as fh_out:
                for line in fh_in:
                    if counter >= num_lines:
                        break
                    fh_out.write(line)
                    counter += 1

##### Protein_2_OG_table_static.txt
### only for HOMD-data since the Bacterial proteins are the only ones mapped to OGs
### this relies on previous mapping of bacterial proteins to OGs via Hidden Markov Models from eggNOG using HMMer
def create_Protein_2_OG_table():
    """
    fn_in HOMD_Protein_2_OG_parsed.txt (AN-Protein, OG1;OG2) from HMMER results
    fn_outProtein_2_OG_table_static.txt (AN-Protein, OG1)
    :return: None
    """
    print("create_Protein_2_OG_table")
    fn_in = os.path.join(STATIC_DIR, "results_AN_2_HMMs_HOMD_UPstyle_201607_AND_HOMD_UPstyle_201508_static.txt")  # HMMER results, previously 'HOMD_AN2NOGname_parsed.txt'
    fn_out = os.path.join(STATIC_DIR, "Protein_2_OG_table_static.txt")
    with open(fn_in, "r") as fh_in:
        with open(fn_out, "w") as fh_out:
            for line in fh_in:
                try:
                    an, hmm = line.split("\t")
                except ValueError:
                    continue
                try:
                    hmm_list = [ele.split(".")[1] for ele in hmm.split(";")]
                except IndexError:
                    continue
                for hmm in hmm_list:
                    string2write = an + "\t" + hmm + "\n"
                    fh_out.write(string2write)

# #### OG_2_Function_table_static.txt, OGs_table_static.txt, and Functions_table_KEGG_DOM.txt
# http://eggnogdb.embl.de/download/latest/all_OG_annotations.tsv.gz
# #### retrieving eggNOG attributes
def get_og_names():
    """
    return iterable Orthologous Group names
    :return: ArrayOfString
    """
    fn = os.path.join(DOWNLOADS_DIR, "bactNOG.annotations.tsv")
    df = pd.read_csv(fn, sep='\t', names=["bactNOG", "NOGname", "C", "D", "E", "F"])
    og_names = df["NOGname"].unique()
    return og_names

def yield_entry_from_all_annotations():
    """
    ENOG41xxxxx = Unsupervised Cluster of Orthologous Group (present in all levels)
    OG_name_short | GroupName | ProteinCount | description | dunno | GO | KEGG | domains | members |
    """
    fn = os.path.join(DOWNLOADS_DIR, "all_OG_annotations.tsv")
    og_names = get_og_names()
    # og.replace("ENOG41", "") faster but no check below
    og_names_short = {og[6:] for og in og_names}
    with open(fn, "r") as fh:
        for line in fh:
            line_split = line.strip().split("\t")
            if line_split[0] in og_names_short:
                og_name = "ENOG41" + line_split[0]
                description = line_split[3]
                go = line_split[5]
                go = json.loads(go)
                KEGG = line_split[6]
                KEGG = json.loads(KEGG)
                domains = line_split[7]
                domains = json.loads(domains)
                yield (og_name, description, go, KEGG, domains)

def parse_go_terms_or_domains_all_annotations(json_):
    """
    more concise dict coming from all_annotations file
    :param json_:
    :return:
    """
    attributes_list = []
    categories = json_.keys()
    for cat in categories:
        attributes_list += [ele[0] for ele in json_[cat]]
    return attributes_list

def parse_KEGG_all_annotaions(kegg_list):
    pw_name_list, pw_num_list = [], []
    kegg_funcs = [ele[0] for ele in kegg_list]
    for pawthway_name_number in kegg_funcs:
        index_ = pawthway_name_number.index("(")
        pw_name = pawthway_name_number[:index_].strip()
        pw_num = pawthway_name_number[index_ + 1:-1].strip()
        pw_name_list.append(pw_name)
        pw_num_list.append(pw_num)
    return pw_name_list, pw_num_list

def parse_functions(go, KEGG, domains):
    """
    from a single entry in all_OG_annotations.tsv
    parse the GO, KEGG and domain functions and add the appropriate prefix
    :param go: Dict
    :param KEGG: List
    :param domains: Dict
    :return: Tuple(ListOfString Tuple(ListOfString, ListOfString))
    """
    functions = parse_go_terms_or_domains_all_annotations(go)

    domains_list = parse_go_terms_or_domains_all_annotations(domains)
    functions += ["DOM:" + ele for ele in domains_list]

    pw_name_list, pw_num_list = parse_KEGG_all_annotaions(KEGG)
    pw_num_list = ["KEGG:" + ele for ele in pw_num_list]
    functions += pw_num_list

    return functions, zip(pw_name_list, pw_num_list)

def create_OGs_table_and_OG_2_Function_table_and_Functions_table_DOM():
    """
    # OGs_table_static.txt --> complete
    # og, taxid, description (taxid = 2 for all bacterial OGs)

    # OG_2_Function_table_static.txt --> complete
    # og, function

    # Functions_table_KEGG_DOM.txt --> partial
    # type_, description, an
    :return:
    """
    print("create_OGs_table_and_OG_2_Function_table_and_Functions_table_DOM")
    # taxid = "2"
    fn_ogs = os.path.join(STATIC_DIR, "OGs_table_static.txt")
    fn_og_2_func = os.path.join(STATIC_DIR, "OG_2_Function_table_static.txt")
    # fn_func_KEGG = os.path.join(TABLES_DIR, "Functions_table_KEGG_static.txt")
    fn_func_DOM = os.path.join(STATIC_DIR, "Functions_table_DOM_static.txt") # temporary --> merged into Functions_table.txt, therefore not saved
    function_dom_set = set()
    # an_kegg_set = set()
    with open(fn_ogs, "w") as fh_ogs:
        with open(fn_og_2_func, "w") as fh_og_2_func:
            # with open(fn_func_KEGG, "w") as fh_func_KEGG:
            with open(fn_func_DOM, "w") as fh_func_DOM:
                for entry in yield_entry_from_all_annotations():
                    og_name, description, go, KEGG, domains = entry
                    # OGs_table_static.txt
                    # og, taxid, description (taxid = 2 for all bacterial OGs)
                    if description != "NA":
                        # line2write_ogs = og_name + "\t" + taxid + "\t" + description + "\n"
                        line2write_ogs = og_name + "\t" + description + "\n"
                        fh_ogs.write(line2write_ogs)

                    functions, pw_name_num = parse_functions(go, KEGG, domains)
                    functions = set(functions)  # remove redundancies
                    # OG_2_Function_table_static.txt
                    # og, function
                    for function_ in functions:
                        line2write_og_2_func = og_name + "\t" + function_ + "\n"
                        fh_og_2_func.write(line2write_og_2_func)

                    # Functions_table_KEGG_static.txt # obsolete here, since using resource from Lars's frozen KEGG version
                    # type_, description, an
                    # type_ = "KEGG"
                    # for name_num in pw_name_num:
                    #     pw_name, pw_num = name_num
                    #     description_ = pw_name
                    #     an_ = pw_num
                    #     if not an_ in an_kegg_set:
                    #         line2write_func_KEGG = type_ + "\t" + description_ + "\t" + an_ + "\n"
                    #         fh_func_KEGG.write(line2write_func_KEGG)
                    #         an_kegg_set.update([an_])

                    type_ = "DOM"  # this is a bit stupid, since redundant info see DataBase_schema.md
                    for function_ in functions:
                        function_split = function_.split(":")
                        description_ = function_split[1]
                        if function_split[0] == "DOM":
                            if not function_ in function_dom_set:
                                line2write_func_KEGG = type_ + "\t" + description_ + "\t" + function_ + "\n"
                                # fh_func_KEGG.write(line2write_func_KEGG)
                                fh_func_DOM.write(line2write_func_KEGG)
                                function_dom_set.update([function_])

def read_until(fh, start):
    """
    # read each line until it has a certain start, and then puts
    # the start tag back
    """
    while 1:
        pos = fh.tell()
        line = fh.readline()
        if not line:
            break
        if line.startswith(start):
            fh.seek(pos)
            return
    raise EOFError("%s tag cannot be found" % start)

def after_colon(line):
    # macro for getting anything after the :
    return line.split(":", 1)[1].strip()

##### Child_2_Parent_table_UPK.txt, Functions_table_UPK.txt and Function_2_definition_table_UPK.txt
def create_Child_2_Parent_table_UPK__and__Functions_table_UPK__and__Function_2_definition_UPK():
    """
    id_, name --> Functions_table.txt
    id_, is_a_list --> UPKChild_2_UPKParent_table.txt
    :return:
    """
    print("create_Child_2_Parent_table_UPK__and__Functions_table_UPK__and__Function_2_definition_UPK")
    fn = os.path.join(DOWNLOADS_DIR, "keywords-all.obo")
    obo = OBOReader_2_text(fn)
    fn_child2parent = os.path.join(TABLES_DIR, "Child_2_Parent_table_UPK.txt")
    fn_funcs = os.path.join(TABLES_DIR, "Functions_table_UPK.txt")
    # type_ = "UPK"
    etype = "-51"
    # fn_descr = os.path.join(TABLES_DIR, "Function_2_definition_table_UPK.txt")
    with open(fn_funcs, "w") as fh_funcs:
        with open(fn_child2parent, "w") as fh_child2parent:
            # with open(fn_descr, "w") as fh_descr:
            for entry in obo:
                id_, name, is_a_list, definition = entry
                id_ = id_.replace("KW-", "UPK:")
                # line2write_func = type_ + "\t" + name + "\t" + id_ + "\n"
                # line2write_func = type_ + "\t" + name + "\t" + id_ + "\t" + definition + "\n"
                line2write_func = etype + "\t" + name + "\t" + id_ + "\t" + definition + "\n"
                fh_funcs.write(line2write_func)
                for parent in is_a_list:
                    parent = parent.replace("KW-", "UPK:")
                    line2write_cp = id_ + "\t" + parent + "\n"
                    fh_child2parent.write(line2write_cp)
                # line2write_descr = id_ + "\t" + definition + "\n"
                # fh_descr.write(line2write_descr)

##### Child_2_Parent_table_GO.txt, Functions_table_GO.txt and Function_2_definition_table_GO.txt
def create_Child_2_Parent_table_GO__and__Functions_table_GO__and__Function_2_definition_GO():
    """
    id_, name --> Functions_table.txt
    id_, is_a_list --> Child_2_Parent_table_GO.txt
    :return:
    """
    print("create_Child_2_Parent_table_GO__and__Functions_table_GO__and__Function_2_definition_GO")
    fn = os.path.join(DOWNLOADS_DIR, "go-basic.obo")
    obo = OBOReader_2_text(fn)
    GO_dag = obo_parser.GODag(obo_file=os.path.join(DOWNLOADS_DIR, "go-basic.obo"), upk=False)
    fn_child2parent = os.path.join(TABLES_DIR, "Child_2_Parent_table_GO.txt")
    fn_funcs = os.path.join(TABLES_DIR, "Functions_table_GO.txt")
    # type_ = "GO"
    # fn_descr = os.path.join(TABLES_DIR, "Function_2_definition_table_GO.txt")
    with open(fn_funcs, "w") as fh_funcs:
        with open(fn_child2parent, "w") as fh_child2parent:
            # with open(fn_descr, "w") as fh_descr:
            for entry in obo:
                id_, name, is_a_list, definition = entry
                # line2write_func = type_ + "\t" + name + "\t" + id_ + "\t" + definition + "\n"
                etype =  get_entity_type_from_GO_term(id_, GO_dag)
                line2write_func = etype + "\t" + name + "\t" + id_ + "\t" + definition + "\n"
                fh_funcs.write(line2write_func)
                for parent in is_a_list:
                    parent = parent.replace("KW-", "UPK:")
                    line2write_cp = id_ + "\t" + parent + "\n"
                    fh_child2parent.write(line2write_cp)
                # line2write_descr = id_ + "\t" + definition + "\n"
                # fh_descr.write(line2write_descr)

def get_parents_iterative(child, child_2_parent_dict):
    """
    par = {"C22":{"C1"}, "C21":{"C1"}, "C1":{"P1"}}
    get_parents_iterative("C22", par)
    """
    if child not in child_2_parent_dict:
        return []
    # important to set() otherwise parent is updated in orig object
    all_parents = set(child_2_parent_dict[child])
    current_parents = set(all_parents)
    while len(current_parents) > 0:
        new_parents = set()
        for parent in current_parents:
            if parent in child_2_parent_dict:
                temp_parents = child_2_parent_dict[parent].difference(all_parents)
                all_parents.update(temp_parents)
                new_parents.update(temp_parents)
        current_parents = new_parents
    return all_parents

##### Ontologies_table
def create_Ontologies_table(fn_list, fn_out):
    """
    get all parents for each node/child, set Boolean if direct or indirect
    :param fn_list: RawString(each with direct child to parent relationship)
    :param fn_out: RawString
    :return: None
    """
    print("create_Ontologies_table")
    child_2_parent_dict = {}  # key=child, val=SetOfString
    for fn in fn_list:
        with open(fn, 'r') as fh:
            for line in fh:
                child, parent = line.strip().split("\t")
                if not child in child_2_parent_dict:
                    child_2_parent_dict[child] = set([parent])
                else:
                    child_2_parent_dict[child].update([parent])

    with open(fn_out, "w") as fh_out:
        for child in sorted(child_2_parent_dict.keys()):
            parents_set = get_parents_iterative(child, child_2_parent_dict)
            entity_type_num = get_entity_type_number_from_parents_set(parents_set)
            for parent in parents_set:
                if parent in child_2_parent_dict[child]:
                    line2write = child + "\t" + parent + "\t" + "1" + "\t" + entity_type_num + "\n"  # direct parent
                    fh_out.write(line2write)
                else:
                    line2write = child + "\t" + parent + "\t" + "0" + "\t" + entity_type_num + "\n"  # indirect parent
                    fh_out.write(line2write)

def get_entity_type_number_from_parents_set(parents_set):
    """
    based on child column of Ontologies table, determine the entity type
     GO terms will have one of three parents
     UPK unfortunately multiple top parents possible
     if conversion to Integer possible, then TaxID
     if DOID: in all parents, then Disease
    :param parents_set: SetOfString
    :return: String
    """
    key = list(parents_set.intersection(id_2_entityTypeNumber_dict_keys_set))
    if len(key) == 1:
        return id_2_entityTypeNumber_dict[key[0]]
    elif len(key) > 1:  # can happen for UPK
        return id_2_entityTypeNumber_dict[key[0]]
    else:
        # check if convertable to Integers --> TaxID
        try:
            [int(ele) for ele in parents_set]
            return "-3"  # for TaxID
        except ValueError:
            if sum([ele.startswith("DOID:") for ele in parents_set]) == len(parents_set):
                return "-26"  # Diseases
    return "-99"

def concatenate_files(fn_list, fn_out):
    with open(fn_out, "w") as fh_out:
        for fn in fn_list:
            with open(fn, "r") as fh_in:
                for line in fh_in:
                    fh_out.write(line)

##### Protein_2_Funtion_table.txt
# for UniProt AccessionNumbers, UniProt-Keywords and GO-terms
# HOMD ANs are mapped via OGs

# def parse_goa_gaf(fn_in, fn_out, taxid_2_ignore_set=None, protein_2_taxid=False, an_set=None):  # dependency
def parse_goa_gaf(fn_in, fn_out, functions_set, taxid_2_ignore_set=None):
    """
    parse UniProt goa_ref file, write to table.txt for SQL
    restrict to taxid_2_ignore_set (TaxIDs as String) if provided
    also restrict to Functional annotations (GO-terms and UniProt-keywords) that are present in OBO-files)
    :param fn_in: raw String
    :param fn_out: raw String
    :param functions_set: Set of Strings (Functional annotations (GO-terms and UniProt-keywords) that are present in OBO)
    :param taxid_2_ignore_set: SetOfString (flag to skip TaxIDs)
    :return: None
    """
    with open(fn_out, "w") as fh_out:
        for line in yield_line_uncompressed_or_gz_file(fn_in):
            if line[0] == "!":
                continue
            else:
                line_split = line.split("\t")
                if len(line_split) >= 15:
                    an = line_split[1]  # DB_Object_ID
                    goid = line_split[4]  # GO_ID
                    if goid not in functions_set:
                        continue
                    taxid = re.match(r"taxon:(\d+)", line_split[12]).groups()[0]
                    # reduce to specific TaxIDs
                    if taxid_2_ignore_set is not None:
                        if taxid in taxid_2_ignore_set:
                            continue
                    line2write = an + "\t" + goid + "\n"
                    fh_out.write(line2write)

def get_keyword_2_upkan_dict():
    """
    UniProt-keyword 2 UPK-AccessionNumber
    :return: Dict(String2String)
    """
    fn = os.path.join(TABLES_DIR, 'Functions_table_UPK.txt')
    keyword_2_upkan_dict = {}
    with open(fn, "r") as fh:
        for line in fh:
            line_split = line.strip().split("\t")
            keyword = line_split[1]
            upkan = line_split[2]
            keyword_2_upkan_dict[keyword] = upkan
    return keyword_2_upkan_dict

# def parse_upk(fn_in, fn_out, protein_2_taxid=False, an_set=None):
def parse_upk(fn_in, fn_out, functions_set):
    """
    parse UniProt-Keywords file, write to table.txt for SQL
    :param fn_in: raw String
    :param fn_out: raw String
    :param functions_set: Set of String
    :return: None
    """
    keyword_2_upkan_dict = get_keyword_2_upkan_dict()
    # taxid = os.path.basename(fn_in).replace(".upk", "")
    with open(fn_out, "w") as fh_out:
        # with open(fn_in, "r") as fh_in:
        #     fh_in.next() # skip header
        #     for line in fh_in:
        gen = yield_line_uncompressed_or_gz_file(fn_in)
        next(gen)  # skip header Py3
        for line in gen:
            line_split = line.split('\t')
            an = line_split[0]
            keywords = set([ele.strip() for ele in line_split[-1].split(';')])
            if keywords == {""}:  # !!! is this the proper test?
                continue
            for keyword in keywords:
                try:
                    upk_an = keyword_2_upkan_dict[keyword]
                except KeyError:
                    print("keyword_2_upkan_dict KeyError: {}".format(keyword))
                    continue
                if upk_an not in functions_set:
                    continue
                line2write = an + "\t" + upk_an + "\n"
                fh_out.write(line2write)

def create_Protein_2_Function_table(fn_out_temp, verbose=False):
    """
    check that all associations are in the respective Ontology
    e.g. protein with associations A, B, C but C is not in GOterms Ontology any more, therefore remove the association C from protein
    :return:
    """
    print("create_Protein_2_Function_table")
    fn_list_tables, taxid_list_gaf = [], []
    create_Protein_2_Function_table_KEGG(COLUMN_CROSSREF="kegg")
    fn_list_tables.append(os.path.join(TABLES_DIR, "Protein_2_Function_table_KEGG.txt"))
    fn_list = os.listdir(DOWNLOADS_DIR)
    fn_list = sorted(fn_list)
    if verbose:
        print("#"*80, "parsing START")
    functions_set = get_possible_ontology_functions_set() # GO and UPK not KEGG
    for fn in fn_list:
        if fn.endswith(".gaf"): # do all of these first to collect TaxIDs to ignore when parsing ".gaf.gz"
            taxid = fn.replace(".gaf", "")
            fn_gaf = os.path.join(DOWNLOADS_DIR, fn)
            fn_out = os.path.join(TABLES_DIR, "Protein_2_Function_table_GO_{}.txt".format(taxid))
            fn_list_tables.append(fn_out)
            parse_goa_gaf(fn_gaf, fn_out, functions_set)
            if verbose:
                print(fn, fn_out)
            taxid_list_gaf.append(taxid)  # these TaxIDs have curated/filtered annotations, therefore skip them in unfiltered big file

    for fn in fn_list:
        if fn.endswith(".gaf.gz"):
            taxid = fn.replace(".gaf.gz", "")
            fn_gaf_gz = os.path.join(DOWNLOADS_DIR, fn)
            fn_out = os.path.join(TABLES_DIR, "Protein_2_Function_table_GO_{}.txt".format(taxid))
            if verbose:
                print("Parsing {}".format(fn_gaf_gz))
                print(fn, fn_out)
            fn_list_tables.append(fn_out)
            parse_goa_gaf(fn_gaf_gz, fn_out, functions_set, taxid_2_ignore_set=taxid_list_gaf)

        elif fn.endswith(".upk"):
            taxid = fn.replace(".upk", "")
            fn_upk = os.path.join(DOWNLOADS_DIR, fn)
            fn_out = os.path.join(TABLES_DIR, "Protein_2_Function_table_UPK_{}.txt".format(taxid))
            fn_list_tables.append(fn_out)
            if verbose:
                print(fn, fn_out)
            parse_upk(fn_upk, fn_out, functions_set)

        elif fn.endswith(".upk.gz"):
            taxid = fn.replace(".upk.gz", "")
            fn_upk = os.path.join(DOWNLOADS_DIR, fn)
            fn_out = os.path.join(TABLES_DIR, "Protein_2_Function_table_UPK_{}.txt".format(taxid))
            fn_list_tables.append(fn_out)
            if verbose:
                print(fn, fn_out)
            parse_upk(fn_upk, fn_out, functions_set)
    if verbose:
        print("#" * 90, "parsing STOP")

    # fn_out_temp = os.path.join(TABLES_DIR, "Protein_2_Function_table_temp.txt")
    if verbose:
        print("concatenate_files")
        # print(fn_list_tables, fn_out_temp)
    concatenate_files(fn_list_tables, fn_out_temp)

def create_Protein_2_Function_table_wide_format(verbose=False):
    fn_out_temp = os.path.join(TABLES_DIR, "Protein_2_Function_table_temp.txt")
    fn_out = os.path.join(TABLES_DIR, "Protein_2_Function_table.txt")
    create_Protein_2_Function_table(fn_out_temp, verbose)
    if verbose:
        print("converting Protein_2_Function_table to wide format")
    if PLATFORM == "linux":
        shellcmd = "LC_ALL=C sort --parallel {} {} -o {}".format(NUMBER_OF_PROCESSES, fn_out_temp, fn_out_temp)  # sort in-place on first column which is protein_AN # was gsort previously
    else:
        shellcmd = "LC_ALL=C gsort --parallel {} {} -o {}".format(NUMBER_OF_PROCESSES, fn_out_temp, fn_out_temp)  # sort in-place on first column which is protein_AN # was gsort previously

    if verbose:
        print(shellcmd)
    call(shellcmd, shell=True)
    long_2_wide_format(fn_out_temp, fn_out)
    if verbose:
        print("done Protein_2_Function_table")

def long_2_wide_format(fn_in, fn_out, etype=None):
    function_list = []
    with open(fn_in, "r") as fh_in:
        with open(fn_out, "w") as fh_out:
            an_last, function_ = fh_in.readline().strip().split("\t")
            function_list.append(function_)
            for line in fh_in:
                an, function_ = line.strip().split("\t")
                if an == an_last:
                    function_list.append(function_)
                else:
                    if etype is None:
                        fh_out.write(an_last + "\t{" + ','.join('"' + item + '"' for item in set(function_list)) + "}\n")
                    else:
                        fh_out.write(an_last + "\t{" + ','.join('"' + item + '"' for item in set(function_list)) + "}\t" + etype + "\n")

                    function_list = []
                    an_last = an
                    function_list.append(function_)
            # fh_out.write(an + "\t{" + ','.join('"' + item + '"' for item in set(function_list)) + "}\n")
            if etype is None:
                fh_out.write(an + "\t{" + ','.join('"' + item + '"' for item in set(function_list)) + "}\n")
            else:
                fh_out.write(an + "\t{" + ','.join('"' + item + '"' for item in set(function_list)) + "}\t" + etype + "\n")

def parse_secondary_AccessionNumbers(fn):
    line_generator = yield_line_uncompressed_or_gz_file(fn)
    line = next(line_generator)
    while not line.startswith("Secondary AC"):
        line = next(line_generator)
        continue
    _ = next(line_generator)
    for line in line_generator:
        secondary, primary = line.strip().split()
        yield secondary, primary

def create_Protein_Secondary_2_Primary_AN():
    fn_in = os.path.join(DOWNLOADS_DIR, "sec_ac.txt")
    fn_out = os.path.join(TABLES_DIR, "Protein_Secondary_2_Primary_AN_table.txt")
    gen = parse_secondary_AccessionNumbers(fn_in)
    with open(fn_out, "w") as fh:
        for secondary, primary in gen:
            line_2_write = secondary + "\t" + primary + "\n"
            fh.write(line_2_write)

##### GO_2_Slim_table.txt
def create_GO_2_Slim_table(fn_out=None):
    print("create_GO_2_Slim_table")
    fn = os.path.join(DOWNLOADS_DIR, "goslim_generic.obo")
    obo = OBOReader_2_text(fn)
    if fn_out is None:
        fn_out = os.path.join(TABLES_DIR, "GO_2_Slim_table.txt")
    with open(fn_out, "w") as fh_out:
        for entry in obo:
            id_, name, is_a_list, definition = entry
            line2write = id_ + "\t" + "1" + "\n"
            fh_out.write(line2write)

def find_tables_to_remove():
    files_2_remove_list = []
    for fn in os.listdir(TABLES_DIR):
        if not fnmatch.fnmatch(fn, "*_table.txt") and fnmatch.fnmatch(fn, "*.txt"):
            files_2_remove_list.append(os.path.join(TABLES_DIR, fn))
    return files_2_remove_list

def remove_files(fn_list):
    for fn in fn_list:
        if fn in FILES_NOT_2_DELETE:
            continue
        else:
            os.remove(fn)

def parse_kegg_prot_2_path_file_to_dict(fn):
    """
    fn_psm = r"/home/green1/dblyon/kegg_prot_2_path_dict_file.txt"
    kegg_prot_2_path_dict = parse_kegg_prot_2_path_file_to_dict(fn)
    """
    kegg_prot_2_path_dict = {}
    with open(fn, "r") as fh:
        for line in fh:
            prot_an, path_an = line.strip().split("\t")
            kegg_prot_2_path_dict[prot_an] = path_an.split(";")
    return kegg_prot_2_path_dict

def get_df_UniProt_2_KEGG_mapping(fn, COLUMN_CROSSREF): #!!! does this file look the way it should???
    """
    fn = r"/Users/dblyon/modules/cpr/metaprot/sql/downloads/UniProt_2_KEGG_mapping.tab"
    COLUMN_CROSSREF="Cross-reference (KEGG)"
    df = get_df_UniProt_2_KEGG_mapping(fn, COLUMN_CROSSREF)
    """
    df = pd.read_csv(fn, sep='\t')
    # 3 letter code KEGG abbreviation
    df["Abb"] = df[COLUMN_CROSSREF].apply(lambda s: s[0:3])
    df.sort_values(["Abb", COLUMN_CROSSREF], inplace=True)
    return df

def create_Protein_2_Function_table_KEGG(fn_in=None, COLUMN_CROSSREF="Cross-reference (KEGG)"):
    """
    ##### map UniProt AN to KEGG pathways
    ### use UniProt mapping from UniProt protein AN to KEGG protein AN
    ### map KEGG protein AN to KEGG pathway AN via Lars's download of last freely available KEGG:
    ### home/purple1/databases/KEGG/genes/organisms/Specific3CharFolder/*_pathway.list --> parsed into kegg_prot_2_path_dict
    ### map pathway an to pathway name via:
    ###  /home/purple1/databases/KEGG/pathway/pathway.list
    ################################################################################################################
    ##### flow
    an = "P31946"

    UniProt_2_KEGG_mapping.tab
    -->
    "hsa:7529"

    /home/purple1/databases/KEGG/genes/organismns/hsa/hsa_pathways.list
    -->
    hsa:7529    path:hsa04110
    hsa:7529    path:hsa04114
    hsa:7529    path:hsa04722

    # create Protein_2_Function_table_KEGG.txt
    an = "P31946"
    function = "KEGG:04110"

    # create
    /home/purple1/databases/KEGG/pathway/pathway.list
    -->
    04110    Cell cycle
    ################################################################################################################
    # check if Functions_table_KEGG_static.txt is equal or subset of pathway.list
    # add KEGG pathway.list to functions table if not existing yet, or rather only use the this resource and not

    fn_psm = "Protein_2_Function_table_KEGG.txt"
    fn = r"/Users/dblyon/modules/cpr/metaprot/sql/downloads/UniProt_2_KEGG_mapping.tab"
    df_up_2_kegg = get_df_UniProt_2_KEGG_mapping(fn, COLUMN_CROSSREF="Cross-reference (KEGG)")

    kegg_prot_2_path_dict = parse_kegg_prot_2_path_file_to_dict(fn)
    kegg_prot_2_path_dict: key=String(KEGG_protein_an), val=ListOfString(KEGG_path_an)

    # DEBUG:
    no KEGG associations for given protein AN from mouse SwissProt entry
    entity_type = "KEGG"
    limit_2_parent = None
    basic_or_slim = "basic"
    protein_ans_list = ["Q6DFV6"]
    assoc_dict = query.get_association_dict(connection, protein_ans_list, entity_type, limit_2_parent, basic_or_slim)
    assoc_dict

    but AN in mapping
    grep "Q6DFV6" UniProt_2_KEGG_mapping.tab
    --> Q6DFV6    mmu:333564;

    e.g. DEBUG usage
    import create_SQL_tables as cst
    DOWNLOADS_DIR = r"/Volumes/Speedy/PostgreSQL/downloads"
    COLUMN_CROSSREF="Cross-reference (KEGG)"
    fn = os.path.join(DOWNLOADS_DIR, "UniProt_2_KEGG_mapping.tab")
    df_up_2_kegg = cst.get_df_UniProt_2_KEGG_mapping(fn, COLUMN_CROSSREF)
    fn = os.path.join(DOWNLOADS_DIR, "KEGG_prot_2_path_dict_static.txt")
    kegg_prot_2_path_dict = cst.parse_kegg_prot_2_path_file_to_dict(fn)
    an = "Q6DFV6"
    kegg_an = df_up_2_kegg.loc[df_up_2_kegg["Entry"] == an, "Cross-reference (KEGG)"].values[0].split(";")[0]
    print kegg_an
    print kegg_prot_2_path_dict[kegg_an] # --> key error
    """
    if fn_in is None:
        fn_in = os.path.join(DOWNLOADS_DIR, "UniProt_2_KEGG_mapping.tab")
    df_up_2_kegg = get_df_UniProt_2_KEGG_mapping(fn_in, COLUMN_CROSSREF)
    # column_crossref_index = df_up_2_kegg.columns.tolist().index(COLUMN_CROSSREF) + 1

    fn = os.path.join(STATIC_DIR, "KEGG_prot_2_path_dict_static.txt")
    kegg_prot_2_path_dict = parse_kegg_prot_2_path_file_to_dict(fn)

    fn_out = os.path.join(TABLES_DIR, "Protein_2_Function_table_KEGG.txt")
    with open(fn_out, "w") as fh:
        for row in df_up_2_kegg.itertuples():
            # up_an = row.Entry
            up_an = row[1]
            # kegg_prot_ans_string = row[column_crossref_index]
            kegg_prot_ans_string = row[2]

            ## three_char_KEGG_code = row["Abb"]
            # potentially multiple Cross-referenced KEGG protein ANs
            # kegg_prot_ans_string = row[COLUMN_CROSSREF]
            # and for each KEGG protein AN, potentially multiple KEGG pathway ANs
            kegg_prot_ans_list = [ele for ele in kegg_prot_ans_string.split(";") if len(ele) > 0]
            for kegg_prot in kegg_prot_ans_list:
                try:
                    kegg_path_an_list = kegg_prot_2_path_dict[kegg_prot]
                except KeyError:
                    continue
                for kegg_path in kegg_path_an_list:
                    string_2_write = up_an + "\t" + "KEGG:{}".format(kegg_path[3:]) + "\n"
                    fh.write(string_2_write)

def create_Functions_table_KEGG(fn_in=None, fn_out=None, verbose=True):
    # NOT static for STRING
    # static for aGOtool (at least CPR version hosted @ ku.sund.dk)
    # type_ = "KEGG"
    # etype = "-52"
    etype = id_2_entityTypeNumber_dict["KEGG"]
    placeholder_for_definition = ""
    if fn_in is None:
        fn_in = os.path.join(STATIC_DIR, "KEGG_AN_2_Pathway_static.txt")
    if fn_out is None:
        fn_out = os.path.join(STATIC_DIR, "Functions_table_KEGG_static.txt")
    if verbose:
        print("creating {} ".format(fn_out))
    with open(fn_out, "w") as fh_out:
        with open(fn_in, "r") as fh_in:
            for line in fh_in:
                if line.startswith("#"):
                    continue
                an, name = line.strip().split("\t")
                an = "KEGG:" + an
                # string_2_write = type_ + "\t" + name + "\t" + an + "\t"+ placeholder_for_definition + "\n"
                # | etype | name | an | definition |
                string_2_write = etype + "\t" + name + "\t" + an + "\t"+ placeholder_for_definition + "\n"
                fh_out.write(string_2_write)

def get_possible_ontology_functions_set():
    fn = os.path.join(TABLES_DIR, "Ontologies_table.txt")
    df = pd.read_csv(fn, sep='\t', header=None)
    functions_set = set(df[0].tolist() + df[1].tolist())
    return functions_set

def create_bash_scripts_for_DB_if_not_exits(testing=False, foragotool=False):
    """
    psql -h localhost -d agotool -c "CREATE TABLE function_2_definition (
    an text,
    definition text);"

    psql -h localhost -d agotool -c "COPY function_2_definition FROM '{}';"

    psql -h localhost -d agotool -c "CREATE INDEX function_2_definition_an_idx ON function_2_definition(an);"
    psql -h localhost -d agotool -c "CREATE INDEX functions_an_idx ON functions(an);"
    psql -h localhost -d agotool -c "CREATE INDEX go_2_slim_an_idx ON go_2_slim(an);"
    psql -h localhost -d agotool -c "CREATE INDEX ontologies_child_idx ON ontologies(child);"
    psql -h localhost -d agotool -c "CREATE INDEX ontologies_direct_idx ON ontologies(direct);"
    psql -h localhost -d agotool -c "CREATE INDEX ontologies_type_idx ON ontologies(type);"
    psql -h localhost -d agotool -c "CREATE INDEX protein_secondary_2_primary_an_sec_idx ON protein_secondary_2_primary_an(sec);"

    :return: String(executable bash script)
    """
    global TABLES_DIR
    print("creating bash scripts to for PostgreSQL DB creation")
    if testing:
        TABLES_DIR = TEST_DIR
    functions_table = os.path.join(TABLES_DIR, "Functions_table.txt")
    # function_2_definition_table = os.path.join(TABLES_DIR, "Function_2_definition_table.txt")
    go_2_slim_table = os.path.join(TABLES_DIR, "GO_2_Slim_table.txt")
    og_2_function_table = os.path.join(STATIC_DIR, "OG_2_Function_table_static.txt")
    ogs_table = os.path.join(STATIC_DIR, "OGs_table_static.txt")
    ontologies_table = os.path.join(TABLES_DIR, "Ontologies_table.txt")
    protein_2_function_table = os.path.join(TABLES_DIR, "Protein_2_Function_table.txt")
    protein_2_og_table = os.path.join(STATIC_DIR, "Protein_2_OG_table_static.txt")
    protein_secondary_2_primary_an_table = os.path.join(TABLES_DIR, "Protein_Secondary_2_Primary_AN_table.txt")

    if not foragotool:
        postgres_commands = '''#!{}
psql -h localhost -d postgres -c "DROP DATABASE agotool;"
psql -h localhost -d postgres -c "CREATE DATABASE agotool;"

psql -h localhost -d agotool -c "CREATE TABLE functions (
    type text,
    name text,
    an text,
    definition text);"
psql -h localhost -d agotool -c "CREATE TABLE go_2_slim (
    an text,    
    slim boolean);"
psql -h localhost -d agotool -c "CREATE TABLE ogs (
    og text,    
    description text);"
psql -h localhost -d agotool -c "CREATE TABLE og_2_function (
    og text,
    function text);"
psql -h localhost -d agotool -c "CREATE TABLE ontologies (
    child text,
    parent text,
    direct boolean,
    type integer);"
psql -h localhost -d agotool -c "CREATE TABLE protein_2_function (
    an text,
    function text ARRAY);"    
psql -h localhost -d agotool -c "CREATE TABLE protein_secondary_2_primary_an (
    sec text,
    pri text);"
psql -h localhost -d agotool -c "CREATE TABLE protein_2_og (
    an text,
    og text);"

psql -h localhost -d agotool -c "COPY functions FROM '{}';"
psql -h localhost -d agotool -c "COPY go_2_slim FROM '{}';"
psql -h localhost -d agotool -c "COPY ogs FROM '{}';"
psql -h localhost -d agotool -c "COPY og_2_function FROM '{}';"
psql -h localhost -d agotool -c "COPY ontologies FROM '{}';"
psql -h localhost -d agotool -c "COPY protein_2_function FROM '{}';"
psql -h localhost -d agotool -c "COPY protein_secondary_2_primary_an FROM '{}';"
psql -h localhost -d agotool -c "COPY protein_2_og FROM '{}';"

psql -h localhost -d agotool -c "CREATE INDEX ogs_og_idx ON ogs(og);"
psql -h localhost -d agotool -c "CREATE INDEX og_2_function_og_idx ON og_2_function(og);"
psql -h localhost -d agotool -c "CREATE INDEX protein_2_function_an_idx ON protein_2_function(an);"
psql -h localhost -d agotool -c "CREATE INDEX protein_2_og_an_idx ON protein_2_og(an);"'''.format(BASH_LOCATION,
        functions_table, go_2_slim_table,
        ogs_table, og_2_function_table, ontologies_table,
        protein_2_function_table, protein_secondary_2_primary_an_table, protein_2_og_table)
    else: #sudo -u postgres
        postgres_commands = '''#!{}
psql -d postgres -c "DROP DATABASE agotool;"
sudo -u postgres psql postgres -c "CREATE DATABASE agotool OWNER dblyon;"

psql -d agotool -c "CREATE TABLE functions (
    type text,
    name text,
    an text,
    definition text);"
psql -d agotool -c "CREATE TABLE go_2_slim (
    an text,    
    slim boolean);"
psql -d agotool -c "CREATE TABLE ogs (
    og text,    
    description text);"
psql -d agotool -c "CREATE TABLE og_2_function (
    og text,
    function text);"
psql -d agotool -c "CREATE TABLE ontologies (
    child text,
    parent text,
    direct boolean,
    type integer);"
psql -d agotool -c "CREATE TABLE protein_2_function (
    an text,
    function text ARRAY);"    
psql -d agotool -c "CREATE TABLE protein_secondary_2_primary_an (
    sec text,
    pri text);"
psql -d agotool -c "CREATE TABLE protein_2_og (
    an text,
    og text);"

psql -d agotool -c "\copy functions FROM '{}';"
psql -d agotool -c "\copy go_2_slim FROM '{}';"
psql -d agotool -c "\copy ogs FROM '{}';"
psql -d agotool -c "\copy og_2_function FROM '{}';"
psql -d agotool -c "\copy ontologies FROM '{}';"
psql -d agotool -c "\copy protein_2_function FROM '{}';"
psql -d agotool -c "\copy protein_secondary_2_primary_an FROM '{}';"
psql -d agotool -c "\copy protein_2_og FROM '{}';"

psql -d agotool -c "CREATE INDEX ogs_og_idx ON ogs(og);"
psql -d agotool -c "CREATE INDEX og_2_function_og_idx ON og_2_function(og);"
psql -d agotool -c "CREATE INDEX protein_2_function_an_idx ON protein_2_function(an);"
psql -d agotool -c "CREATE INDEX protein_2_og_an_idx ON protein_2_og(an);"
sudo -u postgres psql agotool -c "CREATE USER agotool;"
sudo -u postgres psql agotool -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO agotool;"'''.format(BASH_LOCATION, functions_table, go_2_slim_table,
            ogs_table, og_2_function_table, ontologies_table, protein_2_function_table, protein_secondary_2_primary_an_table, protein_2_og_table)

    if testing:
        postgres_commands = postgres_commands.replace(" agotool", " agotool_test")

    fn_out = os.path.join(POSTGRESQL_DIR, "fn_create_DB_copy_and_index_tables.sh")
    with open(fn_out, "w") as fh:
        fh.write(postgres_commands)
    shellcmd = "chmod 744 {}".format(fn_out)
    call(shellcmd, shell=True)
    return fn_out

def create_psql_script_copy_from_file_and_index(testing=True, execute_cmd_via_python=False):
    """
    removed the following deprecated statements:
    '''
    psql -d postgres -c "DROP DATABASE agotool;"
    sudo -u postgres psql postgres -c "CREATE DATABASE agotool OWNER dblyon;"
    ...
    sudo -u postgres psql agotool -c "CREATE USER agotool;"
    sudo -u postgres psql agotool -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO agotool;
    '''
    :return: String(executable bash script)
    """
    global TABLES_DIR
    print("creating psql scripts for PostgreSQL: copy from file and index")
    if testing:
        TABLES_DIR = TEST_DIR
    functions_table = os.path.join(TABLES_DIR, "Functions_table.txt")
    go_2_slim_table = os.path.join(TABLES_DIR, "GO_2_Slim_table.txt")
    og_2_function_table = os.path.join(STATIC_DIR, "OG_2_Function_table_static.txt")
    ogs_table = os.path.join(STATIC_DIR, "OGs_table_static.txt")
    ontologies_table = os.path.join(TABLES_DIR, "Ontologies_table.txt")
    protein_2_function_table = os.path.join(TABLES_DIR, "Protein_2_Function_table.txt")
    protein_2_og_table = os.path.join(STATIC_DIR, "Protein_2_OG_table_static.txt")
    protein_secondary_2_primary_an_table = os.path.join(TABLES_DIR, "Protein_Secondary_2_Primary_AN_table.txt")

    postgres_commands = '''#!{}
psql -d agotool -c "CREATE TABLE functions_temp (
    type text,
    name text,
    an text,
    definition text);"
psql -d agotool -c "CREATE TABLE go_2_slim_temp (
    an text,    
    slim boolean);"
psql -d agotool -c "CREATE TABLE ogs_temp (
    og text,    
    description text);"
psql -U postgres -d agotool -c "CREATE TABLE og_2_function_temp (
    og text,
    function text);"
psql -U postgres -d agotool -c "CREATE TABLE ontologies_temp (
    child text,
    parent text,
    direct boolean,
    type integer);"
psql -U postgres -d agotool -c "CREATE TABLE protein_2_function_temp (
    an text,
    function text ARRAY);"    
psql -U postgres -d agotool -c "CREATE TABLE protein_secondary_2_primary_an_temp (
    sec text,
    pri text);"
psql -U postgres  -d agotool -c "CREATE TABLE protein_2_og_temp (
    an text,
    og text);"

psql -d agotool -c "\copy functions_temp FROM '{}';"
psql -d agotool -c "\copy go_2_slim_temp FROM '{}';"
psql -d agotool -c "\copy ogs_temp FROM '{}';"
psql -d agotool -c "\copy og_2_function_temp FROM '{}';"
psql -d agotool -c "\copy ontologies_temp FROM '{}';"
psql -d agotool -c "\copy protein_2_function_temp FROM '{}';"
psql -d agotool -c "\copy protein_secondary_2_primary_an_temp FROM '{}';"
psql -d agotool -c "\copy protein_2_og_temp FROM '{}';"

psql -d agotool -c "CREATE INDEX ogs_og_idx_temp ON ogs_temp(og);"
psql -d agotool -c "CREATE INDEX og_2_function_og_idx_temp ON og_2_function_temp(og);"
psql -d agotool -c "CREATE INDEX protein_2_function_an_idx_temp ON protein_2_function_temp(an);"
psql -d agotool -c "CREATE INDEX protein_2_og_an_idx_temp ON protein_2_og_temp(an);"'''.format(BASH_LOCATION, functions_table, go_2_slim_table,
            ogs_table, og_2_function_table, ontologies_table,
            protein_2_function_table, protein_secondary_2_primary_an_table, protein_2_og_table)

    if testing:
        postgres_commands = postgres_commands.replace(" agotool", " agotool_test")

    fn_out = os.path.join(POSTGRESQL_DIR, "fn_create_temp_tables_copy_and_index.psql")
    with open(fn_out, "w") as fh:
        fh.write(postgres_commands)

    if execute_cmd_via_python:
        shellcmd = "chmod 744 {}".format(fn_out)
        call(shellcmd, shell=True)

    return fn_out

def create_psql_script_drop_old_tables_rename_temp_tables_and_indices(testing=True, execute_cmd_via_python=False):
    """
    --> everything is in drop_and_rename.psql #!!!
    """
    # global TABLES_DIR
    print("creating psql scripts for PostgreSQL: drop old tables and rename temp-tables and indices")
    # if testing:
    #     TABLES_DIR = TEST_DIR

    postgres_commands = """DROP TABLE IF EXISTS functions, go_2_slim, ogs, og_2_function, ontologies, protein_2_function, protein_secondary_2_primary_an, protein_2_og;
ALTER TABLE functions_temp RENAME TO functions;
ALTER TABLE go_2_slim_temp RENAME TO go_2_slim;
ALTER TABLE ogs_temp RENAME TO ogs;
ALTER TABLE og_2_function_temp RENAME TO og_2_function;
ALTER TABLE ontologies_temp RENAME TO ontologies;
ALTER TABLE protein_2_function_temp RENAME TO protein_2_function;
ALTER TABLE protein_secondary_2_primary_an_temp RENAME TO protein_secondary_2_primary_an;
ALTER TABLE protein_2_og_temp RENAME TO protein_2_og;

ALTER INDEX ogs_og_idx_temp RENAME TO ogs_og_idx;
ALTER INDEX og_2_function_og_idx_temp RENAME TO og_2_function_og_idx;
ALTER INDEX protein_2_function_an_idx_temp RENAME TO protein_2_function_an_idx;
ALTER INDEX protein_2_og_an_idx_temp RENAME TO protein_2_og_an_idx;"""

    # if testing:
    #     postgres_commands = postgres_commands.replace(" agotool", " agotool_test")

    fn_out = os.path.join(POSTGRESQL_DIR, "fn_create_temp_tables_copy_and_index.psql")
    with open(fn_out, "w") as fh:
        fh.write(postgres_commands)

    if execute_cmd_via_python:
        shellcmd = "chmod 744 {}".format(fn_out)
        call(shellcmd, shell=True)

    return fn_out

def call_script(BASH_LOCATION, script_fn):
    shellcmd = "{} {}".format(BASH_LOCATION, script_fn)
    print(shellcmd)
    call(shellcmd, shell=True)

def count_line_numbers(fn):
    i = 0 # if file can't be opened
    with open(fn, "r") as fh:
        for i, _ in enumerate(fh):
            pass
    return i + 1

def sanity_check_table_dimensions(testing=False):
    # get all the table and file names to count line numbers
    table_name_2_absolute_path_dict = get_table_name_2_absolute_path_dict(testing)
    fn_list = sorted(table_name_2_absolute_path_dict.values())
    # count previous line numbers
    line_numbers_count_log = os.path.join(LOG_DIRECTORY, "table_line_numbers_count_log.txt")
    try:
        table_name_2_number_of_lines_dict_previous = parse_table_line_numbers_count_log(line_numbers_count_log)
    except FileNotFoundError:
        print("Sanity check for number of lines in PostgreSQL tables could not pass since line_numbers_count_log.txt does not exist.\n")
        return False
    # table_name_2_number_of_lines_dict_previous = parse_table_line_numbers_count_log(line_numbers_count_log)
    with open(line_numbers_count_log, "a+") as fh:
        fh.write("### Current date & time " + time.strftime("%c") + "\n")
        for fn in fn_list:
            lines_count = count_line_numbers(fn)
            basename = os.path.basename(fn)
            fh.write(basename + ": " + str(lines_count) + "\n")
        fh.write("#"*50 + "\n")
    # count current line numbers
    table_name_2_number_of_lines_dict_current = parse_table_line_numbers_count_log(line_numbers_count_log)
    # try:
    #     table_name_2_number_of_lines_dict_current = parse_table_line_numbers_count_log(line_numbers_count_log)
    # except FileNotFoundError:
    #     print("Sanity check for number of lines in PostgreSQL tables could not pass since line_numbers_count_log.txt does not exist.\n")
    #     return False
    # compare line numbers
    if are_current_number_of_lines_larger(table_name_2_number_of_lines_dict_previous, table_name_2_number_of_lines_dict_current):
        print("Sanity check for number of lines in PostgreSQL tables passed.\n")
        return True
    else:
        print("Sanity check for number of lines in PostgreSQL tables DID NOT PASS!!\n")
        return False

def parse_table_line_numbers_count_log(fn):
    table_name_2_number_of_lines_dict = {}
    with open(fn, "r") as fh:
        for line in fh:
            line_split = line.strip().split(": ")
            if len(line_split) == 2:
                table_name, number_lines = line_split
                table_name_2_number_of_lines_dict[table_name] = int(number_lines)
    return table_name_2_number_of_lines_dict

def are_current_number_of_lines_larger(previous_dict, current_dict):
    """
    compare line numbers of tables between updates
    :param current_dict: Dict(key=Strin(TableName), val=Int(NumberOfLines))
    :param previous_dict: Dict(key=Strin(TableName), val=Int(NumberOfLines))
    :return: Bool
    """
    # compare dicts, values should be equal or larger
    for table_name, number_lines_previous in previous_dict.items():
        try:
            number_lines_current = current_dict[table_name]
        except KeyError:
            print("Something went wrong while logging for table_line_numbers_count_log.txt")
            return False
        if number_lines_current - number_lines_previous >= 0:
            pass
        else:
            return False
    return True


if __name__ == "__main__":
    ### aGOtool
    # debug = False
    # testing = False
    # verbose = True
    # run_create_tables_for_PostgreSQL(DEBUG=DEBUG, testing=testing, verbose=verbose)
    # sanity_check_table_dimensions(testing=testing)
    # create_test_tables(num_lines=5000)
    # sanity_check_table_dimensions(testing=False)
    # sanity_check_table_dimensions(testing=True)

    ### STRING
    create_tables_STRING(verbose=True, delete_temp_files=False)
    # fn_in = r"/Users/dblyon/modules/cpr/agotool/data/PostgreSQL/downloads/temp.txt"
    # parse_uniprot_dat_dump_yield_entry(fn_in)
    create_test_tables(50000, TABLES_DIR, version_="STRING")

    # ToDo call "sort" python function instead of repeated code, cleanup
    # ToDo stuff stuff into another Snakemake file