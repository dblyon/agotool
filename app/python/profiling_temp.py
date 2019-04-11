import pandas as pd
import numpy as np
import os, sys, re
import tarfile

import tools
import create_SQL_tables_snakemake as cst
import variables
import obo_parser



def yield_entry_UniProt_dat_dump(fn_in):
    lines_list = []
    for line in tools.yield_line_uncompressed_or_gz_file(fn_in):
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

def parse_uniprot_dat_dump_yield_entry_v2(fn_in):
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
    for entry in yield_entry_UniProt_dat_dump(fn_in):
        UniProtAN_list, UniProtAN, Keywords_string = [], "", ""
        Functions_other_list = []

        for line in entry:
            try:
                line_code, rest = line.split(maxsplit=1)
            except ValueError:
                continue
            if line_code == "ID":
                UniProtAN_list.append(rest.split()[0])
            elif line_code == "AC":
                UniProtAN_list += [UniProtAN.strip() for UniProtAN in rest.split(";") if len(UniProtAN) > 0]
            elif line_code == "KW":
                Keywords_string += rest
            elif line_code == "DR":
                Functions_other_list.append(rest)
        UniProtAN_list = sorted(set(UniProtAN_list))
        Keywords_list = sorted(set(Keywords_string.split(";")))
        Keywords_list = [cleanup_Keyword(keyword) for keyword in Keywords_list if len(keyword) > 0]  # remove empty strings from keywords_list
        GO, InterPro, Pfam, KEGG, Reactome, STRING = helper_parse_UniProt_dump_other_functions(Functions_other_list)
        yield UniProtAN_list, Keywords_list, GO, InterPro, Pfam, KEGG, Reactome, STRING

def helper_parse_UniProt_dump_other_functions(list_of_string):
    """
    e.g. input
    [['EMBL; AY548484; AAT09660.1; -; Genomic_DNA.'],
     ['RefSeq; YP_031579.1; NC_005946.1.'],
     ['ProteinModelPortal; Q6GZX4; -.'],
     ['SwissPalm; Q6GZX4; -.'],
     ['GeneID; 2947773; -.'],
     ['KEGG; vg:2947773; -.'],
     ['Proteomes; UP000008770; Genome.'],
     ['GO; GO:0046782; P:regulation of viral transcription; IEA:InterPro.'],
     ['InterPro; IPR007031; Poxvirus_VLTF3.'],
     ['Pfam; PF04947; Pox_VLTF3; 1.']]
     EnsemblPlants; AT3G09880.1; AT3G09880.1; AT3G09880.
    """
    GO, InterPro, Pfam, KEGG, Reactome, STRING = [], [], [], [], [], []
    for row in list_of_string:
        row_split = row.split(";")
        func_type = row_split[0]
        try:
            annotation = row_split[1].strip()
        except IndexError:
            continue

        if func_type == "KEGG":
            KEGG.append(annotation)
        elif func_type == "GO":
            GO.append(annotation)
        elif func_type == "InterPro":
            InterPro.append(annotation)
        elif func_type == "Pfam":
            Pfam.append(annotation)
        elif func_type == "Reactome":
            Reactome.append(annotation)
        elif func_type == "STRING":
            funcs_2_return = []
            try:
                for func in [func.strip() for func in row_split[1:]]:
                    if func.endswith("."):
                        func = func[:-1]
                    if func == "-":
                        continue
                    funcs_2_return.append(func)
            except IndexError:
                continue
            STRING += funcs_2_return
    return GO, InterPro, Pfam, KEGG, Reactome, STRING

