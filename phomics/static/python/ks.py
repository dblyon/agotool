#!/usr/env python

from __future__ import print_function
import sys
import collections
import StringIO
import os

try:
    import numpy as np
except ImportError:
    import pip
    pip.main(['install', 'numpy'])
    import numpy as np

try:
    import scipy as sp
except ImportError:
    if 'pip' not in dir():
        import pip
    pip.main(['install', 'scipy'])
    import scipy as sp

import scipy.stats

# gui stuff
if __name__ == '__main__':
    # dont import gui libaries if the module is imported
    # gui is buggy and not fully tested!!
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

        def initialize(self):
            self.grid()

            # 3 Labels
            for i, label_str in enumerate(('Foreground File', 'Background File', 'Result File')):
                labelVariable = Tkinter.StringVar()
                label = Tkinter.Label(self, textvariable=labelVariable, anchor="w")
                labelVariable.set(label_str)
                label.grid(column=0, row=i, sticky='EW')

            # 3 Entrys
            self.fg_file = Tkinter.StringVar()
            self.bg_file = Tkinter.StringVar()
            self.result_file = Tkinter.StringVar()
            self.result_file.set("results.tsv")

            self.fg_entry = Tkinter.Entry(self,textvariable=self.fg_file)
            self.bg_entry = Tkinter.Entry(self,textvariable=self.bg_file)
            self.result_entry = Tkinter.Entry(self,textvariable=self.result_file)

            self.fg_entry.grid(column=1,row=0,sticky='EW')
            self.bg_entry.grid(column=1,row=1,sticky='EW')
            self.result_entry.grid(column=1,row=2,sticky='EW')

            # 3 Buttons
            fg_button = Tkinter.Button(self, text='Browse', command=self.get_fg_file)
            fg_button.grid(column=2,row=0)
            bg_button = Tkinter.Button(self, text='Browse', command=self.get_bg_file)
            bg_button.grid(column=2,row=1)
            result_button = Tkinter.Button(self, text='Calcuate', command=self.ks_run)
            result_button.grid(column=2,row=2)


        def get_fg_file(self):
            self.fg_file.set(tkFileDialog.askopenfilename(**self.file_opt))


        def get_bg_file(self):
            self.bg_file.set(tkFileDialog.askopenfilename(**self.file_opt))

        def ks_run(self):
            ks_test(self.fg_file.get(), self.bg_file.get(), self.result_file.get())


def ks_test(fg_file, bg_file, result_file):
    reg_scores = get_kinase_scores(fg_file)
    unreg_scores = get_kinase_scores(bg_file)
    if isinstance(result_file, (str, unicode)):
        result_file = open(result_file)

    result_file.write('\t'.join(('Kinase', 'Kinase Family', 'p', 'd', 'Other high')))
    for group in reg_scores.keys():
        results = []
        for kinase in reg_scores[group].keys():
            v_reg, v_unreg = reg_scores[group][kinase], unreg_scores[group][kinase]
            pval = sp.stats.ks_2samp(v_reg, v_unreg)[1]
            dval = abs_dval(v_reg, v_unreg)
            results.append((pval, dval, group, kinase))
        results.sort()
        # best_dval = results[0][1]

        pva, best_dval, group, kinase = results[0]
        if (pval < 0.05):
            result_file.write('\n%s\t' % '\t'.join(map(str,
                                                       (kinase, group, pval, best_dval))))
            other_high = [kinase for pva, dval, group, kinase in results
                          if (pval < 0.05 and dval * 2 > best_dval)]
            result_file.write(';'.join(other_high))


def get_kinase_scores(networkin_file):
    kinase_scores = collections.defaultdict(lambda : collections.defaultdict(list))
    if isinstance(networkin_file, (str, unicode)):
        networkin_file = open(networkin_file)
    for line in networkin_file:
        if line[0] == '#': continue
        tokens = line.rstrip('\r\n').split('\t')
        tree, group, kinase, score = tokens[2:6]
        if tree == 'KIN':
            kinase_scores[group][kinase].append(float(score))
    return kinase_scores


def abs_dval(data1, data2):
    # adapted from scipy.stats :)
    data1, data2 = map(np.asarray, (data1, data2))
    #n1, n2 = data1.shape[0], data2.shape[0]
    n1, n2 = len(data1), len(data2)
    data1 = np.sort(data1)
    data2 = np.sort(data2)
    data_all = np.concatenate([data1,data2])
    cdf1 = np.searchsorted(data1,data_all,side='right')/(1.0*n1)
    cdf2 = (np.searchsorted(data2,data_all,side='right'))/(1.0*n2)
    diff = cdf1 - cdf2
    dmax = np.max(diff)
    dmin = np.min(diff)
    return max((dmin, dmax), key = abs)


def main():
    if len(sys.argv) == 1:
        app = Application(None)
        app.title('Kolmogorov Smirnov Kinase Enrichment Test')
        app.mainloop()
        return
    elif sys.argv[1] == '-h':
        print ('comandline usage: %s regulated_file unregulated_file [result_file]' % sys.argvp[0])
        print (' - if no argument, the program run in GUI mode')
        print (' - the program performs a kolmogorov smirnov test between two NetworKIN files')
        print (' - and returns it as [result_file] or stdout')
        return
    elif len(sys.argv) < 4:
        result_file = sys.stdout
    else:
        result_file = open(sys.argv[3], 'w')

    ks_test(sys.argv[1], sys.argv[2], result_file, result_file)
if __name__ == '__main__':
    main()


