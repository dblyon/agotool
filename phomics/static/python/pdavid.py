#!/urs/bin/env python

from __future__ import print_function
import collections
import sys


try:
    from scipy.stats import fisher_exact
except:
    import math

    fac = math.factorial
    def log_fac(n):
        ln = lambda x: math.log(x, math.e)
        if n < 100:
            return ln(fac(n))
        return n * ln(n) - n + 0.5 * ln(2 * math.pi * n)

    def log_bin_coef(n, k):
        return log_fac(n) - (log_fac(k) + log_fac(n-k))

    def fisher_exact(array):
        (a, c),  (b, d) = array
        a,b,c,d = map(float, (a,b,c,d))

        p = math.e ** ((log_bin_coef(a+b, a) + log_bin_coef(c+d, c)) - log_bin_coef(a+b+c+d, a+c))
        fold = float('nan')
        if 0.0 not in (a,b,c,d):
            fold = ((a / (a+b)) / (c/(c+d)))
        return fold, p



################################################################################
# Gobal variables
################################################################################
CATEGORIES = ['BBID', 'BIOCARTA', 'GOTERM_BP_FAT', 'GOTERM_CC_FAT', 'GOTERM_MF_FAT', 'KEGG_PATHWAY', 'REACTOME_PATHWAY']
SPLIT_CATAGORY_ON = dict(zip(CATEGORIES, ".:~~~::"))

################################################################################
# Graphical interface
################################################################################
if __name__ == '__main__':
    try:
        import Tkinter
        import tkFileDialog
    except:
        # renamed in python3 ?!?!?!?!
        # see http://stackoverflow.com/questions/673174/file-dialog-in-tkinter-python-3
        import tkinter as Tkinter
        import tkinter.filedialog as tkFileDialog
    class Application(Tkinter.Tk):
        def __init__(self,parent):
            Tkinter.Tk.__init__(self,parent)
            self.parent = parent
            self.file_opt = options = {}
            options['defaultextension'] = '.txt'
            # options['filetypes'] = [('all files', '.*'), ('tab separated vector', '.tsv')]
            options['initialfile'] = 'myfile.txt'
            options['parent'] = parent
            options['title'] = 'This is a title'
            self.initialize()


        def make_row(self, label_str, row, button=None):
            variables = []

            for label_type, column_offset in (("Forground", 0), ("Background", 3)):

                # labels
                labelVariable = Tkinter.StringVar()
                label = Tkinter.Label(self, textvariable=labelVariable, anchor="w")
                labelVariable.set('%s %s' % (label_type, label_str))
                label.grid(column=column_offset, row=row, sticky='EW')

                # Entrys
                text = Tkinter.StringVar()
                # text.set()
                entry = Tkinter.Entry(self, textvariable=text)

                if button == None:
                    entry.grid(column=1+column_offset, columnspan=2, row=row, sticky='EW')
                else:
                    entry.grid(column=1+column_offset, row=row, sticky='EW')

                    f = lambda : text.set(tkFileDialog.askopenfilename(**self.file_opt))
                    browse_button = Tkinter.Button(self, text='Browse', command=f)
                    browse_button.grid(column=2+column_offset, row=row)

                variables.append(text)
            return variables

        def initialize(self):
            self.grid()
            self.variables = []

            self.variables.append(self.make_row("Column Name", 0))
            self.variables.append(self.make_row("Input File Name", 1, "Browse"))
            self.variables.append(self.make_row("David File Name", 2, "Browse"))

            # result half row
            labelVariable = Tkinter.StringVar()
            label = Tkinter.Label(self, textvariable=labelVariable, anchor="w")
            labelVariable.set('Result File Name')
            label.grid(column=0, row=3, sticky='EW')

            self.result_file = Tkinter.StringVar()
            self.result_file.set('results.txt')
            entry = Tkinter.Entry(self, textvariable=self.result_file)
            entry.grid(column=1, row=3, sticky='EW')

            f = lambda : text.set(tkFileDialog.asksaveasfilename(**self.file_opt))
            browse_button = Tkinter.Button(self, text='Browse', command=f)
            browse_button.grid(column=2, row=3)


            # FDR / calcuate half row
            labelVariable = Tkinter.StringVar()
            label = Tkinter.Label(self, textvariable=labelVariable, anchor="w")
            labelVariable.set('False Discovery Rate cutoff')
            label.grid(column=3, row=3, sticky='EW')

            self.fdr = Tkinter.StringVar()
            self.fdr.set("0.01")
            entry = Tkinter.Entry(self, textvariable=self.fdr)

            entry.grid(column=4, row=3, sticky='EW')

            browse_button = Tkinter.Button(self, text='Browse', command=self.calculate)
            browse_button.grid(column=5, row=3)

        def calculate(self):
            v = [col_args.get() for row_args in self.variables for col_arg in row_args]
            main(float(self.fdr), v[0], v[1], open(self.result_file, 'w'), *map(open, v[2:]))