def Protein_2_Function_table_UniProt_UniProtSpace(fn_in_Functions_table_UPK, fn_in_obo_GO, fn_in_obo_UPK, fn_in_list_uniprot_dumps, fn_in_interpro_parent_2_child_tree, fn_in_hierarchy_reactome, fn_out_Protein_2_Function_table_UniProt_dump, fn_out_UniProt_2_KEGG_mapping, verbose=True):
    if verbose:
        print("\nparsing UniProt dumps: creating 2 output files \n{}\n{}".format(fn_out_Protein_2_Function_table_UniProt_dump, fn_out_UniProt_2_KEGG_mapping))

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
    UPKs_not_in_obo_list, GOterms_not_in_obo_temp = [], []

    child_2_parent_dict_interpro, _ = cst.get_child_2_direct_parents_and_term_2_level_dict_interpro(fn_in_interpro_parent_2_child_tree)
    lineage_dict_interpro = cst.get_lineage_from_child_2_direct_parent_dict(child_2_parent_dict_interpro)

    child_2_parent_dict_reactome = cst.get_child_2_direct_parent_dict_RCTM(fn_in_hierarchy_reactome)
    with open(fn_out_Protein_2_Function_table_UniProt_dump, "w") as fh_out:
        with open(fn_out_UniProt_2_KEGG_mapping, "w") as fh_out_KEGG:
            for uniprot_dump_fn in fn_in_list_uniprot_dumps:
                if verbose:
                    print("parsing {}".format(uniprot_dump_fn))
                for UniProtAC_and_ID_list, KeyWords_list, GOterm_list, InterPro, Pfam, KEGG, Reactome, STRING in parse_uniprot_dat_dump_yield_entry_v2(uniprot_dump_fn):
                    for UniProtAN in UniProtAC_and_ID_list:
                        if len(KeyWords_list) > 0:
                            UPK_ANs, UPKs_not_in_obo_temp = cst.map_keyword_name_2_AN(UPK_Name_2_AN_dict, KeyWords_list)
                            UPKs_not_in_obo_list += UPKs_not_in_obo_temp
                            UPK_ANs, UPKs_not_in_obo_temp = cst.get_all_parent_terms(UPK_ANs, UPK_dag)
                            UPKs_not_in_obo_list += UPKs_not_in_obo_temp
                            if len(UPK_ANs) > 0:
                                fh_out.write(UniProtAN + "\t" + cst.format_list_of_string_2_postgres_array(sorted(UPK_ANs)) + "\t" + etype_UniProtKeywords + "\n")
                        if len(GOterm_list) > 0:  # do backtracking, split GO into 3 categories and add etype
                            GOterm_list, not_in_obo_GO = cst.get_all_parent_terms(GOterm_list, GO_dag)
                            GOterms_not_in_obo_temp += not_in_obo_GO
                            MFs, CPs, BPs, not_in_obo_GO = cst.divide_into_categories(GOterm_list, GO_dag, [], [], [], [])
                            GOterms_not_in_obo_temp += not_in_obo_GO
                            if MFs:
                                fh_out.write(UniProtAN + "\t" + cst.format_list_of_string_2_postgres_array(sorted(MFs)) + "\t" + etype_GOMF + "\n")  # 'Molecular Function', -23
                            if CPs:
                                fh_out.write(UniProtAN + "\t" + cst.format_list_of_string_2_postgres_array(sorted(CPs)) + "\t" + etype_GOCC + "\n")  # 'Cellular Component', -22
                            if BPs:
                                fh_out.write(UniProtAN + "\t" + cst.format_list_of_string_2_postgres_array(sorted(BPs)) + "\t" + etype_GOBP + "\n")  # 'Biological Process', -21
                        if len(InterPro) > 0:
                            InterPro_set = set(InterPro)
                            for id_ in InterPro:
                                InterPro_set.update(lineage_dict_interpro[id_])
                            fh_out.write(UniProtAN + "\t" + cst.format_list_of_string_2_postgres_array(sorted(InterPro_set)) + "\t" + etype_interpro + "\n")
                        if len(Pfam) > 0:
                            fh_out.write(UniProtAN + "\t" + cst.format_list_of_string_2_postgres_array(sorted(Pfam)) + "\t" + etype_pfam + "\n")
                        if len(Reactome) > 0:
                            reactome_list = Reactome.copy()
                            for term in reactome_list:
                                reactome_list += list(cst.get_parents_iterative(term, child_2_parent_dict_reactome))
                            fh_out.write(UniProtAN + "\t" + cst.format_list_of_string_2_postgres_array(sorted(set(reactome_list))) + "\t" + etype_reactome + "\n")

                        # translation needed from KEGG identifier to pathway
                        # ID vs AC can be easily distinguished via "_"
                        if len(KEGG) > 0:
                            fh_out_KEGG.write(UniProtAN + "\t" + ";".join(sorted(set(KEGG))) + "\n")

def UniProt_2_STRING_2_KEGG_from_dump(fn_list_uniprot_dump, fn_out_UniProt_2_STRING_2_KEGG):
    with open(fn_out_UniProt_2_STRING_2_KEGG, "w") as fh_out:
        for uniprot_dump_file in fn_list_uniprot_dump:
            for stuff in parse_uniprot_dat_dump_yield_entry_v2(uniprot_dump_file):
                UniProtAN_list, Keywords_list, GO, InterPro, Pfam, KEGG, Reactome, STRING = stuff
                fh_out.write(";".join(UniProtAN_list) + "\t" + ";".join(STRING) + "\t" + ";".join(KEGG) + "\n")

def get_KEGG_Protein_2_pathwayName_dict(fn_list):
    """
    from KEGG dump --> e.g. hsa.list
    parse KEGG pathway name 2 KEGG protein information
    rename path: to map
    combine this data with UniProt dump information (UniProtAC 2 KeggProtein)
    --> UniProtAC 2 KeggPathwayName
    """
    Protein_2_pathwayName_dict = {}
    for fn in fn_list:
        basename = os.path.basename(fn)
        acronym = basename.replace(".tar.gz", "")
        tar = tarfile.open(fn, "r:gz")
        fh = tar.extractfile("{}/{}.list".format(acronym, acronym))
        for line in fh.readlines():
                ls = line.decode("utf-8").strip().split("\t")
                pathwayName = "map" + ls[0][-5:]
                KeggProtein = ls[1]
                if KeggProtein not in Protein_2_pathwayName_dict:
                    Protein_2_pathwayName_dict[KeggProtein] = [pathwayName]
                else:
                    Protein_2_pathwayName_dict[KeggProtein].append(pathwayName)
    return Protein_2_pathwayName_dict

