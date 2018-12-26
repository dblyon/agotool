import datetime, time, os, sys, subprocess
PLATFORM = sys.platform


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

def sort_file(fn_in, fn_out, columns=None, fn_bash_script=None, number_of_processes=1, verbose=True):
    if verbose:
        print("#sorting file\nfn_in:\n{}\nfn_out:\n{}".format(fn_in, fn_out))
    if fn_bash_script is None:
        fn_bash_script = "bash_script_sort_{}.sh".format(os.path.basename(fn_in))
    with open(fn_bash_script, "w") as fh:
        fh.write("#!/usr/bin/env bash\n")
        if columns is not None:
            shellcmd = "sort --parallel {} -k {} {} -o {}".format(number_of_processes, columns, fn_in, fn_out)
        else:
            shellcmd = "sort --parallel {} {} -o {}".format(number_of_processes, fn_in, fn_out)

        if PLATFORM != "linux":
            shellcmd = shellcmd.replace("sort ", "LC_ALL=C gsort ")
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