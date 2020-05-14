import os
import pickle
from collections import defaultdict
import urllib
from retrying import retry
import variables
DOWNLOADS_DIR = variables.DOWNLOADS_DIR

#### consider ete3
debug = False
# TopLevel=1
# Archaea=2157
# Bacteria=2
# Eukaryota=2759
# Viruses=10239


@retry(stop_max_attempt_number=5, wait_exponential_multiplier=50000)
def download_gzip_file(url, file_name, verbose=True):
    """
    :param url: String
    :param file_name: String (absolute path of name of downloaded)
    :param verbose: Bool (flag to print infos)
    :return: None
    """
    CHUNK = 16 * 1024
    temp_fn = file_name + ".tmp"
    if verbose:
        print('\nDownloading: {}'.format(url))
        print('TO: {}'.format(file_name))
    try:
        with open(temp_fn, "wb") as temp_fh:
            response = urllib.request.urlopen(url)
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                temp_fh.write(chunk)
                temp_fh.flush()
    except IOError:
        print("Couldn't download {}".format(url))
        os.remove(temp_fn.name)
    os.rename(temp_fn, file_name)
    if verbose:
        print("finished download")


class NCBI_taxonomy(object):
    """
    given a TaxID (e.g. 9606), retrieve parent, getrank, scientific name
    parse yourself
    """
    def __init__(self, taxdump_directory=None, for_SQL=False, update=False):
        """
        TaxID = -1 if not found
        TaxName = "alien" if not found
        Rank = "no rank" if not found
        :param taxdump_directory: String
        :return: None
        """
        homedir = os.path.expanduser("~")
        self.for_SQL = for_SQL
        if self.for_SQL:
            self.taxname_2_scientificname = {}

        if taxdump_directory is None:
            self.taxdump_directory = DOWNLOADS_DIR
        else:
            self.taxdump_directory = taxdump_directory

        self.taxid_2_taxname_dict = defaultdict(lambda: "root") #"alien") # key=TaxID(Int), val=TaxName(String)
        self.taxname_2_taxid_dict = defaultdict(lambda: 1) #-1) # key=TaxID(Int), val=TaxName(String)
        self.taxid_2_parent_taxid_dict = defaultdict(lambda: 1) #-1) # key=TaxID(Int), val=TaxID_parent(Int)
        self.taxid_2_rank_dict = defaultdict(lambda: "no rank")# key=TaxID(Int), val=Rank(String)
        self.taxid_rank2parent_of_rank_dict = {} # key=TaxID_Rank, val=TaxID

        if update:
            self.update_NCBI_taxonomy_files()

        self.parse_names_file(self.taxdump_directory)
        self.parse_nodes_file(self.taxdump_directory)

        self.child_2_parent_dict_fn = os.path.join(self.taxdump_directory, "NCBI_taxonomy_child2parent_dict.p")
        self.taxidsyn_2_taxid_dict_fn = os.path.join(self.taxdump_directory, "taxidsyn_2_taxid_dict.p")
        if os.path.exists(self.child_2_parent_dict_fn):
            self.load_child2parent_dict()
        else:
            self.child2parent_dict = {} # key = taxidChild_taxidParent, val = Bool; e.g. {'3218_33090': True, '3218_33634': False, ...}
        if os.path.exists(self.taxidsyn_2_taxid_dict_fn):
            self.load_taxidsyn_2_taxid_dict()
        else:
            self.taxidsyn_2_taxid_dict = {}  # key=TaxID (synonym), val=TaxID (NCBI)

    def update_NCBI_taxonomy_files(self):
        """
        don't forget to "tar -zxvf filename"
        ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/
        http://stackoverflow.com/questions/2695152/in-python-how-do-i-decode-gzip-encoding
        :return: None
        """
        from subprocess import call
        file_not_downloaded_list = []
        file_name = "taxdump.tar.gz"
        url = "ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/{}".format(file_name)
        file_name_abs = os.path.join(self.taxdump_directory, file_name)
        download_gzip_file(url, file_name_abs, verbose=True)
        print("Extracting files and removing .tar.gz")
        destination = os.path.dirname(file_name_abs)
        shellcmd = "tar -zxvf {} -C {}".format(file_name_abs, destination)
        print(shellcmd)
        call(shellcmd, shell=True)
        os.remove(file_name_abs)

    def parse_nodes_file(self, taxdump_directory):
        """
        Load taxonomy NCBI file ("nodes.dmp")
        nodes.dmp file consists of taxonomy nodes. The description for each node includes the following
        the following fields:
            tax_id					            -- node id in GenBank taxonomy database
            parent tax_id				        -- parent node id in GenBank taxonomy database
            rank					            -- rank of this node (superkingdom, kingdom, ...)
            embl code				            -- locus-name prefix; not unique
            division id				            -- see division.dmp file
            inherited div flag  (1 or 0)	    -- 1 if node inherits division from parent
            genetic code id				        -- see gencode.dmp file
            inherited GC  flag  (1 or 0)		-- 1 if node inherits genetic code from parent
            mitochondrial genetic code id		-- see gencode.dmp file
            inherited MGC flag  (1 or 0)		-- 1 if node inherits mitochondrial gencode from parent
            GenBank hidden flag (1 or 0)        -- 1 if name is suppressed in GenBank entry lineage
            hidden subtree root flag (1 or 0)   -- 1 if this subtree has no sequence data yet
            comments				            -- free-text comments and citations
        :param taxdump_directory: String(absolute path)
        :return: None
        """
        fn = os.path.join(taxdump_directory, "nodes.dmp")
        with open(fn, "r") as fh:
            for line in fh:
                line = line.replace("\t","")
                tab = line.split("|")
                taxid = int(tab[0])
                taxid_parent = int(tab[1])
                rank = str(tab[2])
                # division = str(tab[4])

                self.taxid_2_rank_dict[taxid] = rank
                self.taxid_2_parent_taxid_dict[taxid] = taxid_parent

    def parse_names_file(self, taxdump_directory):
        """
        Load  NCBI names file ("names.dmp")
        names.dmp
        Taxonomy names file has these fields:
            tax_id					-- the id of node associated with this name
            name_txt				-- name itself
            unique name				-- the unique variant of this name if name not unique
            name class				-- (synonym, common name, ...)
        :param taxdump_directory: String(absolute path)
        :return: None
        """
        fn = os.path.join(taxdump_directory, "names.dmp")
        with open(fn, "r") as fh:
            if self.for_SQL:
                for line in fh:
                    line_split = [ele.strip() for ele in line.split("|")]
                    if line_split[3] == "scientific name":
                        scientific_name = 1
                    else:
                        scientific_name = 0
                    taxid, taxname = int(line_split[0]), line_split[1]
                    self.taxname_2_taxid_dict[taxname] = taxid # taxnames should be unique, taxids not
                    self.taxname_2_scientificname[taxname] = scientific_name
                    self.taxid_2_taxname_dict[taxid] = taxname

            else:
                for line in fh:
                    line = line.rstrip()
                    line = line.replace("\t", "") # maybe strip better?
                    tab = line.split("|")
                    if tab[3] == "scientific name":
                        taxid, taxname = int(tab[0]), tab[1]          # Assign tax_id and name ...
                        self.taxid_2_taxname_dict[taxid] = taxname
                        self.taxname_2_taxid_dict[taxname] = taxid

    def get_parent_taxid(self, taxid, rank=None):
        """
        produce TaxID of parent, optionally of given rank.
        If rank can't be found (e.g. looking for species, but taxid at genus level) return 1
        :param taxid: Int
        :param rank: String or None
        :return: Int
        """
        if not rank:
            return self.taxid_2_parent_taxid_dict[taxid]
        else:
            while True:
                rank_taxid = self.taxid_2_rank_dict[taxid]
                if rank == rank_taxid: # already at desired rank level
                    return taxid
                taxid = self.taxid_2_parent_taxid_dict[taxid]
                if taxid == 1 or taxid == -1:
                    return taxid

    def iter_direct_parent(self, taxid):
        while True:
            taxid = self.get_parent_taxid(taxid)
            if taxid == 1 or taxid == -1:
                break
            else:
                yield taxid

    def get_allparents(self, taxid):
        parents_list = []
        while True:
            if taxid == 1 or taxid == -1:
                return parents_list
            taxid = self.taxid_2_parent_taxid_dict[taxid]
            parents_list.append(taxid)

    def get_rank(self, taxid):
        return self.taxid_2_rank_dict[taxid]

    def get_sciname(self, taxid):
        return self.taxid_2_taxname_dict[taxid]

    def get_genus_or_higher(self, taxid, rank='genus'):
        """
        get genus is possible (if on genus level or lower)
        else return given taxid
        :param rank: String
        :param taxid: TaxID(Int)
        return: TaxID(String)
        """
        taxid_parent = self.get_parent_taxid(taxid, rank=rank)
        if rank == self.get_rank(taxid_parent):
            return taxid_parent
        else:
            return taxid

    def get_taxid_parent_of_rank(self, taxid, rank): # !!! check this
        """
        taxid_strain = 266940 # species 131568
        rank = "species"
        print tax.get_parent_of_rank(taxid_strain, rank)
        print tax.get_parent_taxid(taxid_strain, rank)
        tax.taxid_rank2parent_of_rank_dict["266940_species"]

        produce TaxID of given rank of given taxid
        :param taxid: String or Int
        :param rank: String
        :return: Int
        """
        taxid_rank = str(taxid) + "_" + rank
        try:
            return self.taxid_rank2parent_of_rank_dict[taxid_rank]
        except KeyError:
            taxid_parent = self.get_parent_taxid(taxid, rank=rank)
            self.taxid_rank2parent_of_rank_dict[taxid_rank] = taxid_parent
            return taxid_parent

    def get_parent_of_rank(self, taxid, rank):
        """
        just for backwards compatibility
        produce TaxID of given rank of given taxid
        :param taxid: String or Int
        :param rank: String
        :return: Int
        """
        return self.get_taxid_parent_of_rank(taxid, rank)

    def load_child2parent_dict(self):
        self.child2parent_dict = pickle.load(open(self.child_2_parent_dict_fn, "rb"))

    def load_taxidsyn_2_taxid_dict(self):
        self.taxidsyn_2_taxid_dict = pickle.load(open(self.taxidsyn_2_taxid_dict_fn, "rb"))

    def is_taxid_child_of_parent_taxid(self, taxid_child, taxid_parent):
        """
        test if TaxID_child is a child of TaxID_parent
        :param taxid_child: Int
        :param taxid_parent: Int
        :return: Bool
        """
        parents_of_taxid_child = self.get_allparents(taxid_child)
        if len(parents_of_taxid_child ) == 0:
            return False
        if taxid_parent in set(parents_of_taxid_child):
            return True
        else:
            return False

    def is_taxid_child_of_parent_taxid_speed(self, taxid_child, taxid_parent):
        try:
            return self.child2parent_dict[str(taxid_child) + "_" + str(taxid_parent)]
        except KeyError:
            is_child = self.is_taxid_child_of_parent_taxid(taxid_child, taxid_parent)
            self.child2parent_dict[str(taxid_child) + "_" + str(taxid_parent)] = is_child
            return is_child

    # def retrieve_tax_report(self, taxid_list, fn_tax_report_out, full_lineage):
    #     """
    #     download NCBI tax report for given file containing newline separated
    #     list of species names or TaxIDs
    #     :param fn_species_or_taxid_list_in: FileName
    #     :param fn_tax_report_out: FileName
    #     :param full_lineage: Bool
    #     :return: None
    #     """
    #     if full_lineage:
    #         full_lineage_switch = 1
    #     else:
    #         full_lineage_switch = 0
    #     data = {'button': 'Save in file', 'tax': "\n".join([str(ele) for ele in taxid_list]), 'lng': full_lineage_switch}
    #     data = urllib.urlencode(data)
    #     urllib.urlretrieve('http://www.ncbi.nlm.nih.gov/Taxonomy/TaxIdentifier/tax_identifier.cgi', fn_tax_report_out, data=data)

    # def retrieve_parse_pickle_taxidsyn2taxid(self, taxid_list):
    #     """
    #     retrieve taxreport from http://www.ncbi.nlm.nih.gov/Taxonomy/TaxIdentifier/tax_identifier.cgi
    #     parse it and pickle it to taxidsyn_2_taxid_dict
    #
    #     :param taxid_list: ListOfInt
    #     :return: None
    #     """
    #     fn_tax_report_out = "TaxID_synonyms_2_TaxID_NCBI_report_temp.txt"
    #     self.retrieve_tax_report(taxid_list, fn_tax_report_out, full_lineage=False)
    #     df = pd.read_csv(fn_tax_report_out, sep='\t')
    #     keys = df["taxid"].tolist()
    #     vals = df["primary taxid"].tolist()
    #     self.taxidsyn_2_taxid_dict = dict(zip(keys, vals))
    #     fn_out_pickle = os.path.join(self.taxdump_directory, "taxidsyn_2_taxid_dict.p")
    #     pickle.dump(self.taxidsyn_2_taxid_dict, open(fn_out_pickle, "wb"))
    #     os.remove(fn_tax_report_out)

    def get_taxid_from_synonymous_taxid(self, taxid):
        """
        :param taxid: String
        :return: String
        """
        try:
            return self.taxidsyn_2_taxid_dict[taxid]
        except KeyError:
            print("No NCBI taxid found from synonymous Taxid: ", taxid)

    # def write_Taxa_table_AND_taxid_2_rank_table_for_SQL(self, fn_out_taxa, fn_out_taxid_2_rank, update_NCBI_dump_files=False):
    #     """
    #     ## Taxa table
    #     | TaxID | TaxName | scientific
    #     ## TaxID_2_rank table
    #     | TaxID | rank |
    #     """
    #     if update_NCBI_dump_files:
    #         self.update_NCBI_taxonomy_files()
    #     taxid_2_rank__taxid_set = set()
    #     with open(fn_out_taxa, "w") as fh_out_taxa:
    #         with open(fn_out_taxid_2_rank, "w") as fh_out_taxid_2_rank:
    #             for taxname in self.taxname_2_taxid_dict.keys():
    #                 taxid = self.taxname_2_taxid_dict[taxname]
    #             # for taxid, taxnames_list in self.taxname_2_taxid_dict.items():
    #             #     tax
    #             #     if taxid == 1154:
    #             #         print taxid, taxname
    #             #         break
    #                 rank = self.taxid_2_rank_dict[taxid]
    #                 scientificname = self.taxname_2_scientificname[taxname]
    #                 line2write = str(taxid) + "\t" + taxname + "\t" + str(scientificname) + "\n"
    #                 fh_out_taxa.write(line2write)
    #                 if taxid not in taxid_2_rank__taxid_set:
    #                     line2write = str(taxid) + "\t" + rank + "\n"
    #                     fh_out_taxid_2_rank.write(line2write)
    #                 taxid_2_rank__taxid_set.update([taxid])
    #
    # def write_Child_2_Parent_table_Taxa_for_SQL(self, fn_out):
    #     # type_number = "-3"  # entity type = "DOID diseases" from Lars's Entities and types system
    #     with open(fn_out, "w") as fh:
    #         for taxid_child in sorted(self.taxid_2_parent_taxid_dict.keys()):
    #             taxid_parent = self.taxid_2_parent_taxid_dict[taxid_child]
    #             line2write = str(taxid_child) + "\t" + str(taxid_parent) + "\n"
    #             fh.write(line2write)


