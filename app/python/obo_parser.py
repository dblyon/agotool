import sys, os
sys.path.insert(0, os.path.abspath(os.path.realpath('./')))
# import query


try:
    from exceptions import EOFError
except ImportError:
    pass

# import collections as cx

TYPEDEF_TAG, TERM_TAG = "[Typedef]", "[Term]"

GraphEngines = ("pygraphviz", "pydot")


def after_colon(line):
    # macro for getting anything after the :
    return line.split(":", 1)[1].strip()

def relationship_part_of(line):
    return line[21:].split()[0]

def relationship_develops_from(line):
    return line[28:].split()[0]

def read_until(handle, start):
    # read each line until it has a certain start, and then puts
    # the start tag back
    while 1:
        pos = handle.tell()
        line = handle.readline()
        if not line:
            break
        if line.startswith(start):
            handle.seek(pos)
            return
    raise EOFError("%s tag cannot be found" % start)


class OBOReader:
    """
    parse obo file, usually the most updated can be downloaded from
    http://purl.obolibrary.org/obo/go/go-basic.obo
    """
    def __init__(self, obo_file="go-basic.obo", upk=False):
        self.upk = upk
        try:
            self._handle = open(obo_file)
        except:
            print(("download obo file first\n "
                                 "[http://purl.obolibrary.org/obo/"
                                 "go/go-basic.obo]"), file=sys.stderr)
            sys.exit(1)

    def __iter__(self):
        line = self._handle.readline()
        if not line.startswith(TERM_TAG):
            read_until(self._handle, TERM_TAG)
        while 1:
            try:
                yield self.__next__()
            except StopIteration:
                return

    def __next__(self):
        lines = []
        line = self._handle.readline()
        if not line or line.startswith(TYPEDEF_TAG):
            raise StopIteration

        # read until the next tag and save everything in between
        while 1:
            pos = self._handle.tell()   # save current postion for roll-back
            line = self._handle.readline()
            if not line or (line.startswith(TYPEDEF_TAG) or line.startswith(TERM_TAG)):
                self._handle.seek(pos)  # roll-back
                break
            lines.append(line)

        rec = GOTerm()
        for line in lines:
            if line.startswith("id:"):
                id_ = after_colon(line)
                if self.upk:
                    id_ = self.replace_KW_with_UPK(id_)
                # rec.id = after_colon(line)
                rec.id = id_
            if line.startswith("alt_id:"):
                # rec.alt_ids.append(after_colon(line))
                alt_id = after_colon(line)
                if self.upk:
                    alt_id = self.replace_KW_with_UPK(alt_id)
                rec.alt_ids.append(alt_id)
            elif line.startswith("name:"):
                rec.name = after_colon(line)
            elif line.startswith("namespace:"):
                rec.namespace = after_colon(line)
            elif line.startswith("is_a:"):
                # rec._parents.append(after_colon(line).split()[0])
                parents = after_colon(line).split()[0]
                if self.upk:
                    parents = self.replace_KW_with_UPK(parents)
                rec._parents.append(parents)
            elif line.startswith("relationship: part_of"):
                parents = relationship_part_of(line)
                rec._parents.append(parents)
            elif line.startswith("relationship: develops_from"):
                parents = relationship_develops_from(line)
                rec._parents.append(parents)
            elif (line.startswith("is_obsolete:") and
                  after_colon(line) == "true"):
                rec.is_obsolete = True
            elif line.startswith("consider:"):
                rec.consider.append(line.replace("consider: ", "").strip())
        return rec

    def replace_KW_with_UPK(self, id_):
        # return id_.replace("KW-", "UPK:")
        return id_


class OBOReader_2_text(OBOReader):

    # def __init__(self, obo_file):
    #     try:
    #         self._handle = open(obo_file, "r")
    #     except:
    #         sys.exit(1)

    # def __iter__(self):
    #     line = self._handle.readline()
    #     if not line.startswith(TERM_TAG):
    #         read_until(self._handle, TERM_TAG)
    #     while 1:
    #         yield self.__next__()

    def __next__(self):
        lines = []
        line = self._handle.readline()
        if not line or line.startswith(TYPEDEF_TAG):
            raise StopIteration

        # read until the next tag and save everything in between
        while 1:
            pos = self._handle.tell()  # save current postion for roll-back
            line = self._handle.readline()
            if not line or (line.startswith(TYPEDEF_TAG) or line.startswith(TERM_TAG)):
                self._handle.seek(pos)  # roll-back
                break
            lines.append(line)
        id_, name, definition = "", "", ""
        is_a_list = []
        for line in lines:
            # if line.startswith("id_:"):
            if line.startswith("id:"):
                id_ = after_colon(line)
            elif line.startswith("name:"):
                name = after_colon(line)
            elif line.startswith("def:"):
                definition = after_colon(line)
            elif line.startswith("is_a:"):
                is_a_list.append(after_colon(line).split()[0])
            elif line.startswith("relationship: part_of"):
                is_a_list.append(relationship_part_of(line))
        return id_, name, is_a_list, definition


