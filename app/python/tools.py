import datetime, time, os, sys, subprocess, hashlib
PLATFORM = sys.platform

def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if PLATFORM == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def cut_tag_from_html(html_text, tag="style"):
    start_index = html_text.index("<{}>".format(tag))
    stop_index = html_text.index("</{}>".format(tag)) + len("</{}>".format(tag))
    html_tag = html_text[start_index:stop_index]
    html_rest = html_text[:start_index] + html_text[stop_index:]
    return html_tag, html_rest

def split_string_or_nan(string_or_nan, sep=";"):
    try:
        ans = string_or_nan.split(sep)
    except AttributeError: # if nan
        ans = []
    return ans

def commaSepCol2uniqueFlatList(df, colname, sep=";", unique=True):
    series_of_lists = df[colname].apply(split_string_or_nan, 1, args=(sep,))
    nested_list = series_of_lists.tolist()
    flat_list = [item for sublist in nested_list for item in sublist]
    if not unique:
        return sorted(flat_list)
    else:
        return sorted(set(flat_list))

def convert_assoc_dict_2_proteinGroupsAssocDict(assoc_dict, proteinGroups_list):
    """
    proteinGroups_list = ['A;B;C']
    assoc_dict = {'A': set(["a", "b", "c", "d"]),
    'B': set(["a", "b", "c"]),
    'C': set(["a", "b", "d"])}
    create a consensus association dictionary.
    If 50% or more GOterms are associated with each AN within proteinGroup --> keep, else discard
    :param assoc_dict: Dict(key: String(UniProt-AccessionNumber), val:SetOfString(e.g.GOterms))
    :param proteinGroups_list: ListOfString
    :return: Dict(String(UniProt-AccessionNumbers comma separated), val:SetOfString(e.g.GOterms))
    """
    # A.) could try to make redundant list of GOterms and count them
    # B.) Dict (e.g. defaultdict with lambda: 0) that counts associations from each set and then sort by counts (values) take
    # C.) cast string of ANs (proteinGroups) to array
    assoc_dict_pg = {}
    for proteinGroup in proteinGroups_list:
        nested_associations = []
        for an in proteinGroup.split(";"):
            nested_associations.append(list(assoc_dict[an]))
        number_of_lists = len(nested_associations)
        flat_list = [item for sublist in nested_associations for item in sublist]
        consensus_associations = set()
        for goterm in set(flat_list):
            if flat_list.count(goterm) >= (number_of_lists / 2.0):
                consensus_associations.update([goterm])
        assoc_dict_pg[proteinGroup] = consensus_associations
    return assoc_dict_pg

def print_runtime(start_time):
    print("#" * 80, "\n", "--- runtime: {} ---".format(str(datetime.timedelta(seconds=int(time.time() - start_time)))))
    print("# Runtime {} # Datetime {}".format(str(datetime.timedelta(seconds=int(time.time() - start_time))), str(datetime.datetime.now())))

def sort_file(fn_in, fn_out, columns=None, fn_bash_script=None, number_of_processes=1, verbose=True, numeric_sort=False):
    if verbose:
        print("#sorting file\nfn_in:\n{}\nfn_out:\n{}".format(fn_in, fn_out))
    if fn_bash_script is None:
        fn_bash_script = "bash_script_sort_{}.sh".format(os.path.basename(fn_in))
    with open(fn_bash_script, "w") as fh:
        fh.write("#!/usr/bin/env bash\n")
        if numeric_sort:
            sort_ = "sort -n"
        else:
            sort_ = "sort"
        if columns is not None:
            shellcmd = "LC_ALL=C {} --parallel {} -k {} {} -o {}".format(sort_, number_of_processes, columns, fn_in, fn_out)
        else:
            shellcmd = "LC_ALL=C {} --parallel {} {} -o {}".format(sort_, number_of_processes, fn_in, fn_out)
        fh.write(shellcmd)
    if verbose:
        print(shellcmd)
    subprocess.call("chmod 744 ./{}".format(fn_bash_script), shell=True)
    subprocess.call("./{}".format(fn_bash_script), shell=True)
    os.remove(fn_bash_script)

def concatenate_files(fn_list, fn_out):
    print("concatenating files to {}".format(fn_out))
    with open(fn_out, "w") as fh_out:
        for fn in fn_list:
            print(fn)
            with open(fn, "r") as fh_in:
                for line in fh_in:
                    fh_out.write(line)

def line_numbers(fn_in):
    with open(fn_in, "r") as fh_in:
        num_lines = sum(1 for _ in fh_in)
    return num_lines

def yield_line_uncompressed_or_gz_file(fn):
    """
    adapted from
    https://codebright.wordpress.com/2011/03/25/139/
    and
    https://www.reddit.com/r/Python/comments/2olhrf/fast_gzip_in_python/
    http://pastebin.com/dcEJRs1i
    :param fn: String (absolute path)
    :return: GeneratorFunction (yields String)
    """
    if fn.endswith(".gz"):
        if PLATFORM == "darwin": # OSX: "Darwin"
            ph = subprocess.Popen(["gzcat", fn], stdout=subprocess.PIPE)
        elif PLATFORM == "linux": # Debian: "Linux"
            ph = subprocess.Popen(["zcat", fn], stdout=subprocess.PIPE)
        else:
            ph = subprocess.Popen(["cat", fn], stdout=subprocess.PIPE)

        for line in ph.stdout:
            yield line.decode("utf-8")
    else:
        with open(fn, "r") as fh:
            for line in fh:
                yield line

def gunzip_file(fn_in, fn_out=None, verbose=False):
    if not os.path.isfile(fn_in):
        print("gunzip_file: File Name {} does not exits".format(fn_in))
        raise StopIteration
    fn_bash_script = "bash_script_sort_{}.sh".format(os.path.basename(fn_in))
    with open(fn_bash_script, "w") as fh:
        fh.write("#!/usr/bin/env bash\n")
        if fn_out is None:
            fn_out = fn_in + "_temp"
        if verbose:
            print("gunzipping {} to {}".format(fn_in, fn_out))
        shellcmd_1 = "gunzip -c {} > {}".format(fn_in, fn_out)
        fh.write(shellcmd_1 + "\n")
    subprocess.call("chmod 744 ./{}".format(fn_bash_script), shell=True)
    subprocess.call("./{}".format(fn_bash_script), shell=True)
    os.remove(fn_bash_script)

def diff_of_columns_of_2_files(fn_1, fn_2, column_number_1=0, column_number_2=0, sep="\t"):
    list1, list2 = [], []
    with open(fn_1, "r") as fh_1:
        with open(fn_2, "r") as fh_2:
            for line in fh_1:
                list1.append(line.split(sep)[column_number_1].strip())
            for line in fh_2:
                list2.append(line.split(sep)[column_number_2].strip())
    set1 = set(list1)
    set2 = set(list2)
    print("len of list1: {}, len of set1: {}".format(len(list1), len(set1)))
    print("len of list2: {}, len of set2: {}".format(len(list2), len(set2)))
    print("len and diff of set1 - set2: {}\n{}".format(len(set1 - set2), sorted(set1 - set2)))
    print("len and diff of set2 - set1: {}\n{}".format(len(set2 - set1), sorted(set2 - set1)))

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()