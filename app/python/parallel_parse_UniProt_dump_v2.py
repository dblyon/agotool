# from collections import defaultdict
import os, fileinput, subprocess, sys
import zlib, gzip
import tools, variables
import create_SQL_tables_snakemake as cst
import obo_parser
import random, multiprocessing

from collections import deque
PLATFORM = sys.platform


# def unzip_file(fn_in, fn_out, number_of_processes=4):
#     if PLATFORM == "linux":  # Debian: "Linux"
#         fn_bash_script = "bash_script_pigz.sh"
#         with open(fn_bash_script, "w") as fh:
#             fh.write("#!/usr/bin/env bash\n")
#             shellcmd_1 = "pigz -c -d -p {} {} > {}".format(number_of_processes, fn_in, fn_out)
#             fh.write(shellcmd_1 + "\n")
#         subprocess.call("chmod 744 ./{}".format(fn_bash_script), shell=True)
#         subprocess.call("./{}".format(fn_bash_script), shell=True)
#         os.remove(fn_bash_script)
#     else:
#         tools.gunzip_file(fn_in, fn_out=fn_out)
#
# def split_file_into_chunks_using_delimiter(fn_in, dir_out, num_chunks, recstart, recend):
#     if not os.path.exists(dir_out):
#         os.makedirs(dir_out)
#     size = os.path.getsize(fn_in)
#     positions = sorted([random.randint(0, size) for _ in range(num_chunks)])
#     # for



from multiprocessing import JoinableQueue

from multiprocessing.context import Process


class Renderer:
    queue = None

    def __init__(self, nb_workers=2):
        self.queue = JoinableQueue()
        self.processes = [Process(target=self.upload) for i in range(nb_workers)]
        for p in self.processes:
            p.start()

    def render(self, item):
        self.queue.put(item)

    def upload(self):
        while True:
            item = self.queue.get()
            if item is None:
                break

            # process your item here

            self.queue.task_done()

    def terminate(self):
        """ wait until queue is empty and terminate processes """
        self.queue.join()
        for p in self.processes:
            p.terminate()

# r = Renderer()
# r.render(item1)
# r.render(item2)
# r.terminate()



def Protein_2_Function_table_UniProtDump_UPS(fn_in_Functions_table_UPK, fn_in_obo_GO, fn_in_obo_UPK, fn_in_list_uniprot_dumps, fn_in_interpro_parent_2_child_tree, fn_in_hierarchy_reactome, fn_out_Protein_2_Function_table_UniProt_dump, fn_out_UniProtID_2_ENSPs_2_KEGGs_mapping, fn_out_UniProt_AC_2_ID_2_Taxid, verbose=True):

    # fn_in_list_uniprot_dumps_temp = []
    # for fn_in in fn_in_list_uniprot_dumps:
    #     fn_out = fn_in.replace("gz", "") + ".temp"
    #     fn_in_list_uniprot_dumps_temp.append(fn_out)
    #     unzip_file(fn_in, fn_out, number_of_processes=4)

    fn_in_Functions_table_UPK = os.path.join(variables.TABLES_DIR, "Functions_table_UPK.txt")
    fn_in_obo_GO = os.path.join(variables.DOWNLOADS_DIR, "go-basic.obo")
    fn_in_obo_UPK = os.path.join(variables.DOWNLOADS_DIR, "keywords-all.obo")
    fn_in_interpro_parent_2_child_tree = os.path.join(variables.DOWNLOADS_DIR, "interpro_parent_2_child_tree.txt")
    fn_in_hierarchy_reactome = os.path.join(variables.DOWNLOADS_DIR, "RCTM_hierarchy.tsv")
    etype_UniProtKeywords = variables.id_2_entityTypeNumber_dict["UniProtKeywords"]
    etype_GOMF = variables.id_2_entityTypeNumber_dict['GO:0003674']
    etype_GOCC = variables.id_2_entityTypeNumber_dict['GO:0005575']
    etype_GOBP = variables.id_2_entityTypeNumber_dict['GO:0008150']
    etype_interpro = variables.id_2_entityTypeNumber_dict['INTERPRO']
    etype_pfam = variables.id_2_entityTypeNumber_dict['PFAM']
    etype_reactome = variables.id_2_entityTypeNumber_dict['Reactome']
    GO_dag = obo_parser.GODag(obo_file=fn_in_obo_GO, upk=False)
    UPK_dag = obo_parser.GODag(obo_file=fn_in_obo_UPK, upk=True)
    UPK_Name_2_AN_dict = cst.get_keyword_2_upkan_dict(fn_in_Functions_table_UPK)
    # UPKs_not_in_obo_list, GOterms_not_in_obo_temp = [], []
    child_2_parent_dict_interpro, _ = cst.get_child_2_direct_parents_and_term_2_level_dict_interpro(fn_in_interpro_parent_2_child_tree)
    lineage_dict_interpro = cst.get_lineage_from_child_2_direct_parent_dict(child_2_parent_dict_interpro)
    child_2_parent_dict_reactome = cst.get_child_2_direct_parent_dict_RCTM(fn_in_hierarchy_reactome)


    counter = 0
    num_entries = 1000
    num_workers = 10
    # pool = multiprocessing.Pool(num_workers)
    queue = JoinableQueue()
    entries_2_work = deque()
    # entries_2_work.append()
    for uniprot_dump in fn_in_list_uniprot_dumps:
        for entries in yield_entry_UniProt_dat_dump_parallel(uniprot_dump, num_entries):
            entries_2_work.append(entries)


            stuff = entries, UPK_Name_2_AN_dict, UPK_dag, lineage_dict_interpro, child_2_parent_dict_reactome, GO_dag, etype_UniProtKeywords, etype_GOMF, etype_GOCC, etype_GOBP, etype_interpro, etype_pfam, etype_reactome
            # pool.map(bubu, stuff)
            queue.join(bubu, stuff)





