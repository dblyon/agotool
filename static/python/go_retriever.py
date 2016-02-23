import re
import os
import cPickle as pickle
import gzip

import obo_parser
import update_server

PYTHON_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = os.path.abspath(os.path.join(PYTHON_DIR, '..'))
FN_P_PARSER_GO_ANNOTATIONS = os.path.abspath(os.path.join(STATIC_DIR, "data/GOA/Parser_GO_annotations.p"))


class Parser_GO_annotations(object):
    """
    parse UniProt goa_ref files retrieved from ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/
    # e.g. gene_association.goa_ref_yeast
    # additional info http://www.geneontology.org/doc/GO.references
    produce list of GO-terms associated with given AccessionNumber
    file format info:
    http://geneontology.org/page/go-annotation-file-format-20
    Column	Content	Required?	Cardinality	Example
    1	DB	required	1	UniProtKB
    2	DB Object ID	required	1	P12345
    3	DB Object Symbol	required	1	PHO3
    4	Qualifier	optional	0 or greater	NOT
    5	GO ID	required	1	GO:0003993
    6	DB:Reference (|DB:Reference)	required	1 or greater	PMID:2676709
    7	Evidence Code	required	1	IMP
    8	With (or) From	optional	0 or greater	GO:0000346
    9	Aspect	required	1	F
    10	DB Object Name	optional	0 or 1	Toll-like receptor 4
    11	DB Object Synonym (|Synonym)	optional	0 or greater	hToll|Tollbooth
    12	DB Object Type	required	1	protein
    13	Taxon(|taxon)	required	1 or 2	taxon:9606
    14	Date	required	1	20090118
    15	Assigned By	required	1	SGD
    16	Annotation Extension	optional	0 or greater	part_of(CL:0000576)
    17	Gene Product Form ID	optional	0 or 1	UniProtKB:P12345-2
    ############################################################################
    A.) SPECIES SPECIFIC FILTERED
    UniProt-GOA also provides species-specific annotation sets
    using the UniProtKB Complete Proteome and Reference Proteome sets that have undergone an
    additional electronic annotation filtering to remove redundancy.
    The current set of species that we provide these files for are listed on our project website.
    All files can be downloaded from ftp://ftp.ebi.ac.uk/pub/databases/GO/goa.

    B.) UNIPROT UNFILTERED
    If you would like to download an unfiltered GOA UniProt gene association
    file, please use either the GOA ftp site:
    ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/UNIPROT/gene_association.goa_uniprot.gz

    gene association files
    i) gene_association.goa_uniprot --> used in B.)
    This file contains all GO annotations and information for proteins in the UniProt KnowledgeBase (UniProtKB) and
    for entities other than proteins, e.g. macromolecular complexes (IntAct Complex Portal identifiers) or
    RNAs (RNAcentral identifiers). If a particular entity is not annotated with GO, then it will not appear in this file.
    The file is provided as GAF2.0 format (http://www.geneontology.org/GO.format.gaf-2_0.shtml).

    ii) gene_association.goa_<species>  (based on UniProtKB complete proteome). --> used in A.)
    These files contains all GO annotations and information for a species subset of proteins in
    the UniProt KnowledgeBase (UniProtKB) and for entities other than proteins,
    e.g. macromolecular complexes (IntAct Complex Portal identifiers) or RNAs (RNAcentral identifiers).
    These files may provide annotations to more than one protein per gene. The protein accessions
    included in these files are all Swiss-Prot entries for that species plus any TrEMBL
    entries that have an Ensembl DR line. The TrEMBL entries are likely to overlap with
    the Swiss-Prot entries or their isoforms. If a particular entity is not annotated with
    GO, then it will not appear in this file. The file is provided as GAF2.0
    format (http://www.geneontology.org/GO.format.gaf-2_0.shtml).
    ############################################################################

    """
    go_parents_name2num_dict = {"BP": "GO:0008150", "CP": "GO:0005575", "MF": "GO:0003674"}
    my_regex = r"taxon:(\d+)"

    def __init__(self, HOMD=False): #, goa_ref_fn=None, organisms_set=None):
        """
        :param HOMD: Bool (flag to ignore organisms, make it possible to just get GOterms from AN without specifying TaxID)
        :return: None
        """
        # self.date = "not set yet" # generation date
        # self.obolibrary = "not yet set" # link to obo-library
        # self.organism2ans_dict = {} # key=TaxID(String), val=ListOfANs
        # self.an2go_dict = {} # key=AccessionNumber val=ListOfStrings (GO-terms)
        # self.organisms_set = set(organisms_set)
        # self.parse_goa_ref(goa_ref_fn)
        try:
            len(self.organism2ans_dict)
        except AttributeError:
            # self.organism2ans_dict = {} # key=TaxID(String), val=ListOfANs
            self.an2go_dict = {} # key=AccessionNumber val=ListOfStrings (GO-terms)
        self.HOMD = HOMD

    def yield_gz_file_lines(self, fn):
        if fn.endswith(".gz"):
            with gzip.open(fn, "rb") as fh:
                for line in fh:
                    yield line
        else:
            with open(fn, 'r') as fh:
                for line in fh:
                    yield line

    def parse_goa_ref(self, fn, organisms_set=None):
        """
        parse UniProt goa_ref file filling self.an2go_dict
        restrict to organisms (TaxIDs as String) if provided
        :param fn: raw String
        :param organisms_set: SetOfString
        :return: None
        """
        for line in self.yield_gz_file_lines(fn):
            if line[0] == "!":
                if line[0:11] == "!Generated:":
                    self.date = line.replace("!Generated:", "").strip()
                elif line[0:12] == "!GO-version:":
                    self.obolibrary = line.replace("!GO-version:", "").strip()
            else:
                line_split = line.split("\t")
                if len(line_split) >= 15:
                    an = line_split[1] # DB_Object_ID
                    goid = line_split[4] # GO_ID
                    organism = re.match(self.my_regex, line_split[12]).groups()[0]
                    # reduce to specific organisms
                    if organisms_set is not None:
                        if not organism in organisms_set:
                            continue
                    # if not self.organism2ans_dict.has_key(organism):
                    #     self.organism2ans_dict[organism] = [an]
                    # else:
                    #     self.organism2ans_dict[organism].append(an)

                    if not self.an2go_dict.has_key(an): # the only important one ???
                        self.an2go_dict[an] = [goid]
                    else:
                        self.an2go_dict[an].append(goid)
        self.remove_redundant_go_terms()

    def pickle(self, fn_p):
        """
        pickle relevant attributes to given FileName
        :param fn_p: raw String
        :return: None
        """
        dict2pickle = {}
        # dict2pickle["organism2ans_dict"] = self.organism2ans_dict
        dict2pickle["an2godict"] = self.an2go_dict # the only important one ???
        # dict2pickle["date"] = self.date
        # dict2pickle["obolibrary"] = self.obolibrary
        pickle.dump(dict2pickle, open(fn_p, "wb"))
        del dict2pickle

    def unpickle(self):
        """
        unpickle and set relevant attributes to instance
        :param fn_p: raw String
        :return: None
        """
        fn_p = update_server.get_fn_pickle_Parser_GO_annotations()
        dict2pickle = pickle.load(open(fn_p, "rb"))
        # self.organism2ans_dict = dict2pickle["organism2ans_dict"]
        self.an2go_dict = dict2pickle["an2godict"] # the only important one ???
        # self.date = dict2pickle["date"]
        # self.obolibrary = dict2pickle["obolibrary"]
        del dict2pickle

    def get_ans_from_organism(self, organism):
        return self.organism2ans_dict[organism]

    def get_ans(self):
        return self.an2go_dict.keys()

    def get_association_dict_for_organism(self, go_parent, obo_dag, organism):
        '''
        produce association_dictionary, containing all AccessionNumbers of theoretical proteome and
        their corresponding GO-IDs (most specific ones)
        do not report GO-ID without association
        assoc is a dict: key=AN, val=set of go-terms
        go_parent is one of: 'MF', 'BP', 'CP', "all_GO"
        limit the set of GO-terms to the given parent category
        obo_dag is a Dict: key=GO-term, val=GOTerm instance
        can be queried for parent term: obo_dag['GO:1990413'].has_parent('GO:0008150')
        # "BP" "GO:0008150"
        # "CP" "GO:0005575"
        # "MF" "GO:0003674"
        :param go_parent: String
        :param obo_dag: GODag Instance
        :param organism: String (TaxID)
        :return: Dict
        '''
        assoc_dict = {}
        for an in self.get_ans_from_organism(organism):
            if not assoc_dict.has_key(an):
                if go_parent == "all_GO":
                    goterms_list = self.get_goterms_from_an(an)
                else:
                    goterms_list = self.get_goterms_from_an_limit2parent(an, go_parent, obo_dag)
                if goterms_list != -1:
                    assoc_dict[an] = set(goterms_list)
        return assoc_dict

    def get_association_dict(self, go_parent, obo_dag): # WITHOUT the organism distinction
        """
        assoc is a dict: key=AN, val=set of go-terms
        produce dict for all AccessionNumbers not just specific organism cf. above function
        limit the set of GO-terms to the given parent category
        # "BP" "GO:0008150"
        # "CP" "GO:0005575"
        # "MF" "GO:0003674"
        :param go_parent: String
        :param obo_dag: GODag Instance
        :return: Dict
        """
        assoc_dict = {}
        for an in self.get_ans():
            if not assoc_dict.has_key(an):
                if go_parent == "all_GO":
                    goterms_list = self.get_goterms_from_an(an)
                else:
                    goterms_list = self.get_goterms_from_an_limit2parent(an, go_parent, obo_dag)
                if goterms_list != -1:
                    assoc_dict[an] = set(goterms_list)
        return assoc_dict

    def get_goterms_from_an(self, an):
        """
        produce list of GO-terms associated with given AccessionNumber
        :param an: String
        :return: ListOfString
        """
        try:
            return self.an2go_dict[an]
        except KeyError:
            return -1 #!!!

    def get_goterms_from_an_limit2parent(self, an, go_parent, obo_dag):
        '''
        produce list of GO-terms associated with given AccessionNumber
        limit to child terms of given parent
        :param an: String
        :param go_parent: String
        :param obo_dag: GODag Instance
        :return: ListOfString
        '''
        goterms_list = self.get_goterms_from_an(an)
        if goterms_list == -1:
            return -1
        else:
            goterms_of_parent = []
            for goterm in goterms_list:
                if obo_dag.has_key(goterm):
                    if obo_dag[goterm].has_parent(self.go_parents_name2num_dict[go_parent]):
                        goterms_of_parent.append(goterm)
        if len(goterms_of_parent) >= 1:
            return goterms_of_parent
        else:
            return -1

    def remove_redundant_go_terms(self):
        """
        remove redundant go-terms for each AccessionNumber if present
        and sort list of go-terms
        :return: None
        """
        for an in self.an2go_dict.keys():
            self.an2go_dict[an] = sorted(set(self.an2go_dict[an]))

    def get_date(self):
        """
        produce generation date of UniProt resource file
        :return: String
        """
        return self.date

    def get_obolibrary(self):
        """
        produce link to obo-library
        :return: String
        """
        return self.obolibrary

