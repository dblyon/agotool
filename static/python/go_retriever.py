import sys, os
PYTHON_DIR = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
sys.path.append(PYTHON_DIR)
import obo_parser
STATIC_DIR = os.path.abspath(os.path.join(PYTHON_DIR, '..'))
FN_P_PARSER_GO_ANNOTATIONS = os.path.abspath(os.path.join(STATIC_DIR, "data/GOA/Parser_GO_annotations.p"))


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
    # get the direct ancestors, i.e. those that are not covered by an    earlier
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

def get_description(goid, go_dag):
    """
    e.g. dfx['description'] = dfx["GOid"].apply(get_description, args=(go_dag, ))
    """
    return go_dag[goid].name

def get_level(goid, go_dag):
    return go_dag[goid].level


if __name__ == "__main__":
################################################################################
### try new HOMD_GOA.tsv
    # pgoa = Parser_GO_annotations()
    # fn = r'/Users/dblyon/modules/cpr/agotool/static/data/GOA/HOMD_GOA_commasepnotlong.tsv'
    # fn = r'/Users/dblyon/modules/cpr/agotool/static/data/GOA/HOMD_GOA.tsv'
    # pgoa.parse_goa_ref(fn, organisms_set=None)
    print(os.path.abspath(os.path.realpath(__file__)))
    print(obo_parser)

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