def yield_entry_UniProt_dat_dump_parallel(fn_in, num_entries=100):
    entries = []
    counter = 0
    for entry in cst.yield_entry_UniProt_dat_dump(fn_in):
        entries.append(entry)
        counter += 1
        if counter % num_entries == 0:
            yield entries
            entries = []
    yield entries

def bubu(entries, UPK_Name_2_AN_dict, UPK_dag, lineage_dict_interpro, child_2_parent_dict_reactome, GO_dag, etype_UniProtKeywords, etype_GOMF, etype_GOCC, etype_GOBP, etype_interpro, etype_pfam, etype_reactome):
    for UniProtID, UniProtAC_list, NCBI_Taxid, functions_2_return in parse_uniprot_dat_dump_yield_entry_v2_parallel(entries):
        Keywords_list, GOterm_list, InterPro, Pfam, KEGG, Reactome, STRING, *Proteomes = functions_2_return
        # ['Complete proteome', 'Reference proteome', 'Transcription', 'Activator', 'Transcription regulation', ['GO:0046782'], ['IPR007031'], ['PF04947'], ['vg:2947773'], [], [], ['UP000008770']]
        # for UniProtAN in UniProtAC_and_ID_list:
        if len(Keywords_list) > 0:
            UPK_ANs, UPKs_not_in_obo_temp = cst.map_keyword_name_2_AN(UPK_Name_2_AN_dict, Keywords_list)
            # UPKs_not_in_obo_list += UPKs_not_in_obo_temp
            UPK_ANs, UPKs_not_in_obo_temp = cst.get_all_parent_terms(UPK_ANs, UPK_dag)
            # UPKs_not_in_obo_list += UPKs_not_in_obo_temp
            if len(UPK_ANs) > 0:
                # fh_out.write(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(UPK_ANs)) + "\t" + etype_UniProtKeywords + "\t" + NCBI_Taxid + "\n")
                print(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(UPK_ANs)) + "\t" + etype_UniProtKeywords + "\t" + NCBI_Taxid + "\n")
        if len(GOterm_list) > 0: # do backtracking, split GO into 3 categories and add etype
            GOterm_list, not_in_obo_GO = cst.get_all_parent_terms(GOterm_list, GO_dag)
            # GOterms_not_in_obo_temp += not_in_obo_GO
            MFs, CPs, BPs, not_in_obo_GO = cst.divide_into_categories(GOterm_list, GO_dag, [], [], [], [])
            # GOterms_not_in_obo_temp += not_in_obo_GO
            if MFs:
                # fh_out.write(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(MFs)) + "\t" + etype_GOMF + "\t" + NCBI_Taxid + "\n")  # 'Molecular Function', -23
                print(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(MFs)) + "\t" + etype_GOMF + "\t" + NCBI_Taxid + "\n")  # 'Molecular Function', -23
            if CPs:
                # fh_out.write(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(CPs)) + "\t" + etype_GOCC + "\t" + NCBI_Taxid + "\n")  # 'Cellular Component', -22
                print(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(CPs)) + "\t" + etype_GOCC + "\t" + NCBI_Taxid + "\n")  # 'Cellular Component', -22
            if BPs:
                # fh_out.write(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(BPs)) + "\t" + etype_GOBP + "\t" + NCBI_Taxid + "\n")  # 'Biological Process', -21
                print(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(BPs)) + "\t" + etype_GOBP + "\t" + NCBI_Taxid + "\n")  # 'Biological Process', -21
        if len(InterPro) > 0:
            InterPro_set = set(InterPro)
            for id_ in InterPro:
                InterPro_set.update(lineage_dict_interpro[id_])
            # fh_out.write(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(InterPro_set)) + "\t" + etype_interpro + "\t" + NCBI_Taxid + "\n")
            print(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(InterPro_set)) + "\t" + etype_interpro + "\t" + NCBI_Taxid + "\n")
        if len(Pfam) > 0:
            # fh_out.write(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(Pfam)) + "\t" + etype_pfam + "\t" + NCBI_Taxid + "\n")
            print(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(Pfam)) + "\t" + etype_pfam + "\t" + NCBI_Taxid + "\n")
        if len(Reactome) > 0:
            reactome_list = Reactome.copy()
            for term in reactome_list:
                reactome_list += list(cst.get_parents_iterative(term, child_2_parent_dict_reactome))
            # fh_out.write(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(set(reactome_list))) + "\t" + etype_reactome + "\t" + NCBI_Taxid + "\n")
            print(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(set(reactome_list))) + "\t" + etype_reactome + "\t" + NCBI_Taxid + "\n")

        # translation needed from KEGG identifier to pathway, ID vs AC can be easily distinguished via "_"
        if len(KEGG) > 0:
            # fh_out_UniProtID_2_ENSPs_2_KEGGs_mapping.write(UniProtID + "\t" + ";".join(STRING) + "\t" + ";".join(sorted(set(KEGG))) + "\t" + NCBI_Taxid + "\n")
            print("222_UniProtID_2_ENSPs_2_KEGGs_2_Taxid " + UniProtID + "\t" + ";".join(STRING) + "\t" + ";".join(sorted(set(KEGG))) + "\t" + NCBI_Taxid + "\n")

        for AC in UniProtAC_list:
            # fh_out_UniProt_AC_2_ID_2_Taxid.write("{}\t{}\t{}\n".format(AC, UniProtID, NCBI_Taxid))
            print("111_UniProt_AC_2_ID_2_Taxid {}\t{}\t{}\n".format(AC, UniProtID, NCBI_Taxid))