# class NCBI_taxonomy_R(object):
#     """
#     given a TaxID (e.g. 9606), retrieve parent, getrank, scientific name
#     interfaces with R and R-package 'CHNOSZ' to access NCBI-tax-files
#     """
#     def __init__(self, taxdump_directory=None):
#         homedir = os.path.expanduser("~")
#         self.taxid2taxnamesfl_dict = {} # key=TaxID, val=String(Full Lineage of TaxNames for LEfSe analysis)
#         self.taxid2parent_of_rank_dict = {} # key=TaxID_Rank, val=TaxID
#         self.taxid2rank_closest_classified_dict = {1: 'root'} # key=TaxID, val=Rank (String)
#         self.taxid2taxid_closest_classified_dict = {1: 1}
#         self.set2break = {131567, 1} # TaxIDs of CellularOrganisms and Root
#         # self.taxid2superkingdom_dict = {} # key=TaxID, val=
#
#         self.child2parent_dict_fn = os.path.join(homedir, "modules/cpr/metaprot/taxdump/NCBI_taxonomy_child2parent_dict.p")
#         if os.path.exists(self.child2parent_dict_fn):
#             self.load_child2parent_dict()
#         else:
#             self.child2parent_dict = {} # key = taxid_child_taxid_parent, val = Bool; e.g. {'3218_33090': True, '3218_33634': False, ...}
#
#         rpackages.importr('CHNOSZ')
#         if not taxdump_directory:
#             taxdump_directory = os.path.join(homedir, "modules/cpr/metaprot/taxdump")
#             # taxdump = """taxdir <- ('/Users/dblyon/modules/cpr/metaprot/taxdump')"""
#         # else:
#         taxdump = """taxdir <- ('{}')""".format(taxdump_directory)
#         robjects.r(taxdump)
#         robjects.r("""
#         nodes <- getnodes(taxdir=taxdir)
#         names <- getnames(taxdir=taxdir)
#         """)
#
#     def __del__(self):
#         self.save_child2parent_dict()
#
#     def get_parent(self, taxid, rank=None):
#         """
#         produces taxid of parent or of given rank
#         :param taxid: Integer
#         :return: Integer
#         """
#         if rank:
#             string2r = """parent({}, nodes=nodes, rank='{}')""".format(taxid, rank)
#         else:
#             string2r = """parent({}, nodes=nodes, rank=NULL)""".format(taxid)
#         try:
#             tax2return = int(robjects.r(string2r)[0])
#         except TypeError:
#             tax2return = -1
#         # except IndexError:
#         #     tax2return = -1
#         return tax2return
#
#     def get_allparents(self, taxid):
#         """
#         sorted (ascending) list of TaxID-parents of given TaxID (including given TaxID)
#         :param taxid: Integer
#         :return: List of Integer
#         """
#         return [int(taxid) for taxid in robjects.r("""allparents({}, nodes=nodes)""".format(taxid))]
#
#     def info_ranks(self):
#         """
#         produce ascending taxonomic ranks (name of ranks)
#         :return: List of String
#         """
#         # return ["domain", "superkingdom", "kingdom", "phylum (division)",
#         #         "class", "subclass", "order", "superfamily", "family",
#         #         "subfamily", "tribe", "subtribe", "genus", "subgenus",
#         #         "species", "subspecies"]
#         return ["domain", "superkingdom", "kingdom", "subkingdom",
#                 "phylum", 'subphylum', "division",
#                 "class", "subclass",
#                 'superorder', "order", 'suborder', 'infraorder', 'parvorder',
#                 "superfamily", "family", "subfamily",
#                 "tribe", "subtribe",
#                 "genus", "subgenus",
#                 "species", "subspecies"]
#
#     def get_rank(self, taxid):
#         return robjects.r("""getrank({}, nodes=nodes)""".format(taxid))[0]
#
#     def get_sciname(self, taxid):
#         return robjects.r("""sciname({}, names=names)""".format(taxid))[0]
#
#     def get_infos_taxid(self, taxid):
#         """
#         produce given TaxID, scientific name, rank, parent_TaxID
#         :param taxid: Int
#         :return: Tuple(Int, Str, Str, Int)
#         """
#         parent = self.get_parent(taxid)
#         rank = self.get_rank(taxid)
#         sciname = self.get_sciname(taxid)
#         return taxid, sciname, rank, parent
#
#     def get_genus_or_higher(self, taxid, rank='genus'):
#         """
#         get genus is possible (if on genus level or lower)
#         else return given taxid
#         return: taxid (String)
#         """
#         parent = self.get_parent(taxid, rank=rank)
#         if rank == self.get_rank(parent):
#             return parent
#         else:
#             return taxid
#
#     def is_taxid_child_of_parent_taxid(self, taxid_child, taxid_parent):
#         try:
#             parents_of_taxid_child = self.get_allparents(taxid_child)
#         except:
#             print("{} taxid_child, throws Error".format(taxid_child))
#         if taxid_parent in set(parents_of_taxid_child):
#             return True
#         else:
#             return False
#
#     def is_taxid_child_of_parent_taxid_speed(self, taxid_child, taxid_parent):
#         try:
#             return self.child2parent_dict[str(taxid_child) + "_" + str(taxid_parent)]
#         except KeyError:
#             is_child = self.is_taxid_child_of_parent_taxid(taxid_child, taxid_parent)
#             self.child2parent_dict[str(taxid_child) + "_" + str(taxid_parent)] = is_child
#             return is_child
#
#     def filter_include_taxid_child_of_parent_taxid(self, child_taxid_list, parent=2759):
#         """
#         batch process list of child_taxids against the same parent_taxid
#         if child had the given parent --> include in return list
#         :param child_taxid_list: List of Integers
#         :param parent: Integer (default Eukaryota)
#         :return: List of Integers
#         """
#         taxid_list2return = []
#         for taxid in child_taxid_list:
#             if self.is_taxid_child_of_parent_taxid_speed(taxid_child=taxid, taxid_parent=parent):
#                 taxid_list2return.append(taxid)
#         return taxid_list2return
#
#     def filter_exclude_taxid_child_of_parent_taxid(self, child_taxid_list, parent):
#         """
#         if child had the given parent --> exclude in return list
#         :param child_taxid_list: List of Integers
#         :param parent:  Integer
#         :return: List of Integers
#         """
#         taxid_list2return = []
#         for taxid in child_taxid_list:
#             if not self.is_taxid_child_of_parent_taxid_speed(taxid_child=taxid, taxid_parent=parent):
#                 taxid_list2return.append(taxid)
#         return taxid_list2return
#
#     def save_child2parent_dict(self):
#         pickle.dump(self.child2parent_dict, open(self.child2parent_dict_fn, "wb"))
#
#     def load_child2parent_dict(self):
#         self.child2parent_dict = pickle.load(open(self.child2parent_dict_fn, "rb"))
#
#     def TaxID_lineage_info(self, taxid):
#         """
#         prints TaxID, SciName, Rank of given TaxID and all parents
#         :param taxid: TaxID (String or Int)
#         :return: None
#         """
#         print(taxid, "#", self.get_sciname(taxid), "#", self.get_rank(taxid))
#         parent_old = False
#         while True:
#             parent = self.get_parent(taxid)
#             parent_new = parent
#             if parent_old == parent_new:
#                 break
#             print(parent, "#", self.get_sciname(parent), "#", self.get_rank(parent))
#             parent_old = parent
#             taxid = parent
#
#     def unpickle_taxid2taxnamesfl_dict_from_file(self, fn):
#         self.taxid2taxnamesfl_dict = pickle.load(open(fn, "rb"))
#
#     def get_full_lineage_from_taxnames(self, taxid, sep='|'):
#         """
#         produce full taxonomic lineage as TaxName of parents of given TaxID,
#         separated by sep
#         for LEfSe analysis
#         http://huttenhower.sph.harvard.edu/galaxy
#         TaxID: 131567 # cellular organisms # no rank
#         :param taxid: TaxID(Integer)
#         :param sep: separator
#         :return: String
#         """
#         try:
#             return self.taxid2taxnamesfl_dict[taxid]
#         except KeyError:
#             taxid_orig = taxid
#             taxid_list = []
#             taxid_list.append(self.get_sciname(taxid))
#             while True:
#                 parent = self.get_parent(taxid)
#                 if parent in self.set2break: # cellular organisms or root
#                     break
#                 taxid_list.append(self.get_sciname(parent))
#                 taxid = parent
#             taxid_list = taxid_list[::-1]
#             taxnames = "|".join(taxid_list)
#             self.taxid2taxnamesfl_dict[taxid_orig] = taxnames
#             return taxnames
#
#     def get_parent_of_rank(self, taxid, rank):
#         """
#         produce TaxID of given rank of given taxid
#         :param taxid: String or Int
#         :param rank: String
#         :return: Int
#         """
#         taxid_rank = str(taxid) + "_" + rank
#         try:
#             return self.taxid2parent_of_rank_dict[taxid_rank]
#         except KeyError:
#             parent = self.get_parent(taxid, rank=rank)
#             self.taxid2parent_of_rank_dict[taxid_rank] = parent
#             return parent
#
#     def unpickle_taxid2parent_of_rank_dict_from_file(self, fn):
#         self.taxid2parent_of_rank_dict = pickle.load(open(fn, "rb"))
#
#     def get_rank_of_closest_classified(self, taxid):
#         """
#         produce rank of taxid or next highest rank that is NOT 'no rank'
#         :param taxid: TaxID (String or Int)
#         :return: String
#         """
#         try:
#             return self.taxid2rank_closest_classified_dict[taxid]
#         except KeyError:
#             rank = self.get_rank(taxid)
#             if not rank == "no rank":
#                 self.taxid2rank_closest_classified_dict[taxid] = rank
#                 return rank
#             else:
#                 taxid = self.get_parent(taxid)
#                 return self.get_rank_of_closest_classified(taxid)
#
#     def unpickle_taxid2rank_closest_classified_dict_from_file(self, fn):
#         self.taxid2rank_closest_classified_dict = pickle.load(open(fn, "rb"))
#
#     def get_taxid_of_closest_classified(self, taxid):
#         try:
#             return self.taxid2taxid_closest_classified_dict[taxid]
#         except KeyError:
#             rank = self.get_rank(taxid)
#             if not rank == "no rank":
#                 self.taxid2taxid_closest_classified_dict[taxid] = taxid
#                 return taxid
#             else:
#                 taxid = self.get_parent(taxid)
#                 return self.get_taxid_of_closest_classified(taxid)
#
#     def unpickle_taxid2taxid_closest_classified_dict_from_file(self, fn):
#         self.taxid2taxid_closest_classified_dict = pickle.load(open(fn, "rb"))
#
#
# class RankGOH(object):
#     """
#     use-case A.) find 'family' or higher TaxID for given TaxID
#     RankGOH = taxonomy.RankGOH(rank_='family') # initialize object and set rank Genus Or Higher to 'family' level
#     taxid_list = sorted(set(df['TaxID_LCA'].tolist())) # get list of TaxIDs to to initial lookup for
#     RankGOH.fill_dicts(taxid_list) --> has table for speed
#     df['TaxID_GOH'] = df['TaxID_LCA'].apply(RankGOH.get_genus_or_higher, 1) # get the 'family' level TaxID
#     use-case B.) is given TaxID child of TaxID
#     RankGOH = taxonomy.RankGOH(rank_='genus') # fast default due to pickled files
#     RankGOH.fill_parent_dict(df, taxid2compare_column='TaxID_LCA') # for speed
#     RankGOH.is_taxid_child_of_parentTaxID(df, taxid2compare_column='TaxID_LCA', taxid_parent=314295, colname_new='Hominoidea')
#     # also:
#     df["Rank_LCA"] = df["TaxID_LCA"].apply(RankGOH.get_rank, 1)
#     df['TaxID_GOH'] = df['TaxID_LCA'].apply(RankGOH.get_genus_or_higher, 1)
#
#     performs in-place changes to DataFrame (evidence.txt)
#     adds Rank of TaxID and counts genus_or_higher per rawfile
#     interacts with taxonomy module and R
#     speed up: perform lookup of set of TaxIDs --> PyDict, instead of individual lookups
#     if other rank than 'genus' is chosen. disable lookup in taxid2taxidGOH_dict
#     since this is prefilled with 'genus' parents and will give wrong answers.
#     TaxIDs throwing Errors:
#     5563
#     41402
#     451834
#     929613
#     73900
#     406678
#     1400050
#     227529
#     115136
#     117573
#     Viridiplantae 33090
#     Bacteria 2
#     Viruses 10239
#     Mammalia 40674
#     """
#     def __init__(self, pickled_dicts_fn=None, tax_=None, rank_="species"):
#         if tax_:
#             self.tax_ = tax_
#         else:
#             # self.tax_ = NCBI_taxonomy()
#             self.tax_ = NCBI_taxonomy_py()
#         self.rank = rank_
#         self.taxid2sciname_dict = {}
#         self.taxid2rank_dict = {}
#         self.taxid2taxidGOH_dict = {}
#         self.taxid2parents_dict = {} # key=TaxID, val=set(TaxIDs)
#         self.taxid2parent_of_rank_dict = {} # key=TaxID_Rank, val=TaxID
#         self.taxid2rank_closest_classified_dict = {1: 'root'} # key=TaxID, val=Rank (String)
#         self.homedir = os.path.expanduser("~")
#         if self.rank == "species":
#             if not pickled_dicts_fn:
#                 self.pickled_dicts_fn = os.path.join(self.homedir, "modules/cpr/metaprot/RankGOH_pickled_dicts.p")
#             else:
#                 self.pickled_dicts_fn = pickled_dicts_fn
#             if os.path.exists(self.pickled_dicts_fn):
#                 pickled_dicts = pickle.load( open(self.pickled_dicts_fn, "rb" ) )
#                 self.taxid2sciname_dict = pickled_dicts['taxid2sciname_dict']
#                 self.taxid2rank_dict = pickled_dicts['taxid_2_rank_dict']
#                 self.taxid2taxidGOH_dict = pickled_dicts['taxid2taxidGOH_dict']
#         self.taxid2sciname_dict[-1] = 'alien'
#         self.taxid2rank_dict[-1] = 'no rank'
#         self.taxid2taxidGOH_dict[-1] = -1
#
#     def set_df(self, df):
#         self.df = df
#
#     def taxid_list2pickle(self, taxid_list, pickle_fn=None):
#         """
#         e.g.
#         taxid2taxname_fn = r'/Users/dblyon/CloudStation/CPR/Ancient_Proteins_Project/fasta/TaxID/TaxID2TaxName_COMPLETE.txt'
#         taxid_2_taxname_dict = parse_taxid2taxname(taxid2taxname_fn)
#         taxid_list = taxid_2_taxname_dict.keys()
#
#         """
#         if pickle_fn:
#             self.pickled_dicts_fn = pickle_fn
#         for taxid in taxid_list:
#             try:
#                 self.fill_dicts([taxid])
#             except:
#                 print("#"*5)
#                 print("Taxid: ", taxid)
#                 print("#"*5)
#
#         dict2pickle = {
#             "taxid2sciname_dict": self.taxid2sciname_dict,
#             "taxid_2_rank_dict": self.taxid2rank_dict,
#             "taxid2taxidGOH_dict": self.taxid2taxidGOH_dict
#             }
#         pickle.dump(dict2pickle, open(os.path.join(self.homedir, 'modules/cpr/metaprot/RankGOH_pickled_dicts.p'), "wb"))
#
#     def yield_trsp_from_taxid_list(self, taxid_list):
#         for taxid in taxid_list:
#             if taxid == -1:
#                 rank = 'no rank'
#                 sciname = 'alien'
#                 taxid_goh = -1
#             else:
#                 rank = self.tax_.get_rank(taxid)
#                 sciname = self.tax_.get_sciname(taxid)
#                 taxid_goh = self.tax_.get_parent(taxid, rank=self.rank)
#                 if taxid_goh == taxid:
#                     rank_goh = rank
#                     sciname_goh = sciname
#                 else:
#                     rank_goh = self.tax_.get_rank(taxid_goh)
#                     sciname_goh = self.tax_.get_sciname(taxid_goh)
#             yield taxid, rank, sciname, taxid_goh, rank_goh, sciname_goh
#
#     def fill_dicts(self, taxid_list):
#         for taxid_rank_sciname_parenttaxid in self.yield_trsp_from_taxid_list(taxid_list):
#             taxid, rank, sciname, taxid_goh, rank_goh, sciname_goh = taxid_rank_sciname_parenttaxid
#
#             if not self.taxid2sciname_dict.has_key(taxid):
#                 self.taxid2sciname_dict[taxid] = sciname
#             if not self.taxid2sciname_dict.has_key(taxid_goh):
#                 self.taxid2sciname_dict[taxid_goh] = sciname_goh
#
#             if not self.taxid2rank_dict.has_key(taxid):
#                 self.taxid2rank_dict[taxid] = rank
#             if not self.taxid2rank_dict.has_key(taxid_goh):
#                 self.taxid2rank_dict[taxid_goh] = rank_goh
#
#             if not self.taxid2taxidGOH_dict.has_key(taxid):
#                 self.taxid2taxidGOH_dict[taxid] = taxid_goh
#
#     def get_rank(self, taxid):
#         try:
#             return self.taxid2rank_dict[taxid]
#         except KeyError:
#             rank = self.tax_.get_rank(taxid)
#             self.taxid2rank_dict[taxid] = rank
#             return rank
#
#     def get_rank_of_closest_classified(self, taxid):
#         """
#         produce rank of taxid or next highest rank that is NOT 'no rank'
#         :param taxid: TaxID (String or Int)
#         :return: String
#         """
#         try:
#             return self.taxid2rank_closest_classified_dict[taxid]
#         except KeyError:
#             rank = self.get_rank(taxid)
#             if not rank == "no rank":
#                 self.taxid2rank_closest_classified_dict[taxid] = rank
#                 return rank
#             else:
#                 taxid = self.tax_.get_parent(taxid)
#                 return self.get_rank_of_closest_classified(taxid)
#
#     def get_sciname(self, taxid):
#         try:
#             return self.taxid2sciname_dict[taxid]
#         except KeyError:
#             sciname = self.tax_.get_sciname(taxid)
#             self.taxid2sciname_dict[taxid] = sciname
#             return sciname
#
#     def get_parent(self, taxid):
#         """
#         produce TaxID of parent of rank 'genus' or whatever instance has been initialized with
#         else return given TaxID
#         """
#         try:
#             return self.taxid2taxidGOH_dict[taxid]
#         except KeyError:
#             parent = self.tax_.get_parent(taxid, rank=self.rank)
#             self.taxid2taxidGOH_dict[taxid] = parent
#             return parent
#
#     def get_genus_or_higher(self, taxid):
#         taxid_goh = self.get_parent(taxid)
#         if self.rank == self.get_rank(taxid_goh):
#             return taxid_goh
#         else:
#             return taxid
#
#     def get_all_parents(self, taxid):
#         return set(self.tax_.get_allparents(taxid))
#
#     def has_parent(self, taxid, taxid_parent):
#         """
#         if taxid2compare has parent taxid_parent
#         return True
#         else False
#         """
#         if taxid == -1:
#             return False
#         taxid2compare_parents = self.tax_.get_allparents(taxid)
#         if taxid_parent in set(taxid2compare_parents):
#             return True
#         else:
#             return False
#
#     def fill_parent_dict(self, df, taxid2compare_column):
#         """
#         fill dict with TaxIDs 2 all parents of TaxIDs
#         :param df: DataFrame
#         :param taxid2compare_column: String(Column name with TaxID)
#         :return: None
#         """
#         taxid2lookup = set(df[taxid2compare_column].tolist())
#         # if -1 in taxid2lookup: # alien entry, what about 0? #!!!
#         taxid2lookup.discard(-1)
#         self.taxid2parents_dict[-1] = set([])
#         taxid2lookup.discard(0)
#         self.taxid2parents_dict[0] = set([])
#         for taxid in taxid2lookup:
#             try:
#                 self.taxid2parents_dict[taxid] = set(self.get_all_parents(taxid))
#                 # include term itself
#                 # self.taxid2parents_dict[taxid] = set(list(self.get_all_parents(taxid)) + [taxid])
#             except:
#                 print("#####", taxid, "can't be retrieved")
#                 self.taxid2parents_dict[taxid] = {-12345} #RankGOH.taxid2parents_dict[72280] = {-12345}
#
#     def prepare_has_parent_speed(self, taxid_parent):
#         """
#         :param taxid_parent: Int(TaxID)
#         :return: None
#         """
#         self.taxid2parent_temp_dict = {}
#         for taxid in self.taxid2parents_dict:
#             if taxid_parent in self.taxid2parents_dict[taxid]:
#                 self.taxid2parent_temp_dict[taxid] = True
#             else:
#                 self.taxid2parent_temp_dict[taxid] = False
#
#     def has_parent_speed(self, taxid):
#         """
#         e.g.
#         RankGOH.fill_parent_dict(df, taxid2compare_column='TaxID_GOH') --> once only
#         df['Viridiplantae'] = df['TaxID_GOH'].apply(RankGOH.has_parent_speed, 1, args=(33090, ))
#         if taxid2compare has parent taxid_parent
#         return True
#         else False
#         """
#         return self.taxid2parent_temp_dict[taxid]
#
#     def is_taxid_child_of_parentTaxID(self, df, taxid2compare_column, taxid_parent, colname_new):
#         """
#         convenience function
#         produce Boolean in colname_new if TaxID (in taxid2compare_column) has taxid_parent as a parent
#         e.g.
#         RankGOH.fill_parent_dict(df, taxid2compare_column='TaxID_GOH')
#         RankGOH.is_taxid_child_of_parentTaxID(df, taxid2compare_column='TaxID_GOH', taxid_parent=33090, colname_new='Viridiplantae')
#         RankGOH.is_taxid_child_of_parentTaxID(df, taxid2compare_column='TaxID_GOH', taxid_parent=2, colname_new='Bacteria')
#         RankGOH.is_taxid_child_of_parentTaxID(df, taxid2compare_column='TaxID_GOH', taxid_parent=10239, colname_new='Viruses')
#         RankGOH.is_taxid_child_of_parentTaxID(df, taxid2compare_column='TaxID_GOH', taxid_parent=40674, colname_new='Mammalia')
#         RankGOH.is_taxid_child_of_parentTaxID(df, taxid2compare_column='TaxID_GOH', taxid_parent=314295, colname_new='Hominoidea')
#         RankGOH.is_taxid_child_of_parentTaxID(df, taxid2compare_column='TaxID_GOH', taxid_parent=9526, colname_new='Catarrhini') # primates
#         """
#         self.prepare_has_parent_speed(taxid_parent)
#         df[colname_new] = df[taxid2compare_column].apply(self.has_parent_speed, 1)
#
#     def get_parent_of_rank(self, taxid, rank):
#         """
#         produce TaxID of given rank of given taxid
#         :param taxid: String or Int
#         :param rank: String
#         :return: Int
#         """
#         taxid_rank = str(taxid) + "_" + rank
#         try:
#             return self.taxid2parent_of_rank_dict[taxid_rank]
#         except KeyError:
#             parent = self.tax_.get_parent(taxid, rank=rank)
#             self.taxid2parent_of_rank_dict[taxid_rank] = parent
#             return parent
#
#     def unpickle_taxid2parent_of_rank_dict_from_file(self, fn):
#         self.taxid2parent_of_rank_dict = pickle.load(open(fn, "rb"))
#
#
# def get_tax_RankGOH_objects():
#     tax = NCBI_taxonomy()
#     RankGOH_ = RankGOH(tax_=tax)
#     return tax, RankGOH_
#
# def get_pickled_tax_RankGOH():
#     tax = NCBI_taxonomy()
#     RankGOH_ = RankGOH(tax_=tax)
#     fn = r'/Users/dblyon/modules/cpr/metaprot/taxdump/taxid2taxnamesfl_dict.p'
#     tax.unpickle_taxid2taxnamesfl_dict_from_file(fn)
#     fn = r'/Users/dblyon/modules/cpr/metaprot/taxdump/taxid2parent_of_rank_dict.p'
#     tax.unpickle_taxid2parent_of_rank_dict_from_file(fn)
#     fn = r'/Users/dblyon/modules/cpr/metaprot/taxdump/taxid2rank_closest_classified_dict.p'
#     tax.unpickle_taxid2rank_closest_classified_dict_from_file(fn)
#     fn = r'/Users/dblyon/modules/cpr/metaprot/taxdump/taxid2taxid_closest_classified_dict.p'
#     tax.unpickle_taxid2taxid_closest_classified_dict_from_file(fn)
#     return tax, RankGOH_
#
# def add_HomoBacOther_setCatarrhini2Homo_TaxNameSpeciesGenus(df, taxid2compare_column='TaxID_LCA', taxname2compare_column='TaxName_LCA', int_or_str="int", rank_list=("superkingdom", "family", "genus", "species")):
#     if int_or_str == "str":
#         df[taxid2compare_column] = df[taxid2compare_column].astype(int)
#     tax, RankGOH_ = get_tax_RankGOH_objects()
#     # df = set_Catarrhini2Homo(df, RankGOH_, taxid2compare_column, taxname2compare_column, int_or_str)
#     df = set_Catarrhini2Homo(df, RankGOH_, taxid2compare_column, taxname2compare_column) #, int_or_str)
#
#     df = add_col_parent_of_rank(df, tax, colname_taxid="TaxID_LCA", rank_list=rank_list)
#     # add columns with TaxNames for genus and species
#     for rank in rank_list:
#         df['TaxName_{}'.format(rank)] = df[rank].apply(RankGOH_.get_sciname, 1)
#
#     # df['TaxName_species'] = df['species'].apply(RankGOH_.get_sciname, 1)
#     # df['TaxName_genus'] = df['genus'].apply(RankGOH_.get_sciname, 1)
#
#     df = homo_vs_bacteria_vs_other_add_column(df)
#     if int_or_str == "str":
#         df[taxid2compare_column] = df[taxid2compare_column].astype(str)
#     return df
#
# def set_Catarrhini2Homo(df, RankGOH_, taxid2compare_column='TaxID_LCA', taxname2compare_column='TaxName_LCA', int_or_str="int"):
#     # add Catarrhini column
#     # if TaxID_LCA is child of Catarrhini
#     if int_or_str == "str":
#         df[taxid2compare_column] = df[taxid2compare_column].astype(int)
#     RankGOH_.fill_parent_dict(df, taxid2compare_column)
#     RankGOH_.is_taxid_child_of_parentTaxID(df, taxid2compare_column, taxid_parent=9526, colname_new='Catarrhini')
#     # if TaxID_LCA itself is Catarrhini (not just child)
#     df.loc[df[taxid2compare_column] == 9526, "Catarrhini"] = True
#     # set all Catarrhini to Homo sapiens
#     df.loc[df["Catarrhini"], taxid2compare_column] = 9606
#     df.loc[df["Catarrhini"], taxname2compare_column] = "Homo sapiens"
#     df.drop("Catarrhini", axis=1, inplace=True)
#     if int_or_str == "str":
#         df[taxid2compare_column] = df[taxid2compare_column].astype(str)
#     return df
#
# def homo_vs_bacteria_vs_other_add_column(df):
#     df['Homo_Bac_Other'] = "Other"
#     cond = df['species'] == 9606
#     df.loc[cond, 'Homo_Bac_Other'] = "Homo"
#     cond = df['superkingdom'] == 2
#     df.loc[cond, 'Homo_Bac_Other'] = "Bacteria"
#     return df
#
# def add_col_parent_of_rank(df, tax, colname_taxid="TaxID_LCA", rank_list=("superkingdom", "family", "genus", "species")):
#     """
#     add columns of names in rank_list, from TaxID in colname_taxid find TaxID of given rank
#     :param df:
#     :param tax:
#     :param colname_taxid:
#     :param rank_list:
#     :return:
#     """
#     for rank in rank_list:
#         df[rank] = df[colname_taxid].apply(tax.get_parent_of_rank, 1, args=(rank, ))
#     return df
#
# def add_TaxNameSpeciesGenus(df, taxid2compare_column='TaxID_LCA', int_or_str="int"):
#     if int_or_str == "str":
#         df[taxid2compare_column] = df[taxid2compare_column].astype(int)
#     tax, RankGOH_ = get_tax_RankGOH_objects()
#     df = add_col_parent_of_rank(df, tax, colname_taxid=taxid2compare_column)
#     # add columns with TaxNames for genus and species
#     df['TaxName_species'] = df['species'].apply(RankGOH_.get_sciname, 1)
#     df['TaxName_genus'] = df['genus'].apply(RankGOH_.get_sciname, 1)
#     if int_or_str == "str":
#         df[taxid2compare_column] = df[taxid2compare_column].astype(str)
#     return df
#
#
# if __name__ == "__main__":
#     print(os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
#     tax = NCBI_taxonomy()
#     fn_out = r"/Users/dblyon/modules/cpr/metaprot/psql/Taxa_table.txt"
#     tax.write_Taxa_table_for_SQL(fn_out)
#     fn_out = r"/Users/dblyon/modules/cpr/metaprot/psql/TaxonChild_2_TaxonParent_table.txt"
#     tax.write_TaxonChild_2_TaxonParent_table_for_SQL(fn_out)