class GOTerm:
    """
    GO term, actually contain a lot more properties than interfaced here
    """

    def __init__(self):
        self.id = ""                # GO:NNNNNNN
        self.name = ""              # description
        self.namespace = ""         # BP, CC, MF
        self._parents = []          # is_a basestring of parents
        self.parents = []           # parent records
        self.children = []          # children records
        self.level = None           # shortest distance from root node
        self.depth = None           # longest distance from root node
        self.is_obsolete = False    # is_obsolete
        self.alt_ids = []           # alternative identifiers
        self.consider = []          # consider one of these terms instead


    def __repr__(self):
        return "GOTerm({})".format(self.id)

    def has_parent(self, term):
        for p in self.parents:
            if p.id == term or p.has_parent(term):
                return True
        return False

    def has_child(self, term):
        for p in self.children:
            if p.id == term or p.has_child(term):
                return True
        return False


    # def get_all_parents(self):
    #     all_parents = set()
    #     for p in self.parents:
    #         all_parents.add(p.id)
    #         all_parents |= p.get_all_parents()
    #     return all_parents

    def get_all_parents(self):
        try:
            len(self.all_parents)
        except AttributeError:
            self.all_parents = set()
            for p in self.parents:
                self.all_parents.add(p.id)
                self.all_parents |= p.get_all_parents() # same as union of sets, but faster
        return self.all_parents

    def get_direct_parents(self):
        return [p.id for p in self.parents]

    def get_all_children(self):
        all_children = set()
        for p in self.children:
            all_children.add(p.id)
            all_children |= p.get_all_children()
        return all_children

    def get_all_parent_edges(self):
        all_parent_edges = set()
        for p in self.parents:
            all_parent_edges.add((self.id, p.id))
            all_parent_edges |= p.get_all_parent_edges()
        return all_parent_edges

    def get_all_child_edges(self):
        all_child_edges = set()
        for p in self.children:
            all_child_edges.add((p.id, self.id))
            all_child_edges |= p.get_all_child_edges()
        return all_child_edges

    def write_hier_rec(self, gos_printed, out=sys.stdout, 
                      len_dash=1, max_depth=None, num_child=None, short_prt=False,
                      include_only=None, go_marks=None,
                      depth=1, dp="-"):
        """Write hierarchy for a GO Term record."""
        GO_id = self.id
        # Shortens hierarchy report by only printing the hierarchy
        # for the sub-set of user-specified GO terms which are connected.
        if include_only is not None and GO_id not in include_only:
          return
        nrp = short_prt and GO_id in gos_printed
        if go_marks is not None:
          out.write('{} '.format('>' if GO_id in go_marks else ' '))
        if len_dash is not None:
            # Default character indicating hierarchy level is '-'.
            # '=' is used to indicate a hierarchical path printed in detail previously.
            letter = '-' if not nrp or not self.children else '='
            dp = ''.join([letter]*depth)
            out.write('{DASHES:{N}} '.format(DASHES=dp, N=len_dash))
        if num_child is not None:
            out.write('{N:>5} '.format(N=len(self.get_all_children())))
        out.write('{GO}\tL-{L:>02}\tD-{D:>02}\t{desc}\n'.format(
            GO=self.id, L=self.level, D=self.depth, desc=self.name))
        # Track GOs previously printed only if needed
        if short_prt:
          gos_printed.add(GO_id)
        # Do not print hierarchy below this turn if it has already been printed
        if nrp:
            return 
        depth += 1
        if max_depth is not None and depth > max_depth:
            return
        for p in self.children:
            p.write_hier_rec(gos_printed, out, len_dash, max_depth, num_child, short_prt, 
                include_only, go_marks,
                depth, dp)


