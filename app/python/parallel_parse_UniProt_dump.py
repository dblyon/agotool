# from collections import defaultdict
import os, fileinput
import zlib, gzip
import tools, variables
import create_SQL_tables_snakemake as cst
import obo_parser


def Protein_2_Function_table_UniProtDump_UPS():
    fn_in_Functions_table_UPK = os.path.join(variables.TABLES_DIR, "Functions_table_UPK.txt")
    fn_in_obo_GO = os.path.join(variables.DOWNLOADS_DIR, "go-basic.obo")
    fn_in_obo_UPK = os.path.join(variables.DOWNLOADS_DIR, "keywords-all.obo")
    fn_in_interpro_parent_2_child_tree = os.path.join(variables.DOWNLOADS_DIR, "interpro_parent_2_child_tree.txt")
    fn_in_hierarchy_reactome = os.path.join(variables.DOWNLOADS_DIR, "RCTM_hierarchy.tsv")

    etype_UniProtKeywords = variables.id_2_entityTypeNumber_dict["UniProtKeywords"]
    etype_GOMF = variables.id_2_entityTypeNumber_dict['GO:0003674']
    etype_GOCC = variables.id_2_entityTypeNumber_dict['GO:0005575']
    etype_GOBP = variables.id_2_entityTypeNumber_dict['GO:0008150']
    etype_interpro = variables.id_2_entityTypeNumber_dict['INTERPRO']
    etype_pfam = variables.id_2_entityTypeNumber_dict['PFAM']
    etype_reactome = variables.id_2_entityTypeNumber_dict['Reactome']
    GO_dag = obo_parser.GODag(obo_file=fn_in_obo_GO, upk=False)
    UPK_dag = obo_parser.GODag(obo_file=fn_in_obo_UPK, upk=True)
    UPK_Name_2_AN_dict = cst.get_keyword_2_upkan_dict(fn_in_Functions_table_UPK)
    UPKs_not_in_obo_list, GOterms_not_in_obo_temp = [], []
    child_2_parent_dict_interpro, _ = cst.get_child_2_direct_parents_and_term_2_level_dict_interpro(fn_in_interpro_parent_2_child_tree)
    lineage_dict_interpro = cst.get_lineage_from_child_2_direct_parent_dict(child_2_parent_dict_interpro)
    child_2_parent_dict_reactome = cst.get_child_2_direct_parent_dict_RCTM(fn_in_hierarchy_reactome)


    for line in parse_uniprot_dat_dump_yield_entry_v2_parallel():
        print(type(line), line)

    # for UniProtID, UniProtAC_list, NCBI_Taxid, functions_2_return in parse_uniprot_dat_dump_yield_entry_v2_parallel():
        # Keywords_list, GOterm_list, InterPro, Pfam, KEGG, Reactome, STRING, *Proteomes = functions_2_return
        # # ['Complete proteome', 'Reference proteome', 'Transcription', 'Activator', 'Transcription regulation', ['GO:0046782'], ['IPR007031'], ['PF04947'], ['vg:2947773'], [], [], ['UP000008770']]
        # # for UniProtAN in UniProtAC_and_ID_list:
        # if len(Keywords_list) > 0:
        #     UPK_ANs, UPKs_not_in_obo_temp = cst.map_keyword_name_2_AN(UPK_Name_2_AN_dict, Keywords_list)
        #     UPKs_not_in_obo_list += UPKs_not_in_obo_temp
        #     UPK_ANs, UPKs_not_in_obo_temp = cst.get_all_parent_terms(UPK_ANs, UPK_dag)
        #     UPKs_not_in_obo_list += UPKs_not_in_obo_temp
        #     if len(UPK_ANs) > 0:
        #         # fh_out.write(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(UPK_ANs)) + "\t" + etype_UniProtKeywords + "\t" + NCBI_Taxid + "\n")
        #         print(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(UPK_ANs)) + "\t" + etype_UniProtKeywords + "\t" + NCBI_Taxid + "\n")
        # if len(GOterm_list) > 0: # do backtracking, split GO into 3 categories and add etype
        #     GOterm_list, not_in_obo_GO = cst.get_all_parent_terms(GOterm_list, GO_dag)
        #     GOterms_not_in_obo_temp += not_in_obo_GO
        #     MFs, CPs, BPs, not_in_obo_GO = cst.divide_into_categories(GOterm_list, GO_dag, [], [], [], [])
        #     GOterms_not_in_obo_temp += not_in_obo_GO
        #     if MFs:
        #         # fh_out.write(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(MFs)) + "\t" + etype_GOMF + "\t" + NCBI_Taxid + "\n")  # 'Molecular Function', -23
        #         print(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(MFs)) + "\t" + etype_GOMF + "\t" + NCBI_Taxid + "\n")  # 'Molecular Function', -23
        #     if CPs:
        #         # fh_out.write(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(CPs)) + "\t" + etype_GOCC + "\t" + NCBI_Taxid + "\n")  # 'Cellular Component', -22
        #         print(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(CPs)) + "\t" + etype_GOCC + "\t" + NCBI_Taxid + "\n")  # 'Cellular Component', -22
        #     if BPs:
        #         # fh_out.write(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(BPs)) + "\t" + etype_GOBP + "\t" + NCBI_Taxid + "\n")  # 'Biological Process', -21
        #         print(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(BPs)) + "\t" + etype_GOBP + "\t" + NCBI_Taxid + "\n")  # 'Biological Process', -21
        # if len(InterPro) > 0:
        #     InterPro_set = set(InterPro)
        #     for id_ in InterPro:
        #         InterPro_set.update(lineage_dict_interpro[id_])
        #     # fh_out.write(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(InterPro_set)) + "\t" + etype_interpro + "\t" + NCBI_Taxid + "\n")
        #     print(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(InterPro_set)) + "\t" + etype_interpro + "\t" + NCBI_Taxid + "\n")
        # if len(Pfam) > 0:
        #     # fh_out.write(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(Pfam)) + "\t" + etype_pfam + "\t" + NCBI_Taxid + "\n")
        #     print(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(Pfam)) + "\t" + etype_pfam + "\t" + NCBI_Taxid + "\n")
        # if len(Reactome) > 0:
        #     reactome_list = Reactome.copy()
        #     for term in reactome_list:
        #         reactome_list += list(cst.get_parents_iterative(term, child_2_parent_dict_reactome))
        #     # fh_out.write(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(set(reactome_list))) + "\t" + etype_reactome + "\t" + NCBI_Taxid + "\n")
        #     print(UniProtID + "\t" + cst.format_list_of_string_2_postgres_array(sorted(set(reactome_list))) + "\t" + etype_reactome + "\t" + NCBI_Taxid + "\n")
        #
        # # translation needed from KEGG identifier to pathway, ID vs AC can be easily distinguished via "_"
        # if len(KEGG) > 0:
        #     # fh_out_UniProtID_2_ENSPs_2_KEGGs_mapping.write(UniProtID + "\t" + ";".join(STRING) + "\t" + ";".join(sorted(set(KEGG))) + "\t" + NCBI_Taxid + "\n")
        #     print("222_UniProtID_2_ENSPs_2_KEGGs_2_Taxid " + UniProtID + "\t" + ";".join(STRING) + "\t" + ";".join(sorted(set(KEGG))) + "\t" + NCBI_Taxid + "\n")
        #
        # for AC in UniProtAC_list:
        #     # fh_out_UniProt_AC_2_ID_2_Taxid.write("{}\t{}\t{}\n".format(AC, UniProtID, NCBI_Taxid))
        #     print("111_UniProt_AC_2_ID_2_Taxid {}\t{}\t{}\n".format(AC, UniProtID, NCBI_Taxid))