# how about just making one big an2go_dict for all organisms UniProt and HOMD
# load uniprot_all.gz first, then overwrite anything in there with specific files, then add HOMD and check if overwriting AN
# then pickle --> how big in memory???

# assoc_dict = pgoa.get_association_dict_for_organism(go_parent=go_parent, obo_dag=go_dag) # WITHOUT the organism distinction





class UniProtKeywordsParser(object):

    def __init__(self):
        try:
            len(self.organism2assoc_dict)
        except AttributeError:
            self.organism2assoc_dict = {} # key=TaxID(String), val=AssocDict

    def parse_file(self, fn, taxid): #!!!
        """
        :param fn: raw String
        :param taxid: String
        :return: None
        """
        assoc_dict = {}
        with open(fn, 'r') as fh:
            for line in fh:
                line_split = line.split('\t')
                an = line_split[0]
                keywords = set([ele.strip() for ele in line_split[-1].split(';')])
                if keywords != {""}:
                    assoc_dict[an] = keywords
        if not self.organism2assoc_dict.has_key(taxid):
            self.organism2assoc_dict[taxid] = assoc_dict
        else:
            print("organism2assoc_dict already has key {} --> being parsed twice".format(taxid))

    def get_association_dict_from_organims(self, taxid):
        '''
        assoc is a dict: key=AN, val=set of go-terms
        :return: Dict
        '''
        return self.organism2assoc_dict[taxid]

    def pickle(self, fn_p):
        """
        pickle relevant attributes to given FileName
        :param fn_p: raw String
        :return: None
        """
        dict2pickle = {}
        dict2pickle["organism2assoc_dict"] = self.organism2assoc_dict
        pickle.dump(dict2pickle, open(fn_p, "wb"))
        del dict2pickle

    def unpickle(self):
        """
        unpickle and set relevant attributes to instance
        :param fn_p: raw String
        :return: None
        """
        fn_p = update_server.get_fn_UniProtKeywordsParser()
        dict2pickle = pickle.load(open(fn_p, "rb"))
        self.organism2assoc_dict = dict2pickle["organism2assoc_dict"]
        del dict2pickle


