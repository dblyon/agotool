__author__ = 'dblyon'
# assoc is a dict: key=AN, val=set of go-terms

class UniProt_keywords_parser(object):

    def __init__(self, uniprot_keywords_fn):
        self.assoc_dict = self.parse_file(uniprot_keywords_fn)

    def parse_file(self, fn): #!!!
        assoc_dict = {}
        with open(fn, 'r') as fh:
            for line in fh:
                line_split = line.split('\t')
                an = line_split[0]
                keywords = set([ele.strip() for ele in line_split[-1].split(';')])
                assoc_dict[an] = keywords
        return assoc_dict

    def get_association_dict(self):
        '''
        assoc is a dict: key=AN, val=set of go-terms
        :return: Dict
        '''
        return self.assoc_dict