def parse_uniprot_dat_dump_yield_entry_v2_parallel(entries):
    """
    UniProtKeywords
    GO
    InterPro
    Pfam
    KEGG
    Reactome
    @KEGG : I have a mapping from UniProt accession (e.g. "P31946") to KEGG entry (e.g. "hsa:7529")
        what I'm missing is from KEGG entry to KEGG pathway (e.g.
        hsa:7529    path:hsa04110
        hsa:7529    path:hsa04114
        hsa:7529    path:hsa04722)
    """
    # for entry in yield_entry_UniProt_dat_dump(fn_in):
    for entry in entries:
        UniProtAC_list, Keywords_string, functions_2_return = [], "", []
        Functions_other_list = []
        UniProtID, NCBI_Taxid = "-1", "-1"
        for line in entry:
            try:
                line_code, rest = line.split(maxsplit=1)
            except ValueError:
                continue

            if line_code == "ID":
                UniProtID = rest.split()[0]
            elif line_code == "AC":
                UniProtAC_list += [UniProtAN.strip() for UniProtAN in rest.split(";") if len(UniProtAN) > 0]
            elif line_code == "KW":
                Keywords_string += rest
            elif line_code == "DR":
                Functions_other_list.append(rest)
            elif line_code == "OX":
                # OX   NCBI_TaxID=654924;
                # OX   NCBI_TaxID=418404 {ECO:0000313|EMBL:QAB05112.1};
                if rest.startswith("NCBI_TaxID="):
                    NCBI_Taxid = rest.replace("NCBI_TaxID=", "").split(";")[0].split()[0]

        # UniProtAC_list = sorted(set(UniProtAC_list))Taxid_2_funcEnum_2_scores_table_FIN
        Keywords_list = [cst.cleanup_Keyword(keyword) for keyword in sorted(set(Keywords_string.split(";"))) if len(keyword) > 0]  # remove empty strings from keywords_list
        other_functions = cst.helper_parse_UniProt_dump_other_functions(Functions_other_list)
        # GO, InterPro, Pfam, KEGG, Reactome, STRING, Proteomes
        functions_2_return.append(Keywords_list)
        functions_2_return += other_functions
        # Keywords_list, GO, InterPro, Pfam, KEGG, Reactome, STRING, Proteomes
        #                GO, InterPro, Pfam, KEGG, Reactome, STRING, Proteomes
        yield UniProtID, UniProtAC_list, NCBI_Taxid, functions_2_return



if __name__ == "__main__":
    Protein_2_Function_table_UniProtDump_UPS()
