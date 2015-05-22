import cPickle as pickle
import pandas as pd
#import numpy as np

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

    def get_ans(self):
        '''
        produce List of AccessionNumbers
        :return: ListOfString
        '''
        return sorted(self.an2go_dict)

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

    def write_association2file(self, fn_out):
        '''
        produce input file for goatools termed 'association'
        containing all AccessionNumbers of theoretical proteome and
        their corresponding GO-IDs
        e.g.:
        AN tab GO-id1;GO-id2;GO-id3
        ACD5	GO:0005575;GO:0003674;GO:0008219
        :param fn_out: rawString
        :return: None
        '''
        with open(fn_out, 'w') as fh_out:
            for an in self.get_ans():
                go_list = self.get_goterms_from_an(an)
                if go_list == -1:
                    pass # #!!! should there be a default value instead?
                else:
                    fh_out.write(an + '\t' + ';'.join(go_list) + '\n')


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
    samplefreq: Pandas DataFrame 1column
    backgrndfreq: 2D array/Pandas DataFrame, with backgrnd_an, backgrnd_int
    """
    def __init__(self):
        #self.samplefreq = pd.DataFrame()
        #self.backgroundfreq = pd.DataFrame()
        pass

    def temp_setup(self):
        #fn=r"C:\Users\dblyon\CloudStation\CPR\Brian_GO\UserInput.txt"
        fn=r"/Users/dblyon/CloudStation/CPR/Brian_GO/UserInput.txt"
        self.df_orig = pd.read_csv(fn, sep="\t")

    def cleanupforanalysis(self):
        '''
        reduce to non-redundant AccessionNumbers for sample and background-frequency (uses first observed row),
        remove ANs without GO-term(s)
        remove ANs without intensity-values
        concat and align data to single DataFrame
        :return: None
        '''
        cond = pd.isnull(self.df_orig["sample_an"])
        # remove duplicate AccessionNumbers from samplefrequency and backgroundfrequency
        self.samplefreq_ser = self.df_orig.loc[-cond, "sample_an"].drop_duplicates().copy() # copy probably not necessary
        self.backgroundfreq_df = self.df_orig.loc[:, ["backgrnd_an", "backgrnd_int"]].drop_duplicates(subset="backgrnd_an").copy()
        # concatenate data
        self.df = self.concat_and_align_sample_and_background(self.samplefreq_ser, self.backgroundfreq_df)
        # remove AccessionNumbers from sample and background-frequency without intensity values
        self.df  = self.df.loc[pd.notnull(self.df['backgrnd_int']), ]
        self.set_study(self.df.loc[pd.notnull(self.df['sample_an']), 'sample_an'])
        self.set_population(self.df[['backgrnd_int', 'backgrnd_an']])

    def set_study(self, series):
        self.samplefreq_ser =  series

    def get_study(self):
        '''
        return sample frequency (termed 'study' in goatools)
        :return: ListOfString
        '''
        return sorted(self.samplefreq_ser.tolist())

    def set_population(self, population):
        self.backgroundfreq_df = population

    def get_population(self):
        '''
        return background frequency (termed 'population' in goatools)
        :return: ListOfString
        '''
        return sorted(self.backgroundfreq_df['backgrnd_an'].tolist())

    def write_goatools_input2file(self, fn_study, fn_pop):
        '''
        write input files for goatools termed study (sample-frequency) and population (background-frequency)
        consisting of AccessionNumbers (one per line)
        :param fn_study: rawString
        :param fn_pop: rawString
        :return: None
        '''
        with open(fn_study, 'w') as fh_study:
            for an in self.get_study():
                fh_study.write(an + '\n')
        with open(fn_pop, 'w') as fh_pop:
            for an in self.get_population():
                fh_pop.write(an + '\n')

    def remove_ans_without_go_or_int(self, gor):
        '''
        remove AccessionNumbers without GO-term or without intensity value
        change attributes of UserInput instance
        :param gor: goretriever instance
        :return: None
        '''
        ans_sample_filtered = []
        for an in self.get_study():
            goterm_list = gor.get_goterms_from_an(an)
            cond = self.backgroundfreq_df['backgrnd_an'] == an
            intensity_valinlist = self.backgroundfreq_df.loc[cond, 'backgrnd_int'].tolist()
            if goterm_list != -1 and len(intensity_valinlist) != 0:
                ans_sample_filtered += an

    def concat_and_align_sample_and_background(self, sample_ser, background_df):
        '''
        expects a Series and a DataFrames each containing a column with non-redundant
        AccessionNumbers, concatenate by producing the union and aligning the ANs in rows
        :param sample_ser: Pandas.Series
        :param background_df: Pandas.DataFrame
        :return: DataFrame
        '''
        sample_ser.index = sample_ser.tolist()
        background_df.index = background_df['backgrnd_an'].tolist()
        return pd.concat([sample_ser, background_df], axis=1)




if __name__ == "__main__":
    pass
    ##### parse UniProt goa or goa_ref file and create input file for goatools (association-file)
    ##### with AN tab GO-IDs
    # gor = Goretriever()
    # #fn=r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/UniProt_goa/yeast/gene_association.goa_yeast'
    # fn=r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/UniProt_goa/human/gene_association.goa_ref_human'
    # gor.parse_goa_ref(fn)
    # #fn_out = r'/Users/dblyon/CloudStation/CPR/Brian_GO/goatools/data/association_goa_yeast'
    # fn_out = r'/Users/dblyon/CloudStation/CPR/Brian_GO/goatools/data/association_goa_ref_human'
    # gor.write_association2file(fn_out)

