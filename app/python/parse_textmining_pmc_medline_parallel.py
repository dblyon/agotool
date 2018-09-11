import re, fileinput

def parse_textmining_pmc_medline():
    # names = ['PMID_and_crap', 'authors', 'name_and_issue', 'year', 'title', 'text']
    etype = "-56"
    max_len_description = 80
    # xml tags e.g. "<i>Salmonella</i>" and others
    tags_2_remove = re.compile("|".join([r"<[^>]+>", r"\[Purpose\]"]))
    for line in fileinput.input():
        line_split = line.split("\t")
        PMID, *rest = line_split[0].split("|")
        PMID = PMID.strip()
        DOI = ""
        for ele in rest:
            if ele.startswith("DOI:"):
                DOI = ele.strip()
        authors = line_split[1].strip()
        year = line_split[3].strip()
        title = line_split[4].strip()

        if not title:
            title = " ".join(line_split[4:]).strip()
        title = tags_2_remove.sub('', title)

        if len(title) > max_len_description:
            title_2_use = ""
            for word in title.split(" "):
                if len(title_2_use) < max_len_description:
                    title_2_use += word + " "
            title = title_2_use.strip() + "..."

        journal_vol = line_split[2]
        match = re.search("\d", journal_vol)
        if match:
            journal = journal_vol[:match.start()].strip()
            volume = journal_vol[match.start():].strip()
        else:
            journal = journal_vol
            volume = ""  # | etype | an=PMID | name=author list | definition=year | description=title |
        # fh_out.write(etype + "\t" + PMID + "\t" + authors + "\t" + year + "\t" + title + "\n")
        print(etype + "\t" + PMID + "\t" + authors + "\t" + year + "\t" + title)

if __name__ == "__main__":
    parse_textmining_pmc_medline() #, args.fn_out)