def yield_entry_UniProt_dat_dump_parallel():
    """
    yield a single entry, delimited by '//' at the end
    of UniProt DB dump files
    fn_in = "uniprot_sprot.dat.gz"
    '//         Terminator                        Once; ends an entry'
    # ID   D5EJT0_CORAD            Unreviewed;       296 AA.
    # AC   D5EJT0;
    # DT   15-JUN-2010, integrated into UniProtKB/TrEMBL.
    # DT   15-JUN-2010, sequence version 1.
    # DT   25-OCT-2017, entry version 53.
    # DE   SubName: Full=Binding-protein-dependent transport systems inner membrane component {ECO:0000313|EMBL:ADE54679.1};
    # GN   OrderedLocusNames=Caka_1660 {ECO:0000313|EMBL:ADE54679.1};
    # OS   Coraliomargarita akajimensis (strain DSM 45221 / IAM 15411 / JCM 23193
    # OS   / KCTC 12865 / 04OKA010-24).
    # OC   Bacteria; Verrucomicrobia; Opitutae; Puniceicoccales;
    # OC   Puniceicoccaceae; Coraliomargarita.
    # OX   NCBI_TaxID=583355 {ECO:0000313|EMBL:ADE54679.1, ECO:0000313|Proteomes:UP000000925};
    # RN   [1] {ECO:0000313|EMBL:ADE54679.1, ECO:0000313|Proteomes:UP000000925}
    # RP   NUCLEOTIDE SEQUENCE [LARGE SCALE GENOMIC DNA].
    # RC   STRAIN=DSM 45221 / IAM 15411 / JCM 23193 / KCTC 12865
    # RC   {ECO:0000313|Proteomes:UP000000925};
    # RX   PubMed=21304713; DOI=10.4056/sigs.952166;
    # RA   Mavromatis K., Abt B., Brambilla E., Lapidus A., Copeland A.,
    # RA   Deshpande S., Nolan M., Lucas S., Tice H., Cheng J.F., Han C.,
    # RA   Detter J.C., Woyke T., Goodwin L., Pitluck S., Held B., Brettin T.,
    # RA   Tapia R., Ivanova N., Mikhailova N., Pati A., Liolios K., Chen A.,
    # RA   Palaniappan K., Land M., Hauser L., Chang Y.J., Jeffries C.D.,
    # RA   Rohde M., Goker M., Bristow J., Eisen J.A., Markowitz V.,
    # RA   Hugenholtz P., Klenk H.P., Kyrpides N.C.;
    # RT   "Complete genome sequence of Coraliomargarita akajimensis type strain
    # RT   (04OKA010-24).";
    # RL   Stand. Genomic Sci. 2:290-299(2010).
    # CC   -!- SUBCELLULAR LOCATION: Cell membrane
    # CC       {ECO:0000256|RuleBase:RU363032}; Multi-pass membrane protein
    # CC       {ECO:0000256|RuleBase:RU363032}.
    # CC   -!- SIMILARITY: Belongs to the binding-protein-dependent transport
    # CC       system permease family. {ECO:0000256|RuleBase:RU363032,
    # CC       ECO:0000256|SAAS:SAAS00723689}.
    # CC   -----------------------------------------------------------------------
    # CC   Copyrighted by the UniProt Consortium, see http://www.uniprot.org/terms
    # CC   Distributed under the Creative Commons Attribution-NoDerivs License
    # CC   -----------------------------------------------------------------------
    # DR   EMBL; CP001998; ADE54679.1; -; Genomic_DNA.
    # DR   RefSeq; WP_013043401.1; NC_014008.1.
    # DR   STRING; 583355.Caka_1660; -.
    # DR   EnsemblBacteria; ADE54679; ADE54679; Caka_1660.
    # DR   KEGG; caa:Caka_1660; -.
    # DR   eggNOG; ENOG4105C2T; Bacteria.
    # DR   eggNOG; COG1173; LUCA.
    # DR   HOGENOM; HOG000171367; -.
    # DR   KO; K15582; -.
    # DR   OMA; PTGIWWT; -.
    # DR   OrthoDB; POG091H0048; -.
    # DR   Proteomes; UP000000925; Chromosome.
    # DR   GO; GO:0016021; C:integral component of membrane; IEA:UniProtKB-KW.
    # DR   GO; GO:0005886; C:plasma membrane; IEA:UniProtKB-SubCell.
    # DR   GO; GO:0006810; P:transport; IEA:UniProtKB-KW.
    # DR   CDD; cd06261; TM_PBP2; 1.
    # DR   Gene3D; 1.10.3720.10; -; 1.
    # DR   InterPro; IPR000515; MetI-like.
    # DR   InterPro; IPR035906; MetI-like_sf.
    # DR   InterPro; IPR025966; OppC_N.
    # DR   Pfam; PF00528; BPD_transp_1; 1.
    # DR   Pfam; PF12911; OppC_N; 1.
    # DR   SUPFAM; SSF161098; SSF161098; 1.
    # DR   PROSITE; PS50928; ABC_TM1; 1.
    # PE   3: Inferred from homology;
    # KW   Cell membrane {ECO:0000256|SAAS:SAAS00894688};
    # KW   Complete proteome {ECO:0000313|Proteomes:UP000000925};
    # KW   Membrane {ECO:0000256|RuleBase:RU363032,
    # KW   ECO:0000256|SAAS:SAAS00893669};
    # KW   Reference proteome {ECO:0000313|Proteomes:UP000000925};
    # KW   Transmembrane {ECO:0000256|RuleBase:RU363032,
    # KW   ECO:0000256|SAAS:SAAS00894237};
    # KW   Transmembrane helix {ECO:0000256|RuleBase:RU363032,
    # KW   ECO:0000256|SAAS:SAAS00894527};
    # KW   Transport {ECO:0000256|RuleBase:RU363032,
    # KW   ECO:0000256|SAAS:SAAS00723738}.
    # FT   TRANSMEM     34     53       Helical. {ECO:0000256|RuleBase:RU363032}.
    # FT   TRANSMEM     94    119       Helical. {ECO:0000256|RuleBase:RU363032}.
    # FT   TRANSMEM    131    150       Helical. {ECO:0000256|RuleBase:RU363032}.
    # FT   TRANSMEM    156    175       Helical. {ECO:0000256|RuleBase:RU363032}.
    # FT   TRANSMEM    214    239       Helical. {ECO:0000256|RuleBase:RU363032}.
    # FT   TRANSMEM    259    282       Helical. {ECO:0000256|RuleBase:RU363032}.
    # FT   DOMAIN       92    282       ABC transmembrane type-1.
    # FT                                {ECO:0000259|PROSITE:PS50928}.
    # SQ   SEQUENCE   296 AA;  32279 MW;  3DB3B060376AFDB5 CRC64;
    #      MIKQQREAKA VSVAATSLGQ DAWERLKRNN MARIGGTLFA IITALCIVGP WLLPHSYDAQ
    #      NLAYGAQGPS WQHLLGTDDL GRDLLVRILV GGRISIGVGF AASLVALIIG VSYGALAGYI
    #      GGRTESVMMR FVDAVYALPF TMIVIILTVT FDEKSIFLIF MAIGLVEWLT MARIVRGQTK
    #      ALRQLNYIDA ARTMGASHLS ILTRHILPNL LGPVIVFTTL TIPAVILLES ILSFLGLGVQ
    #      PPMSSWGILI NEGADKIDIY PWLLIFPALF FSLTIFALNF IGDGLRDALD PKESQH
    # //
    """
    lines_list = []
    # for line in fileinput.input(mode='rb'):
    # with gzip.open(fileinput.input(mode='rb'), 'rb') as f:
    for line in fileinput.input():
        yield line

        # file_content = f.read().decode()
        # line = zlib.decompress(line.read(), 16+zlib.MAX_WBITS).strip()
        # line = gzip.GzipFile(fileobj=line)
        # print(type(line), line)
        # yield line

        # line = line.decode("utf-8")
        # for line in file_content.split("\n"):

    #     if not line.startswith("//"):
    #         lines_list.append(line)
    #     else:
    #         yield lines_list
    #         lines_list = []
    # if lines_list:
    #     if len(lines_list[0]) == 0:
    #         yield StopIteration
    # else:
    #     yield lines_list

