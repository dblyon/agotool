
import os
import collections
import re
import argparse


######################################################################
# GLOBALS
######################################################################
LOOP_TSV = 'static/data/loop.tsv'
DEBUG = True

UNIPROT_TSV = 'static/data/uniprot-annotation%3A%28type%3A%22positional+domain%22+AND+%22protein+kinase%22%--.tab'
UNIPROT_FASTA = 'static/data/uniprot-annotation%3A%28type%3A%22positional+domain%22+AND+%22protein+kinase%22%--.fasta'


######################################################################
# Helper functions
######################################################################
def diggest(proteins, max_miss_cleavges, cleavage_res='RK', cut_after=True):
    # sets in the rare case that 2 peptides hit the same protein
    peptides = collections.defaultdict(set)
    # alphabet = set('ACDEFGHIKLMNPQRSTVWY')
    offset = int(cut_after) # if cutafter = True, offset = 1
    for name, protein in proteins.items():
        # We use Trypsine/P (no proline exception)
        # decoy = reverse all between RK, swap R and K
        c = n = -1
        tmp_peptides = []
        flag = True
        while flag:
            i = c + 1
            n = c

            # _c/cs and _n/ns referes to the n-term and c-term indexes
            cs = [protein.find(aa, i) for aa in cleavage_res]
            cs = [_c for _c in cs if _c != -1]

            _n = n + offset
            if cs == []:
                seq = protein[_n:]
                flag = False
            else:
                c = min(cs)
                _c = c + offset
                seq = protein[_n:_c]
            if seq != '':
                tmp_peptides.append(seq)

        for i in range(1, max_miss_cleavges+2):
            for j in range(len(tmp_peptides)):
                p = ''.join(tmp_peptides[j:j+i])
                peptides[p].add(name)
    return dict(peptides)


def get_hashes(target_organism):
    gene_hash, start_hash, end_hash = {}, {}, {}
    loop_hash, tryptic_loop_hash, description_hash = {}, {}, {}
    _file = open(LOOP_TSV)
    _file.readline()
    for line in _file:

        acc, gene, description, organism, start, end, loop_seq, loop_seq_tryptic = line.rstrip('\n').split('\t')
        if int(organism) == target_organism:
            gene_hash[acc] = gene
            start_hash[acc] = int(start)
            end_hash[acc] = int(end)
            loop_hash[acc] = loop_seq
            tryptic_loop_hash[acc] = loop_seq_tryptic
            description_hash[acc] = description
    return gene_hash, description_hash, start_hash, end_hash, loop_hash, tryptic_loop_hash


def fasta_to_hash(fasta_file, inclusion):
    proteins = collections.defaultdict(str)
    for line in open(fasta_file):
        if line[0] == '>':
            acc = re.search('>..\|([\w\d]+)|[\w\d_]+', line).groups()[0]
            write_flag = acc in inclusion
        elif write_flag:
            proteins[acc] += line.strip()
    return dict(proteins)

