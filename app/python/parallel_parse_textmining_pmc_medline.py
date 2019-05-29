import re, fileinput


def parse_textmining_pmc_medline():
    # names = ['PMID_and_crap', 'authors', 'name_and_issue', 'year', 'title', 'text']
    etype = "-56"
    # name = ""
    # definition = ""
    max_len_description = 250
    # xml tags e.g. "<i>Salmonella</i>" and others
    # tags_2_remove = re.compile("|".join([r"<[^>]+>", r"\[Purpose\]"]))
    # tags_2_remove = re.compile("|".join([r"<[^>]+>", r"\[Purpose\]", r"\\", "\/"]))
    level = "-1"
    for line in fileinput.input():
        line_split = line.split("\t")
        PMID, *rest = line_split[0].split("|")
        PMID = PMID.strip()
        # DOI = ""
        # for ele in rest:
        #     if ele.startswith("DOI:"):
        #         DOI = ele.strip()
        # authors = line_split[1].strip()
        # journal_vol = line_split[2]
        # match = re.search("\d", journal_vol)
        # if match:
        #     journal = journal_vol[:match.start()].strip()
        #     volume = journal_vol[match.start():].strip()
        # else:
        #     journal = journal_vol
        #     volume = ""
        year = line_split[3].strip()
        if not year:
            year = "...."

        title = line_split[4].strip()
        if not title:
            title = " ".join(line_split[4:]).strip()
        title = clean_messy_string_v2(title) # in order to capture foreign language titles' open and closing brackets e.g. "[bla bla bla]"
        title = cut_long_string_at_word(title, max_len_description)
        # title = tags_2_remove.sub('', title)
        title = clean_messy_string_v2(title)
        description = "(" + str(year) + ") " + title
        description = " ".join(description.split()) # replace multiple spaces with single space
        print(etype + "\t" + PMID + "\t" + description + "\t" + year + "\t" + level)

def cut_long_string_at_word(string_, max_len_description):
    if len(string_) > max_len_description:
        string_2_use = ""
        for word in string_.split(" "):
            if len(string_2_use + word) > max_len_description:
                string_2_return = string_2_use.strip() + " ..."
                assert len(string_2_return) <= (max_len_description + 4)
                return string_2_return
            else:
                string_2_use += word + " "
    else:
        return string_.strip()

def clean_messy_string_v2(string_):
    string_ = string_.strip().replace('"', "'")
    tags_2_remove = re.compile("|".join([r"<[^>]+>", r"\[Purpose\]", r"\\", "\/"]))
    string_ = tags_2_remove.sub('', string_)
    if string_.startswith("[") and string_.endswith("]"):
        return clean_messy_string_v2(string_[1:-1])
    elif string_.startswith("[") and string_.endswith("]."):
        return clean_messy_string_v2(string_[1:-2])
    elif string_.isupper():
        return string_[0] + string_[1:].lower()
    else:
        return string_


if __name__ == "__main__":
    parse_textmining_pmc_medline()