class GODag(dict):

    def __init__(self, obo_file="go-basic.obo", upk=False):
        """
        :param obo_file: String
        :param upk: Bool (flag to convert UniProtKeyword tag from 'KW-0673' to 'UPK:0673')
        """
        self.load_obo_file(obo_file, upk=upk)

    def load_obo_file(self, obo_file, upk):
        obo_reader = OBOReader(obo_file, upk=upk)
        for rec in obo_reader:
            self[rec.id] = rec
            for alt in rec.alt_ids:
                self[alt] = rec
        self.populate_terms()

    def populate_terms(self):

        def _init_level(rec):
            if rec.level is None:
                if not rec.parents:
                    rec.level = 0
                else:
                    rec.level = min(_init_level(rec) for rec in rec.parents) + 1
            return rec.level

        def _init_depth(rec):
            if rec.depth is None:
                if not rec.parents:
                    rec.depth = 0
                else:
                    rec.depth = max(_init_depth(rec) for rec in rec.parents) + 1
            return rec.depth

        # make the parents references to the GO terms
        for rec in self.values():
            rec.parents = [self[x] for x in rec._parents]

        # populate children and levels
        for rec in self.values():
            for p in rec.parents:
                if rec not in p.children:
                    p.children.append(rec)

            if rec.level is None:
                _init_level(rec)

            if rec.depth is None:
                _init_depth(rec)

    # def write_dag(self, out=sys.stdout):
    #     """Write info for all GO Terms in obo file, sorted numerically."""
    #     for rec_id, rec in sorted(self.items()):
    #         print(rec, file=out)
    #
    # def write_hier_all(self, out=sys.stdout,
    #                   len_dash=1, max_depth=None, num_child=None, short_prt=False):
    #     """Write hierarchy for all GO Terms in obo file."""
    #     # Print: [biological_process, molecular_function, and cellular_component]
    #     for go_id in ['GO:0008150', 'GO:0003674', 'GO:0005575']:
    #       self.write_hier(go_id, out, len_dash, max_depth, num_child, short_prt, None)
    #
    # def write_hier(self, GO_id, out=sys.stdout, len_dash=1, max_depth=None, num_child=None, short_prt=False, include_only=None, go_marks=None):
    #     """Write hierarchy for a GO Term."""
    #     gos_printed = set()
    #     self[GO_id].write_hier_rec(gos_printed, out, len_dash, max_depth, num_child,
    #         short_prt, include_only, go_marks)
    #
    # def write_summary_cnts(self, GO_ids, out=sys.stdout):
    #     """Write summary of level and depth counts for specific GO ids."""
    #     cnts = GODag.get_cnts_levels_depths_recs([self[GO] for GO in GO_ids])
    #     self._write_summary_cnts(cnts, out)
    #
    # def write_summary_cnts_all(self, out=sys.stdout):
    #     """Write summary of level and depth counts for all active GO Terms."""
    #     cnts = self.get_cnts_levels_depths_recs(set(self.values()))
    #     self._write_summary_cnts(cnts, out)
    #
    # def _write_summary_cnts(self, cnts, out=sys.stdout):
    #     """Write summary of level and depth counts for active GO Terms."""
    #     # Count level(shortest path to root) and depth(longest path to root)
    #     # values for all unique GO Terms.
    #     max_val = max(max(dep for dep in cnts['depth']),
    #                   max(lev for lev in cnts['level']))
    #     nss = ['biological_process', 'molecular_function', 'cellular_component']
    #     out.write('Dep <-Depth Counts->  <-Level Counts->\n')
    #     out.write('Lev   BP    MF    CC    BP    MF    CC\n')
    #     out.write('--- ----  ----  ----  ----  ----  ----\n')
    #     for i in range(max_val+1):
    #         vals = ['{:>5}'.format(cnts[desc][i][ns]) for desc in cnts for ns in nss]
    #         out.write('{:>02} {}\n'.format(i, ' '.join(vals)))
    #
    # @staticmethod
    # def get_cnts_levels_depths_recs(recs):
    #     """Collect counts of levels and depths in a Group of GO Terms."""
    #     cnts = cx.defaultdict(lambda: cx.defaultdict(cx.Counter))
    #     for rec in recs:
    #         if not rec.is_obsolete:
    #             cnts['level'][rec.level][rec.namespace] += 1
    #             cnts['depth'][rec.depth][rec.namespace] += 1
    #     return cnts
    #
    # @staticmethod
    # def id2int(GO_id): return int(GO_id.replace("GO:", "", 1))

    def query_term(self, term, verbose=False):
        if term not in self:
            print("Term %s not found!" % term, file=sys.stderr)
            return

        rec = self[term]
        print(rec, file=sys.stderr)
        if verbose:
            print("all parents:", rec.get_all_parents(), file=sys.stderr)
            print("all children:", rec.get_all_children(), file=sys.stderr)
        return rec

    def paths_to_top(self, term, verbose=False):
        """ Returns all possible paths to the root node

            Each path includes the term given. The order of the path is
            top -> bottom, i.e. it starts with the root and ends with the
            given term (inclusively).

            Parameters:
            -----------
            - term:
                the id of the GO term, where the paths begin (i.e. the
                accession 'GO:0003682')

            Returns:
            --------
            - a list of lists of GO Terms
        """
        # error handling consistent with original authors
        if term not in self:
            print("Term %s not found!" % term, file=sys.stderr)
            return

        def _paths_to_top_recursive(rec):
            if rec.level == 0:
                return [[rec]]
            paths = []
            for parent in rec.parents:
                top_paths = _paths_to_top_recursive(parent)
                for top_path in top_paths:
                    top_path.append(rec)
                    paths.append(top_path)
            return paths

        go_term = self[term]
        return _paths_to_top_recursive(go_term)

    def update_association(self, association):
        # assoc is a dict: key=AN, val=set of go-terms
        bad_terms = set()
        for key, terms in list(association.items()): # ? key unused, why not use 'values' ? # Anders: use itervalues to iterate over dict if not changing keys
            parents = set()
            for term in terms:
                try:
                    parents.update(self[term].get_all_parents()) # equivalent to parents.update(self.__getitem__(term).get_all_parents())
                except:
                    bad_terms.add(term.strip())
            terms.update(parents) # updates the association object with all parent GO-terms of given GO-terms
        if bad_terms:
            print("number of terms not found: %s" % (len(bad_terms),), file=sys.stderr)