######################################################################
# envoked from flask
######################################################################
def parse_peptides(data, organism, clevage_res='RK', missed_clevages=2, cut_after=True):
    # what I am doing here is not 'super fast'
    # a faster approach would be to diggest the proteins, and make a
    # hash of the peptides, ie O(1) instead of n * m, where
    # n = number of proteins and m is the number og amino acids pr protein

    gene_hash, description_hash, start_hash, end_hash, loop_hash, tryptic_loop_hash = get_hashes(int(organism))
    kinases = fasta_to_hash(UNIPROT_FASTA, gene_hash)
    peptides = diggest(kinases, missed_clevages, clevage_res, cut_after)

    loop_result = collections.defaultdict(list)
    kinase_result = collections.defaultdict(list)
    seq_result = collections.defaultdict(list)
    # seq_loop_result = collections.defaultdict(list)
    # seq_kinase_result = collections.defaultdict(list)
    errors = [] # no error handling :D

    _from, _to = ord('a'), ord('z')
    for seq in data.split('\n'):
        # expand this to also work with PEPpTIDE, PEPT(Ph)IDE
        seq = seq.strip('\r\t _')
        u_seq = seq.upper()
        accs = peptides.get(u_seq)
        if accs:
            local_indexs = [i for (i, aa) in enumerate(seq) if _from < ord(aa) < _to]
            for acc in accs:
                _start, _end = start_hash[acc], end_hash[acc]
                index = kinases[acc].find(u_seq)
                for local_index in local_indexs:
                    pos = local_index + index + 1
                    print pos
                    if _start <= pos <= _end:
                        loop_result[acc].append(pos)
                        kinase_result[acc].append('')
                    else:
                        kinase_result[acc].append(pos)
                        loop_result[acc].append('')
                    seq_result[acc].append(seq)

    # convert to normal dict, because the sorting creates keys in default dict :S
    print kinase_result
    print loop_result
    print
    loop_result = dict(loop_result)
    kinase_result = dict(kinase_result)
    accs = list(set(loop_result.keys()) | set(kinase_result.keys()))
    accs.sort(key=lambda x : (-len(loop_result[x]), -len(kinase_result[x])))

    return [(acc, gene_hash[acc], loop_result[acc], kinase_result[acc],
             seq_result[acc], description_hash[acc]) for acc in accs], errors

    # print kinase_result
    # print loop_result
    # print loop_result.get(acc, ([], [])), kinase_result.get(acc, ([], []))
    # print '-' * 60
    #
    # return [(acc, gene_hash[acc], loop_result.get(acc, ([], [])), kinase_result.get(acc, ([], [])),
    #          description_hash[acc]) for acc in accs], errors

def parse_positions(data, organism):
    gene_hash, description_hash, start_hash, end_hash = get_hashes(int(organism))[:4]
    kinases = fasta_to_hash(UNIPROT_FASTA, gene_hash)
    errors = []

    loop_result = collections.defaultdict(list)
    kinase_result = collections.defaultdict(list)
    for i, line in enumerate(data.split('\n')):
        match = re.search('^([^\s]+).+?(\d+).*?', line)
        if match:
            acc, pos = match.groups()
            if acc in gene_hash:
                pos = int(pos)
                aa = kinases[acc][pos+1]
                if aa not in 'STY':
                    errors.append('Possition %i is a "%s" in uniprot' % (pos, aa))
                else:
                    if start_hash[acc] <= pos <= end_hash[acc]:
                        loop_result[acc].append('%s%i' % (aa, pos))
                    else:
                        kinase_result[acc].append(('%s%i' % (aa, pos)))
        else:
            if not re.search("^\s*#*$", line):
                errors.append('could not parse line %i: "%s"' % (i, line))

    accs = list(set(loop_result.keys()) | set(kinase_result.keys()))
    accs.sort(key=lambda x : (-len(loop_result[x]), -len(kinase_result[x])))
    return [(acc, gene_hash[acc], loop_result[acc], kinase_result[acc], description_hash[acc]) for acc in accs], errors


