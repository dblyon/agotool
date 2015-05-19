import cPickle as pickle
import pandas as pd
import numpy as np

__author__ = 'dblyon'

# parse UniProt goa_ref files
# check if all AccessionNumbers have at least one GO-term, if not manual check if true

class Goretriever(object):
    """
    parse UniProt goa_ref files retrieved from ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/
    # e.g. gene_association.goa_ref_yeast
    # additional info http://www.geneontology.org/doc/GO.references
    produce list of GO-terms associated with given AccessionNumber
    """

    def __init__(self):
        """
        :return: None
        """
        self.an2go_dict = {} # key=AccessionNumber val=ListOfStrings (GO-terms)
        self.date = "not set yet" # generation date
        self.obolibrary = "not yet set" # link to obo-library

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

    def parse_goa_ref(self, fn):
        """
        parse UniProt goa_ref file filling self.an2go_dict
        :param fn: raw String
        :return: None
        """
        fh = open(fn, "r")
        for line in fh:
            if line[0] == "!":
                if line[0:11] == "!Generated:":
                    self.date = line.replace("!Generated:", "").strip()
                elif line[0:12] == "!GO-version:":
                    self.obolibrary = line.replace("!GO-version:", "").strip()
            else:
                line_split = line.split("\t")
                if len(line_split) == 17:
                    an = line_split[1] # DB_Object_ID
                    goid = line_split[4] # GO_ID
                    if not self.an2go_dict.has_key(an):
                        self.an2go_dict[an] = [goid]
                    else:
                        self.an2go_dict[an].append(goid)
        self.remove_redundant_go_terms()
        fh.close()

    def remove_redundant_go_terms(self):
        """
        remove redundant go-terms for each AccessionNumber if present
        and sort list of go-terms
        :return: None
        """
        for an in self.an2go_dict.keys():
            self.an2go_dict[an] = sorted(set(self.an2go_dict[an]))

    def pickle(self, fn_p):
        """
        pickle relevant attributes to given FileName
        :param fn_p: raw String
        :return: None
        """
        dict2pickle = {}
        dict2pickle["an2godict"] = self.an2go_dict
        dict2pickle["date"] = self.date
        dict2pickle["obolibrary"] = self.obolibrary
        pickle.dump(dict2pickle, open(fn_p, "wb"))
        del dict2pickle

    def unpickle(self, fn_p):
        """
        unpickle and set relevant attributes to instance
        :param fn_p: raw String
        :return: None
        """
        dict2pickle = pickle.load(open(fn_p, "rb"))
        self.an2go_dict = dict2pickle["an2godict"]
        self.date = dict2pickle["date"]
        self.obolibrary = dict2pickle["obolibrary"]
        del dict2pickle

class UpdateRescources(object):
    """
    retrieve updated resources from UniProt FTP and geneontology.org
    ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/ --> e.g. gene_association.goa_ref_yeast
    and e.g. http://purl.obolibrary.org/obo/go/releases/2015-04-25/go.owl
    """

    def __init__(self):
        pass

class UserInput(object):
    """
    expects 2 arrays,
    samplefreq: 1D array
    backgrndfreq: 2D array/Pandas DataFrame, with backgrnd_an, backgrnd_int
    """
    def __init__(self):
        #self.samplefreq = pd.Series()
        #self.backgroundfreq = pd.DataFrame()
        pass


    def temp_setup(self):
        fn=r"C:\Users\dblyon\CloudStation\CPR\Brian_GO\UserInput.txt"
        df = pd.read_csv(fn, sep="\t")
        cond = pd.isnull(df["sample_an"])
        self.samplefreq = df.loc[-cond, "sample_an"].drop_duplicates().copy() # copy probably not necessary
        self.backgroundfreq = df.loc[:, ["backgrnd_int", "backgrnd_an"]].drop_duplicates(subset="backgrnd_an").copy()