class KEGGterm:
    """
    GO term, actually contain a lot more properties than interfaced here
    """

    def __init__(self, id_, name):
        self.id = id_       # KEGG:NNNNNNN
        self.name = name              # description
        self.level = 0  # shortest distance from root node
        self.depth = None  # longest distance from root node
        self.is_obsolete = False  # is_obsolete

class Functional_term:
    """
    GO term, actually contain a lot more properties than interfaced here
    """

    def __init__(self, id_, name):
        self.id = id_       # KEGG:NNNNNNN
        self.name = name              # description
        self.level = 0  # shortest distance from root node
        self.depth = None  # longest distance from root node
        self.is_obsolete = False  # is_obsolete



# class KEGG_pseudo_dag(dict):
#     """
#     depends on DB
#     kegg_pseudo_dag: description=name, goterm=id
#     """
#     def __init__(self):
#         KEGG_id_2_name_dict = query.get_function_type_id_2_name_dict("KEGG")
#         # kegg_pseudo_dag: description=name, goterm=id
#         for id_, name in KEGG_id_2_name_dict.items():
#             self[id_] = KEGGterm(id_, name)

# class Pseudo_dag(dict):
#     """
#     depends on DB
#     pseudo_dag: description=name, goterm=id
#     """
#     def __init__(self, etype):
#         Function_id_2_name_dict = query.get_function_type_id_2_name_dict(etype)
#         for id_, name in Function_id_2_name_dict.items():
#             self[id_] = Functional_term(id_, name)



class DOMterm:
    """
    Domain 'term'
    """

    def __init__(self, id_, name):
        self.id = id_       # DOM:NNNNNNN
        self.name = name              # description
        # self.namespace = ""         #
        self.level = 0  # shortest distance from root node
        self.depth = None  # longest distance from root node
        self.is_obsolete = False  # is_obsolete


# class DOM_pseudo_dag(dict):
#
#     def __init__(self):
#         # DOM_id_2_name_dict = query.get_DOM_id_2_name_dict()
#         DOM_id_2_name_dict = query.get_function_type_id_2_name_dict("DOM")
#         # DOM_pseudo_dag: description=name, DOM_term=id
#         for id_, name in DOM_id_2_name_dict.items():
#             self[id_] = DOMterm(id_, name)