def mapslim(go_term, go_dag, goslim_dag):
    """ Maps a GO term (accession) to it's GO slim terms.
        Parameters:
        - go_term: the accession to be mapped to the slim terms
        - go_dag: the (full) Gene Ontology DAG
        - goslim_dag: the GO Slim DAG
        Returns:
            Two sets:
            direct_ancestors, all_ancestors
        - direct_ancestors: The direct ancestors of the given term that are in
                            the GO Slim. Those are the terms that are not
                            covered by earlier ancestors of the GO Slims in
                            _any_ path (from bottom to top). --> without backtracking
        - all_ancestors:    All ancestors of the given term that are part of
                            the GO-Slim terms. --> backtracking
    """
    # check parameters
    if not isinstance(go_dag, obo_parser.GODag):
        raise TypeError("go_dag must be an instance of GODag")
    if not isinstance(goslim_dag, obo_parser.GODag):
        raise TypeError("goslim_dag must be an instance of GODag")
    if go_term not in go_dag:
        raise ValueError("go_term must be an accession that is in the go_dag")
    all_ancestors = set()
    covered_ancestors = set()
    # get all paths for the term in the go_dag
    paths = go_dag.paths_to_top(go_term)
    for path in paths:
        # the next loop needs to run bottom->up, i.e. from the go_term item to
        # the root, thus we need to reverse the list prior to iteration
        path.reverse()
        got_leaf = False
        for term in path:
            if term.id in goslim_dag:
                all_ancestors.add(term.id)
                if got_leaf:
                    covered_ancestors.add(term.id)
                got_leaf = True
    # get the direct ancestors, i.e. those that are not covered by a earlier
    # ancestor of the GO-Slim in _any_ path (in bottom->top order)
    direct_ancestors = all_ancestors - covered_ancestors
    return direct_ancestors, all_ancestors

