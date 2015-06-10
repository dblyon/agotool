import os, re, goatools

ASSOCIATIONS = 'static/data/associations/%s'
UNIPROT_GOTERMS = 'static/data/uniprot_go'
OBO_FILE = 'static/data/go-basic.obo'

def update_data(input_ids, assoc, base_assoc):
    ids = set()
    for line in input_ids.split('\n'):
        if line:
            _id, site = line.strip().split()
            assoc['%s_%s' % (_id, site)] = base_assoc[_id]
            ids.add(_id)
    return ids

def read_associations(assoc_fn):
    assoc = {}
    for row in open(assoc_fn):
        atoms = row.split()
        if len(atoms) == 2:
            a, b = atoms
        elif len(atoms) > 2 and row.count('\t') == 1:
            a, b = row.split("\t")
        else:
            continue
        b = set(b.split(";"))
        assoc[a] = b
    return assoc
    # results, header = penrichment.run(
    #     form.organism.data, form.catagories.data,
    #     form.forground_textarea.data, form.background_textarea.data,
    #     form.alpha.data, form.correction_method.data
    # )

def run(organism, catagories, fg, bg, alpha, min_ratio, correction='fdr'):
    # goatools assumes that every gene is a count rather than every
    # site we fudge this by making a association record with name:
    # ID_SITE, with association equal to the ID

    base_assoc_file = open(ASSOCIATIONS % organism, 'r')
    base_assoc_file.readline()
    base_assoc = {}
    for line in base_assoc_file:
        _id, bp, cc, mf = line.rstrip('\r\n').split('\t')
        _sets = set(bp.split(';')) | set(cc.split(';')) | set(mf.split(';'))
        base_assoc[_id] = _sets

    assoc = {}
    study = update_data(bg, assoc, base_assoc)
    pop   = update_data(fg, assoc, base_assoc)

    obo_dag = goatools.obo_parser.GODag(obo_file=OBO_FILE)
    g = goatools.GOEnrichmentStudy(
            pop, assoc, obo_dag, alpha=alpha, study=study,
    #        methods=["bonferroni", "sidak", "holm", "fdr"]
            methods=["bonferroni", "sidak", "holm"]
    )

    header = goatools.GOEnrichmentRecord()._fields
    results = []
    for rec in g.results:
        rec.update_remaning_fields(min_ratio=min_ratio)

        if (rec.__dict__['p_%s' % correction.lower()] < alpha and
                rec.is_ratio_different):
            data = [rec.__dict__[f] for f in header]
            results.append(data)
    return results, header



################################################################################
# all thise functions are used to generate the uniprot -> goterm associations
# they are used when the script started instead of imported
# ################################################################################

def get_top_nodes(node):
    top_nodes = set()

    def get_parents(node):
        if node.parents == []:
            top_nodes.add(node.id)
        else:
            for n in node.parents:
                get_parents(n)

    get_parents(node)
    return top_nodes



if __name__ == '__main__':

    root_term_meaning = {
        "GO:0008150" : "BP", "GO:0005575" : "CP", "GO:0003674" : "MF"
    }

    obo_dag = goatools.obo_parser.GODag(obo_file=OBO_FILE)
    for go_file_path in os.listdir(UNIPROT_GOTERMS):
        match = re.search(r"uniprot-organism%3A(\d+).tab", go_file_path)
        if match:
            organism = match.groups()[0]
            association_file = open (ASSOCIATIONS % organism, 'w')
            header = ["uniprot ID", "Biological Processes", "Celluar Compartments", "Molecular Function"]
            association_file.write("%s\n" % "\t".join(header))

            print "PARSING", go_file_path
            with open(os.path.join(UNIPROT_GOTERMS, go_file_path), 'r') as go_file:
                go_file.readline()
                for line in go_file:
                    entry, organism, go_descriptions, go_terms, status = line.strip().split('\t')
                    terms = {"BP" : [], "CP" : [], "MF" : []}
                    for go_term in go_terms.split('; '):
                        if go_term:
                            go_term = obo_dag[go_term]
                            if not go_term.is_obsolete:
                                for parent in get_top_nodes(go_term):
                                    terms[root_term_meaning[parent]].append(go_term.id)

                    bp, cp, mf = [';'.join(terms[key]) for key in ("BP", "CP", "MF")]
                    association_file.write('%s\n' % '\t'.join((entry, bp, cp, mf)))
            association_file.close()








    # get go terms from uniprot