################################################################################
# Core functions
################################################################################
def count(my_file, column_name):
    counts = collections.Counter()
    header = [x.strip('"') for x in my_file.readline().split('\t')]
    i = header.index(column_name.strip('"'))
    for line in my_file:
        _id = line.rstrip('\r\n').split('\t')[i].strip('"')
        counts[_id] += 1
    return counts, sum(counts.values())

def main(fdr, fg_column_name, bg_column_name, result_file, david_fg_file,
         david_bg_file, mq_fg_file, mq_bg_file):

    # parse maxquant files into two collection.Counter
    fg_id_counts, fg_total = count(mq_fg_file, fg_column_name)
    bg_id_counts, bg_total = count(mq_bg_file, bg_column_name)
    run(fdr, fg_id_counts, fg_total, bg_id_counts, bg_total, result_file,
        david_fg_file, david_bg_file)

def run(fdr, fg_id_counts, fg_total, bg_id_counts, bg_total, result_file,
    david_fg_file, david_bg_file):

    header = david_bg_file.readline().rstrip('\r\n').split('\t')
    bg_counts = dict(((x, collections.Counter()) for x in categories))
    for line in david_bg_file:
        tab = line.split('\t')
        _id = tab[0]
        for cell, category in zip(tab[3:], categories):
            for item in cell.split(','):
                if item.strip() != '':
                    term = get_term(item, category)
                    bg_counts[category][term] += bg_id_counts[_id]

    benjamini = dict((key, []) for key in categories)
    bonferroni_cor = dict((key, 0) for key in categories)
    lines = []
    line_nr_to_p = {}
    line_nr_to_category = {}
    for i, line in enumerate(david_fg_file):
        line = line.rstrip('\r\n')
        tabs = line.split('\t')
        if tabs[0] == "Category":
            extra = ('FG Count', 'BG Count', 'FG Other', 'BG Other',
                     'fold change', 'p value (fishers exact)',
                     'Bonferroni', 'Benjamini (%.3f)' % fdr)
            line += "\t%s" % '\t'.join(extra)
            indexes = dict(((key, val) for val, key in enumerate(tabs)))
        elif len(tabs) > 3:
            catagory = tabs[indexes['Category']]
            term = get_term(tabs[indexes['Term']], catagory)

            bg_count = bg_counts[catagory][term]
            bg_other = bg_total - bg_count

            genes = tabs[indexes['Genes']].split(', ')
            fg_count = sum((fg_id_counts[_id] for _id in genes))
            fg_other = fg_total - fg_count

            fold, p = fisher_exact(((fg_count, bg_count), (fg_other, bg_other)))
            benjamini[catagory].append(p)
            bonferroni_cor[catagory] = int(tabs[indexes['Pop Total']])
            line_nr_to_p[i] = p
            line_nr_to_category[i] = catagory
            data = map(str, (fg_count, bg_count, fg_other, bg_other))
            line += '\t%s\t%5.3f\t%2.20f' % ('\t'.join(data), fold, p)
        lines.append(line)
    benjamini_cor = {}
    significant = 0
    print ('-' * 700)
    for category, ps in benjamini.items():
        l, i = float(bonferroni_cor[catagory]), 0
        for i, p in enumerate(sorted(ps), 1):
            if (((p * l) / i) > fdr):
                break
        if i != 0:
            benjamini_cor[category] = l / i
            print ("%3i survrived in catagory %s, correctionfactor = %f" % (i, category, l / i))
        else:
            benjamini_cor[category] = float('nan')
            print ("  0 survrived in catagory %s, correctionfactor = 'nan'" % (category))

        significant += i

    print ('%3i in total (fdr=%.4f)' % (significant, fdr))
    print ('-' * 70, '\n')

    for i, line in enumerate(lines):
        result_file.write(line)
        if i in line_nr_to_category:
            category = line_nr_to_category[i]
            p = line_nr_to_p[i]

            result_file.write('\t%.20f' % min((p * bonferroni_cor[category], 1.0)))
            result_file.write('\t%.20f' % min((p * benjamini_cor[category], 1.0)))
        result_file.write('\n')


def get_term(raw_term, category):
    return raw_term.split(SPLIT_CATAGORY_ON[category])[0].strip()


################################################################################
# main
################################################################################
if __name__ == '__main__':
    if len(sys.argv) == 1:
        app = Application(None)
        app.title('David Phospho Enrichment')
        app.mainloop()
    elif sys.argv[1] in ('-h', '--help') or len(sys.argv) < 6:
        print ("usage:\npython %s [fdr] [fg column name] [bg column name] [output_file] " \
              "[david fg file] [david bg file] [input fg file] [input bg file]" % sys.argv[0])
    else:
        v = sys.argv
        main(float(v[1]), v[2], v[3], open(v[4], 'w'), *map(open, sys.argv[5:]))