def gobasic2slims(assoc_dict, go_dag, goslim_dag, backtracking):
    # assoc is a dict: key=AN, val=set of go-terms
    assoc_dict_slims = {}
    for an, go_terms in assoc_dict.items():
        all_direct_anc = set()
        all_covered_anc = set()
        all_all_anc = set()
        for go_term in go_terms:
            if go_term not in go_dag:
                continue
            direct_anc, all_anc = mapslim(go_term, go_dag, goslim_dag)
            all_all_anc |= all_anc
            # collect all covered ancestors, so the direct ancestors
            # can be calculated afterwards
            all_covered_anc |= (all_anc - direct_anc)
        all_direct_anc = all_all_anc - all_covered_anc
        if backtracking:
            assoc_dict_slims[an] = all_all_anc
        else:
            assoc_dict_slims[an] = all_direct_anc
    return assoc_dict_slims


if __name__ == "__main__":
################################################################################
### try new HOMD_GOA.tsv
    pgoa = Parser_GO_annotations()
    fn = r'/Users/dblyon/modules/cpr/agotool/static/data/GOA/HOMD_GOA_commasepnotlong.tsv'
    # fn = r'/Users/dblyon/modules/cpr/agotool/static/data/GOA/HOMD_GOA.tsv'
    pgoa.parse_goa_ref(fn, organisms_set=None)