def parse_uniprot_dat_dump_yield_entry_v2_parallel():
    """
    UniProtKeywords
    GO
    InterPro
    Pfam
    KEGG
    Reactome
    @KEGG : I have a mapping from UniProt accession (e.g. "P31946") to KEGG entry (e.g. "hsa:7529")
        what I'm missing is from KEGG entry to KEGG pathway (e.g.
        hsa:7529    path:hsa04110
        hsa:7529    path:hsa04114
        hsa:7529    path:hsa04722)
    """
    for entry in yield_entry_UniProt_dat_dump_parallel():

        # print(type(entry), entry)
        yield entry

        # UniProtAC_list, Keywords_string, functions_2_return = [], "", []
        # Functions_other_list = []
        # UniProtID, NCBI_Taxid = "-1", "-1"
        # for line in entry:
        #     try:
        #         line_code, rest = line.split(maxsplit=1)
        #     except ValueError:
        #         continue
        #
        #     if line_code == "ID":
        #         UniProtID = rest.split()[0]
        #     elif line_code == "AC":
        #         UniProtAC_list += [UniProtAN.strip() for UniProtAN in rest.split(";") if len(UniProtAN) > 0]
        #     elif line_code == "KW":
        #         Keywords_string += rest
        #     elif line_code == "DR":
        #         Functions_other_list.append(rest)
        #     elif line_code == "OX":
        #         # OX   NCBI_TaxID=654924;
        #         # OX   NCBI_TaxID=418404 {ECO:0000313|EMBL:QAB05112.1};
        #         if rest.startswith("NCBI_TaxID="):
        #             NCBI_Taxid = rest.replace("NCBI_TaxID=", "").split(";")[0].split()[0]
        #
        # # UniProtAC_list = sorted(set(UniProtAC_list))Taxid_2_funcEnum_2_scores_table_FIN
        # Keywords_list = [cst.cleanup_Keyword(keyword) for keyword in sorted(set(Keywords_string.split(";"))) if len(keyword) > 0]  # remove empty strings from keywords_list
        # other_functions = cst.helper_parse_UniProt_dump_other_functions(Functions_other_list)
        # # GO, InterPro, Pfam, KEGG, Reactome, STRING, Proteomes
        # functions_2_return.append(Keywords_list)
        # functions_2_return += other_functions
        # yield UniProtID, UniProtAC_list, NCBI_Taxid, functions_2_return

if __name__ == "__main__":
    Protein_2_Function_table_UniProtDump_UPS()