######################################################################
# used to generate the data
######################################################################
def generate_data(uniprot_tsv, uniprot_fasta):
    ######################################################################
    # Parse uniprot tsv
    ######################################################################
    acc_to_domain = collections.defaultdict(list)
    uniprot_tsv = open(uniprot_tsv)
    uniprot_tsv.readline()
    acc_to_species = {}
    acc_to_gene = {}
    acc_to_description = {}
    # reviewed = {}
    model_organisms = {10090, 10116, 3702, 4932, 6239, 7227, 7955, 8364, 9031, 9606, 9913}
    for line in uniprot_tsv:
        acc, entry_name, protein_description, gene, organism, organism_id, domains, status = line.rstrip('\r\n').split('\t')
        for domain in domains.split('; '):
            match = re.search(r'DOMAIN (\d+) (\d+) Protein kinase.+', domain)
            # reviewed[acc] = status == 'reviewed'
            if match and int(organism_id) in model_organisms and status == 'reviewed':
                acc_to_domain[acc].append(map(int, match.groups()))
                acc_to_species[acc] = int(organism_id)
                acc_to_gene[acc] = gene
                acc_to_description[acc] = protein_description
    ######################################################################
    # Parse uniprot fasta
    ######################################################################
    kinase_domain_fasta = open('static/data/kinase_domains.fasta', 'w')
    kinase_fasta = open('static/data/kinases.fasta', 'w')
    proteins = collections.defaultdict(str)
    proteins = fasta_to_hash(uniprot_fasta, acc_to_domain)
    # for line in uniprot_fasta:
    #     if line[0] == '>':
    #         acc = re.search('>..\|([\w\d]+)|[\w\d]+', line).groups()[0]
    #         write_flag = acc in acc_to_domain
    #     elif write_flag:
    #         proteins[acc] += line.strip()

    for acc, seq in proteins.items():
        # header is from (counting from 1) - to (including number)
        # thus -1, 0
        for domain_start, domain_end in acc_to_domain[acc]:
            kinase_domain_fasta.write('>%i|%s|%i-%i\n' % (acc_to_species[acc], acc, domain_start, domain_end))
            kinase_domain_fasta.write('%s\n' % seq[domain_start-1:domain_end])
            kinase_fasta.write('>%i|%s|\n%s\n' % (acc_to_species[acc], acc, seq))
    kinase_domain_fasta.close()
    kinase_fasta.close()

    ######################################################################
    # align with clustalo
    # and parse alignment
    ######################################################################
    alignment = 'static/data/kinase_domain.clustal'

    # ignored to make debugging faster :D
    if DEBUG == False:
        os.system("clustalo -i %s -o %s --threads=20 -outfmt=clustal " % (kinase_domain_fasta.name, alignment))

    kinase_domain = collections.defaultdict(list)
    alignment_file = open(alignment, 'r')
    alignment_file.readline()
    for line in alignment_file:
        if re.search("^\s*\n$", line):
            continue

        _re = r'(\d+)\|([\d\w]+)\|(\d+)-(\d+)\s+([\w-]+)'
        organism, acc, domain_start, domain_end, seq = re.match(_re, line).groups()
        kinase_domain[acc, int(domain_start)].append(seq)
    kinase_domain = {key : ''.join(seq) for (key, seq) in kinase_domain.items()}

    potential_starts = collections.Counter()
    potential_ends = collections.Counter()
    for seq in kinase_domain.values():
        for m in re.finditer('DFG', seq):
            potential_starts[m.start()] += 1
        for m in re.finditer('APE', seq):
            potential_ends[m.start()] += 1

    start = max(((c, i) for (i, c) in potential_starts.items()))[1]
    end   = max(((c, i) for (i, c) in potential_ends.items()))[1]

    loops_tsv = open (LOOP_TSV, 'w')
    loops_tsv.write('ID\tGene name\tLong Name\torganism\tDFG\tAPE\tLoop Seq\ttryptic Loop\n')
    for (acc, offset), seq in kinase_domain.items():
        # tryptic loop is wrong, everything else SEEMS correct
        protein = proteins[acc]
        dfg = start - seq[:start].count('-') + offset
        ape = end - seq[:end].count('-') + offset + 2
        loop_seq = protein[dfg-1:ape]
        # this math is wrong (maby)
        t_end = min(protein.find('R', ape), protein.find('K', ape)) + 1
        t_begin = max(protein[:dfg-1].rfind('R'), protein[:dfg-1].rfind('K')) + 1
        tryptic_loop_seq = protein[t_begin:t_end]
        data = (acc, acc_to_gene_name[acc], acc_to_description[acc], acc_to_species[acc],
                dfg, ape, loop_seq, tryptic_loop_seq)
        loops_tsv.write('%s\n' % '\t'.join(map(str, data)))
    #
if __name__ == '__main__':
    generate_data(UNIPROT_TSV, UNIPROT_FASTA)
    # main('clustalw2-I20141125-163052-0406-37442669-es.clustalw',
    #      r'../Search Databases/txt/Phospho (STY)Sites.txt',
    #      'activation_loop_result.tsv'
    # )