################################################################################
    # fn_gz = r"../../static/data/GOA/uniprot_test.gz"
    # organisms_set={u'10090',
    #                  u'10116',
    #                  u'3055',
    #                  u'3702',
    #                  u'3880',
    #                  u'39947',
    #                  u'4932',
    #                  u'7227',
    #                  u'7955',
    #                  u'9031',
    #                  u'9606',
    #                  u'9796',
    #                  u'9823'}

    ##### parsing from GOA_ref file
    # pgoa = Parser_GO_annotations(fn_gz, organisms_set)
    # go_dag = obo_parser.GODag(obo_file=r'/Users/dblyon/modules/cpr/agotool/static/data/OBO/go-basic.obo')
    # assoc_dict = pgoa.get_association_dict_for_organism(go_parent='all_GO', obo_dag=go_dag, organism="9606")
    ##### unpickle
    # pgoa = Parser_GO_annotations()
    # pgoa.unpickle()
    # go_dag = obo_parser.GODag(obo_file=r'../../static/data/OBO/go-basic.obo')
    # assoc_dict = pgoa.get_association_dict_for_organism(go_parent="all_GO", obo_dag=go_dag, organism="9606")




################################################################################
################################################################################
##### RIP dead code
# class Parser_UniProt_goa_ref(object):
#     """
#     formerly known as 'Goretriever'
#     parse UniProt goa_ref files retrieved from ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/
#     # e.g. gene_association.goa_ref_yeast
#     # additional info http://www.geneontology.org/doc/GO.references
#     produce list of GO-terms associated with given AccessionNumber
#     """
#     go_parents_name2num_dict = {"BP": "GO:0008150", "CP": "GO:0005575", "MF": "GO:0003674"}
#
#     def __init__(self, goa_ref_fn):
#         """
#         :return: None
#         """
#         self.an2go_dict = {} # key=AccessionNumber val=ListOfStrings (GO-terms)
#         self.date = "not set yet" # generation date
#         self.obolibrary = "not yet set" # link to obo-library
#         self.parse_goa_ref(goa_ref_fn)
#
#     def parse_goa_ref(self, fn):
#         """
#         parse UniProt goa_ref file filling self.an2go_dict
#         :param fn: raw String
#         :return: None
#         """
#         fh = open(fn, "r")
#         for line in fh:
#             if line[0] == "!":
#                 if line[0:11] == "!Generated:":
#                     self.date = line.replace("!Generated:", "").strip()
#                 elif line[0:12] == "!GO-version:":
#                     self.obolibrary = line.replace("!GO-version:", "").strip()
#             else:
#                 line_split = line.split("\t")
#                 if len(line_split) == 17:
#                     an = line_split[1] # DB_Object_ID
#                     goid = line_split[4] # GO_ID
#                     if not self.an2go_dict.has_key(an):
#                         self.an2go_dict[an] = [goid]
#                     else:
#                         self.an2go_dict[an].append(goid)
#         self.remove_redundant_go_terms()
#         fh.close()
#
#     def set2sortedlist(self):
#         for an in self.an2go_dict.keys():
#             self.an2go_dict[an] = sorted(self.an2go_dict[an])
#
#     def get_goterms_from_an(self, an):
#         """
#         produce list of GO-terms associated with given AccessionNumber
#         :param an: String
#         :return: ListOfString
#         """
#         try:
#             return self.an2go_dict[an]
#         except KeyError:
#             return -1 #!!!
#
#     def get_goterms_from_an_limit2parent(self, an, go_parent, obo_dag):
#         '''
#         produce list of GO-terms associated with given AccessionNumber
#         limit to child terms of given parent
#         :param an: String
#         :param go_parent: String
#         :param obo_dag: GODag Instance
#         :return: ListOfString
#         '''
#         goterms_list = self.get_goterms_from_an(an)
#         if goterms_list == -1:
#             return -1
#         else:
#             goterms_of_parent = []
#             for goterm in goterms_list:
#                 if obo_dag.has_key(goterm):
#                     if obo_dag[goterm].has_parent(self.go_parents_name2num_dict[go_parent]):
#                         goterms_of_parent.append(goterm)
#         if len(goterms_of_parent) >= 1:
#             return goterms_of_parent
#         else:
#             return -1
#
#     def get_ans(self):
#         '''
#         produce List of AccessionNumbers
#         :return: ListOfString
#         '''
#         return sorted(self.an2go_dict)
#
#     def get_date(self):
#         """
#         produce generation date of UniProt resource file
#         :return: String
#         """
#         return self.date
#
#     def get_obolibrary(self):
#         """
#         produce link to obo-library
#         :return: String
#         """
#         return self.obolibrary
#
#     def remove_redundant_go_terms(self):
#         """
#         remove redundant go-terms for each AccessionNumber if present
#         and sort list of go-terms
#         :return: None
#         """
#         for an in self.an2go_dict.keys():
#             self.an2go_dict[an] = sorted(set(self.an2go_dict[an]))
#
#     def pickle(self, fn_p):
#         """
#         pickle relevant attributes to given FileName
#         :param fn_p: raw String
#         :return: None
#         """
#         dict2pickle = {}
#         dict2pickle["an2godict"] = self.an2go_dict
#         dict2pickle["date"] = self.date
#         dict2pickle["obolibrary"] = self.obolibrary
#         pickle.dump(dict2pickle, open(fn_p, "wb"))
#         del dict2pickle
#
#     def unpickle(self, fn_p):
#         """
#         unpickle and set relevant attributes to instance
#         :param fn_p: raw String
#         :return: None
#         """
#         dict2pickle = pickle.load(open(fn_p, "rb"))
#         self.an2go_dict = dict2pickle["an2godict"]
#         self.date = dict2pickle["date"]
#         self.obolibrary = dict2pickle["obolibrary"]
#         del dict2pickle
#
#     def write_association2file(self, fn_out):
#         '''
#         produce input file for goatools termed 'association'
#         containing all AccessionNumbers of theoretical proteome and
#         their corresponding GO-IDs
#         e.g.:
#         AN tab GO-id1;GO-id2;GO-id3
#         ACD5	GO:0005575;GO:0003674;GO:0008219
#         :param fn_out: rawString
#         :return: None
#         '''
#         with open(fn_out, 'w') as fh_out:
#             for an in self.get_ans():
#                 go_list = self.get_goterms_from_an(an)
#                 if go_list == -1:
#                     pass # #!!! should there be a default value instead?
#                 else:
#                     fh_out.write(an + '\t' + ';'.join(go_list) + '\n')
#
#     def get_association_dict(self, go_parent, obo_dag):
#         '''
#         produce association_dictionary, containing all AccessionNumbers of theoretical proteome and
#         their corresponding GO-IDs (most specific ones)
#         do not report GO-ID without association
#         assoc is a dict: key=AN, val=set of go-terms
#         go_parten is one of: 'MF', 'BP', 'CP', "all_GO"
#         limit the set of GO-terms to the given parent category
#         obo_dag is a Dict: key=GO-term, val=GOTerm instance
#         can be queried for parent term: obo_dag['GO:1990413'].has_parent('GO:0008150')
#         # "BP" "GO:0008150"
#         # "CP" "GO:0005575"
#         # "MF" "GO:0003674"
#         :param go_parent: String
#         :param obo_dag: GODag Instance
#         :return: Dict
#         '''
#         assoc_dict = {}
#         for an in self.get_ans():
#             if not assoc_dict.has_key(an):
#                 if go_parent == "all_GO":
#                     goterms_list = self.get_goterms_from_an(an)
#                 else:
#                     goterms_list = self.get_goterms_from_an_limit2parent(an, go_parent, obo_dag)
#                 if goterms_list != -1:
#                     assoc_dict[an] = set(goterms_list)
#             else:
#                 if go_parent == "all_GO":
#                     goterms_set = set(self.get_goterms_from_an(an))
#                 else:
#                     goterms_set = set(self.get_goterms_from_an_limit2parent(an, go_parent, obo_dag))
#                 if assoc_dict[an] != goterms_set:
#                     print('Associations-dict: multiple entries of AN with diverging associations:')
#                     print(an + ' ' + self.get_goterms_from_an(an))
#         # return assoc_dict
