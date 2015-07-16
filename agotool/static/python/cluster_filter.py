import pandas as pd
import itertools
import shlex
import subprocess
import os


class MCL(object):

    def __init__(self):
        # self.set_fh_log(os.path.dirname(os.getcwd()) + r'/data/mcl/mcl_log.txt')
        self.abs_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + r'/data/mcl/'
        self.set_fh_log(self.abs_path + 'mcl_log.txt')

    def set_fh_log(self, log_fn):
        self.fh_log = open(log_fn, "a")

    def get_fh_log(self):
        return self.fh_log

    def close_log(self):
        self.get_fh_log().flush()
        self.get_fh_log().close()

    def jaccard_index_ans_setA2B(self, ans_set1, ans_set2):
        B = float(len(ans_set1.intersection(ans_set2)))
        ABC = len(ans_set1.union(ans_set2))
        try:
            return B/ABC
        except ZeroDivisionError:
            return 0.0

    def write_JaccardIndexMatrix(self, df, fn_out):
        """
        expects a DataFrame with a 'ANs_study' column,
        calculates the Jaccard Index for all
        combinations of AN sets.
        :param df: DataFrame
        :param fn_out: rawString
        :return: None
        """
        func = lambda x: set(x.split(","))
        df["ANs_study_set"] = map(func, df["ANs_study"])
        index_of_col = df.columns.tolist().index("ANs_study_set")
        df_ans_study_set = df.values[:, index_of_col]
        with open(fn_out, 'w') as fh:
            for combi in itertools.combinations(df.index, 2):
                c1, c2 = combi
                ans_set1 = df_ans_study_set[c1]
                ans_set2 = df_ans_study_set[c2]
                ji = self.jaccard_index_ans_setA2B(ans_set1, ans_set2)
                line2write = str(c1) + '\t' + str(c2) + '\t' + str(ji) + '\n'
                fh.write(line2write)

    def mcl_cluster2file(self, mcl_in, inflation_factor, mcl_out):
        cmd_text = """mcl %s -I %d --abc -o %s""" % (mcl_in, inflation_factor, mcl_out)
        args = shlex.split(cmd_text)
        ph = subprocess.Popen(args, stdin=None, stdout=self.get_fh_log(), stderr=self.get_fh_log())
        self.get_fh_log().flush()
        return ph.wait()

    def get_clusters(self, mcl_out):
        """
        parse MCL output
        returns nested list of strings
        [
        ['1', '3', '4'],
        ['2', '5']
        ]
        :param mcl_out: rawFile
        :return: ListOfListOfString
        """
        cluster_list = []
        with open(mcl_out, 'r') as fh:
            for line in fh:
                cluster_list.append(line.strip().split('\t'))
        return cluster_list

    def calc_MCL_get_clusters(self, fn_results, inflation_factor=2.0):
        df = pd.read_csv(fn_results, sep='\t')
        mcl_in = self.abs_path + 'mcl_in.txt'
        mcl_out = self.abs_path + 'mcl_out.txt'
        self.write_JaccardIndexMatrix(df, mcl_in)
        self.mcl_cluster2file(mcl_in, inflation_factor, mcl_out)
        return self.get_clusters(mcl_out)


class Filter(object):

    def __init__(self, go_dag):
        self.go_lineage_dict = {}
        # key=GO-term, val=set of GO-terms
        for go_term_name in go_dag:
            GOTerm_instance = go_dag[go_term_name]
            self.go_lineage_dict[go_term_name] = GOTerm_instance.get_all_parents().union(GOTerm_instance.get_all_children())

    def filter_term_lineage(self, header, results, indent):
        """
        produce reduced list of results
        from each GO-term lineage (all descendants (children) and ancestors
        (parents), but not 'siblings') pick the term with the lowest p-value.
        :param header: String
        :param results: ListOfString
        :param indent: Bool
        :return: ListOfString
        """
        results_filtered = []
        blacklist = set(["GO:0008150", "GO:0005575", "GO:0003674"])
        # {"BP": "GO:0008150", "CP": "GO:0005575", "MF": "GO:0003674"}
        index_p = header.index('p_uncorrected')
        index_go = header.index('id')
        results.sort(key=lambda x: float(x[index_p]))
        for res in results:
            if indent:
                dot_goterm = res[index_go]
                goterm = dot_goterm[dot_goterm.find("GO:"):]
                if not goterm in blacklist:
                    results_filtered.append(res)
                    blacklist = blacklist.union(self.go_lineage_dict[goterm])
            else:
                if not res[index_go] in blacklist:
                    results_filtered.append(res)
                    blacklist = blacklist.union(self.go_lineage_dict[res[index_go]])
        return results_filtered


if __name__ == "__main__":
    pass
    # fn = r'/Users/dblyon/modules/cpr/goterm/mcl/Yeast_Acetyl_vs_AbCorr_UPK.txt'
    # mcl_in = 'mcl_in.txt'
    # df = pd.read_csv(fn, sep='\t')
    # mcl = MCL()
    # mcl.write_JaccardIndexMatrix(df, mcl_in)
    # mcl_out = mcl_in.replace('_in.txt', '_out.txt')
    # inflation_factor = 2.0
    # mcl.mcl_cluster2file(mcl_in, inflation_factor, mcl_out)
    # cluster_list = mcl.get_clusters(mcl_out)

    # fn = r'/Users/dblyon/modules/cpr/goterm/mcl/Yeast_Acetyl_vs_AbCorr_UPK.txt'
    # mcl = MCL()
    # cluster_list = mcl.calc_MCL_get_clusters(fn, inflation_factor=2.0)