def Protein_2_Function_table_KEGG_UP(fn_list_KEGG_tar_gz, fn_in_UniProt_2_KEGG_mapping, fn_out_Protein_2_Function_table_KEGG_UP):
    """
    # head fn_in_UniProt_2_KEGG_mapping.txt
    # Q6GZX4  vg:2947773      -52
    # Q6GZX3  vg:2947774      -52
    # Q197F8  vg:4156251      -52
    # Q197F7  vg:4156252      -52
    : param fn_list_KEGG_tar_gz: List of String (list of tar.gz each containing a .list file with protein to pathway annotation)
    : param fn_in_UniProt_2_KEGG_mapping: String (UniProtAC to KEGG protein entry) include UniProtID?
    : param fn_out_Protein_2_Function_table_KEGG_UP: String
    : return: None
    """
    etype_KEGG = variables.id_2_entityTypeNumber_dict['KEGG']
    no_pathway_annotation_KEGG_proteins = []
    Protein_2_pathwayName_dict = get_KEGG_Protein_2_pathwayName_dict(fn_list_KEGG_tar_gz)
    with open(fn_out_Protein_2_Function_table_KEGG_UP, "w") as fh_out:
        with open(fn_in_UniProt_2_KEGG_mapping, "r") as fh_in:  # one to many mapping (though mostly/always only one)
            for line in fh_in:
                uniprot_an_or_id, kegg_an = line.split("\t")
                kegg_protein_list = kegg_an.split(";")
                for kegg_protein_entry in kegg_protein_list:
                    try:
                        pathwayNames_list = Protein_2_pathwayName_dict[kegg_protein_entry]
                    except KeyError:
                        no_pathway_annotation_KEGG_proteins.append(kegg_protein_entry)
                        continue
                    fh_out.write(uniprot_an_or_id + "\t" + cst.format_list_of_string_2_postgres_array(sorted(set(pathwayNames_list))) + "\t" + etype_KEGG + "\n")

if __name__ == "__main__":
    # ToDo rename
    # Protein_2_Function_table_KEGG_temp.txt --> UniProt_2_KEGG_mapping.txt

    # SPEEDUP maybe drop the stupid format for now, and add it after filtering blacklisted terms and mapping to FunctionEnumerations
    # alternatively gunzip file and parallel parse

    fn_in_Functions_table_UPK = os.path.join(variables.TABLES_DIR, "Functions_table_UPK.txt")
    fn_in_obo_GO = os.path.join(variables.DOWNLOADS_DIR, "go-basic.obo")
    fn_in_obo_UPK = os.path.join(variables.DOWNLOADS_DIR, "keywords-all.obo")
    fn_in_uniprot_SwissProt_dat = os.path.join(variables.DOWNLOADS_DIR, "uniprot_sprot.dat.gz")
    fn_in_uniprot_TrEMBL_dat = os.path.join(variables.DOWNLOADS_DIR, "uniprot_trembl.dat.gz")
    fn_in_list_uniprot_dumps = [fn_in_uniprot_SwissProt_dat] #, fn_in_uniprot_TrEMBL_dat]
    fn_out_Protein_2_Function_table_UPK = os.path.join(variables.TABLES_DIR, "Protein_2_Function_table_UPK_v2.txt")
    fn_in_interpro_parent_2_child_tree = os.path.join(variables.DOWNLOADS_DIR, "interpro_parent_2_child_tree.txt")
    fn_in_hierarchy_reactome = os.path.join(variables.DOWNLOADS_DIR, "RCTM_hierarchy.tsv")
    fn_out_Protein_2_Function_table_UniProt_dump = os.path.join(variables.TABLES_DIR, "Protein_2_Function_table_UniProt_dump_temp.txt")
    UniProt_2_KEGG_mapping = os.path.join(variables.TABLES_DIR, "UniProt_2_KEGG_mapping_temp.txt")
    fn_out_Protein_2_Function_table_KEGG_UP = os.path.join(variables.TABLES_DIR, "Protein_2_Function_table_KEGG_UP.txt")

    # profile Protein_2_Function_table_UniProt_UniProtSpace --> VERY slow --> fixed GO category lookup --> parallalize?
    # Protein_2_Function_table_UniProt_UniProtSpace(fn_in_Functions_table_UPK, fn_in_obo_GO, fn_in_obo_UPK, fn_in_list_uniprot_dumps, fn_in_interpro_parent_2_child_tree, fn_in_hierarchy_reactome,fn_out_Protein_2_Function_table_UniProt_dump, UniProt_2_KEGG_mapping, verbose=True)


    # KEGG_dir = r"/mnt/mnemo5/dblyon/STRING_freeze_v11/kegg/pathway/organisms"
    # fn_list_KEGG_tar_gz = os.listdir(KEGG_dir)
    # Protein_2_Function_table_KEGG_UP(fn_list_KEGG_tar_gz, UniProt_2_KEGG_mapping, fn_out_Protein_2_Function_table_KEGG_UP)

    gen = parse_uniprot_dat_dump_yield_entry_v2(fn_in_uniprot_SwissProt_dat)
    counter = 0
    for entry in gen:
        counter += 1