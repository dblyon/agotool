import datetime, time


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

