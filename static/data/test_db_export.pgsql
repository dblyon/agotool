--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.3
-- Dumped by pg_dump version 9.5.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: function_2_definition; Type: TABLE; Schema: public; Owner: dblyon
--

CREATE TABLE function_2_definition (
    id integer NOT NULL,
    an character varying NOT NULL,
    definition character varying NOT NULL
);


ALTER TABLE function_2_definition OWNER TO dblyon;

--
-- Name: function_2_definition_id_seq; Type: SEQUENCE; Schema: public; Owner: dblyon
--

CREATE SEQUENCE function_2_definition_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE function_2_definition_id_seq OWNER TO dblyon;

--
-- Name: function_2_definition_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dblyon
--

ALTER SEQUENCE function_2_definition_id_seq OWNED BY function_2_definition.id;


--
-- Name: functions; Type: TABLE; Schema: public; Owner: dblyon
--

CREATE TABLE functions (
    id integer NOT NULL,
    type character varying NOT NULL,
    name character varying NOT NULL,
    an character varying NOT NULL
);


ALTER TABLE functions OWNER TO dblyon;

--
-- Name: functions_id_seq; Type: SEQUENCE; Schema: public; Owner: dblyon
--

CREATE SEQUENCE functions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE functions_id_seq OWNER TO dblyon;

--
-- Name: functions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dblyon
--

ALTER SEQUENCE functions_id_seq OWNED BY functions.id;


--
-- Name: go_2_slim; Type: TABLE; Schema: public; Owner: dblyon
--

CREATE TABLE go_2_slim (
    id integer NOT NULL,
    an character varying NOT NULL,
    slim integer NOT NULL
);


ALTER TABLE go_2_slim OWNER TO dblyon;

--
-- Name: go_2_slim_id_seq; Type: SEQUENCE; Schema: public; Owner: dblyon
--

CREATE SEQUENCE go_2_slim_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE go_2_slim_id_seq OWNER TO dblyon;

--
-- Name: go_2_slim_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dblyon
--

ALTER SEQUENCE go_2_slim_id_seq OWNED BY go_2_slim.id;


--
-- Name: og_2_function; Type: TABLE; Schema: public; Owner: dblyon
--

CREATE TABLE og_2_function (
    id integer NOT NULL,
    og character varying NOT NULL,
    function character varying NOT NULL
);


ALTER TABLE og_2_function OWNER TO dblyon;

--
-- Name: og_2_function_id_seq; Type: SEQUENCE; Schema: public; Owner: dblyon
--

CREATE SEQUENCE og_2_function_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE og_2_function_id_seq OWNER TO dblyon;

--
-- Name: og_2_function_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dblyon
--

ALTER SEQUENCE og_2_function_id_seq OWNED BY og_2_function.id;


--
-- Name: ogs; Type: TABLE; Schema: public; Owner: dblyon
--

CREATE TABLE ogs (
    id integer NOT NULL,
    og character varying NOT NULL,
    taxid integer NOT NULL,
    description character varying NOT NULL
);


ALTER TABLE ogs OWNER TO dblyon;

--
-- Name: ogs_id_seq; Type: SEQUENCE; Schema: public; Owner: dblyon
--

CREATE SEQUENCE ogs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ogs_id_seq OWNER TO dblyon;

--
-- Name: ogs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dblyon
--

ALTER SEQUENCE ogs_id_seq OWNED BY ogs.id;


--
-- Name: ontologies; Type: TABLE; Schema: public; Owner: dblyon
--

CREATE TABLE ontologies (
    id integer NOT NULL,
    child character varying NOT NULL,
    parent character varying NOT NULL,
    direct integer NOT NULL
);


ALTER TABLE ontologies OWNER TO dblyon;

--
-- Name: ontologies_id_seq; Type: SEQUENCE; Schema: public; Owner: dblyon
--

CREATE SEQUENCE ontologies_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ontologies_id_seq OWNER TO dblyon;

--
-- Name: ontologies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dblyon
--

ALTER SEQUENCE ontologies_id_seq OWNED BY ontologies.id;


--
-- Name: peptides; Type: TABLE; Schema: public; Owner: dblyon
--

CREATE TABLE peptides (
    id integer NOT NULL,
    aaseq character varying NOT NULL,
    an character varying NOT NULL,
    missedcleavages integer NOT NULL,
    length integer NOT NULL
);


ALTER TABLE peptides OWNER TO dblyon;

--
-- Name: peptides_id_seq; Type: SEQUENCE; Schema: public; Owner: dblyon
--

CREATE SEQUENCE peptides_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE peptides_id_seq OWNER TO dblyon;

--
-- Name: peptides_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dblyon
--

ALTER SEQUENCE peptides_id_seq OWNED BY peptides.id;


--
-- Name: protein_2_function; Type: TABLE; Schema: public; Owner: dblyon
--

CREATE TABLE protein_2_function (
    id integer NOT NULL,
    an character varying NOT NULL,
    function character varying NOT NULL
);


ALTER TABLE protein_2_function OWNER TO dblyon;

--
-- Name: protein_2_function_id_seq; Type: SEQUENCE; Schema: public; Owner: dblyon
--

CREATE SEQUENCE protein_2_function_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE protein_2_function_id_seq OWNER TO dblyon;

--
-- Name: protein_2_function_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dblyon
--

ALTER SEQUENCE protein_2_function_id_seq OWNED BY protein_2_function.id;


--
-- Name: protein_2_og; Type: TABLE; Schema: public; Owner: dblyon
--

CREATE TABLE protein_2_og (
    id integer NOT NULL,
    an character varying NOT NULL,
    og character varying NOT NULL
);


ALTER TABLE protein_2_og OWNER TO dblyon;

--
-- Name: protein_2_og_id_seq; Type: SEQUENCE; Schema: public; Owner: dblyon
--

CREATE SEQUENCE protein_2_og_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE protein_2_og_id_seq OWNER TO dblyon;

--
-- Name: protein_2_og_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dblyon
--

ALTER SEQUENCE protein_2_og_id_seq OWNED BY protein_2_og.id;


--
-- Name: protein_2_taxid; Type: TABLE; Schema: public; Owner: dblyon
--

CREATE TABLE protein_2_taxid (
    id integer NOT NULL,
    an character varying NOT NULL,
    taxid integer NOT NULL
);


ALTER TABLE protein_2_taxid OWNER TO dblyon;

--
-- Name: protein_2_taxid_id_seq; Type: SEQUENCE; Schema: public; Owner: dblyon
--

CREATE SEQUENCE protein_2_taxid_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE protein_2_taxid_id_seq OWNER TO dblyon;

--
-- Name: protein_2_taxid_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dblyon
--

ALTER SEQUENCE protein_2_taxid_id_seq OWNED BY protein_2_taxid.id;


--
-- Name: protein_2_version; Type: TABLE; Schema: public; Owner: dblyon
--

CREATE TABLE protein_2_version (
    id integer NOT NULL,
    an character varying NOT NULL,
    version character varying NOT NULL
);


ALTER TABLE protein_2_version OWNER TO dblyon;

--
-- Name: protein_2_version_id_seq; Type: SEQUENCE; Schema: public; Owner: dblyon
--

CREATE SEQUENCE protein_2_version_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE protein_2_version_id_seq OWNER TO dblyon;

--
-- Name: protein_2_version_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dblyon
--

ALTER SEQUENCE protein_2_version_id_seq OWNED BY protein_2_version.id;


--
-- Name: proteins; Type: TABLE; Schema: public; Owner: dblyon
--

CREATE TABLE proteins (
    id integer NOT NULL,
    an character varying NOT NULL,
    header character varying NOT NULL,
    aaseq character varying NOT NULL
);


ALTER TABLE proteins OWNER TO dblyon;

--
-- Name: proteins_id_seq; Type: SEQUENCE; Schema: public; Owner: dblyon
--

CREATE SEQUENCE proteins_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE proteins_id_seq OWNER TO dblyon;

--
-- Name: proteins_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dblyon
--

ALTER SEQUENCE proteins_id_seq OWNED BY proteins.id;


--
-- Name: taxa; Type: TABLE; Schema: public; Owner: dblyon
--

CREATE TABLE taxa (
    id integer NOT NULL,
    taxid integer NOT NULL,
    taxname character varying NOT NULL,
    scientific integer
);


ALTER TABLE taxa OWNER TO dblyon;

--
-- Name: taxa_id_seq; Type: SEQUENCE; Schema: public; Owner: dblyon
--

CREATE SEQUENCE taxa_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE taxa_id_seq OWNER TO dblyon;

--
-- Name: taxa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dblyon
--

ALTER SEQUENCE taxa_id_seq OWNED BY taxa.id;


--
-- Name: taxid_2_rank; Type: TABLE; Schema: public; Owner: dblyon
--

CREATE TABLE taxid_2_rank (
    id integer NOT NULL,
    taxid integer NOT NULL,
    rank character varying NOT NULL
);


ALTER TABLE taxid_2_rank OWNER TO dblyon;

--
-- Name: taxid_2_rank_id_seq; Type: SEQUENCE; Schema: public; Owner: dblyon
--

CREATE SEQUENCE taxid_2_rank_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE taxid_2_rank_id_seq OWNER TO dblyon;

--
-- Name: taxid_2_rank_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dblyon
--

ALTER SEQUENCE taxid_2_rank_id_seq OWNED BY taxid_2_rank.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY function_2_definition ALTER COLUMN id SET DEFAULT nextval('function_2_definition_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY functions ALTER COLUMN id SET DEFAULT nextval('functions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY go_2_slim ALTER COLUMN id SET DEFAULT nextval('go_2_slim_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY og_2_function ALTER COLUMN id SET DEFAULT nextval('og_2_function_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY ogs ALTER COLUMN id SET DEFAULT nextval('ogs_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY ontologies ALTER COLUMN id SET DEFAULT nextval('ontologies_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY peptides ALTER COLUMN id SET DEFAULT nextval('peptides_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY protein_2_function ALTER COLUMN id SET DEFAULT nextval('protein_2_function_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY protein_2_og ALTER COLUMN id SET DEFAULT nextval('protein_2_og_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY protein_2_taxid ALTER COLUMN id SET DEFAULT nextval('protein_2_taxid_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY protein_2_version ALTER COLUMN id SET DEFAULT nextval('protein_2_version_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY proteins ALTER COLUMN id SET DEFAULT nextval('proteins_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY taxa ALTER COLUMN id SET DEFAULT nextval('taxa_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY taxid_2_rank ALTER COLUMN id SET DEFAULT nextval('taxid_2_rank_id_seq'::regclass);


--
-- Data for Name: function_2_definition; Type: TABLE DATA; Schema: public; Owner: dblyon
--

COPY function_2_definition (id, an, definition) FROM stdin;
1	UPK:0001	"Protein which contains at least one 2Fe-2S iron-sulfur cluster: 2 iron atoms complexed to 2 inorganic sulfides and 4 sulfur atoms of cysteines from the protein." []
2	UPK:0002	"Protein, or part of a protein, whose three-dimensional structure has been resolved experimentally (for example by X-ray crystallography or NMR spectroscopy) and whose coordinates are available in the PDB database. Can also be used for theoretical models." []
3	UPK:0003	"Protein which contains at least one 3Fe-4S iron-sulfur cluster: 3 iron atoms complexed to 4 inorganic sulfides and 3 sulfur atoms of cysteines from the protein. In a number of iron-sulfur proteins, the 4Fe-4S cluster can be reversibly converted by oxidation and loss of one iron ion to a 3Fe-4S cluster." []
4	UPK:0004	"Protein which contains at least one 4Fe-4S iron-sulfur cluster: 4 iron atoms complexed to 4 inorganic sulfides and 4 sulfur atoms of cysteines from the protein. In a number of iron-sulfur proteins, the 4Fe-4S cluster can be reversibly converted by oxidation and loss of one iron ion to a 3Fe-4S cluster." []
5	UPK:0937	"Protein involved in the synthesis of abscisic acid (ABA) (5-(1-hydroxy-2,6,6,trimethyl-4-oxocyclohex-2-en-1-y1)-3-methylpenta-2,4-dienoic acid). ABA is a plant hormone which play a role in many aspects of plant growth, development and cellular signaling (e.g. seed dormancy, seed maturation, vegetative growth and responses to various environmental stimuli such as stomatal closure during drought). This phytohormone can be synthesized from farnesyl diphosphate (direct C15 pathway) or from 9-cis-violaxanthine (indirect C40 pathway)." []
6	UPK:0938	"Protein involved in the abscisic acid (ABA) (5-(1-hydroxy-2,6,6,trimethyl-4-oxocyclohex-2-en-1-y1)-3-methylpenta-2,4-dienoic acid) signaling pathway (e.g. transport and signal transduction) that regulates many aspects of plant growth, development and cellular signaling (e.g. seed dormancy, seed maturation, vegetative growth and responses to various environmental stimuli such as stomatal closure during drought). This phytohormone can be synthesized from farnesyl diphosphate (direct C15 pathway) or from 9-cis-violaxanthine (indirect C40 pathway)." []
7	UPK:0005	"Protein involved in the synthesis of acetoin (3-hydroxy-2-butanone). Acetoin is a component of the butanediol cycle (butanediol fermentation) in microorganisms." []
8	UPK:0006	"Protein involved in the degradation of acetoin (3-hydroxy-2-butanone). Acetoin is a component of the butanediol cycle (butanediol fermentation) in microorganisms." []
9	UPK:0007	"Protein which is posttranslationally modified by the attachment of at least one acetyl group; generally at the N-terminus." []
10	UPK:0008	"Toxin which interferes with the function of the nicotinic acetylcholine receptor (nAChR). The nAChR is a postsynaptic membrane protein that undergoes an extensive conformational change upon binding to acetylcholine, leading to opening of an ion-conducting channel across the plasma membrane. These toxins are mostly found in snake and cone snail venoms." []
11	UPK:0117	"Protein that binds to the free end of the actin filament and thereby blocks further addition of subunits." []
12	UPK:0009	"Protein which binds to actin, and thereby can modulate the properties and/or functions of the actin filament." []
13	UPK:1178	"Viral protein that allows the active transport of viral material along actin filaments toward the intracellular replication sites during virus entry. This transport probably involves motor proteins like myosins or polymerization/depolymerization reactions as a driving force. Viruses such as poliovirus may utilize this type of intracellular transport." []
14	UPK:1072	"Viral protein involved in the activation of host autophagy. Autophagy is a major intracellular pathway in the delivery of cytoplasmic material to lysosomes for degradation. It is also essential for the removal of pathogenic protein aggregates from the cell during infection. Although autophagy is clearly important for antiviral immune response, it can also be activated by viruses and serves as platform for viral replication. Some viruses such as poliovirus, use the autophagic pathway as a nonlytic mechanism for viral release." []
15	UPK:1073	"Viral protein involved in the activation of host cell apoptosis by acting on host caspases. While many viruses encode protein that inhibit apoptosis, viruses can also use apoptosis to their advantage to suppress immune response or to disseminate. Therefore, some viral proteins are able to cleave or activate caspases in order to promote apoptosis." []
16	UPK:1074	"Viral protein involved in the activation of host NF-kappa-B. This protein is a pleiotropic transcription factor which is present in almost all cell types and is involved in many biological processed such as inflammation, immunity, differentiation, cell growth, tumorigenesis and apoptosis. Several viruses have developed strategies to activate the NF-kappa-B pathway in order to promote viral replication and prevent virus-induced apoptosis." []
17	UPK:0010	"Protein that positively regulates either the transcription of one or more genes, or the translation of mRNA." []
18	UPK:0011	"Protein involved in acute phase, a response of the vertebrate body to insults, infections, immunological reactions or inflammatory processes; characterised by redness (rubor), heat (calor), swelling (tumor), pain (dolor) and sometimes loss of function." []
19	UPK:0012	"Enzyme catalyzing the transfer of acyl- (RCO-) groups." []
20	UPK:1064	"Protein involved in adaptive immunity. Vertebrates can develop a broad and almost infinite repertoire of antigen-specific receptors, which allows vertebrates to recognize almost any potential pathogen or toxin and to mount antigen-specific responses to it. Two types of adaptive immunity systems have evolved in vertebrates in order to generate immune receptor diversity. The jawed vertebrates strategy uses the V(D)JC recombination to achieve combinatorial diversity of immunoglobulin-based B cell receptors and T cell receptors. The jawless vertebrate strategy uses the somatic rearrangements of variable leucine-rich cassettes in the variable lymphocyte receptors (VLRs). The hallmarks of an adaptive immune system is the production of antigen-specific recognition receptor by somatic gene rearrangement. The long life of some antigen-primed cytotoxic lymphocytes and plasma cells provide protective memory to prevent reinvasion." []
21	UPK:0013	"Protein which is posttranslationally modified by the attachment of at least one ADP-ribosyl group." []
22	UPK:0913	"Protein which, if defective, causes age-related macular degeneration (ARMD), the most common cause of irreversible vision loss in the developed world. In most patients, the disease is manifest as ophthalmoscopically visible yellowish accumulations of protein and lipid (known as drusen) that lie beneath the retinal pigment epithelium and within an elastin-containing structure known as Bruch's membrane. ARMD is likely to be a mechanistically heterogeneous group of disorders, and the specific disease mechanisms that underlie the vast majority of cases are currently unknown. However, a number of studies have suggested that both genetic and environmental factors are likely to play a role." []
23	UPK:0948	"Protein which, if defective, causes Aicardi-Goutieres syndrome, a genetic disorder that is phenotypically similar to in utero viral infection. The disease is characterized by severe neurological dysfunction in infancy, leading to progressive microcephaly, spasticity, dystonic posturing, profound psychomotor retardation and often death in early childhood." []
24	UPK:0014	"Protein encoded by the human immunodeficiency viruses HIV-1 or HIV-2, which are the cause of acquired immunodeficiency syndrome (AIDS). This disease is characterized by a severe defect of cell-mediated immunity which is often accompanied by cancers such as Kaposi's sarcoma, as well as secondary infections such as tuberculosis." []
25	UPK:0015	"Protein which, if defective, causes albinism, a genetically determined or environmentally induced absence of pigmentation in animals normally pigmented. This can lead for example to lack of pigmentation in hair, skin and eyes." []
26	UPK:0016	"Protein involved in the synthesis of alginate. Alginate is an exopolysaccharide in the cell walls of brown algae and in the capsular material of certain strains of Pseudomonas and Azotobacter, in which it provides a protective barrier against host immune defenses and antibiotics." []
27	UPK:0017	"Protein involved in a biochemical reaction with alkaloids, a group of nitrogenous organic molecules (mostly heterocyclic) usually found in plants. Various alkaloids have toxic or medical properties, such as caffeine, morphine and nicotine." []
28	UPK:0019	"Protein involved in alkylphosphonate uptake. Certain bacteria such as Escherichia coli can use alkylphosphonates as a phosphorus source." []
29	UPK:0020	"Protein that stimulates the production of, and reacts with, antibodies (IgE) thus creating an allergic reaction (immediate-type hypersensitivity). Examples are pollen allergens from plants, venom allergens from insects, dust-mite allergens, and animal hair allergens." []
30	UPK:0021	"Enzyme whose activity is modified by the noncovalent binding of an allosteric effector at a site other than the active site. This binding mediates conformational changes, altering its catalytic or binding properties." []
31	UPK:0022	"Protein that inhibits alpha-amylase, an enzyme that catalyzes the endohydrolysis of 1,4-alpha-glucosidic linkages in oligosaccharides and polysaccharides." []
32	UPK:0023	"Protein which, if defective, causes Alport syndrome, an hereditary disorder characterized by a progressive glomerulonephritis leading to end-stage renal disease, often associated with sensorineural hearing loss and ocular abnormalities." []
33	UPK:0024	"Protein for which at least two isoforms exist due to the usage of alternative initiation codons in the same mRNA (the resulting isoforms differ in their N-terminus if they are in frame)." []
34	UPK:0877	"Protein for which at least two isoforms exist due to the alternative usage of promoters." []
35	UPK:0025	"Protein for which at least two isoforms exist due to distinct pre-mRNA splicing events." []
36	UPK:0026	"Protein which, if defective, causes Alzheimer disease, a neurodegenerative disorder characterized by progressive dementia and global loss of cognitive abilities. The condition primarily occurs after age 60, and is marked pathologically by severe cortical atrophy, senile plaques, neurofibrillary tangles, and neuropil threads. Early-onset forms also occurr." []
37	UPK:0986	"Protein which, if defective, causes amelogenesis imperfecta, a clinically and genetically heterogeneous group of disorders affecting the dental enamel. The enamel may be hypoplastic, hypomineralized or both, and affected teeth may be discoloured, sensitive or prone to disintegration either pre-eruption or post-eruption. In the hypoplastic type of amelogenesis imperfecta, the enamel is of normal hardness but does not develop to normal thickness. In the hypomineralized type, the enamel is of normal thickness but opaque or yellowish white without lustre on newly erupted teeth; it is so soft that it is lost soon after eruption. Amelogenesis imperfecta occasionally occurs in conjunction with other dental, oral and extra-oral features." []
38	UPK:0027	"Peptide which is posttranslationally modified by C-terminal amidation. The amino acid to be modified is almost always followed by a glycine, which provides the amide group. In a first reaction step the glycine is oxidized to form alpha-hydroxy-glycine. The oxidized glycine cleaves into the C-terminally amidated peptide and an N-glyoxylated peptide. C-terminal amidation is essential to the biological activity of many neuropeptides and hormones. In a few cases alpha-oxidative cleavage of an amino acid other than glycine has been observed. All such cases are additionally annotated with the word "atypical" in the feature description." []
39	UPK:0028	"Protein involved in the synthesis of naturally-occuring amino acids. In addition to their use for protein biosynthesis, they are the precursors of many molecules such as purines, pyrimidines, histamines, adrenaline and melanin." []
40	UPK:0029	"Protein involved in the transport of amino acids." []
41	UPK:0030	"Enzyme that activates an amino acid for translation by forming an aminoacyladenylate intermediate and then links this activated amino acid to the corresponding tRNA molecule (amino acid-tRNA, aminoacyl-tRNA). In general, a specific aminoacyl-tRNA synthase is available for each amino acid." []
42	UPK:0031	"Enzyme that catalyzes the removal of amino acids from the N-terminus of peptides and proteins." []
43	UPK:0032	"Enzyme that catalyzes the transfer of an alpha-amino group from an amino acid to an alpha-keto acid. The amino group is usually covalently bound by the prosthetic group pyridoxal phosphate." []
44	UPK:0924	"Protein involved in the transport of ammonia/ammonium. Ammonia is an excellent nitrogen source for many bacteria, fungi, and plants, but it can be cytotoxic, especially for animal cells at high concentration. Its transport across cellular membranes is thus of high biological relevance. Ammonia (NH3) is a weak base and exists predominantly as the ammonium ion (NH4+) in biological fluids." []
45	UPK:0878	"Protein specifically found in the skin of animals belonging to the vertebrate class amphibia, that includes frogs, toads, newts, salamanders and worm-like apoda. The skins of anuran amphibians, in addition to mucous glands, contain highly specialized poison glands, which, in reaction to stress or attack, exude a complex noxious species-specific cocktail of biologically active molecules. These secretions often contain a plethora of peptides such as neuropeptides and hormones. The frog dermatous glands also synthesize and store an extraordinarily rich variety of wide-spectrum antimicrobial peptides that are released onto the outer layer of the skin to provide an effective and fast-acting defense against harmful microorganisms." []
92	UPK:0070	"Protein which, if defective, causes autoimmune inflammation of the uvea, which is the vascular middle coat of the eye, comprising the iris, ciliary body and choroid." []
46	UPK:0034	"Proteins which may form wide, insoluble, unbranched filaments possessing a cross-beta sheet quaternary structure, where the beta sheets are oriented perpendicular to the fibre axis. Amyloid fibrils may be involved in abnormal protein depositions, or amyloidosis, such as Alzheimer's or Parkinson's diseases. Functional amyloids, found in a wide range of organism, from bacteria to mammals are involved in diverse functions such as biofilm formation, formation of aerial hyphae, long-term memory or regulation of melanin biosynthesis." []
47	UPK:1008	"Protein which, if defective, causes amyloidosis, a vast group of diseases defined by the accumulation of amyloid in tissues. Amyloidoses are classified according to clinical signs, biochemical type of amyloid protein involved, and the extent of amyloid deposition (generalized or localized). Most amyloidoses are multisystemic diseases affecting several organs or systems. Mainly affected organs are the kidneys, heart, gastrointestinal tract, liver, skin, peripheral nerves and eyes, but any organ can be affected. The most frequent forms are primary amyloidosis, also known as light-chain immunoglobulin amyloidosis (AL), reactive or inflammatory amyloidosis, also known as acquired amyloidosis (AA), and transthyretin amyloidosis (ATTR). Localized amyloidosis affecting the brain is characteristic of Alzheimer's disease, trisomy 21, and prion diseases (transmissible spongiform encephalitis, Creutzfeldt-Jakob disease, Gerstmann-Straussler-Scheinker syndrome, fatal familial insomnia). In prion diseases the amyloid precursor is the prion protein." []
48	UPK:0035	"Protein found in the amyloplast, a colorless plant plastid that forms and stores starch. Amyloplasts are found in many tissues, particularly in storage tissues." []
49	UPK:0036	"Protein which, if defective, causes amyotrophic lateral sclerosis (ALS), a degenerative disorder of motor neurons in the cortex, brain stem and spinal cord. ALS is characterized by muscular weakness and atrophy." []
50	UPK:0037	"Protein involved in angiogenesis, the sprouting or splitting of capillaries from pre-existing vasculature. Angiogenesis plays an important role for example during embryonic development, normal growth of tissues and maintenance of the normal vasculature, wound healing, tumor growth and metastasis." []
51	UPK:0039	"Protein involved in the exchange of anions across a membrane. Anion exchange is a cellular transport function which contributes to the regulation of cell pH and volume by a functionally related anion exchanger protein family." []
52	UPK:0040	"Protein containing at least one ANK repeat, a conserved domain of approximately 33 amino acids, that was originally identified in ankyrin. It has been described as an L-shaped structure consisting of a beta-hairpin and two alpha-helices. Many ankyrin repeat regions are known to function as protein-protein interaction domains." []
53	UPK:0041	"Protein containing at least one annexin repeat, a conserved domain of 61 residues, which is present in proteins of the annexin family in either four or eight copies. The annexin calcium binding sites are found within the repeated domains." []
54	UPK:0042	"Component of an antenna complex or protein regulating the expression of such components. Antenna complexes are light-harvesting systems (LHC) which are protein-pigment complexes in or on photosynthetic membranes. LHCs receive radiant energy and transfer it to the reaction centers; an array of LHCs is often referred to as an "antenna". LHCs typically include one or more associated pigments (phycobilins, chlorophylls, bacteriochlorophylls and carotenoids)." []
55	UPK:0044	"Protein with antibacterial activity." []
56	UPK:0045	"Protein involved in the synthesis of antibiotics. Antibiotics are organic compounds produced by living organims that can selectively inhibit the growth of, or kill bacteria." []
57	UPK:0046	"Protein that confers, on bacteria, the ability to withstand antibiotics. The resistance is often due either to mutations that prevent antibiotic binding to the protein or to amplification of the gene encoding the protein." []
58	UPK:0047	"Protein that lowers the freezing point of blood or other biological fluids by inhibiting the formation of water ice crystals." []
59	UPK:0929	"Protein which has deleterious effects on any type of microbe. Microbe is a general term for microscopic unicellular organisms, such as bacteria, archaea, fungi and protista. While the term microbe is often also used for viruses, we do not apply the keyword antimicrobial to antiviral proteins." []
60	UPK:0049	"Protein capable of counteracting the damaging effects of oxidation, e.g. by trapping free radicals generated during the metabolic burst and possibly inhibiting ageing. Scavengers of highly reactive and harmful oxygen species." []
61	UPK:0050	"Protein involved in the transport of a solute across a biological membrane coupled, directly, to the transport of a different solute in the opposite direction." []
62	UPK:0051	"Protein synthesized or activated in the cell in response to viral infection, or protein with specific antiviral activity within the cell. Eukaryotic cells have an innate immune mechanism to fight viral infection, which is activated through the interferon signaling pathway or through dsRNA detection in the cytoplasm. It leads to the establishment of an antiviral cell state, which prevents virus replication or induces apoptosis. Most viruses have developed specific proteins to prevent the establishment of an antiviral state. About half of all bacteria and most archaea have a CRISPR (clustered regularly interspersed short plaindromic repeats) system of adaptive immunity to exogenous DNA. CRISPRs clusters are tandem arrays of alternating repeats and spacers, where the spacers in some cases are homologous to sequences from virus and plasmid genomes. The CRISPR arrays are transcribed, processed and in some way aid in detection and resistance to foreign DNA. In at least a few bacteria (E.coli, S.epidermidis) it seems DNA is the target, whereas in Pyrococcus furiosis it seems the CRISPR system targets RNA." []
63	UPK:0930	"Protein with antiviral activity. Often this activity is fortuitous (e.g. a bacterial protein displaying anti-HIV activity)." []
64	UPK:0993	"Protein which, if defective, causes aortic aneurysm. Aortic aneurysm is the dilation of the wall of the aorta. It forms a sac that is filled with fluid or clotted blood, often resulting in a pulsating tumor. Aortic aneurysms are classified by their location on the aorta." []
65	UPK:0933	"Protein encoded by the apicoplast genome or protein located in the apicoplast, a plastid found in some apicomplexan parasites which is a non-photosynthetic plastid relict. This organelle contains ring-like DNA of about 35 Kb as a third type of cell genome. Apicoplasts do not contain thylakoids; it is not yet clear if they contain internal membranes." []
66	UPK:0052	"Protein which is found in the part of the plant which is external to the living protoplast, ie the cell wall, the intercellular space and the lumina of dead cells such as xylem vessels and tracheids." []
93	UPK:0071	"Protein involved in the synthesis of an autoinducer, a molecule which triggers the regulators of biosynthetic genes." []
67	UPK:0053	"Protein involved in apoptotic programmed cell death. Apoptosis is characterized by cell morphological changes, including blebbing, cell shrinkage, nuclear fragmentation, chromatin condensation and chromosomal DNA fragmentation, and eventually death. Unlike necrosis, apoptosis produces cell fragments, called apoptotic bodies, that phagocytic cells are able to engulf and quickly remove before the contents of the cell can spill out onto surrounding cells and cause damage. In general, apoptosis confers advantages during an organism's life cycle." []
68	UPK:0054	"Protein involved in arabinose breakdown. Arabinose is a 5-carbon aldose sugar found in plant gums, pectins and bacterial cell wall polysaccharides." []
69	UPK:0974	"Archaeal protein present in a flagellum, a long hair-like cell surface appendage made of polymerized flagellin with an attached hook. This rotating structure with switches propels the cell through a liquid medium. The archaeal flagellum is distinct from its bacterial equivalent in terms of architecture, composition and mechanism of assembly. Thinner (10-15 nm) compared to the bacterial flagellum (18-24 nm), it is usually composed of several types of flagellins and is glycosylated. The archaeal flagellum is considered as a type IV pilus-like structure." []
70	UPK:1209	"Protein which is involved in the formation, organization or maintenance of the archaeal flagellum, a long hair-like cell surface appendage made of polymerized flagellin with an attached hook. This rotating structure with switches propels the cell through a liquid medium. The archaeal flagellum is distinct from its bacterial equivalent in terms of architecture, composition and mechanism of assembly. Thinner (10-15 nm) compared to the bacterial flagellum (18-24 nm), it is usually composed of several types of flagellins and is glycosylated. The archaeal flagellum is considered as a type IV pilus-like structure." []
71	UPK:0055	"Protein involved in the synthesis of the basic amino acid arginine (Arg)." []
72	UPK:0056	"Protein involved in biochemical reactions with the basic amino acid arginine (Arg)." []
73	UPK:0057	"Protein involved in the synthesis of an amino acid with an aromatic side-chain: phenylalanine (Phe), tyrosine (Tyr) and tryptophan (Trp)." []
74	UPK:0058	"Protein involved in the breakdown of aromatic hydrocarbons. Aromatic hydrocarbons are compounds which only contain carbon and hydrogen, examples include the common pollutants benzene and naphthalene." []
75	UPK:0059	"Protein that confers, on bacteria and other microorganisms, the ability to withstand aromatic compounds of arsenic." []
76	UPK:0060	"Protein involved in the synthesis of ascorbate, the ionized form of ascorbic acid (vitamin C). Ascorbic acid is derived from glucose via the uronic acid pathway. This water-soluble vitamin is essential for the synthesis of bone, cartilage and dentine. It is required in the diet of primates and some other species that cannot synthesize L-ascorbic acid because of their deficiency in L-gulono-gamma-lactone oxidase, a key enzyme for the biosynthesis of this vitamin." []
77	UPK:0061	"Protein involved in the synthesis of the polar amino acid asparagine (Asn)." []
78	UPK:0062	"Protein which inhibits the catalytic activity of an aspartyl protease, a class of proteases that contains an active site aspartate residue (Asp), e.g. pepsin, HIV retropepsin, renin, etc." []
79	UPK:0063	"Enzyme which catalyzes the hydrolysis of esters and is characterized by a catalytically active aspartic acid residue in its active site." []
80	UPK:0064	"Proteolytic enzyme with an aspartate residue (Asp) in its active site. There are many families of aspartyl proteases. The most well known one is the pepsin family (A1 in MEROPS classification) which is known to exist in vertebrates, fungi, plants, retroviruses and some plant viruses." []
81	UPK:1270	"Protein which, if defective, is involved in Asperger syndrome, a complex, multifactorial disorder. It is characterized by clinically significant impairment of social interaction, and restricted repetitive and stereotyped patterns of behavior. Asperger syndrome is primarily distinguished from autism by the higher cognitive abilities and a more normal and timely development of language and communicative phrases." []
82	UPK:1058	"Protein which, if defective, is associated with asthma, a bronchial disorder associated with airway inflammation, swelling and obstruction. It is marked by recurrent attacks of paroxysmal dyspnea, with wheezing due to spasmodic contraction of the bronchi." []
83	UPK:0065	"Protein which, if defective, causes atherosclerosis, which is characterized by deposits of plaques (atheromas) in the blood vessels, thus narrowing the vessel lumen and restricting blood flow. Atheromas consist of lipids (cholesterol), carbohydrates, blood products, fibrous tissue and calcium deposits." []
84	UPK:0066	"Protein involved in the synthesis of adenosine 5'-triphosphate (ATP). ATP is a ribonucleotide adenosine (a purine base adenine linked to the sugar D-ribofuranose) which carries 3 phosphate groups esterified to the sugar moiety. It is the cell's source for energy and phosphate." []
85	UPK:0067	"Protein which binds adenosine 5'-triphosphate (ATP), a ribonucleotide adenosine (a purine base adenine linked to the sugar D-ribofuranose) that carries three phosphate groups esterified to the sugar moiety. It is the cell's source for energy and phosphate." []
86	UPK:1020	"Protein which, if defective, causes atrial fibrillation, a common cardiac arrhythmia marked by disorganized atrial electrical activity and rapid randomized contractions of small areas of the atrial myocardium, causing a totally irregular, and rapid, ventricular rate." []
87	UPK:0976	"Protein which, if defective, causes atrial septal defect, a congenital cardiac anomaly characterized by persistent patency of the atrial septum that results in blood flow between the atria. It is due to failure of fusion between either the septum secundum or the septum primum and the endocardial cushions." []
88	UPK:1269	"Protein which, if defective, is involved in autism, a pervasive developmental disorder. It is a complex, multifactorial disease characterized by impairments in reciprocal social interaction and communication, restricted and stereotyped patterns of interests and activities, and the presence of developmental abnormalities by 3 years of age. Most individuals with autism manifest moderate mental retardation." []
89	UPK:1268	"Protein which, if defective, is involved in autism spectrum disorder, a clinically heterogeneous group of disorders that share common features of impaired social relationships, impaired language and communication, repetitive behaviors, and a restricted range of interests. The spectrum includes diverse phenotypic manifestations, such as classic autism, Asperger syndrome, childhood disintegrative disorder, Rett syndrome, and pervasive developmental disorder not otherwise specified." []
90	UPK:0068	"Protein catalyzing its own cleavage." []
91	UPK:0069	"Protein which, if defective, causes autoimmune encephalomyelitis. This form of autoimmune inflammation of the brain and spinal cord causes demyelination." []
94	UPK:0072	"Protein participating in autophagy, a process of intracellular bulk degradation in which cytoplasmic components including organelles are sequestered within double-membrane vesicles that deliver the contents to the lysosome/vacuole for degradation. There are three primary forms of autophagy: chaperone-mediated autophagy, microautophagy and macroautophagy. During macroautophagy, the sequestering vesicles, termed autophagosomes, fuse with the lysosome or vacuole resulting in the delivery of an inner vesicle (autophagic body) into the lumen of the degradative compartment." []
95	UPK:0073	"Protein involved in the synthesis of auxins. Auxins are plant hormones which play a role in many aspects of plant growth and development." []
96	UPK:0927	"Protein involved in the auxin signaling pathway (e.g. transport and signal transduction) that regulates many aspects of plant growth and development (e.g. caulogenesis, rhizogenesis, tropisms, nodulation). The major form of this phytohormone is indole-3-acetic acid (IAA) that can be synthesized both from tryptophan (Trp) using Trp-dependent pathways and from an indolic Trp precursor via Trp-independent pathways. Plants can also obtain IAA by b-oxidation of indole-3-butyric acid (IBA), a second endogenous auxin, or by hydrolysing IAA conjugates, in which IAA is linked to amino acids, sugars or peptides." []
97	UPK:0975	"Bacterial protein present in a flagellum, a long hair-like cell surface appendage. The flagellar apparatus consists of the flagellar filament made of polymerized flagellin, the hook-like structure near the cell surface and a system of rings embedded in the cell enveloppe (the basal body or flagellar motor). The basal body and the hook anchor the whip-like filament to the cell surface. The flagellum is a rotating structure with switches propels the cell through a liquid medium." []
98	UPK:1005	"Protein which is involved in the formation, organization or maintenance of the bacterial flagellum, a long hair-like cell surface appendage. The flagellar apparatus consists of the flagellar filament made of polymerized flagellin, the hook-like structure near the cell surface and a system of rings embedded in the cell enveloppe (the basal body or flagellar motor). The basal body and the hook anchor the whip-like filament to the cell surface. The flagellum is a rotating structure whose switches propels the cell through a liquid medium." []
99	UPK:1006	"Protein which is involved in the export of bacterial flagellar proteins. The bacterial flagellum export apparatus consists of six integral membrane proteins (FlhA, FlhB, FliO, FliP, FliQ and FliR) and three soluble proteins (FliH, FliI and FliJ), and is located at the base of the flagellum. This system is characterized by ATP hydrolysis and a lack of substrate signal peptide cleavage." []
100	UPK:1261	"Viral protein which prevents host gene expression by blocking host transcription or inducing the degradation of the bacterial chromosome. This gives viral transcripts a competitive edge to use the hijacked host translation machinery. Preventing the expression of host proteins is also a strategy to counteract the antiviral response." []
101	UPK:1263	"Viral protein involved in inhibiting transcription of bacterial genes to ensure the shutoff of host proteins expression and give viral transcripts a competitive edge for access to the cellular translation machinery. Preventing the expression of host proteins is also a strategy to counteract the antiviral response. Some bacterial viruses inhibit the host RNAP: bacteriophage SPO1 for example is known to shut off host RNA synthesis." []
102	UPK:0076	"Protein interacting with bacteriochlorophyll, a photosynthetic pigment found in non-oxygenic photosynthetic bacteria. It is a magnesium-porphyrin complex esterified to a long hydrophobic terpenoid side chain (the alcohol phytol). It differs from chlorophyll of oxygenic organisms in the substituents around the tetrapyrrole nucleus of the molecule, and in the absorption spectra. Different bacteria have different species of bacteriochlorophyll." []
103	UPK:0077	"Protein involved in the synthesis of bacteriochlorophylls. These photosynthetic pigments are magnesium-porphyrin complexes with a long hydrophobic terpenoid side chain (the alcohol phytol). Biosynthesis of bacteriochlorophyll is a light-independent reaction." []
104	UPK:0078	"Peptidic antibiotic, often plasmid encoded, produced by specific strains of bacteria that is lethal against other strains of the same or related species. E.g. bacteriocin, colicin, lantibiotic." []
105	UPK:0871	"Protein involved in the synthesis of a bacteriocin." []
106	UPK:0079	"Protein that confers to a bacteria immunity against a specific bacteriocin that it synthesizes." []
107	UPK:0080	"Protein involved in the export of a bacteriocin (bacterial antibiotic)." []
108	UPK:0081	"Enzyme, e.g. lysozyme or endopeptidase, essential for lysis of bacterial cell walls." []
109	UPK:0082	"Protein having a peptide stretch which contains specific cleavage sites for different proteinases, and which enables inhibition of all four classes of proteinases." []
110	UPK:0083	"Protein which, if defective, causes Bardet-Biedl syndrome (BBS), a genetically heterogeneous, autosomal recessive disorder. It is characterized by pigmentary retinopathy, obesity, polydactyly, hypogenitalism, renal malformation and mental retardation. Secondary features include diabetes mellitus, hypertension and congenital heart disease." []
111	UPK:0910	"Protein which, if defective, causes Bartter syndrome (BS). In general, Bartter syndrome refers to a group of autosomal recessive disorders characterized by often severe intravascular volume depletion due to renal salt-wasting associated with low blood pressure, hypokalemic alkalosis, hypercalciuria, and normal serum magnesium levels. Patients with Bartter syndrome are often critically ill from birth onwards, and their long-term clinical course may be complicated by nephrocalcinosis, leading to renal failure. Clinical disease results from defective renal reabsorption of sodium chloride in the thick ascending limb (TAL) of the Henle loop, where only 30% of filtered salt is normally reabsorbed." []
112	UPK:0084	"Protein which is a component of the basement membrane, an extracellular matrix found under epithelial cells and around smooth and striated muscle cells. This matrix contains intrinsic macromolecular components such as collagen, laminin, and sulfated proteoglycans." []
113	UPK:0075	"Protein involved in the activation and proliferation of B-cells. B-cells are activated by the binding of antigen to receptors on its cell surface which causes the cell to divide and proliferate. Some stimulated B-cells become plasma cells, which secrete antibodies. Others become long-lived memory B-cells which can be stimulated at a later time to differentiate into plasma cells." []
114	UPK:0085	"Protein which affects the behavior, the action or reaction, of an organism to a stimulus or situation." []
115	UPK:0086	"Protein which is a dimer of immunoglobulin light chains synthesized in large amounts by patients who have myeloma or bone marrow tumor. Bence-Jones protein is sufficiently small to be excreted by the kidney into urine." []
116	UPK:0087	"Protein which, if defective, causes Bernard Soulier syndrome (BSS), a familial coagulation disorder characterized by a prolonged bleeding time, unusually large platelets, and impaired prothrombin consumption. BSS is caused by a genetic deficiency in platelet membrane glycoprotein Ib alpha chain and platelet glycoprotein IX, where platelets aggregate normally but do not stick to collagen of the sub-endothelial membrane." []
117	UPK:0088	"Protein involved in degradation of bile acids. Bile acids, which exist mainly as bile salts, are a family of carboxylic acid derivatives of cholesterol which play an important role in the digestion and absorption of fat. They are made in the liver, stored in the gallblader, and secreted as needed into the intestines." []
118	UPK:0089	"Protein binding covalently at least one linear tetrapyrrole chromophore, e.g. bilirubin, biliverdin, bilifuscin, biliprasin, choleprasin, bilihumin, and bilicyanin. Bile pigments are produced by breaking down protoporphyrin IX derived from hemoglobin and other heme proteins." []
119	UPK:9999	"Keywords assigned to proteins because they are involved in a particular biological process." []
120	UPK:0090	"Protein involved in the generation of rhythmic pattern of behaviors or activities, e.g. circadian rhythm which is a metabolic or behavioural rhythm within a cycle of 24 hours." []
121	UPK:0091	"Protein involved in the process by which mineral crystals are deposited in an organized fashion in the matrix (either cellular or extracellular) of living organisms. Such process give rise to inorganic-based structures such as bone, tooth, ivory, shells, cuticles, corals or bacterial magnetosomes." []
122	UPK:0092	"Protein which contains at least one biotin as prosthetic group or cofactor (e.g. some carboxylases and decarboxylases, and biotin carboxyl carrier protein) or which binds biotin, like avidin. Biotin is a water-soluble vitamin (member of the B complex vitamins) essential for fatty acid biosynthesis, catabolism, and it acts as a growth factor for many cells." []
123	UPK:0093	"Protein involved in the synthesis of biotin, a prosthetic group for some carboxylase and decarboxylase enzymes. This water-soluble vitamin is essential for fatty acid biosynthesis, catabolism, and it acts as a growth factor for many cells." []
124	UPK:0094	"Protein involved in blood clotting, a complex enzymatic cascade, in which the activated form of one factor catalyzes the activation of the next factor. Both, the extrinsic clotting pathway, induced by a damaged surface, and the intrinsic pathway, induced by a trauma, converge in a final common pathway to form cross-linked fibrin clots." []
125	UPK:1204	"Toxin which activates the blood coagulation cascade, which leads to the production of fibrin clots. Blood coagulation activating toxins include a variety of snake venom proteases." []
126	UPK:1203	"Toxin which inhibits the blood coagulation cascade, which leads to the production of fibrin clots. Blood coagulation inhibiting toxins include a variety of snake venom proteases." []
127	UPK:0095	"Protein belonging to the set of cell surface antigens found chiefly, but not solely, on blood cells. More than fifteen different blood group systems are recognised in humans. In most cases the antigenic determinant resides in the carbohydrate chains of membrane glycoproteins or glycolipids." []
128	UPK:1222	"Toxin which interferes with the function of the bradykinin receptor (BDKR). BDKRs are G-protein coupled receptors whose principal ligand is the 9-amino acid peptide bradykinin." []
129	UPK:1136	"Protein expressed in the bradyzoite stage, a latent, slowly growing and cyst-forming stage in the life cycle of coccidians (e.g. Toxoplasmy). Encysted bradyzoites promote chronic infection and widespread dissemination of the parasite." []
130	UPK:0100	"Protein involved in the synthesis of the essential aliphatic branched-chain amino acids leucine (Leu), isoleucine (Ile) and valine (Val)." []
131	UPK:0101	"Protein involved in the degradation of the branched-chain amino acids leucine (Leu), isoleucine (Ile) and valine (Val)." []
132	UPK:1069	"Protein involved in the synthesis of brassinosteroids, a class of steroid plant hormones. Brassinosteroids are involved in numerous plant processes, such as cell expansion and elongation (in association with auxin), vascular differentiation, pollen elongation and pollen tube formation and protection to plants during chilling and drought stress. Brassinolide is the first isolated brassinosteroid." []
133	UPK:1070	"Protein involved in the brassinosteroid (BR) signaling pathway (e.g. transport and signal transduction) that regulates many aspects of plant growth and development including cell expansion and elongation (in association with auxin), vascular differentiation and pollen elongation and pollen tube formation. Also involved in plants protection during chilling and drought stress. BRs are polyhydroxysteroid phytohormones and over 70 BR compounds have been isolated in plants. Brassinolide was the first BR isolated from Brassica napus and remains one of the most active BR." []
134	UPK:0102	"Protein which is posttranslationally modified by the attachment of at least one bromine." []
135	UPK:0103	"Protein containing at least one bromodomain. The bromodomain is a conserved region, approximately 70 amino acids, characteristic for a class of regulatory proteins. It mediates interactions with proteins that are necessary for transcriptional activation." []
136	UPK:0992	"Protein which, if defective, causes Brugada syndrome, a heart disease characterized by an electrocardiogram pattern showing ST segment elevation in right precordial leads (V1 to V3), incomplete or complete right bundle branch block, and ventricular tachyarrhythmia. In some cases, tachycardia does not terminate spontaneously and it may degenerate into ventricular fibrillation and lead to sudden death." []
137	UPK:0104	"Protein which binds at least one cadmium atom, or protein whose function is cadmium-dependent. Cadmium is a heavy metal, chemical symbol Cd." []
138	UPK:0105	"Protein that confers, on bacteria and other microorganisms, the ability to withstand the transition metal cadmium (Cd)." []
139	UPK:0106	"Protein which binds at least one calcium atom, or protein whose function is calcium-dependent. Calcium is a metal, chemical symbol Ca. Calcium is essential for a variety of bodily functions, such as neurotransmission, muscle contraction and proper heart function." []
140	UPK:0107	"Cell membrane glycoprotein forming a channel in a biological membrane selectively permeable to calcium ions. Calcium is essential for a variety of bodily functions, such as neurotransmission, muscle contraction and proper heart function." []
141	UPK:0108	"Protein which interferes with the function of calcium channels which are membrane proteins forming a channel in a biological membrane selectively permeable to calcium ions. They are found in various venoms from snakes, scorpions and spiders." []
326	UPK:9994	"Keywords assigned to proteins because they have at least one specimen of a specific domain." []
142	UPK:0109	"Protein involved in the transport of calcium ions. Calcium is essential for a variety of bodily functions, such as neurotransmission, muscle contraction and proper heart function." []
143	UPK:1221	"Protein which interferes with the function of calcium-activated potassium channels (KCa) which are membrane proteins forming a channel in a biological membrane selectively permeable to potassium ions and gated by intracellular calcium. They are mostly found in snake and scorpion venoms." []
144	UPK:0111	"Protein which contains at least one binding site for calcium and phospholipid. For example, proteins with annexin repeats, of which a pair may form one binding site for calcium and phospholipid, or some proteins with C2 domains." []
145	UPK:0112	"Protein which binds at least one calmodulin, an ubiquitous small calcium-binding protein. Its binding to proteins may cause a conformational change which either activates or inactivates their function." []
146	UPK:0113	"Protein involved in the cycle of biochemical reactions responsible for photosynthetic CO(2) fixation in many photosynthetic bacteria and in the stroma of plant chloroplasts. The energy and reducing power for this reaction are provided by the ATP and NADPH produced during the light reactions of photosynthesis. The Calvin cycle is the only photosynthetic pathway in C3 plants. In C4 and CAM plants CO(2) is initially fixed into other organic acids that are subsequently decarboxylated to release CO(2) to the Calvin cycle. Non-photosynthetic organism (e.g. Rhizobium) also use the cycle to fix CO(2)." []
147	UPK:0114	"Protein whose function is cAMP-dependent or which catalyzes its hydrolysis. cAMP is the abbreviation for cyclic AMP, adenosine 3',5'-cyclic monophosphate, the first second messenger hormone signaling system to be characterised. It is generated from ATP by the action of adenyl cyclase that is coupled to hormone receptors by G proteins. cAMP activates a specific protein kinase and is inactivated by phosphodiesterase action giving 5'AMP." []
148	UPK:0115	"Protein involved in the synthesis of cAMP. cAMP is the abbreviation for cyclic AMP, adenosine 3',5'-cyclic monophosphate." []
149	UPK:0116	"Protein which binds at least one cAMP. cAMP is the abbreviation for cyclic AMP, adenosine 3',5'-cyclic monophosphate." []
150	UPK:1157	"Protein involved in cap snatching, a process in which a cellular mRNA is cleaved few nucleotides after the 5'cap. The resulting 10- to 13-nucleotides long capped fragment serve as primer for the initiation of viral mRNA synthesis. Cap snatching is used by negative stranded RNA virus which do not encode a guanylyl transferase, like influenza or hantaviruses." []
151	UPK:1232	"Viral decoration protein attached to the capsid of some prokaryotic viruses. Decoration proteins are located on the outermost surface of the capsid and are involved in stabilizing the head structure." []
152	UPK:1231	"Viral protein part of the inner membrane of the capsid, a lipid bilayer contained inside the virion capsid." []
153	UPK:0167	"Structural protein which is part of the complex forming the protective shell around the nucleic acids of the virus. In prokaryotic viruses, this closed shell is also referred to as the head." []
154	UPK:0875	"Protein which is part of a capsule, the protective structure surrounding some bacteria or fungi. The bacterial capsule is a layer of material, usually polysaccharide, attached to the cell wall possibly via covalent attachments to either phospholipid or lipid-A molecules. It has several functions: promote bacterial adhesion to surfaces or interaction with other organisms; act as a permeability barrier, as a defense mechanism against phagocytosis and/or as a nutrient reserve. Among pathogens, capsule formation often correlates with pathogenicity. The fungal capsule is an extracellular layer which lies outside the cell wall and it is usually composed of polysaccharides. It protects the cell from different environmental dangers such as phagocytosis, dessication, etc." []
155	UPK:0972	"Protein which is involved in the formation, organization, maintenance or degradation of the capsule. The capsule is a protective structure surrounding some bacteria or fungi. The bacterial capsule is a layer of material, usually polysaccharide, attached to the cell wall possibly via covalent attachments to either phospholipid or lipid-A molecules. The fungal capsule is an extracellular layer which lies outside the cell wall and it is usually composed of polysaccharides." []
156	UPK:0119	"Protein participating in biochemical reactions in which carbohydrates are involved. Carbohydrate is a general term for sugars and related compounds with the general formula Cn(H2O)n. The smallest are monosaccharides (e.g. glucose); polysaccharides (e.g. starch, cellulose, glycogen) can be large and vary in length." []
157	UPK:0120	"Protein involved in the process of carbon dioxide fixation, e.g. incorporation of carbon dioxide into carbohydrates by photosynthetic organisms or formation of oxaloacetate from pyruvate." []
158	UPK:0121	"Protein that hydrolyzes a C-terminal peptide bond in polypeptide chains." []
159	UPK:0122	"Protein which, if defective, causes cardiomyopathy, a chronic disorder which affects the heart muscle causing a reduced pumping function. It is a major cause of morbidity and mortality." []
160	UPK:0123	"Protein which has a poisonous or deleterious effect upon the heart or other parts of the cardiovascular system." []
161	UPK:0124	"Protein involved in the biosynthesis of carnitine (L-3-hydroxy-4, N,N,N-trimethylaminobutyrate), an essential metabolite with a number of indispensable roles in intermediary metabolism." []
162	UPK:0125	"Protein involved in the synthesis of carotenoids, a group of orange, yellow, red, purple or brown pigments in plants, bacteria and some fungi. Carotenoids, which comprise the carotenes and the xanthophylls, are long polyisoprenoid molecules having conjugated double bonds enabling light absorbtion." []
163	UPK:0898	"Protein which, if defective, causes cataract, a partial or complete ocular opacity that affects the crystalline lens or its capsule, leading to impaired vision or blindness. The many types of cataract are classified by their morphology (size, shape, location) or etiology (cause and time of occurrence). Cataracts may occur as an isolated anomaly, as part of generalized ocular developmental defects, or as a component of a multisystem disorder." []
164	UPK:0127	"Protein involved in the synthesis of catecholamines, which are amine derivatives of catechol (2-hydroxyphenol). They are synthesized from the amino acid tyrosine (Tyr) in sympathetic-nerve terminals and in the adrenal gland. Catecholamines act as hormones or neuro-transmitters, e.g. adrenaline, noradrenaline and dopamine." []
165	UPK:0128	"Protein participating the biochemical reactions in which catecholamines are involved. Catecholamines are amine derivatives of catechol (2-hydroxyphenol). They are synthesized from the amino acid tyrosine (Tyr) in sympathetic-nerve terminals and in the adrenal gland. Catecholamines act as hormones or neuro-transmitters, e.g. adrenaline, noradrenaline and dopamine." []
166	UPK:1166	"Viral protein involved in virus internalization by the host cell via caveolae, which are specialized lipid rafts that form 50-70 nm flask-shaped invaginations of the cell membrane. Caveolins form the structural backbone of caveolae. Internalization via caveolae is not a constitutive process but only occurs upon cell stimulation.Endocytic caveolae deliver their viral content to early endosomes. Caveolae represent a low capacity but highly regulated pathway. This pathway is used by viruses including HPV-31, BK virus, NDV, RSV, Coxsackie B virus, SV40, murine polyomavirus, and Echovirus 1." []
167	UPK:0129	"Protein containing at least one CBS domain, a conserved domain found in a wide range of proteins, which is named after cystathionine beta-synthase (CBS), an enzyme that contains 2 copies of this domain." []
168	UPK:0973	"Protein whose function is c-di-GMP-dependent or which catalyzes its hydrolysis. c-di-GMP is the abbreviation for cyclic di-GMP, bis-(3'-5') cyclic diguanylic acid. It acts as a bacterial second messenger." []
169	UPK:0130	"Protein involved in the adherence of cells to other cells or to a matrix. Cell adhesion is mediated by cell surface proteins." []
170	UPK:1217	"Toxin which interferes with the adherence of cells to other cells or to a matrix. Cell adhesion impairing toxins are mostly found in venom of snakes." []
171	UPK:0131	"Protein involved in the complex series of events by which the cell duplicates its contents and divides into two. The eukaryotic cell cycle can be divided in four phases termed G1 (first gap period), S (synthesis, phase during which the DNA is replicated), G2 (second gap period) and M (mitosis). The prokaryotic cell cycle typically involves a period of growth followed by DNA replication, partition of chromosomes, formation of septum and division into two similar or identical daughter cells." []
172	UPK:0132	"Protein involved in the separation of one cell into two daughter cells. In eukaryotic cells, cell division includes the nuclear division (mitosis) and the subsequent cytoplasmic division (cytokinesis)." []
173	UPK:0997	"Protein found in or associated with the prokaryotic cell inner membrane, a selectively permeable membrane which separates the cytoplasm from the periplasm in prokaryotes with 2 membranes." []
174	UPK:0965	"Protein found in or associated with a cell junction, a cell-cell or cell-extracellular matrix contact within a tissue of a multicellular organism, especially abundant in epithelia. In vertebrates, there are three major types of cell junctions: anchoring junctions (e.g. adherens junctions), communicating junctions (e.g. gap junctions) and occluding junctions (e.g. tight junctions)." []
175	UPK:1003	"Protein found in or associated with the cytoplasmic membrane, a selectively permeable membrane which separates the cytoplasm from its surroundings. Known as the cell inner membrane in prokaryotes with 2 membranes." []
176	UPK:0998	"Protein found in or associated with the prokaryotic cell outer membrane, a selectively permeable membrane which separates the prokaryotic periplasm from its surroundings. Traditionally only Gram-negative bacteria were thought of as having an outer membrane, but recent work has shown some Actinobacteria, including Mycobacterium tuberculosis, as well as at least 1 archaea (Ignicoccus hospitalis) have a cell outer membrane." []
177	UPK:0966	"Protein found in or associated with a cell protrusion such as pseudopodium, filopodium, lamellipodium, growth cone, flagellum, acrosome or axon, or bacterial comet tail. These membrane-cytoskeleton-coupled processes are involved in many biological functions, such as cell motility, cancer-cell invasion, endocytosis, phagocytosis, exocytosis, pathogen infection, neurite extension and cytokinesis." []
178	UPK:0133	"Protein involved in the formation and maintenance of the cell shape, the physical dimensions of a cell. In most plants, algae, bacteria and fungi the cell wall is responsible for the shape of the cells." []
179	UPK:0134	"Protein found in or associated with a complex and rigid layer surrounding the cell. Cell walls are found in bacteria, archaea, fungi, plants, and algae. The cell wall is surrounded by the outer membrane in gram-negative bacteria, and envelopes the inner or plasma membrane in gram-negative, gram-positive and acid-fast bacteria. Cell walls of bacteria contain peptidoglycan whereas those of archaea do not. Some archaea may contain pseudopeptidoglycan, which is composed of N-acetyltalosaminuronic acid, instead of N-acetyl muramic acid in peptidoglycan. The plant cell wall is made of fibrils of cellulose embedded in a matrix of several other kinds of polymers such as pectin and lignin. Algal cell walls are usually composed of cellulose, glycoproteins, sporopollenin, calcium and various polysaccharides such as manosyl, xylanes, alginic acid. Diatom cell walls (or frustules) contain silica. The cell wall plays a role in cell shape, cell stability and development, and protection against environmental dangers." []
180	UPK:0961	"Protein which is involved in the formation, organization, maintenance or degradation of the cell wall. The cell wall is an extracellular layer outside the cell membrane which protects the cell against mechanical damage, osmotic strength and which determines the cell shape. It is prominent in most plants, algae, bacteria and fungi." []
181	UPK:9998	"Keywords assigned to proteins because they are found in a specific cellular or extracellular component." []
182	UPK:0135	"Protein involved in the synthesis of cellulose, a linear polymer of (1-4)-beta-linked D-glucose subunits. It is the most abundant cell-wall and structural polysaccharide in plants and it is also found in some lower invertebrates. Cellulose is the major component of wood and thus of paper. Cotton is the purest natural form of cellulose. As a raw material, it forms the basis for many derivatives used in chromatography, ion exchange materials, explosives manufacturing and pharmaceutical preparations." []
183	UPK:0136	"Protein involved in the conversion of cellulose into D-glucose. Cellulose is the most abundant cell-wall and structural polysaccharide in plants and it is also found in some lower invertebrates. Cellulose is the major component of wood and thus of paper. Cotton is the purest natural form of cellulose. As a raw material, it forms the basis for many derivatives used in chromatography, ion exchange materials, explosives manufacturing and pharmaceutical preparations." []
184	UPK:0137	"Protein which binds centromeres or which is required for the assembly and movement of centromeres. Centromeres are the regions of replicated eukaryotic chromosomes where the two chromatids are joined together." []
185	UPK:0138	"Protein component of the F-type ATP synthase complex CF(0) or protein involved in its assembly. F-type ATPases consist of the two complex components CF(0), the membrane proton channel, and CF(1), the catalytic core." []
186	UPK:0139	"Protein component of the F-type ATP synthase complex CF(1) or protein involved in its assembly. F-type ATPases consist of the two complex components CF(0), the membrane proton channel, and CF(1), the catalytic core." []
187	UPK:0140	"Protein whose function is cGMP-dependent or which catalyzes its hydrolysis. cGMP is the abbreviation for cyclic GMP, guanosine 3',5'-cyclic monophosphate. It acts as a second messenger." []
188	UPK:0141	"Protein involved in the synthesis of cGMP. cGMP is the abbreviation for cyclic GMP, guanosine 3',5'-cyclic monophosphate." []
189	UPK:0142	"Protein which binds at least one cGMP. cGMP is the abbreviation for cyclic GMP, guanosine 3',5'-cyclic monophosphate." []
190	UPK:0143	"Protein which is transiently involved in the noncovalent folding, assembly and/or disassembly of other polypeptides or RNA molecules, including any transport and oligomerisation processes they may undergo, and the refolding and reassembly of protein and RNA molecules denatured by stress. Though involved in these processes, chaperones are not an integral part of these functioning molecules. Also used for metallochaperones, which function to provide a metal directly to target proteins while protecting this metal from scavengers." []
191	UPK:0144	"Protein which, if defective, causes Charcot-Marie-Tooth disease (CMT), a heterogeneous group of hereditary motor and sensory neuropathies (HMSN) characterized by distal muscular atrophy and weakness, hollow feet, absent or diminished deep-tendon reflexes and impaired sensation. CMT is classified into two major classes. CMT type 1 includes demyelinating neuropathies that are characterized by nerve conductance velocities (NCVs) less than 38m/s and segmental demyelination and remyelination; CMT type 2 includes axonal neuropathies that are characterized by normal or mildly reduced NCVs and chronic axonal degeneration and regeneration." []
192	UPK:0145	"Protein involved in the movement of a cell, or organism, along a concentration gradient of a chemotactic agent, such as a protein which causes, mediates or responds to chemotaxis. Chemotactic molecules such as sugars, peptides, cell metabolites, cell-wall or membrane lipids bind to cell surface receptors and trigger activation of intracellular signaling pathways, as well as remodeling of the cytoskeleton through the activation or inhibition of various actin-binding proteins." []
193	UPK:0146	"Protein involved in the breakdown of chitin, a linear polysaccharide consisting of (1->4)-beta-linked D-glucosamine residues, most of which are N-acetylated." []
194	UPK:0147	"Protein which binds chitin, a linear polysaccharide consisting of (1->4)-beta-linked D-glucosamine residues, most of which are N-acetylated. The 30-43 amino acids long chitin-binding domain contains several conserved glycine and cysteines residues. The conserved cysteines form disulfide bonds. Chitin-binding domains have been found in plant, fungal and bacterial proteins." []
195	UPK:0868	"Protein which binds at least one chloride, or protein whose function is chloride-dependent. Chloride is a negatively-charged ion, which is abbreviated Cl(-)." []
196	UPK:0869	"Protein which is part of an anion channel found in the plasma lemma and in intracellular membranes. These channels are permeable for various anions, such as iodide, bromide, but also for nitrates, phosphates and even negatively charged amino acids. They are called chloride channels, because chloride is the most abundant anion and the predominant permeating species in all organisms. They have been classified according to their gating mechanisms, which may depend on changes in the transmembrane electric field (voltage-dependent/gated chloride channels, e.g. ClC family), on a protein kinase/nucleotide mediated mechanism (CFTR), an increase in intracellular calcium (calcium activated chloride channels, e.g. CaCC), cell swelling (volume-regulated anion channels, e.g. VRAC) or binding of a ligand, e.g. glycine or - aminobutyric acid (GABA) activated channels. In contrast with cation channels, they are not involved in the initiation or spread of excitation, but in the regulation of excitability in nerve and muscle. They also participate in many housekeeping processes, such as volume regulation, pH regulation in organelles, electrogenesis and control of synaptic activity. The chloride channels are crucial for transepithelial transport and the control of water flow, and often provide unexpected permeation pathways for a large variety of anions." []
197	UPK:1265	"Protein which interferes with the function of chloride channels which are membrane proteins forming a channel in a biological membrane selectively permeable to chloride ions. Chloride channels include voltage-gated chloride channels (ClC), ionotropic GABA receptors (ligand-gated ion channels activated by GABA) and CFTR ion channels (ABC transporter-class ion channels). Toxins that target these channels are found in venom of several species including scorpions and snakes." []
198	UPK:0148	"Protein which interacts with chlorophyll, the major light-absorbing pigment in most oygenic green organisms. Higher plants contain chlorophyll a and chlorophyll b which are magnesium-porphyrin complexes esterified to a long hydrophobic terpenoid side chain (the alcohol phytol)." []
199	UPK:0149	"Protein involved in the synthesis of chlorophylls. These photosynthetic pigments are magnesium-porphyrin complexes with a long hydrophobic terpenoid side chain (the alcohol phytol). Angiosperms have only a light-dependent pathway for chlorophyll biosynthesis, other oxygenic organisms seem to have both the light-dependent and the light-independent pathways. Non-oxygenic organisms, which make bacteriochlorophyll, only have a light-independent pathway." []
200	UPK:0881	"Protein involved in the degradation of chlorophylls. These photosynthetic pigments are magnesium-porphyrin complexes with a long hydrophobic terpenoid side chain (the alcohol phytol)." []
201	UPK:0150	"Protein encoded by or localized in the chloroplast, the most common form of plastid, found in all photosynthetic organisms except glaucophyte algae. In green (photosynthesizing) tissue they house the machinery necessary for photosynthesis and CO(2) fixation. They are surrounded by between 2 and 4 membranes and contain thylakoids in green tissue." []
202	UPK:0151	"Photosynthetic light-harvesting complexes found in green bacteria. Chlorosomes are sac-like organelles appressed to the cytoplasmic membrane of the cell membrane." []
203	UPK:0152	"Protein involved in the synthesis of cholesterol, the major sterol of higher animals. It is a component of cell membranes, especially of the plasma membrane." []
204	UPK:0153	"Protein which participates in the biochemical reactions where cholesterol is involved, including transport. Cholesterol is the major sterol of higher animals and an important component of cell membranes, especially of the plasma membrane." []
205	UPK:0891	"Protein involved in chondrogenesis, the mechanism of cartilage formation. Chondrogenesis proceeds through determination of cells and their aggregation into prechondrogenic condensations, differentiation into chondrocytes, and later maturation. The formation of the long bones requires a cartilage template." []
206	UPK:0155	"Protein that enables bacteria and other microorganisms to withstand chromate, a salt of chromic acid (H2CrO4)." []
207	UPK:0156	"Protein controlling the opening or closing of chromatin." []
208	UPK:0157	"Protein which interacts with one or more chromophores. A chromophore absorbs and transmits light energy. Originally it was used for visibly colored molecules, but it applies also to UV- and IR-absorbing molecules." []
209	UPK:0957	"Protein found in or associated with a chromoplast, a plastid containing pigments other than chlorophyll. Found in flower, petals and fruit." []
210	UPK:0160	"Protein which can be altered by a structural chromosomal rearrangement. Structural rearrangements result from chromosome breakage, followed by reconstitution in an abnormal combination. Classes of chromosomal rearrangements include: deletions, duplications, insertions, inversions, translocations and transpositions." []
211	UPK:0158	"Protein which is associated with chromosomal DNA, including histones, protamines and high mobility group proteins." []
212	UPK:0159	"Protein involved in chromosome partition, the process by which newly replicated plasmids and chromosomes are actively segregated prior to cell division. E.g., par and soj which contribute to efficient chromosome partitioning by serving functions analogous to centromeres (i.e. pairing or positioning of sister chromosomes)." []
213	UPK:0161	"Protein which, if defective, causes chronic granulomatous disease (CGD), a disease characterized by the failure of activated phagocytes to generate superoxide." []
214	UPK:0162	"Protein component of the chylomicrons or involved in their catabolism. Chylomicrons are the largest lipoprotein complexes with the lowest protein-to-lipid ratio. They are present in the blood or lymph and transport exogenous (dietary) cholesterol, triacylglycerols and other lipids from the intestine to the liver or to the adipose tissue." []
215	UPK:1186	"Protein which, if defective, causes any one of a group of diseases associated with either abnormal formation or function of cilia. Ciliopathies cover a large spectrum of often overlapping phenotypes ranging from relatively mild, tissue-restricted pathologies to severe defects in multiple organs. Although cilia play important roles in many tissues, the predominantly affected organs are kidney, eye, liver and brain. Clinical features typically include retinal degeneration, renal disease and cerebral anomalies. Additional manifestations include congenital fibrocystic diseases of the liver, diabetes, obesity and skeletal dysplasias. Ciliary dysfunction in the embryo may cause randomization of left-right body asymmetry or situs inversus, as well as severe malformations leading to embryonic lethality." []
216	UPK:0969	"Protein found in or associated with a cilium, a cell surface projection found at the surface of a large proportion of eukaryotic cells. The two basic types of cilia, motile (alternatively named flagella) and non-motile, collectively perform a wide variety of functions broadly encompassing cell/fluid movement and sensory perception. Their most prominent structural component is the axoneme which consists of nine doublet microtubules, with all motile cilia - except those at the embryonic node - containing an additional central pair of microtubules. The axonemal microtubules of all cilia nucleate and extend from a basal body, a centriolar structure most often composed of a radial array of nine triplet microtubules. In most cells, basal bodies associate with cell membranes and cilia are assembled as 'extracellular' membrane-enclosed compartments." []
217	UPK:0970	"Protein which is involved in the formation, organization, maintenance and degradation of the cilium, a cell surface projection found at the surface of a large proportion of eukaryotic. Their most prominent structural component is the axoneme which consists of nine doublet microtubules, with all motile cilia - except those at the embryonic node - containing an additional central pair of microtubules." []
218	UPK:0163	"Protein which allows the utilization of the 6-carbon tricarboxylic acid citrate as a sole source of carbon and energy." []
219	UPK:0164	"Protein which is posttranslationally modified by the deimination of one or more arginine residues." []
220	UPK:1167	"Viral protein involved in virus internalization into the host cell via endocytic pathways that involve neither clathrin nor caveolins. These pathways can be further defined by their dependency on various molecules such as cholesterol, DNM2/Dynamin-2, small GTPases or tyrosine kinase and possibly involve non-caveolar lipid rafts. Clathrin- and caveolin-independent pathways are used by viruses including poliovirus, human rhinovirus 14, lymphocytic choriomeningitis virus, murine norovirus-1 and SV40." []
221	UPK:1165	"Viral protein involved in virus internalization by the host cell via clathrin-mediated endocytosis. In response to an internalization signal, clathrin is assembled on the inside face of the cell membrane to form characteristic invaginations or clathrin coated pits that pinch off through the action of DNM1/Dynamin-1 or DNM2/Dynamin-2. The virus bound to its host cell receptor is internalized into clathrin-coated vesicles (CCV). Endocytic CCV deliver their viral content to early endosomes. The endosomal acidic pH and/or receptor binding usually induces structural modifications of the virus surface proteins that lead to penetration of the endosomal membrane via fusion or permeabilization mechanisms." []
222	UPK:0165	"Protein which is posttranslationally modified by the cleavage on at least one pair of basic residues, in order to release one or more mature active peptides (such as hormones)." []
223	UPK:0168	"Protein which is a component of a coated pit. Coated pits are regions of the donor membrane where the assembly of the vesicle coat take place. The coat assembles from soluble protomers such as coat protein complex-I and coat protein complex-II. The components of the coat often define the intracellular sorting station, and contribute to both membrane deformation and local movement of the resulting transport intermediate following scission. During the first steps of the vesicle-mediated membrane transport, coated pits are internalized to form coated vesicles which transport proteins between distinct membrane-bound organelles." []
224	UPK:0846	"Protein which contains at least one cobalamin as cofactor, e.g. methylmalonyl-CoA mutase, or which binds and/or transports cobalamin, such as intrinsic factor or transcobalamins. Cobalamin, which is synthesized by microorganisms, has equatorial sites occupied by a tetrapyrrol ring structure (corrin ring) with a cobalt(III) ion in the center, one axial site occupied by an intramolecularly-bound dimethylbenzimidazole and the other axial site occupied by a number of different ligands such as water (aquacobalamin), cyanide (cyanocobalamin=vitamin B12), glutathione (glutathionylcobalamin), 5'deoxyadenosine (adenosylcobalamin=coenzyme B12) or a methyl group (methylcobalamin). It is a prosthetic group of certain mammalian enzymes, where it is essential for the normal maturation and development of erythrocytes. A deficiency in the diet or more frequently the failure to absorb the vitamin give rise to pernicious anemia." []
390	UPK:0293	"Protein involved in fruiting body formation or expressed in fruiting bodies, any specialized reproductive structure that produces spores or gametes in fungi, slime molds, algae, etc. Fruiting bodies are distinct in size, shape and coloration for each species." []
225	UPK:0169	"Protein involved in the synthesis of cobalamin. Cobalamin, which is synthesized by microorganisms, has equatorial sites occupied by a modified porphyrin ring system, with two of the four pyrrol rings fused directly (without an intervening methine bridge). The modified porphyrin system binds a cobalt(III) ion in the center, and this is called a corrin ring system. One axial site is occupied usually by an intramolecularly-bound dimethylbenzimidazole nucleotide and the other axial site is occupied by a number of different ligands such as water (aquacobalamin), cyanide (cyanocobalamine=vitamin B12), glutathione (glutathionylcobalamine), 5'deoxyadenosine (adenosylcobalamine=coenzyme B12) or a methyl group (methylcobalamin). Vitamin B12, for instance, is a prosthetic group of certain mammalian enzymes, where it is essential for the normal maturation and development of erythrocytes. A deficiency in the diet or more frequently the failure to absorb the vitamin B12 give rise to pernicious anemia." []
226	UPK:0170	"Protein which binds at least one cobalt atom, or protein whose function is cobalt-dependent. Cobalt is a metallic element, chemical symbol Co." []
227	UPK:0171	"Protein involved in the transport of the trace element cobalt, which is a component of vitamin B12." []
228	UPK:0172	"Protein which, if defective, causes Cockayne's syndrome (CS), an autosomal recessive disease characterized by UV-sensitive skin (without pigmentation abnormalities), neurological dysfunction due to demyelination of neurons and calcification of basal ganglia (psychomotor retardation, deafness, optic atrophy, retinal pigmentation and hyperreflexes) and dysmorphic dwarfism (immature sexual development and microcephaly)." []
229	UPK:9997	"Keywords assigned to proteins because their sequences can differ, due to differences in the coding sequences such as polymorphisms, RNA-editing, alternative splicing." []
230	UPK:0173	"Protein involved in the biosynthetic pathway leading from pantothenate to coenzyme A (CoA). CoA has two halves in phosphodiester linkage: a 3',5'-ADP residue, and 4-phosphopantetheine. The phosphopantetheine moiety is itself composed of three structural entities: a branched chain dihydroxy acid in amide linkage to a beta-alanyl residue, which is in turn linked to a cysteamide containing the reactive thiol. Coenzyme A functions as a carrier of acetyl and acyl groups and is essential for numerous biosynthetic, energy-yielding, and degradative metabolic pathways. Acetyl-CoA is the common cellular currency for acetyl transfers." []
231	UPK:0174	"Protein involved in the biosynthesis of coenzyme M. Coenzyme M (2-mercaptoethanesulfonic acid) is the smallest known organic cofactor. CoM serves as a methyl group carrier in key reactions within the pathway of methane formation from C1 precursors. In the alkene metabolism pathway, it is involved in aliphatic epoxyde carboxylation." []
232	UPK:0175	"Protein which contains at least one coiled coil domain, a type of secondary structure composed of two or more alpha helices which entwine to form a cable structure. In proteins, the helical cables serve a mechanical role in forming stiff bundles of fibres." []
233	UPK:0176	"Protein which contains one or more collagen-like domain. Collagen is a fibrous protein found in vertebrates, the major element of skin, bone, tendon, cartilage, blood vessels and teeth. It forms insoluble fibres of high tensile strength and which contains the unusual amino acids hyroxyproline and hydroxylysine. It is rich in glycine but lacks cysteine and tryptophan, and has an unusually regular amino-acid domain." []
234	UPK:0177	"Protein involved in the degradation of collagen, a family of fibrous proteins found in skin, bones, teeth, cartilage and other tissues of vertebrates." []
235	UPK:0178	"Protein involved in competence, the state in which a cell or organism is able to take up DNA and become genetically transformed." []
236	UPK:1018	"Protein involved in the complement activation lectin pathway which activates the proteins of the complement system. This pathway can be activated mainly by mannose-binding lectin (MBL) interacting with carbohydrate structures on microbial surfaces and by ficolins with different fine carbohydrate binding specificity." []
237	UPK:0179	"Protein involved in the complement alternate pathway which activates the proteins of the complement system. This pathway can be activated by IgA immune complexes, but also by bacterial endotoxins, polysaccharides and cell walls, without participation of an antigen-antibody reaction." []
238	UPK:0180	"Pathway which activates the proteins of the complement system, a group of blood proteins of the globulin class involved in the lysis of foreign cells after they have been coated with antibody, and which also promote the removal of antibody-coated foreign particles by phagocytic cells. The pathway proceeds by a cascade reaction of successive binding and proteolytic cleavage of complement components. This pathway can be activated by either IgG or IgM binding to an antigen." []
239	UPK:1216	"Toxin which interferes with the complement system. These toxins act by activating, inhibiting, or mimicking proteins of this system. They are mostly found in snake and spider venoms." []
240	UPK:0181	"Protein which is part of a proteome. A proteome is the set of protein sequences that can be derived by translation of all protein coding genes of a completely sequenced genome, including alternative products such as splice variants for those species in which these may occur. Proteomes may include protein sequences from both the reviewed (UniProtKB /Swiss-Prot) and unreviewed (UniProtKB/TrEMBL) sections of the UniProt Knowledgebase. Note that some proportion of the predicted protein sequences of a given proteome may require further review or correction. The precise proportion depends on the relative distributions of protein sequences between the two sections of UniProtKB and the quality of the underlying genome sequence and gene predictions." []
241	UPK:0182	"Protein which, if defective, causes cone-rod dystrophy, a disease where dystrophy of cone-rod cells is characterized by the initial degeneration of cone photoreceptor cells, thus causing early loss of visual acuity and color vision, followed by the degeneration of rod photoreceptor cells and leading to progressive night blindness and peripheral visual field loss." []
242	UPK:0954	"Protein which, if defective, causes congenital adrenal hyperplasia, a group of inherited disorders of cortisol biosynthesis. Defective cortisol biosynthesis results in compensatory hypersecretion of corticotropin with subsequent adrenal hyperplasia and excessive androgen production. Various clinical types are recognized: "salt wasting form" is the most severe type, "simple virilizing form" with normal aldosterone biosynthesis, "non-classic form" or late onset, and "cryptic form" or asymptomatic." []
281	UPK:0206	"Protein which is a component or which is associated with the cytoskeleton, a dynamic three-dimensional structure that fills the cytoplasm of eukaryotic cells. The cytoskeleton is both a muscle and a skeleton, and is responsible for cell movement, cytokinesis, and the organization of the organelles within the cell. The major components of cytoskeleton are the microfilaments (of actin), microtubules (of tubulin) and intermediate filament systems in cells." []
243	UPK:0900	"Protein which, if defective, causes a congenital disorder of glycosylation. In the endoplasmic reticulum (ER) of eukaryotes, N-linked glycans are first assembled on the lipid carrier dolichyl pyrophosphate. The GlcNAc(2)Man(9)Glc(3) oligosaccharide is transferred to selected asparagine residues of nascent polypeptides. Defects along the biosynthetic pathway of N-glycans are associated with severe multisystemic syndromes called congenital disorders of glycosylation (CDG). The characteristic biochemical feature of CDG is defective glycosylation of glycoproteins due to mutations in genes required for the biosynthesis of N-linked oligosaccharides. Defects of the assembly of dolichyl-linked oligosaccharides or their transfer on to nascent glycoproteins form type I forms of CDG, whereas CDG type II comprises all defects of the trimming and elongation of N-linked oligosaccharides." []
244	UPK:1055	"Protein which, if defective, causes congenital dyserythropoietic anemia, a heterogeneous group of disorders characterized by the occurrence of multinuclear erythroid precursors in the bone marrow, ineffective erythropoiesis, iron overload and anemia. Various forms are differentiated mainly by the morphological appearance of the erythroid precursors." []
245	UPK:0985	"Protein which, if defective, causes congenital absolute erythrocytosis, a disorder characterized by expansion of the erythrocyte compartment in the peripheral blood. Total red cell mass is increased in the absence of a reduction of plasma volume. Erythrocytoses are usually divided into primary and secondary forms. Primary erythrocytoses are due to defects in the erythroid progenitors and are characterized by low erythropoietin levels. Secondary erythrocytoses can be due to defects in hypoxia sensing, or to conditions that cause low tissue oxygen tension with consequent increase in erythropoietin secretion." []
246	UPK:1022	"Protein which, if defective, causes congenital generalized lipodystrophy, a disorder characterized by near complete absence of adipose tissue from birth. Affected patients manifest insulin resistance, early onset diabetes mellitus, hypertriglyceridemia, hepatic steatosis and acanthosis nigricans." []
247	UPK:0984	"Protein which, if defective, causes congenital hypothyroidism, a condition due to thyroid hormones deficiency, presenting at birth. Congenital hypothyroidism occurs when the thyroid gland fails to develop or function properly. In most cases, the thyroid gland is absent, abnormally located, or severely reduced in size. In the remaining cases, a normal-sized or enlarged thyroid gland is present, but production of thyroid hormones is decreased or absent. If untreated, congenital hypothyroidism can lead to mental retardation and growth failure." []
248	UPK:0912	"The congenital muscular dystrophies (CMD) are a heterogeneous group of disorders characterized by hypotonia, muscle weakness, dystrophic changes on skeletal muscle biopsy, and joint contractures that present at birth or during the first 6 months of life. Mental retardation with or without structural brain changes are defects, with or without mental retardation, are additional features of several CMD syndromes." []
249	UPK:1004	"Protein which, if defective, causes congenital myasthenic syndrome. Congenital myasthenic syndromes constitute a group of inherited diseases characterized by a congenital defect in neuromuscular transmission at the neuromuscular junction, including pre-synaptic, synaptic, and post-synaptic disorders that are not of autoimmune origin. Congenital myasthenic syndromes are characterized by muscle weakness affecting the axial and limb muscles (with hypotonia in early-onset forms), the ocular muscles (leading to ptosis and ophthalmoplegia), and the facial and bulbar musculature (affecting sucking and swallowing, and leading to dysphonia). The symptoms fluctuate and worsen with physical effort." []
250	UPK:1014	"Protein which, if defective, causes congenital stationary night blindness that is the failure or imperfection of vision at night or in dim light, with good vision only on bright days." []
251	UPK:0183	"Protein involved in conidiation, the production of conidia which are asexual fungal spores." []
252	UPK:0184	"Protein involved in the temporary fusion of two gametes or two cells leading to the transfer of genetic material. This process is seen in bacteria, ciliate protozoa and certain fungi." []
253	UPK:0186	"Protein which binds at least one copper atom, or protein whose function is copper-dependent. Copper is a trace metallic element, chemical symbol Cu." []
254	UPK:0187	"Protein involved in the transport of ions of the trace element copper." []
255	UPK:0188	"Protein involded in the formation of the copulatory plug, a plug composed of a number of proteins which are secreted by the seminal vesicle under the influence of testosterone. Found in rodents." []
256	UPK:1212	"Protein which, if defective, causes corneal dystrophy. The term corneal dystrophy includes a heterogeneous group of bilateral, primary alterations of the cornea that are not associated with prior inflammation or secondary to systemic disease. Most corneal dystrophies present with variable shaped corneal opacities in a clear or cloudy cornea and they affect visual acuity to different degrees. Corneal dystrophies may be present at birth but more frequently develop during adolescence and progress slowly throughout life." []
257	UPK:0190	"Protein covalently attached to a DNA molecule. For example some viruses contains proteins that are attached to the end of a viral replicating DNA and which are necessary for DNA replication." []
258	UPK:0191	"Protein covalently attached to a RNA molecule. For example some viruses contains proteins that are attached to the end of a viral replicating RNA and which are necessary for RNA replication." []
259	UPK:0989	"Protein which, if defective, causes craniosynostosis, the premature closure of one or more cranial sutures which results in an abnormal head shape. Different types of craniosynostosis are known. All are characterized by skull deformities, with face and often limb involvement in the syndromic forms." []
260	UPK:1257	"Viral protein that inhibits host defense CRISPR-cas system (Clustered Regularly Interspaced Short Palindromic Repeats). The CRISPR-cas system is composed of genomic sensors that allow prokaryotes to acquire DNA fragments from invading viruses and plasmids into the CRISPR locus. These stored fragments (called spacers) are transcribed and processed into small crRNA which are used to destroy matching DNA in future viral and plasmid invasion. Some prokaryotic viruses express specific genes that allow them to evade CRISPR-cas system." []
261	UPK:0192	"Protein involved in crown gall tumor formation, a plant tumor caused by the bacterium Agrobacterium tumefaciens." []
262	UPK:0885	"Protein which contains at least one cysteine tryptophylquinone (CTQ) cross-link modification. CTQ is formed by oxidation of the indole ring of a tryptophan to form tryptophylquinone followed by covalent cross-linking with a cysteine residue. In the quinohemoprotein amine dehydrogenase, CTQ mediates during the catalytic cycle electron transfer from the substrate to either a copper protein, azurin, or cytochrome c-550." []
263	UPK:1062	"Protein which, if defective, causes Cushing syndrome, a condition caused by prolonged exposure to excess levels of cortisol from endogenous or exogenous sources. Endogenous Cushing syndrome is due to excess production of cortisol by the adrenal glands. It may be caused by pituary hypersecretion of adrenocorticotropic hormone (ACTH), ectopic ACTH secretion by non-pituary tumors, or may result from cortisol hypersecretion by adrenal gland tumors (ACTH-independent Cushing syndrome). Cushing syndrome is clinically characterized by upper body obesity, osteoporosis, hypertension, diabetes mellitus, hirsutism, amenorrhea, and excess body fluid." []
264	UPK:0193	"Protein which is a component of the cuticle, the outer protective layer produced by epidermal cells that covers the body of many invertebrates." []
265	UPK:0194	"Protein encoded by the cyanelle genome or protein located in the cyanelle. Cyanelles are the plastids of glaucocystophyte algae. They are surrounded by a double membrane and, in between, a peptidoglycan wall. The cyanelle genome is of chloroplast size and contains genes for tRNAs, rRNAs and approx. 150 proteins, which is more than found in higher plant chloroplast genomes (this feature is also shared by other primitive plastids). Thylakoid membrane architecture and the presence of carboxysomes are cyanobacteria-like. Historically, the term cyanelle is derived from a classification as endosymbiotic cyanobacteria, and thus is not fully correct." []
266	UPK:0195	"Protein that belongs to the cyclin family or that contains a cyclin box-like domain. Cyclins are regulatory subunits of the cyclin-dependent protein kinases. They form kinase holoenzymes, with distinct biochemical characteristics and nonredundant biological functions, which mediate phosphorylation of cellular proteins, including key cell cycle regulatory molecules. In this way, the kinase holoenzymes promote the transit of cells through the division cycle. Cyclins accumulate during interphase of eukaryotic cell cycle and are destroyed at the end of mitosis." []
267	UPK:0196	"Protein that confers, on an organism, the ability to withstand cycloheximide, an antibiotic produced by Streptomyces griseus, which inhibits eukaryotic elongation during protein synthesis. The resistance is often due to mutations that prevent antibiotic binding to the protein." []
268	UPK:0197	"Protein binding cyclosporin or protein whose function is inhibited by cyclosporin, e.g. cyclophilins. Cyclosporins are peptides obtained from certain hyphomycetes which have potent immuno-suppressant activity on humoral and cellular systems. Cyclosporin is used in transplant surgery to suppress the immune response." []
269	UPK:0198	"Protein involved in the synthesis of cysteine, the amino acid with the highly reactive sulfhydryl group (-SH). It is derived from the amino acids methionine and serine. Cysteine plays a special role in shaping some proteins by forming disulfide bonds. In enzymes the unique reactivity of this group is frequently exploited at the catalytic site." []
270	UPK:0199	"Protein which, if defective, causes cystinuria (CSNU), an autosomal recessive condition of persistent excessive urinary excretion of cystine and three other dibasic amino acids: lysine, ornithine, and arginine. CSNU arises from impaired reabsorption of these amino acids through the epithelial cells of the renal tubule and gastrointestinal tract. It is characterized by cystine stones in the kidney, ureter and bladder. Three clinical types of cystinuria have been described: cystinuria type-I (CSNU1), type-II (CSNU2) and type-III (CSNU3)." []
271	UPK:0200	"Protein involved in cytadherence, the attachment of mycoplasma to the epithelium." []
272	UPK:0201	"Protein involved in the biogenesis of c-type cytochromes. Cytochromes c are electron-transfer proteins having one or several heme c groups, bound to the protein by one or, more commonly two, thioether bonds involving sulphydryl groups of cysteine residues." []
273	UPK:0202	"Small secreted proteins from higher eukaryotes which affect the growth, division and functions of other cells, e.g. interleukins, lymphokines, TNF and interferons. Generally, growth factors are not classified as cytokines, though TGF is an exception. Chemokines are a subset of cytokines. They differ from classical hormones in that they are produced by a number of tissues or cell types rather than by specialized glands. They generally act locally in a paracrine or autocrine rather than endocrine manner." []
274	UPK:0203	"Protein involved in the synthesis of cytokinins, a class of plant hormones which promote cell division (e.g. kinetin, zeatin, benzyl adenine). They are also involved in cell growth, cell differentiation and in other physiological processes." []
275	UPK:0932	"Protein involved in the cytokinin signaling pathway (i.e. transport or signal transduction). Cytokinins (i.e. kinetin and zeatin) are defined more by their biological activity (e.g. inducing cell division in tissue culture) rather than by structure. These phytohormones are synthesized in the root apical meristem and transported through the plant in the xylem sap. Cytokinins are involved in several physiological processes such as promoting cell division and chloroplast maturation, regulating cell growth and differentiation, and monitoring nutrient uptake and senescence. Together with auxin, they also regulate the cell cycle and tissue morphogenesis." []
276	UPK:0204	"Protein involved in the rupture of cell membranes and loss of cytoplasm, e.g. exotoxin, cytolysin." []
277	UPK:0963	"Protein found in the cytoplasm, the content of a cell within the plasma membrane and, in eukaryotics cells, surrounding the nucleus. This three-dimensional, jelly-like lattice interconnects and supports the other solid structures. The cytosol (the soluble portion of the cytoplasm outside the organelles) is mostly composed of water and many low molecular weight compounds. In eukaryotes, the cytoplasm also contains a network of cytoplasmic filaments (cytoskeleton)." []
278	UPK:1176	"Viral protein that allows the active transport of viral components along cytoskeletal filaments toward the intracellular replication sites during virus entry. Viruses such as adenoviruses, adeno-associated virus, vaccinia virus, poliovirus, canine parvovirus, African swine fever virus, rabies virus, human herpes virus 1, foamy virus are thought to use active intracellular transport of viral components." []
279	UPK:0968	"Protein found in or associated with cytoplasmic vesicles, which mediate vesicular transport among the organelles of secretory and endocytic systems. These transport vesicles are classified by the identity of the protein coat used in their formation and also by the cargo they contain, e.g. clathrin-, COPI-, and COPII-coated vesicles, synaptic vesicles, secretory vesicles, phagosomes, etc." []
280	UPK:0205	"Protein involved in the biochemical reactions with the pyrimidine base cytosine." []
282	UPK:0208	"Protein which contains at least one D-amino acid. All of the amino acids derived from natural proteins are of the L configuration. D-amino acids are found in nature, especially as components of certain peptide antibiotics and in walls of certain microorganisms." []
283	UPK:0209	"Protein which, if defective, causes a partial or total inability to hear. The two principal types of deafness are conductive deafness that results from changes in the middle ear, and nerve or sensorineural deafness that is caused by damages to the inner ear, the nerve pathways to the brain, or the area of the brain that receives sound information." []
284	UPK:0210	"Enzyme that belongs to the lyase family and which catalyzes the spliting of CO(2) from the carboxylic group of amino acids, beta-keto acids and alpha-keto acids." []
285	UPK:1132	"Viral protein involved in the degradation of host mRNAs. Viruses have evolved ways of degrading host mRNAs to inhibit cellular translation. This global inhibition of cellular protein synthesis serves to ensure maximal viral gene expression and to evade host immune response. Decay of host mRNAs can be achieved by endonucleotic RNA cleavage or associated with PABPC1 nuclear relocalization." []
286	UPK:0211	"Families of microbicidal and cytotoxic peptides. Defensins have antibacterial, antifungal and antiviral properties. Defensins kills cells by forming voltage-regulated multimeric channels in the susceptible cell's membrane." []
287	UPK:1238	"Virion protein involved in breaking down host cell capsule to reach the host cell wall, and finally the host cytoplasmic membrane. Many prokaryotic viruses carry for example glycanase, polysaccharide lyase or deacetylase activities to specifically digest host capsule." []
288	UPK:1235	"Virion protein involved in breaking down host cell surface components to reach the host cytoplasmic membrane. Many prokaryotic viruses for example carry enzymatic activities to degrade the host cell lipopolysaccharide layer, cell wall, or capsule." []
289	UPK:1247	"Viral protein that rapidly degrades the host DNA at the onset of infection. The breakdown products can be reused to synthesize viral DNA or can be excreted from the host cell. Degrading host chromosome provides an advantage during the virus life cycle by reducing or eliminating competing host macromolecular synthesis. Bacteriophages such as T4 or T5 for example are known to induce degradation of the host chromosome and excretion of the host DNA degradation products." []
290	UPK:1237	"Virion protein involved in breaking down host cell lipopolysaccharides (LPS) to reach the cytoplasmic membrane of prokaryotes with 2 membranes. Many prokaryotic viruses carry glycanase or deacetylase activities to digest host LPS." []
291	UPK:1236	"Virion exolysin involved in breaking down host cell peptidoglycans (e.g. murein, pseudomurein) to reach the host cytoplasmic membrane during virus entry. Exolysins are usually part of the tail or the base plate of prokaryotic viruses. Exolysins can display various enzymatic activities such as lysozyme, transglycosylase, muramidase or even protease activity. Murein hydrolases for example are widespread in bacteriophages infecting Gram-positive or Gram-negative bacteria." []
292	UPK:0213	"Protein which, if defective, causes Dejerine-Sottas disease. DSS is a hereditary motor and sensory neuropathy (HMSN) of the Charcot-Marie-Tooth disease type 1 class. DSS is characterized by severe early onset, very slow nerve conduction velocities (less than 12m/sec) and raised cerebrospinal fluid protein concentrations (0.7 g/l). Clinical signs are delayed age of walking as well as areflexia." []
293	UPK:0214	"Protein involved in dental caries or important in the prevention of dental caries. Dental caries are localized destruction of the tooth surface, initiated by decalcification of the enamel and followed by enzymatic lysis of organic structures, the result of which is cavity formation. The cavity may penetrate the enamel and dentin, and reach the pulp. The disease may be caused by acids produced by bacteria which lead to decalcification, or by microorganisms that destroy the enamel protein, or by keratolytic microorganisms producing chelates that lead to decalcification." []
294	UPK:0215	"Protein involved in the synthesis of deoxyribonucleotides, the basic repeating units in DNA. Deoxyribonucleotides consist of a purine or a pyrimidine base bonded to deoxyribose, which in turn is bound to a phosphate group. They are synthesised by reduction of ribonucleoside diphosphates." []
295	UPK:1061	"Protein involved in the necrosis of the skin." []
296	UPK:0911	"Protein which, if defective, causes desmin-related myopathy (DRM), a clinically and genetically heterogeneous group of muscular disorders defined morphologically by intrasarcoplasmic aggregates of desmin, usually accompanied by other protein aggregates. Both autosomal dominant and autosomal recessive inheritance have been reported. Approximately one-third of DRMs are thought to be caused by mutations in the desmin gene." []
297	UPK:0216	"Protein involved in degrading toxic compounds. Detoxification generally takes place in the liver or kidney and inactivates toxins, either by degradation or by conjugation of residues to a hydrophilic moiety in order to promote excretion." []
298	UPK:0217	"Protein involved in development, the process whereby a multicellular organism develops from its early immature forms, e.g., zygote, larva, embryo, into an adult." []
299	UPK:9996	"Keywords assigned to proteins because they are expressed specifically in a given developmental stage." []
300	UPK:0218	"Protein which, if defective, causes diabetes insipidus, a rare form of diabetes in which the kidney tubules do not reabsorb enough water resulting in excessive urine excretion (polyuria). Two types of diabetes insipidus are recognized: central or neurohypophyseal diabetes insipidus which is due to defects in the neurohypophyseal system and results in a deficient quantity of anti-diuretic hormone being produced or released; nephrogenic diabetes insipidus, a vasopressin unresponsive condition of polyuria and hyposthenuria." []
301	UPK:0219	"Protein which, if defective, causes diabetes mellitus, a disorder of impaired carbohydrate, protein, and fat metabolism due to insufficient secretion of insulin or to target tissue insulin resistance. Diabetes mellitus can be divided into two main types, type I or insulin-dependent diabetes mellitus (IDDM), and type II, or non insulin-dependent diabetes mellitus (NIDDM). Type I diabetes mellitus normally starts in childhood or adolescence and is caused by the body's own immune system which destroys the insulin-producing beta cells in the pancreas. Classical features are polydipsia, polyphagia and polyuria, due to hyperglycemia-induced osmotic diuresis. Type II diabetes mellitus normally starts in adulthood and is caused by a lack of sensitivity to the body's own insulin. It is usually characterized by a gradual onset with minimal or no symptoms of metabolic disturbance. Both forms of diabetes mellitus lead to secondary complications (notably cardiovascular, nephropathy, retinopathy, neuropathy). Two other major subcategories of diabetes mellitus are gestational diabetes and diabetes secondary to other medical conditions. In common usage, the term diabetes, when used alone, refers to diabetes mellitus and not diabetes insipidus." []
302	UPK:0220	"Protein involved in the synthesis of diaminopimelate, the ionic form of the amino acid diaminopimelic acid (DAP) which is found in the murein peptidoglycans of bacterial cell walls. Diaminopimelic acid is synthesised from aspartate." []
303	UPK:1024	"Protein which, if defective, causes Diamond-Blackfan anemia, a rare congenital non-regenerative hypoplastic anemia that usually presents early in infancy. The disease is characterized by a moderate to severe macrocytic anemia, erythroblastopenia, and an increased risk of developing leukemia. 30 to 40% of Diamond-Blackfan anemia patients present with short stature and congenital anomalies, the most frequent being craniofacial (Pierre-Robin syndrome and cleft palate), thumb and urogenital anomalies." []
304	UPK:0221	"Protein involved in differentiation, the developmental process of a multicellular organism by which cells become specialized for particular functions. Differentiation requires selective expression of the genome; the fully differentiated state may be preceded by a stage in which the cell is already programmed for differentiation but is not yet expressing the characteristic phenotype determination. Also used for fungal conidiation proteins, and for some bacteria that present specialization of function in cell types, such as Caulobacter crescentus." []
305	UPK:0222	"Protein involved in the process whereby nutrients are rendered soluble and capable of being absorbed by the organism or cell, by action of various hydrolytic enzymes that break down proteins, carbohydrates, fats, etc." []
306	UPK:0223	"Enzyme that reduces molecular oxygen by incorporating both atoms into its substrate(s)." []
307	UPK:0224	"Enzyme that hydrolyzes a dipeptide into its constituent amino acids." []
308	UPK:0903	"Protein, whose amino acid sequence has been partially (more than one residue) or completely determined experimentally by Edman degradation or by mass spectrometry." []
309	UPK:9995	"Keywords assigned to proteins because they are involved in a specific disease." []
310	UPK:0225	"Protein for which at least one variant, responsible for a disease, is described in the feature table of its Swiss-Prot entry." []
311	UPK:1015	"Protein which is modified by the formation of a bond between the thiol groups of two peptidyl-cysteine residues. The process of chemical oxidation that forms interchain disulfide bonds can produce stable, covalently linked protein dimers, multimers or complexes, whereas intrachain disulfide bonds can contribute to protein folding and stability. Depending on the protein environment, some disulfide bonds are more labile, forming transient redox-active disulfide bonds that are alternately reduced and oxidized in the course of an enzymatic reaction." []
312	UPK:0226	"Protein involved in DNA condensation. In most eukaryotes, the chromosomal packing involves the wrapping of DNA around a core of histones to form nucleosomes. Adjacent nucleosomes are packaged together via Histone 1 and nucleosomes are organised into a 30 nm chromatin fibre. DNA condensation takes place as cells enter mitosis or when germ cells enter meiosis." []
313	UPK:0227	"Protein induced by DNA damage or protein involved in the response to DNA damage. Drug- or radiation-induced injuries in DNA introduce deviations from its normal double-helical conformation. These changes include structural distortions which interfere with replication and transcription, as well as point mutations which disrupt base pairs and exert damaging effects on future generations through changes in DNA sequence. Response to DNA damage results in either repair or tolerance." []
314	UPK:1256	"Viral protein that inhibits or counteracts prokaryotic host helicase/nuclease proteins in order to escape the antiviral activity of the latter. When functioning in their exonuclease mode, helicase/nuclease proteins such as bacterial RecBCD or AddAB degrade any free DNA end as well as the linear dsDNA products resulting from restriction Type II cleavage. Any prokaryotic virus that exposes free dsDNA ends as part of its life cycle must find the means to evade destruction by these host enzymes. Prokaryotic viruses escape this host defense by expressing inhibitors or by protecting the ends of their linear genomes from digestion." []
315	UPK:0228	"Protein involved in the repair of damages to one strand of DNA (loss of purines due to thermal fluctuations, formation of pyrimidine dimers by UV irradiation, for instance). The site of damage is recognized, excised by an endonuclease, the correct sequence is copied from the complementary strand by a polymerase and the ends of this correct sequence are joined to the rest of the strand by a ligase. In bacterial systems, the polymerase also acts as endonuclease. Excisase A and other proteins involved in recombination mediate DNA excision; a process whereby abnormal or mismatched nucleotides are enzymatically cut out of a strand of a DNA molecule." []
316	UPK:0229	"Protein involved in DNA integration, a process that mediates the insertion of foreign genetic material, or other duplex DNA, into a chromosome, or another replicon, in order to form a covalently linked DNA continuous with the host DNA." []
317	UPK:0230	"Specific recombinases which catalyze the inversion of a DNA segment within a nucleoprotein structure termed invertasome." []
318	UPK:0233	"Protein involved in DNA recombination, i.e. any process in which DNA molecules are cleaved and the fragments are rejoined to give a new combination." []
319	UPK:0234	"Protein involved in the repair of DNA, the various biochemical processes by which damaged DNA can be restored. DNA repair embraces, for instance, not only the direct reversal of some types of damage (such as the enzymatic photoreactivation of thymine dimers), but also multiple distinct mechanisms for excising damaged base; termed nucleotide excision repair (NER), base excision repair (BER) and mismatch repair (MMR); or mechanisms for repairing double-strand breaks." []
320	UPK:0235	"Protein involved in DNA replication, i.e. the duplication of DNA by making a new copy of an existing molecule. The parental double-stranded DNA molecule is replicated semi conservatively, i.e. each copy contains one of the original strands paired with a newly synthesized strand that is complementary in terms of AT and GC base pairing." []
321	UPK:0236	"Protein involved in the inhibition of DNA replication." []
322	UPK:0237	"Protein involved in the synthesis of DNA from deoxyribonucleic acid monomers." []
323	UPK:0238	"Protein which binds to DNA, typically to pack or modify the DNA, or to regulate gene expression. Among those proteins that recognize specific DNA sequences, there are a number of characteristic conserved motifs believed to be essential for specificity. Many DNA-binding domains are described in PROSITE." []
324	UPK:0239	"Enzyme that catalyzes DNA synthesis by addition of deoxyribonucleotide units to a DNA chain using DNA as a template. They can also possess exonuclease activity and therefore function in DNA repair." []
325	UPK:0240	"Protein of the DNA-directed RNA polymerase complexes, which catalyze RNA synthesis the by addition of ribonucleotide units to a RNA chain using DNA as a template. They can initiate a chain de novo. Prokaryotes have a single enzyme for the three RNA types that is subject to stringent regulatory mechanisms. Eukaryotes have type I that synthesizes all rRNA except the 5S component, type II that synthesizes mRNA and hnRNA and type III that synthesizes tRNA and the 5S component of rRNA." []
327	UPK:0241	"Protein which, if defective, causes Down's syndrome, a condition due to the presence of three copies of chromosome 21 (trisomy 21), characterized by some degree of mental retardation, short stature and poor muscle tone. Common (1 in 700 live births); incidence increases with maternal age. The cause is usually non-disjunction at meiosis but occasionally a translocation of fused chromosomes 21 and 14." []
328	UPK:0242	"Protein which, if defective, causes dwarfism, a skeletal growth defect resulting in the condition of being undersized." []
329	UPK:0243	"Large multimeric complex with ATPase activity, responsible for the movement of eukaryotic cilia and flagella (axonemal dynein) and for the intracellular retrograde motility of vesicles, organelles and chromosomes along microtubules (cytosolic dynein). Constitutes the side arms of the outer microtubule doublets in the ciliary axoneme and is responsible for the sliding. Also used for the dynein-associated microtubule-binding proteins (MTBs), e.g. dynactin." []
330	UPK:1011	"Protein which, if defective, causes dyskeratosis congenita, a clinically and genetically heterogeneous disorder characterized by abnormal skin pigmentation, mucosal leukoplakia, nail dystrophy, progressive bone marrow failure, and increased predisposition to cancer." []
331	UPK:1023	"Protein which, if defective, causes dystonia or dystonic conditions that feature persistent or recurrent episodes of dystonia as a major manifestation of disease. Dystonia is a movement disorder with a neurological basis, due to disordered tonicity of muscle. It is characterized by sustained involuntary muscle contractions that cause abnormal postures, twisting, repetitive and patterned movements. It may affect muscles throughout the body (generalized), in certain parts of the body (segmental), or may be confined to particular muscles or muscle groups (focal)." []
332	UPK:1215	"Protein which, if defective, causes any of the muscular disorders caused by aberrant glycosylation of dystroglycan. These genetically heterogeneous diseases include a range of conditions with different degrees of severity. At the most severe end of the clinical spectrum, Walker-Warburg syndrome (WWS), muscle-eye-brain disease (MEB) and Fukuyama congenital muscular dystrophy (FCMD) are characterized by congenital muscular dystrophy and severe structural brain and eye abnormalities, which in WWS result in early infantile death. At the mildest end of the clinical spectrum, affected individuals present with limb girdle muscular dystrophy (LGMD), without brain and eye involvement." []
333	UPK:0244	"Bacteriophage or viral protein expressed in the first phase of the infectious cycle." []
334	UPK:0038	"Protein which, if defective, causes ectodermal dysplasia, a heterogeneous group of developmental disorders affecting tissues of ectodermal origin. Ectodermal dysplasias are characterized by abnormal development of two or more ectodermal structures such as hair, teeth, nails and sweat glands, with or without any additional clinical sign. Each combination of clinical features represents a different type of ectodermal dysplasia." []
335	UPK:0245	"Protein containing at least one EGF-like domain, a sequence of about thirty to forty amino-acid residues long found in the sequence of epidermal growth factor (EGF). It has been shown to be present, in a more or less conserved form, in a large number of proteins. The EGF-like domain contains six cysteines which form disulfide bonds within the domain (C1-C3, C2-C4, C5-C6)." []
336	UPK:0248	"Protein which, if defective, causes Ehlers-Danlos syndrome (EDS), a genetically and phenotypically heterogeneous group of connective-tissue disorders. It affects primarily the skin, ligaments, joints, and blood vessels. Typical features include skin hyperextensibility, joint hypermobility, easy bruisability, friability of tissues with bleeding and poor wound healing. Inheritance can be autosomal dominant, autosomal recessive, or X-linked recessive." []
337	UPK:0249	"Protein involved in the transport of electrons, a process by which electrons are transported through a series of reactions from the reductant, or electron donor, to the oxidant, or electron acceptor, with concomitant energy conversion. Necessary for both photosynthesis and aerobic respiration." []
338	UPK:0250	"Protein which, if defective, causes elliptocytosis, a disorder characterized by variable haemolytic anaemia and elliptical red blood cell shape. Caused by deficiency/dysfunction of red blood cell membrane proteins." []
339	UPK:0251	"Protein that associates with ribosomes cyclically during the elongation phase of protein synthesis, and catalyze formation of the acyl bond between the incoming amino-acid residue and the peptide chain." []
340	UPK:1067	"Protein which, if defective, causes Emery-Dreifuss muscular dystrophy, a heterogenous group of inherited muscular dystrophy without the involvement of nervous system. The disease is characterized by slowly progressive muscle weakness, contracture of the elbows, Achilles tendon and posterior cervical muscles, and cardiac features." []
341	UPK:0254	"Protein involved in endocytosis, a process by which extracellular materials are taken up into a cell by invagination of the plasma membrane to form vesicles enclosing these materials." []
342	UPK:0255	"Phosphodiesterase capable of cleaving at phosphodiester internal bonds within a DNA or RNA substrate." []
343	UPK:0256	"Protein whose subcellular location is the endoplasmic reticulum, a membrane system continuous with the outer nuclear membrane. It consists of flattened, single-membrane vesicles whose inner compartments, the cisternae, interconnect to form channels throughout the cytoplasm. The rough-surface portion is studded with ribosomes." []
344	UPK:0257	"Morphine-like peptides produced by the brain in response to neurotransmitters. They bind to neuron receptors that mediate the action of opiates and induce analgesia and sedation." []
345	UPK:0967	"Protein found in or associated with endosomes. Endosomes are highly dynamic membrane systems involved in transport within the cell, they receive endocytosed cell membrane molecules and sort them for either degradation or recycling back to the cell surface. They also receive newly synthesised proteins destined for vacuolar/lysosomal compartments. In certain cell types, endosomal multivesicular bodies may fuse with the cell surface in an exocytic manner. These released vesicles are called exosomes." []
346	UPK:0259	"Protein involved in the synthesis of enterobactin, a compound that transports iron from the bacterial environment into the cell cytoplasm." []
347	UPK:0260	"Toxin which, either when ingested or when produced by enterobacteria within the intestine, acts on the intestinal mucosa and induces diarrhea by perturbing ion and water transport systems." []
391	UPK:0294	"Protein involved in the biochemical reactions with fucose. L-fucose (6-deoxy-L-galactose) is present in some algae and identified in the chains of glycoproteins; it is the only polysaccharides of certain bacterias." []
392	UPK:0295	"Protein capable of killing or inhibiting growth of fungi." []
348	UPK:0263	"Protein which, if defective, causes epidermolysis bullosa, any of a group of mechano-bullous disorders characterized by blistering and/or erosion of the skin and mucous membranes which occur spontaneously or as a result of mild physical trauma. Traditionally, epidermolysis bullosa is divided into three broad categories based on the level of tissue separation: in epidermolysis bullosa simplex (EBS), tissue separation is intraepidermal and occurs within the basal keratinocytes at the bottom layer of epidermis; the junctional forms (JEB) display tissue separation within the dermo-epidermal basement membrane (basement membrane zone, BMZ), primarily within the lamina lucida; in the dystrophic forms (DEB), tissue separation occurs below the lamina densa within the upper papillary dermis. Some forms of epidermolysis bullosa display tissue separation at the basal cell/lamina lucida interface, at the level of the hemidesmosomes (hemidesmosomal variants). The hemidesmosomal variants overlap with the traditional subtypes, particularly the simplex and junctional forms. In addition to skin involvement, various extracutaneous manifestations can be associated with distinct subtypes of epidermolysis bullosa." []
349	UPK:0887	"Protein which, if defective, causes epilepsy, any of a group of disorders characterized by paroxysmal transient disturbances of the electrical activity of the brain that may be manifested as episodic impairment or loss of consciousness, abnormal motor phenomena, psychic or sensory disturbances, or perturbation of the autonomic nervous system. Epilepsy is classified as either symptomatic or idiopathic according to whether the cause is known or unknown. Both of these types can be classified into partial and generalized epilepsy, depending on whether the seizures are due to limited or to widespread brain lesions, respectively." []
350	UPK:0931	"Protein involved in the 'ER-to-Golgi' transport, a bidirectional membrane traffic between the endoplasmic reticulum and the Golgi apparatus which mediates the transfer of cargo molecules by means of small vesicles or tubular-saccular extensions." []
351	UPK:0895	"Protein encoded by proviral genes of endogenous retroviruses. When a retrovirus infects a host cell, viral reverse transcriptase (RT) makes a DNA copy of the RNA viral genome. The integrated DNA form of a retrovirus is referred to as a provirus. Proviral genes are expressed by cellular mechanisms. Retroviruses that enter the germline are referred to as endogenous retroviruses (ERVs) to distinguish them from horizontally transmitted, not passed on to host progeny, "exogenous" retroviruses. Amplification of ERV copy number via retrotransposition or reinfection has given rise to numerous ERV sequences in the vertebrate genomes. As much as 8% of the human genome, and 10% of the mouse genome, consists of sequences derived from ERV insertions." []
352	UPK:0265	"Protein involved in the maturation of erythrocytes, the predominant type of cells present in vertebrate blood and which contain the gas-transporting protein, hemoglobin." []
353	UPK:0266	"Protein involved in the synthesis of ethylene (C2H4), an unsaturated hydrocarbon gas mainly produced in plants. It has developmental effects as a hormone, including growth inhibition, regulation of fruit development, leaf abscission and aging." []
354	UPK:0936	"Protein involved in the ethylene signaling pathway (e.g. transport and signal transduction) that regulates many aspects of plant growth and development (e.g. seed germination, root and shoot growth, flower development, plant defense, senescence, abscission and ripening). This phytohormone can be synthesized from methionin." []
355	UPK:1262	"Viral protein which prevents host gene expression by blocking host transcription, mRNA export or translation. This gives viral transcripts a competitive edge to use the hijacked translation machinery. Preventing the expression of host proteins is also a strategy to counteract the antiviral response." []
356	UPK:1191	"Viral protein involved in inhibiting host transcription to ensure the shutoff of cellular proteins expression and give virus transcripts a competitive edge for access to the cellular translation machinery. Preventing the expression of host proteins is also a strategy to counteract the antiviral response. Inhibition of transcription can be performed by interfering with host RNA pol-II function or interfering with general transcription factors." []
357	UPK:1193	"Viral protein involved in inhibiting the host translational machinery to shutoff cellular gene expression. This gives virus transcripts a competitive edge to use the hijacked translation machinery. Preventing the expression of host proteins is also a strategy to counteract the antiviral response. Several virus are known to inhibit host translation mostly by inactivating translation factors." []
358	UPK:1259	"Viral protein that counteracts the translation shutoff set up by the bacterial host in order to inhibit viral replication. This antiviral defense system alters a crucial cellular process thereby blocking virus multiplication and ending up with host dormancy or even cell death. For example, some E.coli strains infected by bacteriophage T4 activate an anticodon nuclease which causes depletion of tRNA(Lys) and, consequently, abolishes T4 protein synthesis and causes cell death. However, this effect is counteracted by the repair of tRNA(Lys) in consecutive reactions catalyzed by the viral enzymes polynucleotide kinase and RNA ligase. The ToxIN system functions as a toxin-antitoxin (TA) tandem which is used as a antiviral defense mechanism." []
359	UPK:1125	"Viral protein sharing sequence homology with host interleukins. Interleukins are produced by immune system cells such as lymphocytes, macrophages and monocytes, and modulate inflammation and immunity by regulating growth, mobility and differentiation of lymphoid and other cells. Several viruses encode interleukin-like proteins playing a role in immune evasion. Additionally, viral interleukins have been shown to activate cellular signaling cascades that enhance virus replication." []
360	UPK:0267	"Enzyme which excises abnormal or mismatched nucleotides from a DNA strand." []
361	UPK:0268	"Protein involved in exocytosis, a process by which a material is transported out of a cell using a vesicle that first engulfs the material and then is extruded through an opening in the cell membrane. The exocyst protein complex plays an important role in exocytosis by directing exocytic vesicles to their precise sites of fusion in the plasma membrane." []
362	UPK:0269	"Enzyme that degrades DNA or RNA by progressively splitting off single nucleotides from one end of the chain." []
363	UPK:0270	"Protein involved in the synthesis of exopolysaccharide (EPS), a high molecular-weight polymer composed of saccharide subunits. An example is succinoglycan (EPS I) of Rhizobium meliloti, that is important for invasion of the nodules that it elicits on its host, Medicago sativa." []
364	UPK:0271	"Protein which is a component of the exosome, a complex of proteins that includes 3->5 exoribonucleases and that plays a major role in diverse RNA processing and degradation pathways in eukaryotes and archaea." []
365	UPK:0952	"Protein originating from a species thought to be extinct, i.e. from a species for which no known surviving specimens are known to exist. Eg. Dodo, Mammoth or Neanderthal." []
366	UPK:0272	"Protein found in the extracellular matrix. The extracellular matrix consists of any material produced by cells and secreted into the surrounding medium, but this term generally applies to the non-cellular components of animal tissues. The extracellular matrix forms a supportive meshwork around cells and is largely composed of collagen, laminin, fibronectin and glycosaminoglycans. It can influence the properties of the cells that it supports. In certain tissues, specific modifications to the extracellular matrix occur. For instance, the matrix of bone is mineralized to resist compression." []
367	UPK:0273	"Protein found in the lens, a transparent body at the front of the vertebrate eye." []
368	UPK:0274	"Protein involved in flavin adenine dinucleotide synthesis or protein which contains at least one FAD as prosthetic group/cofactor (flavoprotein) such as many oxidation-reduction enzymes. FAD is an electron carrier molecule that functions as a hydrogen acceptor. The generic term "flavin" derives from the Latin word flavius ("yellow") because of the brilliant yellow color they exhibit as solids and in neutral aqueous solutions." []
369	UPK:0951	"Protein which, if defective, causes familial hemophagocytic lymphohistiocytosis. FHL is a genetically heterogeneous, autosomal recessive disorder characterized by immune dysregulation with hypercytokinemia and defective natural killer cell function. The clinical features of the disease include fever, hepatosplenomegaly, cytopenia, hypertriglyceridemia, hypofibrinogenemia, and neurological abnormalities ranging from irritability and hypotonia to seizures, cranial nerve deficits and ataxia. Hemophagocytosis is a prominent feature of the disease, and non-malignant infiltration of macrophages and activated T lymphocytes in lymph nodes, spleen and other organs is also found." []
370	UPK:0923	"Protein which, if defective, causes Fanconi anemia. Fanconi anemia is a rare recessive disorder characterized by progressive pancytopenia, hypoplasia of the bone marrow and patchy brown discoloration of the skin, due to melanin deposition. It is associated with multiple congenital anomalies of the musculoskeletal and genitourinary systems." []
371	UPK:0275	"Protein involved in the synthesis of fatty acids, long chain organic acids of the general formula CH3(CnHx)COOH. They are constituents of lipids and can be saturated or unsaturated. The esterified forms are important both as energy storage molecules and structural molecules." []
372	UPK:0276	"Protein involved in the biochemical reactions with fatty acids. Fatty acids are long chain organic acids of the general formula CH3(CnHx)COOH. They are constituents of lipids and can be saturated or unsaturated. The esterified forms are important both as energy storage molecules and structural molecules." []
373	UPK:0278	"Protein involved in fertilization, the union of two haploid cells, the gametes, to form a diploid cell, the zygote." []
374	UPK:1206	"Toxin involved in fibrinogen degradation leading to a decrease of plasma fibrinogen concentration. Fibrinogenolytic toxins are mostly snake venom proteases." []
375	UPK:0280	"Protein involved in fibrin degradation leading to the dissolving of blood clots." []
376	UPK:1205	"Toxin involved in fibrin degradation leading to the dissolution of fibrin clots. Fibrinolytic toxins are mostly snake venom proteases." []
377	UPK:0281	"Protein found in a fimbrium or pilus. A fimbrium or pilus is a hair-like, non-flagellar, polymeric filamentous appendage that extend from the bacterial or archaeal cell surface, such as type 1 pili, P-pili, type IV pili or curli. Pili perform a variety of functions, including surface adhesion, motility, cell-cell interactions, biofilm formation, conjugation, DNA uptake, and twitching motility." []
378	UPK:1029	"Protein which is involved in the formation, organization or maintenance of the fimbrium, a long hair-like cell surface appendage. The flagellar apparatus consists of the flagellar filament made of polymerized flagellin, the hook-like structure near the cell surface and a system of rings embedded in the cell enveloppe (the basal body or flagellar motor). The basal body and the hook anchor the whip-like filament to the cell surface. The flagellum is a rotating structure whose switches propels the cell through a liquid medium." []
379	UPK:0283	"Protein involved in the movement of the flagella." []
380	UPK:0282	"Protein present in or involved in the biogenesis or function of the flagellum, a long whip-like or feathery structure which propels the cell through a liquid medium. This motile cilium is produced by the unicellular eukaryotes, and by the motile male gametes of many eukaryotic organisms. The flagella commonly have a characteristic axial '9+2' microtubular array (axoneme) and bends are generated along the length of the flagellum by restricted sliding of the nine outer doublets." []
381	UPK:0284	"Protein involved in the synthesis of flavonoids, polyphenolic compounds possessing 15 carbon atoms; two benzene rings joined by a linear three carbon chain, a C6-C3-C6 skeleton. C6 presents a benzene ring, C3 often is part of of an oxygen-containing ring. Flavonoids are coloured phenolic pigments originally considered vitamins (Vitamins P, C2) but not shown to have any nutritional role. They are responsible for the red/purple colours of many higher plants." []
382	UPK:0285	"Enzymes which contain one or more flavin nucleotides (FAD or FMN) as redox cofactors. Flavoproteins are involved, for example, in the oxidative degradation of pyruvate, fatty acids and amino acids, and in the process of electron transport." []
383	UPK:0286	"Protein which stimulates or which is involved in flight, the act of passing through the air by the use of wings." []
384	UPK:0287	"Protein involved in the transition from vegetative to reproductive development in plants." []
385	UPK:0288	"Protein involved in flavin adenine mononucleotide synthesis or protein which contains at least one FMN as prosthetic group/cofactor (flavoproteins), such as many oxidation-reduction enzymes. FMN is an electron carrier molecule that functions as a hydrogen acceptor. The generic term "flavin" derives from the Latin word flavius ("yellow") because of the brilliant yellow color they exhibit as solids and in neutral aqueous solutions." []
386	UPK:0289	"Protein involved in the synthesis of folate, the ionic form of folic acid (Latin folium, 'leaf'), first found in spinach leaves. Folate is converted in a two-step reduction into its coenzyme form tetrahydrofolate, often abbreviated FH4 or THF, which acts as a carrier of one-carbon units at several oxidation levels in a variety of biosyntheses." []
387	UPK:0290	"Protein that binds folate, the ionic form of folic acid." []
388	UPK:0291	"A protein in which either the N-terminal N-formylmethionine has not been processed by the methionyl-tRNA formyltransferase or which is posttranslationally modified by the attachment of at least one formyl group." []
389	UPK:0292	"Protein involved in fruit ripening. The fruit is the matured ovary of a plant, enclosing the seed(s). The plant hormone ethylene stimulates fruit ripening." []
393	UPK:1169	"Viral protein involved in the merging of the virus envelope with host cytoplasmic membrane during viral penetration into host cell. Virus fusion proteins drive this fusion reaction by undergoing a major conformational change that is triggered by interactions with the target cell. This pathway is used by viruses whose fusion protein is usually pH independent such as most paramyxoviruses, herpesviruses and retroviruses. MHV-JHM coronavirus has been shown to fuse directly with the host cytoplasmic membrane. Prokaryotic viruses such as Tectiviridae fuse their inner membrane with the host cytoplasmic membrane whereas Cystoviridae fuse their outer membrane with the host cytoplasmic membrane." []
394	UPK:1170	"Viral protein involved in the merging of the virus envelope with host endosomal membrane during viral penetration into host cell. Viral fusion proteins drive this fusion reaction by undergoing a major conformational change that is triggered by interactions with the target cell. The specific trigger is mainly endosome acidification which induce activation of the fusion protein by conformational change. This pathway is used by enveloped viruses which are endocytosed and whose fusion protein is usually pH-dependent like influenza A virus, rhabdoviruses, bornaviruses, filoviruses, asfarviridae, flaviviridae, alphaviruses, HIV-1, avian leukosis virus, SARS, 229E, and MHV-2 coronaviruses." []
395	UPK:1168	"Viral protein involved in the merging of the virion membrane with a host membrane during viral penetration into host cell. Viral fusion proteins drive this fusion reaction by undergoing a major conformational change that is triggered by interactions with the target cell. The specific trigger depends on the virus and can be exposure to low pH in the endocytic pathway or interaction of the virion with the host receptor(s). In prokaryotic viruses, host-virus membrane fusion can occur either at the host outer membrane or plasma membrane. Bacteriophages such as cystoviridae fuse their external envelope with the host outer membrane, whereas others like tectiviridae fuse their inner envelope with the host plasma membrane." []
396	UPK:1239	"Viral protein involved in the merging of the virion external lipidic membrane (envelope) with the prokaryotic host outer membrane during viral penetration into host cell. Bacteriophages such as Cystoviridae for example fuse their membrane with the host outer membrane." []
397	UPK:1077	"Viral protein involved in the modulation of host cell cycle progression by dysregulating the G0/G1 transition. Some viruses benefit from keeping cells in resting state (G0), while others favor entry through G1 and subsequent cell division to replicate more efficiently." []
398	UPK:1078	"Viral protein involved in the modulation of host cell cycle progression by dysregulating the G1/S transition. Some viruses benefit from an arrest in G1 to S phase transition, while others force through S phase to favor their own replication." []
399	UPK:0298	"Protein involved in the biochemical reactions with galactitol. This sugar alcohol is derived from galactose. It can be found in certain bacteria, yeasts, fungi and plants. In humans, the congenital galactosemic cataracts are due to an accumulation of galactitol within the lens." []
400	UPK:0299	"Protein involved in the biochemical reactions with the monosaccharide galactose. This optical isomer (epimer) of glucose is a constituent of various oligosaccharides (e.g. lactose, raffinose), polysaccharides (e.g. galactans, agar, gum arabic) and also of sphingolipids (galactocerebrosides)." []
401	UPK:0301	"Protein which possesses at least one gamma-carboxyglutamic acid, a vitamin K dependent post-translational modification of a glutamate residue found in blood coagulation proteins and in the proteins of calcified tissues. Gamma-carboxyglutamyl residues are good chelators of calcium ions. There are two natural forms of vitamin K, which are phylloquinone (vitamin K1 or phytylmenaquinone) in green vegetables and menaquinone (vitamin K2 or menaquinone-n, depending of the number of isoprene units of the side-chain or MK-n) in intestinal bacteria, as well as one synthetic provitamin form, menadione (vitamin K3). In infants, the primary symptom of a deficiency of this fat-soluble vitamin is a hemorrhagic syndrome." []
402	UPK:0331	"Protein which, if defective, causes gangliosidosis. Gangliosidosis defines any of a group of autosomal recessive lysosomal storage diseases characterized by the accumulation of gangliosides GM1 or GM2 and related glycoconiugates, and by progressive psychomotor deterioration. Subtypes include GM1-gangliosidoses and GM2-gangliosidoses." []
403	UPK:0303	"Protein component of gap junctions which are specialized regions of the plasma membrane formed by a cluster of channels allowing small molecules to diffuse from the cytosol of one cell to that of an adjacent cell. A current model of the gap junction consists of a cluster of gap-junction channels. Both membranes contain connexon hemichannels, composed of a hexamer of an integral membrane protein which is often referred to as connexin. The junction of two adjacent connexons forms a gap-junction channel." []
404	UPK:0302	"A group of insect proteins which are crucial for the development of proper embryonic segmentation. These are the first proteins that define the coarsest subdivisions. Generally, gap gene mutations are lethal and eliminate a large block of contiguous segments from the embryo." []
405	UPK:0304	"Protein component of, or involved in the formation of, gas vesicles, which are a rigid, hollow structure found in five phyla of the Bacteria and two groups of the Archaea, but mostly restricted to planktonic microorganisms, in which they provide buoyancy. By regulating their relative gas vesicle content, aquatic microbes are able to perform vertical migrations. The gas vesicle is impermeable to liquid water, but is highly permeable to gases and is normally filled with air. Two proteins have been shown to be present in the gas vesicle: GVPa, which makes the ribs that form the structure, and GVPc, which binds to the outside of the ribs and stiffens the structure against collapse." []
406	UPK:0305	"Protein involved in the exchange of gases." []
407	UPK:0306	"Protein involved in gastrulation, a stage in early embryogenesis in which cell movements result in a massive reorganization of the embryo from an initially unstructured group of cells, the blastula, into a multi-layered organism. During gastrulation, the primary germ layers (endoderm, mesoderm, and ectoderm) are formed and organized in their proper locations for further development." []
408	UPK:0307	"Protein which, if defective, causes Gaucher disease, the most prevalent sphingolipid storage disorder caused by a recessively inherited deficiency of the enzyme glucocerebrosidase. Most common in Ashkenazi Jews, it is associated with hepatosplenomegaly (enlargement of liver and spleen) and, in severe early onset forms of the disease, with neurological dysfunction." []
409	UPK:0308	"Any protein used in a biotechnological process that results in the modification of a naturally occurring food (crop or livestock). Examples include proteins introduced to enable herbicide or insect resistance or proteins that act in fruit ripening." []
410	UPK:0309	"Protein involved in germination, the physiological and developmental changes by a seed, spore, pollen grain (microspore), or zygote that occur after release from dormancy, and encompassing events prior to and including the first visible indications of growth." []
411	UPK:0939	"Protein involved in the gibberellin (GA) signaling pathway (e.g. transport and signal transduction) that regulates many aspects of plant growth including seed germination, hypocotyl elongation, stem elongation, leaf expansion, trichome development, pollen maturation and flower and fruit development. GAs are tetracyclic diterpenoid phytohormones found in plants, fungi and bacteria. They are named GA1....GAn in order of discovery. The term "gibberellin" was first given to a substance, produced by the fungus Gibberella fujikuroi, which caused overgrowth symptoms in rice. This substance was later proven to be a mixture of GAs, with GA1 and GA3 being the active factors." []
412	UPK:0955	"Protein which, if defective, causes glaucoma, a group of eye diseases characterized by pathological changes in the optic disk, progressive loss of optic nerve axons and visual field defects. Most of the patients with glaucoma have an increased intraocular pressure. The disease is painless and often diagnosed at a late stage, when visual field defects are severe. Glaucoma is one of the leading causes of blindness worldwide." []
413	UPK:0311	"Protein involved in the biochemical pathway(s) in which gluconate is the carbon source." []
414	UPK:0312	"Protein involved in the biosynthesis of "new" glucose from such noncarbohydrate precursors as pyruvate, lactate, certain amino acids and intermediates of the tricarboxylic acid cycle." []
415	UPK:0313	"Protein involved in the biochemical reactions with the 6-carbon aldose sugar glucose." []
416	UPK:0314	"Protein involved in the synthesis of the acidic amino acid glutamate. Glutamate is a component of proteins and can also act as a neurotransmitter in the central nervous system." []
417	UPK:0315	"Enzyme that catalyzes the removal of the ammonia group from glutamine and transfers it to a substrate to form a new carbon-nitrogen group. Glutamine amidotransferase (GATase) domains can occur either as single polypeptides or as domains in larger multifunctional proteins. There exist two classes of glutamine amidotransferases domains: I and II." []
418	UPK:0316	"Protein which, if defective, causes glutaricaciduria (GA), a metabolic disorder characterized by the excretion of glutaric acid in the urine. Type I GA is caused by the deficiency of glutaryl-CoA dehydrogenase, a mitochondrial enzyme involved in the metabolism of lysine, hydroxylysine and tryptophan. Type II GA differs from type I in that multiple acyl-CoA dehydrogenase deficiencies result in a large excretion not only of glutaric acid but also of lactic, ethylmalonic, butyric, isobutyric, 2-methyl-butyric, and isovaleric acids. GA II can result from a deficiency of any one of 3 mitochondrial molecules: the alpha and beta subunits of electron transfer flavoprotein and electron transfer flavoprotein-ubiquinone oxidoreductase." []
419	UPK:0317	"Protein involved in the synthesis of the tripeptide glutathione (Gamma-Glu-Cys-Gly). Glutathione sulphydryl group is kept largely in the reduced state; this allows it to act as a sulphydryl buffer, reducing any disulphide bonds formed within cytoplasmic proteins to cysteines. Glutathione is also important as a cofactor for the enzyme glutathione peroxidase, in the uptake of amino acids and participates in leucotriene synthesis. Glutathione contains an unusual peptide linkage between the carboxyl group of the glutamate side chain and the amine group of cysteine." []
420	UPK:0318	"Protein which is posttranslationally modified by the attachment of a glutathione molecule by a disulfide bond." []
421	UPK:0971	"Protein containing one or more covalently linked glucose residues, resulting from a non-enzymatic spontaneous reaction. The carbohydrate is attached to an amino-acid nitrogen atom (e.g. from a lysine side chain, or the amino-terminal group). This modification is a side effect of diabetes and aging. Glycation is the first step toward the formation of advanced glycation endproducts (AGEs). Some AGEs are benign, but others are implicated in age-related chronic diseases such as: type II diabetes mellitus, cardiovascular diseases, Alzheimer's disease, etc." []
422	UPK:0319	"Protein involved in the biochemical reactions with the 3-carbon sugar alcohol glycerol. Glycerol is primarily of interest as the central structural component of the major classes of biological lipids, triglycerides and phosphatidyl phospholipids. It is also an important intermediate in carbohydrate and lipid metabolism." []
423	UPK:0320	"Protein involved in the synthesis of glycogen, a branched polymer of D-glucose (mostly -(1-4) linked, but with some -(1-6) linked residues at branch points). Glycogen is the major short term storage polymer of animal cells and is particularly abundant in liver and to a lesser extent in muscles." []
424	UPK:0321	"Protein involved in the biochemical reactions with glycogen, a branched polymer of D-glucose (mostly -(1-4) linked, but with some - (1-6) linked residues at branch points). Glycogen is the major short term storage polymer of animal cells and is particularly abundant in liver and to a lesser extent in muscles." []
425	UPK:0322	"Protein which, if defective, causes glycogen storage disease, a group of inherited metabolic disorders involving the enzymes responsible for the synthesis and degradation of glycogen. At least thirteen types of this disease have been described." []
426	UPK:0323	"Protein involved in the glycolate pathway, synthesis of the amino acids serine and glycine from glycolate via a glyoxylate intermediate." []
427	UPK:0324	"Protein involved in the anaerobic enzymatic conversion of glucose to lactate or pyruvate, resulting in energy stored in the form of adenosine triphosphate (ATP), as occurs in skeletal muscle and in embryonic tissue." []
428	UPK:0325	"Protein containing one or more covalently linked carbohydrates of various types, i.e. from monosaccharides to branched polysaccharides, including glycosylphosphatidylinositol (GPI), glycosaminoglycans (GAG)." []
429	UPK:0326	"Hydrolases which attack glycosidic bonds in carbohydrates, glycoproteins and glycolipids. The glycosidases are not highly specific. Usually they distinguish only the type of bond, e.g. O- or N-glycosidic, and its configuration (alpha or beta)." []
430	UPK:0327	"Protein present in the glycosome, a microbody-like organelle found in all members of the protist order Kinetoplastida examined. Nine enzymes involved in glucose and glycerol metabolism are associated with these organelles. These enzymes are involved in pathways which, in other organisms, are usually located in the cytosol." []
431	UPK:0328	"Enzymes that catalyze the transfer of glycosyl (sugar) residues to an acceptor, both during degradation (cosubstrates= water or inorganic phosphate) and during biosynthesis of polysaccharides, glycoproteins and glycolipids. In biosynthetic glycosyl transfers, the common activated monomeric sugar intermediate is a nucleoside diphosphate sugar." []
432	UPK:0329	"Protein involved in the glyoxylate bypass, an alternate route in bacteria, plants, and fungi which bypasses the CO2-evolving steps of the tricarboxylic acid cycle, thus permiting the utilization of fatty acids or acetate, in the form of acetyl-CoA, as sole carbon source, particularly for the net biosynthesis of carbohydrate from fatty acids. The glyoxylate bypass is especially prominent in plant seeds." []
433	UPK:0330	"Protein present in the glyoxysome, a membrane-surrounded plant cell organelle, especially found in germinating seeds, and involved in the breakdown and conversion of fatty acids to acetyl-CoA for the glyoxylate bypass. Since it is also rich in catalase, the glyoxysome may be related to the microbodies or peroxisomes or derived from them." []
434	UPK:0332	"Protein involved in the synthesis of GMP. GMP is the abbreviation for the nucleotide guanosine 5'-monophosphate." []
435	UPK:0333	"Protein found in the Golgi apparatus, an organelle present in eukaryotic cells that appears as a stack of 6-8 plate-like membranous compartments and associated vesicles and vacuoles, often located near the centrosome. It has four functionally distinct compartments: cis, medial and trans Golgi stacks, and the trans Golgi network (TGN). The first three are involved in posttranslational modifications of proteins (e.g., N- or O-glycosylation, sulfation, processing of acid hydrolases), while the TGN is involved in sorting the proteins to their final destination (e.g., to lysosomes, to secretory vesicles, or to plasma membrane)." []
436	UPK:0334	"Protein involved in gonadal differentiation, the progressive restriction of the developmental potential and increasing specialization of function which takes place during the embryonic development and leads to the formation of gamete-producing glands, such as ovary or testis." []
437	UPK:0335	"Protein which, if defective, causes gout, a recurrent acute arthritis of peripheral joints caused by the precipitation of monosodium urate crystals in articular cartilage. Gout is usually due to overproduction of uric acid secondary to an inherited abnormality of purine metabolism, but may be a result of urate under-excretion." []
438	UPK:0336	"Protein bound to the lipid bilayer of a membrane through either a GPI-anchor (glycosylphosphatidylinositol anchor), a complex oligoglycan linked to a phosphatidylinositol group, or a GPI-like-anchor, a similar complex oligoglycan linked to a sphingolipidinositol group, resulting in the attachment of the C-terminus of the protein to the membrane." []
439	UPK:0337	"Protein involved in the synthesis or the attachment to a protein of a GPI-anchor (glycosylphosphatidylinositol anchor) or a GPI-like-anchor (glycosylsphingolipidinositol anchor), both of which have complex oligoglycan linked to a phospholipidinositol molecule that serves to attach the C-terminus of some extracellular membrane proteins to the lipid bilayer of a membrane. The core glycolipid is composed of a tetraglycan: three mannose units and one glucosamine linked to a phospholipidinositol. The terminal mannose is linked to the protein via an ethanolamine attached to the C-terminal of the mature protein. The core structure is conserved from protozoa to humans. There are, however, marked differences in the glycosyl side chains attached to the core glycolipid. The phospholipid component may be either a phosphatide (two long chain fatty acids attached by ester linkage to glycerol phosphate) or a sphingolipid (a long chain fatty acid attached by amide linkage to a ceramide phosphate). Some yeast and Dictyosteliida synthesize the GPI-like anchor de novo, whereas other organisms may interconvert the lipid components by a "resculpting" process after the anchor is attached to the protein." []
440	UPK:1214	"Toxin which interferes with the function of the muscarinic acetylcholine receptor (mAChR). The mAChR is a specific class of G-protein coupled receptor (GPCR) that binds acetylcholine. These toxins are mostly found in snake venoms." []
441	UPK:0297	"Receptors which transduce extracellular signals across the cell membrane. At the external side they receive a ligand (a photon in case of opsins), and at the cytosolic side they activate a guanine nucleotide-binding (G) protein. These receptors are hydrophobic proteins that cross the membrane seven times." []
442	UPK:1213	"Toxin which interferes with the function of G-protein coupled receptors (GPCRs). These toxins are mostly found in snake and scorpion venoms." []
443	UPK:0338	"Protein involved in growth arrest, a phenomenon occurring when a cell does not proceed through the cell cycle." []
444	UPK:0339	"Protein which, by binding to a cell-surface receptor, triggers an intracellular signal-transduction pathway leading to differentiation, proliferation, or other cellular response." []
445	UPK:0340	"Protein other than a receptor that binds to a cell's growth factor." []
446	UPK:0341	"Protein involved in growth regulation, which usually implies the control of the rate of division rather than that of the size of an individual cell." []
447	UPK:0343	"GTPase-activating protein (GAP) by itself does not hydrolyze GTP but, by binding to a GTPase, accelerates its intrinsic GTPase activity." []
448	UPK:0342	"Protein which binds guanosine 5'-triphosphate (GTP), a ribonucleotide guanosine (a purine base guanine linked to the sugar D-ribofuranose) that carries three phosphate groups esterified to the sugar moiety." []
449	UPK:0344	"Protein which catalyzes the release of GDP (guanosine 5'-diphosphate)." []
450	UPK:0345	"Protein or apolipoprotein associated with High-Density Lipoproteins (HDL), a class of proteins involved in lipid (cholesterol, phospholipids and triacylglycerol) metabolism in the body fluids. HDL are formed in the liver and are involved in reverse cholesterol transport, the transport of cholesterol from peripherical tissues to the liver. Apolipoproteins are proteins which are specifically associated with lipoproteins, which is not the case for all the proteins associated with HDL or with the other lipoprotein classes." []
451	UPK:1009	"Protein involved in hearing, the special sense by which an organism is able to receive an auditory stimulus, convert it to a molecular signal, and recognize and characterize the signal. Sonic stimuli are detected in the form of vibrations and are processed to form a sound." []
452	UPK:1139	"Viral protein that forms a helical capsid to protect the viral genome. Viral helical capsids are about 7-30 nm in diameter and 200-2000 nm long." []
453	UPK:0347	"Protein with an helicase activity. Helicases are ATPases that catalyze the unwinding of double-stranded nucleic acids. They are tightly integrated (or coupled) components of various macromolecular complexes which are involved in processes such as DNA replication, recombination, and nucleotide excision repair, as well as RNA transcription and splicing." []
454	UPK:0348	"Protein which causes agglutination of erythrocytes or other cell types: In viruses, a protein which is responsible for attaching the virus to cell receptors and for initiating infection." []
455	UPK:0349	"Protein containing at least one heme, an iron atom coordinated to a protoporphyrin IX. In myoglobin and hemoglobin, one of the coordination positions of iron is occupied by oxygen or other ligands, such as carbon monoxide. Hemes are also found in cytochromes of the electron-transport chain where they bind electrons, in reducing peroxides (catalases and peroxidases), and act as terminal components in multienzyme systems involved in hydroxylation. Cytochrome c is the only common heme protein in which the heme is covalently bound." []
456	UPK:0350	"Protein involved in the synthesis of heme, an iron atom coordinated to a protoporphyrin IX." []
457	UPK:0351	"Protein which binds hemoglobin, a gas-carrying protein found in red blood cells." []
458	UPK:0353	"Protein involved in the coagulation of hemolymph, the circulatory fluid of invertebrate animals which is functionally comparable to the blood and lymph of vertebrates." []
459	UPK:0354	"Protein involved in hemolysis, the disruption of the integrity of the red cell membrane, thus causing the release of hemoglobin." []
460	UPK:1068	"Protein which, if defective, causes hemolytic uremic syndrome, a disorder characterized by non-immune hemolytic anemia, thrombocytopenia and renal failure. The vast majority of cases are sporadic, occur in young children and are associated with epidemics of diarrhea due to bacterial infections. This typical form of the disease has a good prognosis and death rate is very low. In contrast to typical hemolytic uremic syndrome, atypical forms present without a prodrome of enterocolitis and diarrhea and have a poor prognosis, with frequent development of end-stage renal disease or death." []
461	UPK:0355	"Protein which, if defective, causes hemophilia, a genetic disease characterized by uncontrollable bleeding due to a sex-linked recessive deficiency of blood-clotting factor (usually of Factor VIII)." []
462	UPK:1200	"Toxin which induces the leakage of blood components into tissues by damaging endothelial cells or disturbing endothelial cell interactions with the basement membrane. Hemorrhagic toxins are mostly found in snake venoms." []
463	UPK:0356	"Protein involved in the arrest of bleeding through blood clotting and contraction of blood vessels." []
464	UPK:1199	"Toxin which interferes with hemostasis regrouping all mechanisms implicated in the cessation of blood loss through damaged vessels. Hence, hemostasis impairing toxins not only interfere with platelet aggregation, the coagulation cascade, fibrinogen depletion, and fibrin clot degradation (fibrinolysis), but also provoke hemorrhage by damaging endothelial cells or disturbing their interaction with the basement membrane. Numerous snake venom families have the capacity to interfere with hemostasis." []
465	UPK:0357	"Protein containing at least one heparan sulfate, a highly sulfated glycosaminoglycan, closely related to heparin, which consists of repeating units of disaccharides composed of iduronic acid, glucosamine and N-acetylglucosamine." []
466	UPK:0358	"Protein which binds heparin, a highly sulfated glycosaminoglycan which consists of repeating units of disaccharides composed of D-glucosamine, D-glucuronic acid or L-iduronic acid. This anticoagulant is found in the granules of mast cells." []
467	UPK:0359	"Protein that confers, on plants, bacteria or other microorganisms, the ability to withstand herbicide action. Herbicides are chemicals that selectively kill plants. Herbicide resistance occurs usually as a result of mutation or amplification of a gene, e.g. 3-phosphoshikimate 1-carboxyvinyltransferase." []
468	UPK:0360	"Protein which, if defective, causes hereditary hemolytic anemia, a hereditary disease characterized by the premature destruction of red blood cells." []
469	UPK:0361	"Protein which, if defective, causes hereditary multiple exostoses (EXT). It is an autosomal dominant disease characterized by the formation of cartilage-capped benign tumors (exostoses), developing from the juxtaepiphyseal regions of the long bones and often accompanied by skeletal deformities and short stature." []
470	UPK:0362	"Protein which, if defective, causes hereditary non-polyposis colorectal cancer (HNPCC), also known as Lynch's syndrome. It is an autosomal dominant syndrome which confers an increased risk for colorectal and endometrial cancers as well as others tumors. Clinically, HNPCC is often divided into two subgroups: type I, characterized by a hereditary predisposition to colorectal cancer, a young age of onset, and carcinoma observed in the proximal colon; type II, characterized by an increased risk for cancers in certain tissues such as the uterus, ovary, breast, stomach, small intestine, skin, and larynx in addition to the colon." []
471	UPK:0890	"Protein which, if defective, causes hereditary spastic paraplegias (HSPs). HSPs are a diverse class of hereditary degenerative spinal cord disorders characterized by a slow, gradual, progressive weakness and spasticity (stiffness) of the legs. Initial symptoms may include difficulty with balance, weakness and stiffness in the legs, muscle spasms, and dragging the toes when walking. In some forms of the disorder, bladder symptoms (such as incontinence) may appear, or the weakness and stiffness may spread to other parts of the body. Rate of progression and the severity of symptoms are quite variable." []
472	UPK:0363	"Protein which, if defective, causes Hermansky-Pudlak syndrome, a rare autosomal recessive disorder characterized by oculocutaneous albinism and storage pool deficiency due to an absence of platelet dense bodies. Lysosomal ceroid lipofuscinosis, pulmonary fibrosis and granulomatous colitis are occasional manifestations of the disease." []
473	UPK:0364	"Protein which is implicated in heterocyst formation. A heterocyst is a differentiated cyanobacterial cell that carries out nitrogen fixation. The heterocysts function as the sites for nitrogen fixation under aerobic conditions. They are formed in response to a lack of fixed nitrogen (NH4 or NO3). The morphological differentiation is accompanied by biochemical alterations. The mature heterocysts contain no functional photosystem II and cannot produce oxygen. Instead, they contain only photosystem I, which enables them to carry out cyclic photophosphorylation and ATP regeneration. These changes provide the appropriate conditions for the functioning of the oxygen-sensitive nitrogenase." []
474	UPK:1056	"Protein which, if defective, causes heterotaxy, a broad group of disorders caused by failure to correctly establish left-right patterning during embryogenesis with consequent abnormal segmental arrangements of cardiac chambers, vessels, lungs, and/or abdominal organs. Heterotaxy include complex cardiac malformations, situs inversus, situs ambiguus, isomerism. Situs inversus indicates complete left-right reversal of organ position and is not usually associated with structural anomalies. Situs ambiguus is an abnormal arrangement of viscera almost invariably associated with complex cardiovascular malformations as well as anomalies of the spleen and the gastrointestinal system. Isomerism is a defect in asymmetry of paired organs that usually have distinct right and left forms, but in this condition, are mirror images." []
475	UPK:0909	"Protein involved in the process of hibernation. Hibernation is a state of inactivity in an animal brought about by short day lengths, cold temperatures and limitations of food." []
476	UPK:0367	"Hirschsprung's disease (HSCR); a genetic disorder of neural crest development characterized by the absence of intramural ganglion cells in the hindgut; often resulting in intestinal obstruction." []
477	UPK:0368	"Protein involved in the synthesis of the weakly basic amino acid histidine." []
478	UPK:0369	"Protein involved in the biochemical reactions with the weakly basic amino acid histidine." []
479	UPK:0370	"A clinically variable and genetically heterogeneous malformation in which the developing forebrain fails to correctly separate into right and left hemispheres. In its most severe form (alobar holoprosencephaly), the forebrain consists of a single ventricle, and midbrain structures may be malformed as well. In the most extreme cases, anophthalmia or cyclopia is evident along with a congenital absence of the mature nose. In milder forms (semilobar or lobar holoprosencephaly), rudimentary midline structures are present. The less severe form features facial dysmorphia characterized by ocular hypertelorism, defects of the upper lip and/or nose, and absence of the olfactory nerves or corpus callosum. The majority of cases are sporadic, although families with both autosomal dominant and autosomal recessive holoprosencephaly have been described." []
480	UPK:0371	"Protein which contains at least one homeobox, a conserved sequence originally detected, on the nucleotide level, in many of the genes which give rise to homeotic and segmentation mutants in Drosophila. The homeobox, also termed homeodomain, consists of about 60 amino acids and is involved in DNA-binding." []
481	UPK:0372	"Protein which functions as a hormone, a biochemical substance secreted by specialized cells that affects the metabolism or behavior of other cells which possess functional receptors for the hormone. Hormones may be hydrophilic, like insulin, in which case the receptors are on the cell surface, or lipophilic, like the steroids, where the receptor can be intracellular." []
482	UPK:1030	"Protein found in or associated with the prokaryotic host cell inner membrane, a selectively permeable membrane which separates the host cytoplasm from the host periplasm in prokaryotes with 2 membranes." []
483	UPK:1031	"Protein found in or associated with a host cell junction, a host cell-host cell or host cell-host extracellular matrix contact within a tissue of a host multicellular organism, especially abundant in host epithelia. In vertebrates, there are three major types of cell junctions: anchoring junctions (e.g. adherens junctions), communicating junctions (e.g. gap junctions) and occluding junctions (e.g. tight junctions)." []
484	UPK:0578	"Viral protein involved in the lysis of the host cell allowing the release of mature, newly formed virions. Viruses use different way to lyse their host cell. They can express viroporins as Adenoviridae or Picornaviridae do in the late phase of infection. Phycodnaviridae for their part seem to express lytic phospholipids. In dsDNA prokaryotic viruses, lysis-specific proteins are expressed: a holin, which permeabilizes the inner membrane and an endolysin which then gains access to and degrades the host peptidoglycans. Some bacterioviruses express a signal-containing endolysin and thus do not need the holin function." []
485	UPK:1032	"Protein found in or associated with the host cytoplasmic membrane, a selectively permeable membrane which separates the cytoplasm from its surroundings. Known as the host cell inner membrane in prokaryotes with 2 membranes." []
486	UPK:1033	"Protein found in or associated with the prokaryotic cell outer membrane, a selectively permeable membrane which separates the prokaryotic periplasm from its surroundings in prokaryotes with 2 membranes. Traditionally only Gram-negative bacteria were thought of as having an outer membrane, but recent work has shown some Actinobacteria, including Mycobacterium tuberculosis, as well as at least 1 archaea (Ignicoccus hospitalis) have a cell outer membrane." []
487	UPK:1034	"Protein found in or associated with a host cell projection, a host cell protrusion such as pseudopodium, filopodium, lamellipodium, growth cone, flagellum, acrosome, axon, pili or bacterial comet tail. These membrane-cytoskeleton-coupled processes are involved in many biological functions, such as host cell motility, cancer-cell invasion, endocytosis, phagocytosis, exocytosis, pathogen infection, neurite extension and cytokinesis." []
488	UPK:1183	"Cell surface protein used by a virus as an attachment and entry receptor. In some cases, binding to a cellular receptor is not sufficient for infection: an additional cell surface molecule, or coreceptor, is required for entry. Some viruses are able to use different receptors depending on the target cell type. In prokaryotic viruses, cell receptor for virus entry can also be localized on host outer membrane, pilus or flagellum." []
489	UPK:1035	"Protein found in the host cytoplasm, the content of a host cell within the plasma membrane and, in eukaryotics cells, surrounds the host nucleus." []
490	UPK:1036	"Protein found in or associated with host cytoplasmic vesicles, which mediate vesicular transport among the organelles of host secretory and endocytic systems." []
491	UPK:1037	"Protein which is a component or which is associated with the host cytoskeleton, a dynamic three-dimensional structure that fills the host cytoplasm of eukaryotic cells. It is responsible for cell movement, cytokinesis, and the organization of the organelles or organelle-like structures within the host cell." []
492	UPK:1038	"Protein whose subcellular location is the host endoplasmic reticulum (ER), which is an extensive network of membrane tubules, vesicles and flattened cisternae (sac-like structures) found throughout the eukaryotic host cell, especially those responsible for the production of hormones and other secretory products." []
493	UPK:1039	"Protein found in or associated with host endosomes, which are highly dynamic membrane systems involved in transport within the host cell, they receive endocytosed host cell membrane molecules and sort them for either degradation or recycling back to the host cell surface. They also receive newly synthesised proteins destined for host vacuolar/lysosomal compartments." []
494	UPK:1079	"Viral protein involved in the modulation of host cell cycle by inhibiting the G2/M transition. A variety of viruses have been associated with G2/M arrest, including some DNA viruses, some RNA viruses and retroviruses but the mechanisms by which arrest is achieved greatly differs between those viruses." []
495	UPK:1190	"Viral protein which prevents host gene expression by blocking for example host transcription, mRNA export or translation. This gives virus transcripts a competitive edge to use the hijacked translation machinery. Preventing the expression of host proteins is also a strategy to counteract the antiviral response." []
496	UPK:1040	"Protein found in the host Golgi apparatus, a series of flattened, cisternal membranes and similar vesicles usually arranged in close apposition to each other to form stacks. In mammalian cells, the host Golgi apparatus is juxtanuclear, often pericentriolar. The stacks are connected laterally by tubules to create a perinuclear ribbon structure, the 'Golgi ribbon'. In plants and lower animal cells, the host Golgi exists as many copies of discrete stacks dispersed throughout the host cytoplasm. It is a polarized structure with, in most higher eukaryotic cells, a cis-face associated with a tubular reticular network of membranes facing the endoplasmic reticulum, the cis-Golgi network (CGN), a medial area of disk-shaped flattened cisternae, and a trans-face associated with another tubular reticular membrane network, the trans-Golgi network (TGN) directed toward the host plasma membrane and compartments of the host endocytic pathway." []
497	UPK:1041	"Protein characteristic of host lipid droplet, a dynamic cytoplasmic host organelle which consists of an heterogeneous macromolecular assembly of lipids and proteins covered by a unique phospholipid monolayer. They may play a role in host lipid metabolism and storage, and they may be involved in the regulation of intracellular trafficking and signal transduction." []
498	UPK:1042	"Protein found in the host lysosome, a membrane-limited organelle present in all eukaryotic cells, which contains a large number of hydrolytic enzymes that are used for degrading almost any kind of cellular constituent, including entire organelles. The mechanisms responsible for delivering cytoplasmic cargo to the host lysosome/vacuole are known collectively as autophagy and play an important role in the maintenance of homeostasis." []
499	UPK:1043	"Protein which is membrane-bound or membrane-associated with the host membrane, a lipid bilayer which surrounds host enclosed spaces and compartments. This selectively permeable structure is essential for effective separation of a host cell or organelle from its surroundings." []
500	UPK:1044	"Protein found in host microsomes, which are a heterogenous set of vesicles 20-200 nm in diameter and formed from the host endoplasmic reticulum when host cells are disrupted." []
\.


--
-- Name: function_2_definition_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dblyon
--

SELECT pg_catalog.setval('function_2_definition_id_seq', 1, false);


--
-- Data for Name: functions; Type: TABLE DATA; Schema: public; Owner: dblyon
--

COPY functions (id, type, name, an) FROM stdin;
1	GO	mitochondrion inheritance	GO:0000001
2	GO	mitochondrial genome maintenance	GO:0000002
3	GO	reproduction	GO:0000003
4	GO	obsolete ribosomal chaperone activity	GO:0000005
5	GO	high-affinity zinc uptake transmembrane transporter activity	GO:0000006
6	GO	low-affinity zinc ion transmembrane transporter activity	GO:0000007
7	GO	obsolete thioredoxin	GO:0000008
8	GO	alpha-1,6-mannosyltransferase activity	GO:0000009
9	GO	trans-hexaprenyltranstransferase activity	GO:0000010
10	GO	vacuole inheritance	GO:0000011
11	GO	single strand break repair	GO:0000012
12	GO	single-stranded DNA endodeoxyribonuclease activity	GO:0000014
13	GO	phosphopyruvate hydratase complex	GO:0000015
14	GO	lactase activity	GO:0000016
15	GO	alpha-glucoside transport	GO:0000017
16	GO	regulation of DNA recombination	GO:0000018
17	GO	regulation of mitotic recombination	GO:0000019
18	GO	obsolete negative regulation of recombination within rDNA repeats	GO:0000020
19	GO	mitotic spindle elongation	GO:0000022
20	GO	maltose metabolic process	GO:0000023
21	GO	maltose biosynthetic process	GO:0000024
22	GO	maltose catabolic process	GO:0000025
23	GO	alpha-1,2-mannosyltransferase activity	GO:0000026
24	GO	ribosomal large subunit assembly	GO:0000027
25	GO	ribosomal small subunit assembly	GO:0000028
26	GO	mannosyltransferase activity	GO:0000030
27	GO	mannosylphosphate transferase activity	GO:0000031
28	GO	cell wall mannoprotein biosynthetic process	GO:0000032
29	GO	alpha-1,3-mannosyltransferase activity	GO:0000033
30	GO	adenine deaminase activity	GO:0000034
31	GO	acyl binding	GO:0000035
32	GO	ACP phosphopantetheine attachment site binding involved in fatty acid biosynthetic process	GO:0000036
33	GO	very long-chain fatty acid metabolic process	GO:0000038
34	GO	obsolete plasma membrane long-chain fatty acid transporter	GO:0000039
35	GO	low-affinity iron ion transmembrane transport	GO:0000040
36	GO	transition metal ion transport	GO:0000041
37	GO	protein targeting to Golgi	GO:0000042
38	GO	obsolete ascorbate stabilization	GO:0000044
39	GO	autophagosome assembly	GO:0000045
40	GO	obsolete Rieske iron-sulfur protein	GO:0000047
41	GO	peptidyltransferase activity	GO:0000048
42	GO	tRNA binding	GO:0000049
43	GO	urea cycle	GO:0000050
44	GO	obsolete urea cycle intermediate metabolic process	GO:0000051
45	GO	citrulline metabolic process	GO:0000052
46	GO	argininosuccinate metabolic process	GO:0000053
47	GO	ribosomal subunit export from nucleus	GO:0000054
48	GO	ribosomal large subunit export from nucleus	GO:0000055
49	GO	ribosomal small subunit export from nucleus	GO:0000056
50	GO	protein import into nucleus, docking	GO:0000059
51	GO	protein import into nucleus, translocation	GO:0000060
52	GO	protein import into nucleus, substrate release	GO:0000061
53	GO	fatty-acyl-CoA binding	GO:0000062
54	GO	L-ornithine transmembrane transporter activity	GO:0000064
55	GO	mitochondrial ornithine transport	GO:0000066
56	GO	obsolete DNA replication and chromosome cycle	GO:0000067
57	GO	mitotic sister chromatid segregation	GO:0000070
58	GO	obsolete M phase specific microtubule process	GO:0000072
59	GO	spindle pole body separation	GO:0000073
60	GO	cell cycle checkpoint	GO:0000075
61	GO	DNA replication checkpoint	GO:0000076
62	GO	DNA damage checkpoint	GO:0000077
63	GO	obsolete cytokinesis after mitosis checkpoint	GO:0000078
64	GO	regulation of cyclin-dependent protein serine/threonine kinase activity	GO:0000079
65	GO	mitotic G1 phase	GO:0000080
66	GO	G1/S transition of mitotic cell cycle	GO:0000082
67	GO	regulation of transcription involved in G1/S transition of mitotic cell cycle	GO:0000083
68	GO	mitotic S phase	GO:0000084
69	GO	mitotic G2 phase	GO:0000085
70	GO	G2/M transition of mitotic cell cycle	GO:0000086
71	GO	mitotic M phase	GO:0000087
72	GO	mitotic prophase	GO:0000088
73	GO	mitotic metaphase	GO:0000089
74	GO	mitotic anaphase	GO:0000090
75	GO	mitotic anaphase A	GO:0000091
76	GO	mitotic anaphase B	GO:0000092
77	GO	mitotic telophase	GO:0000093
78	GO	obsolete septin assembly and septum formation	GO:0000094
79	GO	S-adenosyl-L-methionine transmembrane transporter activity	GO:0000095
80	GO	sulfur amino acid metabolic process	GO:0000096
81	GO	sulfur amino acid biosynthetic process	GO:0000097
82	GO	sulfur amino acid catabolic process	GO:0000098
83	GO	sulfur amino acid transmembrane transporter activity	GO:0000099
84	GO	S-methylmethionine transmembrane transporter activity	GO:0000100
85	GO	sulfur amino acid transport	GO:0000101
86	GO	L-methionine secondary active transmembrane transporter activity	GO:0000102
87	GO	sulfate assimilation	GO:0000103
88	GO	succinate dehydrogenase activity	GO:0000104
89	GO	histidine biosynthetic process	GO:0000105
90	GO	imidazoleglycerol-phosphate synthase activity	GO:0000107
91	GO	obsolete repairosome	GO:0000108
92	GO	nucleotide-excision repair complex	GO:0000109
93	GO	nucleotide-excision repair factor 1 complex	GO:0000110
94	GO	nucleotide-excision repair factor 2 complex	GO:0000111
95	GO	nucleotide-excision repair factor 3 complex	GO:0000112
96	GO	nucleotide-excision repair factor 4 complex	GO:0000113
97	GO	obsolete regulation of transcription involved in G1 phase of mitotic cell cycle	GO:0000114
98	GO	obsolete regulation of transcription involved in S phase of mitotic cell cycle	GO:0000115
99	GO	obsolete regulation of transcription involved in G2-phase of mitotic cell cycle	GO:0000116
100	GO	regulation of transcription involved in G2/M transition of mitotic cell cycle	GO:0000117
101	GO	histone deacetylase complex	GO:0000118
102	GO	RNA polymerase I transcription factor complex	GO:0000120
103	GO	glycerol-1-phosphatase activity	GO:0000121
104	GO	negative regulation of transcription from RNA polymerase II promoter	GO:0000122
105	GO	histone acetyltransferase complex	GO:0000123
106	GO	SAGA complex	GO:0000124
107	GO	PCAF complex	GO:0000125
108	GO	transcription factor TFIIIB complex	GO:0000126
109	GO	transcription factor TFIIIC complex	GO:0000127
110	GO	flocculation	GO:0000128
111	GO	incipient cellular bud site	GO:0000131
112	GO	establishment of mitotic spindle orientation	GO:0000132
113	GO	polarisome	GO:0000133
114	GO	alpha-1,6-mannosyltransferase complex	GO:0000136
115	GO	Golgi cis cisterna	GO:0000137
116	GO	Golgi trans cisterna	GO:0000138
117	GO	Golgi membrane	GO:0000139
118	GO	acylglycerone-phosphate reductase activity	GO:0000140
119	GO	cellular bud neck contractile ring	GO:0000142
120	GO	cellular bud neck septin ring	GO:0000144
121	GO	exocyst	GO:0000145
122	GO	microfilament motor activity	GO:0000146
123	GO	actin cortical patch assembly	GO:0000147
124	GO	1,3-beta-D-glucan synthase complex	GO:0000148
125	GO	SNARE binding	GO:0000149
126	GO	recombinase activity	GO:0000150
127	GO	ubiquitin ligase complex	GO:0000151
128	GO	nuclear ubiquitin ligase complex	GO:0000152
129	GO	cytoplasmic ubiquitin ligase complex	GO:0000153
130	GO	rRNA modification	GO:0000154
131	GO	phosphorelay sensor kinase activity	GO:0000155
132	GO	phosphorelay response regulator activity	GO:0000156
133	GO	protein phosphatase type 2A complex	GO:0000159
134	GO	phosphorelay signal transduction system	GO:0000160
135	GO	MAPK cascade involved in osmosensory signaling pathway	GO:0000161
136	GO	tryptophan biosynthetic process	GO:0000162
137	GO	protein phosphatase type 1 complex	GO:0000164
138	GO	MAPK cascade	GO:0000165
139	GO	nucleotide binding	GO:0000166
140	GO	activation of MAPKKK activity involved in osmosensory signaling pathway	GO:0000167
141	GO	activation of MAPKK activity involved in osmosensory signaling pathway	GO:0000168
142	GO	activation of MAPK activity involved in osmosensory signaling pathway	GO:0000169
143	GO	sphingosine hydroxylase activity	GO:0000170
144	GO	ribonuclease MRP activity	GO:0000171
145	GO	ribonuclease MRP complex	GO:0000172
146	GO	inactivation of MAPK activity involved in osmosensory signaling pathway	GO:0000173
147	GO	obsolete inactivation of MAPK (mating sensu Saccharomyces)	GO:0000174
148	GO	3'-5'-exoribonuclease activity	GO:0000175
149	GO	nuclear exosome (RNase complex)	GO:0000176
150	GO	cytoplasmic exosome (RNase complex)	GO:0000177
151	GO	exosome (RNase complex)	GO:0000178
152	GO	rRNA (adenine-N6,N6-)-dimethyltransferase activity	GO:0000179
153	GO	obsolete cytosolic large ribosomal subunit	GO:0000180
154	GO	obsolete cytosolic small ribosomal subunit	GO:0000181
155	GO	rDNA binding	GO:0000182
156	GO	chromatin silencing at rDNA	GO:0000183
157	GO	nuclear-transcribed mRNA catabolic process, nonsense-mediated decay	GO:0000184
158	GO	activation of MAPKKK activity	GO:0000185
159	GO	activation of MAPKK activity	GO:0000186
160	GO	activation of MAPK activity	GO:0000187
161	GO	inactivation of MAPK activity	GO:0000188
162	GO	MAPK import into nucleus	GO:0000189
163	GO	obsolete MAPKKK cascade (pseudohyphal growth)	GO:0000190
164	GO	obsolete activation of MAPKKK (pseudohyphal growth)	GO:0000191
165	GO	obsolete activation of MAPKK (pseudohyphal growth)	GO:0000192
166	GO	obsolete activation of MAPK (pseudohyphal growth)	GO:0000193
167	GO	obsolete inactivation of MAPK (pseudohyphal growth)	GO:0000194
168	GO	obsolete nuclear translocation of MAPK (pseudohyphal growth)	GO:0000195
169	GO	MAPK cascade involved in cell wall organization or biogenesis	GO:0000196
170	GO	activation of MAPKKK activity involved in cell wall organization or biogenesis	GO:0000197
171	GO	activation of MAPKK activity involved in cell wall organization or biogenesis	GO:0000198
172	GO	activation of MAPK activity involved in cell wall organization or biogenesis	GO:0000199
173	GO	inactivation of MAPK activity involved in cell wall organization or biogenesis	GO:0000200
174	GO	MAPK import into nucleus involved in cell wall organization or biogenesis	GO:0000201
175	GO	obsolete MAPKKK cascade during sporulation (sensu Saccharomyces)	GO:0000202
176	GO	obsolete activation of MAPKKK during sporulation (sensu Saccharomyces)	GO:0000203
177	GO	obsolete activation of MAPKK during sporulation (sensu Saccharomyces)	GO:0000204
178	GO	obsolete activation of MAPK during sporulation (sensu Saccharomyces)	GO:0000205
179	GO	obsolete inactivation of MAPK during sporulation (sensu Saccharomyces)	GO:0000206
180	GO	obsolete nuclear translocation of MAPK during sporulation (sensu Saccharomyces)	GO:0000207
181	GO	MAPK import into nucleus involved in osmosensory signaling pathway	GO:0000208
182	GO	protein polyubiquitination	GO:0000209
183	GO	NAD+ diphosphatase activity	GO:0000210
184	GO	obsolete protein degradation tagging activity	GO:0000211
185	GO	meiotic spindle organization	GO:0000212
186	GO	tRNA-intron endonuclease activity	GO:0000213
187	GO	tRNA-intron endonuclease complex	GO:0000214
188	GO	tRNA 2'-phosphotransferase activity	GO:0000215
189	GO	obsolete M/G1 transition of mitotic cell cycle	GO:0000216
190	GO	DNA secondary structure binding	GO:0000217
191	GO	obsolete vacuolar hydrogen-transporting ATPase	GO:0000219
192	GO	vacuolar proton-transporting V-type ATPase, V0 domain	GO:0000220
193	GO	vacuolar proton-transporting V-type ATPase, V1 domain	GO:0000221
194	GO	plasma membrane proton-transporting V-type ATPase, V0 domain	GO:0000222
195	GO	plasma membrane proton-transporting V-type ATPase, V1 domain	GO:0000223
196	GO	peptide-N4-(N-acetyl-beta-glucosaminyl)asparagine amidase activity	GO:0000224
197	GO	N-acetylglucosaminylphosphatidylinositol deacetylase activity	GO:0000225
198	GO	microtubule cytoskeleton organization	GO:0000226
199	GO	oxaloacetate secondary active transmembrane transporter activity	GO:0000227
200	GO	nuclear chromosome	GO:0000228
201	GO	cytoplasmic chromosome	GO:0000229
202	GO	obsolete nuclear mitotic chromosome	GO:0000230
203	GO	obsolete cytoplasmic mitotic chromosome	GO:0000231
204	GO	obsolete nuclear interphase chromosome	GO:0000232
205	GO	obsolete cytoplasmic interphase chromosome	GO:0000233
206	GO	phosphoethanolamine N-methyltransferase activity	GO:0000234
207	GO	astral microtubule	GO:0000235
208	GO	mitotic prometaphase	GO:0000236
209	GO	leptotene	GO:0000237
210	GO	zygotene	GO:0000238
211	GO	pachytene	GO:0000239
212	GO	diplotene	GO:0000240
213	GO	diakinesis	GO:0000241
214	GO	pericentriolar material	GO:0000242
215	GO	commitment complex	GO:0000243
216	GO	spliceosomal tri-snRNP complex assembly	GO:0000244
217	GO	spliceosomal complex assembly	GO:0000245
218	GO	delta24(24-1) sterol reductase activity	GO:0000246
219	GO	C-8 sterol isomerase activity	GO:0000247
220	GO	C-5 sterol desaturase activity	GO:0000248
221	GO	C-22 sterol desaturase activity	GO:0000249
222	GO	lanosterol synthase activity	GO:0000250
223	GO	C-3 sterol dehydrogenase (C-4 sterol decarboxylase) activity	GO:0000252
224	GO	3-keto sterol reductase activity	GO:0000253
225	GO	C-4 methylsterol oxidase activity	GO:0000254
226	GO	allantoin metabolic process	GO:0000255
227	GO	allantoin catabolic process	GO:0000256
228	GO	nitrilase activity	GO:0000257
229	GO	obsolete isoleucine/valine:sodium symporter activity	GO:0000258
230	GO	obsolete intracellular nucleoside transmembrane transporter activity	GO:0000259
231	GO	obsolete hydrogen-translocating V-type ATPase activity	GO:0000260
232	GO	obsolete sodium-translocating V-type ATPase activity	GO:0000261
233	GO	mitochondrial chromosome	GO:0000262
234	GO	obsolete heterotrimeric G-protein GTPase, alpha-subunit	GO:0000263
235	GO	obsolete heterotrimeric G-protein GTPase, beta-subunit	GO:0000264
236	GO	obsolete heterotrimeric G-protein GTPase, gamma-subunit	GO:0000265
237	GO	mitochondrial fission	GO:0000266
238	GO	obsolete cell fraction	GO:0000267
239	GO	peroxisome targeting sequence binding	GO:0000268
240	GO	toxin export channel activity	GO:0000269
241	GO	peptidoglycan metabolic process	GO:0000270
242	GO	polysaccharide biosynthetic process	GO:0000271
243	GO	polysaccharide catabolic process	GO:0000272
244	GO	mitochondrial proton-transporting ATP synthase, stator stalk	GO:0000274
245	GO	mitochondrial proton-transporting ATP synthase complex, catalytic core F(1)	GO:0000275
246	GO	mitochondrial proton-transporting ATP synthase complex, coupling factor F(o)	GO:0000276
247	GO	[cytochrome c]-lysine N-methyltransferase activity	GO:0000277
248	GO	mitotic cell cycle	GO:0000278
249	GO	M phase	GO:0000279
250	GO	nuclear division	GO:0000280
251	GO	mitotic cytokinesis	GO:0000281
252	GO	cellular bud site selection	GO:0000282
253	GO	obsolete shmoo orientation	GO:0000284
254	GO	1-phosphatidylinositol-3-phosphate 5-kinase activity	GO:0000285
255	GO	alanine dehydrogenase activity	GO:0000286
256	GO	magnesium ion binding	GO:0000287
257	GO	nuclear-transcribed mRNA catabolic process, deadenylation-dependent decay	GO:0000288
258	GO	nuclear-transcribed mRNA poly(A) tail shortening	GO:0000289
259	GO	deadenylation-dependent decapping of nuclear-transcribed mRNA	GO:0000290
260	GO	nuclear-transcribed mRNA catabolic process, exonucleolytic	GO:0000291
261	GO	RNA fragment catabolic process	GO:0000292
262	GO	ferric-chelate reductase activity	GO:0000293
263	GO	nuclear-transcribed mRNA catabolic process, endonucleolytic cleavage-dependent decay	GO:0000294
264	GO	adenine nucleotide transmembrane transporter activity	GO:0000295
265	GO	spermine transport	GO:0000296
266	GO	spermine transmembrane transporter activity	GO:0000297
267	GO	endopolyphosphatase activity	GO:0000298
268	GO	obsolete integral to membrane of membrane fraction	GO:0000299
269	GO	obsolete peripheral to membrane of membrane fraction	GO:0000300
270	GO	retrograde transport, vesicle recycling within Golgi	GO:0000301
271	GO	response to reactive oxygen species	GO:0000302
272	GO	response to superoxide	GO:0000303
273	GO	response to singlet oxygen	GO:0000304
274	GO	response to oxygen radical	GO:0000305
275	GO	extrinsic component of vacuolar membrane	GO:0000306
276	GO	cyclin-dependent protein kinase holoenzyme complex	GO:0000307
277	GO	cytoplasmic cyclin-dependent protein kinase holoenzyme complex	GO:0000308
278	GO	nicotinamide-nucleotide adenylyltransferase activity	GO:0000309
279	GO	xanthine phosphoribosyltransferase activity	GO:0000310
280	GO	plastid large ribosomal subunit	GO:0000311
281	GO	plastid small ribosomal subunit	GO:0000312
282	GO	organellar ribosome	GO:0000313
283	GO	organellar small ribosomal subunit	GO:0000314
284	GO	organellar large ribosomal subunit	GO:0000315
285	GO	sulfite transport	GO:0000316
286	GO	sulfite transmembrane transporter activity	GO:0000319
287	GO	re-entry into mitotic cell cycle	GO:0000320
288	GO	re-entry into mitotic cell cycle after pheromone arrest	GO:0000321
289	GO	storage vacuole	GO:0000322
290	GO	lytic vacuole	GO:0000323
291	GO	fungal-type vacuole	GO:0000324
292	GO	plant-type vacuole	GO:0000325
293	GO	protein storage vacuole	GO:0000326
294	GO	lytic vacuole within protein storage vacuole	GO:0000327
295	GO	fungal-type vacuole lumen	GO:0000328
296	GO	fungal-type vacuole membrane	GO:0000329
297	GO	plant-type vacuole lumen	GO:0000330
298	GO	contractile vacuole	GO:0000331
299	GO	template for synthesis of G-rich strand of telomere DNA activity	GO:0000332
300	GO	telomerase catalytic core complex	GO:0000333
301	GO	3-hydroxyanthranilate 3,4-dioxygenase activity	GO:0000334
302	GO	negative regulation of transposition, DNA-mediated	GO:0000335
303	GO	positive regulation of transposition, DNA-mediated	GO:0000336
304	GO	regulation of transposition, DNA-mediated	GO:0000337
305	GO	protein deneddylation	GO:0000338
306	GO	RNA cap binding	GO:0000339
307	GO	RNA 7-methylguanosine cap binding	GO:0000340
308	GO	RNA trimethylguanosine cap binding	GO:0000341
309	GO	RNA cap 4 binding	GO:0000342
310	GO	plastid-encoded plastid RNA polymerase complex A	GO:0000343
311	GO	plastid-encoded plastid RNA polymerase complex B	GO:0000344
312	GO	cytosolic DNA-directed RNA polymerase complex	GO:0000345
313	GO	transcription export complex	GO:0000346
314	GO	THO complex	GO:0000347
315	GO	mRNA branch site recognition	GO:0000348
316	GO	generation of catalytic spliceosome for first transesterification step	GO:0000349
317	GO	generation of catalytic spliceosome for second transesterification step	GO:0000350
318	GO	trans assembly of SL-containing precatalytic spliceosome	GO:0000352
319	GO	formation of quadruple SL/U4/U5/U6 snRNP	GO:0000353
320	GO	cis assembly of pre-catalytic spliceosome	GO:0000354
321	GO	obsolete first U2-type spliceosomal transesterification activity	GO:0000362
322	GO	obsolete first U12-type spliceosomal transesterification activity	GO:0000363
323	GO	obsolete second U2-type spliceosomal transesterification activity	GO:0000364
324	GO	mRNA trans splicing, via spliceosome	GO:0000365
325	GO	intergenic mRNA trans splicing	GO:0000366
326	GO	obsolete second U12-type spliceosomal transesterification activity	GO:0000367
327	GO	Group I intron splicing	GO:0000372
328	GO	Group II intron splicing	GO:0000373
329	GO	Group III intron splicing	GO:0000374
330	GO	RNA splicing, via transesterification reactions	GO:0000375
331	GO	RNA splicing, via transesterification reactions with guanosine as nucleophile	GO:0000376
332	GO	RNA splicing, via transesterification reactions with bulged adenosine as nucleophile	GO:0000377
333	GO	RNA exon ligation	GO:0000378
334	GO	tRNA-type intron splice site recognition and cleavage	GO:0000379
335	GO	alternative mRNA splicing, via spliceosome	GO:0000380
336	GO	regulation of alternative mRNA splicing, via spliceosome	GO:0000381
337	GO	first spliceosomal transesterification activity	GO:0000384
338	GO	second spliceosomal transesterification activity	GO:0000386
339	GO	spliceosomal snRNP assembly	GO:0000387
340	GO	spliceosome conformational change to release U4 (or U4atac) and U1 (or U11)	GO:0000388
341	GO	mRNA 3'-splice site recognition	GO:0000389
342	GO	spliceosomal complex disassembly	GO:0000390
343	GO	spliceosomal conformational changes to generate catalytic conformation	GO:0000393
344	GO	RNA splicing, via endonucleolytic cleavage and ligation	GO:0000394
345	GO	mRNA 5'-splice site recognition	GO:0000395
346	GO	mRNA splicing, via spliceosome	GO:0000398
347	GO	cellular bud neck septin structure	GO:0000399
348	GO	four-way junction DNA binding	GO:0000400
349	GO	open form four-way junction DNA binding	GO:0000401
350	GO	crossed form four-way junction DNA binding	GO:0000402
351	GO	Y-form DNA binding	GO:0000403
352	GO	heteroduplex DNA loop binding	GO:0000404
353	GO	bubble DNA binding	GO:0000405
354	GO	double-strand/single-strand DNA junction binding	GO:0000406
355	GO	pre-autophagosomal structure	GO:0000407
356	GO	EKC/KEOPS complex	GO:0000408
357	GO	regulation of transcription by galactose	GO:0000409
358	GO	negative regulation of transcription by galactose	GO:0000410
359	GO	positive regulation of transcription by galactose	GO:0000411
360	GO	histone peptidyl-prolyl isomerization	GO:0000412
361	GO	protein peptidyl-prolyl isomerization	GO:0000413
362	GO	regulation of histone H3-K36 methylation	GO:0000414
363	GO	negative regulation of histone H3-K36 methylation	GO:0000415
364	GO	positive regulation of histone H3-K36 methylation	GO:0000416
365	GO	HIR complex	GO:0000417
366	GO	DNA-directed RNA polymerase IV complex	GO:0000418
367	GO	DNA-directed RNA polymerase V complex	GO:0000419
368	GO	autophagosome membrane	GO:0000421
369	GO	mitophagy	GO:0000422
370	GO	macromitophagy	GO:0000423
371	GO	microautophagy of mitochondrion	GO:0000424
372	GO	macropexophagy	GO:0000425
373	GO	micropexophagy	GO:0000426
374	GO	plastid-encoded plastid RNA polymerase complex	GO:0000427
375	GO	DNA-directed RNA polymerase complex	GO:0000428
376	GO	carbon catabolite regulation of transcription from RNA polymerase II promoter	GO:0000429
377	GO	regulation of transcription from RNA polymerase II promoter by glucose	GO:0000430
378	GO	regulation of transcription from RNA polymerase II promoter by galactose	GO:0000431
379	GO	positive regulation of transcription from RNA polymerase II promoter by glucose	GO:0000432
380	GO	negative regulation of transcription from RNA polymerase II promoter by glucose	GO:0000433
381	GO	negative regulation of transcription from RNA polymerase II promoter by galactose	GO:0000434
382	GO	positive regulation of transcription from RNA polymerase II promoter by galactose	GO:0000435
383	GO	carbon catabolite activation of transcription from RNA polymerase II promoter	GO:0000436
384	GO	carbon catabolite repression of transcription from RNA polymerase II promoter	GO:0000437
385	GO	core TFIIH complex portion of holo TFIIH complex	GO:0000438
386	GO	core TFIIH complex	GO:0000439
387	GO	core TFIIH complex portion of NEF3 complex	GO:0000440
388	GO	MIS12/MIND type complex	GO:0000444
389	GO	THO complex part of transcription export complex	GO:0000445
390	GO	nucleoplasmic THO complex	GO:0000446
391	GO	endonucleolytic cleavage in ITS1 to separate SSU-rRNA from 5.8S rRNA and LSU-rRNA from tricistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, LSU-rRNA)	GO:0000447
392	GO	cleavage in ITS2 between 5.8S rRNA and LSU-rRNA of tricistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, LSU-rRNA)	GO:0000448
393	GO	endonucleolytic cleavage of tricistronic rRNA transcript (SSU-rRNA, LSU-rRNA, 5S)	GO:0000449
394	GO	cleavage of bicistronic rRNA transcript (SSU-rRNA, LSU-rRNA)	GO:0000450
395	GO	rRNA 2'-O-methylation	GO:0000451
396	GO	snoRNA guided rRNA 2'-O-methylation	GO:0000452
397	GO	enzyme-directed rRNA 2'-O-methylation	GO:0000453
398	GO	snoRNA guided rRNA pseudouridine synthesis	GO:0000454
399	GO	enzyme-directed rRNA pseudouridine synthesis	GO:0000455
400	GO	dimethylation involved in SSU-rRNA maturation	GO:0000456
401	GO	endonucleolytic cleavage between SSU-rRNA and LSU-rRNA of tricistronic rRNA transcript (SSU-rRNA, LSU-rRNA, 5S)	GO:0000457
402	GO	endonucleolytic cleavage between LSU-rRNA and 5S rRNA of tricistronic rRNA transcript (SSU-rRNA, LSU-rRNA, 5S)	GO:0000458
403	GO	exonucleolytic trimming involved in rRNA processing	GO:0000459
404	GO	maturation of 5.8S rRNA	GO:0000460
405	GO	endonucleolytic cleavage to generate mature 3'-end of SSU-rRNA from (SSU-rRNA, 5.8S rRNA, LSU-rRNA)	GO:0000461
406	GO	maturation of SSU-rRNA from tricistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, LSU-rRNA)	GO:0000462
407	GO	maturation of LSU-rRNA from tricistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, LSU-rRNA)	GO:0000463
408	GO	endonucleolytic cleavage in ITS1 upstream of 5.8S rRNA from tricistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, LSU-rRNA)	GO:0000464
409	GO	exonucleolytic trimming to generate mature 5'-end of 5.8S rRNA from tricistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, LSU-rRNA)	GO:0000465
410	GO	maturation of 5.8S rRNA from tricistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, LSU-rRNA)	GO:0000466
411	GO	exonucleolytic trimming to generate mature 3'-end of 5.8S rRNA from tricistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, LSU-rRNA)	GO:0000467
412	GO	generation of mature 3'-end of LSU-rRNA from tricistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, LSU-rRNA)	GO:0000468
413	GO	cleavage involved in rRNA processing	GO:0000469
414	GO	maturation of LSU-rRNA	GO:0000470
415	GO	endonucleolytic cleavage in 3'-ETS of tricistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, LSU-rRNA)	GO:0000471
416	GO	endonucleolytic cleavage to generate mature 5'-end of SSU-rRNA from (SSU-rRNA, 5.8S rRNA, LSU-rRNA)	GO:0000472
417	GO	maturation of LSU-rRNA from tetracistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, 2S rRNA, LSU-rRNA)	GO:0000473
418	GO	maturation of SSU-rRNA from tetracistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, 2S rRNA, LSU-rRNA)	GO:0000474
419	GO	maturation of 2S rRNA	GO:0000475
420	GO	maturation of 4.5S rRNA	GO:0000476
421	GO	generation of mature 5'-end of LSU-rRNA from tricistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, LSU-rRNA)	GO:0000477
422	GO	endonucleolytic cleavage involved in rRNA processing	GO:0000478
423	GO	endonucleolytic cleavage of tricistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, LSU-rRNA)	GO:0000479
424	GO	endonucleolytic cleavage in 5'-ETS of tricistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, LSU-rRNA)	GO:0000480
425	GO	maturation of 5S rRNA	GO:0000481
426	GO	maturation of 5S rRNA from tetracistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, LSU-rRNA)	GO:0000482
427	GO	endonucleolytic cleavage of tetracistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, 2S rRNA, LSU-rRNA)	GO:0000483
428	GO	cleavage between SSU-rRNA and 5.8S rRNA of tetracistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, 2S rRNA, LSU-rRNA)	GO:0000484
429	GO	cleavage between 2S rRNA and LSU-rRNA of tetracistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, 2S rRNA, LSU-rRNA)	GO:0000485
430	GO	cleavage between 5.8S rRNA and 2S rRNA of tetracistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, 2S rRNA, LSU-rRNA)	GO:0000486
431	GO	maturation of 5.8S rRNA from tetracistronic rRNA transcript (SSU-rRNA, 5.8S rRNA, 2S rRNA, LSU-rRNA)	GO:0000487
432	GO	maturation of LSU-rRNA from tetracistronic rRNA transcript (SSU-rRNA, LSU-rRNA, 4.5S-rRNA, 5S-rRNA)	GO:0000488
433	GO	maturation of SSU-rRNA from tetracistronic rRNA transcript (SSU-rRNA, LSU-rRNA, 4.5S-rRNA, 5S-rRNA)	GO:0000489
434	GO	small nucleolar ribonucleoprotein complex assembly	GO:0000491
435	GO	box C/D snoRNP assembly	GO:0000492
436	GO	box H/ACA snoRNP assembly	GO:0000493
437	GO	box C/D snoRNA 3'-end processing	GO:0000494
438	GO	box H/ACA snoRNA 3'-end processing	GO:0000495
439	GO	base pairing	GO:0000496
440	GO	base pairing with DNA	GO:0000497
441	GO	base pairing with RNA	GO:0000498
442	GO	base pairing with mRNA	GO:0000499
443	GO	RNA polymerase I upstream activating factor complex	GO:0000500
444	GO	flocculation via cell wall protein-carbohydrate interaction	GO:0000501
445	GO	proteasome complex	GO:0000502
446	GO	obsolete proteasome regulatory particle (sensu Bacteria)	GO:0000504
447	GO	glycosylphosphatidylinositol-N-acetylglucosaminyltransferase (GPI-GnT) complex	GO:0000506
448	GO	embryonic axis specification	GO:0000578
449	GO	mismatch base pair DNA N-glycosylase activity	GO:0000700
450	GO	purine-specific mismatch base pair DNA N-glycosylase activity	GO:0000701
451	GO	oxidized base lesion DNA N-glycosylase activity	GO:0000702
452	GO	oxidized pyrimidine nucleobase lesion DNA N-glycosylase activity	GO:0000703
453	GO	pyrimidine dimer DNA N-glycosylase activity	GO:0000704
454	GO	achiasmate meiosis I	GO:0000705
455	GO	meiotic DNA double-strand break processing	GO:0000706
456	GO	meiotic DNA recombinase assembly	GO:0000707
457	GO	meiotic strand invasion	GO:0000708
458	GO	meiotic joint molecule formation	GO:0000709
459	GO	meiotic mismatch repair	GO:0000710
460	GO	meiotic DNA repair synthesis	GO:0000711
461	GO	resolution of meiotic recombination intermediates	GO:0000712
462	GO	meiotic heteroduplex formation	GO:0000713
463	GO	meiotic strand displacement	GO:0000714
464	GO	nucleotide-excision repair, DNA damage recognition	GO:0000715
465	GO	transcription-coupled nucleotide-excision repair, DNA damage recognition	GO:0000716
466	GO	nucleotide-excision repair, DNA duplex unwinding	GO:0000717
467	GO	nucleotide-excision repair, DNA damage removal	GO:0000718
468	GO	photoreactive repair	GO:0000719
469	GO	pyrimidine dimer repair by nucleotide-excision repair	GO:0000720
470	GO	(R,R)-butanediol dehydrogenase activity	GO:0000721
471	GO	telomere maintenance via recombination	GO:0000722
472	GO	telomere maintenance	GO:0000723
473	GO	double-strand break repair via homologous recombination	GO:0000724
474	GO	recombinational repair	GO:0000725
475	GO	non-recombinational repair	GO:0000726
476	GO	double-strand break repair via break-induced replication	GO:0000727
477	GO	gene conversion at mating-type locus, DNA double-strand break formation	GO:0000728
478	GO	DNA double-strand break processing	GO:0000729
479	GO	DNA recombinase assembly	GO:0000730
480	GO	DNA synthesis involved in DNA repair	GO:0000731
481	GO	strand displacement	GO:0000732
482	GO	DNA strand renaturation	GO:0000733
483	GO	gene conversion at mating-type locus, DNA repair synthesis	GO:0000734
484	GO	removal of nonhomologous ends	GO:0000735
485	GO	double-strand break repair via single-strand annealing, removal of nonhomologous ends	GO:0000736
486	GO	DNA catabolic process, endonucleolytic	GO:0000737
487	GO	DNA catabolic process, exonucleolytic	GO:0000738
488	GO	obsolete DNA strand annealing activity	GO:0000739
489	GO	nuclear membrane fusion	GO:0000740
490	GO	karyogamy	GO:0000741
491	GO	karyogamy involved in conjugation with cellular fusion	GO:0000742
492	GO	nuclear migration involved in conjugation with cellular fusion	GO:0000743
493	GO	karyogamy involved in conjugation with mutual genetic exchange	GO:0000744
494	GO	nuclear migration involved in conjugation with mutual genetic exchange	GO:0000745
495	GO	conjugation	GO:0000746
496	GO	conjugation with cellular fusion	GO:0000747
497	GO	conjugation with mutual genetic exchange	GO:0000748
498	GO	response to pheromone involved in conjugation with cellular fusion	GO:0000749
499	GO	pheromone-dependent signal transduction involved in conjugation with cellular fusion	GO:0000750
500	GO	mitotic cell cycle arrest in response to pheromone	GO:0000751
\.


--
-- Name: functions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dblyon
--

SELECT pg_catalog.setval('functions_id_seq', 1, false);


--
-- Data for Name: go_2_slim; Type: TABLE DATA; Schema: public; Owner: dblyon
--

COPY go_2_slim (id, an, slim) FROM stdin;
1	GO:0000003	1
2	GO:0000228	1
3	GO:0000229	1
4	GO:0000902	1
5	GO:0000988	1
6	GO:0001071	1
7	GO:0002376	1
8	GO:0003013	1
9	GO:0003674	1
10	GO:0003677	1
11	GO:0003723	1
12	GO:0003729	1
13	GO:0003735	1
14	GO:0003924	1
15	GO:0004386	1
16	GO:0004518	1
17	GO:0004871	1
18	GO:0005198	1
19	GO:0005575	1
20	GO:0005576	1
21	GO:0005578	1
22	GO:0005615	1
23	GO:0005618	1
24	GO:0005622	1
25	GO:0005623	1
26	GO:0005634	1
27	GO:0005635	1
28	GO:0005654	1
29	GO:0005694	1
30	GO:0005730	1
31	GO:0005737	1
32	GO:0005739	1
33	GO:0005764	1
34	GO:0005768	1
35	GO:0005773	1
36	GO:0005777	1
37	GO:0005783	1
38	GO:0005794	1
39	GO:0005811	1
40	GO:0005815	1
41	GO:0005829	1
42	GO:0005840	1
43	GO:0005856	1
44	GO:0005886	1
45	GO:0005929	1
46	GO:0005975	1
47	GO:0006091	1
48	GO:0006259	1
49	GO:0006397	1
50	GO:0006399	1
51	GO:0006412	1
52	GO:0006457	1
53	GO:0006461	1
54	GO:0006464	1
55	GO:0006520	1
56	GO:0006605	1
57	GO:0006629	1
58	GO:0006790	1
59	GO:0006810	1
60	GO:0006913	1
61	GO:0006914	1
62	GO:0006950	1
63	GO:0007005	1
64	GO:0007009	1
65	GO:0007010	1
66	GO:0007034	1
67	GO:0007049	1
68	GO:0007059	1
69	GO:0007067	1
70	GO:0007155	1
71	GO:0007165	1
72	GO:0007267	1
73	GO:0007568	1
74	GO:0008092	1
75	GO:0008134	1
76	GO:0008135	1
77	GO:0008150	1
78	GO:0008168	1
79	GO:0008219	1
80	GO:0008233	1
81	GO:0008283	1
82	GO:0008289	1
83	GO:0008565	1
84	GO:0009056	1
85	GO:0009058	1
86	GO:0009536	1
87	GO:0009579	1
88	GO:0009790	1
89	GO:0015979	1
90	GO:0016023	1
91	GO:0016192	1
92	GO:0016301	1
93	GO:0016491	1
94	GO:0016746	1
95	GO:0016757	1
96	GO:0016765	1
97	GO:0016779	1
98	GO:0016791	1
99	GO:0016798	1
100	GO:0016810	1
101	GO:0016829	1
102	GO:0016853	1
103	GO:0016874	1
104	GO:0016887	1
105	GO:0019748	1
106	GO:0019843	1
107	GO:0019899	1
108	GO:0021700	1
109	GO:0022607	1
110	GO:0022618	1
111	GO:0022857	1
112	GO:0030154	1
113	GO:0030198	1
114	GO:0030234	1
115	GO:0030312	1
116	GO:0030533	1
117	GO:0030555	1
118	GO:0030674	1
119	GO:0030705	1
120	GO:0032182	1
121	GO:0032196	1
122	GO:0034330	1
123	GO:0034641	1
124	GO:0034655	1
125	GO:0040007	1
126	GO:0040011	1
127	GO:0042254	1
128	GO:0042393	1
129	GO:0042592	1
130	GO:0043167	1
131	GO:0043226	1
132	GO:0043234	1
133	GO:0043473	1
134	GO:0044281	1
135	GO:0044403	1
136	GO:0048646	1
137	GO:0048856	1
138	GO:0048870	1
139	GO:0050877	1
140	GO:0051082	1
141	GO:0051186	1
142	GO:0051276	1
143	GO:0051301	1
144	GO:0051604	1
145	GO:0055085	1
146	GO:0061024	1
147	GO:0065003	1
148	GO:0071554	1
149	GO:0071941	1
\.


--
-- Name: go_2_slim_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dblyon
--

SELECT pg_catalog.setval('go_2_slim_id_seq', 1, false);


--
-- Data for Name: og_2_function; Type: TABLE DATA; Schema: public; Owner: dblyon
--

COPY og_2_function (id, og, function) FROM stdin;
1	ENOG4106EW3	DOM:SIGNAL
2	ENOG4106EW2	GO:0043565
3	ENOG4106EW2	GO:0097159
4	ENOG4106EW2	DOM:BetR
5	ENOG4106EW2	DOM:HTH_3
6	ENOG4106EW2	DOM:HTH_XRE
7	ENOG4106EW2	GO:0005488
8	ENOG4106EW2	GO:0003676
9	ENOG4106EW2	GO:0003677
10	ENOG4106EW2	GO:1901363
11	ENOG4106EW0	GO:0044700
12	ENOG4106EW0	GO:0051716
13	ENOG4106EW0	GO:0050896
14	ENOG4106EW0	GO:0009987
15	ENOG4106EW0	GO:0044464
16	ENOG4106EW0	DOM:TRANS
17	ENOG4106EW0	GO:0005623
18	ENOG4106EW0	GO:0050794
19	ENOG4106EW0	GO:0044763
20	ENOG4106EW0	GO:0007165
21	ENOG4106EW0	GO:0023052
22	ENOG4106EW0	GO:0007154
23	ENOG4106EW0	GO:0065007
24	ENOG4106EW0	GO:0005622
25	ENOG4106EW0	DOM:SIGNAL
26	ENOG4106EW0	GO:0050789
27	ENOG4106EW0	GO:0044699
28	ENOG4106EW5	DOM:COIL
29	ENOG4106EW5	DOM:UPF0150
30	ENOG4106EW4	GO:0003824
31	ENOG4106EW4	DOM:COIL
32	ENOG4106EW4	GO:0016874
33	ENOG4106EW4	DOM:TRANS
34	ENOG4106EW4	GO:0008152
35	ENOG4106EW8	DOM:TPR_1
36	ENOG4106EW8	DOM:TPR_2
37	ENOG4106EW8	DOM:TPR
38	ENOG4106EW8	DOM:TRANS
39	ENOG4106EW8	DOM:COIL
40	ENOG4107QRH	GO:0016787
41	ENOG4107QRH	GO:0008484
42	ENOG4107QRH	DOM:Sulfatase
43	ENOG4107QRH	DOM:TRANS
44	ENOG4107QRH	GO:0016788
45	ENOG4107QRH	GO:0003824
46	ENOG4107QRH	KEGG:00600
47	ENOG4107QRH	DOM:Phosphodiest
48	ENOG4107QRH	GO:0008152
49	ENOG4107QRH	KEGG:00140
50	ENOG4107QRH	DOM:SIGNAL
51	ENOG4107QRH	GO:0004065
52	ENOG4106EWS	DOM:SIGNAL
53	ENOG4106EWS	DOM:TRANS
54	ENOG4106EWR	GO:0043565
55	ENOG4106EWR	GO:0097159
56	ENOG4106EWR	DOM:Peptidase_S24
57	ENOG4106EWR	DOM:HTH_3
58	ENOG4106EWR	DOM:HTH_XRE
59	ENOG4106EWR	GO:0005488
60	ENOG4106EWR	GO:0003676
61	ENOG4106EWR	GO:0003677
62	ENOG4106EWR	GO:1901363
63	ENOG4106EWP	GO:0003824
64	ENOG4106EWP	GO:0016874
65	ENOG4106EWP	DOM:Wzy_C
66	ENOG4106EWP	GO:0008152
67	ENOG4106EWP	DOM:TRANS
68	ENOG4106EWW	GO:0016021
69	ENOG4106EWW	GO:0016020
70	ENOG4106EWW	DOM:TRANS
71	ENOG4106EWW	DOM:DUF2628
72	ENOG4106EWW	GO:0044425
73	ENOG4106EWW	GO:0031224
74	ENOG4106EWZ	DOM:COIL
75	ENOG4106EWZ	DOM:SIGNAL
76	ENOG4106EWX	DOM:FhuF_C
77	ENOG4106EWX	GO:0051536
78	ENOG4106EWX	GO:0051537
79	ENOG4106EWX	GO:0005488
80	ENOG4106EWX	GO:0051540
81	ENOG4106EWC	KEGG:05132
82	ENOG4106EWC	GO:0043547
83	ENOG4106EWC	GO:0009894
84	ENOG4106EWC	GO:0019220
85	ENOG4106EWC	GO:0080090
86	ENOG4106EWC	GO:0019222
87	ENOG4106EWC	GO:0035023
88	ENOG4106EWC	GO:0005085
89	ENOG4106EWC	GO:0030036
90	ENOG4106EWC	GO:0032862
91	ENOG4106EWC	GO:0008047
92	ENOG4106EWC	GO:0023051
93	ENOG4106EWC	GO:0010646
94	ENOG4106EWC	GO:0043087
95	ENOG4106EWC	GO:0050789
96	ENOG4106EWC	GO:0043085
97	ENOG4106EWC	GO:0032319
98	ENOG4106EWC	GO:0032318
99	ENOG4106EWC	GO:0031329
100	ENOG4106EWC	GO:0051345
101	ENOG4106EWC	GO:0009966
102	ENOG4106EWC	GO:0016043
103	ENOG4106EWC	GO:0030811
104	ENOG4106EWC	KEGG:05100
105	ENOG4106EWC	GO:0005576
106	ENOG4106EWC	GO:0065007
107	ENOG4106EWC	GO:0071840
108	ENOG4106EWC	GO:0044093
109	ENOG4106EWC	GO:0065009
110	ENOG4106EWC	GO:0051056
111	ENOG4106EWC	GO:0033121
112	ENOG4106EWC	GO:0009987
113	ENOG4106EWC	GO:0030029
114	ENOG4106EWC	GO:0033124
115	ENOG4106EWC	GO:0019219
116	ENOG4106EWC	GO:0031323
117	ENOG4106EWC	GO:0030234
118	ENOG4106EWC	GO:0050790
119	ENOG4106EWC	GO:0005096
120	ENOG4106EWC	GO:0048583
121	ENOG4106EWC	GO:0050794
122	ENOG4106EWC	GO:0051174
123	ENOG4106EWC	GO:0030695
124	ENOG4106EWC	GO:0032856
125	ENOG4106EWC	GO:0009405
126	ENOG4106EWC	GO:0051171
127	ENOG4106EWC	GO:0006140
128	ENOG4106EWC	GO:0009118
129	ENOG4106EWC	GO:0060589
130	ENOG4106EWC	GO:0051704
131	ENOG4106EWC	GO:0051336
132	ENOG4106EWC	GO:0044699
133	ENOG4106EWC	GO:1900542
134	ENOG4106EWC	GO:0007010
135	ENOG4106EWC	GO:0046578
136	ENOG4106EWC	DOM:SopE_GEF
137	ENOG4106EWC	GO:0031532
138	ENOG4106EWC	GO:0032320
139	ENOG4106EWC	GO:0032321
140	ENOG4106EWC	GO:0006996
141	ENOG4106EWC	DOM:SecIII_SopE_N
142	ENOG4106EWC	GO:0044763
143	ENOG4106EWB	DOM:COIL
144	ENOG4106EWB	DOM:SIGNAL
145	ENOG4106EWB	DOM:TRANS
146	ENOG4106EWA	DOM:N_methyl
147	ENOG4106EWA	DOM:SIGNAL
148	ENOG4106EWA	DOM:TRANS
149	ENOG4106EWA	KEGG:05111
150	ENOG4106EWG	GO:0071704
151	ENOG4106EWG	GO:0016787
152	ENOG4106EWG	GO:0044710
153	ENOG4106EWG	GO:0043170
154	ENOG4106EWG	DOM:Redoxin
155	ENOG4106EWG	GO:0044238
156	ENOG4106EWG	GO:0019538
157	ENOG4106EWG	DOM:SIGNAL
158	ENOG4106EWG	GO:0016209
159	ENOG4106EWG	GO:0016705
160	ENOG4106EWG	GO:0051920
161	ENOG4106EWG	GO:0003824
162	ENOG4106EWG	GO:0008152
163	ENOG4106EWG	GO:0006508
164	ENOG4106EWG	GO:0008233
165	ENOG4106EWG	GO:0016684
166	ENOG4106EWG	DOM:AhpC-TSA
167	ENOG4106EWG	GO:0004601
168	ENOG4106EWG	GO:0055114
169	ENOG4106EWG	GO:0016491
170	ENOG4106EWE	DOM:SIGNAL
171	ENOG4106EWD	DOM:ABM
172	ENOG4106EWD	DOM:COIL
173	ENOG4106EWK	DOM:TRANS
174	ENOG4106EWJ	DOM:Phage_tail
175	ENOG4106EWI	KEGG:00230
176	ENOG4106EWI	DOM:CYTH
177	ENOG4106EWM	DOM:Abhydrolase_2
178	ENOG4106EWM	DOM:FSH1
179	ENOG4106EWV	GO:0008104
180	ENOG4106EWV	GO:0031975
181	ENOG4106EWV	GO:0071944
182	ENOG4106EWV	GO:0009276
183	ENOG4106EWV	GO:0009274
184	ENOG4106EWV	GO:0031224
185	ENOG4106EWV	GO:0008565
186	ENOG4106EWV	GO:0005618
187	ENOG4106EWV	GO:0016021
188	ENOG4106EWV	GO:0016020
189	ENOG4106EWV	GO:0071702
190	ENOG4106EWV	GO:0033036
191	ENOG4106EWV	DOM:SIGNAL
192	ENOG4106EWV	GO:0005215
193	ENOG4106EWV	GO:0006810
194	ENOG4106EWV	GO:0030313
195	ENOG4106EWV	GO:0030312
196	ENOG4106EWV	GO:0045184
197	ENOG4106EWV	KEGG:03070
198	ENOG4106EWV	GO:0051234
199	ENOG4106EWV	GO:0051179
200	ENOG4106EWV	GO:0022892
201	ENOG4106EWV	GO:0044464
202	ENOG4106EWV	DOM:TRANS
203	ENOG4106EWV	GO:0005623
204	ENOG4106EWV	DOM:GspL
205	ENOG4106EWV	GO:0015031
206	ENOG4106EWV	GO:0044425
207	ENOG4108W6K	DOM:Acyl_transf_3
208	ENOG4108W6K	GO:0016020
209	ENOG4108W6K	DOM:TRANS
210	ENOG4108W6K	GO:0003824
211	ENOG4108W6K	GO:0016740
212	ENOG4108W6K	GO:0016746
213	ENOG4108W6K	GO:0016747
214	ENOG4108W6K	GO:0008152
215	ENOG4108W6K	DOM:OpgC_C
216	ENOG410841R	DOM:TRANS
217	ENOG41085R9	GO:0044238
218	ENOG41085R9	GO:0005975
219	ENOG41085R9	GO:0005976
220	ENOG41085R9	GO:0016020
221	ENOG41085R9	GO:0000271
222	ENOG41085R9	DOM:TRANS
223	ENOG41085R9	DOM:Polysacc_synt
224	ENOG41085R9	GO:0016051
225	ENOG41085R9	GO:0071704
226	ENOG41085R9	GO:0009058
227	ENOG41085R9	GO:0009059
228	ENOG41085R9	GO:0008152
229	ENOG41085R9	GO:0044723
230	ENOG41085R9	GO:1901576
231	ENOG41085R9	GO:0043170
232	ENOG41085R0	DOM:Abhydrolase_2
233	ENOG41085R0	DOM:Abhydrolase_1
234	ENOG41085R0	DOM:Esterase
235	ENOG41085R0	DOM:DLH
236	ENOG41085R0	DOM:Peptidase_S9
237	ENOG41085R0	DOM:SIGNAL
238	ENOG41085R1	DOM:DUF2076
239	ENOG41085R1	DOM:COIL
240	ENOG41085R7	GO:0016787
241	ENOG41085R7	DOM:Abhydrolase_3
242	ENOG41085R7	DOM:TRANS
243	ENOG41085R7	GO:0003824
244	ENOG41085R7	GO:0008152
245	ENOG41085R7	DOM:Lipase_GDSL
246	ENOG41085R7	DOM:SIGNAL
247	ENOG41085R5	GO:0035639
248	ENOG41085R5	GO:0016310
249	ENOG41085R5	DOM:HATPase_c
250	ENOG41085R5	GO:0005488
251	ENOG41085R5	GO:0000166
252	ENOG41085R5	GO:1901363
253	ENOG41085R5	GO:0001883
254	ENOG41085R5	GO:0001882
255	ENOG41085R5	GO:0043168
256	ENOG41085R5	GO:0044267
257	ENOG41085R5	GO:0044260
258	ENOG41085R5	GO:0071704
259	ENOG41085R5	GO:0043167
260	ENOG41085R5	GO:0004674
261	ENOG41085R5	GO:0016740
262	ENOG41085R5	GO:1901265
263	ENOG41085R5	GO:0032549
264	ENOG41085R5	GO:0017076
265	ENOG41085R5	GO:0005524
266	ENOG41085R5	GO:0006468
267	ENOG41085R5	GO:0016301
268	ENOG41085R5	GO:0006793
269	ENOG41085R5	GO:0004672
270	ENOG41085R5	GO:0006464
271	ENOG41085R5	GO:0036094
272	ENOG41085R5	GO:0003824
273	ENOG41085R5	GO:0043412
274	ENOG41085R5	GO:0036211
275	ENOG41085R5	GO:0008152
276	ENOG41085R5	GO:0044238
277	ENOG41085R5	GO:0030554
278	ENOG41085R5	GO:0016773
279	ENOG41085R5	GO:0097159
280	ENOG41085R5	DOM:STAS
281	ENOG41085R5	GO:0044237
282	ENOG41085R5	GO:0043170
283	ENOG41085R5	GO:0019538
284	ENOG41085R5	GO:0006796
285	ENOG41085R5	GO:0032559
286	ENOG41085R5	GO:0016772
287	ENOG41085R5	GO:0032555
288	ENOG41085R5	GO:0009987
289	ENOG41085R5	GO:0032550
290	ENOG41085R5	GO:0032553
291	ENOG4108ECT	GO:0009187
292	ENOG4108ECT	GO:0006807
293	ENOG4108ECT	GO:0044249
294	ENOG4108ECT	GO:0034641
295	ENOG4108ECT	GO:0009165
296	ENOG4108ECT	GO:0023052
297	ENOG4108ECT	GO:0007165
298	ENOG4108ECT	GO:0035556
299	ENOG4108ECT	GO:1901362
300	ENOG4108ECT	GO:0050789
301	ENOG4108ECT	GO:1901360
302	ENOG4108ECT	GO:1901576
303	ENOG4108ECT	GO:0044710
304	ENOG4108ECT	GO:0016829
305	ENOG4108ECT	GO:0016849
306	ENOG4108ECT	GO:0071704
307	ENOG4108ECT	KEGG:04113
308	ENOG4108ECT	GO:0065007
309	ENOG4108ECT	GO:0044699
310	ENOG4108ECT	DOM:Guanylate_cyc
311	ENOG4108ECT	GO:0009190
312	ENOG4108ECT	KEGG:00230
313	ENOG4108ECT	GO:0018130
314	ENOG4108ECT	GO:0006139
315	ENOG4108ECT	DOM:CHASE2
316	ENOG4108ECT	GO:0009987
317	ENOG4108ECT	GO:0006725
318	ENOG4108ECT	GO:0051716
319	ENOG4108ECT	GO:0050794
320	ENOG4108ECT	GO:0003824
321	ENOG4108ECT	GO:0009058
322	ENOG4108ECT	GO:0009117
323	ENOG4108ECT	GO:0008152
324	ENOG4108ECT	GO:0019438
325	ENOG4108ECT	GO:0034654
326	ENOG4108ECT	GO:0007154
327	ENOG4108ECT	GO:0090407
328	ENOG4108ECT	GO:0055086
329	ENOG4108ECT	GO:0046483
330	ENOG4108ECT	GO:0044700
331	ENOG4108ECT	GO:0044271
332	ENOG4108ECT	GO:0050896
333	ENOG4108ECT	DOM:CYCc
334	ENOG4108ECT	DOM:TRANS
335	ENOG4108ECT	GO:0044237
336	ENOG4108ECT	GO:0006796
337	ENOG4108ECT	GO:0044238
338	ENOG4108ECT	GO:1901293
339	ENOG4108ECT	GO:0006793
340	ENOG4108ECT	GO:0019637
341	ENOG4108ECT	GO:0044763
342	ENOG4108ECT	GO:0006753
343	ENOG4108ECT	GO:0044281
344	ENOG41085RP	GO:0043169
345	ENOG41085RP	GO:0016151
346	ENOG41085RP	GO:0043170
347	ENOG41085RP	DOM:HypA
348	ENOG41085RP	GO:0044260
349	ENOG41085RP	GO:0046914
350	ENOG41085RP	GO:0044238
351	ENOG41085RP	GO:0019538
352	ENOG41085RP	GO:0044237
353	ENOG41085RP	GO:0009987
354	ENOG41085RP	GO:0006464
355	ENOG41085RP	GO:0043167
356	ENOG41085RP	GO:0071704
357	ENOG41085RP	GO:0043412
358	ENOG41085RP	GO:0036211
359	ENOG41085RP	GO:0005488
360	ENOG41085RP	GO:0008152
361	ENOG41085RP	GO:0044267
362	ENOG41085RP	GO:0046872
363	ENOG41085RU	DOM:PIG-L
364	ENOG41085RK	GO:0044238
365	ENOG41085RK	GO:0038023
366	ENOG41085RK	GO:0003676
367	ENOG41085RK	GO:0016310
368	ENOG41085RK	GO:0060089
369	ENOG41085RK	GO:0023052
370	ENOG41085RK	GO:0007165
371	ENOG41085RK	GO:0004871
372	ENOG41085RK	GO:0003677
373	ENOG41085RK	GO:0016772
374	ENOG41085RK	GO:0050789
375	ENOG41085RK	GO:0044699
376	ENOG41085RK	GO:0043565
377	ENOG41085RK	GO:0051716
378	ENOG41085RK	GO:0044260
379	ENOG41085RK	GO:0000160
380	ENOG41085RK	GO:1901363
381	ENOG41085RK	GO:0071704
382	ENOG41085RK	GO:0016740
383	ENOG41085RK	GO:0065007
384	ENOG41085RK	GO:0023014
385	ENOG41085RK	GO:0004673
386	ENOG41085RK	GO:0004672
387	ENOG41085RK	GO:0004872
388	ENOG41085RK	GO:0006793
389	ENOG41085RK	GO:0006468
390	ENOG41085RK	GO:0009987
391	ENOG41085RK	GO:0044267
392	ENOG41085RK	GO:0016301
393	ENOG41085RK	DOM:HTH_3
394	ENOG41085RK	GO:0006464
395	ENOG41085RK	GO:0050794
396	ENOG41085RK	GO:0003824
397	ENOG41085RK	GO:0043412
398	ENOG41085RK	GO:0036211
399	ENOG41085RK	GO:0044763
400	ENOG41085RK	GO:0008152
401	ENOG41085RK	GO:0007154
402	ENOG41085RK	GO:0044700
403	ENOG41085RK	GO:0016773
404	ENOG41085RK	GO:0000155
405	ENOG41085RK	GO:0050896
406	ENOG41085RK	GO:0016775
407	ENOG41085RK	GO:0043170
408	ENOG41085RK	GO:0019538
409	ENOG41085RK	GO:0006796
410	ENOG41085RK	DOM:HTH_XRE
411	ENOG41085RK	GO:0097159
412	ENOG41085RK	GO:0044237
413	ENOG41085RK	DOM:PAS_4
414	ENOG41085RK	GO:0005488
415	ENOG4108ECV	DOM:HCBP_related
416	ENOG41085RB	GO:0006633
417	ENOG41085RB	GO:0006631
418	ENOG41085RB	GO:0044237
419	ENOG41085RB	GO:0009317
420	ENOG41085RB	GO:0019752
421	ENOG41085RB	GO:0044249
422	ENOG41085RB	GO:0016885
423	ENOG41085RB	GO:0044281
424	ENOG41085RB	GO:0044283
425	ENOG41085RB	GO:0072330
426	ENOG41085RB	GO:0005737
427	ENOG41085RB	GO:1901576
428	ENOG41085RB	GO:0044710
429	ENOG41085RB	GO:0044711
430	ENOG41085RB	GO:0005623
431	ENOG41085RB	KEGG:00720
432	ENOG41085RB	KEGG:00640
433	ENOG41085RB	KEGG:01100
434	ENOG41085RB	GO:0071704
435	ENOG41085RB	KEGG:00620
436	ENOG41085RB	GO:0003989
437	ENOG41085RB	KEGG:00253
438	ENOG41085RB	KEGG:01120
439	ENOG41085RB	DOM:Biotin_lipoyl
440	ENOG41085RB	GO:0006629
441	ENOG41085RB	GO:0009987
442	ENOG41085RB	GO:0032787
443	ENOG41085RB	GO:0003824
444	ENOG41085RB	GO:0009058
445	ENOG41085RB	GO:0008152
446	ENOG41085RB	GO:0043436
447	ENOG41085RB	GO:0044255
448	ENOG41085RB	GO:0016874
449	ENOG41085RB	GO:0008610
450	ENOG41085RB	GO:0043234
451	ENOG41085RB	GO:0044238
452	ENOG41085RB	GO:0032991
453	ENOG41085RB	GO:0006082
454	ENOG41085RB	GO:0046394
455	ENOG41085RB	GO:0044464
456	ENOG41085RB	GO:0016053
457	ENOG41085RB	GO:0016421
458	ENOG41085RB	GO:0005622
459	ENOG41085RB	KEGG:00061
460	ENOG41085RB	GO:0044444
461	ENOG41085RB	KEGG:01110
462	ENOG41085RB	GO:0044424
463	ENOG41085RC	DOM:DUF927
464	ENOG41085RA	GO:0032774
465	ENOG41085RA	GO:0034062
466	ENOG41085RA	DOM:zf-CHC2
467	ENOG41085RA	DOM:COIL
468	ENOG41085RA	GO:0090304
469	ENOG41085RA	GO:0044249
470	ENOG41085RA	GO:0034641
471	ENOG41085RA	GO:0006807
472	ENOG41085RA	GO:0005488
473	ENOG41085RA	GO:0003676
474	ENOG41085RA	GO:0003677
475	ENOG41085RA	GO:1901576
476	ENOG41085RA	GO:1901362
477	ENOG41085RA	GO:1901363
478	ENOG41085RA	GO:1901360
479	ENOG41085RA	GO:0043169
480	ENOG41085RA	GO:0046914
481	ENOG41085RA	GO:0043167
482	ENOG41085RA	GO:0071704
483	ENOG41085RA	GO:0016740
484	ENOG41085RA	GO:0006260
485	ENOG41085RA	GO:0006261
486	ENOG41085RA	GO:0046872
487	ENOG41085RA	GO:0006269
488	ENOG41085RA	GO:0018130
489	ENOG41085RA	GO:0006139
490	ENOG41085RA	GO:0009987
491	ENOG41085RA	GO:0006725
492	ENOG41085RA	GO:0003824
493	ENOG41085RA	GO:0034645
494	ENOG41085RA	GO:0009059
495	ENOG41085RA	GO:0008152
496	ENOG41085RA	GO:0019438
497	ENOG41085RA	GO:0034654
498	ENOG41085RA	GO:0046483
499	ENOG41085RA	GO:0016070
500	ENOG41085RA	GO:0044238
\.


--
-- Name: og_2_function_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dblyon
--

SELECT pg_catalog.setval('og_2_function_id_seq', 1, false);


--
-- Data for Name: ogs; Type: TABLE DATA; Schema: public; Owner: dblyon
--

COPY ogs (id, og, taxid, description) FROM stdin;
1	ENOG4106EW0	2	Lipoprotein
2	ENOG4106EW5	2	Uncharacterised protein family (UPF0150)
3	ENOG4106EW4	2	Streptolysin associated protein SagC
4	ENOG4107QRH	2	Arylsulfatase (Ec 3.1.6.1)
5	ENOG4106EWR	2	HTH_XRE
6	ENOG4106EWP	2	O-Antigen ligase
7	ENOG4106EWW	2	Protein of unknown function (DUF2628)    
8	ENOG4106EWC	2	guanine nucleotide exchange factor (GEF). This activation results in actin cytoskeleton rearrangements and stimulates membrane ruffling
9	ENOG4106EWB	2	(LipO)protein
10	ENOG4106EWG	2	Redoxin
11	ENOG4106EWJ	2	Major tail protein
12	ENOG4106EWI	2	Adenylate cyclase
13	ENOG4106EWV	2	Type II secretion system protein L
14	ENOG4108W6K	2	Acyl-transferase
15	ENOG41085R9	2	biosynthesis protein
16	ENOG41085R1	2	Periplasmic ligand-binding sensor protein
17	ENOG41085R7	2	lipolytic protein G-D-S-L family
18	ENOG41085R5	2	anti-sigma regulatory factor serine threonine protein kinase
19	ENOG4108ECT	2	Adenylate guanylate cyclase with Chase sensor
20	ENOG41085RP	2	hydrogenase nickel incorporation protein hypA
21	ENOG41085RU	2	GlcNAc-PI de-N-acetylase
22	ENOG41085RK	2	Xre family transcriptional regulator
23	ENOG4108ECV	2	Inherit from COG: Hemolysin-type calcium-binding
24	ENOG41085RB	2	Biotin carboxyl carrier protein
25	ENOG41085RC	2	Inherit from COG: Domain of unknown function (DUF927)
26	ENOG41085RA	2	Inherit from COG: DNA primase activity
27	ENOG41085RF	2	Regulatory protein, FmdB family
28	ENOG4108TP2	2	Clp protease
29	ENOG41075IK	2	Protein of unknown function (DUF933)
30	ENOG4107AC1	2	Inherit from COG: TadE family
31	ENOG4107ACA	2	Calcium-binding protein required for initiation of chromosome replication
32	ENOG4107ACB	2	Protein of unknown function (DUF2795)
33	ENOG4105RN8	2	Inherit from COG: Efflux transporter rnd family, mfp subunit
34	ENOG4105RN6	2	reductase
35	ENOG4105RN7	2	Transcriptional regulator
36	ENOG4105RN5	2	Protein of unknown function DUF86
37	ENOG4105RN2	2	ATPase associated with various cellular activities
38	ENOG4105RN3	2	DivIVA protein
39	ENOG4105RN1	2	integral membrane protein
40	ENOG4105RNN	2	lysozyme
41	ENOG4105RNM	2	Pfam:DUF255
42	ENOG4105RNJ	2	Domain of unknown function (DUF1735)
43	ENOG4105RNK	2	insecticidal toxin complex protein
44	ENOG4105RNH	2	Calcineurin-like phosphoesterase
45	ENOG4105RNI	2	Protein of unknown function (DUF721)
46	ENOG4105RNG	2	membrane
47	ENOG4105RND	2	Porphyromonas gingivalis family protein
48	ENOG4105RNE	2	flagellar basal body-associated protein flil
49	ENOG4105RNC	2	avirulence D
50	ENOG4105RNZ	2	Pyridoxamine 5-phosphate oxidase-related, FMN-binding
51	ENOG4105RNX	2	Diguanylate cyclase
52	ENOG4105RNV	2	carboxymuconolactone decarboxylase
53	ENOG4105RNW	2	Domain-Containing protein
54	ENOG4105RNT	2	hemolysin-type calcium-binding region
55	ENOG4105RNU	2	Aminoglycoside phosphotransferase
56	ENOG4105RNQ	2	Protein of unknown function (DUF1471)
57	ENOG4108AE9	2	Glycosyl transferase family 2
58	ENOG4108AE8	2	Uncharacterized protein family UPF0016
59	ENOG4108AE5	2	YqaJ-like viral recombinase domain
60	ENOG4108AE0	2	extracellular solute-binding protein family 1
61	ENOG4108AEN	2	Protein of unknown function (DUF541)
62	ENOG4108AEJ	2	CRISPR-associated protein, Cse1 family
63	ENOG4108AEI	2	YceI family
64	ENOG4108AEG	2	NlpC/P60 family
65	ENOG4108AEF	2	dUTPase
66	ENOG4108AEE	2	Inherit from COG: deaminase
67	ENOG4108AED	2	Domain of unknown function (DUF1794)
68	ENOG4108AEC	2	D12 class N6 adenine-specific DNA methyltransferase
69	ENOG4108AEB	2	Calcineurin-like phosphoesterase
70	ENOG4108AEA	2	Uncharacterised protein family (UPF0104)
71	ENOG4108AEZ	2	Transcriptional regulator, BadM Rrf2 family
72	ENOG4108AEY	2	RNA polymerase sigma factor
73	ENOG4108AEW	2	Uncharacterized protein conserved in bacteria (DUF2094)
74	ENOG4108AET	2	Saccharopine dehydrogenase 
75	ENOG4108AES	2	Dihydroorotate dehydrogenase
76	ENOG4106ATC	2	Trans_reg_C
77	ENOG4106ATF	2	DNA RNA non-specific endonuclease
78	ENOG4106ATI	2	Hypoxia induced protein conserved region
79	ENOG4106ATM	2	Protein of unknown function (DUF1797)
80	ENOG4106ATQ	2	transposase
81	ENOG4106ATW	2	Inherit from COG: Nucleic-acid-binding protein containing a Zn-ribbon
82	ENOG4106ATU	2	VRR-NUC domain-containing protein
83	ENOG4106ATZ	2	DnaJ domain protein
84	ENOG4106ATX	2	Uncharacterized protein conserved in bacteria (DUF2065)
85	ENOG4106AT2	2	Protein of unknown function (DUF3489)
86	ENOG4106AT1	2	ABC-2 type transporter
87	ENOG4106AT6	2	prevent-host-death family
88	ENOG4106AT7	2	Protein of unknown function (DUF2919)
89	ENOG4106AT4	2	metallophosphoesterase
90	ENOG4107EV6	2	Inherit from COG: YD repeat protein
91	ENOG4106G46	2	SpoVT_AbrB
92	ENOG4106G47	2	Hnh endonuclease
93	ENOG4106G40	2	Phosphotransferase enzyme family
94	ENOG4106G42	2	TPR
95	ENOG4106G43	2	Pfam:DUF1813
96	ENOG4106G4D	2	Predicted membrane-bound metal-dependent hydrolase (DUF457)
97	ENOG4106G4N	2	lipase class 3
98	ENOG4106G4H	2	rdd domain-containing protein
99	ENOG4106G4I	2	IS630 family transposase
100	ENOG4106G4U	2	Protein of unknown function (DUF550)
101	ENOG4106G4S	2	MobA/MobL family
102	ENOG4106G4X	2	TetR family transcriptional regulator-like protein
103	ENOG4106G4Z	2	Protein of unknown function (DUF2283)
104	ENOG410622C	2	Transposase
105	ENOG4106220	2	Pilus assembly protein, PilO
106	ENOG4106227	2	Protein of unknown function (DUF2945)
107	ENOG4106228	2	TOBE domain
108	ENOG4105YKD	2	Transcriptional regulator, TetR family
109	ENOG41090GW	2	choline kinase involved in LPS biosynthesis
110	ENOG41090GV	2	transcriptional regulator AsnC family
111	ENOG410647H	2	pH adaptation potassium efflux system protein B 1 sodium hydrogen antiporter subunit
112	ENOG410647N	2	response to DNA damage stimulus
113	ENOG410647E	2	flagellar hook
114	ENOG410647Z	2	gliding motility-associated lipoprotein GldH
115	ENOG4107JH0	2	UspA domain protein
116	ENOG4107JH6	2	Acetyltransferase (GNAT) family
117	ENOG41090GD	2	phage major capsid protein, HK97
118	ENOG4107JHZ	2	Starch binding domain
119	ENOG4107JHX	2	Cupin domain
120	ENOG4107JHY	2	Uncharacterized protein conserved in bacteria (DUF2336)
121	ENOG4107JHW	2	Predicted membrane-bound metal-dependent hydrolase (DUF457)
122	ENOG4107JHT	2	Prokaryotic N-terminal methylation motif
123	ENOG4107JHN	2	Citrate lyase
124	ENOG41090GN	2	phosphoglycerate
125	ENOG4107JHC	2	SusD family
126	ENOG4107JHD	2	SlyX family
127	ENOG4107JHE	2	ATP synthase I chain
128	ENOG41090GI	2	NLP P60 protein
129	ENOG41090GH	2	Cell wall anchor domain protein
130	ENOG4106472	2	Fimbrial protein
131	ENOG4106Z6A	2	Dynamin family
132	ENOG4106Z6Y	2	LuxR family Transcriptional regulator
133	ENOG4106Z6P	2	RICIN
134	ENOG4106Z68	2	Pfam:Transposase_30
135	ENOG4106Z66	2	CBS domain
136	ENOG4106Z62	2	Protein of unknown function (DUF2767)
137	ENOG4106Z61	2	Cna protein B-type domain
138	ENOG4108231	2	aminopeptidase
139	ENOG4107BGF	2	Phosphotransferase enzyme family
140	ENOG4106N1K	2	peptidase S8 and S53
141	ENOG4106N1I	2	Inherit from NOG: l-lactate permease
142	ENOG4106N1N	2	Glycosyl transferases group 1
143	ENOG4106N1A	2	Pfam:DUF820
144	ENOG4106N1F	2	Pfam:DUF820
145	ENOG4106N1G	2	Conjugative transfer protein
146	ENOG4106N1E	2	Glycosyl hydrolase family 62 
147	ENOG4106N1S	2	Uncharacterized protein conserved in bacteria (DUF2325)
148	ENOG4106N1P	2	HTH_ARAC
149	ENOG4106N1Q	2	Protein of unknown function (DUF1549)
150	ENOG4106N1W	2	TonB dependent receptor
151	ENOG4106N1T	2	Predicted membrane protein (DUF2142)
152	ENOG4106N1U	2	Hsp70 protein
153	ENOG41065AY	2	prolyl-tRNA synthetase
154	ENOG410823R	2	SNARE associated Golgi protein
155	ENOG4106N18	2	LysR family (Transcriptional regulator
156	ENOG4106N12	2	AMP-binding enzyme
157	ENOG4106N16	2	had-superfamily hydrolase, subfamily iib
158	ENOG4106N17	2	DnaB domain protein helicase domain protein
159	ENOG4106N15	2	Dicarboxylate carrier protein MatC N-terminus
160	ENOG41065AA	2	Predicted membrane protein (DUF2339)
161	ENOG41065AE	2	methyltransferase FkbM
162	ENOG41065A4	2	Bidirectionally degrades single-stranded DNA into large acid-insoluble oligonucleotides, which are then degraded further into small acid-soluble oligonucleotides (By similarity)
163	ENOG410823Z	2	Transfers the 4'-phosphopantetheine moiety from coenzyme A to a Ser of acyl-carrier-protein (By similarity)
164	ENOG4108MVZ	2	rhodanese domain-containing protein
165	ENOG4108MVW	2	CRISPR-associated RAMP protein, Csx10 family
166	ENOG4108MVT	2	Histidine kinase
167	ENOG4108MVP	2	nicotinamide mononucleotide transporter pnuc
168	ENOG4108MVQ	2	NADPH-dependent f420 reductase
169	ENOG4108MVJ	2	extracellular solute-binding protein
170	ENOG4108MVK	2	Receptor
171	ENOG4108MVF	2	domain protein
172	ENOG4108MVG	2	integral membrane protein
173	ENOG4108MVD	2	Zinc finger SWIM domain protein
174	ENOG4108MVE	2	Inherit from COG: transposase
175	ENOG4108MVA	2	peptidase, S41
176	ENOG4108MV8	2	Inherit from COG: Diguanylate cyclase
177	ENOG4108MV9	2	Phage domain protein
178	ENOG4108MV6	2	Trap transporter solute receptor
179	ENOG4108MV7	2	Cytosolic protein
180	ENOG4108MV5	2	ATPase associated with various cellular activities aaa_5
181	ENOG4108MV2	2	Involved in light-induced Na( )-dependent proton extrusion. Also seems to be involved in CO(2) transport (By similarity)
182	ENOG4108MV0	2	Pfam:Bug
183	ENOG4108MV1	2	tyrosinase
184	ENOG41079ZY	2	Pilin like competence factor
185	ENOG41079ZX	2	spore coat U domain-containing protein
186	ENOG41079ZN	2	Protein of unknown function (DUF1268)
187	ENOG41079ZK	2	oxidoreductase
188	ENOG41079ZG	2	Lipid A 3-O-deacylase (PagL)
189	ENOG41079ZF	2	FlgN protein
190	ENOG41079Z9	2	Colicin V production protein
191	ENOG41079Z3	2	Putative peptidoglycan binding domain
192	ENOG4107PTT	2	prevent-host-death family
193	ENOG4107PTR	2	Ankyrin repeat
194	ENOG4107PTY	2	Inherit from NOG: Transposase (IS4 family
195	ENOG4107PTD	2	protein translocase subunit secG
196	ENOG4107PTF	2	Inherit from COG: Capsular Polysaccharide Biosynthesis Protein-Like Protein
197	ENOG4107PTG	2	Inherit from NOG: MSHA biogenesis protein MshQ
198	ENOG4107PTA	2	Adenylate and Guanylate cyclase catalytic domain
199	ENOG4107PTC	2	Bacterial protein of unknown function (DUF883)
200	ENOG4107PTM	2	Phosphotransferase enzyme family
201	ENOG4107PTJ	2	Dynamin family
202	ENOG4107PTK	2	von Willebrand factor type A domain
203	ENOG4107PT8	2	Inherit from COG: Provides the precursors necessary for DNA synthesis. Catalyzes the biosynthesis of deoxyribonucleotides from the corresponding ribonucleotides (By similarity)
204	ENOG4107PT9	2	Sporulation related domain
205	ENOG4108BKI	2	Type IV leader peptidase family
206	ENOG4108BKA	2	Phage integrase family
207	ENOG4108BKF	2	Pfam:SBP_bac_9
208	ENOG4108BKU	2	ATP synthase, Delta/Epsilon chain, beta-sandwich domain
209	ENOG4108BK3	2	Pfam:DUF894
210	ENOG4108R4Z	2	Functions in the N-end rule pathway of protein degradation where it conjugates Leu, Phe and, less efficiently, Met from aminoacyl-tRNAs to the N-termini of proteins containing an N-terminal arginine or lysine (By similarity)
211	ENOG4108R4Y	2	LuxR family transcriptional regulator
212	ENOG4108R4X	2	integral membrane protein
213	ENOG4108R4Q	2	HlyD family secretion protein
214	ENOG4108R4P	2	Protein of unknown function (DUF2764)
215	ENOG4108R4T	2	Two component transcriptional regulator, winged helix family
216	ENOG4108R4I	2	s-layer domain-containing protein
217	ENOG4108R4N	2	DNA primase
218	ENOG4108R4B	2	Pseudouridine synthase
219	ENOG4108R4A	2	Alpha beta superfamily hydrolase
220	ENOG4108R4G	2	transcriptional regulator MERR family
221	ENOG4108R4E	2	acyl-Coa dehydrogenase
222	ENOG4108R4D	2	thioesterase Superfamily protein
223	ENOG4108R49	2	cell wall binding
224	ENOG4108R43	2	precorrin-3b synthase
225	ENOG4108R42	2	response regulator
226	ENOG4108R47	2	YceI family
227	ENOG4108R45	2	Transcriptional regulator
228	ENOG4108R44	2	Lipid A oxidase
229	ENOG41065NU	2	Uncharacterised protein family (UPF0227)
230	ENOG41065NP	2	Protein of unknown function (DUF1471)
231	ENOG41065NX	2	Hydrolase
232	ENOG41065NY	2	nucleotidyltransferase family
233	ENOG41065NE	2	bacteriophage lysis protein
234	ENOG41065NF	2	Fimbrial assembly family protein
235	ENOG41065NG	2	family Transcriptional regulator
236	ENOG41065NC	2	limonene-12-epoxide hydrolase
237	ENOG41065NM	2	gCN5-related N-acetyltransferase
238	ENOG41065NN	2	acetyltransferase, (GNAT) family
239	ENOG4107T4H	2	Inherit from COG: 40-residue yvtn family beta-propeller repeat protein
240	ENOG4107T4K	2	DNA polymerase III is a complex, multichain enzyme responsible for most of the replicative synthesis in bacteria. This DNA polymerase also exhibits 3' to 5' exonuclease activity. The beta chain is required for initiation of replication once it is clamped onto DNA, it slides freely (bidirectional and ATP- independent) along duplex DNA (By similarity)
241	ENOG41065N5	2	Pfam:DUF322
242	ENOG41065N6	2	Protein of unknown function (DUF3013)
243	ENOG41065N1	2	inhibitor
244	ENOG41065N9	2	Inherit from NOG: Catalyzes the acylation of glycosyl-4,4'- diaponeurosporenoate, i.e. the esterification of glucose at the C6'' position with the carboxyl group of the C(15) fatty acid 12- methyltetradecanoic acid, to yield staphyloxanthin. This is the last step in the biosynthesis of this orange pigment, present in most staphylococci strains (By similarity)
245	ENOG4107T4T	2	Major Facilitator
246	ENOG4106VE7	2	Flagellar biosynthesis protein, FliO
247	ENOG4106VE4	2	Xylose isomerase-like TIM barrel
248	ENOG4106VE5	2	Replication initiator protein A (RepA) N-terminus
249	ENOG4107T4Y	2	Patatin-like phospholipase
250	ENOG4106VER	2	von Willebrand factor, type A
251	ENOG4106VES	2	MGS
252	ENOG4106VEM	2	tagatose-6-phosphate kinase
253	ENOG4106VED	2	Bacterial regulatory proteins, tetR family
254	ENOG4106VEE	2	cytochrome C family protein
255	ENOG4106VEB	2	Glycosyl Transferase
256	ENOG4106YE8	2	type IV pilus modification protein PilV
257	ENOG4105UB9	2	Methyl-accepting chemotaxis
258	ENOG4105Z7Y	2	Anti-feci sigma factor, fecr
259	ENOG4105UBQ	2	Methyltransferase
260	ENOG4105Z7T	2	PTS system lactose cellobiose-specific transporter subunit IIB
261	ENOG4105Z7W	2	Bacterial protein of unknown function (DUF937)
262	ENOG4105Z7Q	2	Cytosolic protein
263	ENOG4106YER	2	Transglycosylase associated protein
264	ENOG4105Z7K	2	domain protein
265	ENOG4105Z7J	2	Transport-associated protein
266	ENOG4105Z0H	2	glycine cleavage system regulatory protein
267	ENOG4105Z0I	2	Had-superfamily hydrolase, subfamily ia, variant 1
268	ENOG4105Z0J	2	(type IV) pilus
269	ENOG4105Z0M	2	Protein of unknown function (DUF3015)
270	ENOG4105Z0D	2	Gtra family
271	ENOG4105Z0E	2	Amino acid ABC transporter substrate-binding protein
272	ENOG4105Z0F	2	Cytochrome
273	ENOG4105Z0G	2	FR47-like protein
274	ENOG4105Z0X	2	Glyoxalase Bleomycin resistance protein (Dioxygenase
275	ENOG4105Z0R	2	rieske 2fe-2S domain-containing protein
276	ENOG4107T40	2	Inherit from COG: Glycosyltransferase 36
277	ENOG4107T41	2	NifU domain protein
278	ENOG4107T46	2	Permease for cytosine/purines, uracil, thiamine, allantoin
279	ENOG4105Z70	2	deacetylase-like protein
280	ENOG4105Z08	2	DNA Polymerase Beta Domain Protein Region
281	ENOG4105Z05	2	domain protein
282	ENOG4105YCM	2	glyoxalase bleomycin resistance protein dioxygenase
283	ENOG4105YCJ	2	short chain dehydrogenase
284	ENOG41084ZV	2	Protein of unknown function (DUF972)
285	ENOG4105YCQ	2	EamA-like transporter family
286	ENOG4105YX7	2	Protein of unknown function (DUF2867)
287	ENOG41089D0	2	Inherit from COG: Retrotransposon protein
288	ENOG41089D2	2	e3 binding domain
289	ENOG41089D5	2	Predicted membrane-bound metal-dependent hydrolase (DUF457)
290	ENOG41089D6	2	2Fe-2S iron-sulfur cluster binding domain
291	ENOG41089D7	2	Acetyltransferase (GNAT) family
292	ENOG4105YCZ	2	Antifreeze protein, type I
293	ENOG4108YJX	2	Phage-related protein
294	ENOG4108YJY	2	Signal transduction histidine kinase, lyts
295	ENOG4108YJV	2	endoribonuclease L-psp
296	ENOG4108YJW	2	Single-strand binding protein
297	ENOG4108YJT	2	Conserved Protein
298	ENOG4108YJU	2	acetyltransferase
299	ENOG4108YJR	2	gCN5-related N-acetyltransferase
300	ENOG4108YJS	2	FecR family
301	ENOG4108YJP	2	EamA-like transporter family
302	ENOG4108YJQ	2	gCN5-related N-acetyltransferase
303	ENOG4108YJK	2	tail protein
304	ENOG4108YJH	2	exported protein
305	ENOG4108YJI	2	fatty acid hydroxylase
306	ENOG4108YJF	2	Inherit from COG: serine acetyltransferase
307	ENOG4108YJE	2	hydrolase
308	ENOG4108YJB	2	Sarcosine oxidase, gamma subunit
309	ENOG4108YJC	2	Protein of unknown function (DUF2000)
310	ENOG4108YJA	2	DNA polymerase III is a complex, multichain enzyme responsible for most of the replicative synthesis in bacteria. This DNA polymerase also exhibits 3' to 5' exonuclease activity. The beta chain is required for initiation of replication once it is clamped onto DNA, it slides freely (bidirectional and ATP- independent) along duplex DNA (By similarity)
311	ENOG4108YJ9	2	mechanosensitive ion channel
312	ENOG4108YJ6	2	Pfam:DUF395
313	ENOG4108YJ7	2	Protein of unknown function (DUF796)
314	ENOG4108YJ4	2	Protein of unknown function (DUF736)
315	ENOG4108YJ5	2	Converts heme B (protoheme IX) to heme O by substitution of the vinyl group on carbon 2 of heme B porphyrin ring with a hydroxyethyl farnesyl side group (By similarity)
316	ENOG4108YJ2	2	Dihydrofolate reductase
317	ENOG4108YJ0	2	cytochrome C
318	ENOG4105ENU	2	Cupin 2, conserved barrel domain protein
319	ENOG4105ENT	2	Efflux transporter rnd family, mfp subunit
320	ENOG4105ENW	2	Domain of Unknown Function (DUF748)
321	ENOG4105ENV	2	phosphonate C-P lyase system protein PhnK
322	ENOG4105ENQ	2	Alpha-L-fucosidase
323	ENOG4105ENP	2	Beta (1-6) glucans synthase
324	ENOG4105ENR	2	peptidase, M24
325	ENOG4105ENY	2	Ethanolamine utilization protein eutH
326	ENOG4105ENX	2	hydrolase
327	ENOG4105ENZ	2	Membrane
328	ENOG4105ENE	2	Histidine kinase
329	ENOG4105END	2	lipolytic protein G-D-S-L family
330	ENOG4105ENG	2	CRISPR-associated protein, Csy1 family
331	ENOG4105ENF	2	sensor Signal transduction histidine kinase
332	ENOG4105ENA	2	helicase
333	ENOG4105ENC	2	DNA mismatch repair protein MutS domain protein
334	ENOG4105ENB	2	ATPase involved in DNA replication initiation
335	ENOG4105ENM	2	Universal stress protein
336	ENOG4105ENN	2	converts alpha-aldose to the beta-anomer. It is active on D-glucose, L-arabinose, D-xylose, D-galactose, maltose and lactose (By similarity)
337	ENOG4105ENI	2	DNA helicase
338	ENOG4105ENH	2	Sulfatase
339	ENOG4105ENK	2	ABC transporter, permease
340	ENOG4105ENJ	2	RND efflux system, outer membrane lipoprotein
341	ENOG4105EN5	2	repeat protein
342	ENOG4105EN4	2	Integrase
343	ENOG4105EN7	2	major facilitator superfamily
344	ENOG4105EN6	2	Membrane
345	ENOG4105EN3	2	adenine specific DNA methyltransferase
346	ENOG4105EN2	2	IstB domain-containing protein ATP-binding protein
347	ENOG4105EN9	2	uBA THIF-type NAD FAD binding
348	ENOG4105EN8	2	Extracellular solute-binding protein, family 5
349	ENOG4105F7A	2	domain protein
350	ENOG4105F7G	2	Chitodextrinase
351	ENOG4107PXM	2	NDH-1 shuttles electrons from NADH, via FMN and iron- sulfur (Fe-S) centers, to quinones in the respiratory chain. The immediate electron acceptor for the enzyme in this species is believed to be a menaquinone. Couples the redox reaction to proton translocation (for every two electrons transferred, four hydrogen ions are translocated across the cytoplasmic membrane), and thus conserves the redox energy in a proton gradient (By similarity)
352	ENOG4107AC4	2	Pfam:PhdYeFM
353	ENOG4107ACH	2	E3 binding domain protein
354	ENOG4106MFV	2	virulence plasmid
355	ENOG4106MFD	2	gCN5-related N-acetyltransferase
356	ENOG4106MFB	2	Bacterial regulatory proteins, tetR family
357	ENOG4106MFK	2	Oligogalacturonate-specific porin protein (KdgM)
358	ENOG4106MF9	2	amino acid
359	ENOG410726S	2	MspA
360	ENOG4107HF0	2	Cyclic nucleotide-binding domain
361	ENOG4107269	2	Penicillin binding protein transpeptidase domain
362	ENOG4107N0F	2	MarR family Transcriptional regulator
363	ENOG4107N0B	2	HTH_MARR
364	ENOG4107N0C	2	K08084 type IV fimbrial biogenesis protein FimT
365	ENOG4107N0A	2	Flagellar basal body-associated protein FliL
366	ENOG4107N0N	2	Inherit from NOG: Cellulase (glycosyl hydrolase family 5)
367	ENOG4107N0S	2	AraC-like ligand binding domain
368	ENOG4107N0P	2	Transglycosylase associated protein
369	ENOG4107N0X	2	Sel1 repeat
370	ENOG410718S	2	Protein of unknown function (DUF1367)
371	ENOG410718T	2	Aminotransferase class I and II
372	ENOG410718H	2	heme exporter protein B
373	ENOG410718J	2	Thioredoxin
374	ENOG410718M	2	HTH_ARAC
375	ENOG410718N	2	His Kinase A (phospho-acceptor) domain
376	ENOG410718E	2	Inherit from COG: addiction module antidote protein
377	ENOG4108WP2	2	Pfam:Transposase_17
378	ENOG4108WP3	2	exonuclease RNase T and DNA polymerase III
379	ENOG4108WP0	2	Cell envelope-related transcriptional attenuator domain
380	ENOG4108WP1	2	Histidine kinase
381	ENOG4108WP6	2	protein tyrosine serine phosphatase
382	ENOG4108WP7	2	Transcriptional regulator, MarR family
383	ENOG4108WP8	2	short-chain dehydrogenase reductase
384	ENOG4108WP9	2	Replication Protein
385	ENOG4108WPP	2	Glyoxalase Bleomycin resistance protein (Dioxygenase
386	ENOG4108WPQ	2	Protein of unknown function, DUF481
387	ENOG4108WPW	2	transcriptional regulator, PucR family
388	ENOG4108WPT	2	Radical SAM superfamily
389	ENOG4108WPU	2	DNA polymerase III subunit psi
390	ENOG4108WPZ	2	methyltransferase, type 11
391	ENOG4108WPX	2	Membrane
392	ENOG4108WPY	2	collagen triple helix repeat-containing protein
393	ENOG4108WPC	2	Methyltransferase, type 11
394	ENOG4108WPG	2	ABC-2 type transporter
395	ENOG4108WPD	2	ROK family
396	ENOG4108WPE	2	(LipO)protein
397	ENOG4108WPJ	2	Ferritin-like domain
398	ENOG4108WPK	2	Transposase
399	ENOG4108WPH	2	sigma 54 modulation protein ribosomal protein S30EA
400	ENOG4108WPN	2	Signal peptide
401	ENOG4108WPM	2	protocatechuate 4,5-dioxygenase subunit alpha
402	ENOG4108YA0	2	cysteine dioxygenase
403	ENOG4108YA9	2	YqcI/YcgG family
404	ENOG4108YA8	2	lysozyme
405	ENOG4107N04	2	TfoX C-terminal domain
406	ENOG4107HFB	2	Protein of unknown function (DUF3021)
407	ENOG4106QHX	2	Uncharacterized protein conserved in bacteria (DUF2169)
408	ENOG4107HFI	2	Inherit from NOG: Sporulation domain protein
409	ENOG4108YAT	2	Nudix Hydrolase
410	ENOG4105NJ7	2	s-adenosyl-methyltransferase mraw
411	ENOG4105NJ4	2	nudix hydrolase
412	ENOG4105NJ0	2	GAF sensor signal transduction histidine kinase
413	ENOG4105NJW	2	AraC Family Transcriptional Regulator
414	ENOG4105NJJ	2	-acetyltransferase
415	ENOG4105NJK	2	type I restriction-modification system, specificity subunit
416	ENOG4105NJF	2	merr family transcriptional regulator
417	ENOG4105NJD	2	Acetoacetyl-CoA reductase
418	ENOG4107BI1	2	replication protein A
419	ENOG4107BI2	2	Reductive dehalogenase anchoring protein
420	ENOG4108AE3	2	FecR protein
421	ENOG4108AE2	2	Inherit from COG: acetyltransferase
422	ENOG4108AE1	2	CAAX protease self-immunity
423	ENOG4108AEV	2	Transposase
424	ENOG4105G3K	2	Radical SAM superfamily
425	ENOG4108AEU	2	PLDc
426	ENOG4108AEQ	2	Phosphotransferase enzyme family
427	ENOG4108AEP	2	Prolipoprotein diacylglyceryl transferase
428	ENOG4105G3R	2	Polysaccharide deacetylase
429	ENOG4105G3Y	2	Monovalent cation H antiporter subunit C
430	ENOG4105G37	2	Transcriptional regulator
431	ENOG4105G30	2	Gas vesicle
432	ENOG4105SDR	2	Outer membrane protein OmpT
433	ENOG4106FNR	2	ATP cone domain
434	ENOG4106FNV	2	Flagellar assembly protein
435	ENOG4106FNY	2	Bacteriophage, scaffolding protein
436	ENOG4106FNB	2	EamA-like transporter family
437	ENOG4106FNG	2	ParB domain protein nuclease
438	ENOG4106FND	2	NAD dependent epimerase dehydratase family
439	ENOG4106FNI	2	ParB-like nuclease domain
440	ENOG4106FNM	2	Domain of unknown function (DUF1836)
441	ENOG4106FN3	2	tellurium resistance protein
442	ENOG4106FN0	2	K07480 insertion element IS1 protein InsB
443	ENOG4106FN7	2	HTH_XRE
444	ENOG4106FN5	2	Protein of unknown function (DUF3278)
445	ENOG4106FN4	2	Endonuclease Exonuclease phosphatase
446	ENOG4106FN8	2	Predicted membrane-bound metal-dependent hydrolase (DUF457)
447	ENOG4108B30	2	Pfam:DUF419
448	ENOG4108B31	2	Spore germination protein
449	ENOG4108B36	2	FlgN protein
450	ENOG4108B38	2	PP2Cc
451	ENOG4108B39	2	Inherit from COG: YD repeat protein
452	ENOG4108B3B	2	Inherit from COG: ATPase (AAA superfamily)-like protein
453	ENOG4108B3A	2	Activator of Hsp90 ATPase homolog 1-like protein
454	ENOG4108B3D	2	feoA family
455	ENOG4107IPH	2	Sigma-70 region 2 
456	ENOG4108GRC	2	Pfam:DUF820
457	ENOG4108GRD	2	Pfam:UPF0005
458	ENOG4108GRX	2	Protein of unknown function (DUF3738)
459	ENOG4108GRY	2	VirB8 protein
460	ENOG4108GRZ	2	Cna protein B-type domain
461	ENOG4108GRR	2	Bacterial protein of unknown function (DUF937)
462	ENOG4108GRU	2	Pfam:Muc_lac_enz
463	ENOG4108GRV	2	DinB family
464	ENOG4108GR0	2	3-hydroxyacyl-CoA dehydrogenase NAD-binding protein
465	ENOG4107IPD	2	Protein tyrosine kinase
466	ENOG4107IPF	2	YhjQ protein
467	ENOG4107IPZ	2	Peptidase M15 
468	ENOG4108XYN	2	Tetr family transcriptional regulator
469	ENOG4108XYM	2	Pfam:DUF1821
470	ENOG4108XYF	2	Protein of unknown function (DUF3089)
471	ENOG4108XYG	2	Gcn5-related n-acetyltransferase
472	ENOG4108XYD	2	Inherit from COG: phosphate abc transporter
473	ENOG4108XYE	2	Thioesterase
474	ENOG4108XYC	2	methyl-accepting chemotaxis
475	ENOG4108XYA	2	glycerophosphoryl diester phosphodiesterase
476	ENOG4108XYZ	2	transcriptional regulator
477	ENOG4108XYX	2	Putative neutral zinc metallopeptidase
478	ENOG4108XYU	2	Short-chain dehydrogenase reductase Sdr
479	ENOG4108XYS	2	)-transporter
480	ENOG4108XY8	2	activator of Hsp90 ATPase 1 family protein
481	ENOG4108XY9	2	(Anaerobic) ribonucleoside-triphosphate reductase activating protein
482	ENOG4108XY7	2	type IV pilus assembly pilz
483	ENOG4108XY5	2	MaoC like domain
484	ENOG4108XY2	2	Oxidoreductase domain protein
485	ENOG4108XY1	2	Glyoxalase Bleomycin resistance protein (Dioxygenase
486	ENOG4106TJ5	2	integral membrane protein
487	ENOG4106TJI	2	Aldehyde dehydrogenase family
488	ENOG4107IP7	2	Membrane protein of unknown function
489	ENOG4106TJD	2	NAD-dependent glycerol-3-phosphate dehydrogenase C-terminus
490	ENOG4107IP6	2	HEAT repeat
491	ENOG4106TJZ	2	Ferredoxin-dependent bilin reductase
492	ENOG4106TJS	2	Protein of unknown function (DUF1559)
493	ENOG4107IIR	2	Pfam:PhdYeFM
494	ENOG4107IIY	2	TadE-like protein
495	ENOG4105S6F	2	ECF subfamily RNA polymerase, sigma-24
496	ENOG4105S6E	2	Inherit from NOG: Conserved hypothetical, protein
497	ENOG4105S6I	2	transcriptional repressor, copy family
498	ENOG4105S6H	2	anti-sigma regulatory factor serine threonine protein kinase
499	ENOG4105S6S	2	Invasion gene expression up-regulator, SirB
500	ENOG4105S6R	2	Iron-hydroxamate transporter permease subunit
\.


--
-- Name: ogs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dblyon
--

SELECT pg_catalog.setval('ogs_id_seq', 1, false);


--
-- Data for Name: ontologies; Type: TABLE DATA; Schema: public; Owner: dblyon
--

COPY ontologies (id, child, parent, direct) FROM stdin;
1	287144	11308	0
2	287144	1	0
3	287144	119210	1
4	287144	439488	0
5	287144	10239	0
6	287144	35301	0
7	287144	197911	0
8	287144	11320	0
9	378467	33090	0
10	378467	4272	1
11	378467	91827	0
12	378467	1437201	0
13	378467	131221	0
14	378467	58024	0
15	378467	71275	0
16	378467	3398	0
17	378467	71243	0
18	378467	35493	0
19	378467	71240	0
20	378467	78536	0
21	378467	1437183	0
22	378467	91835	0
23	378467	3193	0
24	378467	26000	0
25	378467	1	0
26	378467	58023	0
27	378467	131567	0
28	378467	2759	0
29	378464	33090	0
30	378464	58023	0
31	378464	91827	0
32	378464	1437201	0
33	378464	131221	0
34	378464	58024	0
35	378464	71275	0
36	378464	3398	0
37	378464	71243	0
38	378464	35493	0
39	378464	71240	0
40	378464	26005	1
41	378464	1437183	0
42	378464	91835	0
43	378464	3193	0
44	378464	26000	0
45	378464	1	0
46	378464	131567	0
47	378464	78536	0
48	378464	2759	0
49	378465	33090	0
50	378465	58023	0
51	378465	91827	0
52	378465	1437201	0
53	378465	131221	0
54	378465	58024	0
55	378465	71275	0
56	378465	3398	0
57	378465	71243	0
58	378465	35493	0
59	378465	71240	0
60	378465	26005	1
61	378465	1437183	0
62	378465	91835	0
63	378465	3193	0
64	378465	26000	0
65	378465	1	0
66	378465	131567	0
67	378465	78536	0
68	378465	2759	0
69	378462	33090	0
70	378462	58023	0
71	378462	91827	0
72	378462	1437201	0
73	378462	131221	0
74	378462	58024	0
75	378462	71275	0
76	378462	3398	0
77	378462	71243	0
78	378462	35493	0
79	378462	71240	0
80	378462	26005	1
81	378462	1437183	0
82	378462	91835	0
83	378462	3193	0
84	378462	26000	0
85	378462	1	0
86	378462	131567	0
87	378462	78536	0
88	378462	2759	0
89	287141	11308	0
90	287141	1	0
91	287141	119210	1
92	287141	439488	0
93	287141	10239	0
94	287141	35301	0
95	287141	197911	0
96	287141	11320	0
97	287142	11308	0
98	287142	1	0
99	287142	119210	1
100	287142	439488	0
101	287142	10239	0
102	287142	35301	0
103	287142	197911	0
104	287142	11320	0
105	287145	11308	0
106	287145	1	0
107	287145	119210	1
108	287145	439488	0
109	287145	10239	0
110	287145	35301	0
111	287145	197911	0
112	287145	11320	0
113	287148	11308	0
114	287148	1	0
115	287148	119210	1
116	287148	439488	0
117	287148	10239	0
118	287148	35301	0
119	287148	197911	0
120	287148	11320	0
121	287149	11308	0
122	287149	1	0
123	287149	119210	1
124	287149	439488	0
125	287149	10239	0
126	287149	35301	0
127	287149	197911	0
128	287149	11320	0
129	378468	33090	0
130	378468	58023	0
131	378468	91827	0
132	378468	1437201	0
133	378468	131221	0
134	378468	58024	0
135	378468	71275	0
136	378468	3398	0
137	378468	71243	0
138	378468	35493	0
139	378468	71240	0
140	378468	78536	0
141	378468	1437183	0
142	378468	91835	0
143	378468	140412	1
144	378468	26000	0
145	378468	3193	0
146	378468	1	0
147	378468	131567	0
148	378468	2759	0
149	378469	33090	0
150	378469	58023	0
151	378469	91827	0
152	378469	1437201	0
153	378469	131221	0
154	378469	58024	0
155	378469	71275	0
156	378469	3398	0
157	378469	71243	0
158	378469	35493	0
159	378469	71240	0
160	378469	78536	0
161	378469	1437183	0
162	378469	91835	0
163	378469	140412	1
164	378469	26000	0
165	378469	3193	0
166	378469	1	0
167	378469	131567	0
168	378469	2759	0
169	89370	6340	0
170	89370	6383	0
171	89370	33208	0
172	89370	33213	0
173	89370	1206795	0
174	89370	131567	0
175	89370	33317	0
176	89370	1	0
177	89370	6381	0
178	89370	6072	0
179	89370	42113	0
180	89370	6382	0
181	89370	33154	0
182	89370	6389	1
183	89370	6388	0
184	89370	2759	0
185	89371	641	0
186	89371	1	0
187	89371	1236	0
188	89371	1224	0
189	89371	87806	1
190	89371	2	0
191	89371	662	0
192	89371	135623	0
193	89371	131567	0
194	89372	31989	0
195	89372	1	0
196	89372	1224	0
197	89372	204455	0
198	89372	2	0
199	89372	131567	0
200	89372	58841	1
201	89372	28211	0
202	89373	2	0
203	89373	976	0
204	89373	768503	0
205	89373	768507	1
206	89373	1783270	0
207	89373	1	0
208	89373	131567	0
209	89373	68336	0
210	89374	2	0
211	89374	976	0
212	89374	1853228	0
213	89374	1853229	1
214	89374	1783270	0
215	89374	1	0
216	89374	131567	0
217	89374	68336	0
218	89376	41297	0
219	89376	1	0
220	89376	1224	0
221	89376	204457	0
222	89376	2	0
223	89376	41298	0
224	89376	131567	0
225	89376	122612	1
226	89376	28211	0
227	89377	135618	1
228	89377	1	0
229	89377	1236	0
230	89377	2	0
231	89377	1224	0
232	89377	131567	0
233	89378	33208	0
234	89378	33511	0
235	89378	9347	0
236	89378	337687	0
237	89378	33553	0
238	89378	1338369	0
239	89378	314147	0
240	89378	8287	0
241	89378	40674	0
242	89378	52801	1
243	89378	9989	0
244	89378	117571	0
245	89378	117570	0
246	89378	131567	0
247	89378	33213	0
248	89378	7711	0
249	89378	1	0
250	89378	337673	0
251	89378	314146	0
252	89378	7742	0
253	89378	7776	0
254	89378	1437010	0
255	89378	6072	0
256	89378	89593	0
257	89378	33154	0
258	89378	32525	0
259	89378	32524	0
260	89378	32523	0
261	89378	2759	0
262	89379	33208	0
263	89379	33511	0
264	89379	9347	0
265	89379	337687	0
266	89379	33553	0
267	89379	1338369	0
268	89379	314147	0
269	89379	8287	0
270	89379	40674	0
271	89379	52801	0
272	89379	89378	1
273	89379	9989	0
274	89379	117571	0
275	89379	117570	0
276	89379	131567	0
277	89379	33213	0
278	89379	7711	0
279	89379	1	0
280	89379	337673	0
281	89379	314146	0
282	89379	7742	0
283	89379	7776	0
284	89379	1437010	0
285	89379	6072	0
286	89379	89593	0
287	89379	33154	0
288	89379	32525	0
289	89379	32524	0
290	89379	32523	0
291	89379	2759	0
292	378463	33090	0
293	378463	58023	0
294	378463	91827	0
295	378463	1437201	0
296	378463	131221	0
297	378463	58024	0
298	378463	71275	0
299	378463	3398	0
300	378463	71243	0
301	378463	35493	0
302	378463	71240	0
303	378463	26005	1
304	378463	1437183	0
305	378463	91835	0
306	378463	3193	0
307	378463	26000	0
308	378463	1	0
309	378463	131567	0
310	378463	78536	0
311	378463	2759	0
312	378460	33090	0
313	378460	58023	0
314	378460	91827	0
315	378460	1437201	0
316	378460	131221	0
317	378460	58024	0
318	378460	71275	0
319	378460	3398	0
320	378460	71243	0
321	378460	35493	0
322	378460	71240	0
323	378460	26005	1
324	378460	1437183	0
325	378460	91835	0
326	378460	3193	0
327	378460	26000	0
328	378460	1	0
329	378460	131567	0
330	378460	78536	0
331	378460	2759	0
332	378461	33090	0
333	378461	58023	0
334	378461	91827	0
335	378461	1437201	0
336	378461	131221	0
337	378461	58024	0
338	378461	71275	0
339	378461	3398	0
340	378461	71243	0
341	378461	35493	0
342	378461	71240	0
343	378461	26005	1
344	378461	1437183	0
345	378461	91835	0
346	378461	3193	0
347	378461	26000	0
348	378461	1	0
349	378461	131567	0
350	378461	78536	0
351	378461	2759	0
352	1758239	33208	0
353	1758239	9479	0
354	1758239	314293	0
355	1758239	9347	0
356	1758239	9443	0
357	1758239	376913	0
358	1758239	1338369	0
359	1758239	9498	0
360	1758239	8287	0
361	1758239	40674	0
362	1758239	117571	0
363	1758239	117570	0
364	1758239	9480	0
365	1758239	9494	1
366	1758239	131567	0
367	1758239	33213	0
368	1758239	7711	0
369	1758239	1	0
370	1758239	314146	0
371	1758239	7742	0
372	1758239	7776	0
373	1758239	1437010	0
374	1758239	6072	0
375	1758239	89593	0
376	1758239	33511	0
377	1758239	33154	0
378	1758239	32525	0
379	1758239	32524	0
380	1758239	32523	0
381	1758239	2759	0
382	244768	33090	0
383	244768	58023	0
384	244768	91827	0
385	244768	1437201	0
386	244768	1003876	1
387	244768	58024	0
388	244768	71275	0
389	244768	3398	0
390	244768	78536	0
391	244768	35493	0
392	244768	71240	0
393	244768	1	0
394	244768	1437183	0
395	244768	91835	0
396	244768	3193	0
397	244768	71239	0
398	244768	131221	0
399	244768	3650	0
400	244768	131567	0
401	244768	2759	0
402	1698377	1	0
403	1698377	976	0
404	1698377	2	0
405	1698377	1783270	0
406	1698377	68336	0
407	1698377	237	1
408	1698377	131567	0
409	1698377	49546	0
410	1698377	200644	0
411	1698377	117743	0
412	1698376	1	0
413	1698376	976	0
414	1698376	2	0
415	1698376	1783270	0
416	1698376	68336	0
417	1698376	237	1
418	1698376	131567	0
419	1698376	49546	0
420	1698376	200644	0
421	1698376	117743	0
422	1698375	1	0
423	1698375	976	0
424	1698375	2	0
425	1698375	1783270	0
426	1698375	68336	0
427	1698375	237	1
428	1698375	131567	0
429	1698375	49546	0
430	1698375	200644	0
431	1698375	117743	0
432	1698374	1	0
433	1698374	976	0
434	1698374	2	0
435	1698374	1783270	0
436	1698374	68336	0
437	1698374	237	1
438	1698374	131567	0
439	1698374	49546	0
440	1698374	200644	0
441	1698374	117743	0
442	1698373	1	0
443	1698373	976	0
444	1698373	2	0
445	1698373	1783270	0
446	1698373	68336	0
447	1698373	237	1
448	1698373	131567	0
449	1698373	49546	0
450	1698373	200644	0
451	1698373	117743	0
452	1698372	1	0
453	1698372	976	0
454	1698372	2	0
455	1698372	1783270	0
456	1698372	68336	0
457	1698372	237	1
458	1698372	131567	0
459	1698372	49546	0
460	1698372	200644	0
461	1698372	117743	0
462	1698371	2	0
463	1698371	1	0
464	1698371	267889	0
465	1698371	1224	0
466	1698371	28228	1
467	1698371	131567	0
468	1698371	1236	0
469	1698371	135622	0
470	1698370	1	0
471	1698370	85023	0
472	1698370	110934	1
473	1698370	2	0
474	1698370	1760	0
475	1698370	1783272	0
476	1698370	85006	0
477	1698370	131567	0
478	1698370	201174	0
479	1698379	1	0
480	1698379	976	0
481	1698379	2	0
482	1698379	1783270	0
483	1698379	68336	0
484	1698379	237	1
485	1698379	131567	0
486	1698379	49546	0
487	1698379	200644	0
488	1698379	117743	0
489	1698378	1	0
490	1698378	976	0
491	1698378	2	0
492	1698378	1783270	0
493	1698378	68336	0
494	1698378	237	1
495	1698378	131567	0
496	1698378	49546	0
497	1698378	200644	0
498	1698378	117743	0
499	UPK:0654	UPK:9991	0
500	UPK:0654	UPK:0325	1
\.


--
-- Name: ontologies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dblyon
--

SELECT pg_catalog.setval('ontologies_id_seq', 1, false);


--
-- Data for Name: peptides; Type: TABLE DATA; Schema: public; Owner: dblyon
--

COPY peptides (id, aaseq, an, missedcleavages, length) FROM stdin;
1	MTMDKSELVQK	P31946	1	11
2	MTMDKSELVQKAK	P31946	2	13
3	TMDKSELVQK	P31946	1	10
4	TMDKSELVQKAK	P31946	2	12
5	SELVQKAK	P31946	1	8
6	SELVQKAKLAEQAER	P31946	2	15
7	AKLAEQAER	P31946	1	9
8	AKLAEQAERYDDMAAAMK	P31946	2	18
9	LAEQAER	P31946	0	7
10	LAEQAERYDDMAAAMK	P31946	1	16
11	LAEQAERYDDMAAAMKAVTEQGHELSNEER	P31946	2	30
12	YDDMAAAMK	P31946	0	9
13	YDDMAAAMKAVTEQGHELSNEER	P31946	1	23
14	YDDMAAAMKAVTEQGHELSNEERNLLSVAYK	P31946	2	31
15	AVTEQGHELSNEER	P31946	0	14
16	AVTEQGHELSNEERNLLSVAYK	P31946	1	22
17	AVTEQGHELSNEERNLLSVAYKNVVGAR	P31946	2	28
18	NLLSVAYK	P31946	0	8
19	NLLSVAYKNVVGAR	P31946	1	14
20	NLLSVAYKNVVGARR	P31946	2	15
21	NVVGARR	P31946	1	7
22	NVVGARRSSWR	P31946	2	11
23	RSSWRVISSIEQK	P31946	2	13
24	SSWRVISSIEQK	P31946	1	12
25	SSWRVISSIEQKTER	P31946	2	15
26	VISSIEQK	P31946	0	8
27	VISSIEQKTER	P31946	1	11
28	VISSIEQKTERNEK	P31946	2	14
29	TERNEKK	P31946	2	7
30	NEKKQQMGK	P31946	2	9
31	KQQMGKEYR	P31946	2	9
32	QQMGKEYR	P31946	1	8
33	QQMGKEYREK	P31946	2	10
34	EYREKIEAELQDICNDVLELLDK	P31946	2	23
35	EKIEAELQDICNDVLELLDK	P31946	1	20
36	EKIEAELQDICNDVLELLDKYLIPNATQPESK	P31946	2	32
37	IEAELQDICNDVLELLDK	P31946	0	18
38	IEAELQDICNDVLELLDKYLIPNATQPESK	P31946	1	30
39	IEAELQDICNDVLELLDKYLIPNATQPESKVFYLK	P31946	2	35
40	YLIPNATQPESK	P31946	0	12
41	YLIPNATQPESKVFYLK	P31946	1	17
42	YLIPNATQPESKVFYLKMK	P31946	2	19
43	VFYLKMK	P31946	1	7
44	VFYLKMKGDYFR	P31946	2	12
45	MKGDYFR	P31946	1	7
46	MKGDYFRYLSEVASGDNK	P31946	2	18
47	GDYFRYLSEVASGDNK	P31946	1	16
48	GDYFRYLSEVASGDNKQTTVSNSQQAYQEAFEISK	P31946	2	35
49	YLSEVASGDNK	P31946	0	11
50	YLSEVASGDNKQTTVSNSQQAYQEAFEISK	P31946	1	30
51	YLSEVASGDNKQTTVSNSQQAYQEAFEISKK	P31946	2	31
52	QTTVSNSQQAYQEAFEISK	P31946	0	19
53	QTTVSNSQQAYQEAFEISKK	P31946	1	20
54	QTTVSNSQQAYQEAFEISKKEMQPTHPIR	P31946	2	29
55	KEMQPTHPIR	P31946	1	10
56	KEMQPTHPIRLGLALNFSVFYYEILNSPEK	P31946	2	30
57	EMQPTHPIR	P31946	0	9
58	EMQPTHPIRLGLALNFSVFYYEILNSPEK	P31946	1	29
59	EMQPTHPIRLGLALNFSVFYYEILNSPEKACSLAK	P31946	2	35
60	LGLALNFSVFYYEILNSPEK	P31946	0	20
61	LGLALNFSVFYYEILNSPEKACSLAK	P31946	1	26
62	LGLALNFSVFYYEILNSPEKACSLAKTAFDEAIAELDTLNEESYK	P31946	2	45
63	ACSLAKTAFDEAIAELDTLNEESYK	P31946	1	25
64	ACSLAKTAFDEAIAELDTLNEESYKDSTLIMQLLR	P31946	2	35
65	TAFDEAIAELDTLNEESYK	P31946	0	19
66	TAFDEAIAELDTLNEESYKDSTLIMQLLR	P31946	1	29
67	TAFDEAIAELDTLNEESYKDSTLIMQLLRDNLTLWTSENQGDEGDAGEGEN	P31946	2	51
68	DSTLIMQLLR	P31946	0	10
69	DSTLIMQLLRDNLTLWTSENQGDEGDAGEGEN	P31946	1	32
70	DNLTLWTSENQGDEGDAGEGEN	P31946	0	22
71	MAVMAPR	P04439	0	7
72	MAVMAPRTLLLLLSGALALTQTWAGSHSMR	P04439	1	30
73	MAVMAPRTLLLLLSGALALTQTWAGSHSMRYFFTSVSRPGR	P04439	2	41
74	AVMAPRTLLLLLSGALALTQTWAGSHSMR	P04439	1	29
75	AVMAPRTLLLLLSGALALTQTWAGSHSMRYFFTSVSRPGR	P04439	2	40
76	TLLLLLSGALALTQTWAGSHSMR	P04439	0	23
77	TLLLLLSGALALTQTWAGSHSMRYFFTSVSRPGR	P04439	1	34
78	TLLLLLSGALALTQTWAGSHSMRYFFTSVSRPGRGEPR	P04439	2	38
79	YFFTSVSRPGR	P04439	0	11
80	YFFTSVSRPGRGEPR	P04439	1	15
81	YFFTSVSRPGRGEPRFIAVGYVDDTQFVR	P04439	2	29
82	GEPRFIAVGYVDDTQFVR	P04439	1	18
83	GEPRFIAVGYVDDTQFVRFDSDAASQR	P04439	2	27
84	FIAVGYVDDTQFVR	P04439	0	14
85	FIAVGYVDDTQFVRFDSDAASQR	P04439	1	23
86	FIAVGYVDDTQFVRFDSDAASQRMEPR	P04439	2	27
87	FDSDAASQR	P04439	0	9
88	FDSDAASQRMEPR	P04439	1	13
89	FDSDAASQRMEPRAPWIEQEGPEYWDQETR	P04439	2	30
90	MEPRAPWIEQEGPEYWDQETR	P04439	1	21
91	MEPRAPWIEQEGPEYWDQETRNVK	P04439	2	24
92	APWIEQEGPEYWDQETR	P04439	0	17
93	APWIEQEGPEYWDQETRNVK	P04439	1	20
94	APWIEQEGPEYWDQETRNVKAQSQTDR	P04439	2	27
95	NVKAQSQTDR	P04439	1	10
96	NVKAQSQTDRVDLGTLR	P04439	2	17
97	AQSQTDR	P04439	0	7
98	AQSQTDRVDLGTLR	P04439	1	14
99	AQSQTDRVDLGTLRGYYNQSEAGSHTIQIMYGCDVGSDGR	P04439	2	40
100	VDLGTLR	P04439	0	7
101	VDLGTLRGYYNQSEAGSHTIQIMYGCDVGSDGR	P04439	1	33
102	VDLGTLRGYYNQSEAGSHTIQIMYGCDVGSDGRFLR	P04439	2	36
103	GYYNQSEAGSHTIQIMYGCDVGSDGR	P04439	0	26
104	GYYNQSEAGSHTIQIMYGCDVGSDGRFLR	P04439	1	29
105	GYYNQSEAGSHTIQIMYGCDVGSDGRFLRGYR	P04439	2	32
106	FLRGYRQDAYDGK	P04439	2	13
107	GYRQDAYDGK	P04439	1	10
108	GYRQDAYDGKDYIALNEDLR	P04439	2	20
109	QDAYDGK	P04439	0	7
110	QDAYDGKDYIALNEDLR	P04439	1	17
111	QDAYDGKDYIALNEDLRSWTAADMAAQITK	P04439	2	30
112	DYIALNEDLR	P04439	0	10
113	DYIALNEDLRSWTAADMAAQITK	P04439	1	23
114	DYIALNEDLRSWTAADMAAQITKR	P04439	2	24
115	SWTAADMAAQITK	P04439	0	13
116	SWTAADMAAQITKR	P04439	1	14
117	SWTAADMAAQITKRK	P04439	2	15
118	RKWEAAHEAEQLR	P04439	2	13
119	KWEAAHEAEQLR	P04439	1	12
120	KWEAAHEAEQLRAYLDGTCVEWLR	P04439	2	24
121	WEAAHEAEQLR	P04439	0	11
122	WEAAHEAEQLRAYLDGTCVEWLR	P04439	1	23
123	WEAAHEAEQLRAYLDGTCVEWLRR	P04439	2	24
124	AYLDGTCVEWLR	P04439	0	12
125	AYLDGTCVEWLRR	P04439	1	13
126	AYLDGTCVEWLRRYLENGK	P04439	2	19
127	RYLENGK	P04439	1	7
128	RYLENGKETLQR	P04439	2	12
129	YLENGKETLQR	P04439	1	11
130	YLENGKETLQRTDPPK	P04439	2	16
131	ETLQRTDPPK	P04439	1	10
132	ETLQRTDPPKTHMTHHPISDHEATLR	P04439	2	26
133	TDPPKTHMTHHPISDHEATLR	P04439	1	21
134	TDPPKTHMTHHPISDHEATLRCWALGFYPAEITLTWQR	P04439	2	38
135	THMTHHPISDHEATLR	P04439	0	16
136	THMTHHPISDHEATLRCWALGFYPAEITLTWQR	P04439	1	33
137	THMTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQK	P04439	2	57
138	CWALGFYPAEITLTWQR	P04439	0	17
139	CWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQK	P04439	1	41
140	CWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQR	P04439	2	54
141	DGEDQTQDTELVETRPAGDGTFQK	P04439	0	24
142	DGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQR	P04439	1	37
143	DGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLR	P04439	2	54
144	WAAVVVPSGEEQR	P04439	0	13
145	WAAVVVPSGEEQRYTCHVQHEGLPKPLTLR	P04439	1	30
146	WAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWELSSQPTIPIVGIIAGLVLLGAVITGAVVAAVMWR	P04439	2	66
147	YTCHVQHEGLPKPLTLR	P04439	0	17
148	YTCHVQHEGLPKPLTLRWELSSQPTIPIVGIIAGLVLLGAVITGAVVAAVMWR	P04439	1	53
149	YTCHVQHEGLPKPLTLRWELSSQPTIPIVGIIAGLVLLGAVITGAVVAAVMWRR	P04439	2	54
150	WELSSQPTIPIVGIIAGLVLLGAVITGAVVAAVMWR	P04439	0	36
151	WELSSQPTIPIVGIIAGLVLLGAVITGAVVAAVMWRR	P04439	1	37
152	WELSSQPTIPIVGIIAGLVLLGAVITGAVVAAVMWRRK	P04439	2	38
153	SSDRKGGSYTQAASSDSAQGSDVSLTACK	P04439	2	29
154	KGGSYTQAASSDSAQGSDVSLTACK	P04439	1	25
155	KGGSYTQAASSDSAQGSDVSLTACKV	P04439	2	26
156	GGSYTQAASSDSAQGSDVSLTACK	P04439	0	24
157	GGSYTQAASSDSAQGSDVSLTACKV	P04439	1	25
158	MLVMAPR	P01889	0	7
159	MLVMAPRTVLLLLSAALALTETWAGSHSMR	P01889	1	30
160	MLVMAPRTVLLLLSAALALTETWAGSHSMRYFYTSVSRPGR	P01889	2	41
161	LVMAPRTVLLLLSAALALTETWAGSHSMR	P01889	1	29
162	LVMAPRTVLLLLSAALALTETWAGSHSMRYFYTSVSRPGR	P01889	2	40
163	TVLLLLSAALALTETWAGSHSMR	P01889	0	23
164	TVLLLLSAALALTETWAGSHSMRYFYTSVSRPGR	P01889	1	34
165	TVLLLLSAALALTETWAGSHSMRYFYTSVSRPGRGEPR	P01889	2	38
166	YFYTSVSRPGR	P01889	0	11
167	YFYTSVSRPGRGEPR	P01889	1	15
168	YFYTSVSRPGRGEPRFISVGYVDDTQFVR	P01889	2	29
169	GEPRFISVGYVDDTQFVR	P01889	1	18
170	GEPRFISVGYVDDTQFVRFDSDAASPR	P01889	2	27
171	FISVGYVDDTQFVR	P01889	0	14
172	FISVGYVDDTQFVRFDSDAASPR	P01889	1	23
173	FISVGYVDDTQFVRFDSDAASPREEPR	P01889	2	27
174	FDSDAASPR	P01889	0	9
175	FDSDAASPREEPR	P01889	1	13
176	FDSDAASPREEPRAPWIEQEGPEYWDR	P01889	2	27
177	EEPRAPWIEQEGPEYWDR	P01889	1	18
178	EEPRAPWIEQEGPEYWDRNTQIYK	P01889	2	24
179	APWIEQEGPEYWDR	P01889	0	14
180	APWIEQEGPEYWDRNTQIYK	P01889	1	20
181	APWIEQEGPEYWDRNTQIYKAQAQTDR	P01889	2	27
182	NTQIYKAQAQTDR	P01889	1	13
183	NTQIYKAQAQTDRESLR	P01889	2	17
184	AQAQTDR	P01889	0	7
185	AQAQTDRESLR	P01889	1	11
186	AQAQTDRESLRNLR	P01889	2	14
187	ESLRNLR	P01889	1	7
188	ESLRNLRGYYNQSEAGSHTLQSMYGCDVGPDGR	P01889	2	33
189	NLRGYYNQSEAGSHTLQSMYGCDVGPDGR	P01889	1	29
190	NLRGYYNQSEAGSHTLQSMYGCDVGPDGRLLR	P01889	2	32
191	GYYNQSEAGSHTLQSMYGCDVGPDGR	P01889	0	26
192	GYYNQSEAGSHTLQSMYGCDVGPDGRLLR	P01889	1	29
193	GYYNQSEAGSHTLQSMYGCDVGPDGRLLRGHDQYAYDGK	P01889	2	39
194	LLRGHDQYAYDGK	P01889	1	13
195	LLRGHDQYAYDGKDYIALNEDLR	P01889	2	23
196	GHDQYAYDGK	P01889	0	10
197	GHDQYAYDGKDYIALNEDLR	P01889	1	20
198	GHDQYAYDGKDYIALNEDLRSWTAADTAAQITQR	P01889	2	34
199	DYIALNEDLR	P01889	0	10
200	DYIALNEDLRSWTAADTAAQITQR	P01889	1	24
201	DYIALNEDLRSWTAADTAAQITQRK	P01889	2	25
202	SWTAADTAAQITQR	P01889	0	14
203	SWTAADTAAQITQRK	P01889	1	15
204	SWTAADTAAQITQRKWEAAR	P01889	2	20
205	KWEAAREAEQR	P01889	2	11
206	WEAAREAEQR	P01889	1	10
207	WEAAREAEQRR	P01889	2	11
208	EAEQRRAYLEGECVEWLR	P01889	2	18
209	RAYLEGECVEWLR	P01889	1	13
210	RAYLEGECVEWLRR	P01889	2	14
211	AYLEGECVEWLR	P01889	0	12
212	AYLEGECVEWLRR	P01889	1	13
213	AYLEGECVEWLRRYLENGK	P01889	2	19
214	RYLENGK	P01889	1	7
215	RYLENGKDK	P01889	2	9
216	YLENGKDK	P01889	1	8
217	YLENGKDKLER	P01889	2	11
218	DKLERADPPK	P01889	2	10
219	LERADPPK	P01889	1	8
220	LERADPPKTHVTHHPISDHEATLR	P01889	2	24
221	ADPPKTHVTHHPISDHEATLR	P01889	1	21
222	ADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQR	P01889	2	38
223	THVTHHPISDHEATLR	P01889	0	16
437	FDSDAASPR	Q95365	0	9
224	THVTHHPISDHEATLRCWALGFYPAEITLTWQR	P01889	1	33
225	THVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDR	P01889	2	53
226	CWALGFYPAEITLTWQR	P01889	0	17
227	CWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDR	P01889	1	37
228	CWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQK	P01889	2	41
229	DGEDQTQDTELVETRPAGDR	P01889	0	20
230	DGEDQTQDTELVETRPAGDRTFQK	P01889	1	24
231	DGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQR	P01889	2	37
232	TFQKWAAVVVPSGEEQR	P01889	1	17
233	TFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLR	P01889	2	34
234	WAAVVVPSGEEQR	P01889	0	13
235	WAAVVVPSGEEQRYTCHVQHEGLPKPLTLR	P01889	1	30
236	WAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCR	P01889	2	66
237	YTCHVQHEGLPKPLTLR	P01889	0	17
238	YTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCR	P01889	1	53
239	YTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCRR	P01889	2	54
240	WEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCR	P01889	0	36
241	WEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCRR	P01889	1	37
242	WEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCRRK	P01889	2	38
243	RKSSGGK	P01889	2	7
244	KSSGGKGGSYSQAACSDSAQGSDVSLTA	P01889	2	28
245	SSGGKGGSYSQAACSDSAQGSDVSLTA	P01889	1	27
246	GGSYSQAACSDSAQGSDVSLTA	P01889	0	22
247	MRVTAPR	P30464	1	7
248	MRVTAPRTVLLLLSGALALTETWAGSHSMR	P30464	2	30
249	RVTAPRTVLLLLSGALALTETWAGSHSMR	P30464	2	29
250	VTAPRTVLLLLSGALALTETWAGSHSMR	P30464	1	28
251	VTAPRTVLLLLSGALALTETWAGSHSMRYFYTAMSRPGR	P30464	2	39
252	TVLLLLSGALALTETWAGSHSMR	P30464	0	23
253	TVLLLLSGALALTETWAGSHSMRYFYTAMSRPGR	P30464	1	34
254	TVLLLLSGALALTETWAGSHSMRYFYTAMSRPGRGEPR	P30464	2	38
255	YFYTAMSRPGR	P30464	0	11
256	YFYTAMSRPGRGEPR	P30464	1	15
257	YFYTAMSRPGRGEPRFIAVGYVDDTQFVR	P30464	2	29
258	GEPRFIAVGYVDDTQFVR	P30464	1	18
259	GEPRFIAVGYVDDTQFVRFDSDAASPR	P30464	2	27
260	FIAVGYVDDTQFVR	P30464	0	14
261	FIAVGYVDDTQFVRFDSDAASPR	P30464	1	23
262	FIAVGYVDDTQFVRFDSDAASPRMAPR	P30464	2	27
263	FDSDAASPR	P30464	0	9
264	FDSDAASPRMAPR	P30464	1	13
265	FDSDAASPRMAPRAPWIEQEGPEYWDR	P30464	2	27
266	MAPRAPWIEQEGPEYWDR	P30464	1	18
267	MAPRAPWIEQEGPEYWDRETQISK	P30464	2	24
268	APWIEQEGPEYWDR	P30464	0	14
269	APWIEQEGPEYWDRETQISK	P30464	1	20
270	APWIEQEGPEYWDRETQISKTNTQTYR	P30464	2	27
271	ETQISKTNTQTYR	P30464	1	13
272	ETQISKTNTQTYRESLR	P30464	2	17
273	TNTQTYR	P30464	0	7
274	TNTQTYRESLR	P30464	1	11
275	TNTQTYRESLRNLR	P30464	2	14
276	ESLRNLR	P30464	1	7
277	ESLRNLRGYYNQSEAGSHTLQR	P30464	2	22
278	NLRGYYNQSEAGSHTLQR	P30464	1	18
279	NLRGYYNQSEAGSHTLQRMYGCDVGPDGR	P30464	2	29
280	GYYNQSEAGSHTLQR	P30464	0	15
281	GYYNQSEAGSHTLQRMYGCDVGPDGR	P30464	1	26
282	GYYNQSEAGSHTLQRMYGCDVGPDGRLLR	P30464	2	29
283	MYGCDVGPDGR	P30464	0	11
284	MYGCDVGPDGRLLR	P30464	1	14
285	MYGCDVGPDGRLLRGHDQSAYDGK	P30464	2	24
286	LLRGHDQSAYDGK	P30464	1	13
287	LLRGHDQSAYDGKDYIALNEDLSSWTAADTAAQITQR	P30464	2	37
288	GHDQSAYDGK	P30464	0	10
289	GHDQSAYDGKDYIALNEDLSSWTAADTAAQITQR	P30464	1	34
290	GHDQSAYDGKDYIALNEDLSSWTAADTAAQITQRK	P30464	2	35
291	DYIALNEDLSSWTAADTAAQITQR	P30464	0	24
292	DYIALNEDLSSWTAADTAAQITQRK	P30464	1	25
293	DYIALNEDLSSWTAADTAAQITQRKWEAAR	P30464	2	30
294	KWEAAREAEQWR	P30464	2	12
295	WEAAREAEQWR	P30464	1	11
296	WEAAREAEQWRAYLEGLCVEWLR	P30464	2	23
297	EAEQWRAYLEGLCVEWLR	P30464	1	18
298	EAEQWRAYLEGLCVEWLRR	P30464	2	19
299	AYLEGLCVEWLR	P30464	0	12
300	AYLEGLCVEWLRR	P30464	1	13
301	AYLEGLCVEWLRRYLENGK	P30464	2	19
302	RYLENGK	P30464	1	7
303	RYLENGKETLQR	P30464	2	12
304	YLENGKETLQR	P30464	1	11
305	YLENGKETLQRADPPK	P30464	2	16
306	ETLQRADPPK	P30464	1	10
307	ETLQRADPPKTHVTHHPISDHEATLR	P30464	2	26
308	ADPPKTHVTHHPISDHEATLR	P30464	1	21
309	ADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQR	P30464	2	38
310	THVTHHPISDHEATLR	P30464	0	16
311	THVTHHPISDHEATLRCWALGFYPAEITLTWQR	P30464	1	33
312	THVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDR	P30464	2	53
313	CWALGFYPAEITLTWQR	P30464	0	17
314	CWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDR	P30464	1	37
315	CWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQK	P30464	2	41
316	DGEDQTQDTELVETRPAGDR	P30464	0	20
317	DGEDQTQDTELVETRPAGDRTFQK	P30464	1	24
318	DGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQR	P30464	2	37
319	TFQKWAAVVVPSGEEQR	P30464	1	17
320	TFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLR	P30464	2	34
321	WAAVVVPSGEEQR	P30464	0	13
322	WAAVVVPSGEEQRYTCHVQHEGLPKPLTLR	P30464	1	30
323	WAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCR	P30464	2	66
324	YTCHVQHEGLPKPLTLR	P30464	0	17
325	YTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCR	P30464	1	53
326	YTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRR	P30464	2	54
327	WEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCR	P30464	0	36
328	WEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRR	P30464	1	37
438	FDSDAASPREEPR	Q95365	1	13
329	WEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRK	P30464	2	38
330	RKSSGGK	P30464	2	7
331	KSSGGKGGSYSQAASSDSAQGSDVSLTA	P30464	2	28
332	SSGGKGGSYSQAASSDSAQGSDVSLTA	P30464	1	27
333	GGSYSQAASSDSAQGSDVSLTA	P30464	0	22
334	MRVTAPR	P30685	1	7
335	MRVTAPRTVLLLLWGAVALTETWAGSHSMR	P30685	2	30
336	RVTAPRTVLLLLWGAVALTETWAGSHSMR	P30685	2	29
337	VTAPRTVLLLLWGAVALTETWAGSHSMR	P30685	1	28
338	VTAPRTVLLLLWGAVALTETWAGSHSMRYFYTAMSRPGR	P30685	2	39
339	TVLLLLWGAVALTETWAGSHSMR	P30685	0	23
340	TVLLLLWGAVALTETWAGSHSMRYFYTAMSRPGR	P30685	1	34
341	TVLLLLWGAVALTETWAGSHSMRYFYTAMSRPGRGEPR	P30685	2	38
342	YFYTAMSRPGR	P30685	0	11
343	YFYTAMSRPGRGEPR	P30685	1	15
344	YFYTAMSRPGRGEPRFIAVGYVDDTQFVR	P30685	2	29
345	GEPRFIAVGYVDDTQFVR	P30685	1	18
346	GEPRFIAVGYVDDTQFVRFDSDAASPR	P30685	2	27
347	FIAVGYVDDTQFVR	P30685	0	14
348	FIAVGYVDDTQFVRFDSDAASPR	P30685	1	23
349	FIAVGYVDDTQFVRFDSDAASPRTEPR	P30685	2	27
350	FDSDAASPR	P30685	0	9
351	FDSDAASPRTEPR	P30685	1	13
352	FDSDAASPRTEPRAPWIEQEGPEYWDR	P30685	2	27
353	TEPRAPWIEQEGPEYWDR	P30685	1	18
354	TEPRAPWIEQEGPEYWDRNTQIFK	P30685	2	24
355	APWIEQEGPEYWDR	P30685	0	14
356	APWIEQEGPEYWDRNTQIFK	P30685	1	20
357	APWIEQEGPEYWDRNTQIFKTNTQTYR	P30685	2	27
358	NTQIFKTNTQTYR	P30685	1	13
359	NTQIFKTNTQTYRESLR	P30685	2	17
360	TNTQTYR	P30685	0	7
361	TNTQTYRESLR	P30685	1	11
362	TNTQTYRESLRNLR	P30685	2	14
363	ESLRNLR	P30685	1	7
364	ESLRNLRGYYNQSEAGSHIIQR	P30685	2	22
365	NLRGYYNQSEAGSHIIQR	P30685	1	18
366	NLRGYYNQSEAGSHIIQRMYGCDLGPDGR	P30685	2	29
367	GYYNQSEAGSHIIQR	P30685	0	15
368	GYYNQSEAGSHIIQRMYGCDLGPDGR	P30685	1	26
369	GYYNQSEAGSHIIQRMYGCDLGPDGRLLR	P30685	2	29
370	MYGCDLGPDGR	P30685	0	11
371	MYGCDLGPDGRLLR	P30685	1	14
372	MYGCDLGPDGRLLRGHDQSAYDGK	P30685	2	24
373	LLRGHDQSAYDGK	P30685	1	13
374	LLRGHDQSAYDGKDYIALNEDLSSWTAADTAAQITQR	P30685	2	37
375	GHDQSAYDGK	P30685	0	10
376	GHDQSAYDGKDYIALNEDLSSWTAADTAAQITQR	P30685	1	34
377	GHDQSAYDGKDYIALNEDLSSWTAADTAAQITQRK	P30685	2	35
378	DYIALNEDLSSWTAADTAAQITQR	P30685	0	24
379	DYIALNEDLSSWTAADTAAQITQRK	P30685	1	25
380	DYIALNEDLSSWTAADTAAQITQRKWEAAR	P30685	2	30
381	KWEAARVAEQLR	P30685	2	12
382	WEAARVAEQLR	P30685	1	11
383	WEAARVAEQLRAYLEGLCVEWLR	P30685	2	23
384	VAEQLRAYLEGLCVEWLR	P30685	1	18
385	VAEQLRAYLEGLCVEWLRR	P30685	2	19
386	AYLEGLCVEWLR	P30685	0	12
387	AYLEGLCVEWLRR	P30685	1	13
388	AYLEGLCVEWLRRYLENGK	P30685	2	19
389	RYLENGK	P30685	1	7
390	RYLENGKETLQR	P30685	2	12
391	YLENGKETLQR	P30685	1	11
392	YLENGKETLQRADPPK	P30685	2	16
393	ETLQRADPPK	P30685	1	10
394	ETLQRADPPKTHVTHHPVSDHEATLR	P30685	2	26
395	ADPPKTHVTHHPVSDHEATLR	P30685	1	21
396	ADPPKTHVTHHPVSDHEATLRCWALGFYPAEITLTWQR	P30685	2	38
397	THVTHHPVSDHEATLR	P30685	0	16
398	THVTHHPVSDHEATLRCWALGFYPAEITLTWQR	P30685	1	33
399	THVTHHPVSDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDR	P30685	2	53
400	CWALGFYPAEITLTWQR	P30685	0	17
401	CWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDR	P30685	1	37
402	CWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQK	P30685	2	41
403	DGEDQTQDTELVETRPAGDR	P30685	0	20
404	DGEDQTQDTELVETRPAGDRTFQK	P30685	1	24
405	DGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQR	P30685	2	37
406	TFQKWAAVVVPSGEEQR	P30685	1	17
407	TFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLR	P30685	2	34
408	WAAVVVPSGEEQR	P30685	0	13
409	WAAVVVPSGEEQRYTCHVQHEGLPKPLTLR	P30685	1	30
410	WAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCR	P30685	2	66
411	YTCHVQHEGLPKPLTLR	P30685	0	17
412	YTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCR	P30685	1	53
413	YTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRR	P30685	2	54
414	WEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCR	P30685	0	36
415	WEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRR	P30685	1	37
416	WEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRK	P30685	2	38
417	RKSSGGK	P30685	2	7
418	KSSGGKGGSYSQAASSDSAQGSDVSLTA	P30685	2	28
419	SSGGKGGSYSQAASSDSAQGSDVSLTA	P30685	1	27
420	GGSYSQAASSDSAQGSDVSLTA	P30685	0	22
421	MLVMAPR	Q95365	0	7
422	MLVMAPRTVLLLLSAALALTETWAGSHSMR	Q95365	1	30
423	MLVMAPRTVLLLLSAALALTETWAGSHSMRYFYTSVSRPGR	Q95365	2	41
424	LVMAPRTVLLLLSAALALTETWAGSHSMR	Q95365	1	29
425	LVMAPRTVLLLLSAALALTETWAGSHSMRYFYTSVSRPGR	Q95365	2	40
426	TVLLLLSAALALTETWAGSHSMR	Q95365	0	23
427	TVLLLLSAALALTETWAGSHSMRYFYTSVSRPGR	Q95365	1	34
428	TVLLLLSAALALTETWAGSHSMRYFYTSVSRPGRGEPR	Q95365	2	38
429	YFYTSVSRPGR	Q95365	0	11
430	YFYTSVSRPGRGEPR	Q95365	1	15
431	YFYTSVSRPGRGEPRFISVGYVDDTQFVR	Q95365	2	29
432	GEPRFISVGYVDDTQFVR	Q95365	1	18
433	GEPRFISVGYVDDTQFVRFDSDAASPR	Q95365	2	27
434	FISVGYVDDTQFVR	Q95365	0	14
435	FISVGYVDDTQFVRFDSDAASPR	Q95365	1	23
436	FISVGYVDDTQFVRFDSDAASPREEPR	Q95365	2	27
439	FDSDAASPREEPRAPWIEQEGPEYWDR	Q95365	2	27
440	EEPRAPWIEQEGPEYWDR	Q95365	1	18
441	EEPRAPWIEQEGPEYWDRNTQICK	Q95365	2	24
442	APWIEQEGPEYWDR	Q95365	0	14
443	APWIEQEGPEYWDRNTQICK	Q95365	1	20
444	APWIEQEGPEYWDRNTQICKTNTQTYR	Q95365	2	27
445	NTQICKTNTQTYR	Q95365	1	13
446	NTQICKTNTQTYRENLR	Q95365	2	17
447	TNTQTYR	Q95365	0	7
448	TNTQTYRENLR	Q95365	1	11
449	TNTQTYRENLRIALR	Q95365	2	15
450	ENLRIALR	Q95365	1	8
451	ENLRIALRYYNQSEAGSHTLQR	Q95365	2	22
452	IALRYYNQSEAGSHTLQR	Q95365	1	18
453	IALRYYNQSEAGSHTLQRMYGCDVGPDGR	Q95365	2	29
454	YYNQSEAGSHTLQR	Q95365	0	14
455	YYNQSEAGSHTLQRMYGCDVGPDGR	Q95365	1	25
456	YYNQSEAGSHTLQRMYGCDVGPDGRLLR	Q95365	2	28
457	MYGCDVGPDGR	Q95365	0	11
458	MYGCDVGPDGRLLR	Q95365	1	14
459	MYGCDVGPDGRLLRGHNQFAYDGK	Q95365	2	24
460	LLRGHNQFAYDGK	Q95365	1	13
461	LLRGHNQFAYDGKDYIALNEDLSSWTAADTAAQITQR	Q95365	2	37
462	GHNQFAYDGK	Q95365	0	10
463	GHNQFAYDGKDYIALNEDLSSWTAADTAAQITQR	Q95365	1	34
464	GHNQFAYDGKDYIALNEDLSSWTAADTAAQITQRK	Q95365	2	35
465	DYIALNEDLSSWTAADTAAQITQR	Q95365	0	24
466	DYIALNEDLSSWTAADTAAQITQRK	Q95365	1	25
467	DYIALNEDLSSWTAADTAAQITQRKWEAAR	Q95365	2	30
468	KWEAARVAEQLR	Q95365	2	12
469	WEAARVAEQLR	Q95365	1	11
470	WEAARVAEQLRTYLEGTCVEWLR	Q95365	2	23
471	VAEQLRTYLEGTCVEWLR	Q95365	1	18
472	VAEQLRTYLEGTCVEWLRR	Q95365	2	19
473	TYLEGTCVEWLR	Q95365	0	12
474	TYLEGTCVEWLRR	Q95365	1	13
475	TYLEGTCVEWLRRYLENGK	Q95365	2	19
476	RYLENGK	Q95365	1	7
477	RYLENGKETLQR	Q95365	2	12
478	YLENGKETLQR	Q95365	1	11
479	YLENGKETLQRADPPK	Q95365	2	16
480	ETLQRADPPK	Q95365	1	10
481	ETLQRADPPKTHVTHHPISDHEATLR	Q95365	2	26
482	ADPPKTHVTHHPISDHEATLR	Q95365	1	21
483	ADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQR	Q95365	2	38
484	THVTHHPISDHEATLR	Q95365	0	16
485	THVTHHPISDHEATLRCWALGFYPAEITLTWQR	Q95365	1	33
486	THVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDR	Q95365	2	53
487	CWALGFYPAEITLTWQR	Q95365	0	17
488	CWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDR	Q95365	1	37
489	CWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQK	Q95365	2	41
490	DGEDQTQDTELVETRPAGDR	Q95365	0	20
491	DGEDQTQDTELVETRPAGDRTFQK	Q95365	1	24
492	DGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQR	Q95365	2	37
493	TFQKWAAVVVPSGEEQR	Q95365	1	17
494	TFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLR	Q95365	2	34
495	WAAVVVPSGEEQR	Q95365	0	13
496	WAAVVVPSGEEQRYTCHVQHEGLPKPLTLR	Q95365	1	30
497	WAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCR	Q95365	2	66
498	YTCHVQHEGLPKPLTLR	Q95365	0	17
499	YTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCR	Q95365	1	53
500	YTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCRR	Q95365	2	54
\.


--
-- Name: peptides_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dblyon
--

SELECT pg_catalog.setval('peptides_id_seq', 1, false);


--
-- Data for Name: protein_2_function; Type: TABLE DATA; Schema: public; Owner: dblyon
--

COPY protein_2_function (id, an, function) FROM stdin;
1	F0Q046	aaa02020
2	F0Q047	aaa00230
3	F0Q047	aaa00240
4	F0Q047	aaa01100
5	F0Q047	aaa03030
6	F0Q047	aaa03430
7	F0Q047	aaa03440
8	F0Q066	aaa00260
9	F0Q066	aaa00270
10	F0Q066	aaa00300
11	F0Q066	aaa01100
12	F0Q066	aaa01110
13	F0Q066	aaa01120
14	F0Q071	aaa00230
15	F0Q071	aaa00240
16	F0Q071	aaa01100
17	F0Q071	aaa03030
18	F0Q071	aaa03430
19	F0Q071	aaa03440
20	F0Q075	aaa00290
21	F0Q075	aaa00620
22	F0Q075	aaa01100
23	F0Q075	aaa01110
24	F0Q077	aaa00400
25	F0Q077	aaa01100
26	F0Q077	aaa01110
27	F0Q085	aaa00071
28	F0Q085	aaa00072
29	F0Q085	aaa00280
30	F0Q085	aaa00310
31	F0Q085	aaa00362
32	F0Q085	aaa00380
33	F0Q085	aaa00620
34	F0Q085	aaa00630
35	F0Q085	aaa00640
36	F0Q085	aaa00650
37	F0Q085	aaa00900
38	F0Q085	aaa01100
39	F0Q085	aaa01110
40	F0Q085	aaa01120
41	F0Q085	aaa02020
42	F0Q098	aaa00633
43	F0Q098	aaa01120
44	F0Q099	aaa02010
45	F0Q0A0	aaa02010
46	F0Q0A1	aaa02010
47	F0Q0A2	aaa00480
48	F0Q0B4	aaa00281
49	F0Q0B4	aaa01110
50	F0Q0B5	aaa00071
51	F0Q0B5	aaa00280
52	F0Q0B5	aaa00281
53	F0Q0B5	aaa00310
54	F0Q0B5	aaa00362
55	F0Q0B5	aaa00380
56	F0Q0B5	aaa00410
57	F0Q0B5	aaa00627
58	F0Q0B5	aaa00640
59	F0Q0B5	aaa00650
60	F0Q0B5	aaa00903
61	F0Q0B5	aaa00930
62	F0Q0B5	aaa01100
63	F0Q0B5	aaa01110
64	F0Q0B5	aaa01120
65	F0Q0B6	aaa00281
66	F0Q0B6	aaa01110
67	F0Q0B7	aaa00281
68	F0Q0B7	aaa01110
69	F0Q110	aaa00860
70	F0Q110	aaa01100
71	F0Q111	aaa00860
72	F0Q111	aaa01100
73	F0Q112	aaa00860
74	F0Q112	aaa01100
75	F0Q113	aaa00860
76	F0Q113	aaa01100
77	F0Q114	aaa00860
78	F0Q114	aaa01100
79	F0Q115	aaa00860
80	F0Q115	aaa01100
81	F0Q116	aaa00860
82	F0Q116	aaa01100
83	F0Q117	aaa00860
84	F0Q117	aaa01100
85	F0Q119	aaa00860
86	F0Q119	aaa01100
87	F0Q123	aaa00362
88	F0Q123	aaa01100
89	F0Q123	aaa01120
90	F0Q145	aaa00860
91	F0Q145	aaa01100
92	F0Q164	aaa02010
93	F0Q165	aaa02010
94	F0Q169	aaa00930
95	F0Q169	aaa01100
96	F0Q169	aaa01120
97	F0Q173	aaa00650
98	F0Q174	aaa00330
99	F0Q174	aaa01100
100	F0Q174	aaa01110
101	F0Q175	aaa00330
102	F0Q175	aaa01110
103	F0Q177	aaa00260
104	F0Q177	aaa00564
105	F0Q177	aaa01100
106	F0Q1V9	aaa00360
107	F0Q1V9	aaa00910
108	F0Q1W7	aaa00010
109	F0Q1W7	aaa00020
110	F0Q1W7	aaa00620
111	F0Q1W7	aaa01100
112	F0Q1W7	aaa01110
113	F0Q1W7	aaa01120
114	F0Q1X2	aaa00260
115	F0Q1X2	aaa00290
116	F0Q1X2	aaa01100
117	F0Q1X2	aaa01110
118	F0Q1X7	aaa00350
119	F0Q1X7	aaa01100
120	F0Q1X7	aaa01120
121	F0Q1X9	aaa00350
122	F0Q1X9	aaa00643
123	F0Q1X9	aaa01100
124	F0Q1X9	aaa01120
125	F0Q1Y2	aaa00330
126	F0Q1Y2	aaa01110
127	F0Q1Y3	aaa00260
128	F0Q1Y3	aaa00750
129	F0Q1Y3	aaa01100
130	F0Q1Y3	aaa01120
131	F0Q1Z1	aaa00360
132	F0Q1Z1	aaa01120
133	F0Q1Z2	aaa00360
134	F0Q1Z2	aaa01120
135	F0Q1Z3	aaa00624
136	F0Q1Z3	aaa00626
137	F0Q1Z3	aaa00642
138	F0Q1Z3	aaa01100
139	F0Q1Z3	aaa01120
140	F0Q1Z4	aaa02020
141	F0Q1Z4	aaa02030
142	F0Q201	aaa00270
143	F0Q201	aaa00450
144	F0Q201	aaa00670
145	F0Q201	aaa01100
146	F0Q201	aaa01110
147	F0Q208	aaa03018
148	F0Q219	aaa00250
149	F0Q219	aaa00330
150	F0Q219	aaa00471
151	F0Q219	aaa00910
152	F0Q219	aaa01100
153	F0Q2Q2	aaa02010
154	F0Q2Q3	aaa02010
155	F0Q2Q4	aaa02010
156	F0Q2Q5	aaa02010
157	F0Q2Q6	aaa02010
158	F0Q2Q7	aaa00630
159	F0Q2Q7	aaa00910
160	F0Q2S0	aaa02010
161	F0Q2S3	aaa00230
162	F0Q2S3	aaa01100
163	F0Q2S3	aaa01120
164	F0Q2T0	aaa00270
165	F0Q2T0	aaa00450
166	F0Q2T0	aaa00670
167	F0Q2T0	aaa01100
168	F0Q2T0	aaa01110
169	F0Q2T7	aaa00562
170	F0Q2T7	aaa00564
171	F0Q2T7	aaa01100
172	F0Q2U6	aaa02020
173	F0Q2U6	aaa02030
174	F0Q2U8	aaa02020
175	F0Q2U9	aaa02020
176	F0Q2W3	aaa00630
177	F0Q2W3	aaa01100
178	F0Q2W3	aaa01120
179	F0Q2W5	aaa00630
180	F0Q2W5	aaa01100
181	F0Q2W5	aaa01120
182	F0Q2X1	aaa00480
183	F0Q2X1	aaa00590
184	F0Q3J1	aaa00473
185	F0Q3J1	aaa01100
186	F0Q3J3	aaa02010
187	F0Q3J4	aaa00350
188	F0Q3J4	aaa00643
189	F0Q3J4	aaa01100
190	F0Q3J4	aaa01120
191	F0Q3J7	aaa00480
192	F0Q3J8	aaa00770
193	F0Q3J8	aaa01100
194	F0Q3J8	aaa01110
195	F0Q3K2	aaa00280
196	F0Q3K2	aaa00290
197	F0Q3K2	aaa00770
198	F0Q3K2	aaa01100
199	F0Q3K2	aaa01110
200	F0Q3M7	aaa03410
201	F0Q3M8	aaa00240
202	F0Q3M8	aaa01100
203	F0Q3N0	aaa00970
204	F0Q3N0	aaa01100
205	F0Q3N2	aaa03440
206	F0Q3N3	aaa00970
207	F0Q3N3	aaa01100
208	F0Q3N4	aaa00970
209	F0Q3N4	aaa01100
210	F0Q3N8	aaa00550
211	F0Q3P0	aaa02010
212	F0Q3P3	aaa00260
213	F0Q3P3	aaa00270
214	F0Q3P3	aaa01100
215	F0Q3P3	aaa01110
216	F0Q3Q8	aaa03020
217	F0Q3Q9	aaa00920
218	F0Q3Q9	aaa01100
219	F0Q3Q9	aaa01120
220	F0Q4D6	aaa02020
221	F0Q4D7	aaa02020
222	F0Q4E0	aaa00361
223	F0Q4E0	aaa00364
224	F0Q4E0	aaa00623
225	F0Q4E0	aaa01100
226	F0Q4E0	aaa01120
227	F0Q4E5	aaa00230
228	F0Q4E5	aaa01100
229	F0Q4E7	aaa00860
230	F0Q4E7	aaa01100
231	F0Q4E7	aaa01110
232	F0Q4F2	aaa00550
233	F0Q4F2	aaa01100
234	F0Q4F3	aaa03010
235	F0Q4F4	aaa03010
236	F0Q4F7	aaa03010
237	F0Q4F8	aaa03010
238	F0Q4F9	aaa03010
239	F0Q4G0	aaa03010
240	F0Q4G1	aaa03010
241	F0Q4G2	aaa03010
242	F0Q4G3	aaa03010
243	F0Q4G4	aaa03010
244	F0Q4G5	aaa03010
245	F0Q4G6	aaa03010
246	F0Q4G7	aaa03010
247	F0Q4H2	aaa00053
248	F0Q4H2	aaa02060
249	F0Q4H4	aaa02060
250	F0Q4H7	aaa02020
251	F0Q4H8	aaa02020
252	F0Q4H9	aaa02020
253	F0Q4I0	aaa02020
254	F0Q4I1	aaa02020
255	F0Q4I4	aaa00785
256	F0Q4I4	aaa01100
257	F0Q4I5	aaa00785
258	F0Q4I5	aaa01100
259	F0Q4I8	aaa00190
260	F0Q4I8	aaa01100
261	F0Q4I9	aaa00190
262	F0Q4I9	aaa01100
263	F0Q4J0	aaa00190
264	F0Q4J0	aaa01100
265	F0Q4J1	aaa00190
266	F0Q4J1	aaa01100
267	F0Q4J2	aaa00190
268	F0Q4J2	aaa01100
269	F0Q4J3	aaa00190
270	F0Q4J3	aaa01100
271	F0Q4J4	aaa00190
272	F0Q4J4	aaa01100
273	F0Q4J5	aaa00190
274	F0Q4J5	aaa01100
275	F0Q4J7	aaa03410
276	F0Q4J7	aaa03420
277	F0Q4J7	aaa03430
278	F0Q4J7	aaa03450
279	F0Q590	aaa00362
280	F0Q590	aaa01100
281	F0Q590	aaa01120
282	F0Q592	aaa02020
283	F0Q592	aaa02030
284	F0Q593	aaa00620
285	F0Q593	aaa00630
286	F0Q593	aaa01100
287	F0Q593	aaa01120
288	F0Q596	aaa00030
289	F0Q596	aaa01100
290	F0Q596	aaa01110
291	F0Q599	aaa00970
292	F0Q5A3	aaa02010
293	F0Q5A4	aaa02020
294	F0Q5A4	aaa03020
295	F0Q5A7	aaa02020
296	F0Q5A7	aaa02030
297	F0Q5B0	aaa02010
298	F0Q5B4	aaa02020
299	F0Q5B4	aaa02030
300	F0Q5B6	aaa00564
301	F0Q5B6	aaa01100
302	F0Q5B8	aaa00730
303	F0Q5B8	aaa01100
304	F0Q5C2	aaa00620
305	F0Q5C2	aaa01100
306	F0Q5C8	aaa00030
307	F0Q5C8	aaa00040
308	F0Q5C8	aaa01100
309	F0Q5C8	aaa01110
310	F0Q5C8	aaa01120
311	F0Q5D0	aaa00630
312	F0Q5D0	aaa01100
313	F0Q5D2	aaa00400
314	F0Q5D2	aaa01100
315	F0Q5D2	aaa01110
316	F0Q5D3	aaa01110
317	F0Q5D8	aaa03070
318	F0Q5D9	aaa03070
319	F0Q5E0	aaa03070
320	F0Q5E2	aaa03070
321	F0Q5E3	aaa03070
322	F0Q5E5	aaa03070
323	F0Q5F4	aaa03070
324	F0Q5F5	aaa03070
325	F0Q5F7	aaa03070
326	F0Q638	aaa03070
327	F0Q645	aaa00400
328	F0Q645	aaa01100
329	F0Q645	aaa01110
330	F0Q648	aaa00400
331	F0Q648	aaa01100
332	F0Q648	aaa01110
333	F0Q650	aaa00400
334	F0Q650	aaa01100
335	F0Q650	aaa01110
336	F0Q651	aaa03410
337	F0Q653	aaa00430
338	F0Q653	aaa00460
339	F0Q653	aaa00480
340	F0Q653	aaa00590
341	F0Q653	aaa01100
342	F0Q660	aaa03440
343	F0Q663	aaa00130
344	F0Q663	aaa01100
345	F0Q663	aaa01110
346	F0Q667	aaa00330
347	F0Q667	aaa01100
348	F0Q667	aaa01110
349	F0Q668	aaa00561
350	F0Q668	aaa01100
351	F0Q676	aaa00564
352	F0Q677	aaa03010
353	F0Q678	aaa03010
354	F0Q679	aaa03010
355	F0Q680	aaa03010
356	F0Q681	aaa03010
357	F0Q682	aaa03010
358	F0Q683	aaa03010
359	F0Q684	aaa03010
360	F0Q685	aaa03010
361	F0Q686	aaa03010
362	F0Q687	aaa03060
363	F0Q687	aaa03070
364	F0Q688	aaa03010
365	F0Q689	aaa03010
366	F0Q690	aaa03010
367	F0Q691	aaa03010
368	F0Q692	aaa00230
369	F0Q692	aaa00240
370	F0Q692	aaa01100
371	F0Q692	aaa03020
372	F0Q693	aaa03010
373	F0Q697	aaa00540
374	F0Q697	aaa01100
375	F0Q6A4	aaa00260
376	F0Q6A4	aaa01100
377	F0Q6A4	aaa01110
378	F0Q6A4	aaa01120
379	F0Q6Y2	aaa00630
380	F0Q6Y2	aaa00670
381	F0Q6Y8	aaa02020
382	F0Q6Z4	aaa00910
383	F0Q6Z4	aaa01120
384	F0Q6Z4	aaa02020
385	F0Q6Z5	aaa00910
386	F0Q6Z5	aaa01120
387	F0Q6Z5	aaa02020
388	F0Q6Z6	aaa00910
389	F0Q6Z6	aaa01120
390	F0Q6Z6	aaa02020
391	F0Q6Z7	aaa00910
392	F0Q6Z7	aaa01120
393	F0Q6Z7	aaa02020
394	F0Q6Z9	aaa00910
395	F0Q700	aaa00230
396	F0Q700	aaa00240
397	F0Q700	aaa01100
398	F0Q737	aaa00290
399	F0Q737	aaa00770
400	F0Q737	aaa01100
401	F0Q737	aaa01110
402	F0Q749	aaa00330
403	F0Q749	aaa01100
404	F0Q749	aaa01110
405	F0Q750	aaa00360
406	F0Q7T0	aaa03410
407	F0Q7T6	aaa00360
408	F0Q7T7	aaa02010
409	F0Q7T8	aaa02010
410	F0Q7T9	aaa02010
411	F0Q7U0	aaa02010
412	F0Q7U1	aaa02010
413	F0Q7W8	aaa00480
414	F0Q7W9	aaa00300
415	F0Q7W9	aaa01100
416	F0Q7W9	aaa01110
417	F0Q7W9	aaa01120
418	F0Q7X3	aaa02020
419	F0Q7X3	aaa02030
420	F0Q7Y5	aaa00550
421	F0Q7Y6	aaa00300
422	F0Q7Y6	aaa00550
423	F0Q7Y7	aaa00300
424	F0Q7Y7	aaa00550
425	F0Q7Y7	aaa01100
426	F0Q7Y8	aaa00550
427	F0Q7Y8	aaa01100
428	F0Q7Y9	aaa00471
429	F0Q7Y9	aaa00550
430	F0Q7Y9	aaa01100
431	F0Q7Z1	aaa00550
432	F0Q7Z1	aaa01100
433	F0Q7Z2	aaa00471
434	F0Q7Z2	aaa00550
435	F0Q7Z2	aaa01100
436	F0Q7Z3	aaa00473
437	F0Q7Z3	aaa00550
438	F0Q7Z3	aaa01100
439	F0Q7Z7	aaa00540
440	F0Q7Z7	aaa01100
441	F0Q7Z9	aaa00730
442	F0Q7Z9	aaa01100
443	F0Q801	aaa02020
444	F0Q801	aaa02030
445	F0Q803	aaa03440
446	F0Q804	aaa00564
447	F0Q804	aaa01100
448	F0Q8M7	aaa00550
449	F0Q8M8	aaa00400
450	F0Q8M8	aaa01100
451	F0Q8M8	aaa01110
452	F0Q8N4	aaa00970
453	F0Q8N4	aaa01100
454	F0Q8N8	aaa00400
455	F0Q8N8	aaa01100
456	F0Q8N8	aaa01110
457	F0Q8P3	aaa00061
458	F0Q8P3	aaa00620
459	F0Q8P3	aaa00640
460	F0Q8P3	aaa01100
461	F0Q8P3	aaa01110
462	F0Q8P5	aaa00061
463	F0Q8P5	aaa00620
464	F0Q8P5	aaa00640
465	F0Q8P5	aaa01100
466	F0Q8P5	aaa01110
467	F0Q8P5	aaa01120
468	F0Q8P8	aaa00230
469	F0Q8P8	aaa01100
470	F0Q8Q0	aaa00230
471	F0Q8Q0	aaa00240
472	F0Q8Q0	aaa01100
473	F0Q8Q1	aaa00230
474	F0Q8Q1	aaa00240
475	F0Q8Q1	aaa01100
476	F0Q8Q3	aaa02020
477	F0Q8Q4	aaa02020
478	F0Q8Q7	aaa03060
479	F0Q8Q7	aaa03070
480	F0Q8Q9	aaa02020
481	F0Q8R1	aaa02020
482	F0Q8R9	aaa03020
483	F0Q8S6	aaa02010
484	F0Q8S8	aaa02010
485	F0Q8S9	aaa02010
486	F0Q8T0	aaa02010
487	F0Q8T1	aaa02010
488	F0Q8T3	aaa00740
489	F0Q8T3	aaa01100
490	F0Q8T7	aaa00071
491	F0Q8T7	aaa00280
492	F0Q8T7	aaa00281
493	F0Q8T7	aaa00310
494	F0Q8T7	aaa00362
495	F0Q8T7	aaa00380
496	F0Q8T7	aaa00410
497	F0Q8T7	aaa00627
498	F0Q8T7	aaa00640
499	F0Q8T7	aaa00650
500	F0Q8T7	aaa00903
\.


--
-- Name: protein_2_function_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dblyon
--

SELECT pg_catalog.setval('protein_2_function_id_seq', 1, false);


--
-- Data for Name: protein_2_og; Type: TABLE DATA; Schema: public; Owner: dblyon
--

COPY protein_2_og (id, an, og) FROM stdin;
1	EQC87119.1	ENOG410791G
2	EQC87120.1	ENOG4105MA4
3	EQC87121.1	ENOG4105FA2
4	EQC87122.1	ENOG4108ZMD
5	EQC87123.1	ENOG4105CK6
6	EQC87124.1	ENOG4105EB3
7	EQC87124.1	ENOG4108ET4
8	EQC87125.1	ENOG41067TZ
9	EQC87126.1	ENOG4107WDE
10	EQC87128.1	ENOG4105CS2
11	EQC87129.1	ENOG4105CK1
12	EQC87130.1	ENOG4107GUH
13	EQC87131.1	ENOG4105VCP
14	EQC87132.1	ENOG4105VZJ
15	EQC87133.1	ENOG4108FPI
16	EQC87134.1	ENOG4105C1J
17	EQC87135.1	ENOG4105D22
18	EQC87136.1	ENOG4105CK4
19	EQC87137.1	ENOG4106UJV
20	EQC87138.1	ENOG41060Q7
21	EQC87140.1	ENOG4107YCK
22	EQC87141.1	ENOG4105WD6
23	EQC87142.1	ENOG4106E6V
24	EQC87143.1	ENOG4108FKN
25	EQC87144.1	ENOG4105QNR
26	EQC87145.1	ENOG41090C7
27	EQC87146.1	ENOG4108VCV
28	EQC87147.1	ENOG4105C41
29	EQC87149.1	ENOG4105C6H
30	EQC87150.1	ENOG4105C6H
31	EQC87151.1	ENOG4105RCD
32	EQC87152.1	ENOG4105CI3
33	EQC87155.1	ENOG4108ZME
34	EQC87156.1	ENOG41068Z9
35	EQC87157.1	ENOG4105DKQ
36	EQC87158.1	ENOG4105WZW
37	EQC87159.1	ENOG4105HUF
38	EQC87160.1	ENOG4105CQ3
39	EQC87161.1	ENOG4108ZQX
40	EQC87162.1	ENOG4105D5Q
41	EQC87163.1	ENOG4107QXA
42	EQC87164.1	ENOG4105C5B
43	EQC87165.1	ENOG4105C5B
44	EQC87166.1	ENOG4105D5Q
45	EQC87167.1	ENOG4105DBV
46	EQC87168.1	ENOG4105CEU
47	EQC87169.1	ENOG4107SYD
48	EQC87170.1	ENOG4105XBY
49	EQC87171.1	ENOG4105DFU
50	EQC87173.1	ENOG4105C0D
51	EQC87174.1	ENOG4107XTZ
52	EQC87175.1	ENOG41074EB
53	EQC87176.1	ENOG4108IW0
54	EQC87177.1	ENOG4105D8C
55	EQC87178.1	ENOG4105GYP
56	EQC87179.1	ENOG4108Z86
57	EQC87180.1	ENOG4108KUQ
58	EQC87181.1	ENOG4107QQC
59	EQC87182.1	ENOG4105C20
60	EQC87183.1	ENOG4108W2Y
61	EQC87184.1	ENOG4105KX1
62	EQC87185.1	ENOG4108ICC
63	EQC87186.1	ENOG41064PW
64	EQC87187.1	ENOG4105MQI
65	EQC87188.1	ENOG41080U4
66	EQC87189.1	ENOG4106XRI
67	EQC87190.1	ENOG4105CTP
68	EQC87191.1	ENOG4105F9F
69	EQC87193.1	ENOG4106TAE
70	EQC87195.1	ENOG41080NU
71	EQC87197.1	ENOG4108PM6
72	EQC87198.1	ENOG4107TEC
73	EQC87200.1	ENOG4105D95
74	EQC87201.1	ENOG4108IJ9
75	EQC87202.1	ENOG4105CBD
76	EQC87218.1	ENOG4105CKN
77	EQC87219.1	ENOG4105CRD
78	EQC87220.1	ENOG4105ENN
79	EQC87221.1	ENOG4108TCI
80	EQC87222.1	ENOG4107VZS
81	EQC87223.1	ENOG4108RMZ
82	EQC87224.1	ENOG4105CFP
83	EQC87225.1	ENOG4105XYU
84	EQC87227.1	ENOG4105DHI
85	EQC87228.1	ENOG4106N3A
86	EQC87229.1	ENOG4105E5I
87	EQC87230.1	ENOG4105YNR
88	EQC87231.1	ENOG4105K59
89	EQC87232.1	ENOG4106GBV
90	EQC87233.1	ENOG4105C64
91	EQC87234.1	ENOG4108UIK
92	EQC87235.1	ENOG4105C59
93	EQC87236.1	ENOG4107YMD
94	EQC87237.1	ENOG4105CMR
95	EQC87238.1	ENOG4107QW6
96	EQC87239.1	ENOG4107RBJ
97	EQC87242.1	ENOG4105C8D
98	EQC87243.1	ENOG4105DI7
99	EQC87244.1	ENOG4108KGH
100	EQC87245.1	ENOG4108B6G
101	EQC87246.1	ENOG4105K8N
102	EQC87247.1	ENOG4107BU2
103	EQC87248.1	ENOG4107URF
104	EQC87249.1	ENOG4105C5Y
105	EQC87250.1	ENOG4107ZU8
106	EQC87251.1	ENOG4107414
107	EQC87252.1	ENOG4107QJF
108	EQC87253.1	ENOG4105C8B
109	EQC87254.1	ENOG4105WHI
110	EQC87255.1	ENOG410743R
111	EQC87256.1	ENOG4106BD9
112	EQC87257.1	ENOG41073JJ
113	EQC87258.1	ENOG4107K2V
114	EQC87259.1	ENOG4107U5W
115	EQC87290.1	ENOG4105VTR
116	EQC87291.1	ENOG4105VJG
117	EQC87292.1	ENOG4105E03
118	EQC87293.1	ENOG4108M1A
119	EQC87294.1	ENOG4105C91
120	EQC87295.1	ENOG4105G1S
121	EQC87297.1	ENOG4105M0U
122	EQC87299.1	ENOG4108D5F
123	EQC87300.1	ENOG4105F4C
124	EQC87301.1	ENOG4105NAE
125	EQC87302.1	ENOG4105CEH
126	EQC87304.1	ENOG4108JYZ
127	EQC87305.1	ENOG4108JYZ
128	EQC87306.1	ENOG4107AYK
129	EQC87307.1	ENOG4105C9M
130	EQC87308.1	ENOG4107R36
131	EQC87309.1	ENOG4105WT3
132	EQC87310.1	ENOG4105BZQ
133	EQC87311.1	ENOG4105MY8
134	EQC87312.1	ENOG4107RR8
135	EQC87313.1	ENOG4107S19
136	EQC87314.1	ENOG410848D
137	EQC87315.1	ENOG4105C3X
138	EQC87316.1	ENOG4108Z8I
139	EQC87317.1	ENOG4105VUF
140	EQC87318.1	ENOG4105F9F
141	EQC87328.1	ENOG4105KXT
142	EQC87329.1	ENOG41073T5
143	EQC87330.1	ENOG41067YF
144	EQC87331.1	ENOG41075Y2
145	EQC87333.1	ENOG4107XC6
146	EQC87334.1	ENOG4108R7S
147	EQC87335.1	ENOG41079PF
148	EQC87336.1	ENOG4105ZMH
149	EQC87337.1	ENOG4108URH
150	EQC87338.1	ENOG4105YY7
151	EQC87339.1	ENOG4107CE6
152	EQC87340.1	ENOG4108I7W
153	EQC87341.1	ENOG4105D5G
154	EQC87342.1	ENOG4105C80
155	EQC87344.1	ENOG41074QN
156	EQC87345.1	ENOG41074QN
157	EQC87346.1	ENOG4106N1J
158	EQC87349.1	ENOG4106FJ5
159	EQC87351.1	ENOG4105T6C
160	EQC87352.1	ENOG4106ERX
161	EQC87364.1	ENOG4105F9F
162	EQC87365.1	ENOG4105W0R
163	EQC87366.1	ENOG41067KN
164	EQC87369.1	ENOG4105VW6
165	EQC87371.1	ENOG4105F9F
166	EQC87372.1	ENOG4105C0B
167	EQC87373.1	ENOG4105MHI
168	EQC87374.1	ENOG4106EQ3
169	EQC87375.1	ENOG4105WD6
170	EQC87376.1	ENOG41084VM
171	EQC87377.1	ENOG4107YT9
172	EQC87378.1	ENOG4108IGA
173	EQC87379.1	ENOG4105K70
174	EQC87380.1	ENOG4105QZP
175	EQC87381.1	ENOG4108RCR
176	EQC87382.1	ENOG4108UT2
177	EQC87383.1	ENOG4105TWF
178	EQC87384.1	ENOG4106JDM
179	EQC87385.1	ENOG4108M15
180	EQC87386.1	ENOG4108MUX
181	EQC87387.1	ENOG4107Z8C
182	EQC87388.1	ENOG4108SMS
183	EQC87389.1	ENOG4105TWF
184	EQC87390.1	ENOG4105Z8B
185	EQC87392.1	ENOG4105CJ2
186	EQC87393.1	ENOG4107U8T
187	EQC87394.1	ENOG4108IQI
188	EQC87395.1	ENOG4108R5K
189	EQC87396.1	ENOG4105EMS
190	EQC87397.1	ENOG4107YMH
191	EQC87398.1	ENOG4107XUU
192	EQC87399.1	ENOG4105NX3
193	EQC87400.1	ENOG4105MIX
194	EQC87401.1	ENOG4105T58
195	EQC87402.1	ENOG4105WUC
196	EQC87403.1	ENOG4105WUC
197	EQC87404.1	ENOG4105C85
198	EQC87405.1	ENOG4105C85
199	EQC87406.1	ENOG4105C68
200	EQC87407.1	ENOG4105CAQ
201	EQC87408.1	ENOG4105CWT
202	EQC87409.1	ENOG4105C1J
203	EQC87410.1	ENOG4105C8A
204	EQC87411.1	ENOG4108JQ7
205	EQC87412.1	ENOG4105C3U
206	EQC87413.1	ENOG4105C2T
207	EQC87414.1	ENOG4105CJM
208	EQC87415.1	ENOG4108HE0
209	EQC87416.1	ENOG4107EES
210	EQC87417.1	ENOG4105CPF
211	EQC87418.1	ENOG4105F3K
212	EQC87419.1	ENOG4107RF6
213	EQC87420.1	ENOG4108JU3
214	EQC87421.1	ENOG4107ZCT
215	EQC87422.1	ENOG4105DKJ
216	EQC87423.1	ENOG4108YZK
217	EQC87424.1	ENOG4105KVH
218	EQC87425.1	ENOG4105CV8
219	EQC87426.1	ENOG4105F27
220	EQC87427.1	ENOG4108S6S
221	EQC87428.1	ENOG4105S6R
222	EQC87429.1	ENOG4105S6R
223	EQC87430.1	ENOG4105VZ8
224	EQC87431.1	ENOG4108UMI
225	EQC87432.1	ENOG4108JEI
226	EQC87433.1	ENOG4105D01
227	EQC87434.1	ENOG4105D01
228	EQC87435.1	ENOG41084PM
229	EQC87436.1	ENOG4108Z66
230	EQC87437.1	ENOG4105VKD
231	EQC87438.1	ENOG4108SMS
232	EQC87439.1	ENOG4105E0A
233	EQC87440.1	ENOG4106CGA
234	EQC87441.1	ENOG4105WD6
235	EQC87442.1	ENOG4108JQ6
236	EQC87444.1	ENOG4108TQA
237	EQC87458.1	ENOG4105C80
238	EQC87459.1	ENOG4107RBV
239	EQC87460.1	ENOG4105CRK
240	EQC87461.1	ENOG4105TWF
241	EQC87462.1	ENOG4108TQA
242	EQC87468.1	ENOG41081BS
243	EQC87469.1	ENOG4108TQA
244	EQC87482.1	ENOG4107DVX
245	EQC87483.1	ENOG4105DA0
246	EQC87485.1	ENOG4105YEN
247	EQC87497.1	ENOG4107BHU
248	EQC87498.1	ENOG4107B07
249	EQC87499.1	ENOG4108XXH
250	EQC87500.1	ENOG4105K5Y
251	EQC87501.1	ENOG4108UUM
252	EQC87502.1	ENOG4107QMW
253	EQC87503.1	ENOG4108VDD
254	EQC87504.1	ENOG4105N2R
255	EQC87505.1	ENOG4105CJ9
256	EQC87506.1	ENOG4108UI2
257	EQC87507.1	ENOG4105BZ4
258	EQC87508.1	ENOG4107X35
259	EQC87509.1	ENOG4107B07
260	EQC87510.1	ENOG4105DEA
261	EQC87511.1	ENOG4105YV2
262	EQC87512.1	ENOG4105CDF
263	EQC87513.1	ENOG4108TDN
264	EQC87514.1	ENOG4105WBI
265	EQC87515.1	ENOG41090SU
266	EQC87516.1	ENOG4108UKS
267	EQC87517.1	ENOG4108TQA
268	EQC87524.1	ENOG4108TQA
269	EQC87525.1	ENOG4107QWA
270	EQC87526.1	ENOG4105H1H
271	EQC87527.1	ENOG4106IB6
272	EQC87529.1	ENOG4105C50
273	EQC87530.1	ENOG4105EEA
274	EQC87531.1	ENOG4105EEA
275	EQC87532.1	ENOG4107C9C
276	EQC87533.1	ENOG4107UYD
277	EQC87534.1	ENOG4105C2V
278	EQC87535.1	ENOG4106JDM
279	EQC87536.1	ENOG4105D5G
280	EQC87542.1	ENOG4105EN2
281	EQC87543.1	ENOG4106HXZ
282	EQC87544.1	ENOG4108TQA
283	EQC87545.1	ENOG4106T9N
284	EQC87991.1	ENOG4105CIH
285	EQC87992.1	ENOG4105ECC
286	EQC87993.1	ENOG4105E21
287	EQC87997.1	ENOG4108TQA
288	EQC87998.1	ENOG4108STG
289	EQC87999.1	ENOG4108SMS
290	EQC88002.1	ENOG4106I62
291	EQC88003.1	ENOG410694Q
292	EQC88004.1	ENOG4107NTS
293	EQC88005.1	ENOG4105K8F
294	EQC88006.1	ENOG4105C0S
295	EQC88007.1	ENOG4105CJV
296	EQC88008.1	ENOG4108UJE
297	EQC88009.1	ENOG4105ECC
298	EQC88012.1	ENOG4105TWF
299	EQC88013.1	ENOG4105CRK
300	EQC88014.1	ENOG41081BS
301	EQC88015.1	ENOG4107RBV
302	EQC88016.1	ENOG41081BS
303	EQC88017.1	ENOG4107V8S
304	EQC88018.1	ENOG4105D8I
305	EQC88019.1	ENOG4108V3G
306	EQC88020.1	ENOG4108X3M
307	EQC88021.1	ENOG4105EEQ
308	EQC88023.1	ENOG4105DA0
309	EQC88024.1	ENOG4105BZ4
310	EQC88025.1	ENOG4105CN9
311	EQC88027.1	ENOG4105N2R
312	EQC88028.1	ENOG4108VDD
313	EQC88029.1	ENOG4107QMW
314	EQC88030.1	ENOG4108UUM
315	EQC88031.1	ENOG4105K5Y
316	EQC88032.1	ENOG4105CJ9
317	EQC88033.1	ENOG4105Q2H
318	EQC88034.1	ENOG4105EB3
319	EQC88035.1	ENOG4105CK6
320	EQC88036.1	ENOG4108ZMD
321	EQC88037.1	ENOG4105FA2
322	EQC88038.1	ENOG4105MA4
323	EQC88039.1	ENOG410791G
324	EQC88040.1	ENOG4105CU0
325	EQC88042.1	ENOG4108UJR
326	EQC88043.1	ENOG41060Q7
327	EQC88044.1	ENOG4105DU8
328	EQC88045.1	ENOG4106UJV
329	EQC88046.1	ENOG4105CK4
330	EQC88047.1	ENOG4105D22
331	EQC88048.1	ENOG4108FPI
332	EQC88049.1	ENOG4107RBP
333	EQC88050.1	ENOG4105VZJ
334	EQC88051.1	ENOG4105VCP
335	EQC88052.1	ENOG4107GUH
336	EQC88053.1	ENOG4105CS2
337	EQC88054.1	ENOG4105C77
338	EQC88055.1	ENOG4105CBD
339	EQC88056.1	ENOG4108IJ9
340	EQC88057.1	ENOG4105D95
341	EQC88058.1	ENOG4105C8B
342	EQC88059.1	ENOG4107QJF
343	EQC88060.1	ENOG4107414
344	EQC88061.1	ENOG4107ZU8
345	EQC88062.1	ENOG4105C5Y
346	EQC88063.1	ENOG4105C71
347	EQC88064.1	ENOG4107URF
348	EQC88065.1	ENOG4107BU2
349	EQC88067.1	ENOG4105K8N
350	EQC88068.1	ENOG4108B6G
351	EQC88069.1	ENOG4108KGH
352	EQC88071.1	ENOG41066S5
353	EQC88072.1	ENOG4105QJV
354	EQC88073.1	ENOG4107ZTK
355	EQC88074.1	ENOG4106SUW
356	EQC88075.1	ENOG4107ZK2
357	EQC88080.1	ENOG4105C0R
358	EQC88082.1	ENOG4106XGA
359	EQC88083.1	ENOG4107U5W
360	EQC88085.1	ENOG4107RE8
361	EQC88086.1	ENOG4106959
362	EQC88087.1	ENOG4105HBC
363	EQC88091.1	ENOG4107ACT
364	EQC88093.1	ENOG4108YDK
365	EQC88094.1	ENOG4106AUN
366	EQC88097.1	ENOG4106H1X
367	EQC88098.1	ENOG4108Z1K
368	EQC88100.1	ENOG4105C72
369	EQC88101.1	ENOG4105D5G
370	EQC88104.1	ENOG4105S6R
371	EQC88105.1	ENOG4105S6R
372	EQC88106.1	ENOG4108V5C
373	EQC88107.1	ENOG4108S6S
374	EQC88108.1	ENOG4105F27
375	EQC88109.1	ENOG4105CV8
376	EQC88110.1	ENOG4105KVH
377	EQC88111.1	ENOG4108YZK
378	EQC88112.1	ENOG4105DKJ
379	EQC88113.1	ENOG4107ZCT
380	EQC88114.1	ENOG4108JU3
381	EQC88115.1	ENOG4107RF6
382	EQC88116.1	ENOG4105F3K
383	EQC88117.1	ENOG4105CPF
384	EQC88118.1	ENOG4107EES
385	EQC88119.1	ENOG4108HE0
386	EQC88120.1	ENOG4108HE0
387	EQC88121.1	ENOG4105CJM
388	EQC88122.1	ENOG4105C2T
389	EQC88123.1	ENOG4105C3U
390	EQC88124.1	ENOG4108JQ7
391	EQC88125.1	ENOG4105C8A
392	EQC88126.1	ENOG4105C1J
393	EQC88127.1	ENOG4105CWT
394	EQC88128.1	ENOG4105CAQ
395	EQC88129.1	ENOG4105ERD
396	EQC88130.1	ENOG4105C68
397	EQC88131.1	ENOG4105C85
398	EQC88132.1	ENOG4105C85
399	EQC88133.1	ENOG4105WUC
400	EQC88134.1	ENOG4105WUC
401	EQC88135.1	ENOG4105T58
402	EQC88136.1	ENOG4105MIX
403	EQC88137.1	ENOG4105NX3
404	EQC88138.1	ENOG4107XUU
405	EQC88139.1	ENOG4107YMH
406	EQC88140.1	ENOG4105EMS
407	EQC88141.1	ENOG4108R5K
408	EQC88142.1	ENOG4108IQI
409	EQC88143.1	ENOG4107U8T
410	EQC88144.1	ENOG4105CJ2
411	EQC88145.1	ENOG4108I7W
412	EQC88147.1	ENOG4105DKW
413	EQC88148.1	ENOG4105MQS
414	EQC88149.1	ENOG4105C0C
415	EQC88150.1	ENOG4105C01
416	EQC88151.1	ENOG4107KY0
417	EQC88152.1	ENOG4107KY0
418	EQC88154.1	ENOG4105KZ5
419	EQC88155.1	ENOG41085NV
420	EQC88155.1	ENOG41074UD
421	EQC88157.1	ENOG4105CYQ
422	EQC88158.1	ENOG4105WD6
423	EQC88159.1	ENOG4105C7B
424	EQC88160.1	ENOG4105C6M
425	EQC88161.1	ENOG4108ZP8
426	EQC88162.1	ENOG4105WD6
427	EQC88163.1	ENOG4105C01
428	EQC88164.1	ENOG4105CH2
429	EQC88165.1	ENOG4108ZJ4
430	EQC88167.1	ENOG4105G6W
431	EQC88168.1	ENOG4105BZM
432	EQC88169.1	ENOG4105EKD
433	EQC88170.1	ENOG4105CN5
434	EQC88171.1	ENOG4106EHS
435	EQC88172.1	ENOG41072GX
436	EQC88173.1	ENOG4105KEG
437	EQC88174.1	ENOG4105CPM
438	EQC88176.1	ENOG4105FWV
439	EQC88177.1	ENOG4107T3K
440	EQC88178.1	ENOG4105D5T
441	EQC88179.1	ENOG4105S7S
442	EQC88180.1	ENOG4105S7S
443	EQC88181.1	ENOG4107REI
444	EQC88182.1	ENOG4108V1J
445	EQC88183.1	ENOG4105CD8
446	EQC88184.1	ENOG4107VF0
447	EQC88185.1	ENOG4108W5J
448	EQC88186.1	ENOG41076HS
449	EQC88187.1	ENOG4105PHB
450	EQC88188.1	ENOG4105BZ1
451	EQC88189.1	ENOG4105BZ1
452	EQC88190.1	ENOG4105CDF
453	EQC88191.1	ENOG4105VEM
454	EQC88192.1	ENOG4105VKD
455	EQC88193.1	ENOG4108Z66
456	EQC88194.1	ENOG41084PM
457	EQC88195.1	ENOG4105D01
458	EQC88196.1	ENOG4105D01
459	EQC88197.1	ENOG4105D01
460	EQC88198.1	ENOG4105D01
461	EQC88199.1	ENOG4108JEI
462	EQC88200.1	ENOG4108UMI
463	EQC88201.1	ENOG4108V7D
464	EQC88202.1	ENOG4108JJB
465	EQC88203.1	ENOG4106GWW
466	EQC88204.1	ENOG4105VZ8
467	EQC88205.1	ENOG4105GIG
468	EQC88206.1	ENOG4105GIG
469	EQC88207.1	ENOG41082W5
470	EQC88210.1	ENOG4106CGA
471	EQC88211.1	ENOG4105E0A
472	EQC88212.1	ENOG4105S6R
473	EQC88213.1	ENOG4107FQX
474	EQC88214.1	ENOG4105C79
475	EQC88216.1	ENOG4105D5G
476	EQC88217.1	ENOG4108XZ3
477	EQC88218.1	ENOG4108FW6
478	EQC88219.1	ENOG4105C73
479	EQC88220.1	ENOG4105D5G
480	EQC88221.1	ENOG4105D5G
481	EQC88222.1	ENOG4105VE8
482	EQC88223.1	ENOG4105DMF
483	EQC88224.1	ENOG4105EEQ
484	EQC88227.1	ENOG4108I3C
485	EQC88228.1	ENOG4105CH2
486	EQC88229.1	ENOG4108JJB
487	EQC88230.1	ENOG4105EK6
488	EQC88231.1	ENOG41061R1
489	EQC88232.1	ENOG4108JJB
490	EQC88233.1	ENOG4108I3C
491	EQC88234.1	ENOG4105CWF
492	EQC88235.1	ENOG4108I7W
493	EQC88237.1	ENOG4107BHU
494	EQC88238.1	ENOG4106TB0
495	EQC88239.1	ENOG4108ZUI
496	EQC88240.1	ENOG4106HXZ
497	EQC88245.1	ENOG4106128
498	EQC88246.1	ENOG4106BHR
499	EQC88248.1	ENOG4108436
500	EQC88250.1	ENOG4106372
\.


--
-- Name: protein_2_og_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dblyon
--

SELECT pg_catalog.setval('protein_2_og_id_seq', 1, false);


--
-- Data for Name: protein_2_taxid; Type: TABLE DATA; Schema: public; Owner: dblyon
--

COPY protein_2_taxid (id, an, taxid) FROM stdin;
1	P31946	9606
2	P04439	9606
3	P01889	9606
4	P30464	9606
5	P30685	9606
6	Q95365	9606
7	Q04826	9606
8	P30484	9606
9	P30492	9606
10	P30493	9606
11	P18465	9606
12	Q29836	9606
13	Q31610	9606
14	P30499	9606
15	Q29865	9606
16	P14060	9606
17	P26439	9606
18	Q9Y3L3	9606
19	P78314	9606
20	P29372	9606
21	P28566	9606
22	Q8NAA4	9606
23	P01009	9606
24	P29274	9606
25	P29275	9606
26	Q9NRG9	9606
27	P31941	9606
28	O94911	9606
29	Q9NUT2	9606
30	Q9NRK6	9606
31	Q9H221	9606
32	Q8TB40	9606
33	O94929	9606
34	Q8N961	9606
35	O00763	9606
36	Q9H845	9606
37	P11310	9606
38	Q96P50	9606
39	O00400	9606
40	Q5T8D3	9606
41	Q9BR61	9606
42	Q5FVE4	9606
43	P30443	9606
44	P01892	9606
45	P13746	9606
46	Q96QU6	9606
47	P30447	9606
48	P18462	9606
49	P16190	9606
50	P30455	9606
51	P30457	9606
52	P01891	9606
53	P30460	9606
54	P30480	9606
55	P30483	9606
56	Q29940	9606
57	P30498	9606
58	Q9TNN7	9606
59	Q29963	9606
60	P30505	9606
61	P30510	9606
62	Q95604	9606
63	Q16537	9606
64	Q66LE6	9606
65	Q9Y2T4	9606
66	P13760	9606
67	P20039	9606
68	P01911	9606
69	Q7L8J4	9606
70	O60239	9606
71	Q13541	9606
72	O60516	9606
73	P28222	9606
74	P28221	9606
75	O95264	9606
76	P34969	9606
77	Q969T7	9606
78	P52209	9606
79	P36639	9606
80	Q676U5	9606
81	P02763	9606
82	P20848	9606
83	Q96IX9	9606
84	Q9NPC4	9606
85	P05067	9606
86	Q96GX2	9606
87	Q9H7C9	9606
88	Q13685	9606
89	Q9Y312	9606
90	Q8NHS2	9606
91	P00505	9606
92	Q9NUQ8	9606
93	Q9H222	9606
94	P16219	9606
95	Q8NC06	9606
96	Q709F0	9606
97	Q4AC99	9606
98	P30450	9606
99	P16188	9606
100	P10314	9606
101	P30456	9606
102	P10316	9606
103	P30461	9606
104	P30485	9606
105	P30487	9606
106	P18464	9606
107	P30490	9606
108	P10319	9606
109	Q31612	9606
110	Q29718	9606
111	P30504	9606
112	P10321	9606
113	P30508	9606
114	Q29960	9606
115	Q29974	9606
116	Q13542	9606
117	P41595	9606
118	P28335	9606
119	Q13639	9606
120	P50406	9606
121	Q9H0P0	9606
122	P49902	9606
123	Q5TYW2	9606
124	Q5VUR7	9606
125	P0DMS8	9606
126	Q9NS82	9606
127	Q8N5Z0	9606
128	O43741	9606
129	Q9UGJ0	9606
130	Q9BTE6	9606
131	Q9UDR5	9606
132	Q9NY61	9606
133	Q9NRW3	9606
134	Q6NTF7	9606
135	Q9BZC7	9606
136	P78363	9606
137	Q4W5N1	9606
138	Q86UK0	9606
139	Q9NSE7	9606
140	P45844	9606
141	Q0P651	9606
142	Q9Y235	9606
143	Q8WW27	9606
144	Q96I13	9606
145	Q8NFV4	9606
146	Q9P2A4	9606
147	Q969K4	9606
148	Q15027	9606
149	Q15057	9606
150	Q8N6N7	9606
151	P45954	9606
152	Q5QJU3	9606
153	P12821	9606
154	Q9NPB9	9606
155	Q9Y614	9606
156	P62258	9606
157	Q04917	9606
158	P61981	9606
159	Q9TQE0	9606
160	P31937	9606
161	P30939	9606
162	P28223	9606
163	Q9BXI3	9606
164	P05408	9606
165	Q6PD74	9606
166	Q2M2I8	9606
167	Q9Y478	9606
168	P54619	9606
169	Q9UGI9	9606
170	Q96AK3	9606
171	Q99758	9606
172	O75027	9606
173	Q09428	9606
174	P08910	9606
175	Q8WTS1	9606
176	Q9BUJ0	9606
177	Q96IU4	9606
178	P42684	9606
179	Q9ULW3	9606
180	Q9BYF1	9606
181	P32297	9606
182	Q05901	9606
183	P30926	9606
184	Q9UKV3	9606
185	Q07912	9606
186	Q16570	9606
187	P20309	9606
188	Q8WXI4	9606
189	Q8N1Q8	9606
190	Q99798	9606
191	Q3I5F7	9606
192	P63104	9606
193	P05534	9606
194	P30512	9606
195	P16189	9606
196	P30453	9606
197	P30459	9606
198	P30462	9606
199	P30466	9606
200	P03989	9606
201	P18463	9606
202	P30475	9606
203	P30479	9606
204	P30481	9606
205	P30486	9606
206	P30488	9606
207	P30491	9606
208	P30495	9606
209	P30501	9606
210	P04222	9606
211	Q07000	9606
212	Q15172	9606
213	Q13362	9606
214	Q30134	9606
215	P46952	9606
216	Q8WXA8	9606
217	A5X5Y0	9606
218	P04217	9606
219	Q9NQ94	9606
220	Q5SQ80	9606
221	Q4UJ75	9606
222	Q5T5F5	9606
223	P22760	9606
224	Q15758	9606
225	Q86V21	9606
226	P54646	9606
227	Q5VST6	9606
228	Q7Z5R6	9606
229	Q9UH17	9606
230	Q8IUX4	9606
231	Q9HC16	9606
232	O95477	9606
233	Q8WWZ7	9606
234	Q8IZY2	9606
235	Q2M3G0	9606
236	Q9NP58	9606
237	O60706	9606
238	O14678	9606
239	Q8NE71	9606
240	Q8N2K0	9606
241	Q96SE0	9606
242	Q8WU67	9606
243	Q9BV23	9606
244	Q8IZP0	9606
245	O14639	9606
246	Q6H8Q1	9606
247	Q9P1F3	9606
248	Q8N0Z2	9606
249	P07108	9606
250	Q8TDN7	9606
251	Q9NUN7	9606
252	P43681	9606
253	Q07001	9606
254	Q9Y615	9606
255	Q8WYK0	9606
256	Q9NUB1	9606
257	Q4L235	9606
258	Q8TC94	9606
259	Q03154	9606
260	P11171	9606
261	Q9NRA8	9606
262	P08195	9606
263	P08908	9606
264	P46098	9606
265	Q70Z44	9606
266	P47898	9606
267	Q96P26	9606
268	P21589	9606
269	P56378	9606
270	P19652	9606
271	U3KPV4	9606
272	Q7RTV5	9606
273	Q8N139	9606
274	Q8IUA7	9606
275	Q8WWZ4	9606
276	Q86UQ4	9606
277	Q96J66	9606
278	P33897	9606
279	Q9UNQ0	9606
280	P41238	9606
281	Q9H3Z7	9606
282	P00519	9606
283	Q12979	9606
284	Q96AP0	9606
285	P25106	9606
286	Q86TX2	9606
287	Q8N9L9	9606
288	Q15067	9606
289	Q99424	9606
290	P13798	9606
291	P12814	9606
292	O75078	9606
293	Q9Y3Q7	9606
294	Q6NVV9	9606
295	Q9H2U9	9606
296	P78325	9606
297	Q9NPF8	9606
298	Q08462	9606
299	O95622	9606
300	P35612	9606
301	P30153	9606
302	Q00005	9606
303	P04229	9606
304	Q30167	9606
305	Q5Y7A7	9606
306	Q9H2F3	9606
307	O95336	9606
308	P0DKL9	9606
309	Q8NF67	9606
310	A0PJZ0	9606
311	P08697	9606
312	P01023	9606
313	A7E2S9	9606
314	Q9UNA3	9606
315	P30542	9606
316	Q7Z5M8	9606
317	Q96GS6	9606
318	Q6PCB6	9606
319	O95870	9606
320	Q13085	9606
321	Q9UKU7	9606
322	P28330	9606
323	P49748	9606
324	Q96GR2	9606
325	P30532	9606
326	Q15825	9606
327	Q9UGM1	9606
328	P08172	9606
329	P21399	9606
330	O00767	9606
331	Q96QF7	9606
332	P33121	9606
333	P63267	9606
334	Q8TDG2	9606
335	O43506	9606
336	O75077	9606
337	P08913	9606
338	Q9BZ11	9606
339	Q96M93	9606
340	Q6DHV7	9606
341	Q99965	9606
342	O00116	9606
343	Q5VUY0	9606
344	Q08828	9606
345	P35611	9606
346	Q8N7X0	9606
347	Q6IQ32	9606
348	Q9BRR6	9606
349	Q96A54	9606
350	Q6UXC1	9606
351	Q8N556	9606
352	Q6ULP2	9606
353	Q5I7T1	9606
354	P31947	9606
355	P27348	9606
356	Q09160	9606
357	Q15173	9606
358	Q14738	9606
359	P30154	9606
360	P63151	9606
361	P01912	9606
362	P13761	9606
363	Q95IE3	9606
364	Q9GIY3	9606
365	Q8IZ83	9606
366	P02750	9606
367	A8K2U0	9606
368	P01011	9606
369	Q13131	9606
370	Q4LEZ3	9606
371	P86434	9606
372	P17174	9606
373	Q9NP78	9606
374	O95342	9606
375	Q9UBJ2	9606
376	P28288	9606
377	P61221	9606
378	Q9UG63	9606
379	Q9H172	9606
380	Q6UXT9	9606
381	Q9NUJ1	9606
382	Q7L211	9606
383	Q9NYB9	9606
384	Q15822	9606
385	O96019	9606
386	Q9Y305	9606
387	P10323	9606
388	Q68CK6	9606
389	Q53FZ2	9606
390	Q6NUN0	9606
391	P62736	9606
392	Q9BYX7	9606
393	P68032	9606
394	Q8TDY3	9606
395	Q04771	9606
396	Q7Z695	9606
397	Q3MIX3	9606
398	O60266	9606
399	P51828	9606
400	P07327	9606
401	P00325	9606
402	P00326	9606
403	Q8WTP8	9606
404	A6NIR3	9606
405	Q9H0P7	9606
406	Q53H12	9606
407	Q14246	9606
408	Q9BY15	9606
409	Q5T601	9606
410	Q86Y34	9606
411	O00253	9606
412	Q9BRQ8	9606
413	Q8N1P7	9606
414	Q9Y4K1	9606
415	Q6JQN1	9606
416	P22303	9606
417	Q9GZZ6	9606
418	P02708	9606
419	P11230	9606
420	P07510	9606
421	O00590	9606
422	O94805	9606
423	P53396	9606
424	P11229	9606
425	P08173	9606
426	Q8TDX5	9606
427	Q9NPJ3	9606
428	O14561	9606
429	Q8NEB7	9606
430	Q9NR19	9606
431	Q96CM8	9606
432	Q9UKU0	9606
433	Q08AH1	9606
434	P0C7M7	9606
435	Q9H6R3	9606
436	P63261	9606
437	P42025	9606
438	P61163	9606
439	P37023	9606
440	O14672	9606
441	O43184	9606
442	P78536	9606
443	Q9P0K1	9606
444	Q9UKQ2	9606
445	Q9UKF5	9606
446	Q13443	9606
447	P00813	9606
448	Q8NI60	9606
449	Q5VUY2	9606
450	Q8NFM4	9606
451	P40145	9606
452	Q9NRN7	9606
453	Q3LIE5	9606
454	Q16186	9606
455	P22570	9606
456	Q9H0C2	9606
457	Q96SZ5	9606
458	Q8TED9	9606
459	P42568	9606
460	P51816	9606
461	Q9UHB7	9606
462	Q8TF27	9606
463	Q5VW22	9606
464	P52594	9606
465	O95394	9606
466	Q9H9G7	9606
467	Q86SQ6	9606
468	O60241	9606
469	P50052	9606
470	P35869	9606
471	Q86UN6	9606
472	Q9P0M2	9606
473	Q92667	9606
474	A6NHY2	9606
475	Q53H80	9606
476	Q5T1N1	9606
477	P00352	9606
478	P36544	9606
479	P17787	9606
480	Q04844	9606
481	Q5JWF8	9606
482	P08912	9606
483	P49753	9606
484	O14734	9606
485	Q6ZNF0	9606
486	Q08AH3	9606
487	Q4G176	9606
488	Q9ULC5	9606
489	Q6P461	9606
490	P35609	9606
491	Q08043	9606
492	O43707	9606
493	P07311	9606
494	Q13444	9606
495	P35348	9606
496	P25100	9606
497	Q9UKJ8	9606
498	Q8TC27	9606
499	Q8NCV1	9606
500	O75689	9606
\.


--
-- Name: protein_2_taxid_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dblyon
--

SELECT pg_catalog.setval('protein_2_taxid_id_seq', 1, false);


--
-- Data for Name: protein_2_version; Type: TABLE DATA; Schema: public; Owner: dblyon
--

COPY protein_2_version (id, an, version) FROM stdin;
1	P31946	201607
2	P04439	201607
3	P01889	201607
4	P30464	201607
5	P30685	201607
6	Q95365	201607
7	Q04826	201607
8	P30484	201607
9	P30492	201607
10	P30493	201607
11	P18465	201607
12	Q29836	201607
13	Q31610	201607
14	P30499	201607
15	Q29865	201607
16	P14060	201607
17	P26439	201607
18	Q9Y3L3	201607
19	P78314	201607
20	P29372	201607
21	P28566	201607
22	Q8NAA4	201607
23	P01009	201607
24	P29274	201607
25	P29275	201607
26	Q9NRG9	201607
27	P31941	201607
28	O94911	201607
29	Q9NUT2	201607
30	Q9NRK6	201607
31	Q9H221	201607
32	Q8TB40	201607
33	O94929	201607
34	Q8N961	201607
35	O00763	201607
36	Q9H845	201607
37	P11310	201607
38	Q96P50	201607
39	O00400	201607
40	Q5T8D3	201607
41	Q9BR61	201607
42	Q5FVE4	201607
43	P30443	201607
44	P01892	201607
45	P13746	201607
46	Q96QU6	201607
47	P30447	201607
48	P18462	201607
49	P16190	201607
50	P30455	201607
51	P30457	201607
52	P01891	201607
53	P30460	201607
54	P30480	201607
55	P30483	201607
56	Q29940	201607
57	P30498	201607
58	Q9TNN7	201607
59	Q29963	201607
60	P30505	201607
61	P30510	201607
62	Q95604	201607
63	Q16537	201607
64	Q66LE6	201607
65	Q9Y2T4	201607
66	P13760	201607
67	P20039	201607
68	P01911	201607
69	Q7L8J4	201607
70	O60239	201607
71	Q13541	201607
72	O60516	201607
73	P28222	201607
74	P28221	201607
75	O95264	201607
76	P34969	201607
77	Q969T7	201607
78	P52209	201607
79	P36639	201607
80	Q676U5	201607
81	P02763	201607
82	P20848	201607
83	Q96IX9	201607
84	Q9NPC4	201607
85	P05067	201607
86	Q96GX2	201607
87	Q9H7C9	201607
88	Q13685	201607
89	Q9Y312	201607
90	Q8NHS2	201607
91	P00505	201607
92	Q9NUQ8	201607
93	Q9H222	201607
94	P16219	201607
95	Q8NC06	201607
96	Q709F0	201607
97	Q4AC99	201607
98	P30450	201607
99	P16188	201607
100	P10314	201607
101	P30456	201607
102	P10316	201607
103	P30461	201607
104	P30485	201607
105	P30487	201607
106	P18464	201607
107	P30490	201607
108	P10319	201607
109	Q31612	201607
110	Q29718	201607
111	P30504	201607
112	P10321	201607
113	P30508	201607
114	Q29960	201607
115	Q29974	201607
116	Q13542	201607
117	P41595	201607
118	P28335	201607
119	Q13639	201607
120	P50406	201607
121	Q9H0P0	201607
122	P49902	201607
123	Q5TYW2	201607
124	Q5VUR7	201607
125	P0DMS8	201607
126	Q9NS82	201607
127	Q8N5Z0	201607
128	O43741	201607
129	Q9UGJ0	201607
130	Q9BTE6	201607
131	Q9UDR5	201607
132	Q9NY61	201607
133	Q9NRW3	201607
134	Q6NTF7	201607
135	Q9BZC7	201607
136	P78363	201607
137	Q4W5N1	201607
138	Q86UK0	201607
139	Q9NSE7	201607
140	P45844	201607
141	Q0P651	201607
142	Q9Y235	201607
143	Q8WW27	201607
144	Q96I13	201607
145	Q8NFV4	201607
146	Q9P2A4	201607
147	Q969K4	201607
148	Q15027	201607
149	Q15057	201607
150	Q8N6N7	201607
151	P45954	201607
152	Q5QJU3	201607
153	P12821	201607
154	Q9NPB9	201607
155	Q9Y614	201607
156	P62258	201607
157	Q04917	201607
158	P61981	201607
159	Q9TQE0	201607
160	P31937	201607
161	P30939	201607
162	P28223	201607
163	Q9BXI3	201607
164	P05408	201607
165	Q6PD74	201607
166	Q2M2I8	201607
167	Q9Y478	201607
168	P54619	201607
169	Q9UGI9	201607
170	Q96AK3	201607
171	Q99758	201607
172	O75027	201607
173	Q09428	201607
174	P08910	201607
175	Q8WTS1	201607
176	Q9BUJ0	201607
177	Q96IU4	201607
178	P42684	201607
179	Q9ULW3	201607
180	Q9BYF1	201607
181	P32297	201607
182	Q05901	201607
183	P30926	201607
184	Q9UKV3	201607
185	Q07912	201607
186	Q16570	201607
187	P20309	201607
188	Q8WXI4	201607
189	Q8N1Q8	201607
190	Q99798	201607
191	Q3I5F7	201607
192	P63104	201607
193	P05534	201607
194	P30512	201607
195	P16189	201607
196	P30453	201607
197	P30459	201607
198	P30462	201607
199	P30466	201607
200	P03989	201607
201	P18463	201607
202	P30475	201607
203	P30479	201607
204	P30481	201607
205	P30486	201607
206	P30488	201607
207	P30491	201607
208	P30495	201607
209	P30501	201607
210	P04222	201607
211	Q07000	201607
212	Q15172	201607
213	Q13362	201607
214	Q30134	201607
215	P46952	201607
216	Q8WXA8	201607
217	A5X5Y0	201607
218	P04217	201607
219	Q9NQ94	201607
220	Q5SQ80	201607
221	Q4UJ75	201607
222	Q5T5F5	201607
223	P22760	201607
224	Q15758	201607
225	Q86V21	201607
226	P54646	201607
227	Q5VST6	201607
228	Q7Z5R6	201607
229	Q9UH17	201607
230	Q8IUX4	201607
231	Q9HC16	201607
232	O95477	201607
233	Q8WWZ7	201607
234	Q8IZY2	201607
235	Q2M3G0	201607
236	Q9NP58	201607
237	O60706	201607
238	O14678	201607
239	Q8NE71	201607
240	Q8N2K0	201607
241	Q96SE0	201607
242	Q8WU67	201607
243	Q9BV23	201607
244	Q8IZP0	201607
245	O14639	201607
246	Q6H8Q1	201607
247	Q9P1F3	201607
248	Q8N0Z2	201607
249	P07108	201607
250	Q8TDN7	201607
251	Q9NUN7	201607
252	P43681	201607
253	Q07001	201607
254	Q9Y615	201607
255	Q8WYK0	201607
256	Q9NUB1	201607
257	Q4L235	201607
258	Q8TC94	201607
259	Q03154	201607
260	P11171	201607
261	Q9NRA8	201607
262	P08195	201607
263	P08908	201607
264	P46098	201607
265	Q70Z44	201607
266	P47898	201607
267	Q96P26	201607
268	P21589	201607
269	P56378	201607
270	P19652	201607
271	U3KPV4	201607
272	Q7RTV5	201607
273	Q8N139	201607
274	Q8IUA7	201607
275	Q8WWZ4	201607
276	Q86UQ4	201607
277	Q96J66	201607
278	P33897	201607
279	Q9UNQ0	201607
280	P41238	201607
281	Q9H3Z7	201607
282	P00519	201607
283	Q12979	201607
284	Q96AP0	201607
285	P25106	201607
286	Q86TX2	201607
287	Q8N9L9	201607
288	Q15067	201607
289	Q99424	201607
290	P13798	201607
291	P12814	201607
292	O75078	201607
293	Q9Y3Q7	201607
294	Q6NVV9	201607
295	Q9H2U9	201607
296	P78325	201607
297	Q9NPF8	201607
298	Q08462	201607
299	O95622	201607
300	P35612	201607
301	P30153	201607
302	Q00005	201607
303	P04229	201607
304	Q30167	201607
305	Q5Y7A7	201607
306	Q9H2F3	201607
307	O95336	201607
308	P0DKL9	201607
309	Q8NF67	201607
310	A0PJZ0	201607
311	P08697	201607
312	P01023	201607
313	A7E2S9	201607
314	Q9UNA3	201607
315	P30542	201607
316	Q7Z5M8	201607
317	Q96GS6	201607
318	Q6PCB6	201607
319	O95870	201607
320	Q13085	201607
321	Q9UKU7	201607
322	P28330	201607
323	P49748	201607
324	Q96GR2	201607
325	P30532	201607
326	Q15825	201607
327	Q9UGM1	201607
328	P08172	201607
329	P21399	201607
330	O00767	201607
331	Q96QF7	201607
332	P33121	201607
333	P63267	201607
334	Q8TDG2	201607
335	O43506	201607
336	O75077	201607
337	P08913	201607
338	Q9BZ11	201607
339	Q96M93	201607
340	Q6DHV7	201607
341	Q99965	201607
342	O00116	201607
343	Q5VUY0	201607
344	Q08828	201607
345	P35611	201607
346	Q8N7X0	201607
347	Q6IQ32	201607
348	Q9BRR6	201607
349	Q96A54	201607
350	Q6UXC1	201607
351	Q8N556	201607
352	Q6ULP2	201607
353	Q5I7T1	201607
354	P31947	201607
355	P27348	201607
356	Q09160	201607
357	Q15173	201607
358	Q14738	201607
359	P30154	201607
360	P63151	201607
361	P01912	201607
362	P13761	201607
363	Q95IE3	201607
364	Q9GIY3	201607
365	Q8IZ83	201607
366	P02750	201607
367	A8K2U0	201607
368	P01011	201607
369	Q13131	201607
370	Q4LEZ3	201607
371	P86434	201607
372	P17174	201607
373	Q9NP78	201607
374	O95342	201607
375	Q9UBJ2	201607
376	P28288	201607
377	P61221	201607
378	Q9UG63	201607
379	Q9H172	201607
380	Q6UXT9	201607
381	Q9NUJ1	201607
382	Q7L211	201607
383	Q9NYB9	201607
384	Q15822	201607
385	O96019	201607
386	Q9Y305	201607
387	P10323	201607
388	Q68CK6	201607
389	Q53FZ2	201607
390	Q6NUN0	201607
391	P62736	201607
392	Q9BYX7	201607
393	P68032	201607
394	Q8TDY3	201607
395	Q04771	201607
396	Q7Z695	201607
397	Q3MIX3	201607
398	O60266	201607
399	P51828	201607
400	P07327	201607
401	P00325	201607
402	P00326	201607
403	Q8WTP8	201607
404	A6NIR3	201607
405	Q9H0P7	201607
406	Q53H12	201607
407	Q14246	201607
408	Q9BY15	201607
409	Q5T601	201607
410	Q86Y34	201607
411	O00253	201607
412	Q9BRQ8	201607
413	Q8N1P7	201607
414	Q9Y4K1	201607
415	Q6JQN1	201607
416	P22303	201607
417	Q9GZZ6	201607
418	P02708	201607
419	P11230	201607
420	P07510	201607
421	O00590	201607
422	O94805	201607
423	P53396	201607
424	P11229	201607
425	P08173	201607
426	Q8TDX5	201607
427	Q9NPJ3	201607
428	O14561	201607
429	Q8NEB7	201607
430	Q9NR19	201607
431	Q96CM8	201607
432	Q9UKU0	201607
433	Q08AH1	201607
434	P0C7M7	201607
435	Q9H6R3	201607
436	P63261	201607
437	P42025	201607
438	P61163	201607
439	P37023	201607
440	O14672	201607
441	O43184	201607
442	P78536	201607
443	Q9P0K1	201607
444	Q9UKQ2	201607
445	Q9UKF5	201607
446	Q13443	201607
447	P00813	201607
448	Q8NI60	201607
449	Q5VUY2	201607
450	Q8NFM4	201607
451	P40145	201607
452	Q9NRN7	201607
453	Q3LIE5	201607
454	Q16186	201607
455	P22570	201607
456	Q9H0C2	201607
457	Q96SZ5	201607
458	Q8TED9	201607
459	P42568	201607
460	P51816	201607
461	Q9UHB7	201607
462	Q8TF27	201607
463	Q5VW22	201607
464	P52594	201607
465	O95394	201607
466	Q9H9G7	201607
467	Q86SQ6	201607
468	O60241	201607
469	P50052	201607
470	P35869	201607
471	Q86UN6	201607
472	Q9P0M2	201607
473	Q92667	201607
474	A6NHY2	201607
475	Q53H80	201607
476	Q5T1N1	201607
477	P00352	201607
478	P36544	201607
479	P17787	201607
480	Q04844	201607
481	Q5JWF8	201607
482	P08912	201607
483	P49753	201607
484	O14734	201607
485	Q6ZNF0	201607
486	Q08AH3	201607
487	Q4G176	201607
488	Q9ULC5	201607
489	Q6P461	201607
490	P35609	201607
491	Q08043	201607
492	O43707	201607
493	P07311	201607
494	Q13444	201607
495	P35348	201607
496	P25100	201607
497	Q9UKJ8	201607
498	Q8TC27	201607
499	Q8NCV1	201607
500	O75689	201607
\.


--
-- Name: protein_2_version_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dblyon
--

SELECT pg_catalog.setval('protein_2_version_id_seq', 1, false);


--
-- Data for Name: proteins; Type: TABLE DATA; Schema: public; Owner: dblyon
--

COPY proteins (id, an, header, aaseq) FROM stdin;
1	P31946	>sp|P31946|1433B_HUMAN 14-3-3 protein beta/alpha GN=YWHAB PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MTMDKSELVQKAKLAEQAERYDDMAAAMKAVTEQGHELSNEERNLLSVAYKNVVGARRSSWRVISSIEQKTERNEKKQQMGKEYREKIEAELQDICNDVLELLDKYLIPNATQPESKVFYLKMKGDYFRYLSEVASGDNKQTTVSNSQQAYQEAFEISKKEMQPTHPIRLGLALNFSVFYYEILNSPEKACSLAKTAFDEAIAELDTLNEESYKDSTLIMQLLRDNLTLWTSENQGDEGDAGEGEN
2	P04439	>sp|P04439|1A03_HUMAN HLA class I histocompatibility antigen, A-3 alpha chain GN=HLA-A PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMAPRTLLLLLSGALALTQTWAGSHSMRYFFTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDQETRNVKAQSQTDRVDLGTLRGYYNQSEAGSHTIQIMYGCDVGSDGRFLRGYRQDAYDGKDYIALNEDLRSWTAADMAAQITKRKWEAAHEAEQLRAYLDGTCVEWLRRYLENGKETLQRTDPPKTHMTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWELSSQPTIPIVGIIAGLVLLGAVITGAVVAAVMWRRKSSDRKGGSYTQAASSDSAQGSDVSLTACKV
3	P01889	>sp|P01889|1B07_HUMAN HLA class I histocompatibility antigen, B-7 alpha chain GN=HLA-B PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MLVMAPRTVLLLLSAALALTETWAGSHSMRYFYTSVSRPGRGEPRFISVGYVDDTQFVRFDSDAASPREEPRAPWIEQEGPEYWDRNTQIYKAQAQTDRESLRNLRGYYNQSEAGSHTLQSMYGCDVGPDGRLLRGHDQYAYDGKDYIALNEDLRSWTAADTAAQITQRKWEAAREAEQRRAYLEGECVEWLRRYLENGKDKLERADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCRRKSSGGKGGSYSQAACSDSAQGSDVSLTA
4	P30464	>sp|P30464|1B15_HUMAN HLA class I histocompatibility antigen, B-15 alpha chain GN=HLA-B PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTVLLLLSGALALTETWAGSHSMRYFYTAMSRPGRGEPRFIAVGYVDDTQFVRFDSDAASPRMAPRAPWIEQEGPEYWDRETQISKTNTQTYRESLRNLRGYYNQSEAGSHTLQRMYGCDVGPDGRLLRGHDQSAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAAREAEQWRAYLEGLCVEWLRRYLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
5	P30685	>sp|P30685|1B35_HUMAN HLA class I histocompatibility antigen, B-35 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTVLLLLWGAVALTETWAGSHSMRYFYTAMSRPGRGEPRFIAVGYVDDTQFVRFDSDAASPRTEPRAPWIEQEGPEYWDRNTQIFKTNTQTYRESLRNLRGYYNQSEAGSHIIQRMYGCDLGPDGRLLRGHDQSAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAARVAEQLRAYLEGLCVEWLRRYLENGKETLQRADPPKTHVTHHPVSDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
6	Q95365	>sp|Q95365|1B38_HUMAN HLA class I histocompatibility antigen, B-38 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLVMAPRTVLLLLSAALALTETWAGSHSMRYFYTSVSRPGRGEPRFISVGYVDDTQFVRFDSDAASPREEPRAPWIEQEGPEYWDRNTQICKTNTQTYRENLRIALRYYNQSEAGSHTLQRMYGCDVGPDGRLLRGHNQFAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAARVAEQLRTYLEGTCVEWLRRYLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
7	Q04826	>sp|Q04826|1B40_HUMAN HLA class I histocompatibility antigen, B-40 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTLLLLLWGAVALTETWAGSHSMRYFHTSVSRPGRGEPRFITVGYVDDTLFVRFDSDATSPRKEPRAPWIEQEGPEYWDRETQISKTNTQTYRESLRNLRGYYNQSEAGSHTLQSMYGCDVGPDGRLLRGHNQYAYDGKDYIALNEDLRSWTAADTAAQITQRKWEAARVAEQLRAYLEGECVEWLRRYLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCRRKSSGGKGGSYSQAACSDSAQGSDVSLTA
8	P30484	>sp|P30484|1B46_HUMAN HLA class I histocompatibility antigen, B-46 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTVLLLLSGALALTETWAGSHSMRYFYTAMSRPGRGEPRFIAVGYVDDTQFVRFDSDAASPRMAPRAPWIEQEGPEYWDRETQKYKRQAQTDRVSLRNLRGYYNQSEAGSHTLQRMYGCDVGPDGRLLRGHDQSAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAAREAEQWRAYLEGLCVEWLRRYLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
9	P30492	>sp|P30492|1B54_HUMAN HLA class I histocompatibility antigen, B-54 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTLLLLLWGALALTETWAGSHSMRYFYTAMSRPGRGEPRFIAVGYVDDTQFVRFDSDAASPRGEPRAPWVEQEGPEYWDRNTQIYKAQAQTDRESLRNLRGYYNQSEAGSHTWQTMYGCDLGPDGRLLRGHNQLAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAARVAEQLRAYLEGTCVEWLRRYLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
10	P30493	>sp|P30493|1B55_HUMAN HLA class I histocompatibility antigen, B-55 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTLLLLLWGALALTETWAGSHSMRYFYTAMSRPGRGEPRFIAVGYVDDTQFVRFDSDAASPREEPRAPWIEQEGPEYWDRNTQIYKAQAQTDRESLRNLRGYYNQSEAGSHTWQTMYGCDLGPDGRLLRGHNQLAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAAREAEQLRAYLEGTCVEWLRRYLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
11	P18465	>sp|P18465|1B57_HUMAN HLA class I histocompatibility antigen, B-57 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTVLLLLWGAVALTETWAGSHSMRYFYTAMSRPGRGEPRFIAVGYVDDTQFVRFDSDAASPRMAPRAPWIEQEGPEYWDGETRNMKASAQTYRENLRIALRYYNQSEAGSHIIQVMYGCDVGPDGRLLRGHDQSAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAARVAEQLRAYLEGLCVEWLRRYLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCRRKSSGGKGGSYSQAACSDSAQGSDVSLTA
12	Q29836	>sp|Q29836|1B67_HUMAN HLA class I histocompatibility antigen, B-67 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLVMAPRTVLLLLSAALALTETWAGSHSMRYFYTSVSRPGRGEPRFISVGYVDDTQFVRFDSDAASPREEPRAPWIEQEGPEYWDRNTQIYKAQAQTDRESLRNLRGYYNQSEAGSHTLQRMYGCDVGPDGRLLRGHNQFAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAARVAEQLRTYLEGTCVEWLRRYLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
13	Q31610	>sp|Q31610|1B81_HUMAN HLA class I histocompatibility antigen, B-81 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLVMAPRTVLLLLWGAVALTETWAGSHSMRYFYTSVSRPGRGEPRFISVGYVDDTQFVRFDSDAASPREEPRAPWIEQEGPEYWDRNTQIYKAQAQTDRESLRNLRGYYNQSEAGSHTLQSMYGCDVGPDGRLLRGHNQYAYDGKDYIALNEDLRSWTAADTAAQISQRKLEAARVAEQLRAYLEGECVEWLRRYLENGKDKLERADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWTAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCRRKSSGGKGGSYSQAACSDSAQGSDVSLTA
14	P30499	>sp|P30499|1C01_HUMAN HLA class I histocompatibility antigen, Cw-1 alpha chain GN=HLA-C PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVMEPRTLILLLSGALALTETWACSHSMKYFFTSVSRPGRGEPRFISVGYVDDTQFVRFDSDAASPRGEPRAPWVEQEGPEYWDRETQKYNRQAQTDRVSLRNLRGYYNQSEAGSHTLQWMCGCDLGPDGRLLRGYDQYAYDGKDYIALNEDLRSWTAADTAAQITQRKWEAAREAEERRAYLEGTCVEWLRRYLENGKESLQRAEHPKTHVTHHPVSDHEATLRCWALGFYPAEITLTWQWDGEDQTQDTELVETRPAGDGTFQKWAAVMVPSGEEQRYTCHVQHEGLPEPLTLRWEPSSQPTIPIVGIVAGLAVLAVLAVLGAVVAVVMCRRKSSGGKGGSCSQAASSNSAQGSDESLIASKA
15	Q29865	>sp|Q29865|1C18_HUMAN HLA class I histocompatibility antigen, Cw-18 alpha chain GN=HLA-C PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVMAPRALLLLLSGGLALTETWACSHSMRYFDTAVSRPGRGEPRFISVGYVDDTQFVRFDSDAASPRGEPRAPWVEQEGPEYWDRETQKYKRQAQADRVNLRKLRGYYNQSEDGSHTLQRMFGCDLGPDGRLLRGYNQFAYDGKDYIALNEDLRSWTAADTAAQITQRKWEAAREAEQRRAYLEGTCVEWLRRYLENGKETLQRAEHPKTHVTHHPVSDHEATLRCWALGFYPAEITLTWQWDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPEPLTLRWKPSSQPTIPIVGIVAGLAVLVVLAVLGAVVAVVMCRRKSSGGKGGSCSQAASSNSAQGSDESLIACKA
16	P14060	>sp|P14060|3BHS1_HUMAN 3 beta-hydroxysteroid dehydrogenase/Delta 5-->4-isomerase type 1 GN=HSD3B1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MTGWSCLVTGAGGFLGQRIIRLLVKEKELKEIRVLDKAFGPELREEFSKLQNKTKLTVLEGDILDEPFLKRACQDVSVIIHTACIIDVFGVTHRESIMNVNVKGTQLLLEACVQASVPVFIYTSSIEVAGPNSYKEIIQNGHEEEPLENTWPAPYPHSKKLAEKAVLAANGWNLKNGGTLYTCALRPMYIYGEGSRFLSASINEALNNNGILSSVGKFSTVNPVYVGNVAWAHILALRALQDPKKAPSIRGQFYYISDDTPHQSYDNLNYTLSKEFGLRLDSRWSFPLSLMYWIGFLLEIVSFLLRPIYTYRPPFNRHIVTLSNSVFTFSYKKAQRDLAYKPLYSWEEAKQKTVEWVGSLVDRHKETLKSKTQ
17	P26439	>sp|P26439|3BHS2_HUMAN 3 beta-hydroxysteroid dehydrogenase/Delta 5-->4-isomerase type 2 GN=HSD3B2 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MGWSCLVTGAGGLLGQRIVRLLVEEKELKEIRALDKAFRPELREEFSKLQNRTKLTVLEGDILDEPFLKRACQDVSVVIHTACIIDVFGVTHRESIMNVNVKGTQLLLEACVQASVPVFIYTSSIEVAGPNSYKEIIQNGHEEEPLENTWPTPYPYSKKLAEKAVLAANGWNLKNGDTLYTCALRPTYIYGEGGPFLSASINEALNNNGILSSVGKFSTVNPVYVGNVAWAHILALRALRDPKKAPSVRGQFYYISDDTPHQSYDNLNYILSKEFGLRLDSRWSLPLTLMYWIGFLLEVVSFLLSPIYSYQPPFNRHTVTLSNSVFTFSYKKAQRDLAYKPLYSWEEAKQKTVEWVGSLVDRHKETLKSKTQ
18	Q9Y3L3	>sp|Q9Y3L3|3BP1_HUMAN SH3 domain-binding protein 1 GN=SH3BP1 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MMKRQLHRMRQLAQTGSLGRTPETAEFLGEDLLQVEQRLEPAKRAAHNIHKRLQACLQGQSGADMDKRVKKLPLMALSTTMAESFKELDPDSSMGKALEMSCAIQNQLARILAEFEMTLERDVLQPLSRLSEEELPAILKHKKSLQKLVSDWNTLKSRLSQATKNSGSSQGLGGSPGSHSHTTMANKVETLKEEEEELKRKVEQCRDEYLADLYHFVTKEDSYANYFIRLLEIQADYHRRSLSSLDTALAELRENHGQADHSPSMTATHFPRVYGVSLATHLQELGREIALPIEACVMMLLSEGMKEEGLFRLAAGASVLKRLKQTMASDPHSLEEFCSDPHAVAGALKSYLRELPEPLMTFDLYDDWMRAASLKEPGARLQALQEVCSRLPPENLSNLRYLMKFLARLAEEQEVNKMTPSNIAIVLGPNLLWPPEKEGDQAQLDAASVSSIQVVGVVEALIQSADTLFPGDINFNVSGLFSAVTLQDTVSDRLASEELPSTAVPTPATTPAPAPAPAPAPAPALASAATKERTESEVPPRPASPKVTRSPPETAAPVEDMARRTKRPAPARPTMPPPQVSGSRSSPPAPPLPPGSGSPGTPQALPRRLVGSSLRAPTVPPPLPPTPPQPARRQSRRSPASPSPASPGPASPSPVSLSNPAQVDLGAATAEGGAPEAISGVPTPPAIPPQPRPRSLASETN
19	P78314	>sp|P78314|3BP2_HUMAN SH3 domain-binding protein 2 GN=SH3BP2 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAAEEMHWPVPMKAIGAQNLLTMPGGVAKAGYLHKKGGTQLQLLKWPLRFVIIHKRCVYYFKSSTSASPQGAFSLSGYNRVMRAAEETTSNNVFPFKIIHISKKHRTWFFSASSEEERKSWMALLRREIGHFHEKKDLPLDTSDSSSDTDSFYGAVERPVDISLSPYPTDNEDYEHDDEDDSYLEPDSPEPGRLEDALMHPPAYPPPPVPTPRKPAFSDMPRAHSFTSKGPGPLLPPPPPKHGLPDVGLAAEDSKRDPLCPRRAEPCPRVPATPRRMSDPPLSTMPTAPGLRKPPCFRESASPSPEPWTPGHGACSTSSAAIMATATSRNCDKLKSFHLSPRGPPTSEPPPVPANKPKFLKIAEEDPPREAAMPGLFVPPVAPRPPALKLPVPEAMARPAVLPRPEKPQLPHLQRSPPDGQSFRSFSFEKPRQPSQADTGGDDSDEDYEKVPLPNSVFVNTTESCEVERLFKATSPRGEPQDGLYCIRNSSTKSGKVLVVWDETSNKVRNYRIFEKDSKFYLEGEVLFVSVGSMVEHYHTHVLPSHQSLLLRHPYGYTGPR
20	P29372	>sp|P29372|3MG_HUMAN DNA-3-methyladenine glycosylase GN=MPG PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MVTPALQMKKPKQFCRRMGQKKQRPARAGQPHSSSDAAQAPAEQPHSSSDAAQAPCPRERCLGPPTTPGPYRSIYFSSPKGHLTRLGLEFFDQPAVPLARAFLGQVLVRRLPNGTELRGRIVETEAYLGPEDEAAHSRGGRQTPRNRGMFMKPGTLYVYIIYGMYFCMNISSQGDGACVLLRALEPLEGLETMRQLRSTLRKGTASRVLKDRELCSGPSKLCQALAINKSFDQRDLAQDEAVWLERGPLEPSEPAVVAAARVGVGHAGEWARKPLRFYVRGSPWVSVVDRVAEQDTQA
21	P28566	>sp|P28566|5HT1E_HUMAN 5-hydroxytryptamine receptor 1E GN=HTR1E PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MNITNCTTEASMAIRPKTITEKMLICMTLVVITTLTTLLNLAVIMAIGTTKKLHQPANYLICSLAVTDLLVAVLVMPLSIIYIVMDRWKLGYFLCEVWLSVDMTCCTCSILHLCVIALDRYWAITNAIEYARKRTAKRAALMILTVWTISIFISMPPLFWRSHRRLSPPPSQCTIQHDHVIYTIYSTLGAFYIPLTLILILYYRIYHAAKSLYQKRGSSRHLSNRSTDSQNSFASCKLTQTFCVSDFSTSDPTTEFEKFHASIRIPPFDNDLDHPGERQQISSTRERKAARILGLILGAFILSWLPFFIKELIVGLSIYTVSSEVADFLTWLGYVNSLINPLLYTSFNEDFKLAFKKLIRCREHT
22	Q8NAA4	>sp|Q8NAA4|A16L2_HUMAN Autophagy-related protein 16-2 GN=ATG16L2 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAGPGVPGAPAARWKRHIVRQLRLRDRTQKALFLELVPAYNHLLEKAELLDKFSKKLQPEPNSVTPTTHQGPWEESELDSDQVPSLVALRVKWQEEEEGLRLVCGEMAYQVVEKGAALGTLESELQQRQSRLAALEARVAQLREARAQQAQQVEEWRAQNAVQRAAYEALRAHVGLREAALRRLQEEARDLLERLVQRKARAAAERNLRNERRERAKQARVSQELKKAAKRTVSISEGPDTLGDGMRERRETLALAPEPEPLEKEACEKWKRPFRSASATSLTLSHCVDVVKGLLDFKKRRGHSIGGAPEQRYQIIPVCVAARLPTRAQDVLDAHLSEVNAVRFGPNSSLLATGGADRLIHLWNVVGSRLEANQTLEGAGGSITSVDFDPSGYQVLAATYNQAAQLWKVGEAQSKETLSGHKDKVTAAKFKLTRHQAVTGSRDRTVKEWDLGRAYCSRTINVLSYCNDVVCGDHIIISGHNDQKIRFWDSRGPHCTQVIPVQGRVTSLSLSHDQLHLLSCSRDNTLKVIDLRVSNIRQVFRADGFKCGSDWTKAVFSPDRSYALAGSCDGALYIWDVDTGKLESRLQGPHCAAVNAVAWCYSGSHMVSVDQGRKVVLWQ
23	P01009	>sp|P01009|A1AT_HUMAN Alpha-1-antitrypsin GN=SERPINA1 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MPSSVSWGILLLAGLCCLVPVSLAEDPQGDAAQKTDTSHHDQDHPTFNKITPNLAEFAFSLYRQLAHQSNSTNIFFSPVSIATAFAMLSLGTKADTHDEILEGLNFNLTEIPEAQIHEGFQELLRTLNQPDSQLQLTTGNGLFLSEGLKLVDKFLEDVKKLYHSEAFTVNFGDTEEAKKQINDYVEKGTQGKIVDLVKELDRDTVFALVNYIFFKGKWERPFEVKDTEEEDFHVDQVTTVKVPMMKRLGMFNIQHCKKLSSWVLLMKYLGNATAIFFLPDEGKLQHLENELTHDIITKFLENEDRRSASLHLPKLSITGTYDLKSVLGQLGITKVFSNGADLSGVTEEAPLKLSKAVHKAVLTIDEKGTEAAGAMFLEAIPMSIPPEVKFNKPFVFLMIEQNTKSPLFMGKVVNPTQK
24	P29274	>sp|P29274|AA2AR_HUMAN Adenosine receptor A2a GN=ADORA2A PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MPIMGSSVYITVELAIAVLAILGNVLVCWAVWLNSNLQNVTNYFVVSLAAADIAVGVLAIPFAITISTGFCAACHGCLFIACFVLVLTQSSIFSLLAIAIDRYIAIRIPLRYNGLVTGTRAKGIIAICWVLSFAIGLTPMLGWNNCGQPKEGKNHSQGCGEGQVACLFEDVVPMNYMVYFNFFACVLVPLLLMLGVYLRIFLAARRQLKQMESQPLPGERARSTLQKEVHAAKSLAIIVGLFALCWLPLHIINCFTFFCPDCSHAPLWLMYLAIVLSHTNSVVNPFIYAYRIREFRQTFRKIIRSHVLRQQEPFKAAGTSARVLAAHGSDGEQVSLRLNGHPPGVWANGSAPHPERRPNGYALGLVSGGSAQESQGNTGLPDVELLSHELKGVCPEPPGLDDPLAQDGAGVS
25	P29275	>sp|P29275|AA2BR_HUMAN Adenosine receptor A2b GN=ADORA2B PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLLETQDALYVALELVIAALSVAGNVLVCAAVGTANTLQTPTNYFLVSLAAADVAVGLFAIPFAITISLGFCTDFYGCLFLACFVLVLTQSSIFSLLAVAVDRYLAICVPLRYKSLVTGTRARGVIAVLWVLAFGIGLTPFLGWNSKDSATNNCTEPWDGTTNESCCLVKCLFENVVPMSYMVYFNFFGCVLPPLLIMLVIYIKIFLVACRQLQRTELMDHSRTTLQREIHAAKSLAMIVGIFALCWLPVHAVNCVTLFQPAQGKNKPKWAMNMAILLSHANSVVNPIVYAYRNRDFRYTFHKIISRYLLCQADVKSGNGQAGVQPALGVGL
26	Q9NRG9	>sp|Q9NRG9|AAAS_HUMAN Aladin GN=AAAS PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MCSLGLFPPPPPRGQVTLYEHNNELVTGSSYESPPPDFRGQWINLPVLQLTKDPLKTPGRLDHGTRTAFIHHREQVWKRCINIWRDVGLFGVLNEIANSEEEVFEWVKTASGWALALCRWASSLHGSLFPHLSLRSEDLIAEFAQVTNWSSCCLRVFAWHPHTNKFAVALLDDSVRVYNASSTIVPSLKHRLQRNVASLAWKPLSASVLAVACQSCILIWTLDPTSLSTRPSSGCAQVLSHPGHTPVTSLAWAPSGGRLLSASPVDAAIRVWDVSTETCVPLPWFRGGGVTNLLWSPDGSKILATTPSAVFRVWEAQMWTCERWPTLSGRCQTGCWSPDGSRLLFTVLGEPLIYSLSFPERCGEGKGCVGGAKSATIVADLSETTIQTPDGEERLGGEAHSMVWDPSGERLAVLMKGKPRVQDGKPVILLFRTRNSPVFELLPCGIIQGEPGAQPQLITFHPSFNKGALLSVGWSTGRIAHIPLYFVNAQFPRFSPVLGRAQEPPAGGGGSIHDLPLFTETSPTSAPWDPLPGPPPVLPHSPHSHL
27	P31941	>sp|P31941|ABC3A_HUMAN DNA dC->dU-editing enzyme APOBEC-3A GN=APOBEC3A PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MEASPASGPRHLMDPHIFTSNFNNGIGRHKTYLCYEVERLDNGTSVKMDQHRGFLHNQAKNLLCGFYGRHAELRFLDLVPSLQLDPAQIYRVTWFISWSPCFSWGCAGEVRAFLQENTHVRLRIFAARIYDYDPLYKEALQMLRDAGAQVSIMTYDEFKHCWDTFVDHQGCPFQPWDGLDEHSQALSGRLRAILQNQGN
37	P11310	>sp|P11310|ACADM_HUMAN Medium-chain specific acyl-CoA dehydrogenase, mitochondrial GN=ACADM PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAAGFGRCCRVLRSISRFHWRSQHTKANRQREPGLGFSFEFTEQQKEFQATARKFAREEIIPVAAEYDKTGEYPVPLIRRAWELGLMNTHIPENCGGLGLGTFDACLISEELAYGCTGVQTAIEGNSLGQMPIIIAGNDQQKKKYLGRMTEEPLMCAYCVTEPGAGSDVAGIKTKAEKKGDEYIINGQKMWITNGGKANWYFLLARSDPDPKAPANKAFTGFIVEADTPGIQIGRKELNMGQRCSDTRGIVFEDVKVPKENVLIGDGAGFKVAMGAFDKTRPVVAAGAVGLAQRALDEATKYALERKTFGKLLVEHQAISFMLAEMAMKVELARMSYQRAAWEVDSGRRNTYYASIAKAFAGDIANQLATDAVQILGGNGFNTEYPVEKLMRDAKIYQIYEGTSQIQRLIVAREHIDKYKN
134	Q6NTF7	>sp|Q6NTF7|ABC3H_HUMAN DNA dC->dU-editing enzyme APOBEC-3H GN=APOBEC3H PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MALLTAETFRLQFNNKRRLRRPYYPRKALLCYQLTPQNGSTPTRGYFENKKKCHAEICFINEIKSMGLDETQCYQVTCYLTWSPCSSCAWELVDFIKAHDHLNLGIFASRLYYHWCKPQQKGLRLLCGSQVPVEVMGFPKFADCWENFVDHEKPLSFNPYKMLEELDKNSRAIKRRLERIKIPGVRAQGRYMDILCDAEV
28	O94911	>sp|O94911|ABCA8_HUMAN ATP-binding cassette sub-family A member 8 GN=ABCA8 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MRKRKISVCQQTWALLCKNFLKKWRMKRESLMEWLNSLLLLLCLYIYPHSHQVNDFSSLLTMDLGRVDTFNESRFSVVYTPVTNTTQQIMNKVASTPFLAGKEVLGLPDEESIKEFTANYPEEIVRVTFTNTYSYHLKFLLGHGMPAKKEHKDHTAHCYETNEDVYCEVSVFWKEGFVALQAAINAAIIEITTNHSVMEELMSVTGKNMKMHSFIGQSGVITDLYLFSCIISFSSFIYYASVNVTRERKRMKALMTMMGLRDSAFWLSWGLLYAGFIFIMALFLALVIRSTQFIILSGFMVVFSLFLLYGLSLVALAFLMSILVKKSFLTGLVVFLLTVFWGCLGFTSLYRHLPASLEWILSLLSPFAFMLGMAQLLHLDYDLNSNAFPHPSDGSNLIVATNFMLAFDTCLYLALAIYFEKILPNEYGHRRPPLFFLKSSFWSQTQKTDHVALEDEMDADPSFHDSFEQAPPEFQGKEAIRIRNVTKEYKGKPDKIEALKDLVFDIYEGQITAILGHSGAGKSTLLNILSGLSVPTKGSVTIYNNKLSEMADLENLSKLTGVCPQSNVQFDFLTVRENLRLFAKIKGILPQEVDKEIFLLDEPTAGLDPFSRHQVWNLLKERKTDRVILFSTQFMDEADILADRKVFLSQGKLKCAGSSLFLKKKWGIGYHLSLQLNEICVEENITSLVKQHIPDAKLSAKSEGKLIYTLPLERTNKFPELYKDLDSYPDLGIENYGVSMTTLNEVFLKLEGKSTINESDIAILGEVQAEKADDTERLVEMEQVLSSLNKMRKTIGGVALWRQQICAIARVRLLKLKHERKALLALLLILMAGFCPLLVEYTMVKIYQNSYTWELSPHLYFLAPGQQPHDPLTQLLIINKTGASIDDFIQSVEHQNIALEVDAFGTRNGTDDPSYNGAITVCCNEKNYSFSLACNAKRLNCFPVLMDIVSNGLLGMVKPSVHIRTERSTFLENGQDNPIGFLAYIMFWLVLTSSCPPYIAMSSIDDYKNRARSQLRISGLSPSAYWFGQALVDVSLYFLVFVFIYLMSYISNFEDMLLTIIHIIQIPCAVGYSFSLIFMTYVISFIFRKGRKNSGIWSFCFYVVTVFSVAGFAFSIFESDIPFIFTFLIPPATMIGCLFLSSHLLFSSLFSEERMDVQPFLVFLIPFLHFIIFLFTLRCLEWKFGKKSMRKDPFFRISPRSSDVCQNPEEPEGEDEDVQMERVRTANALNSTNFDEKPVIIASCLRKEYAGKRKGCFSKRKNKIATRNVSFCVRKGEVLGLLGHNGAGKSTSIKVITGDTKPTAGQVLLKGSGGGDALEFLGYCPQENALWPNLTVRQHLEVYAAVKGLRKGDAEVAITRLVDALKLQDQLKSPVKTLSEGIKRKLCFVLSILGNPSVVLLDEPSTGMDPEGQQQMWQAIRATFRNTERGALLTTHYMAEAEAVCDRVAIMVSGRLRCIGSIQHLKSKFGKDYLLEMKVKNLAQVEPLHAEILRLFPQAARQERYSSLMVYKLPVEDVQPLAQAFFKLEKVKQSFDLEEYSLSQSTLEQVFLELSKEQELGDFEEDFDPSVKWKLLPQEEP
29	Q9NUT2	>sp|Q9NUT2|ABCB8_HUMAN ATP-binding cassette sub-family B member 8, mitochondrial GN=ABCB8 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MLVHLFRVGIRGGPFPGRLLPPLRFQTFSAVRNTWRNGKTGQLHKAEGEYSDGYRSSSLLRAVAHLRSQLWAHLPRAPLAPRWSPSAWCWVGGALLGPMVLSKHPHLCLVALCEAEEAPPASSTPHVVGSRFNWKLFWQFLHPHLLVLGVAVVLALGAALVNVQIPLLLGQLVEVVAKYTRDHVGSFMTESQNLSTHLLILYGVQGLLTFGYLVLLSHVGERMAVDMRRALFSSLLRQDITFFDANKTGQLVSRLTTDVQEFKSSFKLVISQGLRSCTQVAGCLVSLSMLSTRLTLLLMVATPALMGVGTLMGSGLRKLSRQCQEQIARAMGVADEALGNVRTVRAFAMEQREEERYGAELEACRCRAEELGRGIALFQGLSNIAFNCMVLGTLFIGGSLVAGQQLTGGDLMSFLVASQTVQRSMANLSVLFGQVVRGLSAGARVFEYMALNPCIPLSGGCCVPKEQLRGSVTFQNVCFSYPCRPGFEVLKDFTLTLPPGKIVALVGQSGGGKTTVASLLERFYDPTAGVVMLDGRDLRTLDPSWLRGQVVGFISQEPVLFGTTIMENIRFGKLEASDEEVYTAAREANAHEFITSFPEGYNTVVGERGTTLSGGQKQRLAIARALIKQPTVLILDEATSALDAESERVVQEALDRASAGRTVLVIAHRLSTVRGAHCIVVMADGRVWEAGTHEELLKKGGLYAELIRRQALDAPRTAAPPPKKPEGPRSHQHKS
30	Q9NRK6	>sp|Q9NRK6|ABCBA_HUMAN ATP-binding cassette sub-family B member 10, mitochondrial GN=ABCB10 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MRGPPAWPLRLLEPPSPAEPGRLLPVACVWAAASRVPGSLSPFTGLRPARLWGAGPALLWGVGAARRWRSGCRGGGPGASRGVLGLARLLGLWARGPGSCRCGAFAGPGAPRLPRARFPGGPAAAAWAGDEAWRRGPAAPPGDKGRLRPAAAGLPEARKLLGLAYPERRRLAAAVGFLTMSSVISMSAPFFLGKIIDVIYTNPTVDYSDNLTRLCLGLSAVFLCGAAANAIRVYLMQTSGQRIVNRLRTSLFSSILRQEVAFFDKTRTGELINRLSSDTALLGRSVTENLSDGLRAGAQASVGISMMFFVSPNLATFVLSVVPPVSIIAVIYGRYLRKLTKVTQDSLAQATQLAEERIGNVRTVRAFGKEMTEIEKYASKVDHVMQLARKEAFARAGFFGATGLSGNLIVLSVLYKGGLLMGSAHMTVGELSSFLMYAFWVGISIGGLSSFYSELMKGLGAGGRLWELLEREPKLPFNEGVILNEKSFQGALEFKNVHFAYPARPEVPIFQDFSLSIPSGSVTALVGPSGSGKSTVLSLLLRLYDPASGTISLDGHDIRQLNPVWLRSKIGTVSQEPILFSCSIAENIAYGADDPSSVTAEEIQRVAEVANAVAFIRNFPQGFNTVVGEKGVLLSGGQKQRIAIARALLKNPKILLLDEATSALDAENEYLVQEALDRLMDGRTVLVIAHRLSTIKNANMVAVLDQGKITEYGKHEELLSKPNGIYRKLMNKQSFISA
31	Q9H221	>sp|Q9H221|ABCG8_HUMAN ATP-binding cassette sub-family G member 8 GN=ABCG8 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAGKAAEERGLPKGATPQDTSGLQDRLFSSESDNSLYFTYSGQPNTLEVRDLNYQVDLASQVPWFEQLAQFKMPWTSPSCQNSCELGIQNLSFKVRSGQMLAIIGSSGCGRASLLDVITGRGHGGKIKSGQIWINGQPSSPQLVRKCVAHVRQHNQLLPNLTVRETLAFIAQMRLPRTFSQAQRDKRVEDVIAELRLRQCADTRVGNMYVRGLSGGERRRVSIGVQLLWNPGILILDEPTSGLDSFTAHNLVKTLSRLAKGNRLVLISLHQPRSDIFRLFDLVLLMTSGTPIYLGAAQHMVQYFTAIGYPCPRYSNPADFYVDLTSIDRRSREQELATREKAQSLAALFLEKVRDLDDFLWKAETKDLDEDTCVESSVTPLDTNCLPSPTKMPGAVQQFTTLIRRQISNDFRDLPTLLIHGAEACLMSMTIGFLYFGHGSIQLSFMDTAALLFMIGALIPFNVILDVISKCYSERAMLYYELEDGLYTTGPYFFAKILGELPEHCAYIIIYGMPTYWLANLRPGLQPFLLHFLLVWLVVFCCRIMALAAAALLPTFHMASFFSNALYNSFYLAGGFMINLSSLWTVPAWISKVSFLRWCFEGLMKIQFSRRTYKMPLGNLTIAVSGDKILSVMELDSYPLYAIYLIVIGLSGGFMVLYYVSLRFIKQKPSQDW
32	Q8TB40	>sp|Q8TB40|ABHD4_HUMAN Protein ABHD4 GN=ABHD4 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MADDLEQQSQGWLSSWLPTWRPTSMSQLKNVEARILQCLQNKFLARYVSLPNQNKIWTVTVSPEQNDRTPLVMVHGFGGGVGLWILNMDSLSARRTLHTFDLLGFGRSSRPAFPRDPEGAEDEFVTSIETWRETMGIPSMILLGHSLGGFLATSYSIKYPDRVKHLILVDPWGFPLRPTNPSEIRAPPAWVKAVASVLGRSNPLAVLRVAGPWGPGLVQRFRPDFKRKFADFFEDDTISEYIYHCNAQNPSGETAFKAMMESFGWARRPMLERIHLIRKDVPITMIYGSDTWIDTSTGKKVKMQRPDSYVRDMEIKGASHHVYADQPHIFNAVVEEICDSVD
33	O94929	>sp|O94929|ABLM3_HUMAN Actin-binding LIM protein 3 GN=ABLIM3 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MNTSIPYQQNPYNPRGSSNVIQCYRCGDTCKGEVVRVHNNHFHIRCFTCQVCGCGLAQSGFFFKNQEYICTQDYQQLYGTRCDSCRDFITGEVISALGRTYHPKCFVCSLCRKPFPIGDKVTFSGKECVCQTCSQSMASSKPIKIRGPSHCAGCKEEIKHGQSLLALDKQWHVSCFKCQTCSVILTGEYISKDGVPYCESDYHAQFGIKCETCDRYISGRVLEAGGKHYHPTCARCVRCHQMFTEGEEMYLTGSEVWHPICKQAARAEKKLKHRRTSETSISPPGSSIGSPNRVICAKVDNEILNYKDLAALPKVKSIYEVQRPDLISYEPHSRYMSDEMLERCGYGESLGTLSPYSQDIYENLDLRQRRASSPGYIDSPTYSRQGMSPTFSRSPHHYYRSGPESGRSSPYHSQLDVRSSTPTSYQAPKHFHIPAGDSNIYRKPPIYKRHGDLSTATKSKTSEDISQTSKYSPIYSPDPYYASESEYWTYHGSPKVPRARRFSSGGEEDDFDRSMHKLQSGIGRLILKEEMKARSSSYADPWTPPRSSTSSREALHTAGYEMSLNGSPRSHYLADSDPLISKSASLPAYRRNGLHRTPSADLFHYDSMNAVNWGMREYKIYPYELLLVTTRGRNRLPKDVDRTRLERHLSQEEFYQVFGMTISEFDRLALWKRNELKKQARLF
34	Q8N961	>sp|Q8N961|ABTB2_HUMAN Ankyrin repeat and BTB/POZ domain-containing protein 2 GN=ABTB2 PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAGTYSSTLKTLEDLTLDSGYGAGDSCRSLSLSSSKSNSQALNSSAQQHRGAAWWCYSGSMNSRHNSWDTVNTVLPEDPEVADLFSRCPRLPELEEFPWTEGDVARVLRKGAGGRRLPQFSAEAVRRLAGLLRRALIRVAREAQRLSVLHAKCTRFEVQSAVRLVHSWALAESCALAAVKALSLYSMSAGDGLRRGKSARCGLTFSVGRFFRWMVDTRISVRIHEYAAISLTACMENLVEEIRARVMASHSPDGGGAGGGEVSAEALEMVINNDAELWGVLQPYEHLICGKNANGVLSLPAYFSPYNGGSLGHDERADAYAQLELRTLEQSLLATCVGSISELSDLVSRAMHHMQGRHPLCPGASPARQARQPPQPITWSPDALHTLYYFLRCPQMESMENPNLDPPRMTLNNERPFMLLPPLMEWMRVAITYAEHRRSLTVDSGDIRQAARLLLPGLDCEPRQLKPEHCFSSFRRLDARAATEKFNQDLGFRMLNCGRTDLINQAIEALGPDGVNTMDDQGMTPLMYACAAGDEAMVQMLIDAGANLDIQVPSNSPRHPSIHPDSRHWTSLTFAVLHGHISVVQLLLDAGAHVEGSAVNGGEDSYAETPLQLASAAGNYELVSLLLSRGADPLLSMLEAHGMGSSLHEDMNCFSHSAAHGHRNVLRKLLTQPQQAKADVLSLEEILAEGVEESDASSQGSGSEGPVRLSRTRTKALQEAMYYSAEHGYVDITMELRALGVPWKLHIWIESLRTSFSQSRYSVVQSLLRDFSSIREEEYNEELVTEGLQLMFDILKTSKNDSVIQQLATIFTHCYGSSPIPSIPEIRKTLPARLDPHFLNNKEMSDVTFLVEGKLFYAHKVLLVTASNRFKTLMTNKSEQDGDSSKTIEISDMKYHIFQMMMQYLYYGGTESMEIPTTDILELLSAASLFQLDALQRHCEILCSQTLSMESAVNTYKYAKIHNAPELALFCEGFFLKHMKALLEQDAFRQLIYGRSSKVQGLDPLQDLQNTLAERVHSVYITSRV
35	O00763	>sp|O00763|ACACB_HUMAN Acetyl-CoA carboxylase 2 GN=ACACB PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MVLLLCLSCLIFSCLTFSWLKIWGKMTDSKPITKSKSEANLIPSQEPFPASDNSGETPQRNGEGHTLPKTPSQAEPASHKGPKDAGRRRNSLPPSHQKPPRNPLSSSDAAPSPELQANGTGTQGLEATDTNGLSSSARPQGQQAGSPSKEDKKQANIKRQLMTNFILGSFDDYSSDEDSVAGSSRESTRKGSRASLGALSLEAYLTTGEAETRVPTMRPSMSGLHLVKRGREHKKLDLHRDFTVASPAEFVTRFGGDRVIEKVLIANNGIAAVKCMRSIRRWAYEMFRNERAIRFVVMVTPEDLKANAEYIKMADHYVPVPGGPNNNNYANVELIVDIAKRIPVQAVWAGWGHASENPKLPELLCKNGVAFLGPPSEAMWALGDKIASTVVAQTLQVPTLPWSGSGLTVEWTEDDLQQGKRISVPEDVYDKGCVKDVDEGLEAAERIGFPLMIKASEGGGGKGIRKAESAEDFPILFRQVQSEIPGSPIFLMKLAQHARHLEVQILADQYGNAVSLFGRDCSIQRRHQKIVEEAPATIAPLAIFEFMEQCAIRLAKTVGYVSAGTVEYLYSQDGSFHFLELNPRLQVEHPCTEMIADVNLPAAQLQIAMGVPLHRLKDIRLLYGESPWGVTPISFETPSNPPLARGHVIAARITSENPDEGFKPSSGTVQELNFRSSKNVWGYFSVAATGGLHEFADSQFGHCFSWGENREEAISNMVVALKELSIRGDFRTTVEYLINLLETESFQNNDIDTGWLDYLIAEKVQAEKPDIMLGVVCGALNVADAMFRTCMTDFLHSLERGQVLPADSLLNLVDVELIYGGVKYILKVARQSLTMFVLIMNGCHIEIDAHRLNDGGLLLSYNGNSYTTYMKEEVDSYRITIGNKTCVFEKENDPTVLRSPSAGKLTQYTVEDGGHVEAGSSYAEMEVMKMIMTLNVQERGRVKYIKRPGAVLEAGCVVARLELDDPSKVHPAEPFTGELPAQQTLPILGEKLHQVFHSVLENLTNVMSGFCLPEPVFSIKLKEWVQKLMMTLRHPSLPLLELQEIMTSVAGRIPAPVEKSVRRVMAQYASNITSVLCQFPSQQIATILDCHAATLQRKADREVFFINTQSIVQLVQRYRSGIRGYMKTVVLDLLRRYLRVEHHFQQAHYDKCVINLREQFKPDMSQVLDCIFSHAQVAKKNQLVIMLIDELCGPDPSLSDELISILNELTQLSKSEHCKVALRARQILIASHLPSYELRHNQVESIFLSAIDMYGHQFCPENLKKLILSETTIFDVLPTFFYHANKVVCMASLEVYVRRGYIAYELNSLQHRQLPDGTCVVEFQFMLPSSHPNRMTVPISITNPDLLRHSTELFMDSGFSPLCQRMGAMVAFRRFEDFTRNFDEVISCFANVPKDTPLFSEARTSLYSEDDCKSLREEPIHILNVSIQCADHLEDEALVPILRTFVQSKKNILVDYGLRRITFLIAQEKEFPKFFTFRARDEFAEDRIYRHLEPALAFQLELNRMRNFDLTAVPCANHKMHLYLGAAKVKEGVEVTDHRFFIRAIIRHSDLITKEASFEYLQNEGERLLLEAMDELEVAFNNTSVRTDCNHIFLNFVPTVIMDPFKIEESVRYMVMRYGSRLWKLRVLQAEVKINIRQTTTGSAVPIRLFITNESGYYLDISLYKEVTDSRSGNIMFHSFGNKQGPQHGMLINTPYVTKDLLQAKRFQAQTLGTTYIYDFPEMFRQALFKLWGSPDKYPKDILTYTELVLDSQGQLVEMNRLPGGNEVGMVAFKMRFKTQEYPEGRDVIVIGNDITFRIGSFGPGEDLLYLRASEMARAEGIPKIYVAANSGARIGMAEEIKHMFHVAWVDPEDPHKGFKYLYLTPQDYTRISSLNSVHCKHIEEGGESRYMITDIIGKDDGLGVENLRGSGMIAGESSLAYEEIVTISLVTCRAIGIGAYLVRLGQRVIQVENSHIILTGASALNKVLGREVYTSNNQLGGVQIMHYNGVSHITVPDDFEGVYTILEWLSYMPKDNHSPVPIITPTDPIDREIEFLPSRAPYDPRWMLAGRPHPTLKGTWQSGFFDHGSFKEIMAPWAQTVVTGRARLGGIPVGVIAVETRTVEVAVPADPANLDSEAKIIQQAGQVWFPDSAYKTAQAVKDFNREKLPLMIFANWRGFSGGMKDMYDQVLKFGAYIVDGLRQYKQPILIYIPPYAELRGGSWVVIDATINPLCIEMYADKESRGGVLEPEGTVEIKFRKKDLIKSMRRIDPAYKKLMEQLGEPDLSDKDRKDLEGRLKAREDLLLPIYHQVAVQFADFHDTPGRMLEKGVISDILEWKTARTFLYWRLRRLLLEDQVKQEILQASGELSHVHIQSMLRRWFVETEGAVKAYLWDNNQVVVQWLEQHWQAGDGPRSTIRENITYLKHDSVLKTIRGLVEENPEVAVDCVIYLSQHISPAERAQVVHLLSTMDSPAST
36	Q9H845	>sp|Q9H845|ACAD9_HUMAN Acyl-CoA dehydrogenase family member 9, mitochondrial GN=ACAD9 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MSGCGLFLRTTAAARACRGLVVSTANRRLLRTSPPVRAFAKELFLGKIKKKEVFPFPEVSQDELNEINQFLGPVEKFFTEEVDSRKIDQEGKIPDETLEKLKSLGLFGLQVPEEYGGLGFSNTMYSRLGEIISMDGSITVTLAAHQAIGLKGIILAGTEEQKAKYLPKLASGEHIAAFCLTEPASGSDAASIRSRATLSEDKKHYILNGSKVWITNGGLANIFTVFAKTEVVDSDGSVKDKITAFIVERDFGGVTNGKPEDKLGIRGSNTCEVHFENTKIPVENILGEVGDGFKVAMNILNSGRFSMGSVVAGLLKRLIEMTAEYACTRKQFNKRLSEFGLIQEKFALMAQKAYVMESMTYLTAGMLDQPGFPDCSIEAAMVKVFSSEAAWQCVSEALQILGGLGYTRDYPYERILRDTRILLIFEGTNEILRMYIALTGLQHAGRILTTRIHELKQAKVSTVMDTVGRRLRDSLGRTVDLGLTGNHGVVHPSLADSANKFEENTYCFGRTVETLLLRFGKTIMEEQLVLKRVANILINLYGMTAVLSRASRSIRIGLRNHDHEVLLANTFCVEAYLQNLFSLSQLDKYAPENLDEQIKKVSQQILEKRAYICAHPLDRTC
135	Q9BZC7	>sp|Q9BZC7|ABCA2_HUMAN ATP-binding cassette sub-family A member 2 GN=ABCA2 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MGFLHQLQLLLWKNVTLKRRSPWVLAFEIFIPLVLFFILLGLRQKKPTISVKEAFYTAAPLTSAGILPVMQSLCPDGQRDEFGFLQYANSTVTQLLERLDRVVEEGNLFDPARPSLGSELEALRQHLEALSAGPGTSGSHLDRSTVSSFSLDSVARNPQELWRFLTQNLSLPNSTAQALLAARVDPPEVYHLLFGPSSALDSQSGLHKGQEPWSRLGGNPLFRMEELLLAPALLEQLTCTPGSGELGRILTVPESQKGALQGYRDAVCSGQAAARARRFSGLSAELRNQLDVAKVSQQLGLDAPNGSDSSPQAPPPRRLQALLGDLLDAQKVLQDVDVLSALALLLPQGACTGRTPGPPASGAGGAANGTGAGAVMGPNATAEEGAPSAAALATPDTLQGQCSAFVQLWAGLQPILCGNNRTIEPEALRRGNMSSLGFTSKEQRNLGLLVHLMTSNPKILYAPAGSEVDRVILKANETFAFVGNVTHYAQVWLNISAEIRSFLEQGRLQQHLRWLQQYVAELRLHPEALNLSLDELPPALRQDNFSLPSGMALLQQLDTIDNAACGWIQFMSKVSVDIFKGFHDEESIVNYTLNQAYQDNVTVFASVIFQTRKDGSLPPHVHYKIRQNSSFTEKTNEIRRAYWRPGPNTGGRFYFLYGFVWIQDMMERAIIDTFVGHDVVEPGSYVQMFPYPCYTRDDFLFVIEHMMPLCMVISWVYSVAMTIQHIVAEKEHRLKEVMKTMGLNNAVHWVAWFITGFVQLSISVTALTAILKYGQVLMHSHVVIIWLFLAVYAVATIMFCFLVSVLYSKAKLASACGGIIYFLSYVPYMYVAIREEVAHDKITAFEKCIASLMSTTAFGLGSKYFALYEVAGVGIQWHTFSQSPVEGDDFNLLLAVTMLMVDAVVYGILTWYIEAVHPGMYGLPRPWYFPLQKSYWLGSGRTEAWEWSWPWARTPRLSVMEEDQACAMESRRFEETRGMEEEPTHLPLVVCVDKLTKVYKDDKKLALNKLSLNLYENQVVSFLGHNGAGKTTTMSILTGLFPPTSGSATIYGHDIRTEMDEIRKNLGMCPQHNVLFDRLTVEEHLWFYSRLKSMAQEEIRREMDKMIEDLELSNKRHSLVQTLSGGMKRKLSVAIAFVGGSRAIILDEPTAGVDPYARRAIWDLILKYKPGRTILLSTHHMDEADLLGDRIAIISHGKLKCCGSPLFLKGTYGDGYRLTLVKRPAEPGGPQEPGLASSPPGRAPLSSCSELQVSQFIRKHVASCLLVSDTSTELSYILPSEAAKKGAFERLFQHLERSLDALHLSSFGLMDTTLEEVFLKVSEEDQSLENSEADVKESRKDVLPGAEGPASGEGHAGNLARCSELTQSQASLQSASSVGSARGDEGAGYTDVYGDYRPLFDNPQDPDNVSLQEVEAEALSRVGQGSRKLDGGWLKVRQFHGLLVKRFHCARRNSKALFSQILLPAFFVCVAMTVALSVPEIGDLPPLVLSPSQYHNYTQPRGNFIPYANEERREYRLRLSPDASPQQLVSTFRLPSGVGATCVLKSPANGSLGPTLNLSSGESRLLAARFFDSMCLESFTQGLPLSNFVPPPPSPAPSDSPASPDEDLQAWNVSLPPTAGPEMWTSAPSLPRLVREPVRCTCSAQGTGFSCPSSVGGHPPQMRVVTGDILTDITGHNVSEYLLFTSDRFRLHRYGAITFGNVLKSIPASFGTRAPPMVRKIAVRRAAQVFYNNKGYHSMPTYLNSLNNAILRANLPKSKGNPAAYGITVTNHPMNKTSASLSLDYLLQGTDVVIAIFIIVAMSFVPASFVVFLVAEKSTKAKHLQFVSGCNPIIYWLANYVWDMLNYLVPATCCVIILFVFDLPAYTSPTNFPAVLSLFLLYGWSITPIMYPASFWFEVPSSAYVFLIVINLFIGITATVATFLLQLFEHDKDLKVVNSYLKSCFLIFPNYNLGHGLMEMAYNEYINEYYAKIGQFDKMKSPFEWDIVTRGLVAMAVEGVVGFLLTIMCQYNFLRRPQRMPVSTKPVEDDVDVASERQRVLRGDADNDMVKIENLTKVYKSRKIGRILAVDRLCLGVRPGECFGLLGVNGAGKTSTFKMLTGDESTTGGEAFVNGHSVLKELLQVQQSLGYCPQCDALFDELTAREHLQLYTRLRGISWKDEARVVKWALEKLELTKYADKPAGTYSGGNKRKLSTAIALIGYPAFIFLDEPTTGMDPKARRFLWNLILDLIKTGRSVVLTSHSMEECEALCTRLAIMVNGRLRCLGSIQHLKNRFGDGYMITVRTKSSQSVKDVVRFFNRNFPEAMLKERHHTKVQYQLKSEHISLAQVFSKMEQVSGVLGIEDYSVSQTTLDNVFVNFAKKQSDNLEQQETEPPSALQSPLGCLLSLLRPRSAPTELRALVADEPEDLDTEDEGLISFEEERAQLSFNTDTLC
38	Q96P50	>sp|Q96P50|ACAP3_HUMAN Arf-GAP with coiled-coil, ANK repeat and PH domain-containing protein 3 GN=ACAP3 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MTVEFEECVKDSPRFRATIDEVETDVVEIEAKLDKLVKLCSGMVEAGKAYVSTSRLFVSGVRDLSQQCQGDTVISECLQRFADSLQEVVNYHMILFDQAQRSVRQQLQSFVKEDVRKFKETKKQFDKVREDLELSLVRNAQAPRHRPHEVEEATGALTLTRKCFRHLALDYVLQINVLQAKKKFEILDSMLSFMHAQSSFFQQGYSLLHQLDPYMKKLAAELDQLVIDSAVEKREMERKHAAIQQRTLLQDFSYDESKVEFDVDAPSGVVMEGYLFKRASNAFKTWNRRWFSIQNSQLVYQKKLKDALTVVVDDLRLCSVKPCEDIERRFCFEVLSPTKSCMLQADSEKLRQAWVQAVQASIASAYRESPDSCYSERLDRTASPSTSSIDSATDTRERGVKGESVLQRVQSVAGNSQCGDCGQPDPRWASINLGVLLCIECSGIHRSLGVHCSKVRSLTLDSWEPELLKLMCELGNSAVNQIYEAQCEGAGSRKPTASSSRQDKEAWIKDKYVEKKFLRKAPMAPALEAPRRWRVQKCLRPHSSPRAPTARRKVRLEPVLPCVAALSSVGTLDRKFRRDSLFCPDELDSLFSYFDAGAAGAGPRSLSSDSGLGGSSDGSSDVLAFGSGSVVDSVTEEEGAESEESSGEADGDTEAEAWGLADVRELHPGLLAHRAARARDLPALAAALAHGAEVNWADAEDEGKTPLVQAVLGGSLIVCEFLLQNGADVNQRDSRGRAPLHHATLLGRTGQVCLFLKRGADQHALDQEQRDPLAIAVQAANADIVTLLRLARMAEEMREAEAAPGPPGALAGSPTELQFRRCIQEFISLHLEES
39	O00400	>sp|O00400|ACATN_HUMAN Acetyl-coenzyme A transporter 1 GN=SLC33A1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MSPTISHKDSSRQRRPGNFSHSLDMKSGPLPPGGWDDSHLDSAGREGDREALLGDTGTGDFLKAPQSFRAELSSILLLLFLYVLQGIPLGLAGSIPLILQSKNVSYTDQAFFSFVFWPFSLKLLWAPLVDAVYVKNFGRRKSWLVPTQYILGLFMIYLSTQVDRLLGNTDDRTPDVIALTVAFFLFEFLAATQDIAVDGWALTMLSRENVGYASTCNSVGQTAGYFLGNVLFLALESADFCNKYLRFQPQPRGIVTLSDFLFFWGTVFLITTTLVALLKKENEVSVVKEETQGITDTYKLLFAIIKMPAVLTFCLLILTAKIGFSAADAVTGLKLVEEGVPKEHLALLAVPMVPLQIILPLIISKYTAGPQPLNTFYKAMPYRLLLGLEYALLVWWTPKVEHQGGFPIYYYIVVLLSYALHQVTVYSMYVSIMAFNAKVSDPLIGGTYMTLLNTVSNLGGNWPSTVALWLVDPLTVKECVGASNQNCRTPDAVELCKKLGGSCVTALDGYYVESIICVFIGFGWWFFLGPKFKKLQDEGSSSWKCKRNN
40	Q5T8D3	>sp|Q5T8D3|ACBD5_HUMAN Acyl-CoA-binding domain-containing protein 5 GN=ACBD5 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MFQFHAGSWESWCCCCLIPADRPWDRGQHWQLEMADTRSVHETRFEAAVKVIQSLPKNGSFQPTNEMMLKFYSFYKQATEGPCKLSRPGFWDPIGRYKWDAWSSLGDMTKEEAMIAYVEEMKKIIETMPMTEKVEELLRVIGPFYEIVEDKKSGRSSDITSVRLEKISKCLEDLGNVLTSTPNAKTVNGKAESSDSGAESEEEEAQEEVKGAEQSDNDKKMMKKSADHKNLEVIVTNGYDKDGFVQDIQNDIHASSSLNGRSTEEVKPIDENLGQTGKSAVCIHQDINDDHVEDVTGIQHLTSDSDSEVYCDSMEQFGQEESLDSFTSNNGPFQYYLGGHSSQPMENSGFREDIQVPPGNGNIGNMQVVAVEGKGEVKHGGEDGRNNSGAPHREKRGGETDEFSNVRRGRGHRMQHLSEGTKGRQVGSGGDGERWGSDRGSRGSLNEQIALVLMRLQEDMQNVLQRLQKLETLTALQAKSSTSTLQTAPQPTSQRPSWWPFEMSPGVLTFAIIWPFIAQWLVYLYYQRRRRKLN
41	Q9BR61	>sp|Q9BR61|ACBD6_HUMAN Acyl-CoA-binding domain-containing protein 6 GN=ACBD6 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MASSFLPAGAITGDSGGELSSGDDSGEVEFPHSPEIEETSCLAELFEKAAAHLQGLIQVASREQLLYLYARYKQVKVGNCNTPKPSFFDFEGKQKWEAWKALGDSSPSQAMQEYIAVVKKLDPGWNPQIPEKKGKEANTGFGGPVISSLYHEETIREEDKNIFDYCRENNIDHITKAIKSKNVDVNVKDEEGRALLHWACDRGHKELVTVLLQHRADINCQDNEGQTALHYASACEFLDIVELLLQSGADPTLRDQDGCLPEEVTGCKTVSLVLQRHTTGKA
42	Q5FVE4	>sp|Q5FVE4|ACBG2_HUMAN Long-chain-fatty-acid--CoA ligase ACSBG2 GN=ACSBG2 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MTGTPKTQEGAKDLEVDMNKTEVTPRLWTTCRDGEVLLRLSKHGPGHETPMTIPEFFRESVNRFGTYPALASKNGKKWEILNFNQYYEACRKAAKSLIKLGLERFHGVGILGFNSAEWFITAVGAILAGGLCVGIYATNSAEVCQYVITHAKVNILLVENDQQLQKILSIPQSSLEPLKAIIQYRLPMKKNNNLYSWDDFMELGRSIPDTQLEQVIESQKANQCAVLIYTSGTTGIPKGVMLSHDNITWIAGAVTKDFKLTDKHETVVSYLPLSHIAAQMMDIWVPIKIGALTYFAQADALKGTLVSTLKEVKPTVFIGVPQIWEKIHEMVKKNSAKSMGLKKKAFVWARNIGFKVNSKKMLGKYNTPVSYRMAKTLVFSKVKTSLGLDHCHSFISGTAPLNQETAEFFLSLDIPIGELYGLSESSGPHTISNQNNYRLLSCGKILTGCKNMLFQQNKDGIGEICLWGRHIFMGYLESETETTEAIDDEGWLHSGDLGQLDGLGFLYVTGHIKEILITAGGENVPPIPVETLVKKKIPIISNAMLVGDKLKFLSMLLTLKCEMNQMSGEPLDKLNFEAINFCRGLGSQASTVTEIVKQQDPLVYKAIQQGINAVNQEAMNNAQRIEKWVILEKDFSIYGGELGPMMKLKRHFVAQKYKKQIDHMYH
43	P30443	>sp|P30443|1A01_HUMAN HLA class I histocompatibility antigen, A-1 alpha chain GN=HLA-A PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMAPRTLLLLLSGALALTQTWAGSHSMRYFFTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQKMEPRAPWIEQEGPEYWDQETRNMKAHSQTDRANLGTLRGYYNQSEDGSHTIQIMYGCDVGPDGRFLRGYRQDAYDGKDYIALNEDLRSWTAADMAAQITKRKWEAVHAAEQRRVYLEGRCVDGLRRYLENGKETLQRTDPPKTHMTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWELSSQPTIPIVGIIAGLVLLGAVITGAVVAAVMWRRKSSDRKGGSYTQAASSDSAQGSDVSLTACKV
44	P01892	>sp|P01892|1A02_HUMAN HLA class I histocompatibility antigen, A-2 alpha chain GN=HLA-A PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMAPRTLVLLLSGALALTQTWAGSHSMRYFFTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDGETRKVKAHSQTHRVDLGTLRGYYNQSEAGSHTVQRMYGCDVGSDWRFLRGYHQYAYDGKDYIALKEDLRSWTAADMAAQTTKHKWEAAHVAEQLRAYLEGTCVEWLRRYLENGKETLQRTDAPKTHMTHHAVSDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGQEQRYTCHVQHEGLPKPLTLRWEPSSQPTIPIVGIIAGLVLFGAVITGAVVAAVMWRRKSSDRKGGSYSQAASSDSAQGSDVSLTACKV
45	P13746	>sp|P13746|1A11_HUMAN HLA class I histocompatibility antigen, A-11 alpha chain GN=HLA-A PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMAPRTLLLLLSGALALTQTWAGSHSMRYFYTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDQETRNVKAQSQTDRVDLGTLRGYYNQSEDGSHTIQIMYGCDVGPDGRFLRGYRQDAYDGKDYIALNEDLRSWTAADMAAQITKRKWEAAHAAEQQRAYLEGRCVEWLRRYLENGKETLQRTDPPKTHMTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWELSSQPTIPIVGIIAGLVLLGAVITGAVVAAVMWRRKSSDRKGGSYTQAASSDSAQGSDVSLTACKV
46	Q96QU6	>sp|Q96QU6|1A1L1_HUMAN 1-aminocyclopropane-1-carboxylate synthase-like protein 1 GN=ACCS PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MFTLPQKDFRAPTTCLGPTCMQDLGSSHGEDLEGECSRKLDQKLPELRGVGDPAMISSDTSYLSSRGRMIKWFWDSAEEGYRTYHMDEYDEDKNPSGIINLGTSENKLCFDLLSWRLSQRDMQRVEPSLLQYADWRGHLFLREEVAKFLSFYCKSPVPLRPENVVVLNGGASLFSALATVLCEAGEAFLIPTPYYGAITQHVCLYGNIRLAYVYLDSEVTGLDTRPFQLTVEKLEMALREAHSEGVKVKGLILISPQNPLGDVYSPEELQEYLVFAKRHRLHVIVDEVYMLSVFEKSVGYRSVLSLERLPDPQRTHVMWATSKDFGMSGLRFGTLYTENQDVATAVASLCRYHGLSGLVQYQMAQLLRDRDWINQVYLPENHARLKAAHTYVSEELRALGIPFLSRGAGFFIWVDLRKYLPKGTFEEEMLLWRRFLDNKVLLSFGKAFECKEPGWFRFVFSDQVHRLCLGMQRVQQVLAGKSQVAEDPRPSQSQEPSDQRR
47	P30447	>sp|P30447|1A23_HUMAN HLA class I histocompatibility antigen, A-23 alpha chain GN=HLA-A PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMAPRTLVLLLSGALALTQTWAGSHSMRYFSTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDEETGKVKAHSQTDRENLRIALRYYNQSEAGSHTLQMMFGCDVGSDGRFLRGYHQYAYDGKDYIALKEDLRSWTAADMAAQITQRKWEAARVAEQLRAYLEGTCVDGLRRYLENGKETLQRTDPPKTHMTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQPTVHIVGIIAGLVLLGAVITGAVVAAVMWRRNSSDRKGGSYSQAASSDSAQGSDVSLTACKV
48	P18462	>sp|P18462|1A25_HUMAN HLA class I histocompatibility antigen, A-25 alpha chain GN=HLA-A PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMAPRTLVLLLSGALALTQTWAGSHSMRYFYTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDRNTRNVKAHSQTDRESLRIALRYYNQSEDGSHTIQRMYGCDVGPDGRFLRGYQQDAYDGKDYIALNEDLRSWTAADMAAQITQRKWETAHEAEQWRAYLEGRCVEWLRRYLENGKETLQRTDAPKTHMTHHAVSDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWASVVVPSGQEQRYTCHVQHEGLPKPLTLRWEPSSQPTIPIVGIIAGLVLFGAVIAGAVVAAVMWRRKSSDRKGGSYSQAASSDSAQGSDMSLTACKV
49	P16190	>sp|P16190|1A33_HUMAN HLA class I histocompatibility antigen, A-33 alpha chain GN=HLA-A PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMAPRTLLLLLLGALALTQTWAGSHSMRYFTTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDRNTRNVKAHSQIDRVDLGTLRGYYNQSEAGSHTIQMMYGCDVGSDGRFLRGYQQDAYDGKDYIALNEDLRSWTAADMAAQITQRKWEAARVAEQLRAYLEGTCVEWLRRHLENGKETLQRTDPPKTHMTHHAVSDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWASVVVPSGQEQRYTCHVQHEGLPKPLTLRWEPSSQPTIPIVGIIAGLVLFGAVFAGAVVAAVRWRRKSSDRKGGSYSQAASSDSAQGSDMSLTACKV
79	P36639	>sp|P36639|8ODP_HUMAN 7,8-dihydro-8-oxoguanine triphosphatase GN=NUDT1 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MYWSNQITRRLGERVQGFMSGISPQQMGEPEGSWSGKNPGTMGASRLYTLVLVLQPQRVLLGMKKRGFGAGRWNGFGGKVQEGETIEDGARRELQEESGLTVDALHKVGQIVFEFVGEPELMDVHVFCTDSIQGTPVESDEMRPCWFQLDQIPFKDMWPDDSYWFPLLLQKKKFHGYFKFQGQDTILDYTLREVDTV
50	P30455	>sp|P30455|1A36_HUMAN HLA class I histocompatibility antigen, A-36 alpha chain GN=HLA-A PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMAPRTLLLLLSGALALTQTWAGSHSMRYFFTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQKMEPRAPWIEQEGPEYWDQETRNMKAHSQTDRANLGTLRGYYNQSEDGSHTIQIMYGCDVGPDGRFLRGYRQDAYDGKDYIALNEDLRSWTAADMAAQITKRKWEAVHAAEQRRVYLEGTCVEWLRRYLENGKETLQRTDPPKTHMTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWELSSQPTIPIVGIIAGLVLLGAVITGAVVAAVMWRRKSSDRKGGSYTQAASSDSAQGSDVSLTACKV
51	P30457	>sp|P30457|1A66_HUMAN HLA class I histocompatibility antigen, A-66 alpha chain GN=HLA-A PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMAPRTLVLLLSGALALTQTWAGSHSMRYFYTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDRNTRNVKAQSQTDRVDLGTLRGYYNQSEDGSHTIQRMYGCDVGPDGRFLRGYQQDAYDGKDYIALNEDLRSWTAADMAAQITQRKWETAHEAEQWRAYLEGRCVEWLRRYLENGKETLQRTDAPKTHMTHHAVSDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWASVVVPSGQEQRYTCHVQHEGLPKPLTLRWEPSSQPTIPIVGIIAGLVLFGAVIAGAVVAAVMWRRKSSDRKGGSYSQAASSDSAQGSDMSLTACKV
52	P01891	>sp|P01891|1A68_HUMAN HLA class I histocompatibility antigen, A-68 alpha chain GN=HLA-A PE=1 SV=4 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMAPRTLVLLLSGALALTQTWAGSHSMRYFYTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDRNTRNVKAQSQTDRVDLGTLRGYYNQSEAGSHTIQMMYGCDVGSDGRFLRGYRQDAYDGKDYIALKEDLRSWTAADMAAQTTKHKWEAAHVAEQWRAYLEGTCVEWLRRYLENGKETLQRTDAPKTHMTHHAVSDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWVAVVVPSGQEQRYTCHVQHEGLPKPLTLRWEPSSQPTIPIVGIIAGLVLFGAVITGAVVAAVMWRRKSSDRKGGSYSQAASSDSAQGSDVSLTACKV
53	P30460	>sp|P30460|1B08_HUMAN HLA class I histocompatibility antigen, B-8 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLVMAPRTVLLLLSAALALTETWAGSHSMRYFDTAMSRPGRGEPRFISVGYVDDTQFVRFDSDAASPREEPRAPWIEQEGPEYWDRNTQIFKTNTQTDRESLRNLRGYYNQSEAGSHTLQSMYGCDVGPDGRLLRGHNQYAYDGKDYIALNEDLRSWTAADTAAQITQRKWEAARVAEQDRAYLEGTCVEWLRRYLENGKDTLERADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCRRKSSGGKGGSYSQAACSDSAQGSDVSLTA
54	P30480	>sp|P30480|1B42_HUMAN HLA class I histocompatibility antigen, B-42 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLVMAPRTVLLLLSAALALTETWAGSHSMRYFYTSVSRPGRGEPRFISVGYVDDTQFVRFDSDAASPREEPRAPWIEQEGPEYWDRNTQIYKAQAQTDRESLRNLRGYYNQSEAGSHTLQSMYGCDVGPDGRLLRGHNQYAYDGKDYIALNEDLRSWTAADTAAQITQRKWEAARVAEQDRAYLEGTCVEWLRRYLENGKDTLERADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCRRKSSGGKGGSYSQAACSDSAQGSDVSLTA
55	P30483	>sp|P30483|1B45_HUMAN HLA class I histocompatibility antigen, B-45 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTVLLLLSAALALTETWAGSHSMRYFHTAMSRPGRGEPRFITVGYVDDTLFVRFDSDATSPRKEPRAPWIEQEGPEYWDRETQISKTNTQTYRESLRNLRGYYNQSEAGSHTWQRMYGCDLGPDGRLLRGYNQLAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAARVAEQDRAYLEGLCVESLRRYLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
56	Q29940	>sp|Q29940|1B59_HUMAN HLA class I histocompatibility antigen, B-59 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTLLLLLWGALALTETWAGSHSMRYFYTAMSRPGRGEPRFIAVGYVDDTQFVRFDSDAASPREEPRAPWIEQEGPEYWDRNTQIFKTNTQTYRENLRIALRYYNQSEAGSHTWQTMYGCDLGPDGRLLRGHNQLAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAARVAEQLRAYLEGTCVEWLRRYLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
57	P30498	>sp|P30498|1B78_HUMAN HLA class I histocompatibility antigen, B-78 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTVLLLLWGAVALTETWAGSHSMRYFYTAMSRPGRGEPRFIAVGYVDDTQFVRFDSDAASPRTEPRAPWIEQEGPEYWDRNTQIFKTNTQTDRESLRNLRGYYNQSEAGSHTWQTMYGCDVGPDGRLLRGHNQYAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAAREAEQLRAYLEGLCVEWLRRHLENGKETLQRADPPKTHVTHHPVSDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
58	Q9TNN7	>sp|Q9TNN7|1C05_HUMAN HLA class I histocompatibility antigen, Cw-5 alpha chain GN=HLA-C PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVMAPRTLILLLSGALALTETWACSHSMRYFYTAVSRPGRGEPRFIAVGYVDDTQFVQFDSDAASPRGEPRAPWVEQEGPEYWDRETQKYKRQAQTDRVNLRKLRGYYNQSEAGSHTLQRMYGCDLGPDGRLLRGYNQFAYDGKDYIALNEDLRSWTAADKAAQITQRKWEAAREAEQRRAYLEGTCVEWLRRYLENGKKTLQRAEHPKTHVTHHPVSDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPEPLTLRWGPSSQPTIPIVGIVAGLAVLAVLAVLGAVMAVVMCRRKSSGGKGGSCSQAASSNSAQGSDESLIACKA
59	Q29963	>sp|Q29963|1C06_HUMAN HLA class I histocompatibility antigen, Cw-6 alpha chain GN=HLA-C PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MRVMAPRTLILLLSGALALTETWACSHSMRYFDTAVSRPGRGEPRFISVGYVDDTQFVRFDSDAASPRGEPRAPWVEQEGPEYWDRETQKYKRQAQADRVNLRKLRGYYNQSEDGSHTLQWMYGCDLGPDGRLLRGYDQSAYDGKDYIALNEDLRSWTAADTAAQITQRKWEAAREAEQWRAYLEGTCVEWLRRYLENGKETLQRAEHPKTHVTHHPVSDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPEPLTLRWEPSSQPTIPIVGIVAGLAVLAVLAVLGAVMAVVMCRRKSSGGKGGSCSQAASSNSAQGSDESLIACKA
60	P30505	>sp|P30505|1C08_HUMAN HLA class I histocompatibility antigen, Cw-8 alpha chain GN=HLA-C PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVMAPRTLILLLSGALALTETWACSHSMRYFYTAVSRPGRGEPRFIAVGYVDDTQFVQFDSDAASPRGEPRAPWVEQEGPEYWDRETQKYKRQAQTDRVSLRNLRGYYNQSEAGSHTLQRMYGCDLGPDGRLLRGYNQFAYDGKDYIALNEDLRSWTAADTAAQITQRKWEAARTAEQLRAYLEGTCVEWLRRYLENGKKTLQRAEHPKTHVTHHPVSDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPEPLTLRWGPSSQPTIPIVGIVAGLAVLAVLAVLGAVMAVVMCRRKSSGGKGGSCSQAASSNSAQGSDESLIACKA
61	P30510	>sp|P30510|1C14_HUMAN HLA class I histocompatibility antigen, Cw-14 alpha chain GN=HLA-C PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MRVMAPRTLILLLSGALALTETWACSHSMRYFSTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASPRGEPRAPWVEQEGPEYWDRETQKYKRQAQTDRVSLRNLRGYYNQSEAGSHTLQWMFGCDLGPDGRLLRGYDQSAYDGKDYIALNEDLRSWTAADTAAQITQRKWEAAREAEQRRAYLEGTCVEWLRRYLENGKETLQRAEHPKTHVTHHPVSDHEATLRCWALGFYPAEITLTWQWDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPEPLTLRWEPSSQPTIPIVGIVAGLAVLAVLAVLGAVVAVVMCRRKSSGGKGGSCSQAASSNSAQGSDESLIACKA
62	Q95604	>sp|Q95604|1C17_HUMAN HLA class I histocompatibility antigen, Cw-17 alpha chain GN=HLA-C PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVMAPQALLLLLSGALALIETWAGSHSMRYFYTAVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASPRGEPRAPWVEQEGPEYWDRETQKYKRQAQADRVNLRKLRGYYNQSEAGSHTIQRMYGCDLGPDGRLLRGYNQFAYDGKDYIALNEDLRSWTAADTAAQISQRKLEAAREAEQLRAYLEGECVEWLRGYLENGKETLQRAERPKTHVTHHPVSDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGQEQRYTCHVQHEGLQEPCTLRWKPSSQPTIPNLGIVSGPAVLAVLAVLAVLAVLGAVVAAVIHRRKSSGGKGGSCSQAASSNSAQGSDESLIACKA
63	Q16537	>sp|Q16537|2A5E_HUMAN Serine/threonine-protein phosphatase 2A 56 kDa regulatory subunit epsilon isoform GN=PPP2R5E PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MSSAPTTPPSVDKVDGFSRKSVRKARQKRSQSSSQFRSQGKPIELTPLPLLKDVPSSEQPELFLKKLQQCCVIFDFMDTLSDLKMKEYKRSTLNELVDYITISRGCLTEQTYPEVVRMVSCNIFRTLPPSDSNEFDPEEDEPTLEASWPHLQLVYEFFIRFLESQEFQPSIAKKYIDQKFVLQLLELFDSEDPRERDYLKTVLHRIYGKFLGLRAFIRKQINNIFLRFVYETEHFNGVAELLEILGSIINGFALPLKAEHKQFLVKVLIPLHTVRSLSLFHAQLAYCIVQFLEKDPSLTEPVIRGLMKFWPKTCSQKEVMFLGELEEILDVIEPSQFVKIQEPLFKQIAKCVSSPHFQVAERALYYWNNEYIMSLIEENSNVILPIMFSSLYRISKEHWNPAIVALVYNVLKAFMEMNSTMFDELTATYKSDRQREKKKEKEREELWKKLEDLELKRGLRRDGIIPT
136	P78363	>sp|P78363|ABCA4_HUMAN Retinal-specific ATP-binding cassette transporter GN=ABCA4 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MGFVRQIQLLLWKNWTLRKRQKIRFVVELVWPLSLFLVLIWLRNANPLYSHHECHFPNKAMPSAGMLPWLQGIFCNVNNPCFQSPTPGESPGIVSNYNNSILARVYRDFQELLMNAPESQHLGRIWTELHILSQFMDTLRTHPERIAGRGIRIRDILKDEETLTLFLIKNIGLSDSVVYLLINSQVRPEQFAHGVPDLALKDIACSEALLERFIIFSQRRGAKTVRYALCSLSQGTLQWIEDTLYANVDFFKLFRVLPTLLDSRSQGINLRSWGGILSDMSPRIQEFIHRPSMQDLLWVTRPLMQNGGPETFTKLMGILSDLLCGYPEGGGSRVLSFNWYEDNNYKAFLGIDSTRKDPIYSYDRRTTSFCNALIQSLESNPLTKIAWRAAKPLLMGKILYTPDSPAARRILKNANSTFEELEHVRKLVKAWEEVGPQIWYFFDNSTQMNMIRDTLGNPTVKDFLNRQLGEEGITAEAILNFLYKGPRESQADDMANFDWRDIFNITDRTLRLVNQYLECLVLDKFESYNDETQLTQRALSLLEENMFWAGVVFPDMYPWTSSLPPHVKYKIRMDIDVVEKTNKIKDRYWDSGPRADPVEDFRYIWGGFAYLQDMVEQGITRSQVQAEAPVGIYLQQMPYPCFVDDSFMIILNRCFPIFMVLAWIYSVSMTVKSIVLEKELRLKETLKNQGVSNAVIWCTWFLDSFSIMSMSIFLLTIFIMHGRILHYSDPFILFLFLLAFSTATIMLCFLLSTFFSKASLAAACSGVIYFTLYLPHILCFAWQDRMTAELKKAVSLLSPVAFGFGTEYLVRFEEQGLGLQWSNIGNSPTEGDEFSFLLSMQMMLLDAAVYGLLAWYLDQVFPGDYGTPLPWYFLLQESYWLGGEGCSTREERALEKTEPLTEETEDPEHPEGIHDSFFEREHPGWVPGVCVKNLVKIFEPCGRPAVDRLNITFYENQITAFLGHNGAGKTTTLSILTGLLPPTSGTVLVGGRDIETSLDAVRQSLGMCPQHNILFHHLTVAEHMLFYAQLKGKSQEEAQLEMEAMLEDTGLHHKRNEEAQDLSGGMQRKLSVAIAFVGDAKVVILDEPTSGVDPYSRRSIWDLLLKYRSGRTIIMSTHHMDEADLLGDRIAIIAQGRLYCSGTPLFLKNCFGTGLYLTLVRKMKNIQSQRKGSEGTCSCSSKGFSTTCPAHVDDLTPEQVLDGDVNELMDVVLHHVPEAKLVECIGQELIFLLPNKNFKHRAYASLFRELEETLADLGLSSFGISDTPLEEIFLKVTEDSDSGPLFAGGAQQKRENVNPRHPCLGPREKAGQTPQDSNVCSPGAPAAHPEGQPPPEPECPGPQLNTGTQLVLQHVQALLVKRFQHTIRSHKDFLAQIVLPATFVFLALMLSIVIPPFGEYPALTLHPWIYGQQYTFFSMDEPGSEQFTVLADVLLNKPGFGNRCLKEGWLPEYPCGNSTPWKTPSVSPNITQLFQKQKWTQVNPSPSCRCSTREKLTMLPECPEGAGGLPPPQRTQRSTEILQDLTDRNISDFLVKTYPALIRSSLKSKFWVNEQRYGGISIGGKLPVVPITGEALVGFLSDLGRIMNVSGGPITREASKEIPDFLKHLETEDNIKVWFNNKGWHALVSFLNVAHNAILRASLPKDRSPEEYGITVISQPLNLTKEQLSEITVLTTSVDAVVAICVIFSMSFVPASFVLYLIQERVNKSKHLQFISGVSPTTYWVTNFLWDIMNYSVSAGLVVGIFIGFQKKAYTSPENLPALVALLLLYGWAVIPMMYPASFLFDVPSTAYVALSCANLFIGINSSAITFILELFENNRTLLRFNAVLRKLLIVFPHFCLGRGLIDLALSQAVTDVYARFGEEHSANPFHWDLIGKNLFAMVVEGVVYFLLTLLVQRHFFLSQWIAEPTKEPIVDEDDDVAEERQRIITGGNKTDILRLHELTKIYPGTSSPAVDRLCVGVRPGECFGLLGVNGAGKTTTFKMLTGDTTVTSGDATVAGKSILTNISEVHQNMGYCPQFDAIDELLTGREHLYLYARLRGVPAEEIEKVANWSIKSLGLTVYADCLAGTYSGGNKRKLSTAIALIGCPPLVLLDEPTTGMDPQARRMLWNVIVSIIREGRAVVLTSHSMEECEALCTRLAIMVKGAFRCMGTIQHLKSKFGDGYIVTMKIKSPKDDLLPDLNPVEQFFQGNFPGSVQRERHYNMLQFQVSSSSLARIFQLLLSHKDSLLIEEYSVTQTTLDQVFVNFAKQQTESHDLPLHPRAAGASRQAQD
64	Q66LE6	>sp|Q66LE6|2ABD_HUMAN Serine/threonine-protein phosphatase 2A 55 kDa regulatory subunit B delta isoform GN=PPP2R2D PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAGAGGGGCPAGGNDFQWCFSQVKGAIDEDVAEADIISTVEFNYSGDLLATGDKGGRVVIFQREQENKSRPHSRGEYNVYSTFQSHEPEFDYLKSLEIEEKINKIRWLPQQNAAHFLLSTNDKTIKLWKISERDKRAEGYNLKDEDGRLRDPFRITALRVPILKPMDLMVEASPRRIFANAHTYHINSISVNSDHETYLSADDLRINLWHLEITDRSFNIVDIKPANMEELTEVITAAEFHPHQCNVFVYSSSKGTIRLCDMRSSALCDRHSKFFEEPEDPSSRSFFSEIISSISDVKFSHSGRYMMTRDYLSVKVWDLNMESRPVETHQVHEYLRSKLCSLYENDCIFDKFECCWNGSDSAIMTGSYNNFFRMFDRDTRRDVTLEASRESSKPRASLKPRKVCTGGKRRKDEISVDSLDFNKKILHTAWHPVDNVIAVAATNNLYIFQDKIN
65	Q9Y2T4	>sp|Q9Y2T4|2ABG_HUMAN Serine/threonine-protein phosphatase 2A 55 kDa regulatory subunit B gamma isoform GN=PPP2R2C PE=1 SV=4 Homo sapiens OS=Human NCBI_TaxID=9606	MGEDTDTRKINHSFLRDHSYVTEADIISTVEFNHTGELLATGDKGGRVVIFQREPESKNAPHSQGEYDVYSTFQSHEPEFDYLKSLEIEEKINKIKWLPQQNAAHSLLSTNDKTIKLWKITERDKRPEGYNLKDEEGKLKDLSTVTSLQVPVLKPMDLMVEVSPRRIFANGHTYHINSISVNSDCETYMSADDLRINLWHLAITDRSFNIVDIKPANMEDLTEVITASEFHPHHCNLFVYSSSKGSLRLCDMRAAALCDKHSKLFEEPEDPSNRSFFSEIISSVSDVKFSHSGRYMLTRDYLTVKVWDLNMEARPIETYQVHDYLRSKLCSLYENDCIFDKFECAWNGSDSVIMTGAYNNFFRMFDRNTKRDVTLEASRESSKPRAVLKPRRVCVGGKRRRDDISVDSLDFTKKILHTAWHPAENIIAIAATNNLYIFQDKVNSDMH
66	P13760	>sp|P13760|2B14_HUMAN HLA class II histocompatibility antigen, DRB1-4 beta chain GN=HLA-DRB1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MVCLKFPGGSCMAALTVTLMVLSSPLALAGDTRPRFLEQVKHECHFFNGTERVRFLDRYFYHQEEYVRFDSDVGEYRAVTELGRPDAEYWNSQKDLLEQKRAAVDTYCRHNYGVGESFTVQRRVYPEVTVYPAKTQPLQHHNLLVCSVNGFYPGSIEVRWFRNGQEEKTGVVSTGLIQNGDWTFQTLVMLETVPRSGEVYTCQVEHPSLTSPLTVEWRARSESAQSKMLSGVGGFVLGLLFLGAGLFIYFRNQKGHSGLQPTGFLS
67	P20039	>sp|P20039|2B1B_HUMAN HLA class II histocompatibility antigen, DRB1-11 beta chain GN=HLA-DRB1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MVCLRLPGGSCMAVLTVTLMVLSSPLALAGDTRPRFLEYSTSECHFFNGTERVRFLDRYFYNQEEYVRFDSDVGEFRAVTELGRPDEEYWNSQKDFLEDRRAAVDTYCRHNYGVGESFTVQRRVHPKVTVYPSKTQPLQHHNLLVCSVSGFYPGSIEVRWFRNGQEEKTGVVSTGLIHNGDWTFQTLVMLETVPRSGEVYTCQVEHPSVTSPLTVEWRARSESAQSKMLSGVGGFVLGLLFLGAGLFIYFRNQKGHSGLQPRGFLS
68	P01911	>sp|P01911|2B1F_HUMAN HLA class II histocompatibility antigen, DRB1-15 beta chain GN=HLA-DRB1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MVCLKLPGGSCMTALTVTLMVLSSPLALSGDTRPRFLWQPKRECHFFNGTERVRFLDRYFYNQEESVRFDSDVGEFRAVTELGRPDAEYWNSQKDILEQARAAVDTYCRHNYGVVESFTVQRRVQPKVTVYPSKTQPLQHHNLLVCSVSGFYPGSIEVRWFLNGQEEKAGMVSTGLIQNGDWTFQTLVMLETVPRSGEVYTCQVEHPSVTSPLTVEWRARSESAQSKMLSGVGGFVLGLLFLGAGLFIYFRNQKGHSGLQPTGFLS
69	Q7L8J4	>sp|Q7L8J4|3BP5L_HUMAN SH3 domain-binding protein 5-like GN=SH3BP5L PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAELRQVPGGRETPQGELRPEVVEDEVPRSPVAEEPGGGGSSSSEAKLSPREEEELDPRIQEELEHLNQASEEINQVELQLDEARTTYRRILQESARKLNTQGSHLGSCIEKARPYYEARRLAKEAQQETQKAALRYERAVSMHNAAREMVFVAEQGVMADKNRLDPTWQEMLNHATCKVNEAEEERLRGEREHQRVTRLCQQAEARVQALQKTLRRAIGKSRPYFELKAQFSQILEEHKAKVTELEQQVAQAKTRYSVALRNLEQISEQIHARRRGGLPPHPLGPRRSSPVGAEAGPEDMEDGDSGIEGAEGAGLEEGSSLGPGPAPDTDTLSLLSLRTVASDLQKCDSVEHLRGLSDHVSLDGQELGTRSGGRRGSDGGARGGRHQRSVSL
70	O60239	>sp|O60239|3BP5_HUMAN SH3 domain-binding protein 5 GN=SH3BP5 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MDAALKRSRSEEPAEILPPARDEEEEEEEGMEQGLEEEEEVDPRIQGELEKLNQSTDDINRRETELEDARQKFRSVLVEATVKLDELVKKIGKAVEDSKPYWEARRVARQAQLEAQKATQDFQRATEVLRAAKETISLAEQRLLEDDKRQFDSAWQEMLNHATQRVMEAEQTKTRSELVHKETAARYNAAMGRMRQLEKKLKRAINKSKPYFELKAKYYVQLEQLKKTVDDLQAKLTLAKGEYKMALKNLEMISDEIHERRRSSAMGPRGCGVGAEGSSTSVEDLPGSKPEPDAISVASEAFEDDSCSNFVSEDDSETQSVSSFSSGPTSPSEMPDQFPAVVRPGSLDLPSPVSLSEFGMMFPVLGPRSECSGASSPECEVERGDRAEGAENKTSDKANNNRGLSSSSGSGGSSKSQSSTSPEGQALENRMKQLSLQCSKGRDGIIADIKMVQIG
71	Q13541	>sp|Q13541|4EBP1_HUMAN Eukaryotic translation initiation factor 4E-binding protein 1 GN=EIF4EBP1 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MSGGSSCSQTPSRAIPATRRVVLGDGVQLPPGDYSTTPGGTLFSTTPGGTRIIYDRKFLMECRNSPVTKTPPRDLPTIPGVTSPSSDEPPMEASQSHLRNSPEDKRAGGEESQFEMDI
72	O60516	>sp|O60516|4EBP3_HUMAN Eukaryotic translation initiation factor 4E-binding protein 3 GN=EIF4EBP3 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MSTSTSCPIPGGRDQLPDCYSTTPGGTLYATTPGGTRIIYDRKFLLECKNSPIARTPPCCLPQIPGVTTPPTAPLSKLEELKEQETEEEIPDDAQFEMDI
73	P28222	>sp|P28222|5HT1B_HUMAN 5-hydroxytryptamine receptor 1B GN=HTR1B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MEEPGAQCAPPPPAGSETWVPQANLSSAPSQNCSAKDYIYQDSISLPWKVLLVMLLALITLATTLSNAFVIATVYRTRKLHTPANYLIASLAVTDLLVSILVMPISTMYTVTGRWTLGQVVCDFWLSSDITCCTASILHLCVIALDRYWAITDAVEYSAKRTPKRAAVMIALVWVFSISISLPPFFWRQAKAEEEVSECVVNTDHILYTVYSTVGAFYFPTLLLIALYGRIYVEARSRILKQTPNRTGKRLTRAQLITDSPGSTSSVTSINSRVPDVPSESGSPVYVNQVKVRVSDALLEKKKLMAARERKATKTLGIILGAFIVCWLPFFIISLVMPICKDACWFHLAIFDFFTWLGYLNSLINPIIYTMSNEDFKQAFHKLIRFKCTS
74	P28221	>sp|P28221|5HT1D_HUMAN 5-hydroxytryptamine receptor 1D GN=HTR1D PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MSPLNQSAEGLPQEASNRSLNATETSEAWDPRTLQALKISLAVVLSVITLATVLSNAFVLTTILLTRKLHTPANYLIGSLATTDLLVSILVMPISIAYTITHTWNFGQILCDIWLSSDITCCTASILHLCVIALDRYWAITDALEYSKRRTAGHAATMIAIVWAISICISIPPLFWRQAKAQEEMSDCLVNTSQISYTIYSTCGAFYIPSVLLIILYGRIYRAARNRILNPPSLYGKRFTTAHLITGSAGSSLCSLNSSLHEGHSHSAGSPLFFNHVKIKLADSALERKRISAARERKATKILGIILGAFIICWLPFFVVSLVLPICRDSCWIHPALFDFFTWLGYLNSLINPIIYTVFNEEFRQAFQKIVPFRKAS
75	O95264	>sp|O95264|5HT3B_HUMAN 5-hydroxytryptamine receptor 3B GN=HTR3B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLSSVMAPLWACILVAAGILATDTHHPQDSALYHLSKQLLQKYHKEVRPVYNWTKATTVYLDLFVHAILDVDAENQILKTSVWYQEVWNDEFLSWNSSMFDEIREISLPLSAIWAPDIIINEFVDIERYPDLPYVYVNSSGTIENYKPIQVVSACSLETYAFPFDVQNCSLTFKSILHTVEDVDLAFLRSPEDIQHDKKAFLNDSEWELLSVSSTYSILQSSAGGFAQIQFNVVMRRHPLVYVVSLLIPSIFLMLVDLGSFYLPPNCRARIVFKTSVLVGYTVFRVNMSNQVPRSVGSTPLIGHFFTICMAFLVLSLAKSIVLVKFLHDEQRGGQEQPFLCLRGDTDADRPRVEPRAQRAVVTESSLYGEHLAQPGTLKEVWSQLQSISNYLQTQDQTDQQEAEWLVLLSRFDRLLFQSYLFMLGIYTITLCSLWALWGGV
76	P34969	>sp|P34969|5HT7R_HUMAN 5-hydroxytryptamine receptor 7 GN=HTR7 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MMDVNSSGRPDLYGHLRSFLLPEVGRGLPDLSPDGGADPVAGSWAPHLLSEVTASPAPTWDAPPDNASGCGEQINYGRVEKVVIGSILTLITLLTIAGNCLVVISVCFVKKLRQPSNYLIVSLALADLSVAVAVMPFVSVTDLIGGKWIFGHFFCNVFIAMDVMCCTASIMTLCVISIDRYLGITRPLTYPVRQNGKCMAKMILSVWLLSASITLPPLFGWAQNVNDDKVCLISQDFGYTIYSTAVAFYIPMSVMLFMYYQIYKAARKSAAKHKFPGFPRVEPDSVIALNGIVKLQKEVEECANLSRLLKHERKNISIFKREQKAATTLGIIVGAFTVCWLPFFLLSTARPFICGTSCSCIPLWVERTFLWLGYANSLINPFIYAFFNRDLRTTYRSLLQCQYRNINRKLSAAGMHEALKLAERPERPEFVLRACTRRVLLRPEKRPPVSVWVLQSPDHHNWLADKMLTTVEKKVMIHD
77	Q969T7	>sp|Q969T7|5NT3B_HUMAN 7-methylguanosine phosphate-specific 5'-nucleotidase GN=NT5C3B PE=1 SV=4 Homo sapiens OS=Human NCBI_TaxID=9606	MAEEVSTLMKATVLMRQPGRVQEIVGALRKGGGDRLQVISDFDMTLSRFAYNGKRCPSSYNILDNSKIISEECRKELTALLHHYYPIEIDPHRTVKEKLPHMVEWWTKAHNLLCQQKIQKFQIAQVVRESNAMLREGYKTFFNTLYHNNIPLFIFSAGIGDILEEIIRQMKVFHPNIHIVSNYMDFNEDGFLQGFKGQLIHTYNKNSSACENSGYFQQLEGKTNVILLGDSIGDLTMADGVPGVQNILKIGFLNDKVEERRERYMDSYDIVLEKDETLDVVNGLLQHILCQGVQLEMQGP
78	P52209	>sp|P52209|6PGD_HUMAN 6-phosphogluconate dehydrogenase, decarboxylating GN=PGD PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MAQADIALIGLAVMGQNLILNMNDHGFVVCAFNRTVSKVDDFLANEAKGTKVVGAQSLKEMVSKLKKPRRIILLVKAGQAVDDFIEKLVPLLDTGDIIIDGGNSEYRDTTRRCRDLKAKGILFVGSGVSGGEEGARYGPSLMPGGNKEAWPHIKTIFQGIAAKVGTGEPCCDWVGDEGAGHFVKMVHNGIEYGDMQLICEAYHLMKDVLGMAQDEMAQAFEDWNKTELDSFLIEITANILKFQDTDGKHLLPKIRDSAGQKGTGKWTAISALEYGVPVTLIGEAVFARCLSSLKDERIQASKKLKGPQKFQFDGDKKSFLEDIRKALYASKIISYAQGFMLLRQAATEFGWTLNYGGIALMWRGGCIIRSVFLGKIKDAFDRNPELQNLLLDDFFKSAVENCQDSWRRAVSTGVQAGIPMPCFTTALSFYDGYRHEMLPASLIQAQRDYFGAHTYELLAKPGQFIHTNWTGHGGTVSSSSYNA
80	Q676U5	>sp|Q676U5|A16L1_HUMAN Autophagy-related protein 16-1 GN=ATG16L1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MSSGLRAADFPRWKRHISEQLRRRDRLQRQAFEEIILQYNKLLEKSDLHSVLAQKLQAEKHDVPNRHEISPGHDGTWNDNQLQEMAQLRIKHQEELTELHKKRGELAQLVIDLNNQMQRKDREMQMNEAKIAECLQTISDLETECLDLRTKLCDLERANQTLKDEYDALQITFTALEGKLRKTTEENQELVTRWMAEKAQEANRLNAENEKDSRRRQARLQKELAEAAKEPLPVEQDDDIEVIVDETSDHTEETSPVRAISRAATKRLSQPAGGLLDSITNIFGRRSVSSFPVPQDNVDTHPGSGKEVRVPATALCVFDAHDGEVNAVQFSPGSRLLATGGMDRRVKLWEVFGEKCEFKGSLSGSNAGITSIEFDSAGSYLLAASNDFASRIWTVDDYRLRHTLTGHSGKVLSAKFLLDNARIVSGSHDRTLKLWDLRSKVCIKTVFAGSSCNDIVCTEQCVMSGHFDKKIRFWDIRSESIVREMELLGKITALDLNPERTELLSCSRDDLLKVIDLRTNAIKQTFSAPGFKCGSDWTRVVFSPDGSYVAAGSAEGSLYIWSVLTGKVEKVLSKQHSSSINAVAWSPSGSHVVSVDKGCKAVLWAQY
81	P02763	>sp|P02763|A1AG1_HUMAN Alpha-1-acid glycoprotein 1 GN=ORM1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MALSWVLTVLSLLPLLEAQIPLCANLVPVPITNATLDQITGKWFYIASAFRNEEYNKSVQEIQATFFYFTPNKTEDTIFLREYQTRQDQCIYNTTYLNVQRENGTISRYVGGQEHFAHLLILRDTKTYMLAFDVNDEKNWGLSVYADKPETTKEQLGEFYEALDCLRIPKSDVVYTDWKKDKCEPLEKQHEKERKQEEGES
82	P20848	>sp|P20848|A1ATR_HUMAN Putative alpha-1-antitrypsin-related protein GN=SERPINA2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MPFSVSWGVLLLAGLCCLVPSSLVEDPQGDAAQKTDTSHHDQGDWEDLACQKISYNVTDLAFDLYKSWLIYHNQHVLVTPTSVAMAFRMLSLGTKADTRTEILEGLNVNLTETPEAKIHECFQQVLQALSRPDTRLQLTTGSSLFVNKSMKLVDTFLEDTKKLYHSEASSINFRDTEEAKEQINNYVEKRTGRKVVDLVKHLKKDTSLALVDYISFHGKWKDKFKAERIMVEGFHVDDKTIIRVPMINHLGRFDIHRDRELSSWVLAQHYVGNATAFFILPDPKKMWQLEEKLTYSHLENIQRAFDIRSINLHFPKLSISGTYKLKRVPRNLGITKIFSNEADLSGVSQEAPLKLSKAVHVAVLTIDEKGTEATGAPHLEEKAWSKYQTVMFNRPFLVIIKEYITNFPLFIGKVVNPTQK
83	Q96IX9	>sp|Q96IX9|A26L1_HUMAN Putative ankyrin repeat domain-containing protein 26-like 1 GN=ANKRD36BP1 PE=5 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MGTRTLQFEISDSHEKEEDLLHKNHLMQDEIARLRLEIHTIKNQILEKKYLKDIEIIKRKHEDLQKALKQNGEKSTKTIAHYSGQLTALTDENTMLRSKLEKEKQSRQRLTKWNHTIVD
84	Q9NPC4	>sp|Q9NPC4|A4GAT_HUMAN Lactosylceramide 4-alpha-galactosyltransferase GN=A4GALT PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MSKPPDLLLRLLRGAPRQRVCTLFIIGFKFTFFVSIMIYWHVVGEPKEKGQLYNLPAEIPCPTLTPPTPPSHGPTPGNIFFLETSDRTNPNFLFMCSVESAARTHPESHVLVLMKGLPGGNASLPRHLGISLLSCFPNVQMLPLDLRELFRDTPLADWYAAVQGRWEPYLLPVLSDASRIALMWKFGGIYLDTDFIVLKNLRNLTNVLGTQSRYVLNGAFLAFERRHEFMALCMRDFVDHYNGWIWGHQGPQLLTRVFKKWCSIRSLAESRACRGVTTLPPEAFYPIPWQDWKKYFEDINPEELPRLLSATYAVHVWNKKSQGTRFEATSRALLAQLHARYCPTTHEAMKMYL
85	P05067	>sp|P05067|A4_HUMAN Amyloid beta A4 protein GN=APP PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MLPGLALLLLAAWTARALEVPTDGNAGLLAEPQIAMFCGRLNMHMNVQNGKWDSDPSGTKTCIDTKEGILQYCQEVYPELQITNVVEANQPVTIQNWCKRGRKQCKTHPHFVIPYRCLVGEFVSDALLVPDKCKFLHQERMDVCETHLHWHTVAKETCSEKSTNLHDYGMLLPCGIDKFRGVEFVCCPLAEESDNVDSADAEEDDSDVWWGGADTDYADGSEDKVVEVAEEEEVAEVEEEEADDDEDDEDGDEVEEEAEEPYEEATERTTSIATTTTTTTESVEEVVREVCSEQAETGPCRAMISRWYFDVTEGKCAPFFYGGCGGNRNNFDTEEYCMAVCGSAMSQSLLKTTQEPLARDPVKLPTTAASTPDAVDKYLETPGDENEHAHFQKAKERLEAKHRERMSQVMREWEEAERQAKNLPKADKKAVIQHFQEKVESLEQEAANERQQLVETHMARVEAMLNDRRRLALENYITALQAVPPRPRHVFNMLKKYVRAEQKDRQHTLKHFEHVRMVDPKKAAQIRSQVMTHLRVIYERMNQSLSLLYNVPAVAEEIQDEVDELLQKEQNYSDDVLANMISEPRISYGNDALMPSLTETKTTVELLPVNGEFSLDDLQPWHSFGADSVPANTENEVEPVDARPAADRGLTTRPGSGLTNIKTEEISEVKMDAEFRHDSGYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVVIATVIVITLVMLKKKQYTSIHHGVVEVDAAVTPEERHLSKMQQNGYENPTYKFFEQMQN
86	Q96GX2	>sp|Q96GX2|A7L3B_HUMAN Putative ataxin-7-like protein 3B GN=ATXN7L3B PE=3 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MEEISLANLDTNKLEAIAQEIYVDLIEDSCLGFCFEVHRAVKCGYFYLEFAETGSVKDFGIQPVEDKGACRLPLCSLPGEPGNGPDQQLQRSPPEFQ
87	Q9H7C9	>sp|Q9H7C9|AAMDC_HUMAN Mth938 domain-containing protein GN=AAMDC PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MTSPEIASLSWGQMKVKGSNTTYKDCKVWPGGSRTWDWRETGTEHSPGVQPADVKEVVEKGVQTLVIGRGMSEALKVPSSTVEYLKKHGIDVRVLQTEQAVKEYNALVAQGVRVGGVFHSTC
88	Q13685	>sp|Q13685|AAMP_HUMAN Angio-associated migratory cell protein GN=AAMP PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MESESESGAAADTPPLETLSFHGDEEIIEVVELDPGPPDPDDLAQEMEDVDFEEEEEEEGNEEGWVLEPQEGVVGSMEGPDDSEVTFALHSASVFCVSLDPKTNTLAVTGGEDDKAFVWRLSDGELLFECAGHKDSVTCAGFSHDSTLVATGDMSGLLKVWQVDTKEEVWSFEAGDLEWMEWHPRAPVLLAGTADGNTWMWKVPNGDCKTFQGPNCPATCGRVLPDGKRAVVGYEDGTIRIWDLKQGSPIHVLKGTEGHQGPLTCVAANQDGSLILTGSVDCQAKLVSATTGKVVGVFRPETVASQPSLGEGEESESNSVESLGFCSVMPLAAVGYLDGTLAIYDLATQTLRHQCQHQSGIVQLLWEAGTAVVYTCSLDGIVRLWDARTGRLLTDYRGHTAEILDFALSKDASLVVTTSGDHKAKVFCVQRPDR
89	Q9Y312	>sp|Q9Y312|AAR2_HUMAN Protein AAR2 homolog GN=AAR2 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAAVQMDPELAKRLFFEGATVVILNMPKGTEFGIDYNSWEVGPKFRGVKMIPPGIHFLHYSSVDKANPKEVGPRMGFFLSLHQRGLTVLRWSTLREEVDLSPAPESEVEAMRANLQELDQFLGPYPYATLKKWISLTNFISEATVEKLQPENRQICAFSDVLPVLSMKHTKDRVGQNLPRCGIECKSYQEGLARLPEMKPRAGTEIRFSELPTQMFPEGATPAEITKHSMDLSYALETVLNKQFPSSPQDVLGELQFAFVCFLLGNVYEAFEHWKRLLNLLCRSEAAMMKHHTLYINLISILYHQLGEIPADFFVDIVSQDNFLTSTLQVFFSSACSIAVDATLRKKAEKFQAHLTKKFRWDFAAEPEDCAPVVVELPEGIEMG
90	Q8NHS2	>sp|Q8NHS2|AATC2_HUMAN Putative aspartate aminotransferase, cytoplasmic 2 GN=GOT1L1 PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MPTLSVFMDVPLAHKLEGSLLKTYKQDDYPNKIFLAYRVCMTNEGHPWVSLVVQKTRLQISQDPSLNYEYLPTMGLKSFIQASLALLFGKHSQAIVENRVGGVHTVGDSGAFQLGVQFLRAWHKDARIVYIISSQKELHGLVFQDMGFTVYEYSVWDPKKLCMDPDILLNVVEQIPHGCVLVMGNIIDCKLTPSGWAKLMSMIKSKQIFPFFDIPCQGLYTSDLEEDTRILQYFVSQGFEFFCSQSLSKNFGIYDEGVGMLVVVAVNNQQLLCVLSQLEGLAQALWLNPPNTGARVITSILCNPALLGEWKQSLKEVVENIMLTKEKVKEKLQLLGTPGSWGHITEQSGTHGYLGLNSQQVEYLVRKKHIYIPKNGQINFSCINANNINYITEGINEAVLLTESSEMCLPKEKKTLIGIKL
91	P00505	>sp|P00505|AATM_HUMAN Aspartate aminotransferase, mitochondrial GN=GOT2 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MALLHSGRVLPGIAAAFHPGLAAAASARASSWWTHVEMGPPDPILGVTEAFKRDTNSKKMNLGVGAYRDDNGKPYVLPSVRKAEAQIAAKNLDKEYLPIGGLAEFCKASAELALGENSEVLKSGRFVTVQTISGTGALRIGASFLQRFFKFSRDVFLPKPTWGNHTPIFRDAGMQLQGYRYYDPKTCGFDFTGAVEDISKIPEQSVLLLHACAHNPTGVDPRPEQWKEIATVVKKRNLFAFFDMAYQGFASGDGDKDAWAVRHFIEQGINVCLCQSYAKNMGLYGERVGAFTMVCKDADEAKRVESQLKILIRPMYSNPPLNGARIAAAILNTPDLRKQWLQEVKVMADRIIGMRTQLVSNLKKEGSTHNWQHITDQIGMFCFTGLKPEQVERLIKEFSIYMTKDGRISVAGVTSSNVGYLAHAIHQVTK
92	Q9NUQ8	>sp|Q9NUQ8|ABCF3_HUMAN ATP-binding cassette sub-family F member 3 GN=ABCF3 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MATCAEILRSEFPEIDGQVFDYVTGVLHSGSADFESVDDLVEAVGELLQEVSGDSKDDAGIRAVCQRMYNTLRLAEPQSQGNSQVLLDAPIQLSKITENYDCGTKLPGLLKREQSSTVNAKKLEKAEARLKAKQEKRSEKDTLKTSNPLVLEEASASQAGSRKESRLESSGKNKSYDVRIENFDVSFGDRVLLAGADVNLAWGRRYGLVGRNGLGKTTLLKMLATRSLRVPAHISLLHVEQEVAGDDTPALQSVLESDSVREDLLRRERELTAQIAAGRAEGSEAAELAEIYAKLEEIEADKAPARASVILAGLGFTPKMQQQPTREFSGGWRMRLALARALFARPDLLLLDEPTNMLDVRAILWLENYLQTWPSTILVVSHDRNFLNAIATDIIHLHSQRLDGYRGDFETFIKSKQERLLNQQREYEAQQQYRQHIQVFIDRFRYNANRASQVQSKLKMLEKLPELKPVDKESEVVMKFPDGFEKFSPPILQLDEVDFYYDPKHVIFSRLSVSADLESRICVVGENGAGKSTMLKLLLGDLAPVRGIRHAHRNLKIGYFSQHHVEQLDLNVSAVELLARKFPGRPEEEYRHQLGRYGISGELAMRPLASLSGGQKSRVAFAQMTMPCPNFYILDEPTNHLDMETIEALGRALNNFRGGVILVSHDERFIRLVCRELWVCEGGGVTRVEGGFDQYRALLQEQFRREGFL
93	Q9H222	>sp|Q9H222|ABCG5_HUMAN ATP-binding cassette sub-family G member 5 GN=ABCG5 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MGDLSSLTPGGSMGLQVNRGSQSSLEGAPATAPEPHSLGILHASYSVSHRVRPWWDITSCRQQWTRQILKDVSLYVESGQIMCILGSSGSGKTTLLDAMSGRLGRAGTFLGEVYVNGRALRREQFQDCFSYVLQSDTLLSSLTVRETLHYTALLAIRRGNPGSFQKKVEAVMAELSLSHVADRLIGNYSLGGISTGERRRVSIAAQLLQDPKVMLFDEPTTGLDCMTANQIVVLLVELARRNRIVVLTIHQPRSELFQLFDKIAILSFGELIFCGTPAEMLDFFNDCGYPCPEHSNPFDFYMDLTSVDTQSKEREIETSKRVQMIESAYKKSAICHKTLKNIERMKHLKTLPMVPFKTKDSPGVFSKLGVLLRRVTRNLVRNKLAVITRLLQNLIMGLFLLFFVLRVRSNVLKGAIQDRVGLLYQFVGATPYTGMLNAVNLFPVLRAVSDQESQDGLYQKWQMMLAYALHVLPFSVVATMIFSSVCYWTLGLHPEVARFGYFSAALLAPHLIGEFLTLVLLGIVQNPNIVNSVVALLSIAGVLVGSGFLRNIQEMPIPFKIISYFTFQKYCSEILVVNEFYGLNFTCGSSNVSVTTNPMCAFTQGIQFIEKTCPGATSRFTMNFLILYSFIPALVILGIVVFKIRDHLISR
94	P16219	>sp|P16219|ACADS_HUMAN Short-chain specific acyl-CoA dehydrogenase, mitochondrial GN=ACADS PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAAALLARASGPARRALCPRAWRQLHTIYQSVELPETHQMLLQTCRDFAEKELFPIAAQVDKEHLFPAAQVKKMGGLGLLAMDVPEELGGAGLDYLAYAIAMEEISRGCASTGVIMSVNNSLYLGPILKFGSKEQKQAWVTPFTSGDKIGCFALSEPGNGSDAGAASTTARAEGDSWVLNGTKAWITNAWEASAAVVFASTDRALQNKGISAFLVPMPTPGLTLGKKEDKLGIRGSSTANLIFEDCRIPKDSILGEPGMGFKIAMQTLDMGRIGIASQALGIAQTALDCAVNYAENRMAFGAPLTKLQVIQFKLADMALALESARLLTWRAAMLKDNKKPFIKEAAMAKLAASEAATAISHQAIQILGGMGYVTEMPAERHYRDARITEIYEGTSEIQRLVIAGHLLRSYRS
95	Q8NC06	>sp|Q8NC06|ACBD4_HUMAN Acyl-CoA-binding domain-containing protein 4 GN=ACBD4 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MGTEKESPEPDCQKQFQAAVSVIQNLPKNGSYRPSYEEMLRFYSYYKQATMGPCLVPRPGFWDPIGRYKWDAWNSLGKMSREEAMSAYITEMKLVAQKVIDTVPLGEVAEDMFGYFEPLYQVIPDMPRPPETFLRRVTGWKEQVVNGDVGAVSEPPCLPKEPAPPSPESHSPRDLDSEVFCDSLEQLEPELSSGQHLEESVIPGTAPCPPQRKRGCGAARRGPRSWTCGCWGQFEHYRRACRRCRRGCRAWRACPGPLSSLTLSVRLE
96	Q709F0	>sp|Q709F0|ACD11_HUMAN Acyl-CoA dehydrogenase family member 11 GN=ACAD11 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MKPGATGESDLAEVLPQHKFDSKSLEAYLNQHLSGFGAEREATLTIAQYRAGKSNPTFYLQKGFQTYVLRKKPPGSLLPKAHQIDREFKVQKALFSIGFPVPKPILYCSDTSVIGTEFYVMEHVQGRIFRDLTIPGLSPAERSAIYVATVETLAQLRSLNIQSLQLEGYGIGAGYCKRQVSTWTKQYQAAAHQDIPAMQQLSEWLMKNLPDNDNEENLIHGDFRLDNIVFHPKECRVIAVLDWELSTIGHPLSDLAHFSLFYFWPRTVPMINQGSYSENSGIPSMEELISIYCRCRGINSILPNWNFFLALSYFKMAGIAQGVYSRYLLGNNSSEDSFLFANIVQPLAETGLQLSKRTFSTVLPQIDTTGQLFVQTRKGQEVLIKVKHFMKQHILPAEKEVTEFYVQNENSVDKWGKPLVIDKLKEMAKVEGLWNLFLPAVSGLSHVDYALIAEETGKCFFAPDVFNCQAPDTGNMEVLHLYGSEEQKKQWLEPLLQGNITSCFCMTEPDVASSDATNIECSIQRDEDSYVINGKKWWSSGAGNPKCKIAIVLGRTQNTSLSRHKQHSMILVPMNTPGVKIIRPLSVFGYTDNFHGGHFEIHFNQVRVPATNLILGEGRGFEISQGRLGPGRIHHCMRTVGLAERALQIMCERATQRIAFKKKLYAHEVVAHWIAESRIAIEKIRLLTLKAAHSMDTLGSAGAKKEIAMIKVAAPRAVSKIVDWAIQVCGGAGVSQDYPLANMYAITRVLRLADGPDEVHLSAIATMELRDQAKRLTAKI
97	Q4AC99	>sp|Q4AC99|1A1L2_HUMAN Probable inactive 1-aminocyclopropane-1-carboxylate synthase-like protein 2 GN=ACCSL PE=2 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MSHRSDTLPVPSGQRRGRVPRDHSIYTQLLEITLHLQQAMTEHFVQLTSRQGLSLEERRHTEAICEHEALLSRLICRMINLLQSGAASGLELQVPLPSEDSRGDVRYGQRAQLSGQPDPVPQLSDCEAAFVNRDLSIRGIDISVFYQSSFQDYNAYQKDKYHKDKNTLGFINLGTSENKLCMDLMTERLQESDMNCIEDTLLQYPDWRGQPFLREEVARFLTYYCRAPTRLDPENVVVLNGCCSVFCALAMVLCDPGEAFLVPAPFYGGFAFSSRLYAKVELIPVHLESEVTVTNTHPFQLTVDKLEEALLEARLEGKKVRGLVLINPQNPLGDIYSPDSLMKYLEFAKRYNLHVIIDEIYMLSVFDESITFHSILSMKSLPDSNRTHVIWGTSKDFGISGFRFGALYTHNKEVASAVSAFGYLHSISGITQHKLCQLLQNTEWIDKVYLPTNCYRLREAHKYITAELKALEIPFHNRSSGLYVWINLKKYLDPCTFEEERLLYCRFLDNKLLLSRGKTYMCKEPGWFCLIFADELPRLKLAMRRFCDVLQEQKEALIVKQLEDAMRE
98	P30450	>sp|P30450|1A26_HUMAN HLA class I histocompatibility antigen, A-26 alpha chain GN=HLA-A PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMAPRTLVLLLSGALALTQTWAGSHSMRYFYTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDRNTRNVKAHSQTDRANLGTLRGYYNQSEDGSHTIQRMYGCDVGPDGRFLRGYQQDAYDGKDYIALNEDLRSWTAADMAAQITQRKWETAHEAEQWRAYLEGRCVEWLRRYLENGKETLQRTDAPKTHMTHHAVSDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWASVVVPSGQEQRYTCHVQHEGLPKPLTLRWEPSSQPTIPIVGIIAGLVLFGAVIAGAVVAAVMWRRKSSDRKGGSYSQAASSDSAQGSDMSLTACKV
99	P16188	>sp|P16188|1A30_HUMAN HLA class I histocompatibility antigen, A-30 alpha chain GN=HLA-A PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMAPRTLLLLLSGALALTHTWAGSHSMRYFSTSVSRPGSGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQERPEYWDQETRNVKAQSQTDRVDLGTLRGYYNQSEAGSHTIQIMYGCDVGSDGRFLRGYEQHAYDGKDYIALNEDLRSWTAADMAAQITQRKWEAARWAEQLRAYLEGTCVEWLRRYLENGKETLQRTDPPKTHMTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWELSSQPTIPIVGIIAGLVLLGAVITGAVVAAVMWRRKSSDRKGGSYTQAASSDSAQGSDVSLTACKV
100	P10314	>sp|P10314|1A32_HUMAN HLA class I histocompatibility antigen, A-32 alpha chain GN=HLA-A PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMAPRTLLLLLLGALALTQTWAGSHSMRYFFTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDQETRNVKAHSQTDRESLRIALRYYNQSEAGSHTIQMMYGCDVGPDGRLLRGYQQDAYDGKDYIALNEDLRSWTAADMAAQITQRKWEAARVAEQLRAYLEGTCVEWLRRYLENGKETLQRTDAPKTHMTHHAVSDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWASVVVPSGQEQRYTCHVQHEGLPKPLTLRWEPSSQPTIPIVGIIAGLVLFGAMFAGAVVAAVRWRRKSSDRKGGSYSQAASSDSAQGSDMSLTACKV
101	P30456	>sp|P30456|1A43_HUMAN HLA class I histocompatibility antigen, A-43 alpha chain GN=HLA-A PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMAPRTLVLLLSGALALTQTWAGSHSMRYFYTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDLQTRNVKAHSQTDRANLGTLRGYYNQSEDGSHTIQRMYGCDVGPDGRFLRGYQQDAYDGKDYIALNEDLRSWTAADMAAQITQRKWETAHEAEQWRAYLEGRCVEWLRRYLENGKETLQRTDAPKTHMTHHAVSDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWASVVVPSGQEQRYTCHVQHEGLPKPLTLRWEPSSQPTIPIVGIIAGLVLFGAVIAGAVVAAVMWRRKSSDRKGGSYSQAASSDSAQGSDMSLTACKV
102	P10316	>sp|P10316|1A69_HUMAN HLA class I histocompatibility antigen, A-69 alpha chain GN=HLA-A PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMAPRTLVLLLSGALALTQTWAGSHSMRYFYTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDRNTRNVKAQSQTDRVDLGTLRGYYNQSEAGSHTVQRMYGCDVGSDWRFLRGYHQYAYDGKDYIALKEDLRSWTAADMAAQTTKHKWEAAHVAEQLRAYLEGTCVEWLRRYLENGKETLQRTDAPKTHMTHHAVSDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGQEQRYTCHVQHEGLPKPLTLRWEPSSQPTIPIVGIIAGLVLFGAVITGAVVAAVMWRRKSSDRKGGSYSQAASSDSAQGSDVSLTACKV
103	P30461	>sp|P30461|1B13_HUMAN HLA class I histocompatibility antigen, B-13 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTLLLLLWGAVALTETWAGSHSMRYFYTAMSRPGRGEPRFITVGYVDDTQFVRFDSDATSPRMAPRAPWIEQEGPEYWDRETQISKTNTQTYRENLRTALRYYNQSEAGSHTWQTMYGCDLGPDGRLLRGHNQLAYDGKDYIALNEDLSSWTAADTAAQITQLKWEAARVAEQLRAYLEGECVEWLRRYLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCRRKSSGGKGGSYSQAACSDSAQGSDVSLTA
104	P30485	>sp|P30485|1B47_HUMAN HLA class I histocompatibility antigen, B-47 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTLLLLLWGAVALTETWAGSHSMRYFYTAMSRPGRGEPRFITVGYVDDTLFVRFDSDATSPRKEPRAPWIEQEGPEYWDRETQISKTNTQTYREDLRTLLRYYNQSEAGSHTLQRMFGCDVGPDGRLLRGYHQDAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAARVAEQLRAYLEGECVEWLRRYLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVVCRRKSSGGKGGSYSQAACSDSAQGSDVSLTA
105	P30487	>sp|P30487|1B49_HUMAN HLA class I histocompatibility antigen, B-49 alpha chain GN=HLA-B PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTVLLLLSAALALTETWAGSHSMRYFHTAMSRPGRGEPRFITVGYVDDTLFVRFDSDATSPRKEPRAPWIEQEGPEYWDRETQISKTNTQTYRENLRIALRYYNQSEAGSHTWQRMYGCDLGPDGRLLRGYNQLAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAAREAEQLRAYLEGLCVEWLRRYLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
106	P18464	>sp|P18464|1B51_HUMAN HLA class I histocompatibility antigen, B-51 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTVLLLLWGAVALTETWAGSHSMRYFYTAMSRPGRGEPRFIAVGYVDDTQFVRFDSDAASPRTEPRAPWIEQEGPEYWDRNTQIFKTNTQTYRENLRIALRYYNQSEAGSHTWQTMYGCDVGPDGRLLRGHNQYAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAAREAEQLRAYLEGLCVEWLRRHLENGKETLQRADPPKTHVTHHPVSDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
133	Q9NRW3	>sp|Q9NRW3|ABC3C_HUMAN DNA dC->dU-editing enzyme APOBEC-3C GN=APOBEC3C PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MNPQIRNPMKAMYPGTFYFQFKNLWEANDRNETWLCFTVEGIKRRSVVSWKTGVFRNQVDSETHCHAERCFLSWFCDDILSPNTKYQVTWYTSWSPCPDCAGEVAEFLARHSNVNLTIFTARLYYFQYPCYQEGLRSLSQEGVAVEIMDYEDFKYCWENFVYNDNEPFKPWKGLKTNFRLLKRRLRESLQ
107	P30490	>sp|P30490|1B52_HUMAN HLA class I histocompatibility antigen, B-52 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTVLLLLWGAVALTETWAGSHSMRYFYTAMSRPGRGEPRFIAVGYVDDTQFVRFDSDAASPRTEPRAPWIEQEGPEYWDRETQISKTNTQTYRENLRIALRYYNQSEAGSHTWQTMYGCDVGPDGRLLRGHNQYAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAAREAEQLRAYLEGLCVEWLRRHLENGKETLQRADPPKTHVTHHPVSDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
108	P10319	>sp|P10319|1B58_HUMAN HLA class I histocompatibility antigen, B-58 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTVLLLLWGAVALTETWAGSHSMRYFYTAMSRPGRGEPRFIAVGYVDDTQFVRFDSDAASPRTEPRAPWIEQEGPEYWDGETRNMKASAQTYRENLRIALRYYNQSEAGSHIIQRMYGCDLGPDGRLLRGHDQSAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAARVAEQLRAYLEGLCVEWLRRYLENGKETLQRADPPKTHVTHHPVSDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
109	Q31612	>sp|Q31612|1B73_HUMAN HLA class I histocompatibility antigen, B-73 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLVMAPRTVLLLLSAALALTETWAGSHSMRYFHTSVSRPGRGEPRFITVGYVDDTQFVRFDSDAASPREEPRAPWIEQEGPEYWDRNTQICKAKAQTDRVGLRNLRGYYNQSEDGSHTWQTMYGCDMGPDGRLLRGYNQFAYDGKDYIALNEDLRSWTAADTAAQITQRKWEAARVAEQLRAYLEGECVEWLRRHLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGQEQRYTCHVQHEGLQEPCTLRWKPSSQSTIPIVGIVAGLAVLVVTVAVVAVVAAVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
110	Q29718	>sp|Q29718|1B82_HUMAN HLA class I histocompatibility antigen, B-82 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTLLLLLWGALALTETWAGSHSMRYFYTAMSRPGRGEPRFISVGYVDDTQFVRFDSDAASPREEPRAPWIEQEGPEYWDRNTQIYKAQAQTDRESLRNLRGYYNQSEAGSHTLQRMFGCDLGPDGRLLRGHNQLAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAARVAEQDRAYLEDLCVESLRRYLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
111	P30504	>sp|P30504|1C04_HUMAN HLA class I histocompatibility antigen, Cw-4 alpha chain GN=HLA-C PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVMAPRTLILLLSGALALTETWAGSHSMRYFSTSVSWPGRGEPRFIAVGYVDDTQFVRFDSDAASPRGEPREPWVEQEGPEYWDRETQKYKRQAQADRVNLRKLRGYYNQSEDGSHTLQRMFGCDLGPDGRLLRGYNQFAYDGKDYIALNEDLRSWTAADTAAQITQRKWEAAREAEQRRAYLEGTCVEWLRRYLENGKETLQRAEHPKTHVTHHPVSDHEATLRCWALGFYPAEITLTWQWDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPEPLTLRWKPSSQPTIPIVGIVAGLAVLAVLAVLGAMVAVVMCRRKSSGGKGGSCSQAASSNSAQGSDESLIACKA
112	P10321	>sp|P10321|1C07_HUMAN HLA class I histocompatibility antigen, Cw-7 alpha chain GN=HLA-C PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MRVMAPRALLLLLSGGLALTETWACSHSMRYFDTAVSRPGRGEPRFISVGYVDDTQFVRFDSDAASPRGEPRAPWVEQEGPEYWDRETQKYKRQAQADRVSLRNLRGYYNQSEDGSHTLQRMSGCDLGPDGRLLRGYDQSAYDGKDYIALNEDLRSWTAADTAAQITQRKLEAARAAEQLRAYLEGTCVEWLRRYLENGKETLQRAEPPKTHVTHHPLSDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGQEQRYTCHMQHEGLQEPLTLSWEPSSQPTIPIMGIVAGLAVLVVLAVLGAVVTAMMCRRKSSGGKGGSCSQAACSNSAQGSDESLITCKA
113	P30508	>sp|P30508|1C12_HUMAN HLA class I histocompatibility antigen, Cw-12 alpha chain GN=HLA-C PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MRVMAPRTLILLLSGALALTETWACSHSMRYFYTAVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASPRGEPRAPWVEQEGPEYWDRETQKYKRQAQADRVSLRNLRGYYNQSEAGSHTLQRMYGCDLGPDGRLLRGYDQSAYDGKDYIALNEDLRSWTAADTAAQITQRKWEAAREAEQWRAYLEGTCVEWLRRYLENGKETLQRAEHPKTHVTHHPVSDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPEPLTLRWEPSSQPTIPIVGIVAGLAVLAVLAVLGAVMAVVMCRRKSSGGKGGSCSQAASSNSAQGSDESLIACKA
114	Q29960	>sp|Q29960|1C16_HUMAN HLA class I histocompatibility antigen, Cw-16 alpha chain GN=HLA-C PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVMAPRTLILLLSGALALTETWACSHSMRYFYTAVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASPRGEPRAPWVEQEGPEYWDRETQKYKRQAQTDRVSLRNLRGYYNQSEAGSHTLQWMYGCDLGPDGRLLRGYDQSAYDGKDYIALNEHLRSCTAADTAAQITQRKWEAARAAEQQRAYLEGTCVEWLRRYLENGKETLQRAEHPKTHVTHHLVSDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPEPLTLRWEPSSQPTIPIVGIVAGLAVLAVLAVLGAVVAVVMCRRKSSGGKGGSCSQAASSNSAQGSDESLIACKA
115	Q29974	>sp|Q29974|2B1G_HUMAN HLA class II histocompatibility antigen, DRB1-16 beta chain GN=HLA-DRB1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MVCLKLPGGSCMTALTVTLMVLSSPLALAGDTRPRFLWQPKRECHFFNGTERVRFLDRYFYNQEESVRFDSDVGEYRAVTELGRPDAEYWNSQKDFLEDRRAAVDTYCRHNYGVGESFTVQRRVQPKVTVYPSKTQPLQHHNLLVCSVSGFYPGSIEVRWFLNGQEEKAGMVSTGLIQNGDWTFQTLVMLETVPRSGEVYTCQVEHPSVTSPLTVEWRARSESAQSKMLSGVGGFVLGLLFLGAGLFIYFRNQKGHSGLQPTGFLS
116	Q13542	>sp|Q13542|4EBP2_HUMAN Eukaryotic translation initiation factor 4E-binding protein 2 GN=EIF4EBP2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MSSSAGSGHQPSQSRAIPTRTVAISDAAQLPHDYCTTPGGTLFSTTPGGTRIIYDRKFLLDRRNSPMAQTPPCHLPNIPGVTSPGTLIEDSKVEVNNLNNLNNHDRKHAVGDDAQFEMDI
117	P41595	>sp|P41595|5HT2B_HUMAN 5-hydroxytryptamine receptor 2B GN=HTR2B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MALSYRVSELQSTIPEHILQSTFVHVISSNWSGLQTESIPEEMKQIVEEQGNKLHWAALLILMVIIPTIGGNTLVILAVSLEKKLQYATNYFLMSLAVADLLVGLFVMPIALLTIMFEAMWPLPLVLCPAWLFLDVLFSTASIMHLCAISVDRYIAIKKPIQANQYNSRATAFIKITVVWLISIGIAIPVPIKGIETDVDNPNNITCVLTKERFGDFMLFGSLAAFFTPLAIMIVTYFLTIHALQKKAYLVKNKPPQRLTWLTVSTVFQRDETPCSSPEKVAMLDGSRKDKALPNSGDETLMRRTSTIGKKSVQTISNEQRASKVLGIVFFLFLLMWCPFFITNITLVLCDSCNQTTLQMLLEIFVWIGYVSSGVNPLVYTLFNKTFRDAFGRYITCNYRATKSVKTLRKRSSKIYFRNPMAENSKFFKKHGIRNGINPAMYQSPMRLRSSTIQSSSIILLDTLLLTENEGDKTEEQVSYV
118	P28335	>sp|P28335|5HT2C_HUMAN 5-hydroxytryptamine receptor 2C GN=HTR2C PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MVNLRNAVHSFLVHLIGLLVWQCDISVSPVAAIVTDIFNTSDGGRFKFPDGVQNWPALSIVIIIIMTIGGNILVIMAVSMEKKLHNATNYFLMSLAIADMLVGLLVMPLSLLAILYDYVWPLPRYLCPVWISLDVLFSTASIMHLCAISLDRYVAIRNPIEHSRFNSRTKAIMKIAIVWAISIGVSVPIPVIGLRDEEKVFVNNTTCVLNDPNFVLIGSFVAFFIPLTIMVITYCLTIYVLRRQALMLLHGHTEEPPGLSLDFLKCCKRNTAEEENSANPNQDQNARRRKKKERRPRGTMQAINNERKASKVLGIVFFVFLIMWCPFFITNILSVLCEKSCNQKLMEKLLNVFVWIGYVCSGINPLVYTLFNKIYRRAFSNYLRCNYKVEKKPPVRQIPRVAATALSGRELNVNIYRHTNEPVIEKASDNEPGIEMQVENLELPVNPSSVVSERISSV
119	Q13639	>sp|Q13639|5HT4R_HUMAN 5-hydroxytryptamine receptor 4 GN=HTR4 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MDKLDANVSSEEGFGSVEKVVLLTFLSTVILMAILGNLLVMVAVCWDRQLRKIKTNYFIVSLAFADLLVSVLVMPFGAIELVQDIWIYGEVFCLVRTSLDVLLTTASIFHLCCISLDRYYAICCQPLVYRNKMTPLRIALMLGGCWVIPTFISFLPIMQGWNNIGIIDLIEKRKFNQNSNSTYCVFMVNKPYAITCSVVAFYIPFLLMVLAYYRIYVTAKEHAHQIQMLQRAGASSESRPQSADQHSTHRMRTETKAAKTLCIIMGCFCLCWAPFFVTNIVDPFIDYTVPGQVWTAFLWLGYINSGLNPFLYAFLNKSFRRAFLIILCCDDERYRRPSILGQTVPCSTTTINGSTHVLRDAVECGGQWESQCHPPATSPLVAAQPSDT
120	P50406	>sp|P50406|5HT6R_HUMAN 5-hydroxytryptamine receptor 6 GN=HTR6 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MVPEPGPTANSTPAWGAGPPSAPGGSGWVAAALCVVIALTAAANSLLIALICTQPALRNTSNFFLVSLFTSDLMVGLVVMPPAMLNALYGRWVLARGLCLLWTAFDVMCCSASILNLCLISLDRYLLILSPLRYKLRMTPLRALALVLGAWSLAALASFLPLLLGWHELGHARPPVPGQCRLLASLPFVLVASGLTFFLPSGAICFTYCRILLAARKQAVQVASLTTGMASQASETLQVPRTPRPGVESADSRRLATKHSRKALKASLTLGILLGMFFVTWLPFFVANIVQAVCDCISPGLFDVLTWLGYCNSTMNPIIYPLFMRDFKRALGRFLPCPRCPRERQASLASPSLRTSHSGPRPGLSLQQVLPLPLPPDSDSDSDAGSGGSSGLRLTAQLLLPGEATQDPPLPTRAAAAVNFFNIDPAEPELRPHPLGIPTN
121	Q9H0P0	>sp|Q9H0P0|5NT3A_HUMAN Cytosolic 5'-nucleotidase 3A GN=NT5C3A PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MRAPSMDRAAVARVGAVASASVCALVAGVVLAQYIFTLKRKTGRKTKIIEMMPEFQKSSVRIKNPTRVEEIICGLIKGGAAKLQIITDFDMTLSRFSYKGKRCPTCHNIIDNCKLVTDECRKKLLQLKEKYYAIEVDPVLTVEEKYPYMVEWYTKSHGLLVQQALPKAKLKEIVAESDVMLKEGYENFFDKLQQHSIPVFIFSAGIGDVLEEVIRQAGVYHPNVKVVSNFMDFDETGVLKGFKGELIHVFNKHDGALRNTEYFNQLKDNSNIILLGDSQGDLRMADGVANVEHILKIGYLNDRVDELLEKYMDSYDIVLVQDESLEVANSILQKIL
122	P49902	>sp|P49902|5NTC_HUMAN Cytosolic purine 5'-nucleotidase GN=NT5C2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MSTSWSDRLQNAADMPANMDKHALKKYRREAYHRVFVNRSLAMEKIKCFGFDMDYTLAVYKSPEYESLGFELTVERLVSIGYPQELLSFAYDSTFPTRGLVFDTLYGNLLKVDAYGNLLVCAHGFNFIRGPETREQYPNKFIQRDDTERFYILNTLFNLPETYLLACLVDFFTNCPRYTSCETGFKDGDLFMSYRSMFQDVRDAVDWVHYKGSLKEKTVENLEKYVVKDGKLPLLLSRMKEVGKVFLATNSDYKYTDKIMTYLFDFPHGPKPGSSHRPWQSYFDLILVDARKPLFFGEGTVLRQVDTKTGKLKIGTYTGPLQHGIVYSGGSSDTICDLLGAKGKDILYIGDHIFGDILKSKKRQGWRTFLVIPELAQELHVWTDKSSLFEELQSLDIFLAELYKHLDSSSNERPDISSIQRRIKKVTHDMDMCYGMMGSLFRSGSRQTLFASQVMRYADLYAASFINLLYYPFSYLFRAAHVLMPHESTVEHTHVDINEMESPLATRNRTSVDFKDTDYKRHQLTRSISEIKPPNLFPLAPQEITHCHDEDDDEEEEEEEE
123	Q5TYW2	>sp|Q5TYW2|A20A1_HUMAN Ankyrin repeat domain-containing protein 20A1 GN=ANKRD20A1 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MKLFGFGSRRGQTAQGSIDHVYTGSGYRIRDSELQKIHRAAVKGDAAEVERCLARRSGDLDALDKQHRTALHLACTSGHVQVVTLLVNRKCQIDVCDKENRTPLIQAVHCQEEACAVILLEHGANPNLKDIYGNTALHYAVYSESTSLAEKLLSHGAHIEALDKDNNTPLLFAIICKKEKMVEFLLKKKASSHAVDRLRRSALMLAVYYDSPGIVNILLKQNIDVFAQDMCGRDAEDYAISHHLTKIQQQILEHKKKILKKEKSDVGSSDESAVSIFHELRVDSLPASDDKDLNVATKQCVPEKVSEPLPGSSHEKGNRIVNGQGEGPPAKHPSLKPSTEVEDPAVKGAVQRKNVQTLRAEQALPVASEEEQERHERSEKKQPQVKEGNNTNKSEKIQLSENICDSTSSAAAGRLTQQRKIGKTYPQQFPKKLKEEHDRCTLKQENEEKTNVNMLYKKNREELERKEKQYKKEVEAKQLEPTVQSLEMKSKTARNTPNWDFHNHEEMKGLMDENCILKADIAILRQEICTMKNDNLEKENKYLKDIKIVKETNAALEKYIKLNEEMITETAFRYQQELNDLKAENTRLNAELLKEKESKKRLEADIESYQSRLAAAISKHSESVKTERNLKLALERTRDVSVQVEMSSAISKVKAENEFLTEQLSETQIKFNALKDKFRKTRDSLRKKSLALETVQNDLSQTQQQTQEMKEMYQNAEAKVNNSTGKWNCVEERICHLQRENAWLVQQLDDVHQKEDHKEIVTNIQRGFIESGKKDLVLEEKSKKLMNECDHLKESLFQYEREKTEGVVSIKEDKYFQTSRKTI
124	Q5VUR7	>sp|Q5VUR7|A20A3_HUMAN Ankyrin repeat domain-containing protein 20A3 GN=ANKRD20A3 PE=3 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MKLFGFGSRRGQTAQGSIDHVYTGSGYRIRDSELQKIHRAAVKGDAAEVERCLARRSGDLDALDKQHRTALHLACASGHVQVVTLLVNRKCQIDVCDKENRTPLIQAVHCQEEACAVILLEHGANPNLKDIYGNTALHYAVYSESTSLAEKLLSHGAHIEALDKDNNTPLLFAIICKKEKMVEFLLKRKASSHAVDRLRRSALMLAVYYDSPGIVNILLKQNIDVFAQDMCGRDAEDYAISHHLTKIQQQILEHKKKILKKEKSDVGSSDESAVSIFHELRVDSLPASDDKDLNVATKQCVPEKVSEPLPGSSHEKGNRIVNGQGEGPPAKHPSLKPSTEVEDPAVKGAVQRKNVQTLRAEQALPVASEEEQERHERSEKKQPQVKEGNNTNKSEKIQLSENICDSTSSAAAGRLTQQRKIGKTYPQQFPKKLKEEHDRCTLKQENEEKTNVNMLYKKNREELERKEKQYKKEVEAKQLEPTVQSLEMKSKTARNTPNRDFHNHEEMKGLMDENCILKADIAILRQEICTMKNDNLEKENKYLKDIKIVKETNAALEKYIKLNEEMITETAFRYQQELNYLKAENTRLNAELLKEKESKKRLEADIESYQSRLAAAISKHSESVKTERNLKLALERTRDVSVQVEMSSAISKVKDENEFLTEQLSETQIKFNALKDKFRKTRDSLRKKSLALETVQNDLSQTQQQTQEMKEMYQNAEAKVNNSTGKWNCVEERICHLQRENAWLVQQLDDVHQKEDHKEIVTNIQRGFIESGKKDLVLEEKSKKLMNECDHLKESLFQYEREKTEGVVSIKEDKYFQTSRKTI
125	P0DMS8	>sp|P0DMS8|AA3R_HUMAN Adenosine receptor A3 GN=ADORA3 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MPNNSTALSLANVTYITMEIFIGLCAIVGNVLVICVVKLNPSLQTTTFYFIVSLALADIAVGVLVMPLAIVVSLGITIHFYSCLFMTCLLLIFTHASIMSLLAIAVDRYLRVKLTVRYKRVTTHRRIWLALGLCWLVSFLVGLTPMFGWNMKLTSEYHRNVTFLSCQFVSVMRMDYMVYFSFLTWIFIPLVVMCAIYLDIFYIIRNKLSLNLSNSKETGAFYGREFKTAKSLFLVLFLFALSWLPLSIINCIIYFNGEVPQLVLYMGILLSHANSMMNPIVYAYKIKKFKETYLLILKACVVCHPSDSLDTSIEKNSE
126	Q9NS82	>sp|Q9NS82|AAA1_HUMAN Asc-type amino acid transporter 1 GN=SLC7A10 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAGHTQQPSGRGNPRPAPSPSPVPGTVPGASERVALKKEIGLLSACTIIIGNIIGSGIFISPKGVLEHSGSVGLALFVWVLGGGVTALGSLCYAELGVAIPKSGGDYAYVTEIFGGLAGFLLLWSAVLIMYPTSLAVISMTFSNYVLQPVFPNCIPPTTASRVLSMACLMLLTWVNSSSVRWATRIQDMFTGGKLLALSLIIGVGLLQIFQGHFEELRPSNAFAFWMTPSVGHLALAFLQGSFAFSGWNFLNYVTEEMVDARKNLPRAIFISIPLVTFVYTFTNIAYFTAMSPQELLSSNAVAVTFGEKLLGYFSWVMPVSVALSTFGGINGYLFTYSRLCFSGAREGHLPSLLAMIHVRHCTPIPALLVCCGATAVIMLVGDTYTLINYVSFINYLCYGVTILGLLLLRWRRPALHRPIKVNLLIPVAYLVFWAFLLVFSFISEPMVCGVGVIIILTGVPIFFLGVFWRSKPKCVHRLTESMTHWGQELCFVVYPQDAPEEEENGPCPPSLLPATDKPSKPQ
127	Q8N5Z0	>sp|Q8N5Z0|AADAT_HUMAN Kynurenine/alpha-aminoadipate aminotransferase, mitochondrial GN=AADAT PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MNYARFITAASAARNPSPIRTMTDILSRGPKSMISLAGGLPNPNMFPFKTAVITVENGKTIQFGEEMMKRALQYSPSAGIPELLSWLKQLQIKLHNPPTIHYPPSQGQMDLCVTSGSQQGLCKVFEMIINPGDNVLLDEPAYSGTLQSLHPLGCNIINVASDESGIVPDSLRDILSRWKPEDAKNPQKNTPKFLYTVPNGNNPTGNSLTSERKKEIYELARKYDFLIIEDDPYYFLQFNKFRVPTFLSMDVDGRVIRADSFSKIISSGLRIGFLTGPKPLIERVILHIQVSTLHPSTFNQLMISQLLHEWGEEGFMAHVDRVIDFYSNQKDAILAAADKWLTGLAEWHVPAAGMFLWIKVKGINDVKELIEEKAVKMGVLMLPGNAFYVDSSAPSPYLRASFSSASPEQMDVAFQVLAQLIKESL
128	O43741	>sp|O43741|AAKB2_HUMAN 5'-AMP-activated protein kinase subunit beta-2 GN=PRKAB2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MGNTTSDRVSGERHGAKAARSEGAGGHAPGKEHKIMVGSTDDPSVFSLPDSKLPGDKEFVSWQQDLEDSVKPTQQARPTVIRWSEGGKEVFISGSFNNWSTKIPLIKSHNDFVAILDLPEGEHQYKFFVDGQWVHDPSEPVVTSQLGTINNLIHVKKSDFEVFDALKLDSMESSETSCRDLSSSPPGPYGQEMYAFRSEERFKSPPILPPHLLQVILNKDTNISCDPALLPEPNHVMLNHLYALSIKDSVMVLSATHRYKKKYVTTLLYKPI
129	Q9UGJ0	>sp|Q9UGJ0|AAKG2_HUMAN 5'-AMP-activated protein kinase subunit gamma-2 GN=PRKAG2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MGSAVMDTKKKKDVSSPGGSGGKKNASQKRRSLRVHIPDLSSFAMPLLDGDLEGSGKHSSRKVDSPFGPGSPSKGFFSRGPQPRPSSPMSAPVRPKTSPGSPKTVFPFSYQESPPRSPRRMSFSGIFRSSSKESSPNSNPATSPGGIRFFSRSRKTSGLSSSPSTPTQVTKQHTFPLESYKHEPERLENRIYASSSPPDTGQRFCPSSFQSPTRPPLASPTHYAPSKAAALAAALGPAEAGMLEKLEFEDEAVEDSESGVYMRFMRSHKCYDIVPTSSKLVVFDTTLQVKKAFFALVANGVRAAPLWESKKQSFVGMLTITDFINILHRYYKSPMVQIYELEEHKIETWRELYLQETFKPLVNISPDASLFDAVYSLIKNKIHRLPVIDPISGNALYILTHKRILKFLQLFMSDMPKPAFMKQNLDELGIGTYHNIAFIHPDTPIIKALNIFVERRISALPVVDESGKVVDIYSKFDVINLAAEKTYNNLDITVTQALQHRSQYFEGVVKCNKLEILETIVDRIVRAEVHRLVVVNEADSIVGIISLSDILQALILTPAGAKQKETETE
130	Q9BTE6	>sp|Q9BTE6|AASD1_HUMAN Alanyl-tRNA editing protein Aarsd1 GN=AARSD1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAFWCQRDSYAREFTTTVVSCCPAELQTEGSNGKKEVLSGFQVVLEDTVLFPEGGGQPDDRGTINDISVLRVTRRGEQADHFTQTPLDPGSQVLVRVDWERRFDHMQQHSGQHLITAVADHLFKLKTTSWELGRFRSAIELDTPSMTAEQVAAIEQSVNEKIRDRLPVNVRELSLDDPEVEQVSGRGLPDDHAGPIRVVNIEGVDSNMCCGTHVSNLSDLQVIKILGTEKGKKNRTNLIFLSGNRVLKWMERSHGTEKALTALLKCGAEDHVEAVKKLQNSTKILQKNNLNLLRDLAVHIAHSLRNSPDWGGVVILHRKEGDSEFMNIIANEIGSEETLLFLTVGDEKGGGLFLLAGPPASVETLGPRVAEVLEGKGAGKKGRFQGKATKMSRRMEAQALLQDYISTQSAKE
131	Q9UDR5	>sp|Q9UDR5|AASS_HUMAN Alpha-aminoadipic semialdehyde synthase, mitochondrial GN=AASS PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLQVHRTGLGRLGVSLSKGLHHKAVLAVRREDVNAWERRAPLAPKHIKGITNLGYKVLIQPSNRRAIHDKDYVKAGGILQEDISEACLILGVKRPPEEKLMSRKTYAFFSHTIKAQEANMGLLDEILKQEIRLIDYEKMVDHRGVRVVAFGQWAGVAGMINILHGMGLRLLALGHHTPFMHIGMAHNYRNSSQAVQAVRDAGYEISLGLMPKSIGPLTFVFTGTGNVSKGAQAIFNELPCEYVEPHELKEVSQTGDLRKVYGTVLSRHHHLVRKTDAVYDPAEYDKHPERYISRFNTDIAPYTTCLINGIYWEQNTPRLLTRQDAQSLLAPGKFSPAGVEGCPALPHKLVAICDISADTGGSIEFMTECTTIEHPFCMYDADQHIIHDSVEGSGILMCSIDNLPAQLPIEATECFGDMLYPYVEEMILSDATQPLESQNFSPVVRDAVITSNGTLPDKYKYIQTLRESRERAQSLSMGTRRKVLVLGSGYISEPVLEYLSRDGNIEITVGSDMKNQIEQLGKKYNINPVSMDICKQEEKLGFLVAKQDLVISLLPYVLHPLVAKACITNKVNMVTASYITPALKELEKSVEDAGITIIGELGLDPGLDHMLAMETIDKAKEVGATIESYISYCGGLPAPEHSNNPLRYKFSWSPVGVLMNVMQSATYLLDGKVVNVAGGISFLDAVTSMDFFPGLNLEGYPNRDSTKYAEIYGISSAHTLLRGTLRYKGYMKALNGFVKLGLINREALPAFRPEANPLTWKQLLCDLVGISPSSEHDVLKEAVLKKLGGDNTQLEAAEWLGLLGDEQVPQAESILDALSKHLVMKLSYGPEEKDMIVMRDSFGIRHPSGHLEHKTIDLVAYGDINGFSAMAKTVGLPTAMAAKMLLDGEIGAKGLMGPFSKEIYGPILERIKAEGIIYTTQSTIKP
132	Q9NY61	>sp|Q9NY61|AATF_HUMAN Protein AATF GN=AATF PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAGPQPLALQLEQLLNPRPSEADPEADPEEATAARVIDRFDEGEDGEGDFLVVGSIRKLASASLLDTDKRYCGKTTSRKAWNEDHWEQTLPGSSDEEISDEEGSGDEDSEGLGLEEYDEDDLGAAEEQECGDHRESKKSRSHSAKTPGFSVQSISDFEKFTKGMDDLGSSEEEEDEESGMEEGDDAEDSQGESEEDRAGDRNSEDDGVVMTFSSVKVSEEVEKGRAVKNQIALWDQLLEGRIKLQKALLTTNQLPQPDVFPLFKDKGGPEFSSALKNSHKALKALLRSLVGLQEELLFQYPDTRYLVDGTKPNAGSEEISSEDDELVEEKKQQRRRVPAKRKLEMEDYPSFMAKRFADFTVYRNRTLQKWHDKTKLASGKLGKGFGAFERSILTQIDHILMDKERLLRRTQTKRSVYRVLGKPEPAAQPVPESLPGEPEILPQAPANAHLKDLDEEIFDDDDFYHQLLRELIERKTSSLDPNDQVAMGRQWLAIQKLRSKIHKKVDRKASKGRKLRFHVLSKLLSFMAPIDHTTMNDDARTELYRSLFGQLHPPDEGHGD
137	Q4W5N1	>sp|Q4W5N1|ABCAB_HUMAN Putative ATP-binding cassette sub-family A member 11 GN=ABCA11P PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MKYGNEIMNKDPVFRISPRSRGTHTNPEEPEEDVQAERVQAANALTTPNLEEEPVITASCLHKEYYETKKVAFQQQRRKQPSEMFRFVLKSEVLGLLGHNGAGKSTSIKMITGCTVPTAGVVVLQGNRASVRQQRDNSLKFLGTALRRTHCVPNLQ
138	Q86UK0	>sp|Q86UK0|ABCAC_HUMAN ATP-binding cassette sub-family A member 12 GN=ABCA12 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MASLFHQLQILVWKNWLGVKRQPLWTLVLILWPVIIFIILAITRTKFPPTAKPTCYLAPRNLPSTGFFPFLQTLLCDTDSKCKDTPYGPQDLLRRKGIDDALFKDSEILRKSSNLDKDSSLSFQSTQVPERRHASLATVFPSPSSDLEIPGTYTFNGSQVLARILGLEKLLKQNSTSEDIRRELCDSYSGYIVDDAFSWTFLGRNVFNKFCLSNMTLLESSLQELNKQFSQLSSDPNNQKIVFQEIVRMLSFFSQVQEQKAVWQLLSSFPNVFQNDTSLSNLFDVLRKANSVLLVVQKVYPRFATNEGFRTLQKSVKHLLYTLDSPAQGDSDNITHVWNEDDGQTLSPSSLAAQLLILENFEDALLNISANSPYIPYLACVRNVTDSLARGSPENLRLLQSTIRFKKSFLRNGSYEDYFPPVPEVLKSKLSQLRNLTELLCESETFSLIEKSCQLSDMSFGSLCEESEFDLQLLEAAELGTEIAASLLYHDNVISKKVRDLLTGDPSKINLNMDQFLEQALQMNYLENITQLIPIIEAMLHVNNSADASEKPGQLLEMFKNVEELKEDLRRTTGMSNRTIDKLLAIPIPDNRAEIISQVFWLHSCDTNITTPKLEDAMKEFCNLSLSERSRQSYLIGLTLLHYLNIYNFTYKVFFPRKDQKPVEKMMELFIRLKEILNQMASGTHPLLDKMRSLKQMHLPRSVPLTQAMYRSNRMNTPQGSFSTISQALCSQGITTEYLTAMLPSSQRPKGNHTKDFLTYKLTKEQIASKYGIPINSTPFCFSLYKDIINMPAGPVIWAFLKPMLLGRILYAPYNPVTKAIMEKSNVTLRQLAELREKSQEWMDKSPLFMNSFHLLNQAIPMLQNTLRNPFVQVFVKFSVGLDAVELLKQIDELDILRLKLENNIDIIDQLNTLSSLTVNISSCVLYDRIQAAKTIDEMEREAKRLYKSNELFGSVIFKLPSNRSWHRGYDSGNVFLPPVIKYTIRMSLKTAQTTRSLRTKIWAPGPHNSPSHNQIYGRAFIYLQDSIERAIIELQTGRNSQEIAVQVQAIPYPCFMKDNFLTSVSYSLPIVLMVAWVVFIAAFVKKLVYEKDLRLHEYMKMMGVNSCSHFFAWLIESVGFLLVTIVILIIILKFGNILPKTNGFILFLYFSDYSFSVIAMSYLISVFFNNTNIAALIGSLIYIIAFFPFIVLVTVENELSYVLKVFMSLLSPTAFSYASQYIARYEEQGIGLQWENMYTSPVQDDTTSFGWLCCLILADSFIYFLIAWYVRNVFPGTYGMAAPWYFPILPSYWKERFGCAEVKPEKSNGLMFTNIMMQNTNPSASPEYMFSSNIEPEPKDLTVGVALHGVTKIYGSKVAVDNLNLNFYEGHITSLLGPNGAGKTTTISMLTGLFGASAGTIFVYGKDIKTDLHTVRKNMGVCMQHDVLFSYLTTKEHLLLYGSIKVPHWTKKQLHEEVKRTLKDTGLYSHRHKRVGTLSGGMKRKLSISIALIGGSRVVILDEPSTGVDPCSRRSIWDVISKNKTARTIILSTHHLDEAEVLSDRIAFLEQGGLRCCGSPFYLKEAFGDGYHLTLTKKKSPNLNANAVCDTMAVTAMIQSHLPEAYLKEDIGGELVYVLPPFSTKVSGAYLSLLRALDNGMGDLNIGCYGISDTTVEEVFLNLTKESQKNSAMSLEHLTQKKIGNSNANGISTPDDLSVSSSNFTDRDDKILTRGERLDGFGLLLKKIMAILIKRFHHTRRNWKGLIAQVILPIVFVTTAMGLGTLRNSSNSYPEIQISPSLYGTSEQTAFYANYHPSTEALVSAMWDFPGIDNMCLNTSDLQCLNKDSLEKWNTSGEPITNFGVCSCSENVQECPKFNYSPPHRRTYSSQVIYNLTGQRVENYLISTANEFVQKRYGGWSFGLPLTKDLRFDITGVPANRTLAKVWYDPEGYHSLPAYLNSLNNFLLRVNMSKYDAARHGIIMYSHPYPGVQDQEQATISSLIDILVALSILMGYSVTTASFVTYVVREHQTKAKQLQHISGIGVTCYWVTNFIYDMVFYLVPVAFSIGIIAIFKLPAFYSENNLGAVSLLLLLFGYATFSWMYLLAGLFHETGMAFITYVCVNLFFGINSIVSLSVVYFLSKEKPNDPTLELISETLKRIFLIFPQFCFGYGLIELSQQQSVLDFLKAYGVEYPNETFEMNKLGAMFVALVSQGTMFFSLRLLINESLIKKLRLFFRKFNSSHVRETIDEDEDVRAERLRVESGAAEFDLVQLYCLTKTYQLIHKKIIAVNNISIGIPAGECFGLLGVNGAGKTTIFKMLTGDIIPSSGNILIRNKTGSLGHVDSHSSLVGYCPQEDALDDLVTVEEHLYFYARVHGIPEKDIKETVHKLLRRLHLMPFKDRATSMCSYGTKRKLSTALALIGKPSILLLDEPSSGMDPKSKRHLWKIISEEVQNKCSVILTSHSMEECEALCTRLAIMVNGKFQCIGSLQHIKSRFGRGFTVKVHLKNNKVTMETLTKFMQLHFPKTYLKDQHLSMLEYHVPVTAGGVANIFDLLETNKTALNITNFLVSQTTLEEVFINFAKDQKSYETADTSSQGSTISVDSQDDQMES
139	Q9NSE7	>sp|Q9NSE7|ABCCD_HUMAN Putative ATP-binding cassette sub-family C member 13 GN=ABCC13 PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MLSSTQNAGGSYQRVRGALDTQKCSPEKSASFFSKVTYSWFSRVITLGYKRPLEREDLFELKESDSFCTACPIFEKQWRKEVLRNQERQKVKVSCYKEAHIKKPSLLYALWNTFKSILIQVALFKVFADILSFTSPLIMKQIIIFCEHSSDFGWNGYGYAVALLVVVFLQTLILQQYQRFNMLTSAKVKTAVNGLIYKKALLLSNVSRQKFSTGEIINLMSATHGLDSKPQSPLVCPFSNPNGRISPLARAGSSSVSRGGSPCVCYTNKCFSCN
140	P45844	>sp|P45844|ABCG1_HUMAN ATP-binding cassette sub-family G member 1 GN=ABCG1 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MACLMAAFSVGTAMNASSYSAEMTEPKSVCVSVDEVVSSNMEATETDLLNGHLKKVDNNLTEAQRFSSLPRRAAVNIEFRDLSYSVPEGPWWRKKGYKTLLKGISGKFNSGELVAIMGPSGAGKSTLMNILAGYRETGMKGAVLINGLPRDLRCFRKVSCYIMQDDMLLPHLTVQEAMMVSAHLKLQEKDEGRREMVKEILTALGLLSCANTRTGSLSGGQRKRLAIALELVNNPPVMFFDEPTSGLDSASCFQVVSLMKGLAQGGRSIICTIHQPSAKLFELFDQLYVLSQGQCVYRGKVCNLVPYLRDLGLNCPTYHNPADFVMEVASGEYGDQNSRLVRAVREGMCDSDHKRDLGGDAEVNPFLWHRPSEEVKQTKRLKGLRKDSSSMEGCHSFSASCLTQFCILFKRTFLSIMRDSVLTHLRITSHIGIGLLIGLLYLGIGNEAKKVLSNSGFLFFSMLFLMFAALMPTVLTFPLEMGVFLREHLNYWYSLKAYYLAKTMADVPFQIMFPVAYCSIVYWMTSQPSDAVRFVLFAALGTMTSLVAQSLGLLIGAASTSLQVATFVGPVTAIPVLLFSGFFVSFDTIPTYLQWMSYISYVRYGFEGVILSIYGLDREDLHCDIDETCHFQKSEAILRELDVENAKLYLDFIVLGIFFISLRLIAYFVLRYKIRAER
141	Q0P651	>sp|Q0P651|ABD18_HUMAN Protein ABHD18 GN=ABHD18 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MGVSKLDILYRRLLLTKLFIRGWGRPEDLKRLFEFRKMIGNRERCQNLVSSDYPVHIDKIEEQSDCKILDGHFVSPMAHYVPDIMPIESVIARFQFIVPKEWNSKYRPVCIHLAGTGDHHYWRRRTLMARPMIKEARMASLLLENPYYGCRKPKDQVRSSLKNVSDLFVMGGALVLESAALLHWLEREGYGPLGMTGISMGGHMASLAVSNWPKPMPLIPCLSWSTASGVFTTTDSFKMGQEFVKHFTSSADKLTNLNLVSRTLNLDISNQVVSQKPADCHNSSKTSVSATSEGLLLQDTSKMKRFNQTLSTNKSGYTSRNPQSYHLLSKEQSRNSLRKESLIFMKGVMDECTHVANFSVPVDPSLIIVVQAKEDAYIPRTGVRSLQEIWPGCEIRYLEGGHISAYLFKQGLFR
142	Q9Y235	>sp|Q9Y235|ABEC2_HUMAN C->U-editing enzyme APOBEC-2 GN=APOBEC2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAQKEEAAVATEAASQNGEDLENLDDPEKLKELIELPPFEIVTGERLPANFFKFQFRNVEYSSGRNKTFLCYVVEAQGKGGQVQASRGYLEDEHAAAHAEEAFFNTILPAFDPALRYNVTWYVSSSPCAACADRIIKTLSKTKNLRLLILVGRLFMWEEPEIQAALKKLKEAGCKLRIMKPQDFEYVWQNFVEQEEGESKAFQPWEDIQENFLYYEEKLADILK
143	Q8WW27	>sp|Q8WW27|ABEC4_HUMAN Putative C->U-editing enzyme APOBEC-4 GN=APOBEC4 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MEPIYEEYLANHGTIVKPYYWLSFSLDCSNCPYHIRTGEEARVSLTEFCQIFGFPYGTTFPQTKHLTFYELKTSSGSLVQKGHASSCTGNYIHPESMLFEMNGYLDSAIYNNDSIRHIILYSNNSPCNEANHCCISKMYNFLITYPGITLSIYFSQLYHTEMDFPASAWNREALRSLASLWPRVVLSPISGGIWHSVLHSFISGVSGSHVFQPILTGRALADRHNAYEINAITGVKPYFTDVLLQTKRNPNTKAQEALESYPLNNAFPGQFFQMPSGQLQPNLPPDLRAPVVFVLVPLRDLPPMHMGQNPNKPRNIVRHLNMPQMSFQETKDLGRLPTGRSVEIVEITEQFASSKEADEKKKKKGKK
144	Q96I13	>sp|Q96I13|ABHD8_HUMAN Protein ABHD8 GN=ABHD8 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLTGVTDGIFCCLLGTPPNAVGPLESVESSDGYTFVEVKPGRVLRVKHAGPAPAAAPPPPSSASSDAAQGDLSGLVRCQRRITVYRNGRLLVENLGRAPRADLLHGQNGSGEPPAALEVELADPAGSDGRLAPGSAGSGSGSGSGGRRRRARRPKRTIHIDCEKRITSCKGAQADVVLFFIHGVGGSLAIWKEQLDFFVRLGYEVVAPDLAGHGASSAPQVAAAYTFYALAEDMRAIFKRYAKKRNVLIGHSYGVSFCTFLAHEYPDLVHKVIMINGGGPTALEPSFCSIFNMPTCVLHCLSPCLAWSFLKAGFARQGAKEKQLLKEGNAFNVSSFVLRAMMSGQYWPEGDEVYHAELTVPVLLVHGMHDKFVPVEEDQRMAEILLLAFLKLIDEGSHMVMLECPETVNTLLHEFLLWEPEPSPKALPEPLPAPPEDKK
145	Q8NFV4	>sp|Q8NFV4|ABHDB_HUMAN Protein ABHD11 GN=ABHD11 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRAGQQLASMLRWTRAWRLPREGLGPHGPSFARVPVAPSSSSGGRGGAEPRPLPLSYRLLDGEAALPAVVFLHGLFGSKTNFNSIAKILAQQTGRRVLTVDARNHGDSPHSPDMSYEIMSQDLQDLLPQLGLVPCVVVGHSMGGKTAMLLALQRPELVERLIAVDISPVESTGVSHFATYVAAMRAINIADELPRSRARKLADEQLSSVIQDMAVRQHLLTNLVEVDGRFVWRVNLDALTQHLDKILAFPQRQESYLGPTLFLLGGNSQFVHPSHHPEIMRLFPRAQMQTVPNAGHWIHADRPQDFIAAIRGFLV
146	Q9P2A4	>sp|Q9P2A4|ABI3_HUMAN ABI gene family member 3 GN=ABI3 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAELQQLQEFEIPTGREALRGNHSALLRVADYCEDNYVQATDKRKALEETMAFTTQALASVAYQVGNLAGHTLRMLDLQGAALRQVEARVSTLGQMVNMHMEKVARREIGTLATVQRLPPGQKVIAPENLPPLTPYCRRPLNFGCLDDIGHGIKDLSTQLSRTGTLSRKSIKAPATPASATLGRPPRIPEPVHLPVVPDGRLSAASSAFSLASAGSAEGVGGAPTPKGQAAPPAPPLPSSLDPPPPPAAVEVFQRPPTLEELSPPPPDEELPLPLDLPPPPPLDGDELGLPPPPPGFGPDEPSWVPASYLEKVVTLYPYTSQKDNELSFSEGTVICVTRRYSDGWCEGVSSEGTGFFPGNYVEPSC
147	Q969K4	>sp|Q969K4|ABTB1_HUMAN Ankyrin repeat and BTB/POZ domain-containing protein 1 GN=ABTB1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MDTSDLFASCRKGDVGRVRYLLEQRDVEVNVRDKWDSTPLYYACLCGHEELVLYLLANGARCEANTFDGERCLYGALSDPIRRALRDYKQVTASCRRRDYYDDFLQRLLEQGIHSDVVFVVHGKPFRVHRCVLGARSAYFANMLDTKWKGKSVVVLRHPLINPVAFGALLQYLYTGRLDIGVEHVSDCERLAKQCQLWDLLSDLEAKCEKVSEFVASKPGTCVKVLTIEPPPADPRLREDMALLADCALPPELRGDLWELPFPCPDGFNSCPDICFRVAGCSFLCHKAFFCGRSDYFRALLDDHFRESEEPATSGGPPAVTLHGISPDVFTHVLYYMYSDHTELSPEAAYDVLSVADMYLLPGLKRLCGRSLAQMLDEDTVVGVWRVAKLFRLARLEDQCTEYMAKVIEKLVEREDFVEAVKEEAAAVAARQETDSIPLVDDIRFHVASTVQTYSAIEEAQQRLRALEDLLVSIGLDC
148	Q15027	>sp|Q15027|ACAP1_HUMAN Arf-GAP with coiled-coil, ANK repeat and PH domain-containing protein 1 GN=ACAP1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MTVKLDFEECLKDSPRFRASIELVEAEVSELETRLEKLLKLGTGLLESGRHYLAASRAFVVGICDLARLGPPEPMMAECLEKFTVSLNHKLDSHAELLDATQHTLQQQIQTLVKEGLRGFREARRDFWRGAESLEAALTHNAEVPRRRAQEAEEAGAALRTARAGYRGRALDYALQINVIEDKRKFDIMEFVLRLVEAQATHFQQGHEELSRLSQYRKELGAQLHQLVLNSAREKRDMEQRHVLLKQKELGGEEPEPSLREGPGGLVMEGHLFKRASNAFKTWSRRWFTIQSNQLVYQKKYKDPVTVVVDDLRLCTVKLCPDSERRFCFEVVSTSKSCLLQADSERLLQLWVSAVQSSIASAFSQARLDDSPRGPGQGSGHLAIGSAATLGSGGMARGREPGGVGHVVAQVQSVDGNAQCCDCREPAPEWASINLGVTLCIQCSGIHRSLGVHFSKVRSLTLDSWEPELVKLMCELGNVIINQIYEARVEAMAVKKPGPSCSRQEKEAWIHAKYVEKKFLTKLPEIRGRRGGRGRPRGQPPVPPKPSIRPRPGSLRSKPEPPSEDLGSLHPGALLFRASGHPPSLPTMADALAHGADVNWVNGGQDNATPLIQATAANSLLACEFLLQNGANVNQADSAGRGPLHHATILGHTGLACLFLKRGADLGARDSEGRDPLTIAMETANADIVTLLRLAKMREAEAAQGQAGDETYLDIFRDFSLMASDDPEKLSRRSHDLHTL
149	Q15057	>sp|Q15057|ACAP2_HUMAN Arf-GAP with coiled-coil, ANK repeat and PH domain-containing protein 2 GN=ACAP2 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MKMTVDFEECLKDSPRFRAALEEVEGDVAELELKLDKLVKLCIAMIDTGKAFCVANKQFMNGIRDLAQYSSNDAVVETSLTKFSDSLQEMINFHTILFDQTQRSIKAQLQNFVKEDLRKFKDAKKQFEKVSEEKENALVKNAQVQRNKQHEVEEATNILTATRKCFRHIALDYVLQINVLQSKRRSEILKSMLSFMYAHLAFFHQGYDLFSELGPYMKDLGAQLDRLVVDAAKEKREMEQKHSTIQQKDFSSDDSKLEYNVDAANGIVMEGYLFKRASNAFKTWNRRWFSIQNNQLVYQKKFKDNPTVVVEDLRLCTVKHCEDIERRFCFEVVSPTKSCMLQADSEKLRQAWIKAVQTSIATAYREKGDESEKLDKKSSPSTGSLDSGNESKEKLLKGESALQRVQCIPGNASCCDCGLADPRWASINLGITLCIECSGIHRSLGVHFSKVRSLTLDTWEPELLKLMCELGNDVINRVYEANVEKMGIKKPQPGQRQEKEAYIRAKYVERKFVDKYSISLSPPEQQKKFVSKSSEEKRLSISKFGPGDQVRASAQSSVRSNDSGIQQSSDDGRESLPSTVSANSLYEPEGERQDSSMFLDSKHLNPGLQLYRASYEKNLPKMAEALAHGADVNWANSEENKATPLIQAVLGGSLVTCEFLLQNGANVNQRDVQGRGPLHHATVLGHTGQVCLFLKRGANQHATDEEGKDPLSIAVEAANADIVTLLRLARMNEEMRESEGLYGQPGDETYQDIFRDFSQMASNNPEKLNRFQQDSQKF
150	Q8N6N7	>sp|Q8N6N7|ACBD7_HUMAN Acyl-CoA-binding domain-containing protein 7 GN=ACBD7 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MALQADFDRAAEDVRKLKARPDDGELKELYGLYKQAIVGDINIACPGMLDLKGKAKWEAWNLKKGLSTEDATSAYISKAKELIEKYGI
427	Q9NPJ3	>sp|Q9NPJ3|ACO13_HUMAN Acyl-coenzyme A thioesterase 13 GN=ACOT13 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MTSMTQSLREVIKAMTKARNFERVLGKITLVSAAPGKVICEMKVEEEHTNAIGTLHGGLTATLVDNISTMALLCTERGAPGVSVDMNITYMSPAKLGEDIVITAHVLKQGKTLAFTSVDLTNKATGKLIAQGRHTKHLGN
151	P45954	>sp|P45954|ACDSB_HUMAN Short/branched chain specific acyl-CoA dehydrogenase, mitochondrial GN=ACADSB PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MEGLAVRLLRGSRLLRRNFLTCLSSWKIPPHVSKSSQSEALLNITNNGIHFAPLQTFTDEEMMIKSSVKKFAQEQIAPLVSTMDENSKMEKSVIQGLFQQGLMGIEVDPEYGGTGASFLSTVLVIEELAKVDASVAVFCEIQNTLINTLIRKHGTEEQKATYLPQLTTEKVGSFCLSEAGAGSDSFALKTRADKEGDYYVLNGSKMWISSAEHAGLFLVMANVDPTIGYKGITSFLVDRDTPGLHIGKPENKLGLRASSTCPLTFENVKVPEANILGQIGHGYKYAIGSLNEGRIGIAAQMLGLAQGCFDYTIPYIKERIQFGKRLFDFQGLQHQVAHVATQLEAARLLTYNAARLLEAGKPFIKEASMAKYYASEIAGQTTSKCIEWMGGVGYTKDYPVEKYFRDAKIGTIYEGASNIQLNTIAKHIDAEY
152	Q5QJU3	>sp|Q5QJU3|ACER2_HUMAN Alkaline ceramidase 2 GN=ACER2 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MGAPHWWDQLQAGSSEVDWCEDNYTIVPAIAEFYNTISNVLFFILPPICMCLFRQYATCFNSGIYLIWTLLVVVGIGSVYFHATLSFLGQMLDELAVLWVLMCALAMWFPRRYLPKIFRNDRGRFKVVVSVLSAVTTCLAFVKPAINNISLMTLGVPCTALLIAELKRCDNMRVFKLGLFSGLWWTLALFCWISDRAFCELLSSFNFPYLHCMWHILICLAAYLGCVCFAYFDAASEIPEQGPVIKFWPNEKWAFIGVPYVSLLCANKKSSVKIT
153	P12821	>sp|P12821|ACE_HUMAN Angiotensin-converting enzyme GN=ACE PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MGAASGRRGPGLLLPLPLLLLLPPQPALALDPGLQPGNFSADEAGAQLFAQSYNSSAEQVLFQSVAASWAHDTNITAENARRQEEAALLSQEFAEAWGQKAKELYEPIWQNFTDPQLRRIIGAVRTLGSANLPLAKRQQYNALLSNMSRIYSTAKVCLPNKTATCWSLDPDLTNILASSRSYAMLLFAWEGWHNAAGIPLKPLYEDFTALSNEAYKQDGFTDTGAYWRSWYNSPTFEDDLEHLYQQLEPLYLNLHAFVRRALHRRYGDRYINLRGPIPAHLLGDMWAQSWENIYDMVVPFPDKPNLDVTSTMLQQGWNATHMFRVAEEFFTSLELSPMPPEFWEGSMLEKPADGREVVCHASAWDFYNRKDFRIKQCTRVTMDQLSTVHHEMGHIQYYLQYKDLPVSLRRGANPGFHEAIGDVLALSVSTPEHLHKIGLLDRVTNDTESDINYLLKMALEKIAFLPFGYLVDQWRWGVFSGRTPPSRYNFDWWYLRTKYQGICPPVTRNETHFDAGAKFHVPNVTPYIRYFVSFVLQFQFHEALCKEAGYEGPLHQCDIYRSTKAGAKLRKVLQAGSSRPWQEVLKDMVGLDALDAQPLLKYFQPVTQWLQEQNQQNGEVLGWPEYQWHPPLPDNYPEGIDLVTDEAEASKFVEEYDRTSQVVWNEYAEANWNYNTNITTETSKILLQKNMQIANHTLKYGTQARKFDVNQLQNTTIKRIIKKVQDLERAALPAQELEEYNKILLDMETTYSVATVCHPNGSCLQLEPDLTNVMATSRKYEDLLWAWEGWRDKAGRAILQFYPKYVELINQAARLNGYVDAGDSWRSMYETPSLEQDLERLFQELQPLYLNLHAYVRRALHRHYGAQHINLEGPIPAHLLGNMWAQTWSNIYDLVVPFPSAPSMDTTEAMLKQGWTPRRMFKEADDFFTSLGLLPVPPEFWNKSMLEKPTDGREVVCHASAWDFYNGKDFRIKQCTTVNLEDLVVAHHEMGHIQYFMQYKDLPVALREGANPGFHEAIGDVLALSVSTPKHLHSLNLLSSEGGSDEHDINFLMKMALDKIAFIPFSYLVDQWRWRVFDGSITKENYNQEWWSLRLKYQGLCPPVPRTQGDFDPGAKFHIPSSVPYIRYFVSFIIQFQFHEALCQAAGHTGPLHKCDIYQSKEAGQRLATAMKLGFSRPWPEAMQLITGQPNMSASAMLSYFKPLLDWLRTENELHGEKLGWPQYNWTPNSARSEGPLPDSGRVSFLGLDLDAQQARVGQWLLLFLGIALLVATLGLSQRLFSIRHRSLHRHSHGPQFGSEVELRHS
154	Q9NPB9	>sp|Q9NPB9|ACKR4_HUMAN Atypical chemokine receptor 4 GN=ACKR4 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MALEQNQSTDYYYEENEMNGTYDYSQYELICIKEDVREFAKVFLPVFLTIVFVIGLAGNSMVVAIYAYYKKQRTKTDVYILNLAVADLLLLFTLPFWAVNAVHGWVLGKIMCKITSALYTLNFVSGMQFLACISIDRYVAVTKVPSQSGVGKPCWIICFCVWMAAILLSIPQLVFYTVNDNARCIPIFPRYLGTSMKALIQMLEICIGFVVPFLIMGVCYFITARTLMKMPNIKISRPLKVLLTVVIVFIVTQLPYNIVKFCRAIDIIYSLITSCNMSKRMDIAIQVTESIALFHSCLNPILYVFMGASFKNYVMKVAKKYGSWRRQRQSVEEFPFDSEGPTEPTSTFSI
155	Q9Y614	>sp|Q9Y614|ACL7B_HUMAN Actin-like protein 7B GN=ACTL7B PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MATRNSPMPLGTAQGDPGEAGTRPGPDASLRDTGAATQLKMKPRKVHKIKAVIIDLGSQYCKCGYAGEPRPTYFISSTVGKRCPEAADAGDTRKWTLVGHELLNTEAPLKLVNPLKHGIVVDWDCVQDIWEYIFRTAMKILPEEHAVLVSDPPLSPSSNREKYAELMFETFGIPAMHVTSQSLLSIYSYGKTSGLVVESGHGVSHVVPISEGDVLPGLTSRADYAGGDLTNYLMQLLNEAGHAFTDDHLHIIEHIKKKCCYAAFLPEEELGLVPEELRVDYELPDGKLITIGQERFRCSEMLFQPSLAGSTQPGLPELTAACLGRCQDTGFKEEMAANVLLCGGCTMLDGFPERFQRELSLLCPGDSPAVAAAPERKTSVWTGGSILASLQAFQQLWVSKEEFEERGSVAIYSKC
156	P62258	>sp|P62258|1433E_HUMAN 14-3-3 protein epsilon GN=YWHAE PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MDDREDLVYQAKLAEQAERYDEMVESMKKVAGMDVELTVEERNLLSVAYKNVIGARRASWRIISSIEQKEENKGGEDKLKMIREYRQMVETELKLICCDILDVLDKHLIPAANTGESKVFYYKMKGDYHRYLAEFATGNDRKEAAENSLVAYKAASDIAMTELPPTHPIRLGLALNFSVFYYEILNSPDRACRLAKAAFDDAIAELDTLSEESYKDSTLIMQLLRDNLTLWTSDMQGDGEEQNKEALQDVEDENQ
157	Q04917	>sp|Q04917|1433F_HUMAN 14-3-3 protein eta GN=YWHAH PE=1 SV=4 Homo sapiens OS=Human NCBI_TaxID=9606	MGDREQLLQRARLAEQAERYDDMASAMKAVTELNEPLSNEDRNLLSVAYKNVVGARRSSWRVISSIEQKTMADGNEKKLEKVKAYREKIEKELETVCNDVLSLLDKFLIKNCNDFQYESKVFYLKMKGDYYRYLAEVASGEKKNSVVEASEAAYKEAFEISKEQMQPTHPIRLGLALNFSVFYYEIQNAPEQACLLAKQAFDDAIAELDTLNEDSYKDSTLIMQLLRDNLTLWTSDQQDEEAGEGN
158	P61981	>sp|P61981|1433G_HUMAN 14-3-3 protein gamma GN=YWHAG PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MVDREQLVQKARLAEQAERYDDMAAAMKNVTELNEPLSNEERNLLSVAYKNVVGARRSSWRVISSIEQKTSADGNEKKIEMVRAYREKIEKELEAVCQDVLSLLDNYLIKNCSETQYESKVFYLKMKGDYYRYLAEVATGEKRATVVESSEKAYSEAHEISKEHMQPTHPIRLGLALNYSVFYYEIQNAPEQACHLAKTAFDDAIAELDTLNEDSYKDSTLIMQLLRDNLTLWTSDQQDDDGGEGNN
159	Q9TQE0	>sp|Q9TQE0|2B19_HUMAN HLA class II histocompatibility antigen, DRB1-9 beta chain GN=HLA-DRB1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MVCLKLPGGSCMAALTVTLMVLSSPLALAGDTQPRFLKQDKFECHFFNGTERVRYLHRGIYNQEENVRFDSDVGEYRAVTELGRPVAESWNSQKDFLERRRAEVDTVCRHNYGVGESFTVQRRVHPEVTVYPAKTQPLQHHNLLVCSVSGFYPGSIEVRWFRNGQEEKAGVVSTGLIQNGDWTFQTLVMLETVPRSGEVYTCQVEHPSVMSPLTVEWRARSESAQSKMLSGVGGFVLGLLFLGAGLFIYFRNQKGHSGLQPTGFLS
160	P31937	>sp|P31937|3HIDH_HUMAN 3-hydroxyisobutyrate dehydrogenase, mitochondrial GN=HIBADH PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAASLRLLGAASGLRYWSRRLRPAAGSFAAVCSRSVASKTPVGFIGLGNMGNPMAKNLMKHGYPLIIYDVFPDACKEFQDAGEQVVSSPADVAEKADRIITMLPTSINAIEAYSGANGILKKVKKGSLLIDSSTIDPAVSKELAKEVEKMGAVFMDAPVSGGVGAARSGNLTFMVGGVEDEFAAAQELLGCMGSNVVYCGAVGTGQAAKICNNMLLAISMIGTAEAMNLGIRLGLDPKLLAKILNMSSGRCWSSDTYNPVPGVMDGVPSANNYQGGFGTTLMAKDLGLAQDSATSTKSPILLGSLAHQIYRMMCAKGYSKKDFSSVFQFLREEETF
161	P30939	>sp|P30939|5HT1F_HUMAN 5-hydroxytryptamine receptor 1F GN=HTR1F PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MDFLNSSDQNLTSEELLNRMPSKILVSLTLSGLALMTTTINSLVIAAIIVTRKLHHPANYLICSLAVTDFLVAVLVMPFSIVYIVRESWIMGQVVCDIWLSVDITCCTCSILHLSAIALDRYRAITDAVEYARKRTPKHAGIMITIVWIISVFISMPPLFWRHQGTSRDDECIIKHDHIVSTIYSTFGAFYIPLALILILYYKIYRAAKTLYHKRQASRIAKEEVNGQVLLESGEKSTKSVSTSYVLEKSLSDPSTDFDKIHSTVRSLRSEFKHEKSWRRQKISGTRERKAATTLGLILGAFVICWLPFFVKELVVNVCDKCKISEEMSNFLAWLGYLNSLINPLIYTIFNEDFKKAFQKLVRCRC
162	P28223	>sp|P28223|5HT2A_HUMAN 5-hydroxytryptamine receptor 2A GN=HTR2A PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MDILCEENTSLSSTTNSLMQLNDDTRLYSNDFNSGEANTSDAFNWTVDSENRTNLSCEGCLSPSCLSLLHLQEKNWSALLTAVVIILTIAGNILVIMAVSLEKKLQNATNYFLMSLAIADMLLGFLVMPVSMLTILYGYRWPLPSKLCAVWIYLDVLFSTASIMHLCAISLDRYVAIQNPIHHSRFNSRTKAFLKIIAVWTISVGISMPIPVFGLQDDSKVFKEGSCLLADDNFVLIGSFVSFFIPLTIMVITYFLTIKSLQKEATLCVSDLGTRAKLASFSFLPQSSLSSEKLFQRSIHREPGSYTGRRTMQSISNEQKACKVLGIVFFLFVVMWCPFFITNIMAVICKESCNEDVIGALLNVFVWIGYLSSAVNPLVYTLFNKTYRSAFSRYIQCQYKENKKPLQLILVNTIPALAYKSSQLQMGQKKNSKQDAKTTDNDCSMVALGKQHSEEASKDNSDGVNEKVSCV
163	Q9BXI3	>sp|Q9BXI3|5NT1A_HUMAN Cytosolic 5'-nucleotidase 1A GN=NT5C1A PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MEPGQPREPQEPREPGPGAETAAAPVWEEAKIFYDNLAPKKKPKSPKPQNAVTIAVSSRALFRMDEEQQIYTEQGVEEYVRYQLEHENEPFSPGPAFPFVKALEAVNRRLRELYPDSEDVFDIVLMTNNHAQVGVRLINSINHYDLFIERFCMTGGNSPICYLKAYHTNLYLSADAEKVREAIDEGIAAATIFSPSRDVVVSQSQLRVAFDGDAVLFSDESERIVKAHGLDRFFEHEKAHENKPLAQGPLKGFLEALGRLQKKFYSKGLRLECPIRTYLVTARSAASSGARALKTLRSWGLETDEALFLAGAPKGPLLEKIRPHIFFDDQMFHVAGAQEMGTVAAHVPYGVAQTPRRTAPAKQAPSAQ
164	P05408	>sp|P05408|7B2_HUMAN Neuroendocrine protein 7B2 GN=SCG5 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MVSRMVSTMLSGLLFWLASGWTPAFAYSPRTPDRVSEADIQRLLHGVMEQLGIARPRVEYPAHQAMNLVGPQSIEGGAHEGLQHLGPFGNIPNIVAELTGDNIPKDFSEDQGYPDPPNPCPVGKTADDGCLENTPDTAEFSREFQLHQHLFDPEHDYPGLGKWNKKLLYEKMKGGERRKRRSVNPYLQGQRLDNVVAKKSVPHFSDEDKDPE
428	O14561	>sp|O14561|ACPM_HUMAN Acyl carrier protein, mitochondrial GN=NDUFAB1 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MASRVLSAYVSRLPAAFAPLPRVRMLAVARPLSTALCSAGTQTRLGTLQPALVLAQVPGRVTQLCRQYSDMPPLTLEGIQDRVLYVLKLYDKIDPEKLSVNSHFMKDLGLDSLDQVEIIMAMEDEFGFEIPDIDAEKLMCPQEIVDYIADKKDVYE
165	Q6PD74	>sp|Q6PD74|AAGAB_HUMAN Alpha- and gamma-adaptin-binding protein p34 GN=AAGAB PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAAGVPCALVTSCSSVFSGDQLVQHILGTEDLIVEVTSNDAVRFYPWTIDNKYYSADINLCVVPNKFLVTAEIAESVQAFVVYFDSTQKSGLDSVSSWLPLAKAWLPEVMILVCDRVSEDGINRQKAQEWCIKHGFELVELSPEELPEEDDDFPESTGVKRIVQALNANVWSNVVMKNDRNQGFSLLNSLTGTNHSIGSADPCHPEQPHLPAADSTESLSDHRGGASNTTDAQVDSIVDPMLDLDIQELASLTTGGGDVENFERLFSKLKEMKDKAATLPHEQRKVHAEKVAKAFWMAIGGDRDEIEGLSSDEEH
166	Q2M2I8	>sp|Q2M2I8|AAK1_HUMAN AP2-associated protein kinase 1 GN=AAK1 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MKKFFDSRREQGGSGLGSGSSGGGGSTSGLGSGYIGRVFGIGRQQVTVDEVLAEGGFAIVFLVRTSNGMKCALKRMFVNNEHDLQVCKREIQIMRDLSGHKNIVGYIDSSINNVSSGDVWEVLILMDFCRGGQVVNLMNQRLQTGFTENEVLQIFCDTCEAVARLHQCKTPIIHRDLKVENILLHDRGHYVLCDFGSATNKFQNPQTEGVNAVEDEIKKYTTLSYRAPEMVNLYSGKIITTKADIWALGCLLYKLCYFTLPFGESQVAICDGNFTIPDNSRYSQDMHCLIRYMLEPDPDKRPDIYQVSYFSFKLLKKECPIPNVQNSPIPAKLPEPVKASEAAAKKTQPKARLTDPIPTTETSIAPRQRPKAGQTQPNPGILPIQPALTPRKRATVQPPPQAAGSSNQPGLLASVPQPKPQAPPSQPLPQTQAKQPQAPPTPQQTPSTQAQGLPAQAQATPQHQQQLFLKQQQQQQQPPPAQQQPAGTFYQQQQAQTQQFQAVHPATQKPAIAQFPVVSQGGSQQQLMQNFYQQQQQQQQQQQQQQLATALHQQQLMTQQAALQQKPTMAAGQQPQPQPAAAPQPAPAQEPAIQAPVRQQPKVQTTPPPAVQGQKVGSLTPPSSPKTQRAGHRRILSDVTHSAVFGVPASKSTQLLQAAAAEASLNKSKSATTTPSGSPRTSQQNVYNPSEGSTWNPFDDDNFSKLTAEELLNKDFAKLGEGKHPEKLGGSAESLIPGFQSTQGDAFATTSFSAGTAEKRKGGQTVDSGLPLLSVSDPFIPLQVPDAPEKLIEGLKSPDTSLLLPDLLPMTDPFGSTSDAVIEKADVAVESLIPGLEPPVPQRLPSQTESVTSNRTDSLTGEDSLLDCSLLSNPTTDLLEEFAPTAISAPVHKAAEDSNLISGFDVPEGSDKVAEDEFDPIPVLITKNPQGGHSRNSSGSSESSLPNLARSLLLVDQLIDL
167	Q9Y478	>sp|Q9Y478|AAKB1_HUMAN 5'-AMP-activated protein kinase subunit beta-1 GN=PRKAB1 PE=1 SV=4 Homo sapiens OS=Human NCBI_TaxID=9606	MGNTSSERAALERHGGHKTPRRDSSGGTKDGDRPKILMDSPEDADLFHSEEIKAPEKEEFLAWQHDLEVNDKAPAQARPTVFRWTGGGKEVYLSGSFNNWSKLPLTRSHNNFVAILDLPEGEHQYKFFVDGQWTHDPSEPIVTSQLGTVNNIIQVKKTDFEVFDALMVDSQKCSDVSELSSSPPGPYHQEPYVCKPEERFRAPPILPPHLLQVILNKDTGISCDPALLPEPNHVMLNHLYALSIKDGVMVLSATHRYKKKYVTTLLYKPI
168	P54619	>sp|P54619|AAKG1_HUMAN 5'-AMP-activated protein kinase subunit gamma-1 GN=PRKAG1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	METVISSDSSPAVENEHPQETPESNNSVYTSFMKSHRCYDLIPTSSKLVVFDTSLQVKKAFFALVTNGVRAAPLWDSKKQSFVGMLTITDFINILHRYYKSALVQIYELEEHKIETWREVYLQDSFKPLVCISPNASLFDAVSSLIRNKIHRLPVIDPESGNTLYILTHKRILKFLKLFITEFPKPEFMSKSLEELQIGTYANIAMVRTTTPVYVALGIFVQHRVSALPVVDEKGRVVDIYSKFDVINLAAEKTYNNLDVSVTKALQHRSHYFEGVLKCYLHETLETIINRLVEAEVHRLVVVDENDVVKGIVSLSDILQALVLTGGEKKP
169	Q9UGI9	>sp|Q9UGI9|AAKG3_HUMAN 5'-AMP-activated protein kinase subunit gamma-3 GN=PRKAG3 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MEPGLEHALRRTPSWSSLGGSEHQEMSFLEQENSSSWPSPAVTSSSERIRGKRRAKALRWTRQKSVEEGEPPGQGEGPRSRPAAESTGLEATFPKTTPLAQADPAGVGTPPTGWDCLPSDCTASAAGSSTDDVELATEFPATEAWECELEGLLEERPALCLSPQAPFPKLGWDDELRKPGAQIYMRFMQEHTCYDAMATSSKLVIFDTMLEIKKAFFALVANGVRAAPLWDSKKQSFVGMLTITDFILVLHRYYRSPLVQIYEIEQHKIETWREIYLQGCFKPLVSISPNDSLFEAVYTLIKNRIHRLPVLDPVSGNVLHILTHKRLLKFLHIFGSLLPRPSFLYRTIQDLGIGTFRDLAVVLETAPILTALDIFVDRRVSALPVVNECGQVVGLYSRFDVIHLAAQQTYNHLDMSVGEALRQRTLCLEGVLSCQPHESLGEVIDRIAREQVHRLVLVDETQHLLGVVSLSDILQALVLSPAGIDALGA
170	Q96AK3	>sp|Q96AK3|ABC3D_HUMAN DNA dC->dU-editing enzyme APOBEC-3D GN=APOBEC3D PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MNPQIRNPMERMYRDTFYDNFENEPILYGRSYTWLCYEVKIKRGRSNLLWDTGVFRGPVLPKRQSNHRQEVYFRFENHAEMCFLSWFCGNRLPANRRFQITWFVSWNPCLPCVVKVTKFLAEHPNVTLTISAARLYYYRDRDWRWVLLRLHKAGARVKIMDYEDFAYCWENFVCNEGQPFMPWYKFDDNYASLHRTLKEILRNPMEAMYPHIFYFHFKNLLKACGRNESWLCFTMEVTKHHSAVFRKRGVFRNQVDPETHCHAERCFLSWFCDDILSPNTNYEVTWYTSWSPCPECAGEVAEFLARHSNVNLTIFTARLCYFWDTDYQEGLCSLSQEGASVKIMGYKDFVSCWKNFVYSDDEPFKPWKGLQTNFRLLKRRLREILQ
171	Q99758	>sp|Q99758|ABCA3_HUMAN ATP-binding cassette sub-family A member 3 GN=ABCA3 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAVLRQLALLLWKNYTLQKRKVLVTVLELFLPLLFSGILIWLRLKIQSENVPNATIYPGQSIQELPLFFTFPPPGDTWELAYIPSHSDAAKTVTETVRRALVINMRVRGFPSEKDFEDYIRYDNCSSSVLAAVVFEHPFNHSKEPLPLAVKYHLRFSYTRRNYMWTQTGSFFLKETEGWHTTSLFPLFPNPGPREPTSPDGGEPGYIREGFLAVQHAVDRAIMEYHADAATRQLFQRLTVTIKRFPYPPFIADPFLVAIQYQLPLLLLLSFTYTALTIARAVVQEKERRLKEYMRMMGLSSWLHWSAWFLLFFLFLLIAASFMTLLFCVKVKPNVAVLSRSDPSLVLAFLLCFAISTISFSFMVSTFFSKANMAAAFGGFLYFFTYIPYFFVAPRYNWMTLSQKLCSCLLSNVAMAMGAQLIGKFEAKGMGIQWRDLLSPVNVDDDFCFGQVLGMLLLDSVLYGLVTWYMEAVFPGQFGVPQPWYFFIMPSYWCGKPRAVAGKEEEDSDPEKALRNEYFEAEPEDLVAGIKIKHLSKVFRVGNKDRAAVRDLNLNLYEGQITVLLGHNGAGKTTTLSMLTGLFPPTSGRAYISGYEISQDMVQIRKSLGLCPQHDILFDNLTVAEHLYFYAQLKGLSRQKCPEEVKQMLHIIGLEDKWNSRSRFLSGGMRRKLSIGIALIAGSKVLILDEPTSGMDAISRRAIWDLLQRQKSDRTIVLTTHFMDEADLLGDRIAIMAKGELQCCGSSLFLKQKYGAGYHMTLVKEPHCNPEDISQLVHHHVPNATLESSAGAELSFILPRESTHRFEGLFAKLEKKQKELGIASFGASITTMEEVFLRVGKLVDSSMDIQAIQLPALQYQHERRASDWAVDSNLCGAMDPSDGIGALIEEERTAVKLNTGLALHCQQFWAMFLKKAAYSWREWKMVAAQVLVPLTCVTLALLAINYSSELFDDPMLRLTLGEYGRTVVPFSVPGTSQLGQQLSEHLKDALQAEGQEPREVLGDLEEFLIFRASVEGGGFNERCLVAASFRDVGERTVVNALFNNQAYHSPATALAVVDNLLFKLLCGPHASIVVSNFPQPRSALQAAKDQFNEGRKGFDIALNLLFAMAFLASTFSILAVSERAVQAKHVQFVSGVHVASFWLSALLWDLISFLIPSLLLLVVFKAFDVRAFTRDGHMADTLLLLLLYGWAIIPLMYLMNFFFLGAATAYTRLTIFNILSGIATFLMVTIMRIPAVKLEELSKTLDHVFLVLPNHCLGMAVSSFYENYETRRYCTSSEVAAHYCKKYNIQYQENFYAWSAPGVGRFVASMAASGCAYLILLFLIETNLLQRLRGILCALRRRRTLTELYTRMPVLPEDQDVADERTRILAPSPDSLLHTPLIIKELSKVYEQRVPLLAVDRLSLAVQKGECFGLLGFNGAGKTTTFKMLTGEESLTSGDAFVGGHRISSDVGKVRQRIGYCPQFDALLDHMTGREMLVMYARLRGIPERHIGACVENTLRGLLLEPHANKLVRTYSGGNKRKLSTGIALIGEPAVIFLDEPSTGMDPVARRLLWDTVARARESGKAIIITSHSMEECEALCTRLAIMVQGQFKCLGSPQHLKSKFGSGYSLRAKVQSEGQQEALEEFKAFVDLTFPGSVLEDEHQGMVHYHLPGRDLSWAKVFGILEKAKEKYGVDDYSVSQISLEQVFLSFAHLQPPTAEEGR
172	O75027	>sp|O75027|ABCB7_HUMAN ATP-binding cassette sub-family B member 7, mitochondrial GN=ABCB7 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MALLAMHSWRWAAAAAAFEKRRHSAILIRPLVSVSGSGPQWRPHQLGALGTARAYQIPESLKSITWQRLGKGNSGQFLDAAKALQVWPLIEKRTCWHGHAGGGLHTDPKEGLKDVDTRKIIKAMLSYVWPKDRPDLRARVAISLGFLGGAKAMNIVVPFMFKYAVDSLNQMSGNMLNLSDAPNTVATMATAVLIGYGVSRAGAAFFNEVRNAVFGKVAQNSIRRIAKNVFLHLHNLDLGFHLSRQTGALSKAIDRGTRGISFVLSALVFNLLPIMFEVMLVSGVLYYKCGAQFALVTLGTLGTYTAFTVAVTRWRTRFRIEMNKADNDAGNAAIDSLLNYETVKYFNNERYEAQRYDGFLKTYETASLKSTSTLAMLNFGQSAIFSVGLTAIMVLASQGIVAGTLTVGDLVMVNGLLFQLSLPLNFLGTVYRETRQALIDMNTLFTLLKVDTQIKDKVMASPLQITPQTATVAFDNVHFEYIEGQKVLSGISFEVPAGKKVAIVGGSGSGKSTIVRLLFRFYEPQKGSIYLAGQNIQDVSLESLRRAVGVVPQDAVLFHNTIYYNLLYGNISASPEEVYAVAKLAGLHDAILRMPHGYDTQVGERGLKLSGGEKQRVAIARAILKDPPVILYDEATSSLDSITEETILGAMKDVVKHRTSIFIAHRLSTVVDADEIIVLDQGKVAERGTHHGLLANPHSIYSEMWHTQSSRVQNHDNPKWEAKKENISKEEERKKLQEEIVNSVKGCGNCSC
183	P30926	>sp|P30926|ACHB4_HUMAN Neuronal acetylcholine receptor subunit beta-4 GN=CHRNB4 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MRRAPSLVLFFLVALCGRGNCRVANAEEKLMDDLLNKTRYNNLIRPATSSSQLISIKLQLSLAQLISVNEREQIMTTNVWLKQEWTDYRLTWNSSRYEGVNILRIPAKRIWLPDIVLYNNADGTYEVSVYTNLIVRSNGSVLWLPPAIYKSACKIEVKYFPFDQQNCTLKFRSWTYDHTEIDMVLMTPTASMDDFTPSGEWDIVALPGRRTVNPQDPSYVDVTYDFIIKRKPLFYTINLIIPCVLTTLLAILVFYLPSDCGEKMTLCISVLLALTFFLLLISKIVPPTSLDVPLIGKYLMFTMVLVTFSIVTSVCVLNVHHRSPSTHTMAPWVKRCFLHKLPTFLFMKRPGPDSSPARAFPPSKSCVTKPEATATSTSPSNFYGNSMYFVNPASAASKSPAGSTPVAIPRDFWLRSSGRFRQDVQEALEGVSFIAQHMKNDDEDQSVVEDWKYVAMVVDRLFLWVFMFVCVLGTVGLFLPPLFQTHAASEGPYAAQRD
195	P16189	>sp|P16189|1A31_HUMAN HLA class I histocompatibility antigen, A-31 alpha chain GN=HLA-A PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMAPRTLLLLLLGALALTQTWAGSHSMRYFTTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQERPEYWDQETRNVKAHSQIDRVDLGTLRGYYNQSEAGSHTIQMMYGCDVGSDGRFLRGYQQDAYDGKDYIALNEDLRSWTAADMAAQITQRKWEAARVAEQLRAYLEGTCVEWLRRYLENGKETLQRTDPPKTHMTHHAVSDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWASVVVPSGQEQRYTCHVQHEGLPKPLTLRWEPSSQPTIPIVGIIAGLVLFGAVFAGAVVAAVRWRRKSSDRKGGSYSQAASSDSAQGSDMSLTACKV
173	Q09428	>sp|Q09428|ABCC8_HUMAN ATP-binding cassette sub-family C member 8 GN=ABCC8 PE=1 SV=6 Homo sapiens OS=Human NCBI_TaxID=9606	MPLAFCGSENHSAAYRVDQGVLNNGCFVDALNVVPHVFLLFITFPILFIGWGSQSSKVHIHHSTWLHFPGHNLRWILTFMLLFVLVCEIAEGILSDGVTESHHLHLYMPAGMAFMAAVTSVVYYHNIETSNFPKLLIALLVYWTLAFITKTIKFVKFLDHAIGFSQLRFCLTGLLVILYGMLLLVEVNVIRVRRYIFFKTPREVKPPEDLQDLGVRFLQPFVNLLSKGTYWWMNAFIKTAHKKPIDLRAIGKLPIAMRALTNYQRLCEAFDAQVRKDIQGTQGARAIWQALSHAFGRRLVLSSTFRILADLLGFAGPLCIFGIVDHLGKENDVFQPKTQFLGVYFVSSQEFLANAYVLAVLLFLALLLQRTFLQASYYVAIETGINLRGAIQTKIYNKIMHLSTSNLSMGEMTAGQICNLVAIDTNQLMWFFFLCPNLWAMPVQIIVGVILLYYILGVSALIGAAVIILLAPVQYFVATKLSQAQRSTLEYSNERLKQTNEMLRGIKLLKLYAWENIFRTRVETTRRKEMTSLRAFAIYTSISIFMNTAIPIAAVLITFVGHVSFFKEADFSPSVAFASLSLFHILVTPLFLLSSVVRSTVKALVSVQKLSEFLSSAEIREEQCAPHEPTPQGPASKYQAVPLRVVNRKRPAREDCRGLTGPLQSLVPSADGDADNCCVQIMGGYFTWTPDGIPTLSNITIRIPRGQLTMIVGQVGCGKSSLLLAALGEMQKVSGAVFWSSLPDSEIGEDPSPERETATDLDIRKRGPVAYASQKPWLLNATVEENIIFESPFNKQRYKMVIEACSLQPDIDILPHGDQTQIGERGINLSGGQRQRISVARALYQHANVVFLDDPFSALDIHLSDHLMQAGILELLRDDKRTVVLVTHKLQYLPHADWIIAMKDGTIQREGTLKDFQRSECQLFEHWKTLMNRQDQELEKETVTERKATEPPQGLSRAMSSRDGLLQDEEEEEEEAAESEEDDNLSSMLHQRAEIPWRACAKYLSSAGILLLSLLVFSQLLKHMVLVAIDYWLAKWTDSALTLTPAARNCSLSQECTLDQTVYAMVFTVLCSLGIVLCLVTSVTVEWTGLKVAKRLHRSLLNRIILAPMRFFETTPLGSILNRFSSDCNTIDQHIPSTLECLSRSTLLCVSALAVISYVTPVFLVALLPLAIVCYFIQKYFRVASRDLQQLDDTTQLPLLSHFAETVEGLTTIRAFRYEARFQQKLLEYTDSNNIASLFLTAANRWLEVRMEYIGACVVLIAAVTSISNSLHRELSAGLVGLGLTYALMVSNYLNWMVRNLADMELQLGAVKRIHGLLKTEAESYEGLLAPSLIPKNWPDQGKIQIQNLSVRYDSSLKPVLKHVNALIAPGQKIGICGRTGSGKSSFSLAFFRMVDTFEGHIIIDGIDIAKLPLHTLRSRLSIILQDPVLFSGTIRFNLDPERKCSDSTLWEALEIAQLKLVVKALPGGLDAIITEGGENFSQGQRQLFCLARAFVRKTSIFIMDEATASIDMATENILQKVVMTAFADRTVVTIAHRVHTILSADLVIVLKRGAILEFDKPEKLLSRKDSVFASFVRADK
174	P08910	>sp|P08910|ABHD2_HUMAN Monoacylglycerol lipase ABHD2 GN=ABHD2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MNAMLETPELPAVFDGVKLAAVAAVLYVIVRCLNLKSPTAPPDLYFQDSGLSRFLLKSCPLLTKEYIPPLIWGKSGHIQTALYGKMGRVRSPHPYGHRKFITMSDGATSTFDLFEPLAEHCVGDDITMVICPGIANHSEKQYIRTFVDYAQKNGYRCAVLNHLGALPNIELTSPRMFTYGCTWEFGAMVNYIKKTYPLTQLVVVGFSLGGNIVCKYLGETQANQEKVLCCVSVCQGYSALRAQETFMQWDQCRRFYNFLMADNMKKIILSHRQALFGDHVKKPQSLEDTDLSRLYTATSLMQIDDNVMRKFHGYNSLKEYYEEESCMRYLHRIYVPLMLVNAADDPLVHESLLTIPKSLSEKRENVMFVLPLHGGHLGFFEGSVLFPEPLTWMDKLVVEYANAICQWERNKLQCSDTEQVEADLE
175	Q8WTS1	>sp|Q8WTS1|ABHD5_HUMAN 1-acylglycerol-3-phosphate O-acyltransferase ABHD5 GN=ABHD5 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAAEEEEVDSADTGERSGWLTGWLPTWCPTSISHLKEAEEKMLKCVPCTYKKEPVRISNGNKIWTLKFSHNISNKTPLVLLHGFGGGLGLWALNFGDLCTNRPVYAFDLLGFGRSSRPRFDSDAEEVENQFVESIEEWRCALGLDKMILLGHNLGGFLAAAYSLKYPSRVNHLILVEPWGFPERPDLADQDRPIPVWIRALGAALTPFNPLAGLRIAGPFGLSLVQRLRPDFKRKYSSMFEDDTVTEYIYHCNVQTPSGETAFKNMTIPYGWAKRPMLQRIGKMHPDIPVSVIFGARSCIDGNSGTSIQSLRPHSYVKTIAILGAGHYVYADQPEEFNQKVKEICDTVD
176	Q9BUJ0	>sp|Q9BUJ0|ABHEA_HUMAN Protein ABHD14A GN=ABHD14A PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MVGALCGCWFRLGGARPLIPLGPTVVQTSMSRSQVALLGLSLLLMLLLYVGLPGPPEQTSCLWGDPNVTVLAGLTPGNSPIFYREVLPLNQAHRVEVVLLHGKAFNSHTWEQLGTLQLLSQRGYRAVALDLPGFGNSAPSKEASTEAGRAALLERALRDLEVQNAVLVSPSLSGHYALPFLMRGHHQLHGFVPIAPTSTQNYTQEQFWAVKTPTLILYGELDHILARESLRQLRHLPNHSVVKLRNAGHACYLHKPQDFHLVLLAFLDHLP
177	Q96IU4	>sp|Q96IU4|ABHEB_HUMAN Protein ABHD14B GN=ABHD14B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAASVEQREGTIQVQGQALFFREALPGSGQARFSVLLLHGIRFSSETWQNLGTLHRLAQAGYRAVAIDLPGLGHSKEAAAPAPIGELAPGSFLAAVVDALELGPPVVISPSLSGMYSLPFLTAPGSQLPGFVPVAPICTDKINAANYASVKTPALIVYGDQDPMGQTSFEHLKQLPNHRVLIMKGAGHPCYLDKPEEWHTGLLDFLQGLQ
178	P42684	>sp|P42684|ABL2_HUMAN Abelson tyrosine-protein kinase 2 GN=ABL2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MGQQVGRVGEAPGLQQPQPRGIRGSSAARPSGRRRDPAGRTTETGFNIFTQHDHFASCVEDGFEGDKTGGSSPEALHRPYGCDVEPQALNEAIRWSSKENLLGATESDPNLFVALYDFVASGDNTLSITKGEKLRVLGYNQNGEWSEVRSKNGQGWVPSNYITPVNSLEKHSWYHGPVSRSAAEYLLSSLINGSFLVRESESSPGQLSISLRYEGRVYHYRINTTADGKVYVTAESRFSTLAELVHHHSTVADGLVTTLHYPAPKCNKPTVYGVSPIHDKWEMERTDITMKHKLGGGQYGEVYVGVWKKYSLTVAVKTLKEDTMEVEEFLKEAAVMKEIKHPNLVQLLGVCTLEPPFYIVTEYMPYGNLLDYLRECNREEVTAVVLLYMATQISSAMEYLEKKNFIHRDLAARNCLVGENHVVKVADFGLSRLMTGDTYTAHAGAKFPIKWTAPESLAYNTFSIKSDVWAFGVLLWEIATYGMSPYPGIDLSQVYDLLEKGYRMEQPEGCPPKVYELMRACWKWSPADRPSFAETHQAFETMFHDSSISEEVAEELGRAASSSSVVPYLPRLPILPSKTRTLKKQVENKENIEGAQDATENSASSLAPGFIRGAQASSGSPALPRKQRDKSPSSLLEDAKETCFTRDRKGGFFSSFMKKRNAPTPPKRSSSFREMENQPHKKYELTGNFSSVASLQHADGFSFTPAQQEANLVPPKCYGGSFAQRNLCNDDGGGGGGSGTAGGGWSGITGFFTPRLIKKTLGLRAGKPTASDDTSKPFPRSNSTSSMSSGLPEQDRMAMTLPRNCQRSKLQLERTVSTSSQPEENVDRANDMLPKKSEESAAPSRERPKAKLLPRGATALPLRTPSGDLAITEKDPPGVGVAGVAAAPKGKEKNGGARLGMAGVPEDGEQPGWPSPAKAAPVLPTTHNHKVPVLISPTLKHTPADVQLIGTDSQGNKFKLLSEHQVTSSGDKDRPRRVKPKCAPPPPPVMRLLQHPSICSDPTEEPTALTAGQSTSETQEGGKKAALGAVPISGKAGRPVMPPPQVPLPTSSISPAKMANGTAGTKVALRKTKQAAEKISADKISKEALLECADLLSSALTEPVPNSQLVDTGHQLLDYCSGYVDCIPQTRNKFAFREAVSKLELSLQELQVSSAAAGVPGTNPVLNNLLSCVQEISDVVQR
179	Q9ULW3	>sp|Q9ULW3|ABT1_HUMAN Activator of basal transcription 1 GN=ABT1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MEAEESEKAATEQEPLEGTEQTLDAEEEQEESEEAACGSKKRVVPGIVYLGHIPPRFRPLHVRNLLSAYGEVGRVFFQAEDRFVRRKKKAAAAAGGKKRSYTKDYTEGWVEFRDKRIAKRVAASLHNTPMGARRRSPFRYDLWNLKYLHRFTWSHLSEHLAFERQVRRQRLRAEVAQAKRETDFYLQSVERGQRFLAADGDPARPDGSWTFAQRPTEQELRARKAARPGGRERARLATAQDKARSNKGLLARIFGAPPPSESMEGPSLVRDS
180	Q9BYF1	>sp|Q9BYF1|ACE2_HUMAN Angiotensin-converting enzyme 2 GN=ACE2 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MSSSSWLLLSLVAVTAAQSTIEEQAKTFLDKFNHEAEDLFYQSSLASWNYNTNITEENVQNMNNAGDKWSAFLKEQSTLAQMYPLQEIQNLTVKLQLQALQQNGSSVLSEDKSKRLNTILNTMSTIYSTGKVCNPDNPQECLLLEPGLNEIMANSLDYNERLWAWESWRSEVGKQLRPLYEEYVVLKNEMARANHYEDYGDYWRGDYEVNGVDGYDYSRGQLIEDVEHTFEEIKPLYEHLHAYVRAKLMNAYPSYISPIGCLPAHLLGDMWGRFWTNLYSLTVPFGQKPNIDVTDAMVDQAWDAQRIFKEAEKFFVSVGLPNMTQGFWENSMLTDPGNVQKAVCHPTAWDLGKGDFRILMCTKVTMDDFLTAHHEMGHIQYDMAYAAQPFLLRNGANEGFHEAVGEIMSLSAATPKHLKSIGLLSPDFQEDNETEINFLLKQALTIVGTLPFTYMLEKWRWMVFKGEIPKDQWMKKWWEMKREIVGVVEPVPHDETYCDPASLFHVSNDYSFIRYYTRTLYQFQFQEALCQAAKHEGPLHKCDISNSTEAGQKLFNMLRLGKSEPWTLALENVVGAKNMNVRPLLNYFEPLFTWLKDQNKNSFVGWSTDWSPYADQSIKVRISLKSALGDKAYEWNDNEMYLFRSSVAYAMRQYFLKVKNQMILFGEEDVRVANLKPRISFNFFVTAPKNVSDIIPRTEVEKAIRMSRSRINDAFRLNDNSLEFLGIQPTLGPPNQPPVSIWLIVFGVVMGVIVVGIVILIFTGIRDRKKKNKARSGENPYASIDISKGENNPGFQNTDDVQTSF
181	P32297	>sp|P32297|ACHA3_HUMAN Neuronal acetylcholine receptor subunit alpha-3 GN=CHRNA3 PE=1 SV=4 Homo sapiens OS=Human NCBI_TaxID=9606	MGSGPLSLPLALSPPRLLLLLLLSLLPVARASEAEHRLFERLFEDYNEIIRPVANVSDPVIIHFEVSMSQLVKVDEVNQIMETNLWLKQIWNDYKLKWNPSDYGGAEFMRVPAQKIWKPDIVLYNNAVGDFQVDDKTKALLKYTGEVTWIPPAIFKSSCKIDVTYFPFDYQNCTMKFGSWSYDKAKIDLVLIGSSMNLKDYWESGEWAIIKAPGYKHDIKYNCCEEIYPDITYSLYIRRLPLFYTINLIIPCLLISFLTVLVFYLPSDCGEKVTLCISVLLSLTVFLLVITETIPSTSLVIPLIGEYLLFTMIFVTLSIVITVFVLNVHYRTPTTHTMPSWVKTVFLNLLPRVMFMTRPTSNEGNAQKPRPLYGAELSNLNCFSRAESKGCKEGYPCQDGMCGYCHHRRIKISNFSANLTRSSSSESVDAVLSLSALSPEIKEAIQSVKYIAENMKAQNEAKEIQDDWKYVAMVIDRIFLWVFTLVCILGTAGLFLQPLMAREDA
182	Q05901	>sp|Q05901|ACHB3_HUMAN Neuronal acetylcholine receptor subunit beta-3 GN=CHRNB3 PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MLPDFMLVLIVLGIPSSATTGFNSIAENEDALLRHLFQGYQKWVRPVLHSNDTIKVYFGLKISQLVDVDEKNQLMTTNVWLKQEWTDHKLRWNPDDYGGIHSIKVPSESLWLPDIVLFENADGRFEGSLMTKVIVKSNGTVVWTPPASYKSSCTMDVTFFPFDRQNCSMKFGSWTYDGTMVDLILINENVDRKDFFDNGEWEILNAKGMKGNRRDGVYSYPFITYSFVLRRLPLFYTLFLIIPCLGLSFLTVLVFYLPSDEGEKLSLSTSVLVSLTVFLLVIEEIIPSSSKVIPLIGEYLLFIMIFVTLSIIVTVFVINVHHRSSSTYHPMAPWVKRLFLQKLPKLLCMKDHVDRYSSPEKEESQPVVKGKVLEKKKQKQLSDGEKVLVAFLEKAADSIRYISRHVKKEHFISQVVQDWKFVAQVLDRIFLWLFLIVSVTGSVLIFTPALKMWLHSYH
222	Q5T5F5	>sp|Q5T5F5|A4AS1_HUMAN Uncharacterized protein ADAMTSL4-AS1 GN=ADAMTSL4-AS1 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MWLWQDIQCCPAPPSAPPRALEPGRAPPPPGEGLGAGIPSLSPPQKKPQSVGICVRQKGRQKAGLEKGNRKKELRQANCPSLRPQRKGADTRRLPRETRPTKKRTAAAQPFLQLWNPAPHTSNGRTGDL
184	Q9UKV3	>sp|Q9UKV3|ACINU_HUMAN Apoptotic chromatin condensation inducer in the nucleus GN=ACIN1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MWRRKHPRTSGGTRGVLSGNRGVEYGSGRGHLGTFEGRWRKLPKMPEAVGTDPSTSRKMAELEEVTLDGKPLQALRVTDLKAALEQRGLAKSGQKSALVKRLKGALMLENLQKHSTPHAAFQPNSQIGEEMSQNSFIKQYLEKQQELLRQRLEREAREAAELEEASAESEDEMIHPEGVASLLPPDFQSSLERPELELSRHSPRKSSSISEEKGDSDDEKPRKGERRSSRVRQARAAKLSEGSQPAEEEEDQETPSRNLRVRADRNLKTEEEEEEEEEEEEDDEEEEGDDEGQKSREAPILKEFKEEGEEIPRVKPEEMMDERPKTRSQEQEVLERGGRFTRSQEEARKSHLARQQQEKEMKTTSPLEEEEREIKSSQGLKEKSKSPSPPRLTEDRKKASLVALPEQTASEEETPPPLLTKEASSPPPHPQLHSEEEIEPMEGPAPAVLIQLSPPNTDADTRELLVSQHTVQLVGGLSPLSSPSDTKAESPAEKVPEESVLPLVQKSTLADYSAQKDLEPESDRSAQPLPLKIEELALAKGITEECLKQPSLEQKEGRRASHTLLPSHRLKQSADSSSSRSSSSSSSSSRSRSRSPDSSGSRSHSPLRSKQRDVAQARTHANPRGRPKMGSRSTSESRSRSRSRSRSASSNSRKSLSPGVSRDSSTSYTETKDPSSGQEVATPPVPQLQVCEPKERTSTSSSSVQARRLSQPESAEKHVTQRLQPERGSPKKCEAEEAEPPAATQPQTSETQTSHLPESERIHHTVEEKEEVTMDTSENRPENDVPEPPMPIADQVSNDDRPEGSVEDEEKKESSLPKSFKRKISVVSATKGVPAGNSDTEGGQPGRKRRWGASTATTQKKPSISITTESLKSLIPDIKPLAGQEAVVDLHADDSRISEDETERNGDDGTHDKGLKICRTVTQVVPAEGQENGQREEEEEEKEPEAEPPVPPQVSVEVALPPPAEHEVKKVTLGDTLTRRSISQQKSGVSITIDDPVRTAQVPSPPRGKISNIVHISNLVRPFTLGQLKELLGRTGTLVEEAFWIDKIKSHCFVTYSTVEEAVATRTALHGVKWPQSNPKFLCADYAEQDELDYHRGLLVDRPSETKTEEQGIPRPLHPPPPPPVQPPQHPRAEQREQERAVREQWAEREREMERRERTRSEREWDRDKVREGPRSRSRSRDRRRKERAKSKEKKSEKKEKAQEEPPAKLLDDLFRKTKAAPCIYWLPLTDSQIVQKEAERAERAKEREKRRKEQEEEEQKEREKEAERERNRQLEREKRREHSRERDRERERERERDRGDRDRDRERDRERGRERDRRDTKRHSRSRSRSTPVRDRGGRR
185	Q07912	>sp|Q07912|ACK1_HUMAN Activated CDC42 kinase 1 GN=TNK2 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MQPEEGTGWLLELLSEVQLQQYFLRLRDDLNVTRLSHFEYVKNEDLEKIGMGRPGQRRLWEAVKRRKALCKRKSWMSKVFSGKRLEAEFPPHHSQSTFRKTSPAPGGPAGEGPLQSLTCLIGEKDLRLLEKLGDGSFGVVRRGEWDAPSGKTVSVAVKCLKPDVLSQPEAMDDFIREVNAMHSLDHRNLIRLYGVVLTPPMKMVTELAPLGSLLDRLRKHQGHFLLGTLSRYAVQVAEGMGYLESKRFIHRDLAARNLLLATRDLVKIGDFGLMRALPQNDDHYVMQEHRKVPFAWCAPESLKTRTFSHASDTWMFGVTLWEMFTYGQEPWIGLNGSQILHKIDKEGERLPRPEDCPQDIYNVMVQCWAHKPEDRPTFVALRDFLLEAQPTDMRALQDFEEPDKLHIQMNDVITVIEGRAENYWWRGQNTRTLCVGPFPRNVVTSVAGLSAQDISQPLQNSFIHTGHGDSDPRHCWGFPDRIDELYLGNPMDPPDLLSVELSTSRPPQHLGGVKKPTYDPVSEDQDPLSSDFKRLGLRKPGLPRGLWLAKPSARVPGTKASRGSGAEVTLIDFGEEPVVPALRPCAPSLAQLAMDACSLLDETPPQSPTRALPRPLHPTPVVDWDARPLPPPPAYDDVAQDEDDFEICSINSTLVGAGVPAGPSQGQTNYAFVPEQARPPPPLEDNLFLPPQGGGKPPSSAQTAEIFQALQQECMRQLQAPAGSPAPSPSPGGDDKPQVPPRVPIPPRPTRPHVQLSPAPPGEEETSQWPGPASPPRVPPREPLSPQGSRTPSPLVPPGSSPLPPRLSSSPGKTMPTTQSFASDPKYATPQVIQAPGPRAGPCILPIVRDGKKVSSTHYYLLPERPSYLERYQRFLREAQSPEEPTPLPVPLLLPPPSTPAPAAPTATVRPMPQAALDPKANFSTNNSNPGARPPPPRATARLPQRGCPGDGPEAGRPADKIQMAMVHGVTTEECQAALQCHGWSVQRAAQYLKVEQLFGLGLRPRGECHKVLEMFDWNLEQAGCHLLGSWGPAHHKR
186	Q16570	>sp|Q16570|ACKR1_HUMAN Atypical chemokine receptor 1 GN=ACKR1 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MGNCLHRAELSPSTENSSQLDFEDVWNSSYGVNDSFPDGDYGANLEAAAPCHSCNLLDDSALPFFILTSVLGILASSTVLFMLFRPLFRWQLCPGWPVLAQLAVGSALFSIVVPVLAPGLGSTRSSALCSLGYCVWYGSAFAQALLLGCHASLGHRLGAGQVPGLTLGLTVGIWGVAALLTLPVTLASGASGGLCTLIYSTELKALQATHTVACLAIFVLLPLGLFGAKGLKKALGMGPGPWMNILWAWFIFWWPHGVVLGLDFLVRSKLLLLSTCLAQQALDLLLNLAEALAILHCVATPLLLALFCHQATRTLLPSLPLPEGWSSHLDTLGSKS
187	P20309	>sp|P20309|ACM3_HUMAN Muscarinic acetylcholine receptor M3 GN=CHRM3 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MTLHNNSTTSPLFPNISSSWIHSPSDAGLPPGTVTHFGSYNVSRAAGNFSSPDGTTDDPLGGHTVWQVVFIAFLTGILALVTIIGNILVIVSFKVNKQLKTVNNYFLLSLACADLIIGVISMNLFTTYIIMNRWALGNLACDLWLAIDYVASNASVMNLLVISFDRYFSITRPLTYRAKRTTKRAGVMIGLAWVISFVLWAPAILFWQYFVGKRTVPPGECFIQFLSEPTITFGTAIAAFYMPVTIMTILYWRIYKETEKRTKELAGLQASGTEAETENFVHPTGSSRSCSSYELQQQSMKRSNRRKYGRCHFWFTTKSWKPSSEQMDQDHSSSDSWNNNDAAASLENSASSDEEDIGSETRAIYSIVLKLPGHSTILNSTKLPSSDNLQVPEEELGMVDLERKADKLQAQKSVDDGGSFPKSFSKLPIQLESAVDTAKTSDVNSSVGKSTATLPLSFKEATLAKRFALKTRSQITKRKRMSLVKEKKAAQTLSAILLAFIITWTPYNIMVLVNTFCDSCIPKTFWNLGYWLCYINSTVNPVCYALCNKTFRTTFKMLLLCQCDKKKRRKQQYQQRQSVIFHKRAPEQAL
188	Q8WXI4	>sp|Q8WXI4|ACO11_HUMAN Acyl-coenzyme A thioesterase 11 GN=ACOT11 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MIQNVGNHLRRGLASVFSNRTSRKSALRAGNDSAMADGEGYRNPTEVQMSQLVLPCHTNQRGELSVGQLLKWIDTTACLSAERHAGCPCVTASMDDIYFEHTISVGQVVNIKAKVNRAFNSSMEVGIQVASEDLCSEKQWNVCKALATFVARREITKVKLKQITPRTEEEKMEHSVAAERRRMRLVYADTIKDLLANCAIQGDLESRDCSRMVPAEKTRVESVELVLPPHANHQGNTFGGQIMAWMENVATIAASRLCRAHPTLKAIEMFHFRGPSQVGDRLVLKAIVNNAFKHSMEVGVCVEAYRQEAETHRRHINSAFMTFVVLDADDQPQLLPWIRPQPGDGERRYREASARKKIRLDRKYIVSCKQTEVPLSVPWDPSNQVYLSYNNVSSLKMLVAKDNWVLSSEISQVRLYTLEDDKFLSFHMEMVVHVDAAQAFLLLSDLRQRPEWDKHYRSVELVQQVDEDDAIYHVTSPALGGHTKPQDFVILASRRKPCDNGDPYVIALRSVTLPTHRETPEYRRGETLCSGFCLWREGDQLTKCCWVRVSLTELVSASGFYSWGLESRSKGRRSDGWNGKLAGGHLSTLKAIPVAKINSRFGYLQDT
189	Q8N1Q8	>sp|Q8N1Q8|ACO15_HUMAN Acyl-coenzyme A thioesterase THEM5 GN=THEM5 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MIRRCFQVAARLGHHRGLLEAPRILPRLNPASAFGSSTDSMFSRFLPEKTDLKDYALPNASWCSDMLSLYQEFLEKTKSSGWIKLPSFKSNRDHIRGLKLPSGLAVSSDKGDCRIFTRCIQVEGQGFEYVIFFQPTQKKSVCLFQPGSYLEGPPGFAHGGSLAAMMDETFSKTAFLAGEGLFTLSLNIRFKNLIPVDSLVVMDVELDKIEDQKLYMSCIAHSRDQQTVYAKSSGVFLQLQLEEESPQ
190	Q99798	>sp|Q99798|ACON_HUMAN Aconitate hydratase, mitochondrial GN=ACO2 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAPYSLLVTRLQKALGVRQYHVASVLCQRAKVAMSHFEPNEYIHYDLLEKNINIVRKRLNRPLTLSEKIVYGHLDDPASQEIERGKSYLRLRPDRVAMQDATAQMAMLQFISSGLSKVAVPSTIHCDHLIEAQVGGEKDLRRAKDINQEVYNFLATAGAKYGVGFWKPGSGIIHQIILENYAYPGVLLIGTDSHTPNGGGLGGICIGVGGADAVDVMAGIPWELKCPKVIGVKLTGSLSGWSSPKDVILKVAGILTVKGGTGAIVEYHGPGVDSISCTGMATICNMGAEIGATTSVFPYNHRMKKYLSKTGREDIANLADEFKDHLVPDPGCHYDQLIEINLSELKPHINGPFTPDLAHPVAEVGKVAEKEGWPLDIRVGLIGSCTNSSYEDMGRSAAVAKQALAHGLKCKSQFTITPGSEQIRATIERDGYAQILRDLGGIVLANACGPCIGQWDRKDIKKGEKNTIVTSYNRNFTGRNDANPETHAFVTSPEIVTALAIAGTLKFNPETDYLTGTDGKKFRLEAPDADELPKGEFDPGQDTYQHPPKDSSGQHVDVSPTSQRLQLLEPFDKWDGKDLEDLQILIKVKGKCTTDHISAAGPWLKFRGHLDNISNNLLIGAINIENGKANSVRNAVTQEFGPVPDTARYYKKHGIRWVVIGDENYGEGSSREHAALEPRHLGGRAIITKSFARIHETNLKKQGLLPLTFADPADYNKIHPVDKLTIQGLKDFTPGKPLKCIIKHPNGTQETILLNHTFNETQIEWFRAGSALNRMKELQQ
191	Q3I5F7	>sp|Q3I5F7|ACOT6_HUMAN Putative acyl-coenzyme A thioesterase 6 GN=ACOT6 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLQHPKVKGPSIALLGFSKGGDLCLSMASFLKGITATVLINACVANTVAPLHYKDMIIPKLVDDLGKVKITKSGFLTFMDTWSNPLEEHNHQSLVPLEKAQVPFLFIVGMDDQSWKSEFYAQIASERLQAHGKERPQIICYPETGHCIDPPYFPPSRASVHAVLGEAIFYGGEPKAHSKAQVDAWQQIQTFFHKHLNGKKSVKHSKI
192	P63104	>sp|P63104|1433Z_HUMAN 14-3-3 protein zeta/delta GN=YWHAZ PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MDKNELVQKAKLAEQAERYDDMAACMKSVTEQGAELSNEERNLLSVAYKNVVGARRSSWRVVSSIEQKTEGAEKKQQMAREYREKIETELRDICNDVLSLLEKFLIPNASQAESKVFYLKMKGDYYRYLAEVAAGDDKKGIVDQSQQAYQEAFEISKKEMQPTHPIRLGLALNFSVFYYEILNSPEKACSLAKTAFDEAIAELDTLSEESYKDSTLIMQLLRDNLTLWTSDTQGDEAEAGEGGEN
193	P05534	>sp|P05534|1A24_HUMAN HLA class I histocompatibility antigen, A-24 alpha chain GN=HLA-A PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMAPRTLVLLLSGALALTQTWAGSHSMRYFSTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDEETGKVKAHSQTDRENLRIALRYYNQSEAGSHTLQMMFGCDVGSDGRFLRGYHQYAYDGKDYIALKEDLRSWTAADMAAQITKRKWEAAHVAEQQRAYLEGTCVDGLRRYLENGKETLQRTDPPKTHMTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQPTVPIVGIIAGLVLLGAVITGAVVAAVMWRRNSSDRKGGSYSQAASSDSAQGSDVSLTACKV
194	P30512	>sp|P30512|1A29_HUMAN HLA class I histocompatibility antigen, A-29 alpha chain GN=HLA-A PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMAPRTLLLLLLGALALTQTWAGSHSMRYFTTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDLQTRNVKAQSQTDRANLGTLRGYYNQSEAGSHTIQMMYGCHVGSDGRFLRGYRQDAYDGKDYIALNEDLRSWTAADMAAQITQRKWEAARVAEQLRAYLEGTCVEWLRRYLENGKETLQRTDAPKTHMTHHAVSDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWASVVVPSGQEQRYTCHVQHEGLPKPLTLRWEPSSQPTIPIVGIIAGLVLFGAVFAGAVVAAVRWRRKSSDRKGGSYSQAASSDSAQGSDMSLTACKV
196	P30453	>sp|P30453|1A34_HUMAN HLA class I histocompatibility antigen, A-34 alpha chain GN=HLA-A PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAIMAPRTLVLLLSGALALTQTWAGSHSMRYFYTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDRNTRKVKAQSQTDRVDLGTLRGYYNQSEDGSHTIQRMYGCDVGPDGRFLRGYQQDAYDGKDYIALNEDLRSWTAADMAAQITQRKWETAHEAEQWRAYLEGTCVEWLRRYLENGKETLQRTDAPKTHMTHHAVSDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWASVVVPSGQEQRYTCHVQHEGLPKPLTLRWEPSSQPTIPIVGILAGLVLFGAVIAGAVVAAVMWRRKSSDRKGGSYSQAASSDSAQGSDMSLTACKV
197	P30459	>sp|P30459|1A74_HUMAN HLA class I histocompatibility antigen, A-74 alpha chain GN=HLA-A PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMAPRTLLLLLLGALALTQTRAGSHSMRYFFTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDQETRNVKAHSQTDRVDLGTLRGYYNQSEAGSHTIQMMYGCDVGPDGRLLRGYQQDAYDGKDYIALNEDLRSWTAADMAAQITQRKWEAARVAEQLRAYLEGTCVEWLRRYLENGKETLQRTDAPKTHMTHHAVSDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWASVVVPSGQEQRYTCHVQHEGLPKPLTLRWEPSSQPTIPIVGIIAGLVLFGAMFAGAVVAAVRWRRKSSDRKGGSYSQAASSDSAQGSDMSLTACKV
198	P30462	>sp|P30462|1B14_HUMAN HLA class I histocompatibility antigen, B-14 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLVMAPRTVLLLLSAALALTETWAGSHSMRYFYTSVSRPGRGEPRFISVGYVDDTQFVRFDSDAASPREEPRAPWIEQEGPEYWDRNTQICKTNTQTDRESLRNLRGYYNQSEAGSHTLQWMYGCDVGPDGRLLRGYNQFAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAAREAEQLRAYLEGTCVEWLRRHLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
199	P30466	>sp|P30466|1B18_HUMAN HLA class I histocompatibility antigen, B-18 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTLLLLLWGAVALTETWAGSHSMRYFHTSVSRPGRGEPRFISVGYVDGTQFVRFDSDAASPRTEPRAPWIEQEGPEYWDRNTQISKTNTQTYRESLRNLRGYYNQSEAGSHTLQRMYGCDVGPDGRLLRGHDQSAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAARVAEQLRAYLEGTCVEWLRRHLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
200	P03989	>sp|P03989|1B27_HUMAN HLA class I histocompatibility antigen, B-27 alpha chain GN=HLA-B PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTLLLLLWGAVALTETWAGSHSMRYFHTSVSRPGRGEPRFITVGYVDDTLFVRFDSDAASPREEPRAPWIEQEGPEYWDRETQICKAKAQTDREDLRTLLRYYNQSEAGSHTLQNMYGCDVGPDGRLLRGYHQDAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAARVAEQLRAYLEGECVEWLRRYLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCRRKSSGGKGGSYSQAACSDSAQGSDVSLTA
201	P18463	>sp|P18463|1B37_HUMAN HLA class I histocompatibility antigen, B-37 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTLLLLLWGAVALTETWAGSHSMRYFHTSVSRPGRGEPRFISVGYVDDTQFVRFDSDAASPRTEPRAPWIEQEGPEYWDRETQISKTNTQTYREDLRTLLRYYNQSEAGSHTIQRMSGCDVGPDGRLLRGYNQFAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAARVAEQDRAYLEGTCVEWLRRYLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
202	P30475	>sp|P30475|1B39_HUMAN HLA class I histocompatibility antigen, B-39 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLVMAPRTVLLLLSAALALTETWAGSHSMRYFYTSVSRPGRGEPRFISVGYVDDTQFVRFDSDAASPREEPRAPWIEQEGPEYWDRNTQICKTNTQTDRESLRNLRGYYNQSEAGSHTLQRMYGCDVGPDGRLLRGHNQFAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAARVAEQLRTYLEGTCVEWLRRYLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
203	P30479	>sp|P30479|1B41_HUMAN HLA class I histocompatibility antigen, B-41 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTVLLLLSAALALTETWAGSHSMRYFHTAMSRPGRGEPRFITVGYVDDTLFVRFDSDATSPRKEPRAPWIEQEGPEYWDRETQISKTNTQTYRESLRNLRGYYNQSEAGSHTWQRMYGCDVGPDGRLLRGHNQYAYDGKDYIALNEDLRSWTAADTAAQITQRKWEAARVAEQDRAYLEGTCVEWLRRYLENGKDTLERADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCRRKSSGGKGGSYSQAACSDSAQGSDVSLTA
204	P30481	>sp|P30481|1B44_HUMAN HLA class I histocompatibility antigen, B-44 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTLLLLLWGAVALTETWAGSHSMRYFYTAMSRPGRGEPRFITVGYVDDTLFVRFDSDATSPRKEPRAPWIEQEGPEYWDRETQISKTNTQTYRENLRTALRYYNQSEAGSHIIQRMYGCDVGPDGRLLRGYDQDAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAARVAEQDRAYLEGLCVESLRRYLENGKETLQRADPPKTHVTHHPISDHEVTLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCRRKSSGGKGGSYSQAACSDSAQGSDVSLTA
205	P30486	>sp|P30486|1B48_HUMAN HLA class I histocompatibility antigen, B-48 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLVMAPRTVLLLLSAALALTETWAGSHSMRYFYTSVSRPGRGEPRFISVGYVDDTQFVRFDSDAASPREEPRAPWIEQEGPEYWDRETQISKTNTQTYRESLRNLRGYYNQSEAGSHTLQSMYGCDVGPDGRLLRGHNQYAYDGKDYIALNEDLRSWTAADTAAQISQRKLEAARVAEQLRAYLEGECVEWLRRYLENGKDKLERADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWTAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTVPIVGIVAGLAVLAVVVIGAVVAAVMCRRKSSGGKGGSYSQAACSDSAQGSDVSLTA
206	P30488	>sp|P30488|1B50_HUMAN HLA class I histocompatibility antigen, B-50 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTVLLLLSAALALTETWAGSHSMRYFHTAMSRPGRGEPRFITVGYVDDTLFVRFDSDATSPRKEPRAPWIEQEGPEYWDRETQISKTNTQTYRESLRNLRGYYNQSEAGSHTWQRMYGCDLGPDGRLLRGYNQLAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAAREAEQLRAYLEGLCVEWLRRYLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
207	P30491	>sp|P30491|1B53_HUMAN HLA class I histocompatibility antigen, B-53 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTVLLLLWGAVALTETWAGSHSMRYFYTAMSRPGRGEPRFIAVGYVDDTQFVRFDSDAASPRTEPRAPWIEQEGPEYWDRNTQIFKTNTQTYRENLRIALRYYNQSEAGSHIIQRMYGCDLGPDGRLLRGHDQSAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAARVAEQLRAYLEGLCVEWLRRYLENGKETLQRADPPKTHVTHHPVSDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
208	P30495	>sp|P30495|1B56_HUMAN HLA class I histocompatibility antigen, B-56 alpha chain GN=HLA-B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVTAPRTLLLLLWGALALTETWAGSHSMRYFYTAMSRPGRGEPRFIAVGYVDDTQFVRFDSDAASPREEPRAPWIEQEGPEYWDRNTQIYKAQAQTDRESLRNLRGYYNQSEAGSHTWQTMYGCDLGPDGRLLRGHNQLAYDGKDYIALNEDLSSWTAADTAAQITQRKWEAARVAEQLRAYLEGLCVEWLRRYLENGKETLQRADPPKTHVTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDRTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRWEPSSQSTIPIVGIVAGLAVLAVVVIGAVVATVMCRRKSSGGKGGSYSQAASSDSAQGSDVSLTA
209	P30501	>sp|P30501|1C02_HUMAN HLA class I histocompatibility antigen, Cw-2 alpha chain GN=HLA-C PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVMEPRTLILLLSGALALTETWACSHSMRYFYTAVSRPSRGEPHFIAVGYVDDTQFVRFDSDAASPRGEPRGRWVEQEGPEYWDRETQKYNRQAQTDRVNLRKLRGYYNQSEAGSHTLQRMYGCDLGPDGRLLRGYDQSAYDGKDYIALNEDLRSWTAADTAAQITQRKWEAAREAEEWRAYLEGECVEWLRRYLENGKEKLQRAEHPKTHVTHHPVSDHEATLRCWALGFYPTEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPEPLTLRWEPSSQPTIPIVGIVAGLAVLAVLAVLGAVVAVVMCRRKSSGGKGGSCSQAASSNSAQGSDESLIASKA
210	P04222	>sp|P04222|1C03_HUMAN HLA class I histocompatibility antigen, Cw-3 alpha chain GN=HLA-C PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MRVMAPRTLILLLSGALALTETWAGSHSMRYFYTAVSRPGRGEPHFIAVGYVDDTQFVRFDSDAASPRGEPRAPWVEQEGPEYWDRETQKYKRQAQTDRVSLRNLRGYYNQSEAGSHIIQRMYGCDVGPDGRLLRGYDQYAYDGKDYIALNEDLRSWTAADTAAQITQRKWEAAREAEQLRAYLEGLCVEWLRRYLKNGKETLQRAEHPKTHVTHHPVSDHEATLRCWALGFYPAEITLTWQWDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPEPLTLRWEPSSQPTIPIVGIVAGLAVLAVLAVLGAVVAVVMCRRKSSGGKGGSCSQAASSNSAQGSDESLIACKA
211	Q07000	>sp|Q07000|1C15_HUMAN HLA class I histocompatibility antigen, Cw-15 alpha chain GN=HLA-C PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRVMAPRTLLLLLSGALALTETWACSHSMRYFYTAVSRPGRGEPHFIAVGYVDDTQFVRFDSDAASPRGEPRAPWVEQEGPEYWDRETQNYKRQAQTDRVNLRKLRGYYNQSEAGSHIIQRMYGCDLGPDGRLLRGHDQLAYDGKDYIALNEDLRSWTAADTAAQITQRKWEAAREAEQLRAYLEGTCVEWLRRYLENGKETLQRAEHPKTHVTHHPVSDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPEPLTLRWEPSSQPTIPIVGIVAGLAVLAVLAVLGAVMAVVMCRRKSSGGKGGSCSQAASSNSAQGSDESLIACKA
212	Q15172	>sp|Q15172|2A5A_HUMAN Serine/threonine-protein phosphatase 2A 56 kDa regulatory subunit alpha isoform GN=PPP2R5A PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MSSSSPPAGAASAAISASEKVDGFTRKSVRKAQRQKRSQGSSQFRSQGSQAELHPLPQLKDATSNEQQELFCQKLQQCCILFDFMDSVSDLKSKEIKRATLNELVEYVSTNRGVIVESAYSDIVKMISANIFRTLPPSDNPDFDPEEDEPTLEASWPHIQLVYEFFLRFLESPDFQPSIAKRYIDQKFVQQLLELFDSEDPRERDFLKTVLHRIYGKFLGLRAFIRKQINNIFLRFIYETEHFNGVAELLEILGSIINGFALPLKAEHKQFLMKVLIPMHTAKGLALFHAQLAYCVVQFLEKDTTLTEPVIRGLLKFWPKTCSQKEVMFLGEIEEILDVIEPTQFKKIEEPLFKQISKCVSSSHFQVAERALYFWNNEYILSLIEENIDKILPIMFASLYKISKEHWNPTIVALVYNVLKTLMEMNGKLFDDLTSSYKAERQREKKKELEREELWKKLEELKLKKALEKQNSAYNMHSILSNTSAE
213	Q13362	>sp|Q13362|2A5G_HUMAN Serine/threonine-protein phosphatase 2A 56 kDa regulatory subunit gamma isoform GN=PPP2R5C PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MLTCNKAGSRMVVDAANSNGPFQPVVLLHIRDVPPADQEKLFIQKLRQCCVLFDFVSDPLSDLKWKEVKRAALSEMVEYITHNRNVITEPIYPEVVHMFAVNMFRTLPPSSNPTGAEFDPEEDEPTLEAAWPHLQLVYEFFLRFLESPDFQPNIAKKYIDQKFVLQLLELFDSEDPRERDFLKTTLHRIYGKFLGLRAYIRKQINNIFYRFIYETEHHNGIAELLEILGSIINGFALPLKEEHKIFLLKVLLPLHKVKSLSVYHPQLAYCVVQFLEKDSTLTEPVVMALLKYWPKTHSPKEVMFLNELEEILDVIEPSEFVKIMEPLFRQLAKCVSSPHFQVAERALYYWNNEYIMSLISDNAAKILPIMFPSLYRNSKTHWNKTIHGLIYNALKLFMEMNQKLFDDCTQQFKAEKLKEKLKMKEREEAWVKIENLAKANPQYTVYSQASTMSIPVAMETDGPLFEDVQMLRKTVKDEAHQAQKDPKKDRPLARRKSELPQDPHTKKALEAHCRADELASQDGR
214	Q30134	>sp|Q30134|2B18_HUMAN HLA class II histocompatibility antigen, DRB1-8 beta chain GN=HLA-DRB1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MVCLRLPGGSCMAVLTVTLMVLSSPLALAGDTRPRFLEYSTGECYFFNGTERVRFLDRYFYNQEEYVRFDSDVGEYRAVTELGRPSAEYWNSQKDFLEDRRALVDTYCRHNYGVGESFTVQRRVHPKVTVYPSKTQPLQHHNLLVCSVSGFYPGSIEVRWFRNGQEEKTGVVSTGLIHNGDWTFQTLVMLETVPRSGEVYTCQVEHPSVTSPLTVEWSARSESAQSKMLSGVGGFVLGLLFLGAGLFIYFRNQKGHSGLQPTGFLS
215	P46952	>sp|P46952|3HAO_HUMAN 3-hydroxyanthranilate 3,4-dioxygenase GN=HAAO PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MERRLGVRAWVKENRGSFQPPVCNKLMHQEQLKVMFIGGPNTRKDYHIEEGEEVFYQLEGDMVLRVLEQGKHRDVVIRQGEIFLLPARVPHSPQRFANTVGLVVERRRLETELDGLRYYVGDTMDVLFEKWFYCKDLGTQLAPIIQEFFSSEQYRTGKPIPDQLLKEPPFPLSTRSIMEPMSLDAWLDSHHRELQAGTPLSLFGDTYETQVIAYGQGSSEGLRQNVDVWLWQLEGSSVVTMGGRRLSLAPDDSLLVLAGTSYAWERTQGSVALSVTQDPACKKPLG
216	Q8WXA8	>sp|Q8WXA8|5HT3C_HUMAN 5-hydroxytryptamine receptor 3C GN=HTR3C PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MEGGWPARQSALLCLTVSLLLQGRGDAFTINCSGFDQHGVDPAVFQAVFDRKAFRPFTNYSIPTRVNISFTLSAILGVDAQLQLLTSFLWMDLVWDNPFINWNPKECVGINKLTVLAENLWLPDIFIVESMDVDQTPSGLTAYISSEGRIKYDKPMRVTSICNLDIFYFPFDQQNCTFTFSSFLYTVDSMLLGMDKEVWEITDTSRKVIQTQGEWELLGINKATPKMSMGNNLYDQIMFYVAIRRRPSLYIINLLVPSSFLVAIDALSFYLPAESENRAPFKITLLLGYNVFLLMMNDLLPASGTPLISVYFALCLSLMVVSLLETVFITYLLHVATTQPPPMPRWLHSLLLHCTSPGRCCPTAPQKGNKGLGLTLTHLPGPKEPGELAGKKLGPRETEPDGGSGWTKTQLMELWVQFSHAMDTLLFRLYLLFMASSILTVIVLWNT
217	A5X5Y0	>sp|A5X5Y0|5HT3E_HUMAN 5-hydroxytryptamine receptor 3E GN=HTR3E PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MEGSWFHRKRFSFYLLLGFLLQGRGVTFTINCSGFGQHGADPTALNSVFNRKPFRPVTNISVPTQVNISFAMSAILDVNEQLHLLSSFLWLEMVWDNPFISWNPEECEGITKMSMAAKNLWLPDIFIIELMDVDKTPKGLTAYVSNEGRIRYKKPMKVDSICNLDIFYFPFDQQNCTLTFSSFLYTVDSMLLDMEKEVWEITDASRNILQTHGEWELLGLSKATAKLSRGGNLYDQIVFYVAIRRRPSLYVINLLVPSGFLVAIDALSFYLPVKSGNRVPFKITLLLGYNVFLLMMSDLLPTSGTPLIGVYFALCLSLMVGSLLETIFITHLLHVATTQPPPLPRWLHSLLLHCNSPGRCCPTAPQKENKGPGLTPTHLPGVKEPEVSAGQMPGPAEAELTGGSEWTRAQREHEAQKQHSVELWLQFSHAMDAMLFRLYLLFMASSIITVICLWNT
218	P04217	>sp|P04217|A1BG_HUMAN Alpha-1B-glycoprotein GN=A1BG PE=1 SV=4 Homo sapiens OS=Human NCBI_TaxID=9606	MSMLVVFLLLWGVTWGPVTEAAIFYETQPSLWAESESLLKPLANVTLTCQAHLETPDFQLFKNGVAQEPVHLDSPAIKHQFLLTGDTQGRYRCRSGLSTGWTQLSKLLELTGPKSLPAPWLSMAPVSWITPGLKTTAVCRGVLRGVTFLLRREGDHEFLEVPEAQEDVEATFPVHQPGNYSCSYRTDGEGALSEPSATVTIEELAAPPPPVLMHHGESSQVLHPGNKVTLTCVAPLSGVDFQLRRGEKELLVPRSSTSPDRIFFHLNAVALGDGGHYTCRYRLHDNQNGWSGDSAPVELILSDETLPAPEFSPEPESGRALRLRCLAPLEGARFALVREDRGGRRVHRFQSPAGTEALFELHNISVADSANYSCVYVDLKPPFGGSAPSERLELHVDGPPPRPQLRATWSGAVLAGRDAVLRCEGPIPDVTFELLREGETKAVKTVRTPGAAANLELIFVGPQHAGNYRCRYRSWVPHTFESELSDPVELLVAES
219	Q9NQ94	>sp|Q9NQ94|A1CF_HUMAN APOBEC1 complementation factor GN=A1CF PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MESNHKSGDGLSGTQKEAALRALVQRTGYSLVQENGQRKYGGPPPGWDAAPPERGCEIFIGKLPRDLFEDELIPLCEKIGKIYEMRMMMDFNGNNRGYAFVTFSNKVEAKNAIKQLNNYEIRNGRLLGVCASVDNCRLFVGGIPKTKKREEILSEMKKVTEGVVDVIVYPSAADKTKNRGFAFVEYESHRAAAMARRKLLPGRIQLWGHGIAVDWAEPEVEVDEDTMSSVKILYVRNLMLSTSEEMIEKEFNNIKPGAVERVKKIRDYAFVHFSNREDAVEAMKALNGKVLDGSPIEVTLAKPVDKDSYVRYTRGTGGRGTMLQGEYTYSLGQVYDPTTTYLGAPVFYAPQTYAAIPSLHFPATKGHLSNRAIIRAPSVREIYMNVPVGAAGVRGLGGRGYLAYTGLGRGYQVKGDKREDKLYDILPGMELTPMNPVTLKPQGIKLAPQILEEICQKNNWGQPVYQLHSAIGQDQRQLFLYKITIPALASQNPAIHPFTPPKLSAFVDEAKTYAAEYTLQTLGIPTDGGDGTMATAAAAATAFPGYAVPNATAPVSAAQLKQAVTLGQDLAAYTTYEVYPTFAVTARGDGYGTF
220	Q5SQ80	>sp|Q5SQ80|A20A2_HUMAN Ankyrin repeat domain-containing protein 20A2 GN=ANKRD20A2 PE=3 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MKLFGFGSRRGQTAQGSIDHVYTGSGYRIRDSELQKIHRAAVKGDAAEVERCLARRSGDLDALDKQHRTALHLACASGHVQVVTLLVNRKCQIDVCDKENRTPLIQAVHCQEEACAVILLEHGANPNLKDIYGNTALHYAVYSESTSLAEKLLSHGAHIEALDKDNNTPLLFAIICKKEKMVEFLLKRKASSHAVDRLRRSALMLAVYYDSPGIVNILLKQNIDVFAQDMCGRDAEDYAISHHLTKIQQQILEHKKKILKKEKSDVGSSDESAVSIFHELRVDSLPASDDKDLNVATKQCVPEKVSEPLPGSSHEKGNRIVNGQGEGPPAKHPSLKPSTEVEDPAVKGAVQRKNVQTLRAEQALPVASEEEQERHERSEKKQPQVKEGNNTNKSEKIQLSENICDSTSSAAAGRLTQQRKIGKTYPQQFPKKLKEEHDRCTLKQENEEKTNVNMLYKKNREELERKEKQYKKEVEAKQLEPTVQSLEMKSKTARNTPNRDFHNHEEMKGLMDENCILKADIAILRQEICTMKNDNLEKENKYLKDIKIVKETNAALEKYIKLNEEMITETAFRYQQELNDLKAENTRLNAELLKEKESKKRLEADIESYQSRLAAAISKHSESVKTERNLKLALERTRDVSVQVEMSSAISKVKDENEFLTEQLSETQIKFNALKDKFRKTRDSLRKKSLALETVQNDLSQTQQQTQEMKEMYQNAEAKVNNSTGKWNCVEERICHLQRENAWLVQQLDDVHQKEDHKEIVTNIQRGFIESGKKDLVLEEKSKKLMNECDHLKESLFQYEREKTEGVVSIKEDKYFQTSRKKI
221	Q4UJ75	>sp|Q4UJ75|A20A4_HUMAN Ankyrin repeat domain-containing protein 20A4 GN=ANKRD20A4 PE=3 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MKLFGFGSRRGQTAQGSIDHVYTGSGYRIRDSELQKIHRAAVKGDAAEVERCLARRSGELDALDKQHRTALHLACASGHVQVVTLLVNRKCQIDVCDKENRTPLIQAVHCQEEACAVILLEHGANPNLKDIYGNTALHYAVYSESTSLAEKLLSHGAHIEALDKDNNTPLLFAIICKKEKMVEFLLKKKASSHAVDRLRRSALMLAVYYDSPGIVNILLKQNIDVFAQDMCGRDAEDYAISHHLTKIQQQILEHKKKILKKEKSDVGSSDESAVSIFHELRVDSLPASDDKDLNVATKQCVPEKVSEPLPGSSHEKGNRIVNGQGEGPPAKHPSLKPSTEVEDPAVKGAVQRKNVQTLRAEQALPVASEEEQQRHERSEKKQPQVKEGNNTNKSEKIQLSENICDSTSSAAAGRLTQQRKIGKTYPQQFPKKLKEEHDRCTLKQENEEKTNVNMLYKKNREELERKEKQYKKEVEAKQLEPTVQSLEMKSKTARNTPNWDFHNHEEMKGLMDENCILKADIAILRQEICTMKNDNLEKENKYLKDIKIVKETNAALEKYIKLNEEMITETAFRYQQELNDLKAENTRLNAELLKEKESKKRLEADIESYQSRLAAAISKHSESVKTERNLKLALERTQDVSVQVEMSSAISKVKDENEFLTEQLSETQIKFNALKDKFRKTRDSLRKKSLALETVQNNLSQTQQQTQEMKEMYQNAEAKVNNSTGKWNCVEERICHLQRENAWLVQQLDDVHQKEDHKEIVTNIQRGFIESGKKDFVLEEKSKKLMNECDHLKESLFQYEREKTEVVVSIKEDKYFQTSRKKI
223	P22760	>sp|P22760|AAAD_HUMAN Arylacetamide deacetylase GN=AADAC PE=1 SV=5 Homo sapiens OS=Human NCBI_TaxID=9606	MGRKSLYLLIVGILIAYYIYTPLPDNVEEPWRMMWINAHLKTIQNLATFVELLGLHHFMDSFKVVGSFDEVPPTSDENVTVTETKFNNILVRVYVPKRKSEALRRGLFYIHGGGWCVGSAALSGYDLLSRWTADRLDAVVVSTNYRLAPKYHFPIQFEDVYNALRWFLRKKVLAKYGVNPERIGISGDSAGGNLAAAVTQQLLDDPDVKIKLKIQSLIYPALQPLDVDLPSYQENSNFLFLSKSLMVRFWSEYFTTDRSLEKAMLSRQHVPVESSHLFKFVNWSSLLPERFIKGHVYNNPNYGSSELAKKYPGFLDVRAAPLLADDNKLRGLPLTYVITCQYDLLRDDGLMYVTRLRNTGVQVTHNHVEDGFHGAFSFLGLKISHRLINQYIEWLKENL
224	Q15758	>sp|Q15758|AAAT_HUMAN Neutral amino acid transporter B(0) GN=SLC1A5 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MVADPPRDSKGLAAAEPTANGGLALASIEDQGAAAGGYCGSRDQVRRCLRANLLVLLTVVAVVAGVALGLGVSGAGGALALGPERLSAFVFPGELLLRLLRMIILPLVVCSLIGGAASLDPGALGRLGAWALLFFLVTTLLASALGVGLALALQPGAASAAINASVGAAGSAENAPSKEVLDSFLDLARNIFPSNLVSAAFRSYSTTYEERNITGTRVKVPVGQEVEGMNILGLVVFAIVFGVALRKLGPEGELLIRFFNSFNEATMVLVSWIMWYAPVGIMFLVAGKIVEMEDVGLLFARLGKYILCCLLGHAIHGLLVLPLIYFLFTRKNPYRFLWGIVTPLATAFGTSSSSATLPLMMKCVEENNGVAKHISRFILPIGATVNMDGAALFQCVAAVFIAQLSQQSLDFVKIITILVTATASSVGAAGIPAGGVLTLAIILEAVNLPVDHISLILAVDWLVDRSCTVLNVEGDALGAGLLQNYVDRTESRSTEPELIQVKSELPLDPLPVPTEEGNPLLKHYRGPAGDATVASEKESVM
225	Q86V21	>sp|Q86V21|AACS_HUMAN Acetoacetyl-CoA synthetase GN=AACS PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MSKEERPGREEILECQVMWEPDSKKNTQMDRFRAAVGAACGLALESYDDLYHWSVESYSDFWAEFWKFSGIVFSRVYDEVVDTSKGIADVPEWFKGSRLNYAENLLRHKENDRVALYIAREGKEEIVKVTFEELRQEVALFAAAMRKMGVKKGDRVVGYLPNSEHAVEAMLAAASIGAIWSSTSPDFGVNGVLDRFSQIQPKLIFSVEAVVYNGKEHNHMEKLQQVVKGLPDLKKVVVIPYVSSRENIDLSKIPNSVFLDDFLATGTSEQAPQLEFEQLPFSHPLFIMFSSGTTGAPKCMVHSAGGTLIQHLKEHLLHGNMTSSDILLCYTTVGWMMWNWMVSLLATGAAMVLYDGSPLVPTPNVLWDLVDRIGITVLVTGAKWLSVLEEKAMKPVETHSLQMLHTILSTGSPLKAQSYEYVYRCIKSSILLGSISGGTDIISCFMGHNFSLPVYKGEIQARNLGMAVEAWNEEGKAVWGESGELVCTKPIPCQPTHFWNDENGNKYRKAYFSKFPGIWAHGDYCRINPKTGGIVMLGRSDGTLNPNGVRFGSSEIYNIVESFEEVEDSLCVPQYNKYREERVILFLKMASGHAFQPDLVKRIRDAIRMGLSARHVPSLILETKGIPYTLNGKKVEVAVKQIIAGKAVEQGGAFSNPETLDLYRDIPELQGF
226	P54646	>sp|P54646|AAPK2_HUMAN 5'-AMP-activated protein kinase catalytic subunit alpha-2 GN=PRKAA2 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAEKQKHDGRVKIGHYVLGDTLGVGTFGKVKIGEHQLTGHKVAVKILNRQKIRSLDVVGKIKREIQNLKLFRHPHIIKLYQVISTPTDFFMVMEYVSGGELFDYICKHGRVEEMEARRLFQQILSAVDYCHRHMVVHRDLKPENVLLDAHMNAKIADFGLSNMMSDGEFLRTSCGSPNYAAPEVISGRLYAGPEVDIWSCGVILYALLCGTLPFDDEHVPTLFKKIRGGVFYIPEYLNRSVATLLMHMLQVDPLKRATIKDIREHEWFKQDLPSYLFPEDPSYDANVIDDEAVKEVCEKFECTESEVMNSLYSGDPQDQLAVAYHLIIDNRRIMNQASEFYLASSPPSGSFMDDSAMHIPPGLKPHPERMPPLIADSPKARCPLDALNTTKPKSLAVKKAKWHLGIRSQSKPYDIMAEVYRAMKQLDFEWKVVNAYHLRVRRKNPVTGNYVKMSLQLYLVDNRSYLLDFKSIDDEVVEQRSGSSTPQRSCSAAGLHRPRSSFDSTTAESHSLSGSLTGSLTGSTLSSVSPRLGSHTMDFFEMCASLITTLAR
227	Q5VST6	>sp|Q5VST6|AB17B_HUMAN Protein ABHD17B GN=ABHD17B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MNNLSFSELCCLFCCPPCPGKIASKLAFLPPDPTYTLMCDESGSRWTLHLSERADWQYSSREKDAIECFMTRTSKGNRIACMFVRCSPNAKYTLLFSHGNAVDLGQMSSFYIGLGSRINCNIFSYDYSGYGASSGKPTEKNLYADIEAAWLALRTRYGIRPENVIIYGQSIGTVPSVDLAARYESAAVILHSPLTSGMRVAFPDTKKTYCFDAFPNIDKISKITSPVLIIHGTEDEVIDFSHGLALFERCQRPVEPLWVEGAGHNDVELYGQYLERLKQFVSQELVNL
228	Q7Z5R6	>sp|Q7Z5R6|AB1IP_HUMAN Amyloid beta A4 precursor protein-binding family B member 1-interacting protein GN=APBB1IP PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MGESSEDIDQMFSTLLGEMDLLTQSLGVDTLPPPDPNPPRAEFNYSVGFKDLNESLNALEDQDLDALMADLVADISEAEQRTIQAQKESLQNQHHSASLQASIFSGAASLGYGTNVAATGISQYEDDLPPPPADPVLDLPLPPPPPEPLSQEEEEAQAKADKIKLALEKLKEAKVKKLVVKVHMNDNSTKSLMVDERQLARDVLDNLFEKTHCDCNVDWCLYEIYPELQIERFFEDHENVVEVLSDWTRDTENKILFLEKEEKYAVFKNPQNFYLDNRGKKESKETNEKMNAKNKESLLEESFCGTSIIVPELEGALYLKEDGKKSWKRRYFLLRASGIYYVPKGKTKTSRDLACFIQFENVNIYYGTQHKMKYKAPTDYCFVLKHPQIQKESQYIKYLCCDDTRTLNQWVMGIRIAKYGKTLYDNYQRAVAKAGLASRWTNLGTVNAAAPAQPSTGPKTGTTQPNGQIPQATHSVSAVLQEAQRHAETSKDKKPALGNHHDPAVPRAPHAPKSSLPPPPPVRRSSDTSGSPATPLKAKGTGGGGLPAPPDDFLPPPPPPPPLDDPELPPPPPDFMEPPPDFVPPPPPSYAGIAGSELPPPPPPPPAPAPAPVPDSARPPPAVAKRPPVPPKRQENPGHPGGAGGGEQDFMSDLMKALQKKRGNVS
229	Q9UH17	>sp|Q9UH17|ABC3B_HUMAN DNA dC->dU-editing enzyme APOBEC-3B GN=APOBEC3B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MNPQIRNPMERMYRDTFYDNFENEPILYGRSYTWLCYEVKIKRGRSNLLWDTGVFRGQVYFKPQYHAEMCFLSWFCGNQLPAYKCFQITWFVSWTPCPDCVAKLAEFLSEHPNVTLTISAARLYYYWERDYRRALCRLSQAGARVTIMDYEEFAYCWENFVYNEGQQFMPWYKFDENYAFLHRTLKEILRYLMDPDTFTFNFNNDPLVLRRRQTYLCYEVERLDNGTWVLMDQHMGFLCNEAKNLLCGFYGRHAELRFLDLVPSLQLDPAQIYRVTWFISWSPCFSWGCAGEVRAFLQENTHVRLRIFAARIYDYDPLYKEALQMLRDAGAQVSIMTYDEFEYCWDTFVYRQGCPFQPWDGLEEHSQALSGRLRAILQNQGN
230	Q8IUX4	>sp|Q8IUX4|ABC3F_HUMAN DNA dC->dU-editing enzyme APOBEC-3F GN=APOBEC3F PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MKPHFRNTVERMYRDTFSYNFYNRPILSRRNTVWLCYEVKTKGPSRPRLDAKIFRGQVYSQPEHHAEMCFLSWFCGNQLPAYKCFQITWFVSWTPCPDCVAKLAEFLAEHPNVTLTISAARLYYYWERDYRRALCRLSQAGARVKIMDDEEFAYCWENFVYSEGQPFMPWYKFDDNYAFLHRTLKEILRNPMEAMYPHIFYFHFKNLRKAYGRNESWLCFTMEVVKHHSPVSWKRGVFRNQVDPETHCHAERCFLSWFCDDILSPNTNYEVTWYTSWSPCPECAGEVAEFLARHSNVNLTIFTARLYYFWDTDYQEGLRSLSQEGASVEIMGYKDFKYCWENFVYNDDEPFKPWKGLKYNFLFLDSKLQEILE
231	Q9HC16	>sp|Q9HC16|ABC3G_HUMAN DNA dC->dU-editing enzyme APOBEC-3G GN=APOBEC3G PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MKPHFRNTVERMYRDTFSYNFYNRPILSRRNTVWLCYEVKTKGPSRPPLDAKIFRGQVYSELKYHPEMRFFHWFSKWRKLHRDQEYEVTWYISWSPCTKCTRDMATFLAEDPKVTLTIFVARLYYFWDPDYQEALRSLCQKRDGPRATMKIMNYDEFQHCWSKFVYSQRELFEPWNNLPKYYILLHIMLGEILRHSMDPPTFTFNFNNEPWVRGRHETYLCYEVERMHNDTWVLLNQRRGFLCNQAPHKHGFLEGRHAELCFLDVIPFWKLDLDQDYRVTCFTSWSPCFSCAQEMAKFISKNKHVSLCIFTARIYDDQGRCQEGLRTLAEAGAKISIMTYSEFKHCWDTFVDHQGCPFQPWDGLDEHSQDLSGRLRAILQNQEN
232	O95477	>sp|O95477|ABCA1_HUMAN ATP-binding cassette sub-family A member 1 GN=ABCA1 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MACWPQLRLLLWKNLTFRRRQTCQLLLEVAWPLFIFLILISVRLSYPPYEQHECHFPNKAMPSAGTLPWVQGIICNANNPCFRYPTPGEAPGVVGNFNKSIVARLFSDARRLLLYSQKDTSMKDMRKVLRTLQQIKKSSSNLKLQDFLVDNETFSGFLYHNLSLPKSTVDKMLRADVILHKVFLQGYQLHLTSLCNGSKSEEMIQLGDQEVSELCGLPREKLAAAERVLRSNMDILKPILRTLNSTSPFPSKELAEATKTLLHSLGTLAQELFSMRSWSDMRQEVMFLTNVNSSSSSTQIYQAVSRIVCGHPEGGGLKIKSLNWYEDNNYKALFGGNGTEEDAETFYDNSTTPYCNDLMKNLESSPLSRIIWKALKPLLVGKILYTPDTPATRQVMAEVNKTFQELAVFHDLEGMWEELSPKIWTFMENSQEMDLVRMLLDSRDNDHFWEQQLDGLDWTAQDIVAFLAKHPEDVQSSNGSVYTWREAFNETNQAIRTISRFMECVNLNKLEPIATEVWLINKSMELLDERKFWAGIVFTGITPGSIELPHHVKYKIRMDIDNVERTNKIKDGYWDPGPRADPFEDMRYVWGGFAYLQDVVEQAIIRVLTGTEKKTGVYMQQMPYPCYVDDIFLRVMSRSMPLFMTLAWIYSVAVIIKGIVYEKEARLKETMRIMGLDNSILWFSWFISSLIPLLVSAGLLVVILKLGNLLPYSDPSVVFVFLSVFAVVTILQCFLISTLFSRANLAAACGGIIYFTLYLPYVLCVAWQDYVGFTLKIFASLLSPVAFGFGCEYFALFEEQGIGVQWDNLFESPVEEDGFNLTTSVSMMLFDTFLYGVMTWYIEAVFPGQYGIPRPWYFPCTKSYWFGEESDEKSHPGSNQKRISEICMEEEPTHLKLGVSIQNLVKVYRDGMKVAVDGLALNFYEGQITSFLGHNGAGKTTTMSILTGLFPPTSGTAYILGKDIRSEMSTIRQNLGVCPQHNVLFDMLTVEEHIWFYARLKGLSEKHVKAEMEQMALDVGLPSSKLKSKTSQLSGGMQRKLSVALAFVGGSKVVILDEPTAGVDPYSRRGIWELLLKYRQGRTIILSTHHMDEADVLGDRIAIISHGKLCCVGSSLFLKNQLGTGYYLTLVKKDVESSLSSCRNSSSTVSYLKKEDSVSQSSSDAGLGSDHESDTLTIDVSAISNLIRKHVSEARLVEDIGHELTYVLPYEAAKEGAFVELFHEIDDRLSDLGISSYGISETTLEEIFLKVAEESGVDAETSDGTLPARRNRRAFGDKQSCLRPFTEDDAADPNDSDIDPESRETDLLSGMDGKGSYQVKGWKLTQQQFVALLWKRLLIARRSRKGFFAQIVLPAVFVCIALVFSLIVPPFGKYPSLELQPWMYNEQYTFVSNDAPEDTGTLELLNALTKDPGFGTRCMEGNPIPDTPCQAGEEEWTTAPVPQTIMDLFQNGNWTMQNPSPACQCSSDKIKKMLPVCPPGAGGLPPPQRKQNTADILQDLTGRNISDYLVKTYVQIIAKSLKNKIWVNEFRYGGFSLGVSNTQALPPSQEVNDAIKQMKKHLKLAKDSSADRFLNSLGRFMTGLDTKNNVKVWFNNKGWHAISSFLNVINNAILRANLQKGENPSHYGITAFNHPLNLTKQQLSEVALMTTSVDVLVSICVIFAMSFVPASFVVFLIQERVSKAKHLQFISGVKPVIYWLSNFVWDMCNYVVPATLVIIIFICFQQKSYVSSTNLPVLALLLLLYGWSITPLMYPASFVFKIPSTAYVVLTSVNLFIGINGSVATFVLELFTDNKLNNINDILKSVFLIFPHFCLGRGLIDMVKNQAMADALERFGENRFVSPLSWDLVGRNLFAMAVEGVVFFLITVLIQYRFFIRPRPVNAKLSPLNDEDEDVRRERQRILDGGGQNDILEIKELTKIYRRKRKPAVDRICVGIPPGECFGLLGVNGAGKSSTFKMLTGDTTVTRGDAFLNKNSILSNIHEVHQNMGYCPQFDAITELLTGREHVEFFALLRGVPEKEVGKVGEWAIRKLGLVKYGEKYAGNYSGGNKRKLSTAMALIGGPPVVFLDEPTTGMDPKARRFLWNCALSVVKEGRSVVLTSHSMEECEALCTRMAIMVNGRFRCLGSVQHLKNRFGDGYTIVVRIAGSNPDLKPVQDFFGLAFPGSVLKEKHRNMLQYQLPSSLSSLARIFSILSQSKKRLHIEDYSVSQTTLDQVFVNFAKDQSDDDHLKDLSLHKNQTVVDVAVLTSFLQDEKVKESYV
233	Q8WWZ7	>sp|Q8WWZ7|ABCA5_HUMAN ATP-binding cassette sub-family A member 5 GN=ABCA5 PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MSTAIREVGVWRQTRTLLLKNYLIKCRTKKSSVQEILFPLFFLFWLILISMMHPNKKYEEVPNIELNPMDKFTLSNLILGYTPVTNITSSIMQKVSTDHLPDVIITEEYTNEKEMLTSSLSKPSNFVGVVFKDSMSYELRFFPDMIPVSSIYMDSRAGCSKSCEAAQYWSSGFTVLQASIDAAIIQLKTNVSLWKELESTKAVIMGETAVVEIDTFPRGVILIYLVIAFSPFGYFLAIHIVAEKEKKIKEFLKIMGLHDTAFWLSWVLLYTSLIFLMSLLMAVIATASLLFPQSSSIVIFLLFFLYGLSSVFFALMLTPLFKKSKHVGIVEFFVTVAFGFIGLMIILIESFPKSLVWLFSPFCHCTFVIGIAQVMHLEDFNEGASFSNLTAGPYPLIITIIMLTLNSIFYVLLAVYLDQVIPGEFGLRRSSLYFLKPSYWSKSKRNYEELSEGNVNGNISFSEIIEPVSSEFVGKEAIRISGIQKTYRKKGENVEALRNLSFDIYEGQITALLGHSGTGKSTLMNILCGLCPPSDGFASIYGHRVSEIDEMFEARKMIGICPQLDIHFDVLTVEENLSILASIKGIPANNIIQEVQKVLLDLDMQTIKDNQAKKLSGGQKRKLSLGIAVLGNPKILLLDEPTAGMDPCSRHIVWNLLKYRKANRVTVFSTHFMDEADILADRKAVISQGMLKCVGSSMFLKSKWGIGYRLSMYIDKYCATESLSSLVKQHIPGATLLQQNDQQLVYSLPFKDMDKFSGLFSALDSHSNLGVISYGVSMTTLEDVFLKLEVEAEIDQADYSVFTQQPLEEEMDSKSFDEMEQSLLILSETKAALVSTMSLWKQQMYTIAKFHFFTLKRESKSVRSVLLLLLIFFTVQIFMFLVHHSFKNAVVPIKLVPDLYFLKPGDKPHKYKTSLLLQNSADSDISDLISFFTSQNIMVTMINDSDYVSVAPHSAALNVMHSEKDYVFAAVFNSTMVYSLPILVNIISNYYLYHLNVTETIQIWSTPFFQEITDIVFKIELYFQAALLGIIVTAMPPYFAMENAENHKIKAYTQLKLSGLLPSAYWIGQAVVDIPLFFIILILMLGSLLAFHYGLYFYTVKFLAVVFCLIGYVPSVILFTYIASFTFKKILNTKEFWSFIYSVAALACIAITEITFFMGYTIATILHYAFCIIIPIYPLLGCLISFIKISWKNVRKNVDTYNPWDRLSVAVISPYLQCVLWIFLLQYYEKKYGGRSIRKDPFFRNLSTKSKNRKLPEPPDNEDEDEDVKAERLKVKELMGCQCCEEKPSIMVSNLHKEYDDKKDFLLSRKVKKVATKYISFCVKKGEILGLLGPNGAGKSTIINILVGDIEPTSGQVFLGDYSSETSEDDDSLKCMGYCPQINPLWPDTTLQEHFEIYGAVKGMSASDMKEVISRITHALDLKEHLQKTVKKLPAGIKRKLCFALSMLGNPQITLLDEPSTGMDPKAKQHMWRAIRTAFKNRKRAAILTTHYMEEAEAVCDRVAIMVSGQLRCIGTVQHLKSKFGKGYFLEIKLKDWIENLEVDRLQREIQYIFPNASRQESFSSILAYKIPKEDVQSLSQSFFKLEEAKHAFAIEEYSFSQATLEQVFVELTKEQEEEDNSCGTLNSTLWWERTQEDRVVF
234	Q8IZY2	>sp|Q8IZY2|ABCA7_HUMAN ATP-binding cassette sub-family A member 7 GN=ABCA7 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MAFWTQLMLLLWKNFMYRRRQPVQLLVELLWPLFLFFILVAVRHSHPPLEHHECHFPNKPLPSAGTVPWLQGLICNVNNTCFPQLTPGEEPGRLSNFNDSLVSRLLADARTVLGGASAHRTLAGLGKLIATLRAARSTAQPQPTKQSPLEPPMLDVAELLTSLLRTESLGLALGQAQEPLHSLLEAAEDLAQELLALRSLVELRALLQRPRGTSGPLELLSEALCSVRGPSSTVGPSLNWYEASDLMELVGQEPESALPDSSLSPACSELIGALDSHPLSRLLWRRLKPLILGKLLFAPDTPFTRKLMAQVNRTFEELTLLRDVREVWEMLGPRIFTFMNDSSNVAMLQRLLQMQDEGRRQPRPGGRDHMEALRSFLDPGSGGYSWQDAHADVGHLVGTLGRVTECLSLDKLEAAPSEAALVSRALQLLAEHRFWAGVVFLGPEDSSDPTEHPTPDLGPGHVRIKIRMDIDVVTRTNKIRDRFWDPGPAADPLTDLRYVWGGFVYLQDLVERAAVRVLSGANPRAGLYLQQMPYPCYVDDVFLRVLSRSLPLFLTLAWIYSVTLTVKAVVREKETRLRDTMRAMGLSRAVLWLGWFLSCLGPFLLSAALLVLVLKLGDILPYSHPGVVFLFLAAFAVATVTQSFLLSAFFSRANLAAACGGLAYFSLYLPYVLCVAWRDRLPAGGRVAASLLSPVAFGFGCESLALLEEQGEGAQWHNVGTRPTADVFSLAQVSGLLLLDAALYGLATWYLEAVCPGQYGIPEPWNFPFRRSYWCGPRPPKSPAPCPTPLDPKVLVEEAPPGLSPGVSVRSLEKRFPGSPQPALRGLSLDFYQGHITAFLGHNGAGKTTTLSILSGLFPPSGGSAFILGHDVRSSMAAIRPHLGVCPQYNVLFDMLTVDEHVWFYGRLKGLSAAVVGPEQDRLLQDVGLVSKQSVQTRHLSGGMQRKLSVAIAFVGGSQVVILDEPTAGVDPASRRGIWELLLKYREGRTLILSTHHLDEAELLGDRVAVVAGGRLCCCGSPLFLRRHLGSGYYLTLVKARLPLTTNEKADTDMEGSVDTRQEKKNGSQGSRVGTPQLLALVQHWVPGARLVEELPHELVLVLPYTGAHDGSFATLFRELDTRLAELRLTGYGISDTSLEEIFLKVVEECAADTDMEDGSCGQHLCTGIAGLDVTLRLKMPPQETALENGEPAGSAPETDQGSGPDAVGRVQGWALTRQQLQALLLKRFLLARRSRRGLFAQIVLPALFVGLALVFSLIVPPFGHYPALRLSPTMYGAQVSFFSEDAPGDPGRARLLEALLQEAGLEEPPVQHSSHRFSAPEVPAEVAKVLASGNWTPESPSPACQCSRPGARRLLPDCPAAAGGPPPPQAVTGSGEVVQNLTGRNLSDFLVKTYPRLVRQGLKTKKWVNEVRYGGFSLGGRDPGLPSGQELGRSVEELWALLSPLPGGALDRVLKNLTAWAHSLDAQDSLKIWFNNKGWHSMVAFVNRASNAILRAHLPPGPARHAHSITTLNHPLNLTKEQLSEGALMASSVDVLVSICVVFAMSFVPASFTLVLIEERVTRAKHLQLMGGLSPTLYWLGNFLWDMCNYLVPACIVVLIFLAFQQRAYVAPANLPALLLLLLLYGWSITPLMYPASFFFSVPSTAYVVLTCINLFIGINGSMATFVLELFSDQKLQEVSRILKQVFLIFPHFCLGRGLIDMVRNQAMADAFERLGDRQFQSPLRWEVVGKNLLAMVIQGPLFLLFTLLLQHRSQLLPQPRVRSLPLLGEEDEDVARERERVVQGATQGDVLVLRNLTKVYRGQRMPAVDRLCLGIPPGECFGLLGVNGAGKTSTFRMVTGDTLASRGEAVLAGHSVAREPSAAHLSMGYCPQSDAIFELLTGREHLELLARLRGVPEAQVAQTAGSGLARLGLSWYADRPAGTYSGGNKRKLATALALVGDPAVVFLDEPTTGMDPSARRFLWNSLLAVVREGRSVMLTSHSMEECEALCSRLAIMVNGRFRCLGSPQHLKGRFAAGHTLTLRVPAARSQPAAAFVAAEFPGAELREAHGGRLRFQLPPGGRCALARVFGELAVHGAEHGVEDFSVSQTMLEEVFLYFSKDQGKDEDTEEQKEAGVGVDPAPGLQHPKRVSQFLDDPSTAETVL
235	Q2M3G0	>sp|Q2M3G0|ABCB5_HUMAN ATP-binding cassette sub-family B member 5 GN=ABCB5 PE=1 SV=4 Homo sapiens OS=Human NCBI_TaxID=9606	MENSERAEEMQENYQRNGTAEEQPKLRKEAVGSIEIFRFADGLDITLMILGILASLVNGACLPLMPLVLGEMSDNLISGCLVQTNTTNYQNCTQSQEKLNEDMTLLTLYYVGIGVAALIFGYIQISLWIITAARQTKRIRKQFFHSVLAQDIGWFDSCDIGELNTRMTDDIDKISDGIGDKIALLFQNMSTFSIGLAVGLVKGWKLTLVTLSTSPLIMASAAACSRMVISLTSKELSAYSKAGAVAEEVLSSIRTVIAFRAQEKELQRYTQNLKDAKDFGIKRTIASKVSLGAVYFFMNGTYGLAFWYGTSLILNGEPGYTIGTVLAVFFSVIHSSYCIGAAVPHFETFAIARGAAFHIFQVIDKKPSIDNFSTAGYKPESIEGTVEFKNVSFNYPSRPSIKILKGLNLRIKSGETVALVGLNGSGKSTVVQLLQRLYDPDDGFIMVDENDIRALNVRHYRDHIGVVSQEPVLFGTTISNNIKYGRDDVTDEEMERAAREANAYDFIMEFPNKFNTLVGEKGAQMSGGQKQRIAIARALVRNPKILILDEATSALDSESKSAVQAALEKASKGRTTIVVAHRLSTIRSADLIVTLKDGMLAEKGAHAELMAKRGLYYSLVMSQDIKKADEQMESMTYSTERKTNSLPLHSVKSIKSDFIDKAEESTQSKEISLPEVSLLKILKLNKPEWPFVVLGTLASVLNGTVHPVFSIIFAKIITMFGNNDKTTLKHDAEIYSMIFVILGVICFVSYFMQGLFYGRAGEILTMRLRHLAFKAMLYQDIAWFDEKENSTGGLTTILAIDIAQIQGATGSRIGVLTQNATNMGLSVIISFIYGWEMTFLILSIAPVLAVTGMIETAAMTGFANKDKQELKHAGKIATEALENIRTIVSLTREKAFEQMYEEMLQTQHRNTSKKAQIIGSCYAFSHAFIYFAYAAGFRFGAYLIQAGRMTPEGMFIVFTAIAYGAMAIGETLVLAPEYSKAKSGAAHLFALLEKKPNIDSRSQEGKKPDTCEGNLEFREVSFFYPCRPDVFILRGLSLSIERGKTVAFVGSSGCGKSTSVQLLQRLYDPVQGQVLFDGVDAKELNVQWLRSQIAIVPQEPVLFNCSIAENIAYGDNSRVVPLDEIKEAANAANIHSFIEGLPEKYNTQVGLKGAQLSGGQKQRLAIARALLQKPKILLLDEATSALDNDSEKVVQHALDKARTGRTCLVVTHRLSAIQNADLIVVLHNGKIKEQGTHQELLRNRDIYFKLVNAQSVQ
236	Q9NP58	>sp|Q9NP58|ABCB6_HUMAN ATP-binding cassette sub-family B member 6, mitochondrial GN=ABCB6 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MVTVGNYCEAEGPVGPAWMQDGLSPCFFFTLVPSTRMALGTLALVLALPCRRRERPAGADSLSWGAGPRISPYVLQLLLATLQAALPLAGLAGRVGTARGAPLPSYLLLASVLESLAGACGLWLLVVERSQARQRLAMGIWIKFRHSPGLLLLWTVAFAAENLALVSWNSPQWWWARADLGQQVQFSLWVLRYVVSGGLFVLGLWAPGLRPQSYTLQVHEEDQDVERSQVRSAAQQSTWRDFGRKLRLLSGYLWPRGSPALQLVVLICLGLMGLERALNVLVPIFYRNIVNLLTEKAPWNSLAWTVTSYVFLKFLQGGGTGSTGFVSNLRTFLWIRVQQFTSRRVELLIFSHLHELSLRWHLGRRTGEVLRIADRGTSSVTGLLSYLVFNVIPTLADIIIGIIYFSMFFNAWFGLIVFLCMSLYLTLTIVVTEWRTKFRRAMNTQENATRARAVDSLLNFETVKYYNAESYEVERYREAIIKYQGLEWKSSASLVLLNQTQNLVIGLGLLAGSLLCAYFVTEQKLQVGDYVLFGTYIIQLYMPLNWFGTYYRMIQTNFIDMENMFDLLKEETEVKDLPGAGPLRFQKGRIEFENVHFSYADGRETLQDVSFTVMPGQTLALVGPSGAGKSTILRLLFRFYDISSGCIRIDGQDISQVTQASLRSHIGVVPQDTVLFNDTIADNIRYGRVTAGNDEVEAAAQAAGIHDAIMAFPEGYRTQVGERGLKLSGGEKQRVAIARTILKAPGIILLDEATSALDTSNERAIQASLAKVCANRTTIVVAHRLSTVVNADQILVIKDGCIVERGRHEALLSRGGVYADMWQLQQGQEETSEDTKPQTMER
237	O60706	>sp|O60706|ABCC9_HUMAN ATP-binding cassette sub-family C member 9 GN=ABCC9 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MSLSFCGNNISSYNINDGVLQNSCFVDALNLVPHVFLLFITFPILFIGWGSQSSKVQIHHNTWLHFPGHNLRWILTFALLFVHVCEIAEGIVSDSRRESRHLHLFMPAVMGFVATTTSIVYYHNIETSNFPKLLLALFLYWVMAFITKTIKLVKYCQSGLDISNLRFCITGMMVILNGLLMAVEINVIRVRRYVFFMNPQKVKPPEDLQDLGVRFLQPFVNLLSKATYWWMNTLIISAHKKPIDLKAIGKLPIAMRAVTNYVCLKDAYEEQKKKVADHPNRTPSIWLAMYRAFGRPILLSSTFRYLADLLGFAGPLCISGIVQRVNETQNGTNNTTGISETLSSKEFLENAYVLAVLLFLALILQRTFLQASYYVTIETGINLRGALLAMIYNKILRLSTSNLSMGEMTLGQINNLVAIETNQLMWFLFLCPNLWAMPVQIIMGVILLYNLLGSSALVGAAVIVLLAPIQYFIATKLAEAQKSTLDYSTERLKKTNEILKGIKLLKLYAWEHIFCKSVEETRMKELSSLKTFALYTSLSIFMNAAIPIAAVLATFVTHAYASGNNLKPAEAFASLSLFHILVTPLFLLSTVVRFAVKAIISVQKLNEFLLSDEIGDDSWRTGESSLPFESCKKHTGVQPKTINRKQPGRYHLDSYEQSTRRLRPAETEDIAIKVTNGYFSWGSGLATLSNIDIRIPTGQLTMIVGQVGCGKSSLLLAILGEMQTLEGKVHWSNVNESEPSFEATRSRNRYSVAYAAQKPWLLNATVEENITFGSPFNKQRYKAVTDACSLQPDIDLLPFGDQTEIGERGINLSGGQRQRICVARALYQNTNIVFLDDPFSALDIHLSDHLMQEGILKFLQDDKRTLVLVTHKLQYLTHADWIIAMKDGSVLREGTLKDIQTKDVELYEHWKTLMNRQDQELEKDMEADQTTLERKTLRRAMYSREAKAQMEDEDEEEEEEEDEDDNMSTVMRLRTKMPWKTCWRYLTSGGFFLLILMIFSKLLKHSVIVAIDYWLATWTSEYSINNTGKADQTYYVAGFSILCGAGIFLCLVTSLTVEWMGLTAAKNLHHNLLNKIILGPIRFFDTTPLGLILNRFSADTNIIDQHIPPTLESLTRSTLLCLSAIGMISYATPVFLVALLPLGVAFYFIQKYFRVASKDLQELDDSTQLPLLCHFSETAEGLTTIRAFRHETRFKQRMLELTDTNNIAYLFLSAANRWLEVRTDYLGACIVLTASIASISGSSNSGLVGLGLLYALTITNYLNWVVRNLADLEVQMGAVKKVNSFLTMESENYEGTMDPSQVPEHWPQEGEIKIHDLCVRYENNLKPVLKHVKAYIKPGQKVGICGRTGSGKSSLSLAFFRMVDIFDGKIVIDGIDISKLPLHTLRSRLSIILQDPILFSGSIRFNLDPECKCTDDRLWEALEIAQLKNMVKSLPGGLDAVVTEGGENFSVGQRQLFCLARAFVRKSSILIMDEATASIDMATENILQKVVMTAFADRTVVTIAHRVSSIMDAGLVLVFSEGILVECDTVPNLLAHKNGLFSTLVMTNK
238	O14678	>sp|O14678|ABCD4_HUMAN ATP-binding cassette sub-family D member 4 GN=ABCD4 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAVAGPAPGAGARPRLDLQFLQRFLQILKVLFPSWSSQNALMFLTLLCLTLLEQFVIYQVGLIPSQYYGVLGNKDLEGFKTLTFLAVMLIVLNSTLKSFDQFTCNLLYVSWRKDLTEHLHRLYFRGRAYYTLNVLRDDIDNPDQRISQDVERFCRQLSSMASKLIISPFTLVYYTYQCFQSTGWLGPVSIFGYFILGTVVNKTLMGPIVMKLVHQEKLEGDFRFKHMQIRVNAEPAAFYRAGHVEHMRTDRRLQRLLQTQRELMSKELWLYIGINTFDYLGSILSYVVIAIPIFSGVYGDLSPAELSTLVSKNAFVCIYLISCFTQLIDLSTTLSDVAGYTHRIGQLRETLLDMSLKSQDCEILGESEWGLDTPPGWPAAEPADTAFLLERVSISAPSSDKPLIKDLSLKISEGQSLLITGNTGTGKTSLLRVLGGLWTSTRGSVQMLTDFGPHGVLFLPQKPFFTDGTLREQVIYPLKEVYPDSGSADDERILRFLELAGLSNLVARTEGLDQQVDWNWYDVLSPGEMQRLSFARLFYLQPKYAVLDEATSALTEEVESELYRIGQQLGMTFISVGHRQSLEKFHSLVLKLCGGGRWELMRIKVE
239	Q8NE71	>sp|Q8NE71|ABCF1_HUMAN ATP-binding cassette sub-family F member 1 GN=ABCF1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MPKAPKQQPPEPEWIGDGESTSPSDKVVKKGKKDKKIKKTFFEELAVEDKQAGEEEKVLKEKEQQQQQQQQQQKKKRDTRKGRRKKDVDDDGEEKELMERLKKLSVPTSDEEDEVPAPKPRGGKKTKGGNVFAALIQDQSEEEEEEEKHPPKPAKPEKNRINKAVSEEQQPALKGKKGKEEKSKGKAKPQNKFAALDNEEEDKEEEIIKEKEPPKQGKEKAKKAEQGSEEEGEGEEEEEEGGESKADDPYAHLSKKEKKKLKKQMEYERQVASLKAANAAENDFSVSQAEMSSRQAMLENASDIKLEKFSISAHGKELFVNADLYIVAGRRYGLVGPNGKGKTTLLKHIANRALSIPPNIDVLLCEQEVVADETPAVQAVLRADTKRLKLLEEERRLQGQLEQGDDTAAERLEKVYEELRATGAAAAEAKARRILAGLGFDPEMQNRPTQKFSGGWRMRVSLARALFMEPTLLMLDEPTNHLDLNAVIWLNNYLQGWRKTLLIVSHDQGFLDDVCTDIIHLDAQRLHYYRGNYMTFKKMYQQKQKELLKQYEKQEKKLKELKAGGKSTKQAEKQTKEALTRKQQKCRRKNQDEESQEAPELLKRPKEYTVRFTFPDPPPLSPPVLGLHGVTFGYQGQKPLFKNLDFGIDMDSRICIVGPNGVGKSTLLLLLTGKLTPTHGEMRKNHRLKIGFFNQQYAEQLRMEETPTEYLQRGFNLPYQDARKCLGRFGLESHAHTIQICKLSGGQKARVVFAELACREPDVLILDEPTNNLDIESIDALGEAINEYKGAVIVVSHDARLITETNCQLWVVEEQSVSQIDGDFEDYKREVLEALGEVMVSRPRE
240	Q8N2K0	>sp|Q8N2K0|ABD12_HUMAN Monoacylglycerol lipase ABHD12 GN=ABHD12 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MRKRTEPVALEHERCAAAGSSSSGSAAAALDADCRLKQNLRLTGPAAAEPRCAADAGMKRALGRRKGVWLRLRKILFCVLGLYIAIPFLIKLCPGIQAKLIFLNFVRVPYFIDLKKPQDQGLNHTCNYYLQPEEDVTIGVWHTVPAVWWKNAQGKDQMWYEDALASSHPIILYLHGNAGTRGGDHRVELYKVLSSLGYHVVTFDYRGWGDSVGTPSERGMTYDALHVFDWIKARSGDNPVYIWGHSLGTGVATNLVRRLCERETPPDALILESPFTNIREEAKSHPFSVIYRYFPGFDWFFLDPITSSGIKFANDENVKHISCPLLILHAEDDPVVPFQLGRKLYSIAAPARSFRDFKVQFVPFHSDLGYRHKYIYKSPELPRILREFLGKSEPEHQH
241	Q96SE0	>sp|Q96SE0|ABHD1_HUMAN Protein ABHD1 GN=ABHD1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MLSSFLSPQNGTWADTFSLLLALAVALYLGYYWACVLQRPRLVAGPQFLAFLEPHCSITTETFYPTLWCFEGRLQSIFQVLLQSQPLVLYQSDILQTPDGGQLLLDWAKQPDSSQDPDPTTQPIVLLLPGITGSSQDTYVLHLVNQALRDGYQAVVFNNRGCRGEELRTHRAFCASNTEDLETVVNHIKHRYPQAPLLAVGISFGGILVLNHLAQARQAAGLVAALTLSACWDSFETTRSLETPLNSLLFNQPLTAGLCQLVERNRKVIEKVVDIDFVLQARTIRQFDERYTSVAFGYQDCVTYYKAASPRTKIDAIRIPVLYLSAADDPFSPVCALPIQAAQHSPYVALLITARGGHIGFLEGLLPWQHWYMSRLLHQYAKAIFQDPEGLPDLRALLPSEDRNS
242	Q8WU67	>sp|Q8WU67|ABHD3_HUMAN Phospholipase ABHD3 GN=ABHD3 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MQRLAMDLRMLSRELSLYLEHQVRVGFFGSGVGLSLILGFSVAYAFYYLSSIAKKPQLVTGGESFSRFLQDHCPVVTETYYPTVWCWEGRGQTLLRPFITSKPPVQYRNELIKTADGGQISLDWFDNDNSTCYMDASTRPTILLLPGLTGTSKESYILHMIHLSEELGYRCVVFNNRGVAGENLLTPRTYCCANTEDLETVIHHVHSLYPSAPFLAAGVSMGGMLLLNYLGKIGSKTPLMAAATFSVGWNTFACSESLEKPLNWLLFNYYLTTCLQSSVNKHRHMFVKQVDMDHVMKAKSIREFDKRFTSVMFGYQTIDDYYTDASPSPRLKSVGIPVLCLNSVDDVFSPSHAIPIETAKQNPNVALVLTSYGGHIGFLEGIWPRQSTYMDRVFKQFVQAMVEHGHELS
243	Q9BV23	>sp|Q9BV23|ABHD6_HUMAN Monoacylglycerol lipase ABHD6 GN=ABHD6 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MDLDVVNMFVIAGGTLAIPILAFVASFLLWPSALIRIYYWYWRRTLGMQVRYVHHEDYQFCYSFRGRPGHKPSILMLHGFSAHKDMWLSVVKFLPKNLHLVCVDMPGHEGTTRSSLDDLSIDGQVKRIHQFVECLKLNKKPFHLVGTSMGGQVAGVYAAYYPSDVSSLCLVCPAGLQYSTDNQFVQRLKELQGSAAVEKIPLIPSTPEEMSEMLQLCSYVRFKVPQQILQGLVDVRIPHNNFYRKLFLEIVSEKSRYSLHQNMDKIKVPTQIIWGKQDQVLDVSGADMLAKSIANCQVELLENCGHSVVMERPRKTAKLIIDFLASVHNTDNNKKLD
244	Q8IZP0	>sp|Q8IZP0|ABI1_HUMAN Abl interactor 1 GN=ABI1 PE=1 SV=4 Homo sapiens OS=Human NCBI_TaxID=9606	MAELQMLLEEEIPSGKRALIESYQNLTRVADYCENNYIQATDKRKALEETKAYTTQSLASVAYQINALANNVLQLLDIQASQLRRMESSINHISQTVDIHKEKVARREIGILTTNKNTSRTHKIIAPANMERPVRYIRKPIDYTVLDDVGHGVKWLKAKHGNNQPARTGTLSRTNPPTQKPPSPPMSGRGTLGRNTPYKTLEPVKPPTVPNDYMTSPARLGSQHSPGRTASLNQRPRTHSGSSGGSGSRENSGSSSIGIPIAVPTPSPPTIGPENISVPPPSGAPPAPPLAPLLPVSTVIAAPGSAPGSQYGTMTRQISRHNSTTSSTSSGGYRRTPSVTAQFSAQPHVNGGPLYSQNSISIAPPPPPMPQLTPQIPLTGFVARVQENIADSPTPPPPPPPDDIPMFDDSPPPPPPPPVDYEDEEAAVVQYNDPYADGDPAWAPKNYIEKVVAIYDYTKDKDDELSFMEGAIIYVIKKNDDGWYEGVCNRVTGLFPGNYVESIMHYTD
245	O14639	>sp|O14639|ABLM1_HUMAN Actin-binding LIM protein 1 GN=ABLIM1 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MPAFLGLKCLGKLCSSEKSKVTSSERTSARGSNRKRLIVEDRRVSGTSFTAHRRATITHLLYLCPKDYCPRGRVCNSVDPFVAHPQDPHHPSEKPVIHCHKCGEPCKGEVLRVQTKHFHIKCFTCKVCGCDLAQGGFFIKNGEYLCTLDYQRMYGTRCHGCGEFVEGEVVTALGKTYHPNCFACTICKRPFPPGDRVTFNGRDCLCQLCAQPMSSSPKETTFSSNCAGCGRDIKNGQALLALDKQWHLGCFKCKSCGKVLTGEYISKDGAPYCEKDYQGLFGVKCEACHQFITGKVLEAGDKHYHPSCARCSRCNQMFTEGEEMYLQGSTVWHPDCKQSTKTEEKLRPTRTSSESIYSRPGSSIPGSPGHTIYAKVDNEILDYKDLAAIPKVKAIYDIERPDLITYEPFYTSGYDDKQERQSLGESPRTLSPTPSAEGYQDVRDRMIHRSTSQGSINSPVYSRHSYTPTTSRSPQHFHRPGNEPSSGRNSPLPYRPDSRPLTPTYAQAPKHFHVPDQGINIYRKPPIYKQHAALAAQSKSSEDIIKFSKFPAAQAPDPSETPKIETDHWPGPPSFAVVGPDMKRRSSGREEDDEELLRRRQLQEEQLMKLNSGLGQLILKEEMEKESRERSSLLASRYDSPINSASHIPSSKTASLPGYGRNGLHRPVSTDFAQYNSYGDVSGGVRDYQTLPDGHMPAMRMDRGVSMPNMLEPKIFPYEMLMVTNRGRNKILREVDRTRLERHLAPEVFREIFGMSIQEFDRLPLWRRNDMKKKAKLF
246	Q6H8Q1	>sp|Q6H8Q1|ABLM2_HUMAN Actin-binding LIM protein 2 GN=ABLIM2 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MSAVSQPQAAPSPLEKSPSTAILCNTCGNVCKGEVLRVQDKYFHIKCFVCKACGCDLAEGGFFVRQGEYICTLDYQRLYGTRCFSCDQFIEGEVVSALGKTYHPDCFVCAVCRLPFPPGDRVTFNGKECMCQKCSLPVSVGSSAHLSQGLRSCGGCGTEIKNGQALVALDKHWHLGCFKCKSCGKLLNAEYISKDGLPYCEADYHAKFGIRCDSCEKYITGRVLEAGEKHYHPSCALCVRCGQMFAEGEEMYLQGSSIWHPACRQAARTEDRNKETRTSSESIISVPASSTSGSPSRVIYAKLGGEILDYRDLAALPKSKAIYDIDRPDMISYSPYISHSAGDRQSYGEGDQDDRSYKQCRTSSPSSTGSVSLGRYTPTSRSPQHYSRPGSESGRSTPSLSVLSDSKPPPSTYQQAPRHFHVPDTGVKDNIYRKPPIYRQHAARRSDGEDGSLDQDNRKKSSWLMLKGDADTRTNSPDLDTQSLSHSSGTDRDPLQRMAGDSFHSRFPYSKSDPLPGHGKNGLDQRNANLAPCGADPDASWGMREYKIYPYDSLIVTNRIRVKLPKDVDRTRLERHLSPEEFQEVFGMSIEEFDRLALWKRNDLKKKALLF
247	Q9P1F3	>sp|Q9P1F3|ABRAL_HUMAN Costars family protein ABRACL GN=ABRACL PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MNVDHEVNLLVEEIHRLGSKNADGKLSVKFGVLFRDDKCANLFEALVGTLKAAKRRKIVTYPGELLLQGVHDDVDIILLQD
248	Q8N0Z2	>sp|Q8N0Z2|ABRA_HUMAN Actin-binding Rho-activating protein GN=ABRA PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAPGEKESGEGPAKSALRKIRTATLVISLARGWQQWANENSIRQAQEPTGWLPGGTQDSPQAPKPITPPTSHQKAQSAPKSPPRLPEGHGDGQSSEKAPEVSHIKKKEVSKTVVSKTYERGGDVSHLSHRYERDAGVLEPGQPENDIDRILHSHGSPTRRRKCANLVSELTKGWRVMEQEEPTWRSDSVDTEDSGYGGEAEERPEQDGVQVAVVRIKRPLPSQVNRFTEKLNCKAQQKYSPVGNLKGRWQQWADEHIQSQKLNPFSEEFDYELAMSTRLHKGDEGYGRPKEGTKTAERAKRAEEHIYREMMDMCFIICTMARHRRDGKIQVTFGDLFDRYVRISDKVVGILMRARKHGLVDFEGEMLWQGRDDHVVITLLK
249	P07108	>sp|P07108|ACBP_HUMAN Acyl-CoA-binding protein GN=DBI PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MSQAEFEKAAEEVRHLKTKPSDEEMLFIYGHYKQATVGDINTERPGMLDFTGKAKWDAWNELKGTSKEDAMKAYINKVEELKKKYGI
250	Q8TDN7	>sp|Q8TDN7|ACER1_HUMAN Alkaline ceramidase 1 GN=ACER1 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MPSIFAYQSSEVDWCESNFQYSELVAEFYNTFSNIPFFIFGPLMMLLMHPYAQKRSRYIYVVWVLFMIIGLFSMYFHMTLSFLGQLLDEIAILWLLGSGYSIWMPRCYFPSFLGGNRSQFIRLVFITTVVSTLLSFLRPTVNAYALNSIALHILYIVCQEYRKTSNKELRHLIEVSVVLWAVALTSWISDRLLCSFWQRIHFFYLHSIWHVLISITFPYGMVTMALVDANYEMPGETLKVRYWPRDSWPVGLPYVEIRGDDKDC
251	Q9NUN7	>sp|Q9NUN7|ACER3_HUMAN Alkaline ceramidase 3 GN=ACER3 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MAPAADREGYWGPTTSTLDWCEENYSVTWYIAEFWNTVSNLIMIIPPMFGAVQSVRDGLEKRYIASYLALTVVGMGSWCFHMTLKYEMQLLDELPMIYSCCIFVYCMFECFKIKNSVNYHLLFTLVLFSLIVTTVYLKVKEPIFHQVMYGMLVFTLVLRSIYIVTWVYPWLRGLGYTSLGIFLLGFLFWNIDNIFCESLRNFRKKVPPIIGITTQFHAWWHILTGLGSYLHILFSLYTRTLYLRYRPKVKFLFGIWPVILFEPLRKH
252	P43681	>sp|P43681|ACHA4_HUMAN Neuronal acetylcholine receptor subunit alpha-4 GN=CHRNA4 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MELGGPGAPRLLPPLLLLLGTGLLRASSHVETRAHAEERLLKKLFSGYNKWSRPVANISDVVLVRFGLSIAQLIDVDEKNQMMTTNVWVKQEWHDYKLRWDPADYENVTSIRIPSELIWRPDIVLYNNADGDFAVTHLTKAHLFHDGRVQWTPPAIYKSSCSIDVTFFPFDQQNCTMKFGSWTYDKAKIDLVNMHSRVDQLDFWESGEWVIVDAVGTYNTRKYECCAEIYPDITYAFVIRRLPLFYTINLIIPCLLISCLTVLVFYLPSECGEKITLCISVLLSLTVFLLLITEIIPSTSLVIPLIGEYLLFTMIFVTLSIVITVFVLNVHHRSPRTHTMPTWVRRVFLDIVPRLLLMKRPSVVKDNCRRLIESMHKMASAPRFWPEPEGEPPATSGTQSLHPPSPSFCVPLDVPAEPGPSCKSPSDQLPPQQPLEAEKASPHPSPGPCRPPHGTQAPGLAKARSLSVQHMSSPGEAVEGGVRCRSRSIQYCVPRDDAAPEADGQAAGALASRNTHSAELPPPDQPSPCKCTCKKEPSSVSPSATVKTRSTKAPPPHLPLSPALTRAVEGVQYIADHLKAEDTDFSVKEDWKYVAMVIDRIFLWMFIIVCLLGTVGLFLPPWLAGMI
253	Q07001	>sp|Q07001|ACHD_HUMAN Acetylcholine receptor subunit delta GN=CHRND PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MEGPVLTLGLLAALAVCGSWGLNEEERLIRHLFQEKGYNKELRPVAHKEESVDVALALTLSNLISLKEVEETLTTNVWIEHGWTDNRLKWNAEEFGNISVLRLPPDMVWLPEIVLENNNDGSFQISYSCNVLVYHYGFVYWLPPAIFRSSCPISVTYFPFDWQNCSLKFSSLKYTAKEITLSLKQDAKENRTYPVEWIIIDPEGFTENGEWEIVHRPARVNVDPRAPLDSPSRQDITFYLIIRRKPLFYIINILVPCVLISFMVNLVFYLPADSGEKTSVAISVLLAQSVFLLLISKRLPATSMAIPLIGKFLLFGMVLVTMVVVICVIVLNIHFRTPSTHVLSEGVKKLFLETLPELLHMSRPAEDGPSPGALVRRSSSLGYISKAEEYFLLKSRSDLMFEKQSERHGLARRLTTARRPPASSEQAQQELFNELKPAVDGANFIVNHMRDQNNYNEEKDSWNRVARTVDRLCLFVVTPVMVVGTAWIFLQGVYNQPPPQPFPGDPYSYNVQDKRFI
254	Q9Y615	>sp|Q9Y615|ACL7A_HUMAN Actin-like protein 7A GN=ACTL7A PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MWAPPAAIMGDGPTKKVGNQAPLQTQALQTASLRDGPAKRAVWVRHTSSEPQEPTESKAAKERPKQEVTKAVVVDLGTGYCKCGFAGLPRPTHKISTTVGKPYMETAKTGDNRKETFVGQELNNTNVHLKLVNPLRHGIIVDWDTVQDIWEYLFRQEMKIAPEEHAVLVSDPPLSPHTNREKYAEMLFEAFNTPAMHIAYQSRLSMYSYGRTSGLVVEVGHGVSYVVPIYEGYPLPSITGRLDYAGSDLTAYLLGLLNSAGNEFTQDQMGIVEDIKKKCCFVALDPIEEKKVPLSEHTIRYVLPDGKEIQLCQERFLCSEMFFKPSLIKSMQLGLHTQTVSCLNKCDIALKRDLMGNILLCGGSTMLSGFPNRLQKELSSMCPNDTPQVNVLPERDSAVWTGGSILASLQGFQPLWVHRFEYEEHGPFFLYRRCF
255	Q8WYK0	>sp|Q8WYK0|ACO12_HUMAN Acyl-coenzyme A thioesterase 12 GN=ACOT12 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MERPAPGEVVMSQAIQPAHATARGELSAGQLLKWIDTTACLAAEKHAGVSCVTASVDDIQFEETARVGQVITIKAKVTRAFSTSMEISIKVMVQDMLTGIEKLVSVAFSTFVAKPVGKEKIHLKPVTLLTEQDHVEHNLAAERRKVRLQHEDTFNNLMKESSKFDDLIFDEEEGAVSTRGTSVQSIELVLPPHANHHGNTFGGQIMAWMETVATISASRLCWAHPFLKSVDMFKFRGPSTVGDRLVFTAIVNNTFQTCVEVGVRVEAFDCQEWAEGRGRHINSAFLIYNAADDKENLITFPRIQPISKDDFRRYRGAIARKRIRLGRKYVISHKEEVPLCIHWDISKQASLSDSNVEALKKLAAKRGWEVTSTVEKIKIYTLEEHDVLSVWVEKHVGSPAHLAYRLLSDFTKRPLWDPHFVSCEVIDWVSEDDQLYHITCPILNDDKPKDLVVLVSRRKPLKDGNTYTVAVKSVILPSVPPSPQYIRSEIICAGFLIHAIDSNSCIVSYFNHMSASILPYFAGNLGGWSKSIEETAASCIQFLENPPDDGFVSTF
256	Q9NUB1	>sp|Q9NUB1|ACS2L_HUMAN Acetyl-coenzyme A synthetase 2-like, mitochondrial GN=ACSS1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAARTLGRGVGRLLGSLRGLSGQPARPPCGVSAPRRAASGPSGSAPAVAAAAAQPGSYPALSAQAAREPAAFWGPLARDTLVWDTPYHTVWDCDFSTGKIGWFLGGQLNVSVNCLDQHVRKSPESVALIWERDEPGTEVRITYRELLETTCRLANTLKRHGVHRGDRVAIYMPVSPLAVAAMLACARIGAVHTVIFAGFSAESLAGRINDAKCKVVITFNQGLRGGRVVELKKIVDEAVKHCPTVQHVLVAHRTDNKVHMGDLDVPLEQEMAKEDPVCAPESMGSEDMLFMLYTSGSTGMPKGIVHTQAGYLLYAALTHKLVFDHQPGDIFGCVADIGWITGHSYVVYGPLCNGATSVLFESTPVYPNAGRYWETVERLKINQFYGAPTAVRLLLKYGDAWVKKYDRSSLRTLGSVGEPINCEAWEWLHRVVGDSRCTLVDTWWQTETGGICIAPRPSEEGAEILPAMAMRPFFGIVPVLMDEKGSVVEGSNVSGALCISQAWPGMARTIYGDHQRFVDAYFKAYPGYYFTGDGAYRTEGGYYQITGRMDDVINISGHRLGTAEIEDAIADHPAVPESAVIGYPHDIKGEAAFAFIVVKDSAGDSDVVVQELKSMVATKIAKYAVPDEILVVKRLPKTRSGKVMRRLLRKIITSEAQELGDTTTLEDPSIIAEILSVYQKCKDKQAAAK
257	Q4L235	>sp|Q4L235|ACSF4_HUMAN Acyl-CoA synthetase family member 4 GN=AASDH PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MTLQELVHKAASCYMDRVAVCFDECNNQLPVYYTYKTVVNAASELSNFLLLHCDFQGIREIGLYCQPGIDLPSWILGILQVPAAYVPIEPDSPPSLSTHFMKKCNLKYILVEKKQINKFKSFHETLLNYDTFTVEHNDLVLFRLHWKNTEVNLMLNDGKEKYEKEKIKSISSEHVNEEKAEEHMDLRLKHCLAYVLHTSGTTGIPKIVRVPHKCIVPNIQHFRVLFDITQEDVLFLASPLTFDPSVVEIFLALSSGASLLIVPTSVKLLPSKLASVLFSHHRVTVLQATPTLLRRFGSQLIKSTVLSATTSLRVLALGGEAFPSLTVLRSWRGEGNKTQIFNVYGITEVSSWATIYRIPEKTLNSTLKCELPVQLGFPLLGTVVEVRDTNGFTIQEGSGQVFLGGRNRVCFLDDEVTVPLGTMRATGDFVTVKDGEIFFLGRKDSQIKRHGKRLNIELVQQVAEELQQVESCAVTWYNQEKLILFMVSKDASVKEYIFKELQKYLPSHAVPDELVLIDSLPFTSHGKIDVSELNKIYLNYINLKSENKLSGKEDLWEKLQYLWKSTLNLPEDLLRVPDESLFLNSGGDSLKSIRLLSEIEKLVGTSVPGLLEIILSSSILEIYNHILQTVVPDEDVTFRKSCATKRKLSDINQEEASGTSLHQKAIMTFTCHNEINAFVVLSRGSQILSLNSTRFLTKLGHCSSACPSDSVSQTNIQNLKGLNSPVLIGKSKDPSCVAKVSEEGKPAIGTQKMELHVRWRSDTGKCVDASPLVVIPTFDKSSTTVYIGSHSHRMKAVDFYSGKVKWEQILGDRIESSACVSKCGNFIVVGCYNGLVYVLKSNSGEKYWMFTTEDAVKSSATMDPTTGLIYIGSHDQHAYALDIYRKKCVWKSKCGGTVFSSPCLNLIPHHLYFATLGGLLLAVNPATGNVIWKHSCGKPLFSSPQCCSQYICIGCVDGNLLCFTHFGEQVWQFSTSGPIFSSPCTSPSEQKIFFGSHDCFIYCCNMKGHLQWKFETTSRVYATPFAFHNYNGSNEMLLAAASTDGKVWILESQSGQLQSVYELPGEVFSSPVVLESMLIIGCRDNYVYCLDLLGGNQK
258	Q8TC94	>sp|Q8TC94|ACTL9_HUMAN Actin-like protein 9 GN=ACTL9 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MDASRPKSSESQSSLEAPRPGPNPSPNVVNKPLQRDFPGMVADRLPPKTGVVVIDMGTGTCKVGFAGQASPTYTVATILGCQPKKPATSGQSGLQTFIGEAARVLPELTLVQPLRSGIVVDWDAAELIWRHLLEHDLRVATHDHPLLFSDPPFSPATNREKLVEVAFESLRSPAMYVASQSVLSVYAHGRVSGLVVDTGHGVTYTVPVFQGYNLLHATERLDLAGNHLTAFLAEMLLQAGLPLGQQDLDLVENIKHHYCYVASDFQKEQARPEQEYKRTLKLPDGRTVTLGKELFQCPELLFNPPEVPGLSPVGLSTMAKQSLRKLSLEMRADLAQNVLLCGGSSLFTGFEGRFRAELLRALPAETHVVVAAQPTRNFSVWIGGSILASLRAFQSCWVLREQYEEQGPYIVYRKCY
259	Q03154	>sp|Q03154|ACY1_HUMAN Aminoacylase-1 GN=ACY1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MTSKGPEEEHPSVTLFRQYLRIRTVQPKPDYGAAVAFFEETARQLGLGCQKVEVAPGYVVTVLTWPGTNPTLSSILLNSHTDVVPVFKEHWSHDPFEAFKDSEGYIYARGAQDMKCVSIQYLEAVRRLKVEGHRFPRTIHMTFVPDEEVGGHQGMELFVQRPEFHALRAGFALDEGIANPTDAFTVFYSERSPWWVRVTSTGRPGHASRFMEDTAAEKLHKVVNSILAFREKEWQRLQSNPHLKEGSVTSVNLTKLEGGVAYNVIPATMSASFDFRVAPDVDFKAFEEQLQSWCQAAGEGVTLEFAQKWMHPQVTPTDDSNPWWAAFSRVCKDMNLTLEPEIMPAATDNRYIRAVGVPALGFSPMNRTPVLLHDHDERLHEAVFLRGVDIYTRLLPALASVPALPSDS
260	P11171	>sp|P11171|41_HUMAN Protein 4.1 GN=EPB41 PE=1 SV=4 Homo sapiens OS=Human NCBI_TaxID=9606	MTTEKSLVTEAENSQHQQKEEGEEAINSGQQEPQQEESCQTAAEGDNWCEQKLKASNGDTPTHEDLTKNKERTSESRGLSRLFSSFLKRPKSQVSEEEGKEVESDKEKGEGGQKEIEFGTSLDEEIILKAPIAAPEPELKTDPSLDLHSLSSAETQPAQEELREDPDFEIKEGEGLEECSKIEVKEESPQSKAETELKASQKPIRKHRNMHCKVSLLDDTVYECVVEKHAKGQDLLKRVCEHLNLLEEDYFGLAIWDNATSKTWLDSAKEIKKQVRGVPWNFTFNVKFYPPDPAQLTEDITRYYLCLQLRQDIVAGRLPCSFATLALLGSYTIQSELGDYDPELHGVDYVSDFKLAPNQTKELEEKVMELHKSYRSMTPAQADLEFLENAKKLSMYGVDLHKAKDLEGVDIILGVCSSGLLVYKDKLRINRFPWPKVLKISYKRSSFFIKIRPGEQEQYESTIGFKLPSYRAAKKLWKVCVEHHTFFRLTSTDTIPKSKFLALGSKFRYSGRTQAQTRQASALIDRPAPHFERTASKRASRSLDGAAAVDSADRSPRPTSAPAITQGQVAEGGVLDASAKKTVVPKAQKETVKAEVKKEDEPPEQAEPEPTEAWKVEKTHIEVTVPTSNGDQTQKLAEKTEDLIRMRKKKRERLDGENIYIRHSNLMLEDLDKSQEEIKKHHASISELKKNFMESVPEPRPSEWDKRLSTHSPFRTLNINGQIPTGEGPPLVKTQTVTISDNANAVKSEIPTKDVPIVHTETKTITYEAAQTDDNSGDLDPGVLLTAQTITSETPSSTTTTQITKTVKGGISETRIEKRIVITGDADIDHDQVLVQAIKEAKEQHPDMSVTKVVVHQETEIADE
261	Q9NRA8	>sp|Q9NRA8|4ET_HUMAN Eukaryotic translation initiation factor 4E transporter GN=EIF4ENIF1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MDRRSMGETESGDAFLDLKKPPASKCPHRYTKEELLDIKELPHSKQRPSCLSEKYDSDGVWDPEKWHASLYPASGRSSPVESLKKELDTDRPSLVRRIVDPRERVKEDDLDVVLSPQRRSFGGGCHVTAAVSSRRSGSPLEKDSDGLRLLGGRRIGSGRIISARTFEKDHRLSDKDLRDLRDRDRERDFKDKRFRREFGDSKRVFGERRRNDSYTEEEPEWFSAGPTSQSETIELTGFDDKILEEDHKGRKRTRRRTASVKEGIVECNGGVAEEDEVEVILAQEPAADQEVPRDAVLPEQSPGDFDFNEFFNLDKVPCLASMIEDVLGEGSVSASRFSRWFSNPSRSGSRSSSLGSTPHEELERLAGLEQAILSPGQNSGNYFAPIPLEDHAENKVDILEMLQKAKVDLKPLLSSLSANKEKLKESSHSGVVLSVEEVEAGLKGLKVDQQVKNSTPFMAEHLEETLSAVTNNRQLKKDGDMTAFNKLVSTMKASGTLPSQPKVSRNLESHLMSPAEIPGQPVPKNILQELLGQPVQRPASSNLLSGLMGSLEPTTSLLGQRAPSPPLSQVFQTRAASADYLRPRIPSPIGFTPGPQQLLGDPFQGMRKPMSPITAQMSQLELQQAALEGLALPHDLAVQAANFYQPGFGKPQVDRTRDGFRNRQQRVTKSPAPVHRGNSSSPAPAASITSMLSPSFTPTSVIRKMYESKEKSKEEPASGKAALGDSKEDTQKASEENLLSSSSVPSADRDSSPTTNSKLSALQRSSCSTPLSQANRYTKEQDYRPKATGRKTPTLASPVPTTPFLRPVHQVPLVPHVPMVRPAHQLHPGLVQRMLAQGVHPQHLPSLLQTGVLPPGMDLSHLQGISGPILGQPFYPLPAASHPLLNPRPGTPLHLAMVQQQLQRSVLHPPGSGSHAAAVSVQTTPQNVPSRSGLPHMHSQLEHRPSQRSSSPVGLAKWFGSDVLQQPLPSMPAKVISVDELEYRQ
262	P08195	>sp|P08195|4F2_HUMAN 4F2 cell-surface antigen heavy chain GN=SLC3A2 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MELQPPEASIAVVSIPRQLPGSHSEAGVQGLSAGDDSELGSHCVAQTGLELLASGDPLPSASQNAEMIETGSDCVTQAGLQLLASSDPPALASKNAEVTGTMSQDTEVDMKEVELNELEPEKQPMNAASGAAMSLAGAEKNGLVKIKVAEDEAEAAAAAKFTGLSKEELLKVAGSPGWVRTRWALLLLFWLGWLGMLAGAVVIIVRAPRCRELPAQKWWHTGALYRIGDLQAFQGHGAGNLAGLKGRLDYLSSLKVKGLVLGPIHKNQKDDVAQTDLLQIDPNFGSKEDFDSLLQSAKKKSIRVILDLTPNYRGENSWFSTQVDTVATKVKDALEFWLQAGVDGFQVRDIENLKDASSFLAEWQNITKGFSEDRLLIAGTNSSDLQQILSLLESNKDLLLTSSYLSDSGSTGEHTKSLVTQYLNATGNRWCSWSLSQARLLTSFLPAQLLRLYQLMLFTLPGTPVFSYGDEIGLDAAALPGQPMEAPVMLWDESSFPDIPGAVSANMTVKGQSEDPGSLLSLFRRLSDQRSKERSLLHGDFHAFSAGPGLFSYIRHWDQNERFLVVLNFGDVGLSAGLQASDLPASASLPAKADLLLSTQPGREEGSPLELERLKLEPHEGLLLRFPYAA
263	P08908	>sp|P08908|5HT1A_HUMAN 5-hydroxytryptamine receptor 1A GN=HTR1A PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MDVLSPGQGNNTTSPPAPFETGGNTTGISDVTVSYQVITSLLLGTLIFCAVLGNACVVAAIALERSLQNVANYLIGSLAVTDLMVSVLVLPMAALYQVLNKWTLGQVTCDLFIALDVLCCTSSILHLCAIALDRYWAITDPIDYVNKRTPRRAAALISLTWLIGFLISIPPMLGWRTPEDRSDPDACTISKDHGYTIYSTFGAFYIPLLLMLVLYGRIFRAARFRIRKTVKKVEKTGADTRHGASPAPQPKKSVNGESGSRNWRLGVESKAGGALCANGAVRQGDDGAALEVIEVHRVGNSKEHLPLPSEAGPTPCAPASFERKNERNAEAKRKMALARERKTVKTLGIIMGTFILCWLPFFIVALVLPFCESSCHMPTLLGAIINWLGYSNSLLNPVIYAYFNKDFQNAFKKIIKCKFCRQ
264	P46098	>sp|P46098|5HT3A_HUMAN 5-hydroxytryptamine receptor 3A GN=HTR3A PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLLWVQQALLALLLPTLLAQGEARRSRNTTRPALLRLSDYLLTNYRKGVRPVRDWRKPTTVSIDVIVYAILNVDEKNQVLTTYIWYRQYWTDEFLQWNPEDFDNITKLSIPTDSIWVPDILINEFVDVGKSPNIPYVYIRHQGEVQNYKPLQVVTACSLDIYNFPFDVQNCSLTFTSWLHTIQDINISLWRLPEKVKSDRSVFMNQGEWELLGVLPYFREFSMESSNYYAEMKFYVVIRRRPLFYVVSLLLPSIFLMVMDIVGFYLPPNSGERVSFKITLLLGYSVFLIIVSDTLPATAIGTPLIGVYFVVCMALLVISLAETIFIVRLVHKQDLQQPVPAWLRHLVLERIAWLLCLREQSTSQRPPATSQATKTDDCSAMGNHCSHMGGPQDFEKSPRDRCSPPPPPREASLAVCGLLQELSSIRQFLEKRDEIREVARDWLRVGSVLDKLLFHIYLLAVLAYSITLVMLWSIWQYA
265	Q70Z44	>sp|Q70Z44|5HT3D_HUMAN 5-hydroxytryptamine receptor 3D GN=HTR3D PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MQKHSPGPPALALLSQSLLTTGNGDTLIINCPGFGQHRVDPAAFQAVFDRKAIGPVTNYSVATHVNISFTLSAIWNCYSRIHTFNCHHARPWHNQFVQWNPDECGGIKKSGMATENLWLSDVFIEESVDQTPAGLMASMSIVKATSNTISQCGWSASANWTPSISPSMDRARAWRRMSRSFQIHHRTSFRTRREWVLLGIQKRTIKVTVATNQYEQAIFHVAIRRRCRPSPYVVNFLVPSGILIAIDALSFYLPLESGNCAPFKMTVLLGYSVFLLMMNDLLPATSTSSHASLVAPLALMQTPLPAGVYFALCLSLMVGSLLETIFITHLLHVATTQPLPLPRWLHSLLLHCTGQGRCCPTAPQKGNKGPGLTPTHLPGVKEPEVSAGQMPGPGEAELTGGSEWTRAQREHEAQKQHSVELWVQFSHAMDALLFRLYLLFMASSIITVICLWNT
266	P47898	>sp|P47898|5HT5A_HUMAN 5-hydroxytryptamine receptor 5A GN=HTR5A PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MDLPVNLTSFSLSTPSPLETNHSLGKDDLRPSSPLLSVFGVLILTLLGFLVAATFAWNLLVLATILRVRTFHRVPHNLVASMAVSDVLVAALVMPLSLVHELSGRRWQLGRRLCQLWIACDVLCCTASIWNVTAIALDRYWSITRHMEYTLRTRKCVSNVMIALTWALSAVISLAPLLFGWGETYSEGSEECQVSREPSYAVFSTVGAFYLPLCVVLFVYWKIYKAAKFRVGSRKTNSVSPISEAVEVKDSAKQPQMVFTVRHATVTFQPEGDTWREQKEQRAALMVGILIGVFVLCWIPFFLTELISPLCSCDIPAIWKSIFLWLGYSNSFFNPLIYTAFNKNYNSAFKNFFSRQH
267	Q96P26	>sp|Q96P26|5NT1B_HUMAN Cytosolic 5'-nucleotidase 1B GN=NT5C1B PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MSQTSLKQKKNEPGMRSSKESLEAEKRKESDKTGVRLSNQMRRAVNPNHSLRCCPFQGHSSCRRCLCAAEGTALGPCHTIRIYIHMCLLWEQGQQITMMRGSQESSLRKTDSRGYLVRSQWSRISRSPSTKAPSIDEPRSRNTSAKLPSSSTSSRTPSTSPSLHDSSPPPLSGQPSLQPPASPQLPRSLDSRPPTPPEPDPGSRRSTKMQENPEAWAQGIVREIRQTRDSQPLEYSRTSPTEWKSSSQRRGIYPASTQLDRNSLSEQQQQQREDEDDYEAAYWASMRSFYEKNPSCSRPWPPKPKNAITIALSSCALFNMVDGRKIYEQEGLEKYMEYQLTNENVILTPGPAFRFVKALQYVNARLRDLYPDEQDLFDIVLMTNNHAQVGVRLINSVNHYGLLIDRFCLTGGKDPIGYLKAYLTNLYIAADSEKVQEAIQEGIASATMFDGAKDMAYCDTQLRVAFDGDAVLFSDESEHFTKEHGLDKFFQYDTLCESKPLAQGPLKGFLEDLGRLQKKFYAKNERLLCPIRTYLVTARSAASSGARVLKTLRRWGLEIDEALFLAGAPKSPILVKIRPHIFFDDHMFHIEGAQRLGSIAAYGFNKKFSS
268	P21589	>sp|P21589|5NTD_HUMAN 5'-nucleotidase GN=NT5E PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MCPRAARAPATLLLALGAVLWPAAGAWELTILHTNDVHSRLEQTSEDSSKCVNASRCMGGVARLFTKVQQIRRAEPNVLLLDAGDQYQGTIWFTVYKGAEVAHFMNALRYDAMALGNHEFDNGVEGLIEPLLKEAKFPILSANIKAKGPLASQISGLYLPYKVLPVGDEVVGIVGYTSKETPFLSNPGTNLVFEDEITALQPEVDKLKTLNVNKIIALGHSGFEMDKLIAQKVRGVDVVVGGHSNTFLYTGNPPSKEVPAGKYPFIVTSDDGRKVPVVQAYAFGKYLGYLKIEFDERGNVISSHGNPILLNSSIPEDPSIKADINKWRIKLDNYSTQELGKTIVYLDGSSQSCRFRECNMGNLICDAMINNNLRHTDEMFWNHVSMCILNGGGIRSPIDERNNGTITWENLAAVLPFGGTFDLVQLKGSTLKKAFEHSVHRYGQSTGEFLQVGGIHVVYDLSRKPGDRVVKLDVLCTKCRVPSYDPLKMDEVYKVILPNFLANGGDGFQMIKDELLRHDSGDQDINVVSTYISKMKVIYPAVEGRIKFSTGSHCHGSFSLIFLSLWAVIFVLYQ
269	P56378	>sp|P56378|68MP_HUMAN 6.8 kDa mitochondrial proteolipid GN=MP68 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLQSIIKNIWIPMKPYYTKVYQEIWIGMGLMGFIVYKIRAADKRSKALKASAPAPGHH
270	P19652	>sp|P19652|A1AG2_HUMAN Alpha-1-acid glycoprotein 2 GN=ORM2 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MALSWVLTVLSLLPLLEAQIPLCANLVPVPITNATLDRITGKWFYIASAFRNEEYNKSVQEIQATFFYFTPNKTEDTIFLREYQTRQNQCFYNSSYLNVQRENGTVSRYEGGREHVAHLLFLRDTKTLMFGSYLDDEKNWGLSFYADKPETTKEQLGEFYEALDCLCIPRSDVMYTDWKKDKCEPLEKQHEKERKQEEGES
271	U3KPV4	>sp|U3KPV4|A3LT2_HUMAN Alpha-1,3-galactosyltransferase 2 GN=A3GALT2 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MALKEGLRAWKRIFWRQILLTLGLLGLFLYGLPKFRHLEALIPMGVCPSATMSQLRDNFTGALRPWARPEVLTCTPWGAPIIWDGSFDPDVAKQEARQQNLTIGLTIFAVGRYLEKYLERFLETAEQHFMAGQSVMYYVFTELPGAVPRVALGPGRRLPVERVARERRWQDVSMARMRTLHAALGGLPGREAHFMFCMDVDQHFSGTFGPEALAESVAQLHSWHYHWPSWLLPFERDAHSAAAMAWGQGDFYNHAAVFGGSVAALRGLTAHCAGGLDWDRARGLEARWHDESHLNKFFWLHKPAKVLSPEFCWSPDIGPRAEIRRPRLLWAPKGYRLLRN
272	Q7RTV5	>sp|Q7RTV5|AAED1_HUMAN Thioredoxin-like protein AAED1 GN=AAED1 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAAPAPVTRQVSGAAALVPAPSGPDSGQPLAAAVAELPVLDARGQRVPFGALFRERRAVVVFVRHFLCYICKEYVEDLAKIPRSFLQEANVTLIVIGQSSYHHIEPFCKLTGYSHEIYVDPEREIYKRLGMKRGEEIASSGQSPHIKSNLLSGSLQSLWRAVTGPLFDFQGDPAQQGGTLILGPGNNIHFIHRDRNRLDHKPINSVLQLVGVQHVNFTNRPSVIHV
273	Q8N139	>sp|Q8N139|ABCA6_HUMAN ATP-binding cassette sub-family A member 6 GN=ABCA6 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MNMKQKSVYQQTKALLCKNFLKKWRMKRESLLEWGLSILLGLCIALFSSSMRNVQFPGMAPQNLGRVDKFNSSSLMVVYTPISNLTQQIMNKTALAPLLKGTSVIGAPNKTHMDEILLENLPYAMGIIFNETFSYKLIFFQGYNSPLWKEDFSAHCWDGYGEFSCTLTKYWNRGFVALQTAINTAIIEITTNHPVMEELMSVTAITMKTLPFITKNLLHNEMFILFFLLHFSPLVYFISLNVTKERKKSKNLMKMMGLQDSAFWLSWGLIYAGFIFIISIFVTIIITFTQIIVMTGFMVIFILFFLYGLSLVALVFLMSVLLKKAVLTNLVVFLLTLFWGCLGFTVFYEQLPSSLEWILNICSPFAFTTGMIQIIKLDYNLNGVIFPDPSGDSYTMIATFSMLLLDGLIYLLLALYFDKILPYGDERHYSPLFFLNSSSCFQHQRTNAKVIEKEIDAEHPSDDYFEPVAPEFQGKEAIRIRNVKKEYKGKSGKVEALKGLLFDIYEGQITAILGHSGAGKSSLLNILNGLSVPTEGSVTIYNKNLSEMQDLEEIRKITGVCPQFNVQFDILTVKENLSLFAKIKGIHLKEVEQEVQRILLELDMQNIQDNLAKHLSEGQKRKLTFGITILGDPQILLLDEPTTGLDPFSRDQVWSLLRERRADHVILFSTQSMDEADILADRKVIMSNGRLKCAGSSMFLKRRWGLGYHLSLHRNEICNPEQITSFITHHIPDAKLKTENKEKLVYTLPLERTNTFPDLFSDLDKCSDQGVTGYDISMSTLNEVFMKLEGQSTIEQDFEQVEMIRDSESLNEMELAHSSFSEMQTAVSDMGLWRMQVFAMARLRFLKLKRQTKVLLTLLLVFGIAIFPLIVENIMYAMLNEKIDWEFKNELYFLSPGQLPQEPRTSLLIINNTESNIEDFIKSLKHQNILLEVDDFENRNGTDGLSYNGAIIVSGKQKDYRFSVVCNTKRLHCFPILMNIISNGLLQMFNHTQHIRIESSPFPLSHIGLWTGLPDGSFFLFLVLCSISPYITMGSISDYKKNAKSQLWISGLYTSAYWCGQALVDVSFFILILLLMYLIFYIENMQYLLITSQIVFALVIVTPGYAASLVFFIYMISFIFRKRRKNSGLWSFYFFFASTIMFSITLINHFDLSILITTMVLVPSYTLLGFKTFLEVRDQEHYREFPEANFELSATDFLVCFIPYFQTLLFVFVLRCMELKCGKKRMRKDPVFRISPQSRDAKPNPEEPIDEDEDIQTERIRTATALTTSILDEKPVIIASCLHKEYAGQKKSCFSKRKKKIAARNISFCVQEGEILGLLGPNGAGKSSSIRMISGITKPTAGEVELKGCSSVLGHLGYCPQENVLWPMLTLREHLEVYAAVKGLRKADARLAIARLVSAFKLHEQLNVPVQKLTAGITRKLCFVLSLLGNSPVLLLDEPSTGIDPTGQQQMWQAIQAVVKNTERGVLLTTHNLAEAEALCDRVAIMVSGRLRCIGSIQHLKNKLGKDYILELKVKETSQVTLVHTEILKLFPQAAGQERYSSLLTYKLPVADVYPLSQTFHKLEAVKHNFNLEEYSLSQCTLEKVFLELSKEQEVGNFDEEIDTTMRWKLLPHSDEP
274	Q8IUA7	>sp|Q8IUA7|ABCA9_HUMAN ATP-binding cassette sub-family A member 9 GN=ABCA9 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MSKRRMSVGQQTWALLCKNCLKKWRMKRQTLLEWLFSFLLVLFLYLFFSNLHQVHDTPQMSSMDLGRVDSFNDTNYVIAFAPESKTTQEIMNKVASAPFLKGRTIMGWPDEKSMDELDLNYSIDAVRVIFTDTFSYHLKFSWGHRIPMMKEHRDHSAHCQAVNEKMKCEGSEFWEKGFVAFQAAINAAIIEIATNHSVMEQLMSVTGVHMKILPFVAQGGVATDFFIFFCIISFSTFIYYVSVNVTQERQYITSLMTMMGLRESAFWLSWGLMYAGFILIMATLMALIVKSAQIVVLTGFVMVFTLFLLYGLSLITLAFLMSVLIKKPFLTGLVVFLLIVFWGILGFPALYTRLPAFLEWTLCLLSPFAFTVGMAQLIHLDYDVNSNAHLDSSQNPYLIIATLFMLVFDTLLYLVLTLYFDKILPAEYGHRCSPLFFLKSCFWFQHGRANHVVLENETDSDPTPNDCFEPVSPEFCGKEAIRIKNLKKEYAGKCERVEALKGVVFDIYEGQITALLGHSGAGKTTLLNILSGLSVPTSGSVTVYNHTLSRMADIENISKFTGFCPQSNVQFGFLTVKENLRLFAKIKGILPHEVEKEVQRVVQELEMENIQDILAQNLSGGQNRKLTFGIAILGDPQVLLLDEPTAGLDPLSRHRIWNLLKEGKSDRVILFSTQFIDEADILADRKVFISNGKLKCAGSSLFLKKKWGIGYHLSLHLNERCDPESITSLVKQHISDAKLTAQSEEKLVYILPLERTNKFPELYRDLDRCSNQGIEDYGVSITTLNEVFLKLEGKSTIDESDIGIWGQLQTDGAKDIGSLVELEQVLSSFHETRKTISGVALWRQQVCAIAKVRFLKLKKERKSLWTILLLFGISFIPQLLEHLFYESYQKSYPWELSPNTYFLSPGQQPQDPLTHLLVINKTGSTIDNFLHSLRRQNIAIEVDAFGTRNGTDDPSYNGAIIVSGDEKDHRFSIACNTKRLNCFPVLLDVISNGLLGIFNSSEHIQTDRSTFFEEHMDYEYGYRSNTFFWIPMAASFTPYIAMSSIGDYKKKAHSQLRISGLYPSAYWFGQALVDVSLYFLILLLMQIMDYIFSPEEIIFIIQNLLIQILCSIGYVSSLVFLTYVISFIFRNGRKNSGIWSFFFLIVVIFSIVATDLNEYGFLGLFFGTMLIPPFTLIGSLFIFSEISPDSMDYLGASESEIVYLALLIPYLHFLIFLFILRCLEMNCRKKLMRKDPVFRISPRSNAIFPNPEEPEGEEEDIQMERMRTVNAMAVRDFDETPVIIASCLRKEYAGKKKNCFSKRKKKIATRNVSFCVKKGEVIGLLGHNGAGKSTTIKMITGDTKPTAGQVILKGSGGGEPLGFLGYCPQENALWPNLTVRQHLEVYAAVKGLRKGDAMIAITRLVDALKLQDQLKAPVKTLSEGIKRKLCFVLSILGNPSVVLLDEPSTGMDPEGQQQMWQVIRATFRNTERGALLTTHYMAEAEAVCDRVAIMVSGRLRCIGSIQHLKSKFGKDYLLEMKLKNLAQMEPLHAEILRLFPQAAQQERFSSLMVYKLPVEDVRPLSQAFFKLEIVKQSFDLEEYSLSQSTLEQVFLELSKEQELGDLEEDFDPSVKWKLLLQEEP
283	Q12979	>sp|Q12979|ABR_HUMAN Active breakpoint cluster region-related protein GN=ABR PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MEPLSHRGLPRLSWIDTLYSNFSYGTDEYDGEGNEEQKGPPEGSETMPYIDESPTMSPQLSARSQGGGDGVSPTPPEGLAPGVEAGKGLEMRKLVLSGFLASEEIYINQLEALLLPMKPLKATATTSQPVLTIQQIETIFYKIQDIYEIHKEFYDNLCPKVQQWDSQVTMGHLFQKLASQLGVYKAFVDNYKVALETAEKCSQSNNQFQKISEELKVKGPKDSKDSHTSVTMEALLYKPIDRVTRSTLVLHDLLKHTPVDHPDYPLLQDALRISQNFLSSINEDIDPRRTAVTTPKGETRQLVKDGFLVEVSESSRKLRHVFLFTDVLLCAKLKKTSAGKHQQYDCKWYIPLADLVFPSPEESEASPQVHPFPDHELEDMKMKISALKSEIQKEKANKGQSRAIERLKKKMFENEFLLLLNSPTIPFRIHNRNGKSYLFLLSSDYERSEWREAIQKLQKKDLQAFVLSSVELQVLTGSCFKLRTVHNIPVTSNKDDDESPGLYGFLHVIVHSAKGFKQSANLYCTLEVDSFGYFVSKAKTRVFRDTAEPKWDEEFEIELEGSQSLRILCYEKCYDKTKVNKDNNEIVDKIMGKGQIQLDPQTVETKNWHTDVIEMNGIKVEFSMKFTSRDMSLKRTPSKKQTGVFGVKISVVTKRERSKVPYIVRQCVEEVEKRGIEEVGIYRISGVATDIQALKAVFDANNKDILLMLSDMDINAIAGTLKLYFRELPEPLLTDRLYPAFMEGIALSDPAAKENCMMHLLRSLPDPNLITFLFLLEHLKRVAEKEPINKMSLHNLATVFGPTLLRPSEVESKAHLTSAADIWSHDVMAQVQVLLYYLQHPPISFAELKRNTLYFSTDV
304	Q30167	>sp|Q30167|2B1A_HUMAN HLA class II histocompatibility antigen, DRB1-10 beta chain GN=HLA-DRB1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MVCLRLPGGSCMAVLTVTLMVLSSPLALAGDTRPRFLEEVKFECHFFNGTERVRLLERRVHNQEEYARYDSDVGEYRAVTELGRPDAEYWNSQKDLLERRRAAVDTYCRHNYGVGESFTVQRRVQPKVTVYPSKTQPLQHHNLLVCSVNGFYPGSIEVRWFRNGQEEKTGVVSTGLIQNGDWTFQTLVMLETVPQSGEVYTCQVEHPSVMSPLTVEWRARSESAQSKMLSGVGGFVLGLLFLGAGLFIYFRNQKGHSGLPPTGFLS
275	Q8WWZ4	>sp|Q8WWZ4|ABCAA_HUMAN ATP-binding cassette sub-family A member 10 GN=ABCA10 PE=2 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MNKMALASFMKGRTVIGTPDEETMDIELPKKYHEMVGVIFSDTFSYRLKFNWGYRIPVIKEHSEYTEHCWAMHGEIFCYLAKYWLKGFVAFQAAINAAIIEVTTNHSVMEELTSVIGINMKIPPFISKGEIMNEWFHFTCLVSFSSFIYFASLNVARERGKFKKLMTVMGLRESAFWLSWGLTYICFIFIMSIFMALVITSIPIVFHTGFMVIFTLYSLYGLSLIALAFLMSVLIRKPMLAGLAGFLFTVFWGCLGFTVLYRQLPLSLGWVLSLLSPFAFTAGMAQITHLDNYLSGVIFPDPSGDSYKMIATFFILAFDTLFYLIFTLYFERVLPDKDGHGDSPLFFLKSSFWSKHQNTHHEIFENEINPEHSSDDSFEPVSPEFHGKEAIRIRNVIKEYNGKTGKVEALQGIFFDIYEGQITAILGHNGAGKSTLLNILSGLSVSTEGSATIYNTQLSEITDMEEIRKNIGFCPQFNFQFDFLTVRENLRVFAKIKGIQPKEVEQEVKRIIMELDMQSIQDIIAKKLSGGQKRKLTLGIAILGDPQVLLLDEPTAGLDPFSRHRVWSLLKEHKVDRLILFSTQFMDEADILADRKVFLSNGKLKCAGSSLFLKRKWGIGYHLSLHRNEMCDTEKITSLIKQHIPDAKLTTESEEKLVYSLPLEKTNKFPDLYSDLDKCSDQGIRNYAVSVTSLNEVFLNLEGKSAIDEPDFDIGKQEKIHVTRNTGDESEMEQVLCSLPETRKAVSSAALWRRQIYAVATLRFLKLRRERRALLCLLLVLGIAFIPIILEKIMYKVTRETHCWEFSPSMYFLSLEQIPKTPLTSLLIVNNTGSNIEDLVHSLKCQDIVLEIDDFRNRNGSDDPSYNGAIIVSGDQKDYRFSVACNTKKLNCFPVLMGIVSNALMGIFNFTELIQMESTSFSRDDIVLDLGFIDGSIFLLLITNCVSPFIGMSSISDYKKNVQSQLWISGLWPSAYWCGQALVDIPLYFLILFSIHLIYYFIFLGFQLSWELMFVLVVCIIGCAVSLIFLTYVLSFIFRKWRKNNGFWSFGFFIILICVSTIMVSTQYEKLNLILCMIFIPSFTLLGYVMLLIQLDFMRNLDSLDNRINEVNKTILLTTLIPYLQSVIFLFVIRCLEMKYGNEIMNKDPVFRISPRSRETHPNPEEPEEEDEDVQAERVQAANALTAPNLEEEPVITASCLHKEYYETKKSCFSTRKKKIAIRNVSFCVKKGEVLGLLGHNGAGKSTSIKMITGCTKPTAGVVVLQGSRASVRQQHDNSLKFLGYCPQENSLWPKLTMKEHLELYAAVKGLGKEDAALSISRLVEALKLQEQLKAPVKTLSEGIKRKLCFVLSILGNPSVVLLDEPFTGMDPEGQQQMWQILQATVKNKERGTLLTTHYMSEAEAVCDRMAMMVSGTLRCIGSIQHLKNKFGRDYLLEIKMKEPTQVEALHTEILKLFPQAAWQERYSSLMAYKLPVEDVHPLSRAFFKLEAMKQTFNLEEYSLSQATLEQVFLELCKEQELGNVDDKIDTTVEWKLLPQEDP
276	Q86UQ4	>sp|Q86UQ4|ABCAD_HUMAN ATP-binding cassette sub-family A member 13 GN=ABCA13 PE=2 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MGHAGCQFKALLWKNWLCRLRNPVLFLAEFFWPCILFVILTVLRFQEPPRYRDICYLQPRDLPSCGVIPFVQSLLCNTGSRCRNFSYEGSMEHHFRLSRFQTAADPKKVNNLAFLKEIQDLAEEIHGMMDKAKNLKRLWVERSNTPDSSYGSSFFTMDLNKTEEVILKLESLHQQPHIWDFLLLLPRLHTSHDHVEDGMDVAVNLLQTILNSLISLEDLDWLPLNQTFSQVSELVLNVTISTLTFLQQHGVAVTEPVYHLSMQNIVWDPQKVQYDLKSQFGFDDLHTEQILNSSAELKEIPTDTSLEKMVCSVLSSTSEDEAEKWGHVGGCHPKWSEAKNYLVHAVSWLRVYQQVFVQWQQGSLLQKTLTGMGHSLEALRNQFEEESKPWKVVEALHTALLLLNDSLSADGPKDNHTFPKILQHLWKLQSLLQNLPQWPALKRFLQLDGALRNAIAQNLHFVQEVLICLETSANDFKWFELNQLKLEKDVFFWELKQMLAKNAVCPNGRFSEKEVFLPPGNSSIWGGLQGLLCYCNSSETSVLNKLLGSVEDADRILQEVITWHKNMSVLIPEEYLDWQELEMQLSEASLSCTRLFLLLGADPSPENDVFSSDCKHQLVSTVIFHTLEKTQFFLEQAYYWKAFKKFIRKTCEVAQYVNMQESFQNRLLAFPEESPCFEENMDWKMISDNYFQFLNNLLKSPTASISRALNFTKHLLMMEKKLHTLEDEQMNFLLSFVEFFEKLLLPNLFDSSIVPSFHSLPSLTEDILNISSLWTNHLKSLKRDPSATDAQKLLEFGNEVIWKMQTLGSHWIRKEPKNLLRFIELILFEINPKLLELWAYGISKGKRAKLENFFTLLNFSVPENEILSTSFNFSQLFHSDWPKSPAMNIDFVRLSEAIITSLHEFGFLEQEQISEALNTVYAIRNASDLFSALSEPQKQEVDKILTHIHLNVFQDKDSALLLQIYSSFYRYIYELLNIQSRGSSLTFLTQISKHILDIIKQFNFQNISKAFAFLFKTAEVLGGISNVSYCQQLLSIFNFLELQAQSFMSTEGQELEVIHTTLTGLKQLLIIDEDFRISLFQYMSQFFNSSVEDLLDNKCLISDNKHISSVNYSTSEESSFVFPLAQIFSNLSANVSVFNKFMSIHCTVSWLQMWTEIWETISQLFKFDMNVFTSLHHGFTQLLDELEDDVKVSKSCQGILPTHNVARLILNLFKNVTQANDFHNWEDFLDLRDFLVALGNALVSVKKLNLEQVEKSLFTMEAALHQLKTFPFNESTSREFLNSLLEVFIEFSSTSEYIVRNLDSINDFLSNNLTNYGEKFENIITELREAIVFLRNVSHDRDLFSCADIFQNVTECILEDGFLYVNTSQRMLRILDTLNSTFSSENTISSLKGCIVWLDVINHLYLLSNSSFSQGHLQNILGNFRDIENKMNSILKIVTWVLNIKKPLCSSNGSHINCVNIYLKDVTDFLNIVLTTVFEKEKKPKFEILLALLNDSTKQVRMSINNLTTDFDFASQSNWRYFTELILRPIEMSDEIPNQFQNIWLHLITLGKEFQKLVKGIYFNILENNSSSKTENLLNIFATSPKEKDVNSVGNSIYHLASYLAFSLSHDLQNSPKIIISPEIMKATGLGIQLIRDVFNSLMPVVHHTSPQNAGYMQALKKVTSVMRTLKKADIDLLVDQLEQVSVNLMDFFKNISSVGTGNLVVNLLVGLMEKFADSSHSWNVNHLLQLSRLFPKDVVDAVIDVYYVLPHAVRLLQGVPGKNITEGLKDVYSFTLLHGITISNITKEDFAIVIKILLDTIELVSDKPDIISEALACFPVVWCWNHTNSGFRQNSKIDPCNVHGLMSSSFYGKVASILDHFHLSPQGEDSPCSNESSRMEITRKVVCIIHELVDWNSILLELSEVFHVNISLVKTVQKFWHKILPFVPPSINQTRDSISELCPSGSIKQVALQIIEKLKNVNFTKVTSGENILDKLSSLNKILNINEDTETSVQNIISSNLERTVQLISEDWSLEKSTHNLLSLFMMLQNANVTGSSLEALSSFIEKSETPYNFEELWPKFQQIMKDLTQDFRIRHLLSEMNKGIKSINSMALQKITLQFAHFLEILDSPSLKTLEIIEDFLLVTKNWLQEYANEDYSRMIETLFIPVTNESSTEDIALLAKAIATFWGSLKNISRAGNFDVAFLTHLLNQEQLTNFSVVQLLFENILINLINNLAGNSQEAAWNLNDTDLQIMNFINLILNHMQSETSRKTVLSLRSIVDFTEQFLKTFFSLFLKEDSENKISLLLKYFHKDVIAEMSFVPKDKILEILKLDQFLTLMIQDRLMNIFSSLKETIYHLMKSSFILDNGEFYFDTHQGLKFMQDLFNALLRETSMKNKTENNIDFFTVVSQLFFHVNKSEDLFKLNQDLGSALHLVRECSTEMARLLDTILHSPNKDFYALYPTLQEVILANLTDLLFFINNSFPLRNRATLEITKRLVGAISRASEESHVLKPLLEMSGTLVMLLNDSADLRDLATSMDSIVKLLKLVKKVSGKMSTVFKTHFISNTKDSVKFFDTLYSIMQQSVQNLVKEIATLKKIDHFTFEKINDLLVPFLDLAFEMIGVEPYISSNSDIFSMSPSILSYMNQSKDFSDILEEIAEFLTSVKMNLEDMRSLAVAFNNETQTFSMDSVNLREEILGCLVPINNITNQMDFLYPNPISTHSGPQDIKWEIIHEVIPFLDKILSQNSTEIGSFLKMVICLTLEALWKNLKKDNWNVSNVLMTFTQHPNNLLKTIETVLEASSGIKSDYEGDLNKSLYFDTPLSQNITHHQLEKAIHNVLSRIALWRKGLLFNNSEWITSTRTLFQPLFEIFIKATTGKNVTSEKEERTKKEMIDFPYSFKPFFCLEKYLGGLFVLTKYWQQIPLTDQSVVEICEVFQQTVKPSEAMEMLQKVKMMVVRVLTIVAENPSWTKDILCATLSCKQNGIRHLILSAIQGVTLAQDHFQEIEKIWSSPNQLNCESLSKNLSSTLESFKSSLENATGQDCTSQPRLETVQQHLYMLAKSLEETWSSGNPIMTFLSNFTVTEDVKIKDLMKNITKLTEELRSSIQISNETIHSILEANISHSKVLFSALTVALSGKCDQEILHLLLTFPKGEKSWIAAEELCSLPGSKVYSLIVLLSRNLDVRAFIYKTLMPSEANGLLNSLLDIVSSLSALLAKAQHVFEYLPEFLHTFKITALLETLDFQQVSQNVQARSSAFGSFQFVMKMVCKDQASFLSDSNMFINLPRVKELLEDDKEKFNIPEDSTPFCLKLYQEILQLPNGALVWTFLKPILHGKILYTPNTPEINKVIQKANYTFYIVDKLKTLSETLLEMSSLFQRSGSGQMFNQLQEALRNKFVRNFVENQLHIDVDKLTEKLQTYGGLLDEMFNHAGAGRFRFLGSILVNLSSCVALNRFQALQSVDILETKAHELLQQNSFLASIIFSNSLFDKNFRSESVKLPPHVSYTIRTNVLYSVRTDVVKNPSWKFHPQNLPADGFKYNYVFAPLQDMIERAIILVQTGQEALEPAAQTQAAPYPCHTSDLFLNNVGFFFPLIMMLTWMVSVASMVRKLVYEQEIQIEEYMRMMGVHPVIHFLAWFLENMAVLTISSATLAIVLKTSGIFAHSNTFIVFLFLLDFGMSVVMLSYLLSAFFSQANTAALCTSLVYMISFLPYIVLLVLHNQLSFVNQTFLCLLSTTAFGQGVFFITFLEGQETGIQWNNMYQALEQGGMTFGWVCWMILFDSSLYFLCGWYLSNLIPGTFGLRKPWYFPFTASYWKSVGFLVEKRQYFLSSSLFFFNENFDNKGSSLQNREGELEGSAPGVTLVSVTKEYEGHKAVVQDLSLTFYRDQITALLGTNGAGKTTIISMLTGLHPPTSGTIIINGKNLQTDLSRVRMELGVCPQQDILLDNLTVREHLLLFASIKAPQWTKKELHQQVNQTLQDVDLTQHQHKQTRALSGGLKRKLSLGIAFMGMSRTVVLDEPTSGVDPCSRHSLWDILLKYREGRTIIFTTHHLDEAEALSDRVAVLQHGRLRCCGPPFCLKEAYGQGLRLTLTRQPSVLEAHDLKDMACVTSLIKIYIPQAFLKDSSGSELTYTIPKDTDKACLKGLFQALDENLHQLHLTGYGISDTTLEEVFLMLLQDSNKKSHIALGTESELQNHRPTGHLSGYCGSLARPATVQGVQLLRAQVAAILARRLRRTLRAGKSTLADLLLPVLFVALAMGLFMVRPLATEYPPLRLTPGHYQRAETYFFSSGGDNLDLTRVLLRKFRDQDLPCADLNPRQKNSSCWRTDPFSHPEFQDSCGCLKCPNRSASAPYLTNHLGHTLLNLSGFNMEEYLLAPSEKPRLGGWSFGLKIPSEAGGANGNISKPPTLAKVWYNQKGFHSLPSYLNHLNNLILWQHLPPTVDWRQYGITLYSHPYGGALLNKDKILESIRQCGVALCIVLGFSILSASIGSSVVRDRVIGAKRLQHISGLGYRMYWFTNFLYDMLFYLVSVCLCVAVIVAFQLTAFTFRKNLAATALLLSLFGYATLPWMYLMSRIFSSSDVAFISYVSLNFIFGLCTMLITIMPRLLAIISKAKNLQNIYDVLKWVFTIFPQFCLGQGLVELCYNQIKYDLTHNFGIDSYVSPFEMNFLGWIFVQLASQGTVLLLLRVLLHWDLLRWPRGHSTLQGTVKSSKDTDVEKEEKRVFEGRTNGDILVLYNLSKHYRRFFQNIIAVQDISLGIPKGECFGLLGVNGAGKSTTFKMLNGEVSLTSGHAIIRTPMGDAVDLSSAGTAGVLIGYCPQQDALDELLTGWEHLYYYCSLRGIPRQCIPEVAGDLIRRLHLEAHADKPVATYSGGTKRKLSTALALVGKPDILLLDEPSSGMDPCSKRYLWQTIMKEVREGCAAVLTSHSMEECEALCTRLAIMVNGSFKCLGSPQHIKNRFGDGYTVKVWLCKEANQHCTVSDHLKLYFPGIQFKGQHLNLLEYHVPKRWGCLADLFKVIENNKTFLNIKHYSINQTTLEQVFINFASEQQQTLQSTLDPSTDSHHTHHLPI
277	Q96J66	>sp|Q96J66|ABCCB_HUMAN ATP-binding cassette sub-family C member 11 GN=ABCC11 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MTRKRTYWVPNSSGGLVNRGIDIGDDMVSGLIYKTYTLQDGPWSQQERNPEAPGRAAVPPWGKYDAALRTMIPFRPKPRFPAPQPLDNAGLFSYLTVSWLTPLMIQSLRSRLDENTIPPLSVHDASDKNVQRLHRLWEEEVSRRGIEKASVLLVMLRFQRTRLIFDALLGICFCIASVLGPILIIPKILEYSEEQLGNVVHGVGLCFALFLSECVKSLSFSSSWIINQRTAIRFRAAVSSFAFEKLIQFKSVIHITSGEAISFFTGDVNYLFEGVCYGPLVLITCASLVICSISSYFIIGYTAFIAILCYLLVFPLAVFMTRMAVKAQHHTSEVSDQRIRVTSEVLTCIKLIKMYTWEKPFAKIIEDLRRKERKLLEKCGLVQSLTSITLFIIPTVATAVWVLIHTSLKLKLTASMAFSMLASLNLLRLSVFFVPIAVKGLTNSKSAVMRFKKFFLQESPVFYVQTLQDPSKALVFEEATLSWQQTCPGIVNGALELERNGHASEGMTRPRDALGPEEEGNSLGPELHKINLVVSKGMMLGVCGNTGSGKSSLLSAILEEMHLLEGSVGVQGSLAYVPQQAWIVSGNIRENILMGGAYDKARYLQVLHCCSLNRDLELLPFGDMTEIGERGLNLSGGQKQRISLARAVYSDRQIYLLDDPLSAVDAHVGKHIFEECIKKTLRGKTVVLVTHQLQYLEFCGQIILLENGKICENGTHSELMQKKGKYAQLIQKMHKEATSDMLQDTAKIAEKPKVESQALATSLEESLNGNAVPEHQLTQEEEMEEGSLSWRVYHHYIQAAGGYMVSCIIFFFVVLIVFLTIFSFWWLSYWLEQGSGTNSSRESNGTMADLGNIADNPQLSFYQLVYGLNALLLICVGVCSSGIFTKVTRKASTALHNKLFNKVFRCPMSFFDTIPIGRLLNCFAGDLEQLDQLLPIFSEQFLVLSLMVIAVLLIVSVLSPYILLMGAIIMVICFIYYMMFKKAIGVFKRLENYSRSPLFSHILNSLQGLSSIHVYGKTEDFISQFKRLTDAQNNYLLLFLSSTRWMALRLEIMTNLVTLAVALFVAFGISSTPYSFKVMAVNIVLQLASSFQATARIGLETEAQFTAVERILQYMKMCVSEAPLHMEGTSCPQGWPQHGEIIFQDYHMKYRDNTPTVLHGINLTIRGHEVVGIVGRTGSGKSSLGMALFRLVEPMAGRILIDGVDICSIGLEDLRSKLSVIPQDPVLLSGTIRFNLDPFDRHTDQQIWDALERTFLTKAISKFPKKLHTDVVENGGNFSVGERQLLCIARAVLRNSKIILIDEATASIDMETDTLIQRTIREAFQGCTVLVIAHRVTTVLNCDHILVMGNGKVVEFDRPEVLRKKPGSLFAALMATATSSLR
278	P33897	>sp|P33897|ABCD1_HUMAN ATP-binding cassette sub-family D member 1 GN=ABCD1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MPVLSRPRPWRGNTLKRTAVLLALAAYGAHKVYPLVRQCLAPARGLQAPAGEPTQEASGVAAAKAGMNRVFLQRLLWLLRLLFPRVLCRETGLLALHSAALVSRTFLSVYVARLDGRLARCIVRKDPRAFGWQLLQWLLIALPATFVNSAIRYLEGQLALSFRSRLVAHAYRLYFSQQTYYRVSNMDGRLRNPDQSLTEDVVAFAASVAHLYSNLTKPLLDVAVTSYTLLRAARSRGAGTAWPSAIAGLVVFLTANVLRAFSPKFGELVAEEARRKGELRYMHSRVVANSEEIAFYGGHEVELALLQRSYQDLASQINLILLERLWYVMLEQFLMKYVWSASGLLMVAVPIITATGYSESDAEAVKKAALEKKEEELVSERTEAFTIARNLLTAAADAIERIMSSYKEVTELAGYTARVHEMFQVFEDVQRCHFKRPRELEDAQAGSGTIGRSGVRVEGPLKIRGQVVDVEQGIICENIPIVTPSGEVVVASLNIRVEEGMHLLITGPNGCGKSSLFRILGGLWPTYGGVLYKPPPQRMFYIPQRPYMSVGSLRDQVIYPDSVEDMQRKGYSEQDLEAILDVVHLHHILQREGGWEAMCDWKDVLSGGEKQRIGMARMFYHRPKYALLDECTSAVSIDVEGKIFQAAKDAGIALLSITHRPSLWKYHTHLLQFDGEGGWKFEKLDSAARLSLTEEKQRLEQQLAGIPKMQRRLQELCQILGEAVAPAHVPAPSPQGPGGLQGAST
279	Q9UNQ0	>sp|Q9UNQ0|ABCG2_HUMAN ATP-binding cassette sub-family G member 2 GN=ABCG2 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MSSSNVEVFIPVSQGNTNGFPATASNDLKAFTEGAVLSFHNICYRVKLKSGFLPCRKPVEKEILSNINGIMKPGLNAILGPTGGGKSSLLDVLAARKDPSGLSGDVLINGAPRPANFKCNSGYVVQDDVVMGTLTVRENLQFSAALRLATTMTNHEKNERINRVIQELGLDKVADSKVGTQFIRGVSGGERKRTSIGMELITDPSILFLDEPTTGLDSSTANAVLLLLKRMSKQGRTIIFSIHQPRYSIFKLFDSLTLLASGRLMFHGPAQEALGYFESAGYHCEAYNNPADFFLDIINGDSTAVALNREEDFKATEIIEPSKQDKPLIEKLAEIYVNSSFYKETKAELHQLSGGEKKKKITVFKEISYTTSFCHQLRWVSKRSFKNLLGNPQASIAQIIVTVVLGLVIGAIYFGLKNDSTGIQNRAGVLFFLTTNQCFSSVSAVELFVVEKKLFIHEYISGYYRVSSYFLGKLLSDLLPMRMLPSIIFTCIVYFMLGLKPKADAFFVMMFTLMMVAYSASSMALAIAAGQSVVSVATLLMTICFVFMMIFSGLLVNLTTIASWLSWLQYFSIPRYGFTALQHNEFLGQNFCPGLNATGNNPCNYATCTGEEYLVKQGIDLSPWGLWKNHVALACMIVIFLTIAYLKLLFLKKYS
280	P41238	>sp|P41238|ABEC1_HUMAN C->U-editing enzyme APOBEC-1 GN=APOBEC1 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MTSEKGPSTGDPTLRRRIEPWEFDVFYDPRELRKEACLLYEIKWGMSRKIWRSSGKNTTNHVEVNFIKKFTSERDFHPSMSCSITWFLSWSPCWECSQAIREFLSRHPGVTLVIYVARLFWHMDQQNRQGLRDLVNSGVTIQIMRASEYYHCWRNFVNYPPGDEAHWPQYPPLWMMLYALELHCIILSLPPCLKISRRWQNHLTFFRLHLQNCHYQTIPPHILLATGLIHPSVAWR
281	Q9H3Z7	>sp|Q9H3Z7|ABHGB_HUMAN Protein ABHD16B GN=ABHD16B PE=3 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MCVICFVKALVRVFKIYLTASYTYPFRGWPVAFRWDDVRAVGRSSSHRALTCAAAAAGVWLLRDETLGGDALGRPPRGARSQAQCLLQQLRELPGQLASYALAHSLGRWLVYPGSVSLMTRALLPLLQQGQERLVERYHGRRAKLVACDGNEIDTMFMDRRQHPGSHVHGPRLVICCEGNAGFYEMGCLSAPLEAGYSVLGWNHPGFGSSTGVPFPQHDANAMDVVVEYALHRLHFPPAHLVVYGWSVGGFTATWATMTYPELGALVLDATFDDLVPLALKVMPHSWKGLVVRTVREHFNLNVAEQLCCYPGPVLLLRRTQDDVVSTSGRLRPLSPGDVEGNRGNELLLRLLEHRYPVVMAREGRAVVTRWLRAGSLAQEAAFYARYRVDEDWCLALLRSYRARCEEELEGEEALGPHGPAFPWLVGQGLSSRRRRRLALFLARKHLKNVEATHFSPLEPEEFQLPWRL
282	P00519	>sp|P00519|ABL1_HUMAN Tyrosine-protein kinase ABL1 GN=ABL1 PE=1 SV=4 Homo sapiens OS=Human NCBI_TaxID=9606	MLEICLKLVGCKSKKGLSSSSSCYLEEALQRPVASDFEPQGLSEAARWNSKENLLAGPSENDPNLFVALYDFVASGDNTLSITKGEKLRVLGYNHNGEWCEAQTKNGQGWVPSNYITPVNSLEKHSWYHGPVSRNAAEYLLSSGINGSFLVRESESSPGQRSISLRYEGRVYHYRINTASDGKLYVSSESRFNTLAELVHHHSTVADGLITTLHYPAPKRNKPTVYGVSPNYDKWEMERTDITMKHKLGGGQYGEVYEGVWKKYSLTVAVKTLKEDTMEVEEFLKEAAVMKEIKHPNLVQLLGVCTREPPFYIITEFMTYGNLLDYLRECNRQEVNAVVLLYMATQISSAMEYLEKKNFIHRDLAARNCLVGENHLVKVADFGLSRLMTGDTYTAHAGAKFPIKWTAPESLAYNKFSIKSDVWAFGVLLWEIATYGMSPYPGIDLSQVYELLEKDYRMERPEGCPEKVYELMRACWQWNPSDRPSFAEIHQAFETMFQESSISDEVEKELGKQGVRGAVSTLLQAPELPTKTRTSRRAAEHRDTTDVPEMPHSKGQGESDPLDHEPAVSPLLPRKERGPPEGGLNEDERLLPKDKKTNLFSALIKKKKKTAPTPPKRSSSFREMDGQPERRGAGEEEGRDISNGALAFTPLDTADPAKSPKPSNGAGVPNGALRESGGSGFRSPHLWKKSSTLTSSRLATGEEEGGGSSSKRFLRSCSASCVPHGAKDTEWRSVTLPRDLQSTGRQFDSSTFGGHKSEKPALPRKRAGENRSDQVTRGTVTPPPRLVKKNEEAADEVFKDIMESSPGSSPPNLTPKPLRRQVTVAPASGLPHKEEAGKGSALGTPAAAEPVTPTSKAGSGAPGGTSKGPAEESRVRRHKHSSESPGRDKGKLSRLKPAPPPPPAASAGKAGGKPSQSPSQEAAGEAVLGAKTKATSLVDAVNSDAAKPSQPGEGLKKPVLPATPKPQSAKPSGTPISPAPVPSTLPSASSALAGDQPSSTAFIPLISTRVSLRKTRQPPERIASGAITKGVVLDSTEALCLAISRNSEQMASHSAVLEAGKNLYTFCVSYVDSIQQMRNKFAFREAINKLENNLRELQICPATAGSGPAATQDFSKLLSSVKEISDIVQR
294	Q6NVV9	>sp|Q6NVV9|ADAM5_HUMAN Putative disintegrin and metalloproteinase domain-containing protein 5 GN=ADAM5 PE=5 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MQTSILIKSSCRPQFQRRFHHRMQKQIQNIISILSSASVINSYDENDIRHSKPLLVQMDCNYNGYVAGIPNSLVTLSVCSGLRGTMQLKNISYGIEPMEAVSGFIHKIYEEKYADTNILLEENDTYTWFNSEYQVRKSSEKTDFIKLFPRYIEMHIVVDKNLFKPANMICRKSVGKECDFTEYCNGDLPYCLPDTYVRDGEYCDSGGAFCFQGKCRTFDKQCDDLIGRGSRGAPVFCYDEINTRGDNFGNCGTAHCLFQHILCGKLVCTWEHRDLISRPNLSVIYAHVRDQTCVSTYLPRRTPPPVNSPISITSYYSAEDRDETFVQDGSMCGPDMYCFEMHCKHVRFLMNLKLCDASNHCDRHGVCNNFNHCHCEKGYNPPYCQPKQGAFGSIDDGHLVPPTERSYMEEGR
284	Q96AP0	>sp|Q96AP0|ACD_HUMAN Adrenocortical dysplasia protein homolog GN=ACD PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MPGRCQSDAAMRVNGPASRAPAGWTSGSLHTGPRAGRPRAQARGVRGRGLLLRPRPAKELPLPRKGGAWAPAGNPGPLHPLGVAVGMAGSGRLVLRPWIRELILGSETPSSPRAGQLLEVLQDAEAAVAGPSHAPDTSDVGATLLVSDGTHSVRCLVTREALDTSDWEEKEFGFRGTEGRLLLLQDCGVHVQVAEGGAPAEFYLQVDRFSLLPTEQPRLRVPGCNQDLDVQKKLYDCLEEHLSESTSSNAGLSLSQLLDEMREDQEHQGALVCLAESCLTLEGPCTAPPVTHWAASRCKATGEAVYTVPSSMLCISENDQLILSSLGPCQRTQGPELPPPDPALQDLSLTLIASPPSSPSSSGTPALPGHMSSEESGTSISLLPALSLAAPDPGQRSSSQPSPAICSAPATLTPRSPHASRTPSSPLQSCTPSLSPRSHVPSPHQALVTRPQKPSLEFKEFVGLPCKNRPPFPRTGATRGAQEPCSVWEPPKRHRDGSAFQYEYEPPCTSLCARVQAVRLPPQLMAWALHFLMDAQPGSEPTPM
285	P25106	>sp|P25106|ACKR3_HUMAN Atypical chemokine receptor 3 GN=ACKR3 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MDLHLFDYSEPGNFSDISWPCNSSDCIVVDTVMCPNMPNKSVLLYTLSFIYIFIFVIGMIANSVVVWVNIQAKTTGYDTHCYILNLAIADLWVVLTIPVWVVSLVQHNQWPMGELTCKVTHLIFSINLFGSIFFLTCMSVDRYLSITYFTNTPSSRKKMVRRVVCILVWLLAFCVSLPDTYYLKTVTSASNNETYCRSFYPEHSIKEWLIGMELVSVVLGFAVPFSIIAVFYFLLARAISASSDQEKHSSRKIIFSYVVVFLVCWLPYHVAVLLDIFSILHYIPFTCRLEHALFTALHVTQCLSLVHCCVNPVLYSFINRNYRYELMKAFIFKYSAKTGLTKLIDASRVSETEYSALEQSTK
286	Q86TX2	>sp|Q86TX2|ACOT1_HUMAN Acyl-coenzyme A thioesterase 1 GN=ACOT1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAATLILEPAGRCCWDEPVRIAVRGLAPEQPVTLRASLRDEKGALFQAHARYRADTLGELDLERAPALGGSFAGLEPMGLLWALEPEKPLVRLVKRDVRTPLAVELEVLDGHDPDPGRLLCRVRHERYFLPPGVRREPVRAGRVRGTLFLPPEPGPFPGIVDMFGTGGGLLEYRASLLAGKGFAVMALAYYNYEDLPKTMETLHLEYFEEAVNYLLSHPEVKGPGVGLLGISKGGELCLSMASFLKGITAAVVINGSVANVGGTLRYKGETLPPVGVNRNRIKVTKDGYADIVDVLNSPLEGPDQKSFIPVERAESTFLFLVGQDDHNWKSEFYANEACKRLQAHGRRKPQIICYPETGHYIEPPYFPLCRASLHALVGSPIIWGGEPRAHAMAQVDAWKQLQTFFHKHLGGHEGTIPSKV
287	Q8N9L9	>sp|Q8N9L9|ACOT4_HUMAN Acyl-coenzyme A thioesterase 4 GN=ACOT4 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MSATLILEPPGRCCWNEPVRIAVRGLAPEQRVTLRASLRDEKGALFRAHARYCADARGELDLERAPALGGSFAGLEPMGLLWALEPEKPFWRFLKRDVQIPFVVELEVLDGHDPEPGRLLCQAQHERHFLPPGVRRQSVRAGRVRATLFLPPGPGPFPGIIDIFGIGGGLLEYRASLLAGHGFATLALAYYNFEDLPNNMDNISLEYFEEAVCYMLQHPQVKGPGIGLLGISLGADICLSMASFLKNVSATVSINGSGISGNTAINYKHSSIPPLGYDLRRIKVAFSGLVDIVDIRNALVGGYKNPSMIPIEKAQGPILLIVGQDDHNWRSELYAQTVSERLQAHGKEKPQIICYPGTGHYIEPPYFPLCPASLHRLLNKHVIWGGEPRAHSKAQEDAWKQILAFFCKHLGGTQKTAVPKL
288	Q15067	>sp|Q15067|ACOX1_HUMAN Peroxisomal acyl-coenzyme A oxidase 1 GN=ACOX1 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MNPDLRRERDSASFNPELLTHILDGSPEKTRRRREIENMILNDPDFQHEDLNFLTRSQRYEVAVRKSAIMVKKMREFGIADPDEIMWFKKLHLVNFVEPVGLNYSMFIPTLLNQGTTAQKEKWLLSSKGLQIIGTYAQTEMGHGTHLRGLETTATYDPETQEFILNSPTVTSIKWWPGGLGKTSNHAIVLAQLITKGKCYGLHAFIVPIREIGTHKPLPGITVGDIGPKFGYDEIDNGYLKMDNHRIPRENMLMKYAQVKPDGTYVKPLSNKLTYGTMVFVRSFLVGEAARALSKACTIAIRYSAVRHQSEIKPGEPEPQILDFQTQQYKLFPLLATAYAFQFVGAYMKETYHRINEGIGQGDLSELPELHALTAGLKAFTSWTANTGIEACRMACGGHGYSHCSGLPNIYVNFTPSCTFEGENTVMMLQTARFLMKSYDQVHSGKLVCGMVSYLNDLPSQRIQPQQVAVWPTMVDINSPESLTEAYKLRAARLVEIAAKNLQKEVIHRKSKEVAWNLTSVDLVRASEAHCHYVVVKLFSEKLLKIQDKAIQAVLRSLCLLYSLYGISQNAGDFLQGSIMTEPQITQVNQRVKELLTLIRSDAVALVDAFDFQDVTLGSVLGRYDGNVYENLFEWAKNSPLNKAEVHESYKHLKSLQSKL
289	Q99424	>sp|Q99424|ACOX2_HUMAN Peroxisomal acyl-coenzyme A oxidase 2 GN=ACOX2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MGSPVHRVSLGDTWSRQMHPDIESERYMQSFDVERLTNILDGGAQNTALRRKVESIIHSYPEFSCKDNYFMTQNERYKAAMRRAFHIRLIARRLGWLEDGRELGYAYRALSGDVALNIHRVFVRALRSLGSEEQIAKWDPLCKNIQIIATYAQTELGHGTYLQGLETEATYDAATQEFVIHSPTLTATKWWPGDLGRSATHALVQAQLICSGARRGMHAFIVPIRSLQDHTPLPGIIIGDIGPKMDFDQTDNGFLQLNHVRVPRENMLSRFAQVLPDGTYVKLGTAQSNYLPMVVVRVELLSGEILPILQKACVIAMRYSVIRRQSRLRPSDPEAKVLDYQTQQQKLFPQLAISYAFHFLAVSLLEFFQHSYTAILNQDFSFLPELHALSTGMKAMMSEFCTQGAEMCRRACGGHGYSKLSGLPSLVTKLSASCTYEGENTVLYLQVARFLVKSYLQTQMSPGSTPQRSLSPSVAYLTAPDLARCPAQRAADFLCPELYTTAWAHVAVRLIKDSVQHLQTLTQSGADQHEAWNQTTVIHLQAAKVHCYYVTVKGFTEALEKLENEPAIQQVLKRLCDLHAIHGILTNSGDFLHDAFLSGAQVDMARTAYLDLLRLIRKDAILLTDAFDFTDQCLNSALGCYDGNVYERLFQWAQKSPTNTQENPAYEEYIRPLLQSWRSKL
290	P13798	>sp|P13798|ACPH_HUMAN Acylamino-acid-releasing enzyme GN=APEH PE=1 SV=4 Homo sapiens OS=Human NCBI_TaxID=9606	MERQVLLSEPEEAAALYRGLSRQPALSAACLGPEVTTQYGGQYRTVHTEWTQRDLERMENIRFCRQYLVFHDGDSVVFAGPAGNSVETRGELLSRESPSGTMKAVLRKAGGTGPGEEKQFLEVWEKNRKLKSFNLSALEKHGPVYEDDCFGCLSWSHSETHLLYVAEKKRPKAESFFQTKALDVSASDDEIARLKKPDQAIKGDQFVFYEDWGENMVSKSIPVLCVLDVESGNISVLEGVPENVSPGQAFWAPGDAGVVFVGWWHEPFRLGIRFCTNRRSALYYVDLIGGKCELLSDDSLAVSSPRLSPDQCRIVYLQYPSLIPHHQCSQLCLYDWYTKVTSVVVDVVPRQLGENFSGIYCSLLPLGCWSADSQRVVFDSAQRSRQDLFAVDTQVGTVTSLTAGGSGGSWKLLTIDQDLMVAQFSTPSLPPTLKVGFLPSAGKEQSVLWVSLEEAEPIPDIHWGIRVLQPPPEQENVQYAGLDFEAILLQPGSPPDKTQVPMVVMPHGGPHSSFVTAWMLFPAMLCKMGFAVLLVNYRGSTGFGQDSILSLPGNVGHQDVKDVQFAVEQVLQEEHFDASHVALMGGSHGGFISCHLIGQYPETYRACVARNPVINIASMLGSTDIPDWCVVEAGFPFSSDCLPDLSVWAEMLDKSPIRYIPQVKTPLLLMLGQEDRRVPFKQGMEYYRALKTRNVPVRLLLYPKSTHALSEVEVESDSFMNAVLWLRTHLGS
291	P12814	>sp|P12814|ACTN1_HUMAN Alpha-actinin-1 GN=ACTN1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MDHYDSQQTNDYMQPEEDWDRDLLLDPAWEKQQRKTFTAWCNSHLRKAGTQIENIEEDFRDGLKLMLLLEVISGERLAKPERGKMRVHKISNVNKALDFIASKGVKLVSIGAEEIVDGNVKMTLGMIWTIILRFAIQDISVEETSAKEGLLLWCQRKTAPYKNVNIQNFHISWKDGLGFCALIHRHRPELIDYGKLRKDDPLTNLNTAFDVAEKYLDIPKMLDAEDIVGTARPDEKAIMTYVSSFYHAFSGAQKAETAANRICKVLAVNQENEQLMEDYEKLASDLLEWIRRTIPWLENRVPENTMHAMQQKLEDFRDYRRLHKPPKVQEKCQLEINFNTLQTKLRLSNRPAFMPSEGRMVSDINNAWGCLEQVEKGYEEWLLNEIRRLERLDHLAEKFRQKASIHEAWTDGKEAMLRQKDYETATLSEIKALLKKHEAFESDLAAHQDRVEQIAAIAQELNELDYYDSPSVNARCQKICDQWDNLGALTQKRREALERTEKLLETIDQLYLEYAKRAAPFNNWMEGAMEDLQDTFIVHTIEEIQGLTTAHEQFKATLPDADKERLAILGIHNEVSKIVQTYHVNMAGTNPYTTITPQEINGKWDHVRQLVPRRDQALTEEHARQQHNERLRKQFGAQANVIGPWIQTKMEEIGRISIEMHGTLEDQLSHLRQYEKSIVNYKPKIDQLEGDHQLIQEALIFDNKHTNYTMEHIRVGWEQLLTTIARTINEVENQILTRDAKGISQEQMNEFRASFNHFDRDHSGTLGPEEFKACLISLGYDIGNDPQGEAEFARIMSIVDPNRLGVVTFQAFIDFMSRETADTDTADQVMASFKILAGDKNYITMDELRRELPPDQAEYCIARMAPYTGPDSVPGALDYMSFSTALYGESDL
292	O75078	>sp|O75078|ADA11_HUMAN Disintegrin and metalloproteinase domain-containing protein 11 GN=ADAM11 PE=2 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MRLLRRWAFAALLLSLLPTPGLGTQGPAGALRWGGLPQLGGPGAPEVTEPSRLVRESSGGEVRKQQLDTRVRQEPPGGPPVHLAQVSFVIPAFNSNFTLDLELNHHLLSSQYVERHFSREGTTQHSTGAGDHCYYQGKLRGNPHSFAALSTCQGLHGVFSDGNLTYIVEPQEVAGPWGAPQGPLPHLIYRTPLLPDPLGCREPGCLFAVPAQSAPPNRPRLRRKRQVRRGHPTVHSETKYVELIVINDHQLFEQMRQSVVLTSNFAKSVVNLADVIYKEQLNTRIVLVAMETWADGDKIQVQDDLLETLARLMVYRREGLPEPSDATHLFSGRTFQSTSSGAAYVGGICSLSHGGGVNEYGNMGAMAVTLAQTLGQNLGMMWNKHRSSAGDCKCPDIWLGCIMEDTGFYLPRKFSRCSIDEYNQFLQEGGGSCLFNKPLKLLDPPECGNGFVEAGEECDCGSVQECSRAGGNCCKKCTLTHDAMCSDGLCCRRCKYEPRGVSCREAVNECDIAETCTGDSSQCPPNLHKLDGYYCDHEQGRCYGGRCKTRDRQCQVLWGHAAADRFCYEKLNVEGTERGSCGRKGSGWVQCSKQDVLCGFLLCVNISGAPRLGDLVGDISSVTFYHQGKELDCRGGHVQLADGSDLSYVEDGTACGPNMLCLDHRCLPASAFNFSTCPGSGERRICSHHGVCSNEGKCICQPDWTGKDCSIHNPLPTSPPTGETERYKGPSGTNIIIGSIAGAVLVAAIVLGGTGWGFKNIRRGRSGGA
293	Q9Y3Q7	>sp|Q9Y3Q7|ADA18_HUMAN Disintegrin and metalloproteinase domain-containing protein 18 GN=ADAM18 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MFLLLALLTELGRLQAHEGSEGIFLHVTVPRKIKSNDSEVSERKMIYIITIDGQPYTLHLGKQSFLPQNFLVYTYNETGSLHSVSPYFMMHCHYQGYAAEFPNSFVTLSICSGLRGFLQFENISYGIEPVESSARFEHIIYQMKNNDPNVSILAVNYSHIWQKDQPYKVPLNSQIKNLSKLLPQYLEIYIIVEKALYDYMGSEMMAVTQKIVQVIGLVNTMFTQFKLTVILSSLELWSNENQISTSGDADDILQRFLAWKRDYLILRPHDIAYLLVYRKHPKYVGATFPGTVCNKSYDAGIAMYPDAIGLEGFSVIIAQLLGLNVGLTYDDITQCFCLRATCIMNHEAVSASGRKIFSNCSMHDYRYFVSKFETKCLQKLSNLQPLHQNQPVCGNGILESNEECDCGNKNECQFKKCCDYNTCKLKGSVKCGSGPCCTSKCELSIAGTPCRKSIDPECDFTEYCNGTSSNCVPDTYALNGRLCKLGTAYCYNGQCQTTDNQCAKIFGKGAQGAPFACFKEVNSLHERSENCGFKNSQPLPCERKDVLCGKLACVQPHKNANKSDAQSTVYSYIQDHVCVSIATGSSMRSDGTDNAYVADGTMCGPEMYCVNKTCRKVHLMGYNCNATTKCKGKGICNNFGNCQCFPGHRPPDCKFQFGSPGGSIDDGNFQKSGDFYTEKGYNTHWNNWFILSFCIFLPFFIVFTTVIFKRNEISKSCNRENAEYNRNSSVVSESDDVGH
295	Q9H2U9	>sp|Q9H2U9|ADAM7_HUMAN Disintegrin and metalloproteinase domain-containing protein 7 GN=ADAM7 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MLPGCIFLMILLIPQVKEKFILGVEGQQLVRPKKLPLIQKRDTGHTHDDDILKTYEEELLYEIKLNRKTLVLHLLRSREFLGSNYSETFYSMKGEAFTRHPQIMDHCFYQGSIVHEYDSAASISTCNGLRGFFRINDQRYLIEPVKYSDEGEHLVFKYNLRVPYGANYSCTELNFTRKTVPGDNESEEDSKIKGIHDEKYVELFIVADDTVYRRNGHPHNKLRNRIWGMVNFVNMIYKTLNIHVTLVGIEIWTHEDKIELYSNIETTLLRFSFWQEKILKTRKDFDHVVLLSGKWLYSHVQGISYPGGMCLPYYSTSIIKDLLPDTNIIANRMAHQLGHNLGMQHDEFPCTCPSGKCVMDSDGSIPALKFSKCSQNQYHQYLKDYKPTCMLNIPFPYNFHDFQFCGNKKLDEGEECDCGPAQECTNPCCDAHTCVLKPGFTCAEGECCESCQIKKAGSICRPAKDECDFPEMCTGHSPACPKDQFRVNGFPCKNSEGYCFMGKCPTREDQCSELFDDEAIESHDICYKMNTKGNKFGYCKNKENRFLPCEEKDVRCGKIYCTGGELSSLLGEDKTYHLKDPQKNATVKCKTIFLYHDSTDIGLVASGTKCGEGMVCNNGECLNMEKVYISTNCPSQCNENPVDGHGLQCHCEEGQAPVACEETLHVTNITILVVVLVLVIVGIGVLILLVRYRKCIKLKQVQSPPTETLGVENKGYFGDEQQIRTEPILPEIHFLNKPASKDSRGIADPNQSAK
296	P78325	>sp|P78325|ADAM8_HUMAN Disintegrin and metalloproteinase domain-containing protein 8 GN=ADAM8 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MRGLGLWLLGAMMLPAIAPSRPWALMEQYEVVLPWRLPGPRVRRALPSHLGLHPERVSYVLGATGHNFTLHLRKNRDLLGSGYTETYTAANGSEVTEQPRGQDHCFYQGHVEGYPDSAASLSTCAGLRGFFQVGSDLHLIEPLDEGGEGGRHAVYQAEHLLQTAGTCGVSDDSLGSLLGPRTAAVFRPRPGDSLPSRETRYVELYVVVDNAEFQMLGSEAAVRHRVLEVVNHVDKLYQKLNFRVVLVGLEIWNSQDRFHVSPDPSVTLENLLTWQARQRTRRHLHDNVQLITGVDFTGTTVGFARVSAMCSHSSGAVNQDHSKNPVGVACTMAHEMGHNLGMDHDENVQGCRCQERFEAGRCIMAGSIGSSFPRMFSDCSQAYLESFLERPQSVCLANAPDLSHLVGGPVCGNLFVERGEQCDCGPPEDCRNRCCNSTTCQLAEGAQCAHGTCCQECKVKPAGELCRPKKDMCDLEEFCDGRHPECPEDAFQENGTPCSGGYCYNGACPTLAQQCQAFWGPGGQAAEESCFSYDILPGCKASRYRADMCGVLQCKGGQQPLGRAICIVDVCHALTTEDGTAYEPVPEGTRCGPEKVCWKGRCQDLHVYRSSNCSAQCHNHGVCNHKQECHCHAGWAPPHCAKLLTEVHAASGSLPVFVVVVLVLLAVVLVTLAGIIVYRKARSRILSRNVAPKTTMGRSNPLFHQAASRVPAKGGAPAPSRGPQELVPTTHPGQPARHPASSVALKRPPPAPPVTVSSPPFPVPVYTRQAPKQVIKPTFAPPVPPVKPGAGAANPGPAEGAVGPKVALKPPIQRKQGAGAPTAP
297	Q9NPF8	>sp|Q9NPF8|ADAP2_HUMAN Arf-GAP with dual PH domain-containing protein 2 GN=ADAP2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MGDRERNKKRLLELLRAPDTGNAHCADCGAADPDWASYKLGIFICLNCCGVHRNFPDISRVKSVRLDFWDDSIVEFMIHNGNLRVKAKFEARVPAFYYIPQANDCLVLKEQWIRAKYERREFMADGETISLPGNREGFLWKRGRDNSQFLRRKFVLLAREGLLKYFTKEQGKSPKAVISIKDLNATFQTEKIGHPHGLQITYRRDGHTRNLFVYHESGKEIVDWFNALRAARLQYLKMAFPELPESELVPFLTRNYLKQGFMEKTGPKQKEPFKKRWFALDCHERRLLYYKNPLDAFEQGQVFLGNKEQGYEAYEDLPKGIRGNRWKAGLTIVTPERRFVLTCPSEKEQQEWLESLRGVLSSPLTPLNRLTASTESGRSSR
298	Q08462	>sp|Q08462|ADCY2_HUMAN Adenylate cyclase type 2 GN=ADCY2 PE=1 SV=5 Homo sapiens OS=Human NCBI_TaxID=9606	MWQEAMRRRRYLRDRSEEAAGGGDGLPRSRDWLYESYYCMSQQHPLIVFLLLIVMGSCLALLAVFFALGLEVEDHVAFLITVPTALAIFFAIFILVCIESVFKKLLRLFSLVIWICLVAMGYLFMCFGGTVSPWDQVSFFLFIIFVVYTMLPFNMRDAIIASVLTSSSHTIVLSVCLSATPGGKEHLVWQILANVIIFICGNLAGAYHKHLMELALQQTYQDTCNCIKSRIKLEFEKRQQERLLLSLLPAHIAMEMKAEIIQRLQGPKAGQMENTNNFHNLYVKRHTNVSILYADIVGFTRLASDCSPGELVHMLNELFGKFDQIAKENECMRIKILGDCYYCVSGLPISLPNHAKNCVKMGLDMCEAIKKVRDATGVDINMRVGVHSGNVLCGVIGLQKWQYDVWSHDVTLANHMEAGGVPGRVHISSVTLEHLNGAYKVEEGDGDIRDPYLKQHLVKTYFVINPKGERRSPQHLFRPRHTLDGAKMRASVRMTRYLESWGAAKPFAHLHHRDSMTTENGKISTTDVPMGQHNFQNRTLRTKSQKKRFEEELNERMIQAIDGINAQKQWLKSEDIQRISLLFYNKVLEKEYRATALPAFKYYVTCACLIFFCIFIVQILVLPKTSVLGISFGAAFLLLAFILFVCFAGQLLQCSKKASPLLMWLLKSSGIIANRPWPRISLTIITTAIILMMAVFNMFFLSDSEETIPPTANTTNTSFSASNNQVAILRAQNLFFLPYFIYSCILGLISCSVFLRVNYELKMLIMMVALVGYNTILLHTHAHVLGDYSQVLFERPGIWKDLKTMGSVSLSIFFITLLVLGRQNEYYCRLDFLWKNKFKKEREEIETMENLNRVLLENVLPAHVAEHFLARSLKNEELYHQSYDCVCVMFASIPDFKEFYTESDVNKEGLECLRLLNEIIADFDDLLSKPKFSGVEKIKTIGSTYMAATGLSAVPSQEHSQEPERQYMHIGTMVEFAFALVGKLDAINKHSFNDFKLRVGINHGPVIAGVIGAQKPQYDIWGNTVNVASRMDSTGVLDKIQVTEETSLVLQTLGYTCTCRGIINVKGKGDLKTYFVNTEMSRSLSQSNVAS
299	O95622	>sp|O95622|ADCY5_HUMAN Adenylate cyclase type 5 GN=ADCY5 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MSGSKSVSPPGYAAQKTAAPAPRGGPEHRSAWGEADSRANGYPHAPGGSARGSTKKPGGAVTPQQQQRLASRWRSDDDDDPPLSGDDPLAGGFGFSFRSKSAWQERGGDDCGRGSRRQRRGAASGGSTRAPPAGGGGGSAAAAASAGGTEVRPRSVEVGLEERRGKGRAADELEAGAVEGGEGSGDGGSSADSGSGAGPGAVLSLGACCLALLQIFRSKKFPSDKLERLYQRYFFRLNQSSLTMLMAVLVLVCLVMLAFHAARPPLQLPYLAVLAAAVGVILIMAVLCNRAAFHQDHMGLACYALIAVVLAVQVVGLLLPQPRSASEGIWWTVFFIYTIYTLLPVRMRAAVLSGVLLSALHLAIALRTNAQDQFLLKQLVSNVLIFSCTNIVGVCTHYPAEVSQRQAFQETRECIQARLHSQRENQQQERLLLSVLPRHVAMEMKADINAKQEDMMFHKIYIQKHDNVSILFADIEGFTSLASQCTAQELVMTLNELFARFDKLAAENHCLRIKILGDCYYCVSGLPEARADHAHCCVEMGMDMIEAISLVREVTGVNVNMRVGIHSGRVHCGVLGLRKWQFDVWSNDVTLANHMEAGGKAGRIHITKATLNYLNGDYEVEPGCGGERNAYLKEHSIETFLILRCTQKRKEEKAMIAKMNRQRTNSIGHNPPHWGAERPFYNHLGGNQVSKEMKRMGFEDPKDKNAQESANPEDEVDEFLGRAIDARSIDRLRSEHVRKFLLTFREPDLEKKYSKQVDDRFGAYVACASLVFLFICFVQITIVPHSIFMLSFYLTCSLLLTLVVFVSVIYSCVKLFPSPLQTLSRKIVRSKMNSTLVGVFTITLVFLAAFVNMFTCNSRDLLGCLAQEHNISASQVNACHVAESAVNYSLGDEQGFCGSPWPNCNFPEYFTYSVLLSLLACSVFLQISCIGKLVLMLAIELIYVLIVEVPGVTLFDNADLLVTANAIDFFNNGTSQCPEHATKVALKVVTPIIISVFVLALYLHAQQVESTARLDFLWKLQATEEKEEMEELQAYNRRLLHNILPKDVAAHFLARERRNDELYYQSCECVAVMFASIANFSEFYVELEANNEGVECLRLLNEIIADFDEIISEDRFRQLEKIKTIGSTYMAASGLNDSTYDKVGKTHIKALADFAMKLMDQMKYINEHSFNNFQMKIGLNIGPVVAGVIGARKPQYDIWGNTVNVASRMDSTGVPDRIQVTTDMYQVLAANTYQLECRGVVKVKGKGEMMTYFLNGGPPLS
300	P35612	>sp|P35612|ADDB_HUMAN Beta-adducin GN=ADD2 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MSEETVPEAASPPPPQGQPYFDRFSEDDPEYMRLRNRAADLRQDFNLMEQKKRVTMILQSPSFREELEGLIQEQMKKGNNSSNIWALRQIADFMASTSHAVFPTSSMNVSMMTPINDLHTADSLNLAKGERLMRCKISSVYRLLDLYGWAQLSDTYVTLRVSKEQDHFLISPKGVSCSEVTASSLIKVNILGEVVEKGSSCFPVDTTGFCLHSAIYAARPDVRCIIHLHTPATAAVSAMKWGLLPVSHNALLVGDMAYYDFNGEMEQEADRINLQKCLGPTCKILVLRNHGVVALGDTVEEAFYKIFHLQAACEIQVSALSSAGGVENLILLEQEKHRPHEVGSVQWAGSTFGPMQKSRLGEHEFEALMRMLDNLGYRTGYTYRHPFVQEKTKHKSEVEIPATVTAFVFEEDGAPVPALRQHAQKQQKEKTRWLNTPNTYLRVNVADEVQRSMGSPRPKTTWMKADEVEKSSSGMPIRIENPNQFVPLYTDPQEVLEMRNKIREQNRQDVKSAGPQSQLLASVIAEKSRSPSTESQLMSKGDEDTKDDSEETVPNPFSQLTDQELEEYKKEVERKKLELDGEKETAPEEPGSPAKSAPASPVQSPAKEAETKSPLVSPSKSLEEGTKKTETSKAATTEPETTQPEGVVVNGREEEQTAEEILSKGLSQMTTSADTDVDTSKDKTESVTSGPMSPEGSPSKSPSKKKKKFRTPSFLKKSKKKEKVES
301	P30153	>sp|P30153|2AAA_HUMAN Serine/threonine-protein phosphatase 2A 65 kDa regulatory subunit A alpha isoform GN=PPP2R1A PE=1 SV=4 Homo sapiens OS=Human NCBI_TaxID=9606	MAAADGDDSLYPIAVLIDELRNEDVQLRLNSIKKLSTIALALGVERTRSELLPFLTDTIYDEDEVLLALAEQLGTFTTLVGGPEYVHCLLPPLESLATVEETVVRDKAVESLRAISHEHSPSDLEAHFVPLVKRLAGGDWFTSRTSACGLFSVCYPRVSSAVKAELRQYFRNLCSDDTPMVRRAAASKLGEFAKVLELDNVKSEIIPMFSNLASDEQDSVRLLAVEACVNIAQLLPQEDLEALVMPTLRQAAEDKSWRVRYMVADKFTELQKAVGPEITKTDLVPAFQNLMKDCEAEVRAAASHKVKEFCENLSADCRENVIMSQILPCIKELVSDANQHVKSALASVIMGLSPILGKDNTIEHLLPLFLAQLKDECPEVRLNIISNLDCVNEVIGIRQLSQSLLPAIVELAEDAKWRVRLAIIEYMPLLAGQLGVEFFDEKLNSLCMAWLVDHVYAIREAATSNLKKLVEKFGKEWAHATIIPKVLAMSGDPNYLHRMTTLFCINVLSEVCGQDITTKHMLPTVLRMAGDPVANVRFNVAKSLQKIGPILDNSTLQSEVKPILEKLTQDQDVDVKYFAQEALTVLSLA
302	Q00005	>sp|Q00005|2ABB_HUMAN Serine/threonine-protein phosphatase 2A 55 kDa regulatory subunit B beta isoform GN=PPP2R2B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MEEDIDTRKINNSFLRDHSYATEADIISTVEFNHTGELLATGDKGGRVVIFQREQESKNQVHRRGEYNVYSTFQSHEPEFDYLKSLEIEEKINKIRWLPQQNAAYFLLSTNDKTVKLWKVSERDKRPEGYNLKDEEGRLRDPATITTLRVPVLRPMDLMVEATPRRVFANAHTYHINSISVNSDYETYMSADDLRINLWNFEITNQSFNIVDIKPANMEELTEVITAAEFHPHHCNTFVYSSSKGTIRLCDMRASALCDRHTKFFEEPEDPSNRSFFSEIISSISDVKFSHSGRYIMTRDYLTVKVWDLNMENRPIETYQVHDYLRSKLCSLYENDCIFDKFECVWNGSDSVIMTGSYNNFFRMFDRNTKRDVTLEASRENSKPRAILKPRKVCVGGKRRKDEISVDSLDFSKKILHTAWHPSENIIAVAATNNLYIFQDKVN
303	P04229	>sp|P04229|2B11_HUMAN HLA class II histocompatibility antigen, DRB1-1 beta chain GN=HLA-DRB1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MVCLKLPGGSCMTALTVTLMVLSSPLALAGDTRPRFLWQLKFECHFFNGTERVRLLERCIYNQEESVRFDSDVGEYRAVTELGRPDAEYWNSQKDLLEQRRAAVDTYCRHNYGVGESFTVQRRVEPKVTVYPSKTQPLQHHNLLVCSVSGFYPGSIEVRWFRNGQEEKAGVVSTGLIQNGDWTFQTLVMLETVPRSGEVYTCQVEHPSVTSPLTVEWRARSESAQSKMLSGVGGFVLGLLFLGAGLFIYFRNQKGHSGLQPTGFLS
305	Q5Y7A7	>sp|Q5Y7A7|2B1D_HUMAN HLA class II histocompatibility antigen, DRB1-13 beta chain GN=HLA-DRB1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MVCLRLPGGSCMAVLTVTLMVLSSPLALAGDTRPRFLEYSTSECHFFNGTERVRFLDRYFHNQEENVRFDSDVGEFRAVTELGRPDAEYWNSQKDILEDERAAVDTYCRHNYGVVESFTVQRRVHPKVTVYPSKTQPLQHHNLLVCSVSGFYPGSIEVRWFRNGQEEKTGVVSTGLIHNGDWTFQTLVMLETVPRSGEVYTCQVEHPSVTSPLTVEWRARSESAQSKMLSGVGGFVLGLLFLGAGLFIYFRNQKGHSGLQPRGFLS
306	Q9H2F3	>sp|Q9H2F3|3BHS7_HUMAN 3 beta-hydroxysteroid dehydrogenase type 7 GN=HSD3B7 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MADSAQAQKLVYLVTGGCGFLGEHVVRMLLQREPRLGELRVFDQHLGPWLEELKTGPVRVTAIQGDVTQAHEVAAAVAGAHVVIHTAGLVDVFGRASPKTIHEVNVQGTRNVIEACVQTGTRFLVYTSSMEVVGPNTKGHPFYRGNEDTPYEAVHRHPYPCSKALAEWLVLEANGRKVRGGLPLVTCALRPTGIYGEGHQIMRDFYRQGLRLGGWLFRAIPASVEHGRVYVGNVAWMHVLAARELEQRATLMGGQVYFCYDGSPYRSYEDFNMEFLGPCGLRLVGARPLLPYWLLVFLAALNALLQWLLRPLVLYAPLLNPYTLAVANTTFTVSTDKAQRHFGYEPLFSWEDSRTRTILWVQAATGSAQ
307	O95336	>sp|O95336|6PGL_HUMAN 6-phosphogluconolactonase GN=PGLS PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAAPAPGLISVFSSSQELGAALAQLVAQRAACCLAGARARFALGLSGGSLVSMLARELPAAVAPAGPASLARWTLGFCDERLVPFDHAESTYGLYRTHLLSRLPIPESQVITINPELPVEEAAEDYAKKLRQAFQGDSIPVFDLLILGVGPDGHTCSLFPDHPLLQEREKIVAPISDSPKPPPQRVTLTLPVLNAARTVIFVATGEGKAAVLKRILEDQEENPLPAALVQPHTGKLCWFLDEAAARLLTVPFEKHSTL
308	P0DKL9	>sp|P0DKL9|A14EL_HUMAN ARL14 effector protein-like GN=ARL14EPL PE=4 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MNEQSEKNNSIQERHTDHSFPEKNCQIGQKQLQQIERQLKCLAFRNPGPQVADFNPETRQQKKKARMSKMNEYFSTKYKIMRKYDKSGRLICNDADLCDCLEKNCLGCFYPCPKCNSNKCGPECRCNRRWVYDAIVTESGEVISTLPFNVPD
309	Q8NF67	>sp|Q8NF67|A2012_HUMAN Putative ankyrin repeat domain-containing protein 20A12 pseudogene GN=ANKRD20A12P PE=5 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MKEMYENAEDKVNNSTGKWSCVEERICHLQHENPCIEQQLDDVHQKEDHKEIVTNIQRGFIESGKKDLMLEEKNKKLMNECDHLKESLFQYEREKAERVVVVRQLQQEAADSLKKLTMLESPLEGISHYHINLDETQVPKKKLFQVESQFDDLMVEKEAVSSKCVNLAKENQVFQQKLLSMKKVQQECEKLEEDKKMLEEEILNLKTHMENSMVELSKLQEYKSELDERAMQAVEKLEEIHLQEQAQYKKQLEQLNKDIIQLH
310	A0PJZ0	>sp|A0PJZ0|A20A5_HUMAN Putative ankyrin repeat domain-containing protein 20A5 GN=ANKRD20A5P PE=5 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MKLFGFRSRRGQTVLGSIDHLYTGSGYRIRYSELQKIHKAAVKGDAAEMERCLARRSGDLDALDKQHRTALHLACASGHVKVVTLLVNRKCQIDIYDKENRTPLIQAVHCQEEACAVILLEHGANPNLKDIYGNTALHYAVYSESTSLAEKLLFHGENIEALDKV
311	P08697	>sp|P08697|A2AP_HUMAN Alpha-2-antiplasmin GN=SERPINF2 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MALLWGLLVLSWSCLQGPCSVFSPVSAMEPLGRQLTSGPNQEQVSPLTLLKLGNQEPGGQTALKSPPGVCSRDPTPEQTHRLARAMMAFTADLFSLVAQTSTCPNLILSPLSVALALSHLALGAQNHTLQRLQQVLHAGSGPCLPHLLSRLCQDLGPGAFRLAARMYLQKGFPIKEDFLEQSEQLFGAKPVSLTGKQEDDLANINQWVKEATEGKIQEFLSGLPEDTVLLLLNAIHFQGFWRNKFDPSLTQRDSFHLDEQFTVPVEMMQARTYPLRWFLLEQPEIQVAHFPFKNNMSFVVLVPTHFEWNVSQVLANLSWDTLHPPLVWERPTKVRLPKLYLKHQMDLVATLSQLGLQELFQAPDLRGISEQSLVVSGVQHQSTLELSEVGVEAAAATSIAMSRMSLSSFSVNRPFLFFIFEDTTGLPLFVGSVRNPNPSAPRELKEQQDSPGNKDFLQSLKGFPRGDKLFGPDLKLVPPMEEDYPQFGSPK
312	P01023	>sp|P01023|A2MG_HUMAN Alpha-2-macroglobulin GN=A2M PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MGKNKLLHPSLVLLLLVLLPTDASVSGKPQYMVLVPSLLHTETTEKGCVLLSYLNETVTVSASLESVRGNRSLFTDLEAENDVLHCVAFAVPKSSSNEEVMFLTVQVKGPTQEFKKRTTVMVKNEDSLVFVQTDKSIYKPGQTVKFRVVSMDENFHPLNELIPLVYIQDPKGNRIAQWQSFQLEGGLKQFSFPLSSEPFQGSYKVVVQKKSGGRTEHPFTVEEFVLPKFEVQVTVPKIITILEEEMNVSVCGLYTYGKPVPGHVTVSICRKYSDASDCHGEDSQAFCEKFSGQLNSHGCFYQQVKTKVFQLKRKEYEMKLHTEAQIQEEGTVVELTGRQSSEITRTITKLSFVKVDSHFRQGIPFFGQVRLVDGKGVPIPNKVIFIRGNEANYYSNATTDEHGLVQFSINTTNVMGTSLTVRVNYKDRSPCYGYQWVSEEHEEAHHTAYLVFSPSKSFVHLEPMSHELPCGHTQTVQAHYILNGGTLLGLKKLSFYYLIMAKGGIVRTGTHGLLVKQEDMKGHFSISIPVKSDIAPVARLLIYAVLPTGDVIGDSAKYDVENCLANKVDLSFSPSQSLPASHAHLRVTAAPQSVCALRAVDQSVLLMKPDAELSASSVYNLLPEKDLTGFPGPLNDQDNEDCINRHNVYINGITYTPVSSTNEKDMYSFLEDMGLKAFTNSKIRKPKMCPQLQQYEMHGPEGLRVGFYESDVMGRGHARLVHVEEPHTETVRKYFPETWIWDLVVVNSAGVAEVGVTVPDTITEWKAGAFCLSEDAGLGISSTASLRAFQPFFVELTMPYSVIRGEAFTLKATVLNYLPKCIRVSVQLEASPAFLAVPVEKEQAPHCICANGRQTVSWAVTPKSLGNVNFTVSAEALESQELCGTEVPSVPEHGRKDTVIKPLLVEPEGLEKETTFNSLLCPSGGEVSEELSLKLPPNVVEESARASVSVLGDILGSAMQNTQNLLQMPYGCGEQNMVLFAPNIYVLDYLNETQQLTPEIKSKAIGYLNTGYQRQLNYKHYDGSYSTFGERYGRNQGNTWLTAFVLKTFAQARAYIFIDEAHITQALIWLSQRQKDNGCFRSSGSLLNNAIKGGVEDEVTLSAYITIALLEIPLTVTHPVVRNALFCLESAWKTAQEGDHGSHVYTKALLAYAFALAGNQDKRKEVLKSLNEEAVKKDNSVHWERPQKPKAPVGHFYEPQAPSAEVEMTSYVLLAYLTAQPAPTSEDLTSATNIVKWITKQQNAQGGFSSTQDTVVALHALSKYGAATFTRTGKAAQVTIQSSGTFSSKFQVDNNNRLLLQQVSLPELPGEYSMKVTGEGCVYLQTSLKYNILPEKEEFPFALGVQTLPQTCDEPKAHTSFQISLSVSYTGSRSASNMAIVDVKMVSGFIPLKPTVKMLERSNHVSRTEVSSNHVLIYLDKVSNQTLSLFFTVLQDVPVRDLKPAIVKVYDYYETDEFAIAEYNAPCSKDLGNA
313	A7E2S9	>sp|A7E2S9|A30BL_HUMAN Putative ankyrin repeat domain-containing protein 30B-like GN=ANKRD30BL PE=2 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MERLSAAPVKGQTGPERPSPFSQLVYTNNDSYVIHHGDLRKIHKAASRGQAWKLERMMKKTTMDLNIRDAKKRTALYWACANGHAEVVTLLVDRKCQLDVLDGENRTILMKALQCQREACANILIDSGADPNIVDVYGNTAVHYAVNSENLSVVAKLLSCGADIEVKNKAGHTPLLLAIRKRSEEIVEFLLTKNANANAVDKFKCVHQQLLEYKQKISKNSQNSNPEGTSEGTPDEAAPLAERTPDTAESLVERTPDE
314	Q9UNA3	>sp|Q9UNA3|A4GCT_HUMAN Alpha-1,4-N-acetylglucosaminyltransferase GN=A4GNT PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRKELQLSLSVTLLLVCGFLYQFTLKSSCLFCLPSFKSHQGLEALLSHRRGIVFLETSERMEPPHLVSCSVESAAKIYPEWPVVFFMKGLTDSTPMPSNSTYPAFSFLSAIDNVFLFPLDMKRLLEDTPLFSWYNQINASAERNWLHISSDASRLAIIWKYGGIYMDTDVISIRPIPEENFLAAQASRYSSNGIFGFLPHHPFLWECMENFVEHYNSAIWGNQGPELMTRMLRVWCKLEDFQEVSDLRCLNISFLHPQRFYPISYREWRRYYEVWDTEPSFNVSYALHLWNHMNQEGRAVIRGSNTLVENLYRKHCPRTYRDLIKGPEGSVTGELGPGNK
315	P30542	>sp|P30542|AA1R_HUMAN Adenosine receptor A1 GN=ADORA1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MPPSISAFQAAYIGIEVLIALVSVPGNVLVIWAVKVNQALRDATFCFIVSLAVADVAVGALVIPLAILINIGPQTYFHTCLMVACPVLILTQSSILALLAIAVDRYLRVKIPLRYKMVVTPRRAAVAIAGCWILSFVVGLTPMFGWNNLSAVERAWAANGSMGEPVIKCEFEKVISMEYMVYFNFFVWVLPPLLLMVLIYLEVFYLIRKQLNKKVSASSGDPQKYYGKELKIAKSLALILFLFALSWLPLHILNCITLFCPSCHKPSILTYIAIFLTHGNSAMNPIVYAFRIQKFRVTFLKIWNDHFRCQPAPPIDEDLPEERPDD
316	Q7Z5M8	>sp|Q7Z5M8|AB12B_HUMAN Protein ABHD12B GN=ABHD12B PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MDAQDCQAAASPEPPGPPARSCVAAWWDMVDRNLRYFPHSCSMLGRKIAALYDSFTSKSLKEHVFLPLIDMLIYFNFFKAPFLVDLKKPELKIPHTVNFYLRVEPGVMLGIWHTVPSCRGEDAKGKDCCWYEAALRDGNPIIVYLHGSAEHRAASHRLKLVKVLSDGGFHVLSVDYRGFGDSTGKPTEEGLTTDAICVYEWTKARSGITPVCLWGHSLGTGVATNAAKVLEEKGCPVDAIVLEAPFTNMWVASINYPLLKIYRNIPGFLRTLMDALRKDKIIFPNDENVKFLSSPLLILHGEDDRTVPLEYGKKLYEIARNAYRNKERVKMVIFPPGFQHNLLCKSPTLLITVRDFLSKQWS
317	Q96GS6	>sp|Q96GS6|AB17A_HUMAN Protein ABHD17A GN=ABHD17A PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MNGLSLSELCCLFCCPPCPGRIAAKLAFLPPEATYSLVPEPEPGPGGAGAAPLGTLRASSGAPGRWKLHLTERADFQYSQRELDTIEVFPTKSARGNRVSCMYVRCVPGARYTVLFSHGNAVDLGQMSSFYIGLGSRLHCNIFSYDYSGYGASSGRPSERNLYADIDAAWQALRTRYGISPDSIILYGQSIGTVPTVDLASRYECAAVVLHSPLTSGMRVAFPDTKKTYCFDAFPNIEKVSKITSPVLIIHGTEDEVIDFSHGLALYERCPKAVEPLWVEGAGHNDIELYSQYLERLRRFISQELPSQRA
318	Q6PCB6	>sp|Q6PCB6|AB17C_HUMAN Protein ABHD17C GN=ABHD17C PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MPEPGPRMNGFSLGELCWLFCCPPCPSRIAAKLAFLPPEPTYTVLAPEQRGAGASAPAPAQATAAAAAAQPAPQQPEEGAGAGPGACSLHLSERADWQYSQRELDAVEVFFSRTARDNRLGCMFVRCAPSSRYTLLFSHGNAVDLGQMCSFYIGLGSRINCNIFSYDYSGYGVSSGKPSEKNLYADIDAAWQALRTRYGVSPENIILYGQSIGTVPTVDLASRYECAAVILHSPLMSGLRVAFPDTRKTYCFDAFPSIDKISKVTSPVLVIHGTEDEVIDFSHGLAMYERCPRAVEPLWVEGAGHNDIELYAQYLERLKQFISHELPNS
371	P86434	>sp|P86434|AAS1_HUMAN Putative uncharacterized protein ADORA2A-AS1 GN=ADORA2A-AS1 PE=5 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MEQDWQPGEEVTPGPEPCSKGQAPLYPIVHVTELKHTDPNFPSNSNAVGTSSGWNRIGTGCSHTWDWRFSCTQQALLPLLGAWEWSIDTEAGGGRREQSQKPCSNGGPAAAGEGRVLPSPCFPWSTCQAAIHKVCRWQGCTRPALLAPSLATLKEHSYP
319	O95870	>sp|O95870|ABHGA_HUMAN Protein ABHD16A GN=ABHD16A PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MAKLLSCVLGPRLYKIYRERDSERAPASVPETPTAVTAPHSSSWDTYYQPRALEKHADSILALASVFWSISYYSSPFAFFYLYRKGYLSLSKVVPFSHYAGTLLLLLAGVACLRGIGRWTNPQYRQFITILEATHRNQSSENKRQLANYNFDFRSWPVDFHWEEPSSRKESRGGPSRRGVALLRPEPLHRGTADTLLNRVKKLPCQITSYLVAHTLGRRMLYPGSVYLLQKALMPVLLQGQARLVEECNGRRAKLLACDGNEIDTMFVDRRGTAEPQGQKLVICCEGNAGFYEVGCVSTPLEAGYSVLGWNHPGFAGSTGVPFPQNEANAMDVVVQFAIHRLGFQPQDIIIYAWSIGGFTATWAAMSYPDVSAMILDASFDDLVPLALKVMPDSWRGLVTRTVRQHLNLNNAEQLCRYQGPVLLIRRTKDEIITTTVPEDIMSNRGNDLLLKLLQHRYPRVMAEEGLRVVRQWLEASSQLEEASIYSRWEVEEDWCLSVLRSYQAEHGPDFPWSVGEDMSADGRRQLALFLARKHLHNFEATHCTPLPAQNFQMPWHL
320	Q13085	>sp|Q13085|ACACA_HUMAN Acetyl-CoA carboxylase 1 GN=ACACA PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MDEPSPLAQPLELNQHSRFIIGSVSEDNSEDEISNLVKLDLLEEKEGSLSPASVGSDTLSDLGISSLQDGLALHIRSSMSGLHLVKQGRDRKKIDSQRDFTVASPAEFVTRFGGNKVIEKVLIANNGIAAVKCMRSIRRWSYEMFRNERAIRFVVMVTPEDLKANAEYIKMADHYVPVPGGPNNNNYANVELILDIAKRIPVQAVWAGWGHASENPKLPELLLKNGIAFMGPPSQAMWALGDKIASSIVAQTAGIPTLPWSGSGLRVDWQENDFSKRILNVPQELYEKGYVKDVDDGLQAAEEVGYPVMIKASEGGGGKGIRKVNNADDFPNLFRQVQAEVPGSPIFVMRLAKQSRHLEVQILADQYGNAISLFGRDCSVQRRHQKIIEEAPATIATPAVFEHMEQCAVKLAKMVGYVSAGTVEYLYSQDGSFYFLELNPRLQVEHPCTEMVADVNLPAAQLQIAMGIPLYRIKDIRMMYGVSPWGDSPIDFEDSAHVPCPRGHVIAARITSENPDEGFKPSSGTVQELNFRSNKNVWGYFSVAAAGGLHEFADSQFGHCFSWGENREEAISNMVVALKELSIRGDFRTTVEYLIKLLETESFQMNRIDTGWLDRLIAEKVQAERPDTMLGVVCGALHVADVSLRNSVSNFLHSLERGQVLPAHTLLNTVDVELIYEGVKYVLKVTRQSPNSYVVIMNGSCVEVDVHRLSDGGLLLSYDGSSYTTYMKEEVDRYRITIGNKTCVFEKENDPSVMRSPSAGKLIQYIVEDGGHVFAGQCYAEIEVMKMVMTLTAVESGCIHYVKRPGAALDPGCVLAKMQLDNPSKVQQAELHTGSLPRIQSTALRGEKLHRVFHYVLDNLVNVMNGYCLPDPFFSSKVKDWVERLMKTLRDPSLPLLELQDIMTSVSGRIPPNVEKSIKKEMAQYASNITSVLCQFPSQQIANILDSHAATLNRKSEREVFFMNTQSIVQLVQRYRSGIRGHMKAVVMDLLRQYLRVETQFQNGHYDKCVFALREENKSDMNTVLNYIFSHAQVTKKNLLVTMLIDQLCGRDPTLTDELLNILTELTQLSKTTNAKVALRARQVLIASHLPSYELRHNQVESIFLSAIDMYGHQFCIENLQKLILSETSIFDVLPNFFYHSNQVVRMAALEVYVRRAYIAYELNSVQHRQLKDNTCVVEFQFMLPTSHPNRGNIPTLNRMSFSSNLNHYGMTHVASVSDVLLDNSFTPPCQRMGGMVSFRTFEDFVRIFDEVMGCFSDSPPQSPTFPEAGHTSLYDEDKVPRDEPIHILNVAIKTDCDIEDDRLAAMFREFTQQNKATLVDHGIRRLTFLVAQKDFRKQVNYEVDRRFHREFPKFFTFRARDKFEEDRIYRHLEPALAFQLELNRMRNFDLTAIPCANHKMHLYLGAAKVEVGTEVTDYRFFVRAIIRHSDLVTKEASFEYLQNEGERLLLEAMDELEVAFNNTNVRTDCNHIFLNFVPTVIMDPSKIEESVRSMVMRYGSRLWKLRVLQAELKINIRLTPTGKAIPIRLFLTNESGYYLDISLYKEVTDSRTAQIMFQAYGDKQGPLHGMLINTPYVTKDLLQSKRFQAQSLGTTYIYDIPEMFRQSLIKLWESMSTQAFLPSPPLPSDMLTYTELVLDDQGQLVHMNRLPGGNEIGMVAWKMTFKSPEYPEGRDIIVIGNDITYRIGSFGPQEDLLFLRASELARAEGIPRIYVSANSGARIGLAEEIRHMFHVAWVDPEDPYKGYRYLYLTPQDYKRVSALNSVHCEHVEDEGESRYKITDIIGKEEGIGPENLRGSGMIAGESSLAYNEIITISLVTCRAIGIGAYLVRLGQRTIQVENSHLILTGAGALNKVLGREVYTSNNQLGGIQIMHNNGVTHCTVCDDFEGVFTVLHWLSYMPKSVHSSVPLLNSKDPIDRIIEFVPTKTPYDPRWMLAGRPHPTQKGQWLSGFFDYGSFSEIMQPWAQTVVVGRARLGGIPVGVVAVETRTVELSIPADPANLDSEAKIIQQAGQVWFPDSAFKTYQAIKDFNREGLPLMVFANWRGFSGGMKDMYDQVLKFGAYIVDGLRECCQPVLVYIPPQAELRGGSWVVIDSSINPRHMEMYADRESRGSVLEPEGTVEIKFRRKDLVKTMRRVDPVYIHLAERLGTPELSTAERKELENKLKEREEFLIPIYHQVAVQFADLHDTPGRMQEKGVISDILDWKTSRTFFYWRLRRLLLEDLVKKKIHNANPELTDGQIQAMLRRWFVEVEGTVKAYVWDNNKDLAEWLEKQLTEEDGVHSVIEENIKCISRDYVLKQIRSLVQANPEVAMDSIIHMTQHISPTQRAEVIRILSTMDSPST
321	Q9UKU7	>sp|Q9UKU7|ACAD8_HUMAN Isobutyryl-CoA dehydrogenase, mitochondrial GN=ACAD8 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLWSGCRRFGARLGCLPGGLRVLVQTGHRSLTSCIDPSMGLNEEQKEFQKVAFDFAAREMAPNMAEWDQKELFPVDVMRKAAQLGFGGVYIQTDVGGSGLSRLDTSVIFEALATGCTSTTAYISIHNMCAWMIDSFGNEEQRHKFCPPLCTMEKFASYCLTEPGSGSDAASLLTSAKKQGDHYILNGSKAFISGAGESDIYVVMCRTGGPGPKGISCIVVEKGTPGLSFGKKEKKVGWNSQPTRAVIFEDCAVPVANRIGSEGQGFLIAVRGLNGGRINIASCSLGAAHASVILTRDHLNVRKQFGEPLASNQYLQFTLADMATRLVAARLMVRNAAVALQEERKDAVALCSMAKLFATDECFAICNQALQMHGGYGYLKDYAVQQYVRDSRVHQILEGSNEVMRILISRSLLQE
322	P28330	>sp|P28330|ACADL_HUMAN Long-chain specific acyl-CoA dehydrogenase, mitochondrial GN=ACADL PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAARLLRGSLRVLGGHRAPRQLPAARCSHSGGEERLETPSAKKLTDIGIRRIFSPEHDIFRKSVRKFFQEEVIPHHSEWEKAGEVSREVWEKAGKQGLLGVNIAEHLGGIGGDLYSAAIVWEEQAYSNCSGPGFSIHSGIVMSYITNHGSEEQIKHFIPQMTAGKCIGAIAMTEPGAGSDLQGIKTNAKKDGSDWILNGSKVFISNGSLSDVVIVVAVTNHEAPSPAHGISLFLVENGMKGFIKGRKLHKMGLKAQDTAELFFEDIRLPASALLGEENKGFYYIMKELPQERLLIADVAISASEFMFEETRNYVKQRKAFGKTVAHLQTVQHKLAELKTHICVTRAFVDNCLQLHEAKRLDSATACMAKYWASELQNSVAYDCVQLHGGWGYMWEYPIAKAYVDARVQPIYGGTNEIMKELIAREIVFDK
323	P49748	>sp|P49748|ACADV_HUMAN Very long-chain specific acyl-CoA dehydrogenase, mitochondrial GN=ACADVL PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MQAARMAASLGRQLLRLGGGSSRLTALLGQPRPGPARRPYAGGAAQLALDKSDSHPSDALTRKKPAKAESKSFAVGMFKGQLTTDQVFPYPSVLNEEQTQFLKELVEPVSRFFEEVNDPAKNDALEMVEETTWQGLKELGAFGLQVPSELGGVGLCNTQYARLVEIVGMHDLGVGITLGAHQSIGFKGILLFGTKAQKEKYLPKLASGETVAAFCLTEPSSGSDAASIRTSAVPSPCGKYYTLNGSKLWISNGGLADIFTVFAKTPVTDPATGAVKEKITAFVVERGFGGITHGPPEKKMGIKASNTAEVFFDGVRVPSENVLGEVGSGFKVAMHILNNGRFGMAAALAGTMRGIIAKAVDHATNRTQFGEKIHNFGLIQEKLARMVMLQYVTESMAYMVSANMDQGATDFQIEAAISKIFGSEAAWKVTDECIQIMGGMGFMKEPGVERVLRDLRIFRIFEGTNDILRLFVALQGCMDKGKELSGLGSALKNPFGNAGLLLGEAGKQLRRRAGLGSGLSLSGLVHPELSRSGELAVRALEQFATVVEAKLIKHKKGIVNEQFLLQRLADGAIDLYAMVVVLSRASRSLSEGHPTAQHEKMLCDTWCIEAAARIREGMAALQSDPWQQELYRNFKSISKALVERGGVVTSNPLGF
324	Q96GR2	>sp|Q96GR2|ACBG1_HUMAN Long-chain-fatty-acid--CoA ligase ACSBG1 GN=ACSBG1 PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MPRNSGAGYGCPHGDPSMLDSRETPQESRQDMIVRTTQEKLKTSSLTDRQPLSKESLNHALELSVPEKVNNAQWDAPEEALWTTRADGRVRLRIDPSCPQLPYTVHRMFYEALDKYGDLIALGFKRQDKWEHISYSQYYLLARRAAKGFLKLGLKQAHSVAILGFNSPEWFFSAVGTVFAGGIVTGIYTTSSPEACQYIAYDCCANVIMVDTQKQLEKILKIWKQLPHLKAVVIYKEPPPNKMANVYTMEEFMELGNEVPEEALDAIIDTQQPNQCCVLVYTSGTTGNPKGVMLSQDNITWTARYGSQAGDIRPAEVQQEVVVSYLPLSHIAAQIYDLWTGIQWGAQVCFAEPDALKGSLVNTLREVEPTSHMGVPRVWEKIMERIQEVAAQSGFIRRKMLLWAMSVTLEQNLTCPGSDLKPFTTRLADYLVLAKVRQALGFAKCQKNFYGAAPMMAETQHFFLGLNIRLYAGYGLSETSGPHFMSSPYNYRLYSSGKLVPGCRVKLVNQDAEGIGEICLWGRTIFMGYLNMEDKTCEAIDEEGWLHTGDAGRLDADGFLYITGRLKELIITAGGENVPPVPIEEAVKMELPIISNAMLIGDQRKFLSMLLTLKCTLDPDTSDQTDNLTEQAMEFCQRVGSRATTVSEIIEKKDEAVYQAIEEGIRRVNMNAAARPYHIQKWAILERDFSISGGELGPTMKLKRLTVLEKYKGIIDSFYQEQKM
325	P30532	>sp|P30532|ACHA5_HUMAN Neuronal acetylcholine receptor subunit alpha-5 GN=CHRNA5 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAARGSGPRALRLLLLVQLVAGRCGLAGAAGGAQRGLSEPSSIAKHEDSLLKDLFQDYERWVRPVEHLNDKIKIKFGLAISQLVDVDEKNQLMTTNVWLKQEWIDVKLRWNPDDYGGIKVIRVPSDSVWTPDIVLFDNADGRFEGTSTKTVIRYNGTVTWTPPANYKSSCTIDVTFFPFDLQNCSMKFGSWTYDGSQVDIILEDQDVDKRDFFDNGEWEIVSATGSKGNRTDSCCWYPYVTYSFVIKRLPLFYTLFLIIPCIGLSFLTVLVFYLPSNEGEKICLCTSVLVSLTVFLLVIEEIIPSSSKVIPLIGEYLVFTMIFVTLSIMVTVFAINIHHRSSSTHNAMAPLVRKIFLHTLPKLLCMRSHVDRYFTQKEETESGSGPKSSRNTLEAALDSIRYITRHIMKENDVREVVEDWKFIAQVLDRMFLWTFLFVSIVGSLGLFVPVIYKWANILIPVHIGNANK
326	Q15825	>sp|Q15825|ACHA6_HUMAN Neuronal acetylcholine receptor subunit alpha-6 GN=CHRNA6 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLTSKGQGFLHGGLCLWLCVFTPFFKGCVGCATEERLFHKLFSHYNQFIRPVENVSDPVTVHFEVAITQLANVDEVNQIMETNLWLRHIWNDYKLRWDPMEYDGIETLRVPADKIWKPDIVLYNNAVGDFQVEGKTKALLKYNGMITWTPPAIFKSSCPMDITFFPFDHQNCSLKFGSWTYDKAEIDLLIIGSKVDMNDFWENSEWEIIDASGYKHDIKYNCCEEIYTDITYSFYIRRLPMFYTINLIIPCLFISFLTVLVFYLPSDCGEKVTLCISVLLSLTVFLLVITETIPSTSLVVPLVGEYLLFTMIFVTLSIVVTVFVLNIHYRTPTTHTMPRWVKTVFLKLLPQVLLMRWPLDKTRGTGSDAVPRGLARRPAKGKLASHGEPRHLKECFHCHKSNELATSKRRLSHQPLQWVVENSEHSPEVEDVINSVQFIAENMKSHNETKEVEDDWKYVAMVVDRVFLWVFIIVCVFGTAGLFLQPLLGNTGKS
327	Q9UGM1	>sp|Q9UGM1|ACHA9_HUMAN Neuronal acetylcholine receptor subunit alpha-9 GN=CHRNA9 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MNWSHSCISFCWIYFAASRLRAAETADGKYAQKLFNDLFEDYSNALRPVEDTDKVLNVTLQITLSQIKDMDERNQILTAYLWIRQIWHDAYLTWDRDQYDGLDSIRIPSDLVWRPDIVLYNKADDESSEPVNTNVVLRYDGLITWDAPAITKSSCVVDVTYFPFDNQQCNLTFGSWTYNGNQVDIFNALDSGDLSDFIEDVEWEVHGMPAVKNVISYGCCSEPYPDVTFTLLLKRRSSFYIVNLLIPCVLISFLAPLSFYLPAASGEKVSLGVTILLAMTVFQLMVAEIMPASENVPLIGKYYIATMALITASTALTIMVMNIHFCGAEARPVPHWARVVILKYMSRVLFVYDVGESCLSPHHSRERDHLTKVYSKLPESNLKAARNKDLSRKKDMNKRLKNDLGCQGKNPQEAESYCAQYKVLTRNIEYIAKCLKDHKATNSKGSEWKKVAKVIDRFFMWIFFIMVFVMTILIIARAD
328	P08172	>sp|P08172|ACM2_HUMAN Muscarinic acetylcholine receptor M2 GN=CHRM2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MNNSTNSSNNSLALTSPYKTFEVVFIVLVAGSLSLVTIIGNILVMVSIKVNRHLQTVNNYFLFSLACADLIIGVFSMNLYTLYTVIGYWPLGPVVCDLWLALDYVVSNASVMNLLIISFDRYFCVTKPLTYPVKRTTKMAGMMIAAAWVLSFILWAPAILFWQFIVGVRTVEDGECYIQFFSNAAVTFGTAIAAFYLPVIIMTVLYWHISRASKSRIKKDKKEPVANQDPVSPSLVQGRIVKPNNNNMPSSDDGLEHNKIQNGKAPRDPVTENCVQGEEKESSNDSTSVSAVASNMRDDEITQDENTVSTSLGHSKDENSKQTCIRIGTKTPKSDSCTPTNTTVEVVGSSGQNGDEKQNIVARKIVKMTKQPAKKKPPPSREKKVTRTILAILLAFIITWAPYNVMVLINTFCAPCIPNTVWTIGYWLCYINSTINPACYALCNATFKKTFKHLLMCHYKNIGATR
329	P21399	>sp|P21399|ACOC_HUMAN Cytoplasmic aconitate hydratase GN=ACO1 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MSNPFAHLAEPLDPVQPGKKFFNLNKLEDSRYGRLPFSIRVLLEAAIRNCDEFLVKKQDIENILHWNVTQHKNIEVPFKPARVILQDFTGVPAVVDFAAMRDAVKKLGGDPEKINPVCPADLVIDHSIQVDFNRRADSLQKNQDLEFERNRERFEFLKWGSQAFHNMRIIPPGSGIIHQVNLEYLARVVFDQDGYYYPDSLVGTDSHTTMIDGLGILGWGVGGIEAEAVMLGQPISMVLPQVIGYRLMGKPHPLVTSTDIVLTITKHLRQVGVVGKFVEFFGPGVAQLSIADRATIANMCPEYGATAAFFPVDEVSITYLVQTGRDEEKLKYIKKYLQAVGMFRDFNDPSQDPDFTQVVELDLKTVVPCCSGPKRPQDKVAVSDMKKDFESCLGAKQGFKGFQVAPEHHNDHKTFIYDNTEFTLAHGSVVIAAITSCTNTSNPSVMLGAGLLAKKAVDAGLNVMPYIKTSLSPGSGVVTYYLQESGVMPYLSQLGFDVVGYGCMTCIGNSGPLPEPVVEAITQGDLVAVGVLSGNRNFEGRVHPNTRANYLASPPLVIAYAIAGTIRIDFEKEPLGVNAKGQQVFLKDIWPTRDEIQAVERQYVIPGMFKEVYQKIETVNESWNALATPSDKLFFWNSKSTYIKSPPFFENLTLDLQPPKSIVDAYVLLNLGDSVTTDHISPAGNIARNSPAARYLTNRGLTPREFNSYGSRRGNDAVMARGTFANIRLLNRFLNKQAPQTIHLPSGEILDVFDAAERYQQAGLPLIVLAGKEYGAGSSRDWAAKGPFLLGIKAVLAESYERIHRSNLVGMGVIPLEYLPGENADALGLTGQERYTIIIPENLKPQMKVQVKLDTGKTFQAVMRFDTDVELTYFLNGGILNYMIRKMAK
330	O00767	>sp|O00767|ACOD_HUMAN Acyl-CoA desaturase GN=SCD PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MPAHLLQDDISSSYTTTTTITAPPSRVLQNGGDKLETMPLYLEDDIRPDIKDDIYDPTYKDKEGPSPKVEYVWRNIILMSLLHLGALYGITLIPTCKFYTWLWGVFYYFVSALGITAGAHRLWSHRSYKARLPLRLFLIIANTMAFQNDVYEWARDHRAHHKFSETHADPHNSRRGFFFSHVGWLLVRKHPAVKEKGSTLDLSDLEAEKLVMFQRRYYKPGLLMMCFILPTLVPWYFWGETFQNSVFVATFLRYAVVLNATWLVNSAAHLFGYRPYDKNISPRENILVSLGAVGEGFHNYHHSFPYDYSASEYRWHINFTTFFIDCMAALGLAYDRKKVSKAAILARIKRTGDGNYKSG
331	Q96QF7	>sp|Q96QF7|ACRC_HUMAN Acidic repeat-containing protein GN=ACRC PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MDGCKKELPRLQEPEEDEDCYILNVQSSSDDTSGSSVARRAPKRQASCILNVQSRSGDTSGSSVARRAPKRQASSVVVIDSDSDEECHTHEEKKAKLLEINSDDESPECCHVKPAIQEPPIVISDDDNDDDNGNDLEVPDDNSDDSEAPDDNSDDSEAPDDNSDDSEAPDDNSDDSEAPDDNSDDSDVPDDNSDDSSDDNSDDSSDDNSDDSDVPDDKSDDSDVPDDSSDDSDVPDDSSDDSEAPDDSSDDSEAPDDSSDDSEAPDDSSDDSEAPDDSSDDSEASDDSSDDSEASDDSSDDSEAPDDKSDDSDVPEDKSDDSDVPDDNSDDLEVPVPAEDLCNEGQIASDEEELVEAAAAVSQHDSSDDAGEQDLGENLSKPPSDPEANPEVSERKLPTEEEPAPVVEQSGKRKSKTKTIVEPPRKRQTKTKNIVEPPRKRQTKTKNIVEPLRKRKAKTKNVSVTPGHKKRGPSKKKPGAAKVEKRKTRTPKCKVPGCFLQDLEKSKKYSGKNLKRNKDELVQRIYDLFNRSVCDKKLPEKLRIGWNNKMVKTAGLCSTGEMWYPKWRRFAKIQIGLKVCDSADRIRDTLIHEMCHAASWLIDGIHDSHGDAWKYYARKSNRIHPELPRVTRCHNYKINYKVHYECTGCKTRIGCYTKSLDTSRFICAKCKGSLVMVPLTQKDGTRIVPHV
332	P33121	>sp|P33121|ACSL1_HUMAN Long-chain-fatty-acid--CoA ligase 1 GN=ACSL1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MQAHELFRYFRMPELVDFRQYVRTLPTNTLMGFGAFAALTTFWYATRPKPLKPPCDLSMQSVEVAGSGGARRSALLDSDEPLVYFYDDVTTLYEGFQRGIQVSNNGPCLGSRKPDQPYEWLSYKQVAELSECIGSALIQKGFKTAPDQFIGIFAQNRPEWVIIEQGCFAYSMVIVPLYDTLGNEAITYIVNKAELSLVFVDKPEKAKLLLEGVENKLIPGLKIIVVMDAYGSELVERGQRCGVEVTSMKAMEDLGRANRRKPKPPAPEDLAVICFTSGTTGNPKGAMVTHRNIVSDCSAFVKATENTVNPCPDDTLISFLPLAHMFERVVECVMLCHGAKIGFFQGDIRLLMDDLKVLQPTVFPVVPRLLNRMFDRIFGQANTTLKRWLLDFASKRKEAELRSGIIRNNSLWDRLIFHKVQSSLGGRVRLMVTGAAPVSATVLTFLRAALGCQFYEGYGQTECTAGCCLTMPGDWTAGHVGAPMPCNLIKLVDVEEMNYMAAEGEGEVCVKGPNVFQGYLKDPAKTAEALDKDGWLHTGDIGKWLPNGTLKIIDRKKHIFKLAQGEYIAPEKIENIYMRSEPVAQVFVHGESLQAFLIAIVVPDVETLCSWAQKRGFEGSFEELCRNKDVKKAILEDMVRLGKDSGLKPFEQVKGITLHPELFSIDNGLLTPTMKAKRPELRNYFRSQIDDLYSTIKV
333	P63267	>sp|P63267|ACTH_HUMAN Actin, gamma-enteric smooth muscle GN=ACTG2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MCEEETTALVCDNGSGLCKAGFAGDDAPRAVFPSIVGRPRHQGVMVGMGQKDSYVGDEAQSKRGILTLKYPIEHGIITNWDDMEKIWHHSFYNELRVAPEEHPTLLTEAPLNPKANREKMTQIMFETFNVPAMYVAIQAVLSLYASGRTTGIVLDSGDGVTHNVPIYEGYALPHAIMRLDLAGRDLTDYLMKILTERGYSFVTTAEREIVRDIKEKLCYVALDFENEMATAASSSSLEKSYELPDGQVITIGNERFRCPETLFQPSFIGMESAGIHETTYNSIMKCDIDIRKDLYANNVLSGGTTMYPGIADRMQKEITALAPSTMKIKIIAPPERKYSVWIGGSILASLSTFQQMWISKPEYDEAGPSIVHRKCF
334	Q8TDG2	>sp|Q8TDG2|ACTT1_HUMAN Actin-related protein T1 GN=ACTRT1 PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MFNPHALDVPAVIFDNGSGLCKAGLSGEIGPRHVISSVLGHCKFNVPLARLNQKYFVGQEALYKYEALHLHYPIERGLVTGWDDMEKLWKHLFERELGVKPSQQPVLMTEPSLNPREIREKLAEMMFETFSVPGFYLSNHAVAALYASACVTGLVVDSGDGVTCTVPIFEGYSLPHAVTKLCMAGRDITEHLTRLLFASGFNFPCILNKAVVNNIKEKLCYIALEPEKELRKSRGEVLGAYRLPDGHVIHFGDELYQVPEVLFAPDQLGIHSPGLSKMVSSSIMKCDTDIQNKLYADIVLSGGTTLLPGLEERLMKEVEQLASKGTPIKITASPDRCFSAWIGASIMTSMSSFKQMWVTSADFKEYGTSVVQRRCF
335	O43506	>sp|O43506|ADA20_HUMAN Disintegrin and metalloproteinase domain-containing protein 20 GN=ADAM20 PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAVGEPLVHIRVTLLLLWFGMFLSISGHSQARPSQYFTSPEVVIPLKVISRGRGAKAPGWLSYSLRFGGQRYIVHMRVNKLLFAAHLPVFTYTEQHALLQDQPFIQDDCYYHGYVEGVPESLVALSTCSGGFLGMLQINDLVYEIKPISVSATFEHLVYKIDSDDTQFPPMRCGLTEEKIAHQMELQLSYNFTLKQSSFVGWWTHQRFVELVVVVDNIRYLFSQSNATTVQHEVFNVVNIVDSFYHPLEVDVILTGIDIWTASNPLPTSGDLDNVLEDFSIWKNYNLNNRLQHDVAHLFIKDTQGMKLGVAYVKGICQNPFNTGVDVFEDNRLVVFAITLGHELGHNLGMQHDTQWCVCELQWCIMHAYRKVTTKFSNCSYAQYWDSTISSGLCIQPPPYPGNIFRLKYCGNLVVEEGEECDCGTIRQCAKDPCCLLNCTLHPGAACAFGICCKDCKFLPSGTLCRQQVGECDLPEWCNGTSHQCPDDVYVQDGISCNVNAFCYEKTCNNHDIQCKEIFGQDARSASQSCYQEINTQGNRFGHCGIVGTTYVKCWTPDIMCGRVQCENVGVIPNLIEHSTVQQFHLNDTTCWGTDYHLGMAIPDIGEVKDGTVCGPEKICIRKKCASMVHLSQACQPKTCNMRGICNNKQHCHCNHEWAPPYCKDKGYGGSADSGPPPKNNMEGLNVMGKLRYLSLLCLLPLVAFLLFCLHVLFKKRTKSKEDEEG
336	O75077	>sp|O75077|ADA23_HUMAN Disintegrin and metalloproteinase domain-containing protein 23 GN=ADAM23 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MKPPGSSSRQPPLAGCSLAGASCGPQRGPAGSVPASAPARTPPCRLLLVLLLLPPLAASSRPRAWGAAAPSAPHWNETAEKNLGVLADEDNTLQQNSSSNISYSNAMQKEITLPSRLIYYINQDSESPYHVLDTKARHQQKHNKAVHLAQASFQIEAFGSKFILDLILNNGLLSSDYVEIHYENGKPQYSKGGEHCYYHGSIRGVKDSKVALSTCNGLHGMFEDDTFVYMIEPLELVHDEKSTGRPHIIQKTLAGQYSKQMKNLTMERGDQWPFLSELQWLKRRKRAVNPSRGIFEEMKYLELMIVNDHKTYKKHRSSHAHTNNFAKSVVNLVDSIYKEQLNTRVVLVAVETWTEKDQIDITTNPVQMLHEFSKYRQRIKQHADAVHLISRVTFHYKRSSLSYFGGVCSRTRGVGVNEYGLPMAVAQVLSQSLAQNLGIQWEPSSRKPKCDCTESWGGCIMEETGVSHSRKFSKCSILEYRDFLQRGGGACLFNRPTKLFEPTECGNGYVEAGEECDCGFHVECYGLCCKKCSLSNGAHCSDGPCCNNTSCLFQPRGYECRDAVNECDITEYCTGDSGQCPPNLHKQDGYACNQNQGRCYNGECKTRDNQCQYIWGTKAAGSDKFCYEKLNTEGTEKGNCGKDGDRWIQCSKHDVFCGFLLCTNLTRAPRIGQLQGEIIPTSFYHQGRVIDCSGAHVVLDDDTDVGYVEDGTPCGPSMMCLDRKCLQIQALNMSSCPLDSKGKVCSGHGVCSNEATCICDFTWAGTDCSIRDPVRNLHPPKDEGPKGPSATNLIIGSIAGAILVAAIVLGGTGWGFKNVKKRRFDPTQQGPI
337	P08913	>sp|P08913|ADA2A_HUMAN Alpha-2A adrenergic receptor GN=ADRA2A PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MGSLQPDAGNASWNGTEAPGGGARATPYSLQVTLTLVCLAGLLMLLTVFGNVLVIIAVFTSRALKAPQNLFLVSLASADILVATLVIPFSLANEVMGYWYFGKAWCEIYLALDVLFCTSSIVHLCAISLDRYWSITQAIEYNLKRTPRRIKAIIITVWVISAVISFPPLISIEKKGGGGGPQPAEPRCEINDQKWYVISSCIGSFFAPCLIMILVYVRIYQIAKRRTRVPPSRRGPDAVAAPPGGTERRPNGLGPERSAGPGGAEAEPLPTQLNGAPGEPAPAGPRDTDALDLEESSSSDHAERPPGPRRPERGPRGKGKARASQVKPGDSLPRRGPGATGIGTPAAGPGEERVGAAKASRWRGRQNREKRFTFVLAVVIGVFVVCWFPFFFTYTLTAVGCSVPRTLFKFFFWFGYCNSSLNPVIYTIFNHDFRRAFKKILCRGDRKRIV
338	Q9BZ11	>sp|Q9BZ11|ADA33_HUMAN Disintegrin and metalloproteinase domain-containing protein 33 GN=ADAM33 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MGWRPRRARGTPLLLLLLLLLLWPVPGAGVLQGHIPGQPVTPHWVLDGQPWRTVSLEEPVSKPDMGLVALEAEGQELLLELEKNHRLLAPGYIETHYGPDGQPVVLAPNHTDHCHYQGRVRGFPDSWVVLCTCSGMSGLITLSRNASYYLRPWPPRGSKDFSTHEIFRMEQLLTWKGTCGHRDPGNKAGMTSLPGGPQSRGRREARRTRKYLELYIVADHTLFLTRHRNLNHTKQRLLEVANYVDQLLRTLDIQVALTGLEVWTERDRSRVTQDANATLWAFLQWRRGLWAQRPHDSAQLLTGRAFQGATVGLAPVEGMCRAESSGGVSTDHSELPIGAAATMAHEIGHSLGLSHDPDGCCVEAAAESGGCVMAAATGHPFPRVFSACSRRQLRAFFRKGGGACLSNAPDPGLPVPPALCGNGFVEAGEECDCGPGQECRDLCCFAHNCSLRPGAQCAHGDCCVRCLLKPAGALCRQAMGDCDLPEFCTGTSSHCPPDVYLLDGSPCARGSGYCWDGACPTLEQQCQQLWGPGSHPAPEACFQVVNSAGDAHGNCGQDSEGHFLPCAGRDALCGKLQCQGGKPSLLAPHMVPVDSTVHLDGQEVTCRGALALPSAQLDLLGLGLVEPGTQCGPRMVCQSRRCRKNAFQELQRCLTACHSHGVCNSNHNCHCAPGWAPPFCDKPGFGGSMDSGPVQAENHDTFLLAMLLSVLLPLLPGAGLAWCCYRLPGAHLQRCSWGCRRDPACSGPKDGPHRDHPLGGVHPMELGPTATGQPWPLDPENSHEPSSHPEKPLPAVSPDPQADQVQMPRSCLW
339	Q96M93	>sp|Q96M93|ADAD1_HUMAN Adenosine deaminase domain-containing protein 1 GN=ADAD1 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MASNNHWFQSSQVPSFAQMLKKNLPVQPATKTITTPTGWSSESYGLSKMASKVTQVTGNFPEPLLSKNLSSISNPVLPPKKIPKEFIMKYKRGEINPVSALHQFAQMQRVQLDLKETVTTGNVMGPYFAFCAVVDGIQYKTGLGQNKKESRSNAAKLALDELLQLDEPEPRILETSGPPPFPAEPVVLSELAYVSKVHYEGRHIQYAKISQIVKERFNQLISNRSEYLKYSSSLAAFIIERAGQHEVVAIGTGEYNYSQDIKPDGRVLHDTHAVVTARRSLLRYFYRQLLLFYSKNPAMMEKSIFCTEPTSNLLTLKQNINICLYMNQLPKGSAQIKSQLRLNPHSISAFEANEELCLHVAVEGKIYLTVYCPKDGVNRISSMSSSDKLTRWEVLGVQGALLSHFIQPVYISSILIGDGNCSDTRGLEIAIKQRVDDALTSKLPMFYLVNRPHISLVPSAYPLQMNLEYKFLSLNWAQGDVSLEIVDGLSGKITESSPFKSGMSMASRLCKAAMLSRFNLLAKEAKKELLEAGTYHAAKCMSASYQEAKCKLKSYLQQHGYGSWIVKSPCIEQFNM
340	Q6DHV7	>sp|Q6DHV7|ADAL_HUMAN Adenosine deaminase-like protein GN=ADAL PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MIEAEEQQPCKTDFYSELPKVELHAHLNGSISSHTMKKLIAQKPDLKIHDQMTVIDKGKKRTLEECFQMFQTIHQLTSSPEDILMVTKDVIKEFADDGVKYLELRSTPRRENATGMTKKTYVESILEGIKQSKQENLDIDVRYLIAVDRRGGPLVAKETVKLAEEFFLSTEGTVLGLDLSGDPTVGQAKDFLEPLLEAKKAGLKLALHLSEIPNQKKETQILLDLLPDRIGHGTFLNSGEGGSLDLVDFVRQHRIPLELCLTSNVKSQTVPSYDQHHFGFWYSIAHPSVICTDDKGVFATHLSQEYQLAAETFNLTQSQVWDLSYESINYIFASDSTRSELRKKWNHLKPRVLHI
341	Q99965	>sp|Q99965|ADAM2_HUMAN Disintegrin and metalloproteinase domain-containing protein 2 GN=ADAM2 PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MWRVLFLLSGLGGLRMDSNFDSLPVQITVPEKIRSIIKEGIESQASYKIVIEGKPYTVNLMQKNFLPHNFRVYSYSGTGIMKPLDQDFQNFCHYQGYIEGYPKSVVMVSTCTGLRGVLQFENVSYGIEPLESSVGFEHVIYQVKHKKADVSLYNEKDIESRDLSFKLQSVEPQQDFAKYIEMHVIVEKQLYNHMGSDTTVVAQKVFQLIGLTNAIFVSFNITIILSSLELWIDENKIATTGEANELLHTFLRWKTSYLVLRPHDVAFLLVYREKSNYVGATFQGKMCDANYAGGVVLHPRTISLESLAVILAQLLSLSMGITYDDINKCQCSGAVCIMNPEAIHFSGVKIFSNCSFEDFAHFISKQKSQCLHNQPRLDPFFKQQAVCGNAKLEAGEECDCGTEQDCALIGETCCDIATCRFKAGSNCAEGPCCENCLFMSKERMCRPSFEECDLPEYCNGSSASCPENHYVQTGHPCGLNQWICIDGVCMSGDKQCTDTFGKEVEFGPSECYSHLNSKTDVSGNCGISDSGYTQCEADNLQCGKLICKYVGKFLLQIPRATIIYANISGHLCIAVEFASDHADSQKMWIKDGTSCGSNKVCRNQRCVSSSYLGYDCTTDKCNDRGVCNNKKHCHCSASYLPPDCSVQSDLWPGGSIDSGNFPPVAIPARLPERRYIENIYHSKPMRWPFFLFIPFFIIFCVLIAIMVKVNFQRKKWRTEDYSSDEQPESESEPKG
342	O00116	>sp|O00116|ADAS_HUMAN Alkyldihydroxyacetonephosphate synthase, peroxisomal GN=AGPS PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAEAAAAAGGTGLGAGASYGSAADRDRDPDPDRAGRRLRVLSGHLLGRPREALSTNECKARRAASAATAAPTATPAAQESGTIPKKRQEVMKWNGWGYNDSKFIFNKKGQIELTGKRYPLSGMGLPTFKEWIQNTLGVNVEHKTTSKASLNPSDTPPSVVNEDFLHDLKETNISYSQEADDRVFRAHGHCLHEIFLLREGMFERIPDIVLWPTCHDDVVKIVNLACKYNLCIIPIGGGTSVSYGLMCPADETRTIISLDTSQMNRILWVDENNLTAHVEAGITGQELERQLKESGYCTGHEPDSLEFSTVGGWVSTRASGMKKNIYGNIEDLVVHIKMVTPRGIIEKSCQGPRMSTGPDIHHFIMGSEGTLGVITEATIKIRPVPEYQKYGSVAFPNFEQGVACLREIAKQRCAPASIRLMDNKQFQFGHALKPQVSSIFTSFLDGLKKFYITKFKGFDPNQLSVATLLFEGDREKVLQHEKQVYDIAAKFGGLAAGEDNGQRGYLLTYVIAYIRDLALEYYVLGESFETSAPWDRVVDLCRNVKERITRECKEKGVQFAPFSTCRVTQTYDAGACIYFYFAFNYRGISDPLTVFEQTEAAAREEILANGGSLSHHHGVGKLRKQWLKESISDVGFGMLKSVKEYVDPNNIFGNRNLL
343	Q5VUY0	>sp|Q5VUY0|ADCL3_HUMAN Arylacetamide deacetylase-like 3 GN=AADACL3 PE=2 SV=4 Homo sapiens OS=Human NCBI_TaxID=9606	MIFEKLRICSMPQFFCFMQDLPPLKYDPDVVVTDFRFGTIPVKLYQSKASTCTLKPGIVYYHGGGGVMGSLKTHHGICSRLCKESDSVVLAVGYRKLPKHKFPVPVRDCLVATIHFLKSLDAYGVDPARVVVCGDSFGGAIAAVVCQQLVDRPDLPRIRAQILIYAILQALDLQTPSFQQRKNIPLLTWSFICYCFFQNLDFSSSWQEVIMKGAHLPAEVWEKYRKWLGPENIPERFKERGYQLKPHEPMNEAAYLEVSVVLDVMCSPLIAEDDIVSQLPETCIVSCEYDALRDNSLLYKKRLEDLGVPVTWHHMEDGFHGVLRTIDMSFLHFPCSMRILSALVQFVKGL
344	Q08828	>sp|Q08828|ADCY1_HUMAN Adenylate cyclase type 1 GN=ADCY1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAGAPRGGGGGGGGAGEPGGAERAAGTSRRRGLRACDEEFACPELEALFRGYTLRLEQAATLKALAVLSLLAGALALAELLGAPGPAPGLAKGSHPVHCVLFLALLVVTNVRSLQVPQLQQVGQLALLFSLTFALLCCPFALGGPARGSAGAAGGPATAEQGVWQLLLVTFVSYALLPVRSLLAIGFGLVVAASHLLVTATLVPAKRPRLWRTLGANALLFVGVNMYGVFVRILTERSQRKAFLQARSCIEDRLRLEDENEKQERLLMSLLPRNVAMEMKEDFLKPPERIFHKIYIQRHDNVSILFADIVGFTGLASQCTAQELVKLLNELFGKFDELATENHCRRIKILGDCYYCVSGLTQPKTDHAHCCVEMGLDMIDTITSVAEATEVDLNMRVGLHTGRVLCGVLGLRKWQYDVWSNDVTLANVMEAAGLPGKVHITKTTLACLNGDYEVEPGYGHERNSFLKTHNIETFFIVPSHRRKIFPGLILSDIKPAKRMKFKTVCYLLVQLMHCRKMFKAEIPFSNVMTCEDDDKRRALRTASEKLRNRSSFSTNVVYTTPGTRVNRYISRLLEARQTELEMADLNFFTLKYKHVEREQKYHQLQDEYFTSAVVLTLILAALFGLVYLLIFPQSVVVLLLLVFCICFLVACVLYLHITRVQCFPGCLTIQIRTVLCIFIVVLIYSVAQGCVVGCLPWAWSSKPNSSLVVLSSGGQRTALPTLPCESTHHALLCCLVGTLPLAIFFRVSSLPKMILLSGLTTSYILVLELSGYTRTGGGAVSGRSYEPIVAILLFSCALALHARQVDIRLRLDYLWAAQAEEEREDMEKVKLDNRRILFNLLPAHVAQHFLMSNPRNMDLYYQSYSQVGVMFASIPNFNDFYIELDGNNMGVECLRLLNEIIADFDELMEKDFYKDIEKIKTIGSTYMAAVGLAPTSGTKAKKSISSHLSTLADFAIEMFDVLDEINYQSYNDFVLRVGINVGPVVAGVIGARRPQYDIWGNTVNVASRMDSTGVQGRIQVTEEVHRLLRRCPYHFVCRGKVSVKGKGEMLTYFLEGRTDGNGSQIRSLGLDRKMCPFGRAGLQGRRPPVCPMPGVSVRAGLPPHSPGQYLPSAAAGKEA
345	P35611	>sp|P35611|ADDA_HUMAN Alpha-adducin GN=ADD1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MNGDSRAAVVTSPPPTTAPHKERYFDRVDENNPEYLRERNMAPDLRQDFNMMEQKKRVSMILQSPAFCEELESMIQEQFKKGKNPTGLLALQQIADFMTTNVPNVYPAAPQGGMAALNMSLGMVTPVNDLRGSDSIAYDKGEKLLRCKLAAFYRLADLFGWSQLIYNHITTRVNSEQEHFLIVPFGLLYSEVTASSLVKINLQGDIVDRGSTNLGVNQAGFTLHSAIYAARPDVKCVVHIHTPAGAAVSAMKCGLLPISPEALSLGEVAYHDYHGILVDEEEKVLIQKNLGPKSKVLILRNHGLVSVGESVEEAFYYIHNLVVACEIQVRTLASAGGPDNLVLLNPEKYKAKSRSPGSPVGEGTGSPPKWQIGEQEFEALMRMLDNLGYRTGYPYRYPALREKSKKYSDVEVPASVTGYSFASDGDSGTCSPLRHSFQKQQREKTRWLNSGRGDEASEEGQNGSSPKSKTKWTKEDGHRTSTSAVPNLFVPLNTNPKEVQEMRNKIREQNLQDIKTAGPQSQVLCGVVMDRSLVQGELVTASKAIIEKEYQPHVIVSTTGPNPFTTLTDRELEEYRREVERKQKGSEENLDEAREQKEKSPPDQPAVPHPPPSTPIKLEEDLVPEPTTGDDSDAATFKPTLPDLSPDEPSEALGFPMLEKEEEAHRPPSPTEAPTEASPEPAPDPAPVAEEAAPSAVEEGAAADPGSDGSPGKSPSKKKKKFRTPSFLKKSKKKSDS
346	Q8N7X0	>sp|Q8N7X0|ADGB_HUMAN Androglobin GN=ADGB PE=2 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MASKQTKKKEVHRINSAHGSDKSKDFYPFGSNVQSGSTEQKKGKFPLWPEWSEADINSEKWDAGKGAKEKDKTGKSPVFHFFEDPEGKIELPPSLKIYSWKRPQDILFSQTPVVVKNEITFDLFSANEHLLCSELMRWIISEIYAVWKIFNGGILSNYFKGTSGEPPLLPWKPWEHIYSLCKAVKGHMPLFNSYGKYVVKLYWMGCWRKITIDDFLPFDEDNNLLLPATTYEFELWPMLLSKAIIKLANIDIHVADRRELGEFTVIHALTGWLPEVISLHPGYMDKVWELLKEILPEFKLSDEASSESKIAVLDSKLKEPGKEGKEGKEIKDGKEVKDVKEFKPESSLTTLKAPEKSDKVPKEKADARDIGKKRSKDGEKEKFKFSLHGSRPSSEVQYSVQSLSDCSSAIQTSHMVVYATFTPLYLFENKIFSLEKMADSAEKLREYGLSHICSHPVLVTRSRSCPLVAPPKPPPLPPWKLIRQKKETVITDEAQELIVKKPERFLEISSPFLNYRMTPFTIPTEMHFVRSLIKKGIPPGSDLPSVSETDETATHSQTDLSQITKATSQGNTASQVILGKGTDEQTDFGLGDAHQSDGLNLEREIVSQTTATQEKSQEELPTTNNSVSKEIWLDFEDFCVCFQNIYIFHKPSSYCLNFQKSEFKFSEERVSYYLFVDSLKPIELLVCFSALVRWGEYGALTKDSPPIEPGLLTAETFSWKSLKPGSLVLKIHTYATKATVVRLPVGRHMLLFNAYSPVGHSIHICSMVSFVIGDEHVVLPNFEPESCRFTEQSLLIMKAIGNVIANFKDKGKLSAALKDLQTAHYPVPFHDKELTAQHFRVFHLSLWRLMKKVQITKPPPNFKFAFRAMVLDLELLNSSLEEVSLVEWLDVKYCMPTSDKEYSAEEVAAAIKIQAMWRGTYVRLLMKARIPDTKENISVADTLQKVWAVLEMNLEQYAVSLLRLMFKSKCKSLESYPCYQDEETKIAFADYTVTYQEQPPNSWFIVFRETFLVHQDMILVPKVYTTLPICILHIVNNDTMEQVPKVFQKVVPYLYTKNKKGYTFVAEAFTGDTYVAASRWKLRLIGSSAPLPCLSRDSPCNSFAIKEIRDYYIPNDKKILFRYSVKVLTPQPATIQVRTSKPDAFIKLQVLENEETMVSSTGKGQAIIPAFHFLKSEKGLSSQSSKHILSFHSASKKEQEVYVKKKAAQGIQKSPKGRAVSAIQDIGLPLVEEETTSTPTREDSSSTPLQNYKYIIQCSVLYNSWPLTESQLTFVQALKDLKKSNTKAYGERHEELINLGSPDSHTISEGQKSSVTSKTTRKGKEKSSEKEKTAKEKQAPRFEPQISTVHPQQEDPNKPYWILRLVTEHNESELFEVKKDTERADEIRAMKQAWETTEPGRAIKASQARLHYLSGFIKKTSDAESPPISESQTKPKEEVETAARGVKEPNSKNSAGSESKEMTQTGSGSAVWKKWQLTKGLRDVAKSTSSESGGVSSPGKEEREQSTRKENIQTGPRTRSPTILETSPRLIRKALEFMDLSQYVRKTDTDPLLQTDELNQQQAMQKAEEIHQFRQHRTRVLSIRNIDQEERLKLKDEVLDMYKEMQDSLDEARQKIFDIREEYRNKLLEAEHLKLETLAAQEAAMKLETEKMTPAPDTQKKKKGKKK
347	Q6IQ32	>sp|Q6IQ32|ADNP2_HUMAN ADNP homeobox protein 2 GN=ADNP2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MFQIPVENLDNIRKVRKKVKGILVDIGLDSCKELLKDLKGFDPGEKYFHNTSWGDVSLWEPSGKKVRYRTKPYCCGLCKYSTKVLTSFKNHLHRYHEDEIDQELVIPCPNCVFASQPKVVGRHFRMFHAPVRKVQNYTVNILGETKSSRSDVISFTCLKCNFSNTLYYSMKKHVLVAHFHYLINSYFGLRTEEMGEQPKTNDTVSIEKIPPPDKYYCKKCNANASSQDALMYHILTSDIHRDLENKLRSVISEHIKRTGLLKQTHIAPKPAAHLAAPANGSAPSAPAQPPCFHLALPQNSPSPAAGQPVTVAQGAPGSLTHSPPAAGQSHMTLVSSPLPVGQNSLTLQPPAPQPVFLSHGVPLHQSVNPPVLPLSQPVGPVNKSVGTSVLPINQTVRPGVLPLTQPVGPINRPVGPGVLPVSPSVTPGVLQAVSPGVLSVSRAVPSGVLPAGQMTPAGQMTPAGVIPGQTATSGVLPTGQMVQSGVLPVGQTAPSRVLPPGQTAPLRVISAGQVVPSGLLSPNQTVSSSAVVPVNQGVNSGVLQLSQPVVSGVLPVGQPVRPGVLQLNQTVGTNILPVNQPVRPGASQNTTFLTSGSILRQLIPTGKQVNGIPTYTLAPVSVTLPVPPGGLATVAPPQMPIQLLPSGAAAPMAGSMPGMPSPPVLVNAAQSVFVQASSSAADTNQVLKQAKQWKTCPVCNELFPSNVYQVHMEVAHKHSESKSGEKLEPEKLAACAPFLKWMREKTVRCLSCKCLVSEEELIHHLLMHGLGCLFCPCTFHDIKGLSEHSRNRHLGKKKLPMDYSNRGFQLDVDANGNLLFPHLDFITILPKEKLGEREVYLAILAGIHSKSLVPVYVKVRPQAEGTPGSTGKRVSTCPFCFGPFVTTEAYELHLKERHHIMPTVHTVLKSPAFKCIHCCGVYTGNMTLAAIAVHLVRCRSAPKDSSSDLQAQPGFIHNSELLLVSGEVMHDSSFSVKRKLPDGHLGAEDQRHGEEQPPILNADAAPGPEKVTSVVPFKRQRNESRTEGPIVKDEALQILALDPKKYEGRSYEEKKQFLKDYFHKKPYPSKKEIELLSSLFWVWKIDVASFFGKRRYICMKAIKNHKPSVLLGFDMSELKNVKHRLNFEYEP
372	P17174	>sp|P17174|AATC_HUMAN Aspartate aminotransferase, cytoplasmic GN=GOT1 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MAPPSVFAEVPQAQPVLVFKLTADFREDPDPRKVNLGVGAYRTDDCHPWVLPVVKKVEQKIANDNSLNHEYLPILGLAEFRSCASRLALGDDSPALKEKRVGGVQSLGGTGALRIGADFLARWYNGTNNKNTPVYVSSPTWENHNAVFSAAGFKDIRSYRYWDAEKRGLDLQGFLNDLENAPEFSIVVLHACAHNPTGIDPTPEQWKQIASVMKHRFLFPFFDSAYQGFASGNLERDAWAIRYFVSEGFEFFCAQSFSKNFGLYNERVGNLTVVGKEPESILQVLSQMEKIVRITWSNPPAQGARIVASTLSNPELFEEWTGNVKTMADRILTMRSELRARLEALKTPGTWNHITDQIGMFSFTGLNPKQVEYLVNEKHIYLLPSGRINVSGLTTKNLDYVATSIHEAVTKIQ
348	Q9BRR6	>sp|Q9BRR6|ADPGK_HUMAN ADP-dependent glucokinase GN=ADPGK PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MALWRGSAYAGFLALAVGCVFLLEPELPGSALRSLWSSLCLGPAPAPPGPVSPEGRLAAAWDALIVRPVRRWRRVAVGVNACVDVVLSGVKLLQALGLSPGNGKDHSILHSRNDLEEAFIHFMGKGAAAERFFSDKETFHDIAQVASEFPGAQHYVGGNAALIGQKFAANSDLKVLLCGPVGPKLHELLDDNVFVPPESLQEVDEFHLILEYQAGEEWGQLKAPHANRFIFSHDLSNGAMNMLEVFVSSLEEFQPDLVVLSGLHMMEGQSKELQRKRLLEVVTSISDIPTGIPVHLELASMTNRELMSSIVHQQVFPAVTSLGLNEQELLFLTQSASGPHSSLSSWNGVPDVGMVSDILFWILKEHGRSKSRASDLTRIHFHTLVYHILATVDGHWANQLAAVAAGARVAGTQACATETIDTSRVSLRAPQEFMTSHSEAGSRIVLNPNKPVVEWHREGISFHFTPVLVCKDPIRTVGLGDAISAEGLFYSEVHPHY
349	Q96A54	>sp|Q96A54|ADR1_HUMAN Adiponectin receptor protein 1 GN=ADIPOR1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MSSHKGSVVAQGNGAPASNREADTVELAELGPLLEEKGKRVIANPPKAEEEQTCPVPQEEEEEVRVLTLPLQAHHAMEKMEEFVYKVWEGRWRVIPYDVLPDWLKDNDYLLHGHRPPMPSFRACFKSIFRIHTETGNIWTHLLGFVLFLFLGILTMLRPNMYFMAPLQEKVVFGMFFLGAVLCLSFSWLFHTVYCHSEKVSRTFSKLDYSGIALLIMGSFVPWLYYSFYCSPQPRLIYLSIVCVLGISAIIVAQWDRFATPKHRQTRAGVFLGLGLSGVVPTMHFTIAEGFVKATTVGQMGWFFLMAVMYITGAGLYAARIPERFFPGKFDIWFQSHQIFHVLVVAAAFVHFYGVSNLQEFRYGLEGGCTDDTLL
350	Q6UXC1	>sp|Q6UXC1|AEGP_HUMAN Apical endosomal glycoprotein GN=MAMDC4 PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MPLSSHLLPALVLFLAGSSGWAWVPNHCRSPGQAVCNFVCDCRDCSDEAQCGYHGASPTLGAPFACDFEQDPCGWRDISTSGYSWLRDRAGAALEGPGPHSDHTLGTDLGWYMAVGTHRGKEASTAALRSPTLREAASSCKLRLWYHAASGDVAELRVELTHGAETLTLWQSTGPWGPGWQELAVTTGRIRGDFRVTFSATRNATHRGAVALDDLEFWDCGLPTPQANCPPGHHHCQNKVCVEPQQLCDGEDNCGDLSDENPLTCGRHIATDFETGLGPWNRSEGWSRNHRAGGPERPSWPRRDHSRNSAQGSFLVSVAEPGTPAILSSPEFQASGTSNCSLVFYQYLSGSEAGCLQLFLQTLGPGAPRAPVLLRRRRGELGTAWVRDRVDIQSAYPFQILLAGQTGPGGVVGLDDLILSDHCRPVSEVSTLQPLPPGPRAPAPQPLPPSSRLQDSCKQGHLACGDLCVPPEQLCDFEEQCAGGEDEQACGTTDFESPEAGGWEDASVGRLQWRRVSAQESQGSSAAAAGHFLSLQRAWGQLGAEARVLTPLLGPSGPSCELHLAYYLQSQPRGFLALVVVDNGSRELAWQALSSSAGIWKVDKVLLGARRRPFRLEFVGLVDLDGPDQQGAGVDNVTLRDCSPTVTTERDREVSCNFERDTCSWYPGHLSDTHWRWVESRGPDHDHTTGQGHFVLLDPTDPLAWGHSAHLLSRPQVPAAPTECLSFWYHLHGPQIGTLRLAMRREGEETHLWSRSGTQGNRWHEAWATLSHQPGSHAQYQLLFEGLRDGYHGTMALDDVAVRPGPCWAPNYCSFEDSDCGFSPGGQGLWRRQANASGHAAWGPPTDHTTETAQGHYMVVDTSPDALPRGQTASLTSKEHRPLAQPACLTFWYHGSLRSPGTLRVYLEERGRHQVLSLSAHGGLAWRLGSMDVQAERAWRVVFEAVAAGVAHSYVALDDLLLQDGPCPQPGSCDFESGLCGWSHLAWPGLGGYSWDWGGGATPSRYPQPPVDHTLGTEAGHFAFFETGVLGPGGRAAWLRSEPLPATPASCLRFWYHMGFPEHFYKGELKVLLHSAQGQLAVWGAGGHRRHQWLEAQVEVASAKEFQIVFEATLGGQPALGPIALDDVEYLAGQHCQQPAPSPGNTAAPGSVPAVVGSALLLLMLLVLLGLGGRRWLQKKGSCPFQSNTEATAPGFDNILFNADGVTLPASVTSDP
351	Q8N556	>sp|Q8N556|AFAP1_HUMAN Actin filament-associated protein 1 GN=AFAP1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MEELIVELRLFLELLDHEYLTSTVREKKAVITNILLRIQSSKGFDVKDHAQKQETANSLPAPPQMPLPEIPQPWLPPDSGPPPLPTSSLPEGYYEEAVPLSPGKAPEYITSNYDSDAMSSSYESYDEEEEDGKGKKTRHQWPSEEASMDLVKDAKICAFLLRKKRFGQWTKLLCVIKDTKLLCYKSSKDQQPQMELPLQGCNITYIPKDSKKKKHELKITQQGTDPLVLAVQSKEQAEQWLKVIKEAYSGCSGPVDSECPPPPSSPVHKAELEKKLSSERPSSDGEGVVENGITTCNGKEQVKRKKSSKSEAKGTVSKVTGKKITKIISLGKKKPSTDEQTSSAEEDVPTCGYLNVLSNSRWRERWCRVKDNKLIFHKDRTDLKTHIVSIPLRGCEVIPGLDSKHPLTFRLLRNGQEVAVLEASSSEDMGRWIGILLAETGSSTDPEALHYDYIDVEMSASVIQTAKQTFCFMNRRVISANPYLGGTSNGYAHPSGTALHYDDVPCINGSLKGKKPPVASNGVTGKGKTLSSQPKKADPAAVVKRTGSNAAQYKYGKNRVEADAKRLQTKEEELLKRKEALRNRLAQLRKERKDLRAAIEVNAGRKPQAILEEKLKQLEEECRQKEAERVSLELELTEVKESLKKALAGGVTLGLAIEPKSGTSSPQSPVFRHRTLENSPISSCDTSDTEGPVPVNSAAVLKKSQAAPGSSPCRGHVLRKAKEWELKNGT
352	Q6ULP2	>sp|Q6ULP2|AFTIN_HUMAN Aftiphilin GN=AFTPH PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MEPDIIRMYSSSPPPLDNGAEDDDDDEFGEFGGFSEVSPSGVGFVDFDTPDYTRPKEEFVPSNHFMPIHEFSENVDSLTSFKSIKNGNDKDITAELSAPVKGQSDVLLSTTSKEIISSEMLATSIDGMERPGNLNKVVEQRQNVGTLESFSPGDFRTNMNVVHQNKQLESCNGEKPPCLEILTNGFAVLETVNPQGTDDLDNVADSKGRKPLSTHSTEYNLDSVPSPAEEFADFATFSKKERIQLEEIECAVLNDREALTIRENNKINRVNELNSVKEVALGRSLDNKGDTDGEDQVCVSEISIVTNRGFSVEKQGLPTLQQDEFLQSGVQSKAWSLVDSADNSEAIRREQCKTEEKLDLLTSKCAHLCMDSVKTSDDEVGSPKEESRKFTNFQSPNIDPTEENDLDDSLSVKNGDSSNDFVTCNDINEDDFGDFGDFGSASGSTPPFVTGTQDSMSDATFEESSEHFPHFSEPGDDFGEFGDINAVSCQEETILTKSDLKQTSDNLSEECQLARKSSGTGTEPVAKLKNGQEGEIGHFDSVPNIQDDCNGFQDSDDFADFSSAGPSQVVDWNAFEDEQKDSCSWAAFGDQQATESHHRKEAWQSHRTDENIDTPGTPKTHSVPSATSKGAVASGHLQESATSVQTALLNRLERIFEACFPSILVPDAEEEVTSLKHLLETSTLPIKTREALPESGELLDVWTELQDIHDAHGLRYQWGGSHSNKKLLSSLGIDTRNILFTGNKKQPVIVPMYAAGLGMLEPTKEPLKPLSAAEKIASIGQTATMSPDMNTCTSDQFQESLPPVQFDWSSSGLTNPLDASGGSTLLNLDFFGPVDDSSSSSSTTIPGVDPELYELTTSKLEISTSSLKVTDAFARLMSTVEKTSTSTSRKPKREEHLSEEAIKVIAGLPDLTFMHAKVLMFPATLTPSTSSQEKADG
353	Q5I7T1	>sp|Q5I7T1|AG10B_HUMAN Putative Dol-P-Glc:Glc(2)Man(9)GlcNAc(2)-PP-Dol alpha-1,2-glucosyltransferase GN=ALG10B PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAQLEGYCFSAALSCTFLVSCLLFSAFSRALREPYMDEIFHLPQAQRYCEGHFSLSQWDPMITTLPGLYLVSVGVVKPAIWIFAWSEHVVCSIGMLRFVNLLFSVGNFYLLYLLFHKVQPRNKAASSIQRVLSTLTLAVFPTLYFFNFLYYTEAGSMFFTLFAYLMCLYGNHKTSAFLGFCGFMFRQTNIIWAVFCAGNVIAQKLTEAWKTELQKKEDRLPPIKGPFAEFRKILQFLLAYSMSFKNLSMLFCLTWPYILLGFLFCAFVVVNGGIVIGDRSSHEACLHFPQLFYFFSFTLFFSFPHLLSPSKIKTFLSLVWKHGILFLVVTLVSVFLVWKFTYAHKYLLADNRHYTFYVWKRVFQRYAILKYLLVPAYIFAGWSIADSLKSKPIFWNLMFFICLFIVIVPQKLLEFRYFILPYVIYRLNITLPPTSRLVCELSCYAIVNFITFYIFLNKTFQWPNSQDIQRFMW
354	P31947	>sp|P31947|1433S_HUMAN 14-3-3 protein sigma GN=SFN PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MERASLIQKAKLAEQAERYEDMAAFMKGAVEKGEELSCEERNLLSVAYKNVVGGQRAAWRVLSSIEQKSNEEGSEEKGPEVREYREKVETELQGVCDTVLGLLDSHLIKEAGDAESRVFYLKMKGDYYRYLAEVATGDDKKRIIDSARSAYQEAMDISKKEMPPTNPIRLGLALNFSVFHYEIANSPEEAISLAKTTFDEAMADLHTLSEDSYKDSTLIMQLLRDNLTLWTADNAGEEGGEAPQEPQS
355	P27348	>sp|P27348|1433T_HUMAN 14-3-3 protein theta GN=YWHAQ PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MEKTELIQKAKLAEQAERYDDMATCMKAVTEQGAELSNEERNLLSVAYKNVVGGRRSAWRVISSIEQKTDTSDKKLQLIKDYREKVESELRSICTTVLELLDKYLIANATNPESKVFYLKMKGDYFRYLAEVACGDDRKQTIDNSQGAYQEAFDISKKEMQPTHPIRLGLALNFSVFYYEILNNPELACTLAKTAFDEAIAELDTLNEDSYKDSTLIMQLLRDNLTLWTSDSAGEECDAAEGAEN
356	Q09160	>sp|Q09160|1A80_HUMAN HLA class I histocompatibility antigen, A-80 alpha chain GN=HLA-A PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAVMPPRTLLLLLSGALALTQTWAGSHSMRYFFTSVSRPGRGEPRFIAVGYVDDSQFVQFDSDAASQRMEPRAPWIEQEEPEYWDEETRNVKAHSQTNRANLGTLRGYYNQSEDGSHTIQIMYGCDVGSDGRFLRGYRQDAYDGKDYIALNEDLRSWTAADMAAQITKRKWEAARRAEQLRAYLEGECVDGLRRYLENGKETLQRTDPPKTHMTHHPISDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGKEKRYTCHVQHEGLPEPLTLRWEPSSQPTIPIVGIIAGLVLLGAVIAGAVVAAVMWRKKSSVRKGGSYSQAASSDSAQGSDVSLTACKV
357	Q15173	>sp|Q15173|2A5B_HUMAN Serine/threonine-protein phosphatase 2A 56 kDa regulatory subunit beta isoform GN=PPP2R5B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	METKLPPASTPTSPSSPGLSPVPPPDKVDGFSRRSLRRARPRRSHSSSQFRYQSNQQELTPLPLLKDVPASELHELLSRKLAQCGVMFDFLDCVADLKGKEVKRAALNELVECVGSTRGVLIEPVYPDIIRMISVNIFRTLPPSENPEFDPEEDEPNLEPSWPHLQLVYEFFLRFLESPDFQPSVAKRYVDQKFVLMLLELFDSEDPREREYLKTILHRVYGKFLGLRAYIRKQCNHIFLRFIYEFEHFNGVAELLEILGSIINGFALPLKTEHKQFLVRVLIPLHSVKSLSVFHAQLAYCVVQFLEKDATLTEHVIRGLLKYWPKTCTQKEVMFLGEMEEILDVIEPSQFVKIQEPLFKQVARCVSSPHFQVAERALYFWNNEYILSLIEDNCHTVLPAVFGTLYQVSKEHWNQTIVSLIYNVLKTFMEMNGKLFDELTASYKLEKQQEQQKAQERQELWQGLEELRLRRLQGTQGAKEAPLQRLTPQVAASGGQS
358	Q14738	>sp|Q14738|2A5D_HUMAN Serine/threonine-protein phosphatase 2A 56 kDa regulatory subunit delta isoform GN=PPP2R5D PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MPYKLKKEKEPPKVAKCTAKPSSSGKDGGGENTEEAQPQPQPQPQPQAQSQPPSSNKRPSNSTPPPTQLSKIKYSGGPQIVKKERRQSSSRFNLSKNRELQKLPALKDSPTQEREELFIQKLRQCCVLFDFVSDPLSDLKFKEVKRAGLNEMVEYITHSRDVVTEAIYPEAVTMFSVNLFRTLPPSSNPTGAEFDPEEDEPTLEAAWPHLQLVYEFFLRFLESPDFQPNIAKKYIDQKFVLALLDLFDSEDPRERDFLKTILHRIYGKFLGLRAYIRRQINHIFYRFIYETEHHNGIAELLEILGSIINGFALPLKEEHKMFLIRVLLPLHKVKSLSVYHPQLAYCVVQFLEKESSLTEPVIVGLLKFWPKTHSPKEVMFLNELEEILDVIEPSEFSKVMEPLFRQLAKCVSSPHFQVAERALYYWNNEYIMSLISDNAARVLPIMFPALYRNSKSHWNKTIHGLIYNALKLFMEMNQKLFDDCTQQYKAEKQKGRFRMKEREEMWQKIEELARLNPQYPMFRAPPPLPPVYSMETETPTAEDIQLLKRTVETEAVQMLKDIKKEKVLLRRKSELPQDVYTIKALEAHKRAEEFLTASQEAL
359	P30154	>sp|P30154|2AAB_HUMAN Serine/threonine-protein phosphatase 2A 65 kDa regulatory subunit A beta isoform GN=PPP2R1B PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MAGASELGTGPGAAGGDGDDSLYPIAVLIDELRNEDVQLRLNSIKKLSTIALALGVERTRSELLPFLTDTIYDEDEVLLALAEQLGNFTGLVGGPDFAHCLLPPLENLATVEETVVRDKAVESLRQISQEHTPVALEAYFVPLVKRLASGDWFTSRTSACGLFSVCYPRASNAVKAEIRQQFRSLCSDDTPMVRRAAASKLGEFAKVLELDSVKSEIVPLFTSLASDEQDSVRLLAVEACVSIAQLLSQDDLETLVMPTLRQAAEDKSWRVRYMVADRFSELQKAMGPKITLNDLIPAFQNLLKDCEAEVRAAAAHKVKELGENLPIEDRETIIMNQILPYIKELVSDTNQHVKSALASVIMGLSTILGKENTIEHLLPLFLAQLKDECPDVRLNIISNLDCVNEVIGIRQLSQSLLPAIVELAEDAKWRVRLAIIEYMPLLAGQLGVEFFDEKLNSLCMAWLVDHVYAIREAATNNLMKLVQKFGTEWAQNTIVPKVLVMANDPNYLHRMTTLFCINALSEACGQEITTKQMLPIVLKMAGDQVANVRFNVAKSLQKIGPILDTNALQGEVKPVLQKLGQDEDMDVKYFAQEAISVLALA
360	P63151	>sp|P63151|2ABA_HUMAN Serine/threonine-protein phosphatase 2A 55 kDa regulatory subunit B alpha isoform GN=PPP2R2A PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAGAGGGNDIQWCFSQVKGAVDDDVAEADIISTVEFNHSGELLATGDKGGRVVIFQQEQENKIQSHSRGEYNVYSTFQSHEPEFDYLKSLEIEEKINKIRWLPQKNAAQFLLSTNDKTIKLWKISERDKRPEGYNLKEEDGRYRDPTTVTTLRVPVFRPMDLMVEASPRRIFANAHTYHINSISINSDYETYLSADDLRINLWHLEITDRSFNIVDIKPANMEELTEVITAAEFHPNSCNTFVYSSSKGTIRLCDMRASALCDRHSKLFEEPEDPSNRSFFSEIISSISDVKFSHSGRYMMTRDYLSVKIWDLNMENRPVETYQVHEYLRSKLCSLYENDCIFDKFECCWNGSDSVVMTGSYNNFFRMFDRNTKRDITLEASRENNKPRTVLKPRKVCASGKRKKDEISVDSLDFNKKILHTAWHPKENIIAVATTNNLYIFQDKVN
361	P01912	>sp|P01912|2B13_HUMAN HLA class II histocompatibility antigen, DRB1-3 chain GN=HLA-DRB1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MVCLRLPGGSCMAVLTVTLMVLSSPLALAGDTRPRFLEYSTSECHFFNGTERVRYLDRYFHNQEENVRFDSDVGEFRAVTELGRPDAEYWNSQKDLLEQKRGRVDNYCRHNYGVVESFTVQRRVHPKVTVYPSKTQPLQHHNLLVCSVSGFYPGSIEVRWFRNGQEEKTGVVSTGLIHNGDWTFQTLVMLETVPRSGEVYTCQVEHPSVTSPLTVEWRARSESAQSKMLSGVGGFVLGLLFLGAGLFIYFRNQKGHSGLQPRGFLS
362	P13761	>sp|P13761|2B17_HUMAN HLA class II histocompatibility antigen, DRB1-7 beta chain GN=HLA-DRB1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MVCLKLPGGSCMAALTVTLMVLSSPLALAGDTQPRFLWQGKYKCHFFNGTERVQFLERLFYNQEEFVRFDSDVGEYRAVTELGRPVAESWNSQKDILEDRRGQVDTVCRHNYGVGESFTVQRRVHPEVTVYPAKTQPLQHHNLLVCSVSGFYPGSIEVRWFRNGQEEKAGVVSTGLIQNGDWTFQTLVMLETVPRSGEVYTCQVEHPSVMSPLTVEWRARSESAQSKMLSGVGGFVLGLLFLGAGLFIYFRNQKGHSGLQPTGFLS
363	Q95IE3	>sp|Q95IE3|2B1C_HUMAN HLA class II histocompatibility antigen, DRB1-12 beta chain GN=HLA-DRB1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MVCLRLPGGSCMAVLTVTLMVLSSPLALAGDTRPRFLEYSTGECYFFNGTERVRLLERHFHNQEELLRFDSDVGEFRAVTELGRPVAESWNSQKDILEDRRAAVDTYCRHNYGAVESFTVQRRVHPKVTVYPSKTQPLQHHNLLVCSVSGFYPGSIEVRWFRNGQEEKTGVVSTGLIHNGDWTFQTLVMLETVPRSGEVYTCQVEHPSVTSPLTVEWRARSESAQSKMLSGVGGFVLGLLFLGAGLFIYFRNQKGHSGLQPRGFLS
364	Q9GIY3	>sp|Q9GIY3|2B1E_HUMAN HLA class II histocompatibility antigen, DRB1-14 beta chain GN=HLA-DRB1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MVCLRLPGGSCMAVLTVTLMVLSSPLALAGDTRPRFLEYSTSECHFFNGTERVRFLDRYFHNQEEFVRFDSDVGEYRAVTELGRPAAEHWNSQKDLLERRRAEVDTYCRHNYGVVESFTVQRRVHPKVTVYPSKTQPLQHYNLLVCSVSGFYPGSIEVRWFRNGQEEKTGVVSTGLIHNGDWTFQTLVMLETVPRSGEVYTCQVEHPSVTSPLTVEWRARSESAQSKMLSGVGGFVLGLLFLGAGLFIYFRNQKGHSGLQPRGFLS
365	Q8IZ83	>sp|Q8IZ83|A16A1_HUMAN Aldehyde dehydrogenase family 16 member A1 GN=ALDH16A1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAATRAGPRAREIFTSLEYGPVPESHACALAWLDTQDRCLGHYVNGKWLKPEHRNSVPCQDPITGENLASCLQAQAEDVAAAVEAARMAFKGWSAHPGVVRAQHLTRLAEVIQKHQRLLWTLESLVTGRAVREVRDGDVQLAQQLLHYHAIQASTQEEALAGWEPMGVIGLILPPTFSFLEMMWRICPALAVGCTVVALVPPASPAPLLLAQLAGELGPFPGILNVLSGPASLVPILASQPGIRKVAFCGAPEEGRALRRSLAGECAELGLALGTESLLLLTDTADVDSAVEGVVDAAWSDRGPGGLRLLIQESVWDEAMRRLQERMGRLRSGRGLDGAVDMGARGAAACDLVQRFVREAQSQGAQVFQAGDVPSERPFYPPTLVSNLPPASPCAQVEVPWPVVVASPFRTAKEALLVANGTPRGGSASVWSERLGQALELGYGLQVGTVWINAHGLRDPSVPTGGCKESGCSWHGGPDGLYEYLRPSGTPARLSCLSKNLNYDTFGLAVPSTLPAGPEIGPSPAPPYGLFVGGRFQAPGARSSRPIRDSSGNLHGYVAEGGAKDIRGAVEAAHQAFPGWAGQSPGARAALLWALAAALERRKSTLASRLERQGAELKAAEAEVELSARRLRAWGARVQAQGHTLQVAGLRGPVLRLREPLGVLAVVCPDEWPLLAFVSLLAPALAYGNTVVMVPSAACPLLALEVCQDMATVFPAGLANVVTGDRDHLTRCLALHQDVQAMWYFGSAQGSQFVEWASAGNLKPVWASRGCPRAWDQEAEGAGPELGLRVARTKALWLPMGD
366	P02750	>sp|P02750|A2GL_HUMAN Leucine-rich alpha-2-glycoprotein GN=LRG1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MSSWSRQRPKSPGGIQPHVSRTLFLLLLLAASAWGVTLSPKDCQVFRSDHGSSISCQPPAEIPGYLPADTVHLAVEFFNLTHLPANLLQGASKLQELHLSSNGLESLSPEFLRPVPQLRVLDLTRNALTGLPPGLFQASATLDTLVLKENQLEVLEVSWLHGLKALGHLDLSGNRLRKLPPGLLANFTLLRTLDLGENQLETLPPDLLRGPLQLERLHLEGNKLQVLGKDLLLPQPDLRYLFLNGNKLARVAAGAFQGLRQLDMLDLSNNSLASVPEGLWASLGQPNWDMRDGFDISGNPWICDQNLSDLYRWLQAQKDKMFSQNDTRCAGPEAVKGQTLLAVAKSQ
367	A8K2U0	>sp|A8K2U0|A2ML1_HUMAN Alpha-2-macroglobulin-like protein 1 GN=A2ML1 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MWAQLLLGMLALSPAIAEELPNYLVTLPARLNFPSVQKVCLDLSPGYSDVKFTVTLETKDKTQKLLEYSGLKKRHLHCISFLVPPPAGGTEEVATIRVSGVGNNISFEEKKKVLIQRQGNGTFVQTDKPLYTPGQQVYFRIVTMDSNFVPVNDKYSMVELQDPNSNRIAQWLEVVPEQGIVDLSFQLAPEAMLGTYTVAVAEGKTFGTFSVEEYVLPKFKVEVVEPKELSTVQESFLVKICCRYTYGKPMLGAVQVSVCQKANTYWYREVEREQLPDKCRNLSGQTDKTGCFSAPVDMATFDLIGYAYSHQINIVATVVEEGTGVEANATQNIYISPQMGSMTFEDTSNFYHPNFPFSGKIRVRGHDDSFLKNHLVFLVIYGTNGTFNQTLVTDNNGLAPFTLETSGWNGTDVSLEGKFQMEDLVYNPEQVPRYYQNAYLHLRPFYSTTRSFLGIHRLNGPLKCGQPQEVLVDYYIDPADASPDQEISFSYYLIGKGSLVMEGQKHLNSKKKGLKASFSLSLTFTSRLAPDPSLVIYAIFPSGGVVADKIQFSVEMCFDNQVSLGFSPSQQLPGAEVELQLQAAPGSLCALRAVDESVLLLRPDRELSNRSVYGMFPFWYGHYPYQVAEYDQCPVSGPWDFPQPLIDPMPQGHSSQRSIIWRPSFSEGTDLFSFFRDVGLKILSNAKIKKPVDCSHRSPEYSTAMGAGGGHPEAFESSTPLHQAEDSQVRQYFPETWLWDLFPIGNSGKEAVHVTVPDAITEWKAMSFCTSQSRGFGLSPTVGLTAFKPFFVDLTLPYSVVRGESFRLTATIFNYLKDCIRVQTDLAKSHEYQLESWADSQTSSCLCADDAKTHHWNITAVKLGHINFTISTKILDSNEPCGGQKGFVPQKGRSDTLIKPVLVKPEGVLVEKTHSSLLCPKGKVASESVSLELPVDIVPDSTKAYVTVLGDIMGTALQNLDGLVQMPSGCGEQNMVLFAPIIYVLQYLEKAGLLTEEIRSRAVGFLEIGYQKELMYKHSNGSYSAFGERDGNGNTWLTAFVTKCFGQAQKFIFIDPKNIQDALKWMAGNQLPSGCYANVGNLLHTAMKGGVDDEVSLTAYVTAALLEMGKDVDDPMVSQGLRCLKNSATSTTNLYTQALLAYIFSLAGEMDIRNILLKQLDQQAIISGESIYWSQKPTPSSNASPWSEPAAVDVELTAYALLAQLTKPSLTQKEIAKATSIVAWLAKQHNAYGGFSSTQDTVVALQALAKYATTAYMPSEEINLVVKSTENFQRTFNIQSVNRLVFQQDTLPNVPGMYTLEASGQGCVYVQTVLRYNILPPTNMKTFSLSVEIGKARCEQPTSPRSLTLTIHTSYVGSRSSSNMAIVEVKMLSGFSPMEGTNQLLLQQPLVKKVEFGTDTLNIYLDELIKNTQTYTFTISQSVLVTNLKPATIKVYDYYLPDEQATIQYSDPCE
368	P01011	>sp|P01011|AACT_HUMAN Alpha-1-antichymotrypsin GN=SERPINA3 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MERMLPLLALGLLAAGFCPAVLCHPNSPLDEENLTQENQDRGTHVDLGLASANVDFAFSLYKQLVLKAPDKNVIFSPLSISTALAFLSLGAHNTTLTEILKGLKFNLTETSEAEIHQSFQHLLRTLNQSSDELQLSMGNAMFVKEQLSLLDRFTEDAKRLYGSEAFATDFQDSAAAKKLINDYVKNGTRGKITDLIKDLDSQTMMVLVNYIFFKAKWEMPFDPQDTHQSRFYLSKKKWVMVPMMSLHHLTIPYFRDEELSCTVVELKYTGNASALFILPDQDKMEEVEAMLLPETLKRWRDSLEFREIGELYLPKFSISRDYNLNDILLQLGIEEAFTSKADLSGITGARNLAVSQVVHKAVLDVFEEGTEASAATAVKITLLSALVETRTIVRFNRPFLMIIVPTDTQNIFFMSKVTNPKQA
369	Q13131	>sp|Q13131|AAPK1_HUMAN 5'-AMP-activated protein kinase catalytic subunit alpha-1 GN=PRKAA1 PE=1 SV=4 Homo sapiens OS=Human NCBI_TaxID=9606	MRRLSSWRKMATAEKQKHDGRVKIGHYILGDTLGVGTFGKVKVGKHELTGHKVAVKILNRQKIRSLDVVGKIRREIQNLKLFRHPHIIKLYQVISTPSDIFMVMEYVSGGELFDYICKNGRLDEKESRRLFQQILSGVDYCHRHMVVHRDLKPENVLLDAHMNAKIADFGLSNMMSDGEFLRTSCGSPNYAAPEVISGRLYAGPEVDIWSSGVILYALLCGTLPFDDDHVPTLFKKICDGIFYTPQYLNPSVISLLKHMLQVDPMKRATIKDIREHEWFKQDLPKYLFPEDPSYSSTMIDDEALKEVCEKFECSEEEVLSCLYNRNHQDPLAVAYHLIIDNRRIMNEAKDFYLATSPPDSFLDDHHLTRPHPERVPFLVAETPRARHTLDELNPQKSKHQGVRKAKWHLGIRSQSRPNDIMAEVCRAIKQLDYEWKVVNPYYLRVRRKNPVTSTYSKMSLQLYQVDSRTYLLDFRSIDDEITEAKSGTATPQRSGSVSNYRSCQRSDSDAEAQGKSSEVSLTSSVTSLDSSPVDLTPRPGSHTIEFFEMCANLIKILAQ
370	Q4LEZ3	>sp|Q4LEZ3|AARD_HUMAN Alanine and arginine-rich domain-containing protein GN=AARD PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MGPGDFRRCRERISQGLQGLPGRAELWFPPRPACDFFGDGRSTDIQEEALAASPLLEDLRRRLTRAFQWAVQRAISRRVQEAAAAAAAREEQSWTGVEATLARLRAELVEMHFQNHQLARTLLDLNMKVQQLKKEYELEITSDSQSPKDDAANPE
373	Q9NP78	>sp|Q9NP78|ABCB9_HUMAN ATP-binding cassette sub-family B member 9 GN=ABCB9 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRLWKAVVVTLAFMSVDICVTTAIYVFSHLDRSLLEDIRHFNIFDSVLDLWAACLYRSCLLLGATIGVAKNSALGPRRLRASWLVITLVCLFVGIYAMVKLLLFSEVRRPIRDPWFWALFVWTYISLGASFLLWWLLSTVRPGTQALEPGAATEAEGFPGSGRPPPEQASGATLQKLLSYTKPDVAFLVAASFFLIVAALGETFLPYYTGRAIDGIVIQKSMDQFSTAVVIVCLLAIGSSFAAGIRGGIFTLIFARLNIRLRNCLFRSLVSQETSFFDENRTGDLISRLTSDTTMVSDLVSQNINVFLRNTVKVTGVVVFMFSLSWQLSLVTFMGFPIIMMVSNIYGKYYKRLSKEVQNALARASNTAEETISAMKTVRSFANEEEEAEVYLRKLQQVYKLNRKEAAAYMYYVWGSGLTLLVVQVSILYYGGHLVISGQMTSGNLIAFIIYEFVLGDCMESVGSVYSGLMQGVGAAEKVFEFIDRQPTMVHDGSLAPDHLEGRVDFENVTFTYRTRPHTQVLQNVSFSLSPGKVTALVGPSGSGKSSCVNILENFYPLEGGRVLLDGKPISAYDHKYLHRVISLVSQEPVLFARSITDNISYGLPTVPFEMVVEAAQKANAHGFIMELQDGYSTETGEKGAQLSGGQKQRVAMARALVRNPPVLILDEATSALDAESEYLIQQAIHGNLQKHTVLIIAHRLSTVEHAHLIVVLDKGRVVQQGTHQQLLAQGGLYAKLVQRQMLGLQPAADFTAGHNEPVANGSHKA
374	O95342	>sp|O95342|ABCBB_HUMAN Bile salt export pump GN=ABCB11 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MSDSVILRSIKKFGEENDGFESDKSYNNDKKSRLQDEKKGDGVRVGFFQLFRFSSSTDIWLMFVGSLCAFLHGIAQPGVLLIFGTMTDVFIDYDVELQELQIPGKACVNNTIVWTNSSLNQNMTNGTRCGLLNIESEMIKFASYYAGIAVAVLITGYIQICFWVIAAARQIQKMRKFYFRRIMRMEIGWFDCNSVGELNTRFSDDINKINDAIADQMALFIQRMTSTICGFLLGFFRGWKLTLVIISVSPLIGIGAATIGLSVSKFTDYELKAYAKAGVVADEVISSMRTVAAFGGEKREVERYEKNLVFAQRWGIRKGIVMGFFTGFVWCLIFLCYALAFWYGSTLVLDEGEYTPGTLVQIFLSVIVGALNLGNASPCLEAFATGRAAATSIFETIDRKPIIDCMSEDGYKLDRIKGEIEFHNVTFHYPSRPEVKILNDLNMVIKPGEMTALVGPSGAGKSTALQLIQRFYDPCEGMVTVDGHDIRSLNIQWLRDQIGIVEQEPVLFSTTIAENIRYGREDATMEDIVQAAKEANAYNFIMDLPQQFDTLVGEGGGQMSGGQKQRVAIARALIRNPKILLLDMATSALDNESEAMVQEVLSKIQHGHTIISVAHRLSTVRAADTIIGFEHGTAVERGTHEELLERKGVYFTLVTLQSQGNQALNEEDIKDATEDDMLARTFSRGSYQDSLRASIRQRSKSQLSYLVHEPPLAVVDHKSTYEEDRKDKDIPVQEEVEPAPVRRILKFSAPEWPYMLVGSVGAAVNGTVTPLYAFLFSQILGTFSIPDKEEQRSQINGVCLLFVAMGCVSLFTQFLQGYAFAKSGELLTKRLRKFGFRAMLGQDIAWFDDLRNSPGALTTRLATDASQVQGAAGSQIGMIVNSFTNVTVAMIIAFSFSWKLSLVILCFFPFLALSGATQTRMLTGFASRDKQALEMVGQITNEALSNIRTVAGIGKERRFIEALETELEKPFKTAIQKANIYGFCFAFAQCIMFIANSASYRYGGYLISNEGLHFSYVFRVISAVVLSATALGRAFSYTPSYAKAKISAARFFQLLDRQPPISVYNTAGEKWDNFQGKIDFVDCKFTYPSRPDSQVLNGLSVSISPGQTLAFVGSSGCGKSTSIQLLERFYDPDQGKVMIDGHDSKKVNVQFLRSNIGIVSQEPVLFACSIMDNIKYGDNTKEIPMERVIAAAKQAQLHDFVMSLPEKYETNVGSQGSQLSRGEKQRIAIARAIVRDPKILLLDEATSALDTESEKTVQVALDKAREGRTCIVIAHRLSTIQNADIIAVMAQGVVIEKGTHEELMAQKGAYYKLVTTGSPIS
375	Q9UBJ2	>sp|Q9UBJ2|ABCD2_HUMAN ATP-binding cassette sub-family D member 2 GN=ABCD2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MTHMLNAAADRVKWTRSSAAKRAACLVAAAYALKTLYPIIGKRLKQSGHGKKKAAAYPAAENTEILHCTETICEKPSPGVNADFFKQLLELRKILFPKLVTTETGWLCLHSVALISRTFLSIYVAGLDGKIVKSIVEKKPRTFIIKLIKWLMIAIPATFVNSAIRYLECKLALAFRTRLVDHAYETYFTNQTYYKVINMDGRLANPDQSLTEDIMMFSQSVAHLYSNLTKPILDVMLTSYTLIQTATSRGASPIGPTLLAGLVVYATAKVLKACSPKFGKLVAEEAHRKGYLRYVHSRIIANVEEIAFYRGHKVEMKQLQKSYKALADQMNLILSKRLWYIMIEQFLMKYVWSSSGLIMVAIPIITATGFADGEDGQKQVMVSERTEAFTTARNLLASGADAIERIMSSYKEVTELAGYTARVYNMFWVFDEVKRGIYKRTAVIQESESHSKNGAKVELPLSDTLAIKGKVIDVDHGIICENVPIITPAGEVVASRLNFKVEEGMHLLITGPNGCGKSSLFRILSGLWPVYEGVLYKPPPQHMFYIPQRPYMSLGSLRDQVIYPDSVDDMHDKGYTDQDLERILHNVHLYHIVQREGGWDAVMDWKDVLSGGEKQRMGMARMFYHKPKYALLDECTSAVSIDVEGKIFQAAKGAGISLLSITHRPSLWKYHTHLLQFDGEGGWRFEQLDTAIRLTLSEEKQKLESQLAGIPKMQQRLNELCKILGEDSVLKTIKNEDETS
376	P28288	>sp|P28288|ABCD3_HUMAN ATP-binding cassette sub-family D member 3 GN=ABCD3 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAAFSKYLTARNSSLAGAAFLLLCLLHKRRRALGLHGKKSGKPPLQNNEKEGKKERAVVDKVFFSRLIQILKIMVPRTFCKETGYLVLIAVMLVSRTYCDVWMIQNGTLIESGIIGRSRKDFKRYLLNFIAAMPLISLVNNFLKYGLNELKLCFRVRLTKYLYEEYLQAFTYYKMGNLDNRIANPDQLLTQDVEKFCNSVVDLYSNLSKPFLDIVLYIFKLTSAIGAQGPASMMAYLVVSGLFLTRLRRPIGKMTITEQKYEGEYRYVNSRLITNSEEIAFYNGNKREKQTVHSVFRKLVEHLHNFILFRFSMGFIDSIIAKYLATVVGYLVVSRPFLDLSHPRHLKSTHSELLEDYYQSGRMLLRMSQALGRIVLAGREMTRLAGFTARITELMQVLKDLNHGKYERTMVSQQEKGIEGVQVIPLIPGAGEIIIADNIIKFDHVPLATPNGDVLIRDLNFEVRSGANVLICGPNGCGKSSLFRVLGELWPLFGGRLTKPERGKLFYVPQRPYMTLGTLRDQVIYPDGREDQKRKGISDLVLKEYLDNVQLGHILEREGGWDSVQDWMDVLSGGEKQRMAMARLFYHKPQFAILDECTSAVSVDVEGYIYSHCRKVGITLFTVSHRKSLWKHHEYYLHMDGRGNYEFKQITEDTVEFGS
377	P61221	>sp|P61221|ABCE1_HUMAN ATP-binding cassette sub-family E member 1 GN=ABCE1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MADKLTRIAIVNHDKCKPKKCRQECKKSCPVVRMGKLCIEVTPQSKIAWISETLCIGCGICIKKCPFGALSIVNLPSNLEKETTHRYCANAFKLHRLPIPRPGEVLGLVGTNGIGKSTALKILAGKQKPNLGKYDDPPDWQEILTYFRGSELQNYFTKILEDDLKAIIKPQYVDQIPKAAKGTVGSILDRKDETKTQAIVCQQLDLTHLKERNVEDLSGGELQRFACAVVCIQKADIFMFDEPSSYLDVKQRLKAAITIRSLINPDRYIIVVEHDLSVLDYLSDFICCLYGVPSAYGVVTMPFSVREGINIFLDGYVPTENLRFRDASLVFKVAETANEEEVKKMCMYKYPGMKKKMGEFELAIVAGEFTDSEIMVMLGENGTGKTTFIRMLAGRLKPDEGGEVPVLNVSYKPQKISPKSTGSVRQLLHEKIRDAYTHPQFVTDVMKPLQIENIIDQEVQTLSGGELQRVALALCLGKPADVYLIDEPSAYLDSEQRLMAARVVKRFILHAKKTAFVVEHDFIMATYLADRVIVFDGVPSKNTVANSPQTLLAGMNKFLSQLEITFRRDPNNYRPRINKLNSIKDVEQKKSGNYFFLDD
378	Q9UG63	>sp|Q9UG63|ABCF2_HUMAN ATP-binding cassette sub-family F member 2 GN=ABCF2 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MPSDLAKKKAAKKKEAAKARQRPRKGHEENGDVVTEPQVAEKNEANGRETTEVDLLTKELEDFEMKKAAARAVTGVLASHPNSTDVHIINLSLTFHGQELLSDTKLELNSGRRYGLIGLNGIGKSMLLSAIGKREVPIPEHIDIYHLTREMPPSDKTPLHCVMEVDTERAMLEKEAERLAHEDAECEKLMELYERLEELDADKAEMRASRILHGLGFTPAMQRKKLKDFSGGWRMRVALARALFIRPFMLLLDEPTNHLDLDACVWLEEELKTFKRILVLVSHSQDFLNGVCTNIIHMHNKKLKYYTGNYDQYVKTRLELEENQMKRFHWEQDQIAHMKNYIARFGHGSAKLARQAQSKEKTLQKMMASGLTERVVSDKTLSFYFPPCGKIPPPVIMVQNVSFKYTKDGPCIYNNLEFGIDLDTRVALVGPNGAGKSTLLKLLTGELLPTDGMIRKHSHVKIGRYHQHLQEQLDLDLSPLEYMMKCYPEIKEKEEMRKIIGRYGLTGKQQVSPIRNLSDGQKCRVCLAWLAWQNPHMLFLDEPTNHLDIETIDALADAINEFEGGMMLVSHDFRLIQQVAQEIWVCEKQTITKWPGDILAYKEHLKSKLVDEEPQLTKRTHNV
379	Q9H172	>sp|Q9H172|ABCG4_HUMAN ATP-binding cassette sub-family G member 4 GN=ABCG4 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAEKALEAVGCGLGPGAVAMAVTLEDGAEPPVLTTHLKKVENHITEAQRFSHLPKRSAVDIEFVELSYSVREGPCWRKRGYKTLLKCLSGKFCRRELIGIMGPSGAGKSTFMNILAGYRESGMKGQILVNGRPRELRTFRKMSCYIMQDDMLLPHLTVLEAMMVSANLKLSEKQEVKKELVTEILTALGLMSCSHTRTALLSGGQRKRLAIALELVNNPPVMFFDEPTSGLDSASCFQVVSLMKSLAQGGRTIICTIHQPSAKLFEMFDKLYILSQGQCIFKGVVTNLIPYLKGLGLHCPTYHNPADFIIEVASGEYGDLNPMLFRAVQNGLCAMAEKKSSPEKNEVPAPCPPCPPEVDPIESHTFATSTLTQFCILFKRTFLSILRDTVLTHLRFMSHVVIGVLIGLLYLHIGDDASKVFNNTGCLFFSMLFLMFAALMPTVLTFPLEMAVFMREHLNYWYSLKAYYLAKTMADVPFQVVCPVVYCSIVYWMTGQPAETSRFLLFSALATATALVAQSLGLLIGAASNSLQVATFVGPVTAIPVLLFSGFFVSFKTIPTYLQWSSYLSYVRYGFEGVILTIYGMERGDLTCLEERCPFREPQSILRALDVEDAKLYMDFLVLGIFFLALRLLAYLVLRYRVKSER
380	Q6UXT9	>sp|Q6UXT9|ABH15_HUMAN Protein ABHD15 GN=ABHD15 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MPPWGAALALILAVLALLGLLGPRLRGPWGRAVGERTLPGAQDRDDGEEADGGGPADQFSDGREPLPGGCSLVCKPSALAQCLLRALRRSEALEAGPRSWFSGPHLQTLCHFVLPVAPGPELAREYLQLADDGLVALDWVVGPCVRGRRITSAGGLPAVLLVIPNAWGRLTRNVLGLCLLALERGYYPVIFHRRGHHGCPLVSPRLQPFGDPSDLKEAVTYIRFRHPAAPLFAVSEGSGSALLLSYLGECGSSSYVTGAACISPVLRCREWFEAGLPWPYERGFLLHQKIALSRYATALEDTVDTSRLFRSRSLREFEEALFCHTKSFPISWDTYWDRNDPLRDVDEAAVPVLCICSADDPVCGPPDHTLTTELFHSNPYFFLLLSRHGGHCGFLRQEPLPAWSHEVILESFRALTEFFRTEERIKGLSRHRASFLGGRRRGGALQRREVSSSSNLEEIFNWKRSYTR
381	Q9NUJ1	>sp|Q9NUJ1|ABHDA_HUMAN Mycophenolic acid acyl-glucuronide esterase, mitochondrial GN=ABHD10 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAVARLAAVAAWVPCRSWGWAAVPFGPHRGLSVLLARIPQRAPRWLPACRQKTSLSFLNRPDLPNLAYKKLKGKSPGIIFIPGYLSYMNGTKALAIEEFCKSLGHACIRFDYSGVGSSDGNSEESTLGKWRKDVLSIIDDLADGPQILVGSSLGGWLMLHAAIARPEKVVALIGVATAADTLVTKFNQLPVELKKEVEMKGVWSMPSKYSEEGVYNVQYSFIKEAEHHCLLHSPIPVNCPIRLLHGMKDDIVPWHTSMQVADRVLSTDVDVILRKHSDHRMREKADIQLLVYTIDDLIDKLSTIVN
382	Q7L211	>sp|Q7L211|ABHDD_HUMAN Protein ABHD13 GN=ABHD13 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MEKSWMLWNFVERWLIALASWSWALCRISLLPLIVTFHLYGGIILLLLIFISIAGILYKFQDVLLYFPEQPSSSRLYVPMPTGIPHENIFIRTKDGIRLNLILIRYTGDNSPYSPTIIYFHGNAGNIGHRLPNALLMLVNLKVNLLLVDYRGYGKSEGEASEEGLYLDSEAVLDYVMTRPDLDKTKIFLFGRSLGGAVAIHLASENSHRISAIMVENTFLSIPHMASTLFSFFPMRYLPLWCYKNKFLSYRKISQCRMPSLFISGLSDQLIPPVMMKQLYELSPSRTKRLAIFPDGTHNDTWQCQGYFTALEQFIKEVVKSHSPEEMAKTSSNVTII
383	Q9NYB9	>sp|Q9NYB9|ABI2_HUMAN Abl interactor 2 GN=ABI2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAELQMLLEEEIPGGRRALFDSYTNLERVADYCENNYIQSADKQRALEETKAYTTQSLASVAYLINTLANNVLQMLDIQASQLRRMESSINHISQTVDIHKEKVARREIGILTTNKNTSRTHKIIAPANLERPVRYIRKPIDYTILDDIGHGVKWLLRFKVSTQNMKMGGLPRTTPPTQKPPSPPMSGKGTLGRHSPYRTLEPVRPPVVPNDYVPSPTRNMAPSQQSPVRTASVNQRNRTYSSSGSSGGSHPSSRSSSRENSGSGSVGVPIAVPTPSPPSVFPAPAGSAGTPPLPATSASAPAPLVPATVPSSTAPNAAAGGAPNLADGFTSPTPPVVSSTPPTGHPVQFYSMNRPASRHTPPTIGGSLPYRRPPSITSQTSLQNQMNGGPFYSQNPVSDTPPPPPPVEEPVFDESPPPPPPPEDYEEEEAAVVEYSDPYAEEDPPWAPRSYLEKVVAIYDYTKDKEDELSFQEGAIIYVIKKNDDGWYEGVMNGVTGLFPGNYVESIMHYSE
384	Q15822	>sp|Q15822|ACHA2_HUMAN Neuronal acetylcholine receptor subunit alpha-2 GN=CHRNA2 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MGPSCPVFLSFTKLSLWWLLLTPAGGEEAKRPPPRAPGDPLSSPSPTALPQGGSHTETEDRLFKHLFRGYNRWARPVPNTSDVVIVRFGLSIAQLIDVDEKNQMMTTNVWLKQEWSDYKLRWNPTDFGNITSLRVPSEMIWIPDIVLYNNADGEFAVTHMTKAHLFSTGTVHWVPPAIYKSSCSIDVTFFPFDQQNCKMKFGSWTYDKAKIDLEQMEQTVDLKDYWESGEWAIVNATGTYNSKKYDCCAEIYPDVTYAFVIRRLPLFYTINLIIPCLLISCLTVLVFYLPSDCGEKITLCISVLLSLTVFLLLITEIIPSTSLVIPLIGEYLLFTMIFVTLSIVITVFVLNVHHRSPSTHTMPHWVRGALLGCVPRWLLMNRPPPPVELCHPLRLKLSPSYHWLESNVDAEEREVVVEEEDRWACAGHVAPSVGTLCSHGHLHSGASGPKAEALLQEGELLLSPHMQKALEGVHYIADHLRSEDADSSVKEDWKYVAMVIDRIFLWLFIIVCFLGTIGLFLPPFLAGMI
385	O96019	>sp|O96019|ACL6A_HUMAN Actin-like protein 6A GN=ACTL6A PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MSGGVYGGDEVGALVFDIGSYTVRAGYAGEDCPKVDFPTAIGMVVERDDGSTLMEIDGDKGKQGGPTYYIDTNALRVPRENMEAISPLKNGMVEDWDSFQAILDHTYKMHVKSEASLHPVLMSEAPWNTRAKREKLTELMFEHYNIPAFFLCKTAVLTAFANGRSTGLILDSGATHTTAIPVHDGYVLQQGIVKSPLAGDFITMQCRELFQEMNIELVPPYMIASKEAVREGSPANWKRKEKLPQVTRSWHNYMCNCVIQDFQASVLQVSDSTYDEQVAAQMPTVHYEFPNGYNCDFGAERLKIPEGLFDPSNVKGLSGNTMLGVSHVVTTSVGMCDIDIRPGLYGSVIVAGGNTLIQSFTDRLNRELSQKTPPSMRLKLIANNTTVERRFSSWIGGSILASLGTFQQMWISKQEYEEGGKQCVERKCP
386	Q9Y305	>sp|Q9Y305|ACOT9_HUMAN Acyl-coenzyme A thioesterase 9, mitochondrial GN=ACOT9 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MRRAALRLCALGKGQLTPGRGLTQGPQNPKKQGIFHIHEVRDKLREIVGASTNWRDHVKAMEERKLLHSFLAKSQDGLPPRRMKDSYIEVLLPLGSEPELREKYLTVQNTVRFGRILEDLDSLGVLICYMHNKIHSAKMSPLSIVTALVDKIDMCKKSLSPEQDIKFSGHVSWVGKTSMEVKMQMFQLHGDEFCPVLDATFVMVARDSENKGPAFVNPLIPESPEEEELFRQGELNKGRRIAFSSTSLLKMAPSAEERTTIHEMFLSTLDPKTISFRSRVLPSNAVWMENSKLKSLEICHPQERNIFNRIFGGFLMRKAYELAWATACSFGGSRPFVVAVDDIMFQKPVEVGSLLFLSSQVCFTQNNYIQVRVHSEVASLQEKQHTTTNVFHFTFMSEKEVPLVFPKTYGESMLYLDGQRHFNSMSGPATLRKDYLVEP
387	P10323	>sp|P10323|ACRO_HUMAN Acrosin GN=ACR PE=2 SV=4 Homo sapiens OS=Human NCBI_TaxID=9606	MVEMLPTAILLVLAVSVVAKDNATCDGPCGLRFRQNPQGGVRIVGGKAAQHGAWPWMVSLQIFTYNSHRYHTCGGSLLNSRWVLTAAHCFVGKNNVHDWRLVFGAKEITYGNNKPVKAPLQERYVEKIIIHEKYNSATEGNDIALVEITPPISCGRFIGPGCLPHFKAGLPRGSQSCWVAGWGYIEEKAPRPSSILMEARVDLIDLDLCNSTQWYNGRVQPTNVCAGYPVGKIDTCQGDSGGPLMCKDSKESAYVVVGITSWGVGCARAKRPGIYTATWPYLNWIASKIGSNALRMIQSATPPPPTTRPPPIRPPFSHPISAHLPWYFQPPPRPLPPRPPAAQPRPPPSPPPPPPPPASPLPPPPPPPPPTPSSTTKLPQGLSFAKRLQQLIEVLKGKTYSDGKNHYDMETTELPELTSTS
388	Q68CK6	>sp|Q68CK6|ACS2B_HUMAN Acyl-coenzyme A synthetase ACSM2B, mitochondrial GN=ACSM2B PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MHWLRKVQGLCTLWGTQMSSRTLYINSRQLVSLQWGHQEVPAKFNFASDVLDHWADMEKAGKRLPSPALWWVNGKGKELMWNFRELSENSQQAANILSGACGLQRGDRVAVMLPRVPEWWLVILGCIRAGLIFMPGTIQMKSTDILYRLQMSKAKAIVAGDEVIQEVDTVASECPSLRIKLLVSEKSCDGWLNFKKLLNEASTTHHCVETGSQEASAIYFTSGTSGLPKMAEHSYSSLGLKAKMDAGWTGLQASDIMWTISDTGWILNILGSLLESWTLGACTFVHLLPKFDPLVILKTLSSYPIKSMMGAPIVYRMLLQQDLSSYKFPHLQNCLAGGESLLPETLENWRAQTGLDIREFYGQTETGLTCMVSKTMKIKPGYMGTAASCYDVQVIDDKGNVLPPGTEGDIGIRVKPIRPIGIFSGYVENPDKTAANIRGDFWLLGDRGIKDEDGYFQFMGRADDIINSSGYRIGPSEVENALMKHPAVVETAVISSPDPVRGEVVKAFVILASQFLSHDPEQLTKELQQHVKSVTAPYKYPRKIEFVLNLPKTVTGKIQRTKLRDKEWKMSGKARAQ
389	Q53FZ2	>sp|Q53FZ2|ACSM3_HUMAN Acyl-coenzyme A synthetase ACSM3, mitochondrial GN=ACSM3 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MLARVTRKMLRHAKCFQRLAIFGSVRALHKDNRTATPQNFSNYESMKQDFKLGIPEYFNFAKDVLDQWTDKEKAGKKPSNPAFWWINRNGEEMRWSFEELGSLSRKFANILSEACSLQRGDRVILILPRVPEWWLANVACLRTGTVLIPGTTQLTQKDILYRLQSSKANCIITNDVLAPAVDAVASKCENLHSKLIVSENSREGWGNLKELMKHASDSHTCVKTKHNEIMAIFFTSGTSGYPKMTAHTHSSFGLGLSVNGRFWLDLTPSDVMWNTSDTGWAKSAWSSVFSPWIQGACVFTHHLPRFEPTSILQTLSKYPITVFCSAPTVYRMLVQNDITSYKFKSLKHCVSAGEPITPDVTEKWRNKTGLDIYEGYGQTETVLICGNFKGMKIKPGSMGKPSPAFDVKIVDVNGNVLPPGQEGDIGIQVLPNRPFGLFTHYVDNPSKTASTLRGNFYITGDRGYMDKDGYFWFVARADDVILSSGYRIGPFEVENALNEHPSVAESAVVSSPDPIRGEVVKAFVVLNPDYKSHDQEQLIKEIQEHVKKTTAPYKYPRKVEFIQELPKTISGKTKRNELRKKEWKTI
390	Q6NUN0	>sp|Q6NUN0|ACSM5_HUMAN Acyl-coenzyme A synthetase ACSM5, mitochondrial GN=ACSM5 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MRPWLRHLVLQALRNSRAFCGSHGKPAPLPVPQKIVATWEAISLGRQLVPEYFNFAHDVLDVWSRLEEAGHRPPNPAFWWVNGTGAEIKWSFEELGKQSRKAANVLGGACGLQPGDRMMLVLPRLPEWWLVSVACMRTGTVMIPGVTQLTEKDLKYRLQASRAKSIITSDSLAPRVDAISAECPSLQTKLLVSDSSRPGWLNFRELLREASTEHNCMRTKSRDPLAIYFTSGTTGAPKMVEHSQSSYGLGFVASGRRWVALTESDIFWNTTDTGWVKAAWTLFSAWPNGSCIFVHELPRVDAKVILNTLSKFPITTLCCVPTIFRLLVQEDLTRYQFQSLRHCLTGGEALNPDVREKWKHQTGVELYEGYGQSETVVICANPKGMKIKSGSMGKASPPYDVQIVDDEGNVLPPGEEGNVAVRIRPTRPFCFFNCYLDNPEKTAASEQGDFYITGDRARMDKDGYFWFMGRNDDVINSSSYRIGPVEVESALAEHPAVLESAVVSSPDPIRGEVVKAFIVLTPAYSSHDPEALTRELQEHVKRVTAPYKYPRKVAFVSELPKTVSGKIQRSKLRSQEWGK
391	P62736	>sp|P62736|ACTA_HUMAN Actin, aortic smooth muscle GN=ACTA2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MCEEEDSTALVCDNGSGLCKAGFAGDDAPRAVFPSIVGRPRHQGVMVGMGQKDSYVGDEAQSKRGILTLKYPIEHGIITNWDDMEKIWHHSFYNELRVAPEEHPTLLTEAPLNPKANREKMTQIMFETFNVPAMYVAIQAVLSLYASGRTTGIVLDSGDGVTHNVPIYEGYALPHAIMRLDLAGRDLTDYLMKILTERGYSFVTTAEREIVRDIKEKLCYVALDFENEMATAASSSSLEKSYELPDGQVITIGNERFRCPETLFQPSFIGMESAGIHETTYNSIMKCDIDIRKDLYANNVLSGGTTMYPGIADRMQKEITALAPSTMKIKIIAPPERKYSVWIGGSILASLSTFQQMWISKQEYDEAGPSIVHRKCF
392	Q9BYX7	>sp|Q9BYX7|ACTBM_HUMAN Putative beta-actin-like protein 3 GN=POTEKP PE=5 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MDDDTAVLVIDNGSGMCKAGFAGDDAPQAVFPSIVGRPRHQGMMEGMHQKESYVGKEAQSKRGMLTLKYPMEHGIITNWDDMEKIWHHTFYNELRVAPEEHPILLTEAPLNPKANREKMTQIMFETFNTPAMYVAIQAVLSLYTSGRTTGIVMDSGDGFTHTVPIYEGNALPHATLRLDLAGRELTDYLMKILTERGYRFTTTAEQEIVRDIKEKLCYVALDSEQEMAMAASSSSVEKSYELPDGQVITIGNERFRCPEALFQPCFLGMESCGIHKTTFNSIVKSDVDIRKDLYTNTVLSGGTTMYPGIAHRMQKEITALAPSIMKIKIIAPPKRKYSVWVGGSILASLSTFQQMWISKQEYDESGPSIVHRKCF
393	P68032	>sp|P68032|ACTC_HUMAN Actin, alpha cardiac muscle 1 GN=ACTC1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MCDDEETTALVCDNGSGLVKAGFAGDDAPRAVFPSIVGRPRHQGVMVGMGQKDSYVGDEAQSKRGILTLKYPIEHGIITNWDDMEKIWHHTFYNELRVAPEEHPTLLTEAPLNPKANREKMTQIMFETFNVPAMYVAIQAVLSLYASGRTTGIVLDSGDGVTHNVPIYEGYALPHAIMRLDLAGRDLTDYLMKILTERGYSFVTTAEREIVRDIKEKLCYVALDFENEMATAASSSSLEKSYELPDGQVITIGNERFRCPETLFQPSFIGMESAGIHETTYNSIMKCDIDIRKDLYANNVLSGGTTMYPGIADRMQKEITALAPSTMKIKIIAPPERKYSVWIGGSILASLSTFQQMWISKQEYDEAGPSIVHRKCF
394	Q8TDY3	>sp|Q8TDY3|ACTT2_HUMAN Actin-related protein T2 GN=ACTRT2 PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MFNPHALDSPAVIFDNGSGFCKAGLSGEFGPRHMVSSIVGHLKFQAPSAEANQKKYFVGEEALYKQEALQLHSPFERGLITGWDDVERLWKHLFEWELGVKPSDQPLLATEPSLNPRENREKMAEVMFENFGVPAFYLSDQAVLALYASACVTGLVVDSGDAVTCTVPIFEGYSLPHAVTKLHVAGRDITELLMQLLLASGHTFPCQLDKGLVDDIKKKLCYVALEPEKELSRRPEEVLREYKLPDGNIISLGDPLHQAPEALFVPQQLGSQSPGLSNMVSSSITKCDTDIQKILFGEIVLSGGTTLFHGLDDRLLKELEQLASKDTPIKITAPPDRWFSTWIGASIVTSLSSFKQMWVTAADFKEFGTSVVQRRCF
406	Q53H12	>sp|Q53H12|AGK_HUMAN Acylglycerol kinase, mitochondrial GN=AGK PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MTVFFKTLRNHWKKTTAGLCLLTWGGHWLYGKHCDNLLRRAACQEAQVFGNQLIPPNAQVKKATVFLNPAACKGKARTLFEKNAAPILHLSGMDVTIVKTDYEGQAKKLLELMENTDVIIVAGGDGTLQEVVTGVLRRTDEATFSKIPIGFIPLGETSSLSHTLFAESGNKVQHITDATLAIVKGETVPLDVLQIKGEKEQPVFAMTGLRWGSFRDAGVKVSKYWYLGPLKIKAAHFFSTLKEWPQTHQASISYTGPTERPPNEPEETPVQRPSLYRRILRRLASYWAQPQDALSQEVSPEVWKDVQLSTIELSITTRNNQLDPTSKEDFLNICIEPDTISKGDFITIGSRKVRNPKLHVEGTECLQASQCTLLIPEGAGGSFSIDSEEYEAMPVEVKLLPRKLQFFCDPRKREQMLTSPTQ
395	Q04771	>sp|Q04771|ACVR1_HUMAN Activin receptor type-1 GN=ACVR1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MVDGVMILPVLIMIALPSPSMEDEKPKVNPKLYMCVCEGLSCGNEDHCEGQQCFSSLSINDGFHVYQKGCFQVYEQGKMTCKTPPSPGQAVECCQGDWCNRNITAQLPTKGKSFPGTQNFHLEVGLIILSVVFAVCLLACLLGVALRKFKRRNQERLNPRDVEYGTIEGLITTNVGDSTLADLLDHSCTSGSGSGLPFLVQRTVARQITLLECVGKGRYGEVWRGSWQGENVAVKIFSSRDEKSWFRETELYNTVMLRHENILGFIASDMTSRHSSTQLWLITHYHEMGSLYDYLQLTTLDTVSCLRIVLSIASGLAHLHIEIFGTQGKPAIAHRDLKSKNILVKKNGQCCIADLGLAVMHSQSTNQLDVGNNPRVGTKRYMAPEVLDETIQVDCFDSYKRVDIWAFGLVLWEVARRMVSNGIVEDYKPPFYDVVPNDPSFEDMRKVVCVDQQRPNIPNRWFSDPTLTSLAKLMKECWYQNPSARLTALRIKKTLTKIDNSLDKLKTDC
396	Q7Z695	>sp|Q7Z695|ADCK2_HUMAN Uncharacterized aarF domain-containing protein kinase 2 GN=ADCK2 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MVAPWRVSVRVCLSHLRCFELRQGLSLLRPSECPRDARLCWLLLGTLPKVVSLCGDVGEGAPDVLSRRRVRCSGAAGAGPAESLPRAGPLGGVFLHLRLWLRAGALLVKFFPLLLLYPLTYLAPSVSTLWLHLLLKATETSGPTYIKLGQWASTRRDLFSEAFCAQFSKLHVRVTPHPWTHTERFLRQAFGDDWGSILSFENREPVGSGCVAQVYKAYANTAFLETDSVQRLGRASCLPPFSHTGAVGGLRELFGYLGNGRKPPENLADQSFLERLLLPKADLVGSNAGVSRAQVPGHQPEATNLISVAVKVLHPGLLAQVHMDLLLMKIGSRVLGVLPGIKWLSLPEIVEEFEKLMVQQIDLRYEAQNLEHFQVNFRNVKAVKFPTPLRPFVTREVLVETYEESVPVSSYQQAGIPVDLKRKIARLGINMLLKMIFVDNFVHADLHPGNILVQGANGLSSSQEAQLQQADICDTLVVAVPSSLCPLRLVLLDAGIVAELQAPDLRNFRAVFMAVVMGQGQRVAELILHHARASECRDVEGFKTEMAMLVTQARKNTITLEKLHVSSLLSSVFKLLMTHKVKLESNFASIVFAIMVLEGLGRSLDPKLDILEAARPFLLTGPVCPP
397	Q3MIX3	>sp|Q3MIX3|ADCK5_HUMAN Uncharacterized aarF domain-containing protein kinase 5 GN=ADCK5 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MWRPVQLCHFHSALLHRRQKPWPSPAVFFRRNVRGLPPRFSSPTPLWRKVLSTAVVGAPLLLGARYVMAEAREKRRMRLVVDGMGRFGRSLKVGLQISLDYWWCTNVVLRGVEENSPGYLEVMSACHQRAADALVAGAISNGGLYVKLGQGLCSFNHLLPPEYTRTLRVLEDRALKRGFQEVDELFLEDFQALPHELFQEFDYQPIAAASLAQVHRAKLHDGTSVAVKVQYIDLRDRFDGDIHTLELLLRLVEVMHPSFGFSWVLQDLKGTLAQELDFENEGRNAERCARELAHFPYVVVPRVHWDKSSKRVLTADFCAGCKVNDVEAIRSQGLAVHDIAEKLIKAFAEQIFYTGFIHSDPHPGNVLVRKGPDGKAELVLLDHGLYQFLEEKDRAALCQLWRAIILRDDAAMRAHAAALGVQDYLLFAEMLMQRPVRLGQLWGSHLLSREEAAYMVDMARERFEAVMAVLRELPRPMLLVLRNINTVRAINVALGAPVDRYFLMAKRAVRGWSRLAGATYRGVYGTSLLRHAKVVWEMLKFEVALRLETLAMRLTALLARALVHLSLVPPAEELYQYLET
398	O60266	>sp|O60266|ADCY3_HUMAN Adenylate cyclase type 3 GN=ADCY3 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MPRNQGFSEPEYSAEYSAEYSVSLPSDPDRGVGRTHEISVRNSGSCLCLPRFMRLTFVPESLENLYQTYFKRQRHETLLVLVVFAALFDCYVVVMCAVVFSSDKLASLAVAGIGLVLDIILFVLCKKGLLPDRVTRRVLPYVLWLLITAQIFSYLGLNFARAHAASDTVGWQVFFVFSFFITLPLSLSPIVIISVVSCVVHTLVLGVTVAQQQQEELKGMQLLREILANVFLYLCAIAVGIMSYYMADRKHRKAFLEARQSLEVKMNLEEQSQQQENLMLSILPKHVADEMLKDMKKDESQKDQQQFNTMYMYRHENVSILFADIVGFTQLSSACSAQELVKLLNELFARFDKLAAKYHQLRIKILGDCYYCICGLPDYREDHAVCSILMGLAMVEAISYVREKTKTGVDMRVGVHTGTVLGGVLGQKRWQYDVWSTDVTVANKMEAGGIPGRVHISQSTMDCLKGEFDVEPGDGGSRCDYLEEKGIETYLIIASKPEVKKTATQNGLNGSALPNGAPASSKSSSPALIETKEPNGSAHSSGSTSEKPEEQDAQADNPSFPNPRRRLRLQDLADRVVDASEDEHELNQLLNEALLERESAQVVKKRNTFLLSMRFMDPEMETRYSVEKEKQSGAAFSCSCVVLLCTALVEILIDPWLMTNYVTFMVGEILLLILTICSLAAIFPRAFPKKLVAFSTWIDRTRWARNTWAMLAIFILVMANVVDMLSCLQYYTGPSNATAGMETEGSCLENPKYYNYVAVLSLIATIMLVQVSHMVKLTLMLLVAGAVATINLYAWRPVFDEYDHKRFREHDLPMVALEQMQGFNPGLNGTDRLPLVPSKYSMTVMVFLMMLSFYYFSRHVEKLARTLFLWKIEVHDQKERVYEMRRWNEALVTNMLPEHVARHFLGSKKRDEELYSQTYDEIGVMFASLPNFADFYTEESINNGGIECLRFLNEIISDFDSLLDNPKFRVITKIKTIGSTYMAASGVTPDVNTNGFASSNKEDKSERERWQHLADLADFALAMKDTLTNINNQSFNNFMLRIGMNKGGVLAGVIGARKPHYDIWGNTVNVASRMESTGVMGNIQVVEETQVILREYGFRFVRRGPIFVKGKGELLTFFLKGRDKLATFPNGPSVTLPHQVVDNS
399	P51828	>sp|P51828|ADCY7_HUMAN Adenylate cyclase type 7 GN=ADCY7 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MPAKGRYFLNEGEEGPDQDALYEKYQLTSQHGPLLLTLLLVAATACVALIIIAFSQGDPSRHQAILGMAFLVLAVFAALSVLMYVECLLRRWLRALALLTWACLVALGYVLVFDAWTKAACAWEQVPFFLFIVFVVYTLLPFSMRGAVAVGAVSTASHLLVLGSLMGGFTTPSVRVGLQLLANAVIFLCGNLTGAFHKHQMQDASRDLFTYTVKCIQIRRKLRIEKRQQENLLLSVLPAHISMGMKLAIIERLKEHGDRRCMPDNNFHSLYVKRHQNVSILYADIVGFTQLASDCSPKELVVVLNELFGKFDQIAKANECMRIKILGDCYYCVSGLPVSLPTHARNCVKMGLDMCQAIKQVREATGVDINMRVGIHSGNVLCGVIGLRKWQYDVWSHDVSLANRMEAAGVPGRVHITEATLKHLDKAYEVEDGHGQQRDPYLKEMNIRTYLVIDPRSQQPPPPSQHLPRPKGDAALKMRASVRMTRYLESWGAARPFAHLNHRESVSSGETHVPNGRRPKSVPQRHRRTPDRSMSPKGRSEDDSYDDEMLSAIEGLSSTRPCCSKSDDFYTFGSIFLEKGFEREYRLAPIPRARHDFACASLIFVCILLVHVLLMPRTAALGVSFGLVACVLGLVLGLCFATKFSRCCPARGTLCTISERVETQPLLRLTLAVLTIGSLLTVAIINLPLMPFQVPELPVGNETGLLAASSKTRALCEPLPYYTCSCVLGFIACSVFLRMSLEPKVVLLTVALVAYLVLFNLSPCWQWDCCGQGLGNLTKPNGTTSGTPSCSWKDLKTMTNFYLVLFYITLLTLSRQIDYYCRLDCLWKKKFKKEHEEFETMENVNRLLLENVLPAHVAAHFIGDKLNEDWYHQSYDCVCVMFASVPDFKVFYTECDVNKEGLECLRLLNEIIADFDELLLKPKFSGVEKIKTIGSTYMAAAGLSVASGHENQELERQHAHIGVMVEFSIALMSKLDGINRHSFNSFRLRVGINHGPVIAGVIGARKPQYDIWGNTVNVASRMESTGELGKIQVTEETCTILQGLGYSCECRGLINVKGKGELRTYFVCTDTAKFQGLGLN
400	P07327	>sp|P07327|ADH1A_HUMAN Alcohol dehydrogenase 1A GN=ADH1A PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MSTAGKVIKCKAAVLWELKKPFSIEEVEVAPPKAHEVRIKMVAVGICGTDDHVVSGTMVTPLPVILGHEAAGIVESVGEGVTTVKPGDKVIPLAIPQCGKCRICKNPESNYCLKNDVSNPQGTLQDGTSRFTCRRKPIHHFLGISTFSQYTVVDENAVAKIDAASPLEKVCLIGCGFSTGYGSAVNVAKVTPGSTCAVFGLGGVGLSAIMGCKAAGAARIIAVDINKDKFAKAKELGATECINPQDYKKPIQEVLKEMTDGGVDFSFEVIGRLDTMMASLLCCHEACGTSVIVGVPPDSQNLSMNPMLLLTGRTWKGAILGGFKSKECVPKLVADFMAKKFSLDALITHVLPFEKINEGFDLLHSGKSIRTILMF
401	P00325	>sp|P00325|ADH1B_HUMAN Alcohol dehydrogenase 1B GN=ADH1B PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MSTAGKVIKCKAAVLWEVKKPFSIEDVEVAPPKAYEVRIKMVAVGICRTDDHVVSGNLVTPLPVILGHEAAGIVESVGEGVTTVKPGDKVIPLFTPQCGKCRVCKNPESNYCLKNDLGNPRGTLQDGTRRFTCRGKPIHHFLGTSTFSQYTVVDENAVAKIDAASPLEKVCLIGCGFSTGYGSAVNVAKVTPGSTCAVFGLGGVGLSAVMGCKAAGAARIIAVDINKDKFAKAKELGATECINPQDYKKPIQEVLKEMTDGGVDFSFEVIGRLDTMMASLLCCHEACGTSVIVGVPPASQNLSINPMLLLTGRTWKGAVYGGFKSKEGIPKLVADFMAKKFSLDALITHVLPFEKINEGFDLLHSGKSIRTVLTF
402	P00326	>sp|P00326|ADH1G_HUMAN Alcohol dehydrogenase 1C GN=ADH1C PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MSTAGKVIKCKAAVLWELKKPFSIEEVEVAPPKAHEVRIKMVAAGICRSDEHVVSGNLVTPLPVILGHEAAGIVESVGEGVTTVKPGDKVIPLFTPQCGKCRICKNPESNYCLKNDLGNPRGTLQDGTRRFTCSGKPIHHFVGVSTFSQYTVVDENAVAKIDAASPLEKVCLIGCGFSTGYGSAVKVAKVTPGSTCAVFGLGGVGLSVVMGCKAAGAARIIAVDINKDKFAKAKELGATECINPQDYKKPIQEVLKEMTDGGVDFSFEVIGRLDTMMASLLCCHEACGTSVIVGVPPDSQNLSINPMLLLTGRTWKGAIFGGFKSKESVPKLVADFMAKKFSLDALITNILPFEKINEGFDLLRSGKSIRTVLTF
403	Q8WTP8	>sp|Q8WTP8|AEN_HUMAN Apoptosis-enhancing nuclease GN=AEN PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MVPREAPESAQCLCPSLTIPNAKDVLRKRHKRRSRQHQRFMARKALLQEQGLLSMPPEPGSSPLPTPFGAATATEAASSGKQCLRAGSGSAPCSRRPAPGKASGPLPSKCVAIDCEMVGTGPRGRVSELARCSIVSYHGNVLYDKYIRPEMPIADYRTRWSGITRQHMRKAVPFQVAQKEILKLLKGKVVVGHALHNDFQALKYVHPRSQTRDTTYVPNFLSEPGLHTRARVSLKDLALQLLHKKIQVGQHGHSSVEDATTAMELYRLVEVQWEQQEARSLWTCPEDREPDSSTDMEQYMEDQYWPDDLAHGSRGGAREAQDRRN
404	A6NIR3	>sp|A6NIR3|AGAP5_HUMAN Arf-GAP with GTPase, ANK repeat and PH domain-containing protein 5 GN=AGAP5 PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MGNILTCCVHPSVSLEFDQQQGSVCPSESEIYEAGAGDRMAGAPMAAAVQPAEVTVEVGEDLHMHHIRDQEMPEALEFSLSANPEASTIFQRNSQTDALEFNPSANPEASTIFQRNSQTDVVEIRRSNCTNHVSTERFSQQYSSCSTIFLDDSTASQHYLTMTIISVTLEIPHHITQRDADRSLSIPDEQLHSFAVSTVHITKNRNGGGSLNNYSSSIPSTPSTSQEDPQFSVPPTANTPTPVCKRSMRWSNLFTSEKGSHPDKERKAPENHADTIGSGRAIPIKQGMLLKRSGKWLKTWKKKYVTLCSNGVLTYYSSLGDYMKNIHKKEIDLRTSTIKVPGKWPSLATSACAPISSSKSNGLSKDMDTGLGDSICFSPSISSTTSPKLNPPPSPHANKKKHLKKKSTNNFMIVSATGQTWHFEATTYEERDAWVQAIQSQILASLQSCESSKSKSQLTSQSEAMALQSIQNMRGNAHCVDYETQNPKWASLNLGVLMCIECSGIHRSLGTRLSRVRSLELDDWPVELRKVMSSIGNDLANSIWEGSSQGQTKPSVKSTREEKERWIRSKYEEKLFLAPLPCTELSLGQHLLRATADEDLQTAILLLAHGSREEVNETCGEGDGCTALHLACRKGNVVLAQLLIWYGVDVMARDAHGNTALTYARQASSQECINVLLQYGCPDECV
405	Q9H0P7	>sp|Q9H0P7|AGIT1_HUMAN Putative uncharacterized protein encoded by AGPAT4-IT1 GN=AGPAT4-IT1 PE=5 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MADTQCCPPPCEFISSAGTDLALGMGWDATLCLLPFTGFGKCAGIWNHMDEEPDNGDDRGSRRTTGQGRKWAAHGTMAAPRVHTDYHPGGGSACSSVKVRSHVGHTGVFFFVDQDPLAVSLTSQSLIPPLIKPGLLKAWGFLLLCAQPSANGHSLCCLLYTDLVSSHELSPFRALCLGPSDAPSACASCNCLASTYYL
407	Q14246	>sp|Q14246|AGRE1_HUMAN Adhesion G protein-coupled receptor E1 GN=ADGRE1 PE=2 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MRGFNLLLFWGCCVMHSWEGHIRPTRKPNTKGNNCRDSTLCPAYATCTNTVDSYYCACKQGFLSSNGQNHFKDPGVRCKDIDECSQSPQPCGPNSSCKNLSGRYKCSCLDGFSSPTGNDWVPGKPGNFSCTDINECLTSSVCPEHSDCVNSMGSYSCSCQVGFISRNSTCEDVDECADPRACPEHATCNNTVGNYSCFCNPGFESSSGHLSFQGLKASCEDIDECTEMCPINSTCTNTPGSYFCTCHPGFAPSNGQLNFTDQGVECRDIDECRQDPSTCGPNSICTNALGSYSCGCIAGFHPNPEGSQKDGNFSCQRVLFKCKEDVIPDNKQIQQCQEGTAVKPAYVSFCAQINNIFSVLDKVCENKTTVVSLKNTTESFVPVLKQISTWTKFTKEETSSLATVFLESVESMTLASFWKPSANITPAVRTEYLDIESKVINKECSEENVTLDLVAKGDKMKIGCSTIEESESTETTGVAFVSFVGMESVLNERFFKDHQAPLTTSEIKLKMNSRVVGGIMTGEKKDGFSDPIIYTLENIQPKQKFERPICVSWSTDVKGGRWTSFGCVILEASETYTICSCNQMANLAVIMASGELTMDFSLYIISHVGIIISLVCLVLAIATFLLCRSIRNHNTYLHLHLCVCLLLAKTLFLAGIHKTDNKMGCAIIAGFLHYLFLACFFWMLVEAVILFLMVRNLKVVNYFSSRNIKMLHICAFGYGLPMLVVVISASVQPQGYGMHNRCWLNTETGFIWSFLGPVCTVIVINSLLLTWTLWILRQRLSSVNAEVSTLKDTRLLTFKAFAQLFILGCSWVLGIFQIGPVAGVMAYLFTIINSLQGAFIFLIHCLLNGQVREEYKRWITGKTKPSSQSQTSRILLSSMPSASKTG
408	Q9BY15	>sp|Q9BY15|AGRE3_HUMAN Adhesion G protein-coupled receptor E3 GN=ADGRE3 PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MQGPLLLPGLCFLLSLFGAVTQKTKTSCAKCPPNASCVNNTHCTCNHGYTSGSGQKLFTFPLETCNDINECTPPYSVYCGFNAVCYNVEGSFYCQCVPGYRLHSGNEQFSNSNENTCQDTTSSKTTEGRKELQKIVDKFESLLTNQTLWRTEGRQEISSTATTILRDVESKVLETALKDPEQKVLKIQNDSVAIETQAITDNCSEERKTFNLNVQMNSMDIRCSDIIQGDTQGPSAIAFISYSSLGNIINATFFEEMDKKDQVYLNSQVVSAAIGPKRNVSLSKSVTLTFQHVKMTPSTKKVFCVYWKSTGQGSQWSRDGCFLIHVNKSHTMCNCSHLSSFAVLMALTSQEEDPVLTVITYVGLSVSLLCLLLAALTFLLCKAIRNTSTSLHLQLSLCLFLAHLLFLVGIDRTEPKVLCSIIAGALHYLYLAAFTWMLLEGVHLFLTARNLTVVNYSSINRLMKWIMFPVGYGVPAVTVAISAASWPHLYGTADRCWLHLDQGFMWSFLGPVCAIFSANLVLFILVFWILKRKLSSLNSEVSTIQNTRMLAFKATAQLFILGCTWCLGLLQVGPAAQVMAYLFTIINSLQGFFIFLVYCLLSQQVQKQYQKWFREIVKSKSESETYTLSSKMGPDSKPSEGDVFPGQVKRKY
409	Q5T601	>sp|Q5T601|AGRF1_HUMAN Adhesion G-protein coupled receptor F1 GN=ADGRF1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MKVGVLWLISFFTFTDGHGGFLGKNDGIKTKKELIVNKKKHLGPVEEYQLLLQVTYRDSKEKRDLRNFLKLLKPPLLWSHGLIRIIRAKATTDCNSLNGVLQCTCEDSYTWFPPSCLDPQNCYLHTAGALPSCECHLNNLSQSVNFCERTKIWGTFKINERFTNDLLNSSSAIYSKYANGIEIQLKKAYERIQGFESVQVTQFRNGSIVAGYEVVGSSSASELLSAIEHVAEKAKTALHKLFPLEDGSFRVFGKAQCNDIVFGFGSKDDEYTLPCSSGYRGNITAKCESSGWQVIRETCVLSLLEELNKNFSMIVGNATEAAVSSFVQNLSVIIRQNPSTTVGNLASVVSILSNISSLSLASHFRVSNSTMEDVISIADNILNSASVTNWTVLLREEKYASSRLLETLENISTLVPPTALPLNFSRKFIDWKGIPVNKSQLKRGYSYQIKMCPQNTSIPIRGRVLIGSDQFQRSLPETIISMASLTLGNILPVSKNGNAQVNGPVISTVIQNYSINEVFLFFSKIESNLSQPHCVFWDFSHLQWNDAGCHLVNETQDIVTCQCTHLTSFSILMSPFVPSTIFPVVKWITYVGLGISIGSLILCLIIEALFWKQIKKSQTSHTRRICMVNIALSLLIADVWFIVGATVDTTVNPSGVCTAAVFFTHFFYLSLFFWMLMLGILLAYRIILVFHHMAQHLMMAVGFCLGYGCPLIISVITIAVTQPSNTYKRKDVCWLNWSNGSKPLLAFVVPALAIVAVNFVVVLLVLTKLWRPTVGERLSRDDKATIIRVGKSLLILTPLLGLTWGFGIGTIVDSQNLAWHVIFALLNAFQGFFILCFGILLDSKLRQLLFNKLSALSSWKQTEKQNSSDLSAKPKFSKPFNPLQNKGHYAFSHTGDSSDNIMLTQFVSNE
410	Q86Y34	>sp|Q86Y34|AGRG3_HUMAN Adhesion G protein-coupled receptor G3 GN=ADGRG3 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MATPRGLGALLLLLLLPTSGQEKPTEGPRNTCLGSNNMYDIFNLNDKALCFTKCRQSGSDSCNVENLQRYWLNYEAHLMKEGLTQKVNTPFLKALVQNLSTNTAEDFYFSLEPSQVPRQVMKDEDKPPDRVRLPKSLFRSLPGNRSVVRLAVTILDIGPGTLFKGPRLGLGDGSGVLNNRLVGLSVGQMHVTKLAEPLEIVFSHQRPPPNMTLTCVFWDVTKGTTGDWSSEGCSTEVRPEGTVCCCDHLTFFALLLRPTLDQSTVHILTRISQAGCGVSMIFLAFTIILYAFLRLSRERFKSEDAPKIHVALGGSLFLLNLAFLVNVGSGSKGSDAACWARGAVFHYFLLCAFTWMGLEAFHLYLLAVRVFNTYFGHYFLKLSLVGWGLPALMVIGTGSANSYGLYTIRDRENRTSLELCWFREGTTMYALYITVHGYFLITFLFGMVVLALVVWKIFTLSRATAVKERGKNRKKVLTLLGLSSLVGVTWGLAIFTPLGLSTVYIFALFNSLQGVFICCWFTILYLPSQSTTVSSSTARLDQAHSASQE
411	O00253	>sp|O00253|AGRP_HUMAN Agouti-related protein GN=AGRP PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLTAAVLSCALLLALPATRGAQMGLAPMEGIRRPDQALLPELPGLGLRAPLKKTTAEQAEEDLLQEAQALAEVLDLQDREPRSSRRCVRLHESCLGQQVPCCDPCATCYCRFFNAFCYCRKLGTAMNPCSRT
412	Q9BRQ8	>sp|Q9BRQ8|AIFM2_HUMAN Apoptosis-inducing factor 2 GN=AIFM2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MGSQVSVESGALHVVIVGGGFGGIAAASQLQALNVPFMLVDMKDSFHHNVAALRASVETGFAKKTFISYSVTFKDNFRQGLVVGIDLKNQMVLLQGGEALPFSHLILATGSTGPFPGKFNEVSSQQAAIQAYEDMVRQVQRSRFIVVVGGGSAGVEMAAEIKTEYPEKEVTLIHSQVALADKELLPSVRQEVKEILLRKGVQLLLSERVSNLEELPLNEYREYIKVQTDKGTEVATNLVILCTGIKINSSAYRKAFESRLASSGALRVNEHLQVEGHSNVYAIGDCADVRTPKMAYLAGLHANIAVANIVNSVKQRPLQAYKPGALTFLLSMGRNDGVGQISGFYVGRLMVRLTKSRDLFVSTSWKTMRQSPP
413	Q8N1P7	>sp|Q8N1P7|AIM1L_HUMAN Absent in melanoma 1-like protein GN=AIM1L PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MELRTPGTKWSPQGIGSLRRVVWDYSTPEISLFSEEGLKGEQVKLTEALKNSQGLEKPLQVASATVSAGLWLLYPKPLFEDTPYILEPGEYPTSEAWGTSDPSVGSLKPMRLGCPSVEKPGEPRAVVYEAPGFQGRSWEVSRDIYNLQQPEDSQSPHLASVGSLRVLGGCWVGYEKEGFRGHQYLLEEGEYPDWSHWGGYDELLTSLRVIRTDFGDPAVVLFEAMDFEGHGVEVSKALPDVELVQHGPSTQAIHVLSGVWVAYQEVGFSGEQYVLEKGVYRNCEDWGAGNSTLASLQPVLQVGEHDLHFVSKIQLFSRPDFLGDHFSFEDDQAALPASFRPQSCRVHGGSWILFDETNFEGDQHILSEGEFPTLTAMGCLASTVLGSLQKVSLHFSEPSIFLYGLECFEGKEIELSREVRSLQAEGFNNHVLSVRIKGGIWVLCEHSDFRGRQWLVGSCEITNWLTYSGTQRVGSLYPIKQRRVYFRLWNAALGGFLAVPDHVEDMKAGRVVVADPQAGGSCIWYYEDGLLKNQMAPTMSLQVIGPPSPGSKVVLWAESRLPRQTWSISESGHICSQMFEGQILDVKGGRGYDRDHVVLWEPDEDRASQIWTIHVL
414	Q9Y4K1	>sp|Q9Y4K1|AIM1_HUMAN Absent in melanoma 1 protein GN=AIM1 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MEKRSSGRRSGRRRGSQKSTDSPGADAELPESAARDDAVFDDEVAPNAASDNASAEKKVKSPRAALDGGVASAASPESKPSPGTKGQLRGESDRSKQPPPASSPTKRKGRSRALEAVPAPPASGPRAPAKESPPKRVPDPSPVTKGTAAESGEEAARAIPRELPVKSSSLLPEIKPEHKRGPLPNHFNGRAEGGRSRELGRAAGAPGASDADGLKPRNHFGVGRSTVTTKVTLPAKPKHVELNLKTPKNLDSLGNEHNPFSQPVHKGNTATKISLFENKRTNSSPRHTDIRGQRNTPASSKTFVGRAKLNLAKKAKEMEQPEKKVMPNSPQNGVLVKETAIETKVTVSEEEILPATRGMNGDSSENQALGPQPNQDDKADVQTDAGCLSEPVASALIPVKDHKLLEKEDSEAADSKSLVLENVTDTAQDIPTTVDTKDLPPTAMPKPQHTFSDSQSPAESSPGPSLSLSAPAPGDVPKDTCVQSPISSFPCTDLKVSENHKGCVLPVSRQNNEKMPLLELGGETTPPLSTERSPEAVGSECPSRVLVQVRSFVLPVESTQDVSSQVIPESSEVREVQLPTCHSNEPEVVSVASCAPPQEEVLGNEHSHCTAELAAKSGPQVIPPASEKTLPIQAQSQGSRTPLMAESSPTNSPSSGNHLATPQRPDQTVTNGQDSPASLLNISAGSDDSVFDSSSDMEKFTEIIKQMDSAVCMPMKRKKARMPNSPAPHFAMPPIHEDHLEKVFDPKVFTFGLGKKKESQPEMSPALHLMQNLDTKSKLRPKRASAEQSVLFKSLHTNTNGNSEPLVMPEINDKENRDVTNGGIKRSRLEKSALFSSLLSSLPQDKIFSPSVTSVNTMTTAFSTSQNGSLSQSSVSQPTTEGAPPCGLNKEQSNLLPDNSLKVFNFNSSSTSHSSLKSPSHMEKYPQKEKTKEDLDSRSNLHLPETKFSELSKLKNDDMEKANHIESVIKSNLPNCANSDTDFMGLFKSSRYDPSISFSGMSLSDTMTLRGSVQNKLNPRPGKVVIYSEPDVSEKCIEVFSDIQDCSSWSLSPVILIKVVRGCWILYEQPNFEGHSIPLEEGELELSGLWGIEDILERHEEAESDKPVVIGSIRHVVQDYRVSHIDLFTEPEGLGILSSYFDDTEEMQGFGVMQKTCSMKVHWGTWLIYEEPGFQGVPFILEPGEYPDLSFWDTEEAYIGSMRPLKMGGRKVEFPTDPKVVVYEKPFFEGKCVELETGMCSFVMEGGETEEATGDDHLPFTSVGSMKVLRGIWVAYEKPGFTGHQYLLEEGEYRDWKAWGGYNGELQSLRPILGDFSNAHMIMYSEKNFGSKGSSIDVLGIVANLKETGYGVKTQSINVLSGVWVAYENPDFTGEQYILDKGFYTSFEDWGGKNCKISSVQPICLDSFTGPRRRNQIHLFSEPQFQGHSQSFEETTSQIDDSFSTKSCRVSGGSWVVYDGENFTGNQYVLEEGHYPCLSAMGCPPGATFKSLRFIDVEFSEPTIILFEREDFKGKKIELNAETVNLRSLGFNTQIRSVQVIGGIWVTYEYGSYRGRQFLLSPAEVPNWYEFSGCRQIGSLRPFVQKRIYFRLRNKATGLFMSTNGNLEDLKLLRIQVMEDVGADDQIWIYQEGCIKCRIAEDCCLTIVGSLVTSGSKLGLALDQNADSQFWSLKSDGRIYSKLKPNLVLDIKGGTQYDQNHIILNTVSKEKFTQVWEAMVLYT
425	P08173	>sp|P08173|ACM4_HUMAN Muscarinic acetylcholine receptor M4 GN=CHRM4 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MANFTPVNGSSGNQSVRLVTSSSHNRYETVEMVFIATVTGSLSLVTVVGNILVMLSIKVNRQLQTVNNYFLFSLACADLIIGAFSMNLYTVYIIKGYWPLGAVVCDLWLALDYVVSNASVMNLLIISFDRYFCVTKPLTYPARRTTKMAGLMIAAAWVLSFVLWAPAILFWQFVVGKRTVPDNQCFIQFLSNPAVTFGTAIAAFYLPVVIMTVLYIHISLASRSRVHKHRPEGPKEKKAKTLAFLKSPLMKQSVKKPPPGEAAREELRNGKLEEAPPPALPPPPRPVADKDTSNESSSGSATQNTKERPATELSTTEATTPAMPAPPLQPRALNPASRWSKIQIVTKQTGNECVTAIEIVPATPAGMRPAANVARKFASIARNQVRKKRQMAARERKVTRTIFAILLAFILTWTPYNVMVLVNTFCQSCIPDTVWSIGYWLCYVNSTINPACYALCNATFKKTFRHLLLCQYRNIGTAR
415	Q6JQN1	>sp|Q6JQN1|ACD10_HUMAN Acyl-CoA dehydrogenase family member 10 GN=ACAD10 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MCVRSCFQSPRLQWVWRTAFLKHTQRRHQGSHRWTHLGGSTYRAVIFDMGGVLIPSPGRVAAEWEVQNRIPSGTILKALMEGGENGPWMRFMRAEITAEGFLREFGRLCSEMLKTSVPVDSFFSLLTSERVAKQFPVMTEAITQIRAKGLQTAVLSNNFYLPNQKSFLPLDRKQFDVIVESCMEGICKPDPRIYKLCLEQLGLQPSESIFLDDLGTNLKEAARLGIHTIKVNDPETAVKELEALLGFTLRVGVPNTRPVKKTMEIPKDSLQKYLKDLLGIQTTGPLELLQFDHGQSNPTYYIRLANRDLVLRKKPPGTLLPSAHAIEREFRIMKALANAGVPVPNVLDLCEDSSVIGTPFYVMEYCPGLIYKDPSLPGLEPSHRRAIYTAMNTVLCKIHSVDLQAVGLEDYGKQGDYIPRQVRTWVKQYRASETSTIPAMERLIEWLPLHLPRQQRTTVVHGDFRLDNLVFHPEEPEVLAVLDWELSTLGDPLADVAYSCLAHYLPSSFPVLRGINDCDLTQLGIPAAEEYFRMYCLQMGLPPTENWNFYMAFSFFRVAAILQGVYKRSLTGQASSTYAEQTGKLTEFVSNLAWDFAVKEGFRVFKEMPFTNPLTRSYHTWARPQSQWCPTGSRSYSSVPEASPAHTSRGGLVISPESLSPPVRELYHRLKHFMEQRVYPAEPELQSHQASAARWSPSPLIEDLKEKAKAEGLWNLFLPLEADPEKKYGAGLTNVEYAHLCELMGTSLYAPEVCNCSAPDTGNMELLVRYGTEAQKARWLIPLLEGKARSCFAMTEPQVASSDATNIEASIREEDSFYVINGHKWWITGILDPRCQLCVFMGKTDPHAPRHRQQSVLLVPMDTPGIKIIRPLTVYGLEDAPGGHGEVRFEHVRVPKENMVLGPGRGFEIAQGRLGPGRIHHCMRLIGFSERALALMKARVKSRLAFGKPLVEQGTVLADIAQSRVEIEQARLLVLRAAHLMDLAGNKAAALDIAMIKMVAPSMASRVIDRAIQAFGAAGLSSDYPLAQFFTWARALRFADGPDEVHRATVAKLELKHRI
416	P22303	>sp|P22303|ACES_HUMAN Acetylcholinesterase GN=ACHE PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRPPQCLLHTPSLASPLLLLLLWLLGGGVGAEGREDAELLVTVRGGRLRGIRLKTPGGPVSAFLGIPFAEPPMGPRRFLPPEPKQPWSGVVDATTFQSVCYQYVDTLYPGFEGTEMWNPNRELSEDCLYLNVWTPYPRPTSPTPVLVWIYGGGFYSGASSLDVYDGRFLVQAERTVLVSMNYRVGAFGFLALPGSREAPGNVGLLDQRLALQWVQENVAAFGGDPTSVTLFGESAGAASVGMHLLSPPSRGLFHRAVLQSGAPNGPWATVGMGEARRRATQLAHLVGCPPGGTGGNDTELVACLRTRPAQVLVNHEWHVLPQESVFRFSFVPVVDGDFLSDTPEALINAGDFHGLQVLVGVVKDEGSYFLVYGAPGFSKDNESLISRAEFLAGVRVGVPQVSDLAAEAVVLHYTDWLHPEDPARLREALSDVVGDHNVVCPVAQLAGRLAAQGARVYAYVFEHRASTLSWPLWMGVPHGYEIEFIFGIPLDPSRNYTAEEKIFAQRLMRYWANFARTGDPNEPRDPKAPQWPPYTAGAQQYVSLDLRPLEVRRGLRAQACAFWNRFLPKLLSATDTLDEAERQWKAEFHRWSSYMVHWKNQFDHYSKQDRCSDL
417	Q9GZZ6	>sp|Q9GZZ6|ACH10_HUMAN Neuronal acetylcholine receptor subunit alpha-10 GN=CHRNA10 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MGLRSHHLSLGLLLLFLLPAECLGAEGRLALKLFRDLFANYTSALRPVADTDQTLNVTLEVTLSQIIDMDERNQVLTLYLWIRQEWTDAYLRWDPNAYGGLDAIRIPSSLVWRPDIVLYNKADAQPPGSASTNVVLRHDGAVRWDAPAITRSSCRVDVAAFPFDAQHCGLTFGSWTHGGHQLDVRPRGAAASLADFVENVEWRVLGMPARRRVLTYGCCSEPYPDVTFTLLLRRRAAAYVCNLLLPCVLISLLAPLAFHLPADSGEKVSLGVTVLLALTVFQLLLAESMPPAESVPLIGKYYMATMTMVTFSTALTILIMNLHYCGPSVRPVPAWARALLLGHLARGLCVRERGEPCGQSRPPELSPSPQSPEGGAGPPAGPCHEPRCLCRQEALLHHVATIANTFRSHRAAQRCHEDWKRLARVMDRFFLAIFFSMALVMSLLVLVQAL
418	P02708	>sp|P02708|ACHA_HUMAN Acetylcholine receptor subunit alpha GN=CHRNA1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MEPWPLLLLFSLCSAGLVLGSEHETRLVAKLFKDYSSVVRPVEDHRQVVEVTVGLQLIQLINVDEVNQIVTTNVRLKQGDMVDLPRPSCVTLGVPLFSHLQNEQWVDYNLKWNPDDYGGVKKIHIPSEKIWRPDLVLYNNADGDFAIVKFTKVLLQYTGHITWTPPAIFKSYCEIIVTHFPFDEQNCSMKLGTWTYDGSVVAINPESDQPDLSNFMESGEWVIKESRGWKHSVTYSCCPDTPYLDITYHFVMQRLPLYFIVNVIIPCLLFSFLTGLVFYLPTDSGEKMTLSISVLLSLTVFLLVIVELIPSTSSAVPLIGKYMLFTMVFVIASIIITVIVINTHHRSPSTHVMPNWVRKVFIDTIPNIMFFSTMKRPSREKQDKKIFTEDIDISDISGKPGPPPMGFHSPLIKHPEVKSAIEGIKYIAETMKSDQESNNAAAEWKYVAMVMDHILLGVFMLVCIIGTLAVFAGRLIELNQQG
419	P11230	>sp|P11230|ACHB_HUMAN Acetylcholine receptor subunit beta GN=CHRNB1 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MTPGALLMLLGALGAPLAPGVRGSEAEGRLREKLFSGYDSSVRPAREVGDRVRVSVGLILAQLISLNEKDEEMSTKVYLDLEWTDYRLSWDPAEHDGIDSLRITAESVWLPDVVLLNNNDGNFDVALDISVVVSSDGSVRWQPPGIYRSSCSIQVTYFPFDWQNCTMVFSSYSYDSSEVSLQTGLGPDGQGHQEIHIHEGTFIENGQWEIIHKPSRLIQPPGDPRGGREGQRQEVIFYLIIRRKPLFYLVNVIAPCILITLLAIFVFYLPPDAGEKMGLSIFALLTLTVFLLLLADKVPETSLSVPIIIKYLMFTMVLVTFSVILSVVVLNLHHRSPHTHQMPLWVRQIFIHKLPLYLRLKRPKPERDLMPEPPHCSSPGSGWGRGTDEYFIRKPPSDFLFPKPNRFQPELSAPDLRRFIDGPNRAVALLPELREVVSSISYIARQLQEQEDHDALKEDWQFVAMVVDRLFLWTFIIFTSVGTLVIFLDATYHLPPPDPFP
420	P07510	>sp|P07510|ACHG_HUMAN Acetylcholine receptor subunit gamma GN=CHRNG PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MHGGQGPLLLLLLLAVCLGAQGRNQEERLLADLMQNYDPNLRPAERDSDVVNVSLKLTLTNLISLNEREEALTTNVWIEMQWCDYRLRWDPRDYEGLWVLRVPSTMVWRPDIVLENNVDGVFEVALYCNVLVSPDGCIYWLPPAIFRSACSISVTYFPFDWQNCSLIFQSQTYSTNEIDLQLSQEDGQTIEWIFIDPEAFTENGEWAIQHRPAKMLLDPAAPAQEAGHQKVVFYLLIQRKPLFYVINIIAPCVLISSVAILIHFLPAKAGGQKCTVAINVLLAQTVFLFLVAKKVPETSQAVPLISKYLTFLLVVTILIVVNAVVVLNVSLRSPHTHSMARGVRKVFLRLLPQLLRMHVRPLAPAAVQDTQSRLQNGSSGWSITTGEEVALCLPRSELLFQQWQRQGLVAAALEKLEKGPELGLSQFCGSLKQAAPAIQACVEACNLIACARHQQSHFDNGNEEWFLVGRVLDRVCFLAMLSLFICGTAGIFLMAHYNRVPALPFPGDPRPYLPSPD
421	O00590	>sp|O00590|ACKR2_HUMAN Atypical chemokine receptor 2 GN=ACKR2 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAATASPQPLATEDADSENSSFYYYDYLDEVAFMLCRKDAVVSFGKVFLPVFYSLIFVLGLSGNLLLLMVLLRYVPRRRMVEIYLLNLAISNLLFLVTLPFWGISVAWHWVFGSFLCKMVSTLYTINFYSGIFFISCMSLDKYLEIVHAQPYHRLRTRAKSLLLATIVWAVSLAVSIPDMVFVQTHENPKGVWNCHADFGGHGTIWKLFLRFQQNLLGFLLPLLAMIFFYSRIGCVLVRLRPAGQGRALKIAAALVVAFFVLWFPYNLTLFLHTLLDLQVFGNCEVSQHLDYALQVTESIAFLHCCFSPILYAFSSHRFRQYLKAFLAAVLGWHLAPGTAQASLSSCSESSILTAQEEMTGMNDLGERQSENYPNKEDVGNKSA
422	O94805	>sp|O94805|ACL6B_HUMAN Actin-like protein 6B GN=ACTL6B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MSGGVYGGDEVGALVFDIGSFSVRAGYAGEDCPKADFPTTVGLLAAEEGGGLELEGDKEKKGKIFHIDTNALHVPRDGAEVMSPLKNGMIEDWECFRAILDHTYSKHVKSEPNLHPVLMSEAPWNTRAKREKLTELMFEQYNIPAFFLCKTAVLTAFANGRSTGLVLDSGATHTTAIPVHDGYVLQQGIVKSPLAGDFISMQCRELFQEMAIDIIPPYMIAAKEPVREGAPPNWKKKEKLPQVSKSWHNYMCNEVIQDFQASVLQVSDSPYDEQVAAQMPTVHYEMPNGYNTDYGAERLRIPEGLFDPSNVKGLSGNTMLGVGHVVTTSIGMCDIDIRPGLYGSVIVTGGNTLLQGFTDRLNRELSQKTPPSMRLKLIASNSTMERKFSPWIGGSILASLGTFQQMWISKQEYEEGGKQCVERKCP
423	P53396	>sp|P53396|ACLY_HUMAN ATP-citrate synthase GN=ACLY PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MSAKAISEQTGKELLYKFICTTSAIQNRFKYARVTPDTDWARLLQDHPWLLSQNLVVKPDQLIKRRGKLGLVGVNLTLDGVKSWLKPRLGQEATVGKATGFLKNFLIEPFVPHSQAEEFYVCIYATREGDYVLFHHEGGVDVGDVDAKAQKLLVGVDEKLNPEDIKKHLLVHAPEDKKEILASFISGLFNFYEDLYFTYLEINPLVVTKDGVYVLDLAAKVDATADYICKVKWGDIEFPPPFGREAYPEEAYIADLDAKSGASLKLTLLNPKGRIWTMVAGGGASVVYSDTICDLGGVNELANYGEYSGAPSEQQTYDYAKTILSLMTREKHPDGKILIIGGSIANFTNVAATFKGIVRAIRDYQGPLKEHEVTIFVRRGGPNYQEGLRVMGEVGKTTGIPIHVFGTETHMTAIVGMALGHRPIPNQPPTAAHTANFLLNASGSTSTPAPSRTASFSESRADEVAPAKKAKPAMPQDSVPSPRSLQGKSTTLFSRHTKAIVWGMQTRAVQGMLDFDYVCSRDEPSVAAMVYPFTGDHKQKFYWGHKEILIPVFKNMADAMRKHPEVDVLINFASLRSAYDSTMETMNYAQIRTIAIIAEGIPEALTRKLIKKADQKGVTIIGPATVGGIKPGCFKIGNTGGMLDNILASKLYRPGSVAYVSRSGGMSNELNNIISRTTDGVYEGVAIGGDRYPGSTFMDHVLRYQDTPGVKMIVVLGEIGGTEEYKICRGIKEGRLTKPIVCWCIGTCATMFSSEVQFGHAGACANQASETAVAKNQALKEAGVFVPRSFDELGEIIQSVYEDLVANGVIVPAQEVPPPTVPMDYSWARELGLIRKPASFMTSICDERGQELIYAGMPITEVFKEEMGIGGVLGLLWFQKRLPKYSCQFIEMCLMVTADHGPAVSGAHNTIICARAGKDLVSSLTSGLLTIGDRFGGALDAAAKMFSKAFDSGIIPMEFVNKMKKEGKLIMGIGHRVKSINNPDMRVQILKDYVRQHFPATPLLDYALEVEKITTSKKPNLILNVDGLIGVAFVDMLRNCGSFTREEADEYIDIGALNGIFVLGRSMGFIGHYLDQKRLKQGLYRHPWDDISYVLPEHMSM
424	P11229	>sp|P11229|ACM1_HUMAN Muscarinic acetylcholine receptor M1 GN=CHRM1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MNTSAPPAVSPNITVLAPGKGPWQVAFIGITTGLLSLATVTGNLLVLISFKVNTELKTVNNYFLLSLACADLIIGTFSMNLYTTYLLMGHWALGTLACDLWLALDYVASNASVMNLLLISFDRYFSVTRPLSYRAKRTPRRAALMIGLAWLVSFVLWAPAILFWQYLVGERTVLAGQCYIQFLSQPIITFGTAMAAFYLPVTVMCTLYWRIYRETENRARELAALQGSETPGKGGGSSSSSERSQPGAEGSPETPPGRCCRCCRAPRLLQAYSWKEEEEEDEGSMESLTSSEGEEPGSEVVIKMPMVDPEAQAPTKQPPRSSPNTVKRPTKKGRDRAGKGQKPRGKEQLAKRKTFSLVKEKKAARTLSAILLAFILTWTPYNIMVLVSTFCKDCVPETLWELGYWLCYVNSTINPMCYALCNKAFRDTFRLLLLCRWDKRRWRKIPKRPGSVHRTPSRQC
426	Q8TDX5	>sp|Q8TDX5|ACMSD_HUMAN 2-amino-3-carboxymuconate-6-semialdehyde decarboxylase GN=ACMSD PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MKIDIHSHILPKEWPDLKKRFGYGGWVQLQHHSKGEAKLLKDGKVFRVVRENCWDPEVRIREMDQKGVTVQALSTVPVMFSYWAKPEDTLNLCQLLNNDLASTVVSYPRRFVGLGTLPMQAPELAVKEMERCVKELGFPGVQIGTHVNEWDLNAQELFPVYAAAERLKCSLFVHPWDMQMDGRMAKYWLPWLVGMPAETTIAICSMIMGGVFEKFPKLKVCFAHGGGAFPFTVGRISHGFSMRPDLCAQDNPMNPKKYLGSFYTDALVHDPLSLKLLTDVIGKDKVILGTDYPFPLGELEPGKLIESMEEFDEETKNKLKAGNALAFLGLERKQFE
429	Q8NEB7	>sp|Q8NEB7|ACRBP_HUMAN Acrosin-binding protein GN=ACRBP PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRKPAAGFLPSLLKVLLLPLAPAAAQDSTQASTPGSPLSPTEYERFFALLTPTWKAETTCRLRATHGCRNPTLVQLDQYENHGLVPDGAVCSNLPYASWFESFCQFTHYRCSNHVYYAKRVLCSQPVSILSPNTLKEIEASAEVSPTTMTSPISPHFTVTERQTFQPWPERLSNNVEELLQSSLSLGGQEQAPEHKQEQGVEHRQEPTQEHKQEEGQKQEEQEEEQEEEGKQEEGQGTKEGREAVSQLQTDSEPKFHSESLSSNPSSFAPRVREVESTPMIMENIQELIRSAQEIDEMNEIYDENSYWRNQNPGSLLQLPHTEALLVLCYSIVENTCIITPTAKAWKYMEEEILGFGKSVCDSLGRRHMSTCALCDFCSLKLEQCHSEASLQRQQCDTSHKTPFVSPLLASQSLSIGNQVGSPESGRFYGLDLYGGLHMDFWCARLATKGCEDVRVSGWLQTEFLSFQDGDFPTKICDTDYIQYPNYCSFKSQQCLMRNRNRKVSRMRCLQNETYSALSPGKSEDVVLRWSQEFSTLTLGQFG
430	Q9NR19	>sp|Q9NR19|ACSA_HUMAN Acetyl-coenzyme A synthetase, cytoplasmic GN=ACSS2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MGLPEERVRSGSGSRGQEEAGAGGRARSWSPPPEVSRSAHVPSLQRYRELHRRSVEEPREFWGDIAKEFYWKTPCPGPFLRYNFDVTKGKIFIEWMKGATTNICYNVLDRNVHEKKLGDKVAFYWEGNEPGETTQITYHQLLVQVCQFSNVLRKQGIQKGDRVAIYMPMIPELVVAMLACARIGALHSIVFAGFSSESLCERILDSSCSLLITTDAFYRGEKLVNLKELADEALQKCQEKGFPVRCCIVVKHLGRAELGMGDSTSQSPPIKRSCPDVQISWNQGIDLWWHELMQEAGDECEPEWCDAEDPLFILYTSGSTGKPKGVVHTVGGYMLYVATTFKYVFDFHAEDVFWCTADIGWITGHSYVTYGPLANGATSVLFEGIPTYPDVNRLWSIVDKYKVTKFYTAPTAIRLLMKFGDEPVTKHSRASLQVLGTVGEPINPEAWLWYHRVVGAQRCPIVDTFWQTETGGHMLTPLPGATPMKPGSATFPFFGVAPAILNESGEELEGEAEGYLVFKQPWPGIMRTVYGNHERFETTYFKKFPGYYVTGDGCQRDQDGYYWITGRIDDMLNVSGHLLSTAEVESALVEHEAVAEAAVVGHPHPVKGECLYCFVTLCDGHTFSPKLTEELKKQIREKIGPIATPDYIQNAPGLPKTRSGKIMRRVLRKIAQNDHDLGDMSTVADPSVISHLFSHRCLTIQ
431	Q96CM8	>sp|Q96CM8|ACSF2_HUMAN Acyl-CoA synthetase family member 2, mitochondrial GN=ACSF2 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAVYVGMLRLGRLCAGSSGVLGARAALSRSWQEARLQGVRFLSSREVDRMVSTPIGGLSYVQGCTKKHLNSKTVGQCLETTAQRVPEREALVVLHEDVRLTFAQLKEEVDKAASGLLSIGLCKGDRLGMWGPNSYAWVLMQLATAQAGIILVSVNPAYQAMELEYVLKKVGCKALVFPKQFKTQQYYNVLKQICPEVENAQPGALKSQRLPDLTTVISVDAPLPGTLLLDEVVAAGSTRQHLDQLQYNQQFLSCHDPINIQFTSGTTGSPKGATLSHYNIVNNSNILGERLKLHEKTPEQLRMILPNPLYHCLGSVAGTMMCLMYGATLILASPIFNGKKALEAISRERGTFLYGTPTMFVDILNQPDFSSYDISTMCGGVIAGSPAPPELIRAIINKINMKDLVVAYGTTENSPVTFAHFPEDTVEQKAESVGRIMPHTEARIMNMEAGTLAKLNTPGELCIRGYCVMLGYWGEPQKTEEAVDQDKWYWTGDVATMNEQGFCKIVGRSKDMIIRGGENIYPAELEDFFHTHPKVQEVQVVGVKDDRMGEEICACIRLKDGEETTVEEIKAFCKGKISHFKIPKYIVFVTNYPLTISGKIQKFKLREQMERHLNL
432	Q9UKU0	>sp|Q9UKU0|ACSL6_HUMAN Long-chain-fatty-acid--CoA ligase 6 GN=ACSL6 PE=2 SV=4 Homo sapiens OS=Human NCBI_TaxID=9606	MQTQEILRILRLPELGDLGQFFRSLSATTLVSMGALAAILAYWFTHRPKALQPPCNLLMQSEEVEDSGGARRSVIGSGPQLLTHYYDDARTMYQVFRRGLSISGNGPCLGFRKPKQPYQWLSYQEVADRAEFLGSGLLQHNCKACTDQFIGVFAQNRPEWIIVELACYTYSMVVVPLYDTLGPGAIRYIINTADISTVIVDKPQKAVLLLEHVERKETPGLKLIILMDPFEEALKERGQKCGVVIKSMQAVEDCGQENHQAPVPPQPDDLSIVCFTSGTTGNPKGAMLTHGNVVADFSGFLKVTEKVIFPRQDDVLISFLPLAHMFERVIQSVVYCHGGRVGFFQGDIRLLSDDMKALCPTIFPVVPRLLNRMYDKIFSQANTPLKRWLLEFAAKRKQAEVRSGIIRNDSIWDELFFNKIQASLGGCVRMIVTGAAPASPTVLGFLRAALGCQVYEGYGQTECTAGCTFTTPGDWTSGHVGAPLPCNHIKLVDVEELNYWACKGEGEICVRGPNVFKGYLKDPDRTKEALDSDGWLHTGDIGKWLPAGTLKIIDRKKHIFKLAQGEYVAPEKIENIYIRSQPVAQIYVHGDSLKAFLVGIVVPDPEVMPSWAQKRGIEGTYADLCTNKDLKKAILEDMVRLGKESGLHSFEQVKAIHIHSDMFSVQNGLLTPTLKAKRPELREYFKKQIEELYSISM
433	Q08AH1	>sp|Q08AH1|ACSM1_HUMAN Acyl-coenzyme A synthetase ACSM1, mitochondrial GN=ACSM1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MQWLMRFRTLWGIHKSFHNIHPAPSQLRCRSLSEFGAPRWNDYEVPEEFNFASYVLDYWAQKEKEGKRGPNPAFWWVNGQGDEVKWSFREMGDLTRRVANVFTQTCGLQQGDHLALMLPRVPEWWLVAVGCMRTGIIFIPATILLKAKDILYRLQLSKAKGIVTIDALASEVDSIASQCPSLKTKLLVSDHSREGWLDFRSLVKSASPEHTCVKSKTLDPMVIFFTSGTTGFPKMAKHSHGLALQPSFPGSRKLRSLKTSDVSWCLSDSGWIVATIWTLVEPWTAGCTVFIHHLPQFDTKVIIQTLLKYPINHFWGVSSIYRMILQQDFTSIRFPALEHCYTGGEVVLPKDQEEWKRRTGLLLYENYGQSETGLICATYWGMKIKPGFMGKATPPYDVQVIDDKGSILPPNTEGNIGIRIKPVRPVSLFMCYEGDPEKTAKVECGDFYNTGDRGKMDEEGYICFLGRSDDIINASGYRIGPAEVESALVEHPAVAESAVVGSPDPIRGEVVKAFIVLTPQFLSHDKDQLTKELQQHVKSVTAPYKYPRKVEFVSELPKTITGKIERKELRKKETGQM
434	P0C7M7	>sp|P0C7M7|ACSM4_HUMAN Acyl-coenzyme A synthetase ACSM4, mitochondrial GN=ACSM4 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MKIFFRYQTFRFIWLTKPPGRRLHKDHQLWTPLTLADFEAINRCNRPLPKNFNFAADVLDQWSQKEKTGERPANPALWWVNGKGDEVKWSFRELGSLSRKAANVLTKPCGLQRGDRLAVILPRIPEWWLVNVACIRTGIIFMPGTIQLTAKDILYRLRASKAKCIVASEEVAPAVESIVLECPDLKTKLLVSPQSWNGWLSFQELFQFASEEHSCVETGSQEPMTIYFTSGTTGFPKMAQHSQSSLGIGFTLCGRYWLDLKSSDIIWNMSDTGWVKAAIGSVFSSWLCGACVFVHRMAQFDTDTFLDTLTTYPITTLCSPPTVYRMLVQKDLKRYKFKSLRHCLTGGEPLNPEVLEQWRVQTGLELYEGYGQTEVGMICANQKGQEIKPGSMGKGMLPYDVQIIDENGNVLPPGKEGEIALRLKPTRPFCFFSKYVDNPQKTAATIRGDFYVTGDRGVMDSDGYFWFVGRADDVIISSGYRIGPFEVESALIEHPAVVESAVVSSPDQIRGEVVKAFVVLAAPFKSYNPEKLTLELQDHVKKSTAPYKYPRKVEFVQELPKTITGKIKRNVLRDQEWRGR
435	Q9H6R3	>sp|Q9H6R3|ACSS3_HUMAN Acyl-CoA synthetase short-chain family member 3, mitochondrial GN=ACSS3 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MKPSWLQCRKVTSAGGLGGPLPGSSPARGAGAALRALVVPGPRGGLGGRGCRALSSGSGSEYKTHFAASVTDPERFWGKAAEQISWYKPWTKTLENKHSPSTRWFVEGMLNICYNAVDRHIENGKGDKIAIIYDSPVTNTKATFTYKEVLEQVSKLAGVLVKHGIKKGDTVVIYMPMIPQAMYTMLACARIGAIHSLIFGGFASKELSSRIDHVKPKVVVTASFGIEPGRRVEYVPLVEEALKIGQHKPDKILIYNRPNMEAVPLAPGRDLDWDEEMAKAQSHDCVPVLSEHPLYILYTSGTTGLPKGVIRPTGGYAVMLHWSMSSIYGLQPGEVWWAASDLGWVVGHSYICYGPLLHGNTTVLYEGKPVGTPDAGAYFRVLAEHGVAALFTAPTAIRAIRQQDPGAALGKQYSLTRFKTLFVAGERCDVETLEWSKNVFRVPVLDHWWQTETGSPITASCVGLGNSKTPPPGQAGKSVPGYNVMILDDNMQKLKARCLGNIVVKLPLPPGAFSGLWKNQEAFKHLYFEKFPGYYDTMDAGYMDEEGYLYVMSRVDDVINVAGHRISAGAIEESILSHGTVADCAVVGKEDPLKGHVPLALCVLRKDINATEEQVLEEIVKHVRQNIGPVAAFRNAVFVKQLPKTRSGKIPRSALSAIVNGKPYKITSTIEDPSIFGHVEEMLKQA
436	P63261	>sp|P63261|ACTG_HUMAN Actin, cytoplasmic 2 GN=ACTG1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MEEEIAALVIDNGSGMCKAGFAGDDAPRAVFPSIVGRPRHQGVMVGMGQKDSYVGDEAQSKRGILTLKYPIEHGIVTNWDDMEKIWHHTFYNELRVAPEEHPVLLTEAPLNPKANREKMTQIMFETFNTPAMYVAIQAVLSLYASGRTTGIVMDSGDGVTHTVPIYEGYALPHAILRLDLAGRDLTDYLMKILTERGYSFTTTAEREIVRDIKEKLCYVALDFEQEMATAASSSSLEKSYELPDGQVITIGNERFRCPEALFQPSFLGMESCGIHETTFNSIMKCDVDIRKDLYANTVLSGGTTMYPGIADRMQKEITALAPSTMKIKIIAPPERKYSVWIGGSILASLSTFQQMWISKQEYDESGPSIVHRKCF
437	P42025	>sp|P42025|ACTY_HUMAN Beta-centractin GN=ACTR1B PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MESYDIIANQPVVIDNGSGVIKAGFAGDQIPKYCFPNYVGRPKHMRVMAGALEGDLFIGPKAEEHRGLLTIRYPMEHGVVRDWNDMERIWQYVYSKDQLQTFSEEHPVLLTEAPLNPSKNREKAAEVFFETFNVPALFISMQAVLSLYATGRTTGVVLDSGDGVTHAVPIYEGFAMPHSIMRVDIAGRDVSRYLRLLLRKEGVDFHTSAEFEVVRTIKERACYLSINPQKDEALETEKVQYTLPDGSTLDVGPARFRAPELLFQPDLVGDESEGLHEVVAFAIHKSDMDLRRTLFANIVLSGGSTLFKGFGDRLLSEVKKLAPKDIKIKISAPQERLYSTWIGGSILASLDTFKKMWVSKKEYEEDGSRAIHRKTF
438	P61163	>sp|P61163|ACTZ_HUMAN Alpha-centractin GN=ACTR1A PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MESYDVIANQPVVIDNGSGVIKAGFAGDQIPKYCFPNYVGRPKHVRVMAGALEGDIFIGPKAEEHRGLLSIRYPMEHGIVKDWNDMERIWQYVYSKDQLQTFSEEHPVLLTEAPLNPRKNRERAAEVFFETFNVPALFISMQAVLSLYATGRTTGVVLDSGDGVTHAVPIYEGFAMPHSIMRIDIAGRDVSRFLRLYLRKEGYDFHSSSEFEIVKAIKERACYLSINPQKDETLETEKAQYYLPDGSTIEIGPSRFRAPELLFRPDLIGEESEGIHEVLVFAIQKSDMDLRRTLFSNIVLSGGSTLFKGFGDRLLSEVKKLAPKDVKIRISAPQERLYSTWIGGSILASLDTFKKMWVSKKEYEEDGARSIHRKTF
439	P37023	>sp|P37023|ACVL1_HUMAN Serine/threonine-protein kinase receptor R3 GN=ACVRL1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MTLGSPRKGLLMLLMALVTQGDPVKPSRGPLVTCTCESPHCKGPTCRGAWCTVVLVREEGRHPQEHRGCGNLHRELCRGRPTEFVNHYCCDSHLCNHNVSLVLEATQPPSEQPGTDGQLALILGPVLALLALVALGVLGLWHVRRRQEKQRGLHSELGESSLILKASEQGDSMLGDLLDSDCTTGSGSGLPFLVQRTVARQVALVECVGKGRYGEVWRGLWHGESVAVKIFSSRDEQSWFRETEIYNTVLLRHDNILGFIASDMTSRNSSTQLWLITHYHEHGSLYDFLQRQTLEPHLALRLAVSAACGLAHLHVEIFGTQGKPAIAHRDFKSRNVLVKSNLQCCIADLGLAVMHSQGSDYLDIGNNPRVGTKRYMAPEVLDEQIRTDCFESYKWTDIWAFGLVLWEIARRTIVNGIVEDYRPPFYDVVPNDPSFEDMKKVVCVDQQTPTIPNRLAADPVLSGLAQMMRECWYPNPSARLTALRIKKTLQKISNSPEKPKVIQ
440	O14672	>sp|O14672|ADA10_HUMAN Disintegrin and metalloproteinase domain-containing protein 10 GN=ADAM10 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MVLLRVLILLLSWAAGMGGQYGNPLNKYIRHYEGLSYNVDSLHQKHQRAKRAVSHEDQFLRLDFHAHGRHFNLRMKRDTSLFSDEFKVETSNKVLDYDTSHIYTGHIYGEEGSFSHGSVIDGRFEGFIQTRGGTFYVEPAERYIKDRTLPFHSVIYHEDDINYPHKYGPQGGCADHSVFERMRKYQMTGVEEVTQIPQEEHAANGPELLRKKRTTSAEKNTCQLYIQTDHLFFKYYGTREAVIAQISSHVKAIDTIYQTTDFSGIRNISFMVKRIRINTTADEKDPTNPFRFPNIGVEKFLELNSEQNHDDYCLAYVFTDRDFDDGVLGLAWVGAPSGSSGGICEKSKLYSDGKKKSLNTGIITVQNYGSHVPPKVSHITFAHEVGHNFGSPHDSGTECTPGESKNLGQKENGNYIMYARATSGDKLNNNKFSLCSIRNISQVLEKKRNNCFVESGQPICGNGMVEQGEECDCGYSDQCKDECCFDANQPEGRKCKLKPGKQCSPSQGPCCTAQCAFKSKSEKCRDDSDCAREGICNGFTALCPASDPKPNFTDCNRHTQVCINGQCAGSICEKYGLEECTCASSDGKDDKELCHVCCMKKMDPSTCASTGSVQWSRHFSGRTITLQPGSPCNDFRGYCDVFMRCRLVDADGPLARLKKAIFSPELYENIAEWIVAHWWAVLLMGIALIMLMAGFIKICSVHTPSSNPKLPPPKPLPGTLKRRRPPQPIQQPQRQRPRESYQMGHMRR
441	O43184	>sp|O43184|ADA12_HUMAN Disintegrin and metalloproteinase domain-containing protein 12 GN=ADAM12 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MAARPLPVSPARALLLALAGALLAPCEARGVSLWNQGRADEVVSASVGSGDLWIPVKSFDSKNHPEVLNIRLQRESKELIINLERNEGLIASSFTETHYLQDGTDVSLARNYTVILGHCYYHGHVRGYSDSAVSLSTCSGLRGLIVFENESYVLEPMKSATNRYKLFPAKKLKSVRGSCGSHHNTPNLAAKNVFPPPSQTWARRHKRETLKATKYVELVIVADNREFQRQGKDLEKVKQRLIEIANHVDKFYRPLNIRIVLVGVEVWNDMDKCSVSQDPFTSLHEFLDWRKMKLLPRKSHDNAQLVSGVYFQGTTIGMAPIMSMCTADQSGGIVMDHSDNPLGAAVTLAHELGHNFGMNHDTLDRGCSCQMAVEKGGCIMNASTGYPFPMVFSSCSRKDLETSLEKGMGVCLFNLPEVRESFGGQKCGNRFVEEGEECDCGEPEECMNRCCNATTCTLKPDAVCAHGLCCEDCQLKPAGTACRDSSNSCDLPEFCTGASPHCPANVYLHDGHSCQDVDGYCYNGICQTHEQQCVTLWGPGAKPAPGICFERVNSAGDPYGNCGKVSKSSFAKCEMRDAKCGKIQCQGGASRPVIGTNAVSIETNIPLQQGGRILCRGTHVYLGDDMPDPGLVLAGTKCADGKICLNRQCQNISVFGVHECAMQCHGRGVCNNRKNCHCEAHWAPPFCDKFGFGGSTDSGPIRQADNQGLTIGILVTILCLLAAGFVVYLKRKTLIRLLFTNKKTTIEKLRCVRPSRPPRGFQPCQAHLGHLGKGLMRKPPDSYPPKDNPRRLLQCQNVDISRPLNGLNVPQPQSTQRVLPPLHRAPRAPSVPARPLPAKPALRQAQGTCKPNPPQKPLPADPLARTTRLTHALARTPGQWETGLRLAPLRPAPQYPHQVPRSTHTAYIK
442	P78536	>sp|P78536|ADA17_HUMAN Disintegrin and metalloproteinase domain-containing protein 17 GN=ADAM17 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MRQSLLFLTSVVPFVLAPRPPDDPGFGPHQRLEKLDSLLSDYDILSLSNIQQHSVRKRDLQTSTHVETLLTFSALKRHFKLYLTSSTERFSQNFKVVVVDGKNESEYTVKWQDFFTGHVVGEPDSRVLAHIRDDDVIIRINTDGAEYNIEPLWRFVNDTKDKRMLVYKSEDIKNVSRLQSPKVCGYLKVDNEELLPKGLVDREPPEELVHRVKRRADPDPMKNTCKLLVVADHRFYRYMGRGEESTTTNYLIELIDRVDDIYRNTSWDNAGFKGYGIQIEQIRILKSPQEVKPGEKHYNMAKSYPNEEKDAWDVKMLLEQFSFDIAEEASKVCLAHLFTYQDFDMGTLGLAYVGSPRANSHGGVCPKAYYSPVGKKNIYLNSGLTSTKNYGKTILTKEADLVTTHELGHNFGAEHDPDGLAECAPNEDQGGKYVMYPIAVSGDHENNKMFSNCSKQSIYKTIESKAQECFQERSNKVCGNSRVDEGEECDPGIMYLNNDTCCNSDCTLKEGVQCSDRNSPCCKNCQFETAQKKCQEAINATCKGVSYCTGNSSECPPPGNAEDDTVCLDLGKCKDGKCIPFCEREQQLESCACNETDNSCKVCCRDLSGRCVPYVDAEQKNLFLRKGKPCTVGFCDMNGKCEKRVQDVIERFWDFIDQLSINTFGKFLADNIVGSVLVFSLIFWIPFSILVHCVDKKLDKQYESLSLFHPSNVEMLSSMDSASVRIIKPFPAPQTPGRLQPAPVIPSAPAAPKLDHQRMDTIQEDPSTDSHMDEDGFEKDPFPNSSTAAKSFEDLTDHPVTRSEKAASFKLQRQNRVDSKETEC
443	Q9P0K1	>sp|Q9P0K1|ADA22_HUMAN Disintegrin and metalloproteinase domain-containing protein 22 GN=ADAM22 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MQAAVAVSVPFLLLCVLGTCPPARCGQAGDASLMELEKRKENRFVERQSIVPLRLIYRSGGEDESRHDALDTRVRGDLGGPQLTHVDQASFQVDAFGTSFILDVVLNHDLLSSEYIERHIEHGGKTVEVKGGEHCYYQGHIRGNPDSFVALSTCHGLHGMFYDGNHTYLIEPEENDTTQEDFHFHSVYKSRLFEFSLDDLPSEFQQVNITPSKFILKPRPKRSKRQLRRYPRNVEEETKYIELMIVNDHLMFKKHRLSVVHTNTYAKSVVNMADLIYKDQLKTRIVLVAMETWATDNKFAISENPLITLREFMKYRRDFIKEKSDAVHLFSGSQFESSRSGAAYIGGICSLLKGGGVNEFGKTDLMAVTLAQSLAHNIGIISDKRKLASGECKCEDTWSGCIMGDTGYYLPKKFTQCNIEEYHDFLNSGGGACLFNKPSKLLDPPECGNGFIETGEECDCGTPAECVLEGAECCKKCTLTQDSQCSDGLCCKKCKFQPMGTVCREAVNDCDIRETCSGNSSQCAPNIHKMDGYSCDGVQGICFGGRCKTRDRQCKYIWGQKVTASDKYCYEKLNIEGTEKGNCGKDKDTWIQCNKRDVLCGYLLCTNIGNIPRLGELDGEITSTLVVQQGRTLNCSGGHVKLEEDVDLGYVEDGTPCGPQMMCLEHRCLPVASFNFSTCLSSKEGTICSGNGVCSNELKCVCNRHWIGSDCNTYFPHNDDAKTGITLSGNGVAGTNIIIGIIAGTILVLALILGITAWGYKNYREQRQLPQGDYVKKPGDGDSFYSDIPPGVSTNSASSSKKRSNGLSHSWSERIPDTKHISDICENGRPRSNSWQGNLGGNKKKIRGKRFRPRSNSTETLSPAKSPSSSTGSIASSRKYPYPMPPLPDEDKKVNRQSARLWETSI
444	Q9UKQ2	>sp|Q9UKQ2|ADA28_HUMAN Disintegrin and metalloproteinase domain-containing protein 28 GN=ADAM28 PE=2 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MLQGLLPVSLLLSVAVSAIKELPGVKKYEVVYPIRLHPLHKREAKEPEQQEQFETELKYKMTINGKIAVLYLKKNKNLLAPGYTETYYNSTGKEITTSPQIMDDCYYQGHILNEKVSDASISTCRGLRGYFSQGDQRYFIEPLSPIHRDGQEHALFKYNPDEKNYDSTCGMDGVLWAHDLQQNIALPATKLVKLKDRKVQEHEKYIEYYLVLDNGEFKRYNENQDEIRKRVFEMANYVNMLYKKLNTHVALVGMEIWTDKDKIKITPNASFTLENFSKWRGSVLSRRKRHDIAQLITATELAGTTVGLAFMSTMCSPYSVGVVQDHSDNLLRVAGTMAHEMGHNFGMFHDDYSCKCPSTICVMDKALSFYIPTDFSSCSRLSYDKFFEDKLSNCLFNAPLPTDIISTPICGNQLVEMGEDCDCGTSEECTNICCDAKTCKIKATFQCALGECCEKCQFKKAGMVCRPAKDECDLPEMCNGKSGNCPDDRFQVNGFPCHHGKGHCLMGTCPTLQEQCTELWGPGTEVADKSCYNRNEGGSKYGYCRRVDDTLIPCKANDTMCGKLFCQGGSDNLPWKGRIVTFLTCKTFDPEDTSQEIGMVANGTKCGDNKVCINAECVDIEKAYKSTNCSSKCKGHAVCDHELQCQCEEGWIPPDCDDSSVVFHFSIVVGVLFPMAVIFVVVAMVIRHQSSREKQKKDQRPLSTTGTRPHKQKRKPQMVKAVQPQEMSQMKPHVYDLPVEGNEPPASFHKDTNALPPTVFKDNPVSTPKDSNPKA
445	Q9UKF5	>sp|Q9UKF5|ADA29_HUMAN Disintegrin and metalloproteinase domain-containing protein 29 GN=ADAM29 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MKMLLLLHCLGVFLSCSGHIQDEHPQYHSPPDVVIPVRITGTTRGMTPPGWLSYILPFGGQKHIIHIKVKKLLFSKHLPVFTYTDQGAILEDQPFVQNNCYYHGYVEGDPESLVSLSTCFGGFQGILQINDFAYEIKPLAFSTTFEHLVYKMDSEEKQFSTMRSGFMQNEITCRMEFEEIDNSTQKQSSYVGWWIHFRIVEIVVVIDNYLYIRYERNDSKLLEDLYVIVNIVDSILDVIGVKVLLFGLEIWTNKNLIVVDDVRKSVHLYCKWKSENITPRMQHDTSHLFTTLGLRGLSGIGAFRGMCTPHRSCAIVTFMNKTLGTFSIAVAHHLGHNLGMNHDEDTCRCSQPRCIMHEGNPPITKFSNCSYGDFWEYTVERTKCLLETVHTKDIFNVKRCGNGVVEEGEECDCGPLKHCAKDPCCLSNCTLTDGSTCAFGLCCKDCKFLPSGKVCRKEVNECDLPEWCNGTSHKCPDDFYVEDGIPCKERGYCYEKSCHDRNEQCRRIFGAGANTASETCYKELNTLGDRVGHCGIKNATYIKCNISDVQCGRIQCENVTEIPNMSDHTTVHWARFNDIMCWSTDYHLGMKGPDIGEVKDGTECGIDHICIHRHCVHITILNSNCSPAFCNKRGICNNKHHCHCNYLWDPPNCLIKGYGGSVDSGPPPKRKKKKKFCYLCILLLIVLFILLCCLYRLCKKSKPIKKQQDVQTPSAKEEEKIQRRPHELPPQSQPWVMPSQSQPPVTPSQSHPQVMPSQSQPPVTPSQSQPRVMPSQSQPPVMPSQSHPQLTPSQSQPPVTPSQRQPQLMPSQSQPPVTPS
446	Q13443	>sp|Q13443|ADAM9_HUMAN Disintegrin and metalloproteinase domain-containing protein 9 GN=ADAM9 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MGSGARFPSGTLRVRWLLLLGLVGPVLGAARPGFQQTSHLSSYEIITPWRLTRERREAPRPYSKQVSYVIQAEGKEHIIHLERNKDLLPEDFVVYTYNKEGTLITDHPNIQNHCHYRGYVEGVHNSSIALSDCFGLRGLLHLENASYGIEPLQNSSHFEHIIYRMDDVYKEPLKCGVSNKDIEKETAKDEEEEPPSMTQLLRRRRAVLPQTRYVELFIVVDKERYDMMGRNQTAVREEMILLANYLDSMYIMLNIRIVLVGLEIWTNGNLINIVGGAGDVLGNFVQWREKFLITRRRHDSAQLVLKKGFGGTAGMAFVGTVCSRSHAGGINVFGQITVETFASIVAHELGHNLGMNHDDGRDCSCGAKSCIMNSGASGSRNFSSCSAEDFEKLTLNKGGNCLLNIPKPDEAYSAPSCGNKLVDAGEECDCGTPKECELDPCCEGSTCKLKSFAECAYGDCCKDCRFLPGGTLCRGKTSECDVPEYCNGSSQFCQPDVFIQNGYPCQNNKAYCYNGMCQYYDAQCQVIFGSKAKAAPKDCFIEVNSKGDRFGNCGFSGNEYKKCATGNALCGKLQCENVQEIPVFGIVPAIIQTPSRGTKCWGVDFQLGSDVPDPGMVNEGTKCGAGKICRNFQCVDASVLNYDCDVQKKCHGHGVCNSNKNCHCENGWAPPNCETKGYGGSVDSGPTYNEMNTALRDGLLVFFFLIVPLIVCAIFIFIKRDQLWRSYFRKKRSQTYESDGKNQANPSRQPGSVPRHVSPVTPPREVPIYANRFAVPTYAAKQPQQFPSRPPPPQPKVSSQGNLIPARPAPAPPLYSSLT
447	P00813	>sp|P00813|ADA_HUMAN Adenosine deaminase GN=ADA PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MAQTPAFDKPKVELHVHLDGSIKPETILYYGRRRGIALPANTAEGLLNVIGMDKPLTLPDFLAKFDYYMPAIAGCREAIKRIAYEFVEMKAKEGVVYVEVRYSPHLLANSKVEPIPWNQAEGDLTPDEVVALVGQGLQEGERDFGVKARSILCCMRHQPNWSPKVVELCKKYQQQTVVAIDLAGDETIPGSSLLPGHVQAYQEAVKSGIHRTVHAGEVGSAEVVKEAVDILKTERLGHGYHTLEDQALYNRLRQENMHFEICPWSSYLTGAWKPDTEHAVIRLKNDQANYSLNTDDPLIFKSTLDTDYQMTKRDMGFTEEEFKRLNINAAKSSFLPEDEKRELLDLLYKAYGMPPSASAGQNL
448	Q8NI60	>sp|Q8NI60|ADCK3_HUMAN Atypical kinase ADCK3, mitochondrial GN=ADCK3 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAAILGDTIMVAKGLVKLTQAAVETHLQHLGIGGELIMAARALQSTAVEQIGMFLGKVQGQDKHEEYFAENFGGPEGEFHFSVPHAAGASTDFSSASAPDQSAPPSLGHAHSEGPAPAYVASGPFREAGFPGQASSPLGRANGRLFANPRDSFSAMGFQRRFFHQDQSPVGGLTAEDIEKARQAKARPENKQHKQTLSEHARERKVPVTRIGRLANFGGLAVGLGFGALAEVAKKSLRSEDPSGKKAVLGSSPFLSEANAERIVRTLCKVRGAALKLGQMLSIQDDAFINPHLAKIFERVRQSADFMPLKQMMKTLNNDLGPNWRDKLEYFEERPFAAASIGQVHLARMKGGREVAMKIQYPGVAQSINSDVNNLMAVLNMSNMLPEGLFPEHLIDVLRRELALECDYQREAACARKFRDLLKGHPFFYVPEIVDELCSPHVLTTELVSGFPLDQAEGLSQEIRNEICYNILVLCLRELFEFHFMQTDPNWSNFFYDPQQHKVALLDFGATREYDRSFTDLYIQIIRAAADRDRETVRAKSIEMKFLTGYEVKVMEDAHLDAILILGEAFASDEPFDFGTQSTTEKIHNLIPVMLRHRLVPPPEETYSLHRKMGGSFLICSKLKARFPCKAMFEEAYSNYCKRQAQQ
449	Q5VUY2	>sp|Q5VUY2|ADCL4_HUMAN Arylacetamide deacetylase-like 4 GN=AADACL4 PE=3 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAVPWLVLLLALPIFFLGVFVWAVFEHFLTTDIPATLQHPAKLRFLHCIFLYLVTLGNIFEKLGICSMPKFIRFLHDSVRIKKDPELVVTDLRFGTIPVRLFQPKAASSRPRRGIIFYHGGATVFGSLDCYHGLCNYLARETESVLLMIGYRKLPDHHSPALFQDCMNASIHFLKALETYGVDPSRVVVCGESVGGAAVAAITQALVGRSDLPRIRAQVLIYPVVQAFCLQLPSFQQNQNVPLLSRKFMVTSLCNYLAIDLSWRDAILNGTCVPPDVWRKYEKWLSPDNIPKKFKNRGYQPWSPGPFNEAAYLEAKHMLDVENSPLIADDEVIAQLPEAFLVSCENDILRDDSLLYKKRLEDQGVRVTWYHLYDGFHGSIIFFDKKALSFPCSLKIVNAVVSYIKGI
450	Q8NFM4	>sp|Q8NFM4|ADCY4_HUMAN Adenylate cyclase type 4 GN=ADCY4 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MARLFSPRPPPSEDLFYETYYSLSQQYPLLLLLLGIVLCALAALLAVAWASGRELTSDPSFLTTVLCALGGFSLLLGLASREQRLQRWTRPLSGLVWVALLALGHAFLFTGGVVSAWDQVSYFLFVIFTAYAMLPLGMRDAAVAGLASSLSHLLVLGLYLGPQPDSRPALLPQLAANAVLFLCGNVAGVYHKALMERALRATFREALSSLHSRRRLDTEKKHQEHLLLSILPAYLAREMKAEIMARLQAGQGSRPESTNNFHSLYVKRHQGVSVLYADIVGFTRLASECSPKELVLMLNELFGKFDQIAKEHECMRIKILGDCYYCVSGLPLSLPDHAINCVRMGLDMCRAIRKLRAATGVDINMRVGVHSGSVLCGVIGLQKWQYDVWSHDVTLANHMEAGGVPGRVHITGATLALLAGAYAVEDAGMEHRDPYLRELGEPTYLVIDPRAEEEDEKGTAGGLLSSLEGLKMRPSLLMTRYLESWGAAKPFAHLSHGDSPVSTSTPLPEKTLASFSTQWSLDRSRTPRGLDDELDTGDAKFFQVIEQLNSQKQWKQSKDFNPLTLYFREKEMEKEYRLSAIPAFKYYEACTFLVFLSNFIIQMLVTNRPPALAITYSITFLLFLLILFVCFSEDLMRCVLKGPKMLHWLPALSGLVATRPGLRIALGTATILLVFAMAITSLFFFPTSSDCPFQAPNVSSMISNLSWELPGSLPLISVPYSMHCCTLGFLSCSLFLHMSFELKLLLLLLWLAASCSLFLHSHAWLSECLIVRLYLGPLDSRPGVLKEPKLMGAISFFIFFFTLLVLARQNEYYCRLDFLWKKKLRQEREETETMENLTRLLLENVLPAHVAPQFIGQNRRNEDLYHQSYECVCVLFASVPDFKEFYSESNINHEGLECLRLLNEIIADFDELLSKPKFSGVEKIKTIGSTYMAATGLNATSGQDAQQDAERSCSHLGTMVEFAVALGSKLDVINKHSFNNFRLRVGLNHGPVVAGVIGAQKPQYDIWGNTVNVASRMESTGVLGKIQVTEETAWALQSLGYTCYSRGVIKVKGKGQLCTYFLNTDLTRTGPPSATLG
451	P40145	>sp|P40145|ADCY8_HUMAN Adenylate cyclase type 8 GN=ADCY8 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MELSDVRCLTGSEELYTIHPTPPAGDGRSASRPQRLLWQTAVRHITEQRFIHGHRGGSGSGSGGSGKASDPAGGGPNHHAPQLSGDSALPLYSLGPGERAHSTCGTKVFPERSGSGSASGSGGGGDLGFLHLDCAPSNSDFFLNGGYSYRGVIFPTLRNSFKSRDLERLYQRYFLGQRRKSEVVMNVLDVLTKLTLLVLHLSLASAPMDPLKGILLGFFTGIEVVICALVVVRKDTTSHTYLQYSGVVTWVAMTTQILAAGLGYGLLGDGIGYVLFTLFATYSMLPLPLTWAILAGLGTSLLQVILQVVIPRLAVISINQVVAQAVLFMCMNTAGIFISYLSDRAQRQAFLETRRCVEARLRLETENQRQERLVLSVLPRFVVLEMINDMTNVEDEHLQHQFHRIYIHRYENVSILFADVKGFTNLSTTLSAQELVRMLNELFARFDRLAHEHHCLRIKILGDCYYCVSGLPEPRQDHAHCCVEMGLSMIKTIRYVRSRTKHDVDMRIGIHSGSVLCGVLGLRKWQFDVWSWDVDIANKLESGGIPGRIHISKATLDCLNGDYNVEEGHGKERNEFLRKHNIETYLIKQPEDSLLSLPEDIVKESVSSSDRRNSGATFTEGSWSPELPFDNIVGKQNTLAALTRNSINLLPNHLAQALHVQSGPEEINKRIEHTIDLRSGDKLRREHIKPFSLMFKDSSLEHKYSQMRDEVFKSNLVCAFIVLLFITAIQSLLPSSRVMPMTIQFSILIMLHSALVLITTAEDYKCLPLILRKTCCWINETYLARNVIIFASILINFLGAILNILWCDFDKSIPLKNLTFNSSAVFTDICSYPEYFVFTGVLAMVTCAVFLRLNSVLKLAVLLIMIAIYALLTETVYAGLFLRYDNLNHSGEDFLGTKEVSLLLMAMFLLAVFYHGQQLEYTARLDFLWRVQAKEEINEMKELREHNENMLRNILPSHVARHFLEKDRDNEELYSQSYDAVGVMFASIPGFADFYSQTEMNNQGVECLRLLNEIIADFDELLGEDRFQDIEKIKTIGSTYMAVSGLSPEKQQCEDKWGHLCALADFSLALTESIQEINKHSFNNFELRIGISHGSVVAGVIGAKKPQYDIWGKTVNLASRMDSTGVSGRIQVPEETYLILKDQGFAFDYRGEIYVKGISEQEGKIKTYFLLGRVQPNPFILPPRRLPGQYSLAAVVLGLVQSLNRQRQKQLLNENNNTGIIKGHYNRRTLLSPSGTEPGAQAEGTDKSDLP
452	Q9NRN7	>sp|Q9NRN7|ADPPT_HUMAN L-aminoadipate-semialdehyde dehydrogenase-phosphopantetheinyl transferase GN=AASDHPPT PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MVFPAKRFCLVPSMEGVRWAFSCGTWLPSRAEWLLAVRSIQPEEKERIGQFVFARDAKAAMAGRLMIRKLVAEKLNIPWNHIRLQRTAKGKPVLAKDSSNPYPNFNFNISHQGDYAVLAAEPELQVGIDIMKTSFPGRGSIPEFFHIMKRKFTNKEWETIRSFKDEWTQLDMFYRNWALKESFIKAIGVGLGFELQRLEFDLSPLNLDIGQVYKETRLFLDGEEEKEWAFEESKIDEHHFVAVALRKPDGSRHQDVPSQDDSKPTQRQFTILNFNDLMSSAVPMTPEDPSFWDCFCFTEEIPIRNGTKS
453	Q3LIE5	>sp|Q3LIE5|ADPRM_HUMAN Manganese-dependent ADP-ribose/CDP-alcohol diphosphatase GN=ADPRM PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MDDKPNPEALSDSSERLFSFGVIADVQFADLEDGFNFQGTRRRYYRHSLLHLQGAIEDWNNESSMPCCVLQLGDIIDGYNAQYNASKKSLELVMDMFKRLKVPVHHTWGNHEFYNFSREYLTHSKLNTKFLEDQIVHHPETMPSEDYYAYHFVPFPKFRFILLDAYDLSVLGVDQSSPKYEQCMKILREHNPNTELNSPQGLSEPQFVQFNGGFSQEQLNWLNEVLTFSDTNQEKVVIVSHLPIYPDASDNVCLAWNYRDALAVIWSHECVVCFFAGHTHDGGYSEDPFGVYHVNLEGVIETAPDSQAFGTVHVYPDKMMLKGRGRVPDRIMNYKKERAFHC
454	Q16186	>sp|Q16186|ADRM1_HUMAN Proteasomal ubiquitin receptor ADRM1 GN=ADRM1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MTTSGALFPSLVPGSRGASNKYLVEFRAGKMSLKGTTVTPDKRKGLVYIQQTDDSLIHFCWKDRTSGNVEDDLIIFPDDCEFKRVPQCPSGRVYVLKFKAGSKRLFFWMQEPKTDQDEEHCRKVNEYLNNPPMPGALGASGSSGHELSALGGEGGLQSLLGNMSHSQLMQLIGPAGLGGLGGLGALTGPGLASLLGSSGPPGSSSSSSSRSQSAAVTPSSTTSSTRATPAPSAPAAASATSPSPAPSSGNGASTAASPTQPIQLSDLQSILATMNVPAGPAGGQQVDLASVLTPEIMAPILANADVQERLLPYLPSGESLPQTADEIQNTLTSPQFQQALGMFSAALASGQLGPLMCQFGLPAEAVEAANKGDVEAFAKAMQNNAKPEQKEGDTKDKKDEEEDMSLD
455	P22570	>sp|P22570|ADRO_HUMAN NADPH:adrenodoxin oxidoreductase, mitochondrial GN=FDXR PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MASRCWRWWGWSAWPRTRLPPAGSTPSFCHHFSTQEKTPQICVVGSGPAGFYTAQHLLKHPQAHVDIYEKQPVPFGLVRFGVAPDHPEVKNVINTFTQTAHSGRCAFWGNVEVGRDVTVPELREAYHAVVLSYGAEDHRALEIPGEELPGVCSARAFVGWYNGLPENQELEPDLSCDTAVILGQGNVALDVARILLTPPEHLERTDITKAALGVLRQSRVKTVWLVGRRGPLQVAFTIKELREMIQLPGARPILDPVDFLGLQDKIKEVPRPRKRLTELLLRTATEKPGPAEAARQASASRAWGLRFFRSPQQVLPSPDGRRAAGVRLAVTRLEGVDEATRAVPTGDMEDLPCGLVLSSIGYKSRPVDPSVPFDSKLGVIPNVEGRVMDVPGLYCSGWVKRGPTGVIATTMTDSFLTGQMLLQDLKAGLLPSGPRPGYAAIQALLSSRGVRPVSFSDWEKLDAEEVARGQGTGKPREKLVDPQEMLRLLGH
456	Q9H0C2	>sp|Q9H0C2|ADT4_HUMAN ADP/ATP translocase 4 GN=SLC25A31 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MHREPAKKKAEKRLFDASSFGKDLLAGGVAAAVSKTAVAPIERVKLLLQVQASSKQISPEARYKGMVDCLVRIPREQGFFSFWRGNLANVIRYFPTQALNFAFKDKYKQLFMSGVNKEKQFWRWFLANLASGGAAGATSLCVVYPLDFARTRLGVDIGKGPEERQFKGLGDCIMKIAKSDGIAGLYQGFGVSVQGIIVYRASYFGAYDTVKGLLPKPKKTPFLVSFFIAQVVTTCSGILSYPFDTVRRRMMMQSGEAKRQYKGTLDCFVKIYQHEGISSFFRGAFSNVLRGTGGALVLVLYDKIKEFFHIDIGGR
457	Q96SZ5	>sp|Q96SZ5|AEDO_HUMAN 2-aminoethanethiol dioxygenase GN=ADO PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MPRDNMASLIQRIARQACLTFRGSGGGRGASDRDAASGPEAPMQPGFPENLSKLKSLLTQLRAEDLNIAPRKATLQPLPPNLPPVTYMHIYETDGFSLGVFLLKSGTSIPLHDHPGMHGMLKVLYGTVRISCMDKLDAGGGQRPRALPPEQQFEPPLQPREREAVRPGVLRSRAEYTEASGPCILTPHRDNLHQIDAVEGPAAFLDILAPPYDPDDGRDCHYYRVLEPVRPKEASSSACDLPREVWLLETPQADDFWCEGEPYPGPKVFP
458	Q8TED9	>sp|Q8TED9|AF1L1_HUMAN Actin filament-associated protein 1-like 1 GN=AFAP1L1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MDRGQVLEQLLPELTGLLSLLDHEYLSDTTLEKKMAVASILQSLQPLPAKEVSYLYVNTADLHSGPSFVESLFEEFDCDLSDLRDMPEDDGEPSKGASPELAKSPRLRNAADLPPPLPNKPPPEDYYEEALPLGPGKSPEYISSHNGCSPSHSIVDGYYEDADSSYPATRVNGELKSSYNDSDAMSSSYESYDEEEEEGKSPQPRHQWPSEEASMHLVRECRICAFLLRKKRFGQWAKQLTVIREDQLLCYKSSKDRQPHLRLALDTCSIIYVPKDSRHKRHELRFTQGATEVLVLALQSREQAEEWLKVIREVSKPVGGAEGVEVPRSPVLLCKLDLDKRLSQEKQTSDSDSVGVGDNCSTLGRRETCDHGKGKKSSLAELKGSMSRAAGRKITRIIGFSKKKTLADDLQTSSTEEEVPCCGYLNVLVNQGWKERWCRLKCNTLYFHKDHMDLRTHVNAIALQGCEVAPGFGPRHPFAFRILRNRQEVAILEASCSEDMGRWLGLLLVEMGSRVTPEALHYDYVDVETLTSIVSAGRNSFLYARSCQNQWPEPRVYDDVPYEKMQDEEPERPTGAQVKRHASSCSEKSHRVDPQVKVKRHASSANQYKYGKNRAEEDARRYLVEKEKLEKEKETIRTELIALRQEKRELKEAIRSSPGAKLKALEEAVATLEAQCRAKEERRIDLELKLVAVKERLQQSLAGGPALGLSVSSKPKSGETANKPQNSVPEQPLPVNCVSELRKRSPSIVASNQGRVLQKAKEWEMKKT
459	P42568	>sp|P42568|AF9_HUMAN Protein AF-9 GN=MLLT3 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MASSCAVQVKLELGHRAQVRKKPTVEGFTHDWMVFVRGPEHSNIQHFVEKVVFHLHESFPRPKRVCKDPPYKVEESGYAGFILPIEVYFKNKEEPRKVRFDYDLFLHLEGHPPVNHLRCEKLTFNNPTEDFRRKLLKAGGDPNRSIHTSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSTSFSKPHKLMKEHKEKPSKDSREHKSAFKEPSRDHNKSSKESSKKPKENKPLKEEKIVPKMAFKEPKPMSKEPKPDSNLLTITSGQDKKAPSKRPPISDSEELSAKKRKKSSSEALFKSFSSAPPLILTCSADKKQIKDKSHVKMGKVKIESETSEKKKSTLPPFDDIVDPNDSDVEENISSKSDSEQPSPASSSSSSSSSFTPSQTRQQGPLRSIMKDLHSDDNEEESDEVEDNDNDSEMERPVNRGGSRSRRVSLSDGSDSESSSASSPLHHEPPPPLLKTNNNQILEVKSPIKQSKSDKQIKNGECDKAYLDELVELHRRLMTLRERHILQQIVNLIEETGHFHITNTTFDFDLCSLDKTTVRKLQSYLETSGTS
460	P51816	>sp|P51816|AFF2_HUMAN AF4/FMR2 family member 2 GN=AFF2 PE=1 SV=4 Homo sapiens OS=Human NCBI_TaxID=9606	MDLFDFFRDWDLEQQCHYEQDRSALKKREWERRNQEVQQEDDLFSSGFDLFGEPYKVAEYTNKGDALANRVQNTLGNYDEMKNLLTNHSNQNHLVGIPKNSVPQNPNNKNEPSFFPEQKNRIIPPHQDNTHPSAPMPPPSVVILNSTLIHSNRKSKPEWSRDSHNPSTVLASQASGQPNKMQTLTQDQSQAKLEDFFVYPAEQPQIGEVEESNPSAKEDSNPNSSGEDAFKEIFQSNSPEESEFAVQAPGSPLVASSLLAPSSGLSVQNFPPGLYCKTSMGQQKPTAYVRPMDGQDQAPDISPTLKPSIEFENSFGNLSFGTLLDGKPSAASSKTKLPKFTILQTSEVSLPSDPSCVEEILREMTHSWPTPLTSMHTAGHSEQSTFSIPGQESQHLTPGFTLQKWNDPTTRASTKSVSFKSMLEDDLKLSSDEDDLEPVKTLTTQCTATELYQAVEKAKPRNNPVNPPLATPQPPPAVQASGGSGSSSESESSSESDSDTESSTTDSESNEAPRVATPEPEPPSTNKWQLDKWLNKVTSQNKSFICGQNETPMETISLPPPIIQPMEVQMKVKTNASQVPAEPKERPLLSLIREKARPRPTQKIPETKALKHKLSTTSETVSQRTIGKKQPKKVEKNTSTDEFTWPKPNITSSTPKEKESVELHDPPRGRNKATAHKPAPRKEPRPNIPLAPEKKKYRGPGKIVPKSREFIETDSSTSDSNTDQEETLQIKVLPPCIISGGNTAKSKEICGASLTLSTLMSSSGSNNNLSISNEEPTFSPIPVMQTEILSPLRDHENLKNLWVKIDLDLLSRVPGHSSLHAAPAKPDHKETATKPKRQTAVTAVEKPAPKGKRKHKPIEVAEKIPEKKQRLEEATTICLLPPCISPAPPHKPPNTRENNSSRRANRRKEEKLFPPPLSPLPEDPPRRRNVSGNNGPFGQDKNIAMTGQITSTKPKRTEGKFCATFKGISVNEGDTPKKASSATITVTNTAIATATVTATAIVTTTVTATATATATTTTTTTTISTITSTITTGLMDSSHLEMTSWAALPLLSSSSTNVRRPKLTFDDSVHNADYYMQEAKKLKHKADALFEKFGKAVNYADAALSFTECGNAMERDPLEAKSPYTMYSETVELLRYAMRLKNFASPLASDGDKKLAVLCYRCLSLLYLRMFKLKKDHAMKYSRSLMEYFKQNASKVAQIPSPWVSNGKNTPSPVSLNNVSPINAMGNCNNGPVTIPQRIHHMAASHVNITSNVLRGYEHWDMADKLTRENKEFFGDLDTLMGPLTQHSSMTNLVRYVRQGLCWLRIDAHLL
461	Q9UHB7	>sp|Q9UHB7|AFF4_HUMAN AF4/FMR2 family member 4 GN=AFF4 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MNREDRNVLRMKERERRNQEIQQGEDAFPPSSPLFAEPYKVTSKEDKLSSRIQSMLGNYDEMKDFIGDRSIPKLVAIPKPTVPPSADEKSNPNFFEQRHGGSHQSSKWTPVGPAPSTSQSQKRSSGLQSGHSSQRTSAGSSSGTNSSGQRHDRESYNNSGSSSRKKGQHGSEHSKSRSSSPGKPQAVSSLNSSHSRSHGNDHHSKEHQRSKSPRDPDANWDSPSRVPFSSGQHSTQSFPPSLMSKSNSMLQKPTAYVRPMDGQESMEPKLSSEHYSSQSHGNSMTELKPSSKAHLTKLKIPSQPLDASASGDVSCVDEILKEMTHSWPPPLTAIHTPCKTEPSKFPFPTKESQQSNFGTGEQKRYNPSKTSNGHQSKSMLKDDLKLSSSEDSDGEQDCDKTMPRSTPGSNSEPSHHNSEGADNSRDDSSSHSGSESSSGSDSESESSSSDSEANEPSQSASPEPEPPPTNKWQLDNWLNKVNPHKVSPASSVDSNIPSSQGYKKEGREQGTGNSYTDTSGPKETSSATPGRDSKTIQKGSESGRGRQKSPAQSDSTTQRRTVGKKQPKKAEKAAAEEPRGGLKIESETPVDLASSMPSSRHKAATKGSRKPNIKKESKSSPRPTAEKKKYKSTSKSSQKSREIIETDTSSSDSDESESLPPSSQTPKYPESNRTPVKPSSVEEEDSFFRQRMFSPMEEKELLSPLSEPDDRYPLIVKIDLNLLTRIPGKPYKETEPPKGEKKNVPEKHTREAQKQASEKVSNKGKRKHKNEDDNRASESKKPKTEDKNSAGHKPSSNRESSKQSAAKEKDLLPSPAGPVPSKDPKTEHGSRKRTISQSSSLKSSSNSNKETSGSSKNSSSTSKQKKTEGKTSSSSKEVKEKAPSSSSNCPPSAPTLDSSKPRRTKLVFDDRNYSADHYLQEAKKLKHNADALSDRFEKAVYYLDAVVSFIECGNALEKNAQESKSPFPMYSETVDLIKYTMKLKNYLAPDATAADKRLTVLCLRCESLLYLRLFKLKKENALKYSKTLTEHLKNSYNNSQAPSPGLGSKAVGMPSPVSPKLSPGNSGNYSSGASSASASGSSVTIPQKIHQMAASYVQVTSNFLYATEIWDQAEQLSKEQKEFFAELDKVMGPLIFNASIMTDLVRYTRQGLHWLRQDAKLIS
462	Q8TF27	>sp|Q8TF27|AGA11_HUMAN Arf-GAP with GTPase, ANK repeat and PH domain-containing protein 11 GN=AGAP11 PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MTIISVTLEIHHHITERDADRSLTILDEQLYSFAFSTVHITKKRNGGGSLNNYSSSIPLTPSTSQEDLYFSVPPTANTPTPICKQSMGWSNLFTSEKGSDPDKGRKALESHADTIGSGRAIPIKQGMLLKRSGKWLKTWKKKYVTLCSNGVLTYYSSLGDYMKNIHKKEIDLRTSTIKVPGKWPSLATSACAPISSSKSNGLSKDMEALHMSANSDIGLGDSICFSPSISSTTSPKLNLPPSPHANKKKHLKKKSTNNLKDDGLSSTAEEEEEKFMIVSVTGQTCHFKATTYEERDAWVQAIQSQILASLQSCESSKSKSQLTSQSEAMALQSIQNMRGNSHCVDCETQNPKWASLNLGVLMCIECSGIHRSLGTRLSRVRSLELDDWPVELRKVMSSIGNDLANSIWEGSSQGQTKPSIESTREEKERWIRSKYEHKLFLAPLPCTELSLGQHLLRATADEDLRTAILLLAHGSREEVNETCGEGDGCTALHLACRKGNVVLAQLLIWYGVDVMARDAHGNTALTYARQASSQECINVLLQYGCPDECV
463	Q5VW22	>sp|Q5VW22|AGAP6_HUMAN Arf-GAP with GTPase, ANK repeat and PH domain-containing protein 6 GN=AGAP6 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MGNILTCRVHPSVSLEFDQQQGSVCPSESETYEAGARDRMAGAPMAAAVQPAEVTVEVGEDLHMHHVRDREMPEALEFNPSANPEASTIFQRNSQTDVVEIRRSNCTNHVSAVRFSQQYSLCSTIFLDDSTAIQHYLTMTIISVTLEIPHHITQRDADRTLSIPDEQLHSFAVSTVHIMKKRNGGGSLNNYSSSIPSTPSTSQEDPQFSVPPTANTPTPVCKRSMRWSNLFTSEKGSDPDKERKAPENHADTIGSGRAIPIKQGMLLKRSGKWLKTWKKKYVTLCSNGMLTYYSSLGDYMKNIHKKEIDLQTSTIKVPGKWPSLATSACTPISSSKSNGLSKDMDTGLGDSICFSPSISSTTSPKLNPPPSPHANKKKHLKKKSTNNFMIVSATGQTWHFEATTYEERDAWVQAIQSQILASLQSCESSKSKSQLTSQSEAMALQSIQNMRGNAHCVDCETQNPKWASLNLGVLMCIECSGIHRSLGPHLSRVRSLELDDWPVELRKVMSSIVNDLANSIWEGSSQGQTKPSEKSTREEKERWIRSKYEEKLFLAPLPCTELSLGQQLLRATADEDLQTAILLLAHGSCEEVNETCGEGDGCTALHLACRKGNVVLAQLLIWYGVDVMARDAHGNTALTYARQASSQECINVLLQYGCPDECV
464	P52594	>sp|P52594|AGFG1_HUMAN Arf-GAP domain and FG repeat-containing protein 1 GN=AGFG1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAASAKRKQEEKHLKMLRDMTGLPHNRKCFDCDQRGPTYVNMTVGSFVCTSCSGSLRGLNPPHRVKSISMTTFTQQEIEFLQKHGNEVCKQIWLGLFDDRSSAIPDFRDPQKVKEFLQEKYEKKRWYVPPEQAKVVASVHASISGSSASSTSSTPEVKPLKSLLGDSAPTLHLNKGTPSQSPVVGRSQGQQQEKKQFDLLSDLGSDIFAAPAPQSTATANFANFAHFNSHAAQNSANADFANFDAFGQSSGSSNFGGFPTASHSPFQPQTTGGSAASVNANFAHFDNFPKSSSADFGTFNTSQSHQTASAVSKVSTNKAGLQTADKYAALANLDNIFSAGQGGDQGSGFGTTGKAPVGSVVSVPSQSSASSDKYAALAELDSVFSSAATSSNAYTSTSNASSNVFGTVPVVASAQTQPASSSVPAPFGATPSTNPFVAAAGPSVASSTNPFQTNARGATAATFGTASMSMPTGFGTPAPYSLPTSFSGSFQQPAFPAQAAFPQQTAFSQQPNGAGFAAFGQTKPVVTPFGQVAAAGVSSNPFMTGAPTGQFPTGSSSTNPFL
465	O95394	>sp|O95394|AGM1_HUMAN Phosphoacetylglucosamine mutase GN=PGM3 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MDLGAITKYSALHAKPNGLILQYGTAGFRTKAEHLDHVMFRMGLLAVLRSKQTKSTIGVMVTASHNPEEDNGVKLVDPLGEMLAPSWEEHATCLANAEEQDMQRVLIDISEKEAVNLQQDAFVVIGRDTRPSSEKLSQSVIDGVTVLGGQFHDYGLLTTPQLHYMVYCRNTGGRYGKATIEGYYQKLSKAFVELTKQASCSGDEYRSLKVDCANGIGALKLREMEHYFSQGLSVQLFNDGSKGKLNHLCGADFVKSHQKPPQGMEIKSNERCCSFDGDADRIVYYYHDADGHFHLIDGDKIATLISSFLKELLVEIGESLNIGVVQTAYANGSSTRYLEEVMKVPVYCTKTGVKHLHHKAQEFDIGVYFEANGHGTALFSTAVEMKIKQSAEQLEDKKRKAAKMLENIIDLFNQAAGDAISDMLVIEAILALKGLTVQQWDALYTDLPNRQLKVQVADRRVISTTDAERQAVTPPGLQEAINDLVKKYKLSRAFVRPSGTEDVVRVYAEADSQESADHLAHEVSLAVFQLAGGIGERPQPGF
466	Q9H9G7	>sp|Q9H9G7|AGO3_HUMAN Protein argonaute-3 GN=AGO3 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MEIGSAGPAGAQPLLMVPRRPGYGTMGKPIKLLANCFQVEIPKIDVYLYEVDIKPDKCPRRVNREVVDSMVQHFKVTIFGDRRPVYDGKRSLYTANPLPVATTGVDLDVTLPGEGGKDRPFKVSIKFVSRVSWHLLHEVLTGRTLPEPLELDKPISTNPVHAVDVVLRHLPSMKYTPVGRSFFSAPEGYDHPLGGGREVWFGFHQSVRPAMWKMMLNIDVSATAFYKAQPVIQFMCEVLDIHNIDEQPRPLTDSHRVKFTKEIKGLKVEVTHCGTMRRKYRVCNVTRRPASHQTFPLQLENGQTVERTVAQYFREKYTLQLKYPHLPCLQVGQEQKHTYLPLEVCNIVAGQRCIKKLTDNQTSTMIKATARSAPDRQEEISRLVRSANYETDPFVQEFQFKVRDEMAHVTGRVLPAPMLQYGGRNRTVATPSHGVWDMRGKQFHTGVEIKMWAIACFATQRQCREEILKGFTDQLRKISKDAGMPIQGQPCFCKYAQGADSVEPMFRHLKNTYSGLQLIIVILPGKTPVYAEVKRVGDTLLGMATQCVQVKNVIKTSPQTLSNLCLKINVKLGGINNILVPHQRPSVFQQPVIFLGADVTHPPAGDGKKPSIAAVVGSMDAHPSRYCATVRVQRPRQEIIQDLASMVRELLIQFYKSTRFKPTRIIFYRDGVSEGQFRQVLYYELLAIREACISLEKDYQPGITYIVVQKRHHTRLFCADRTERVGRSGNIPAGTTVDTDITHPYEFDFYLCSHAGIQGTSRPSHYHVLWDDNCFTADELQLLTYQLCHTYVRCTRSVSIPAPAYYAHLVAFRARYHLVDKEHDSAEGSHVSGQSNGRDPQALAKAVQIHQDTLRTMYFA
467	Q86SQ6	>sp|Q86SQ6|AGRA1_HUMAN Adhesion G protein-coupled receptor A1 GN=ADGRA1 PE=2 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MDLKTVLSLPRYPGEFLHPVVYACTAVMLLCLLASFVTYIVHQSAIRISRKGRHTLLNFCFHAALTFTVFAGGINRTKYPILCQAVGIVLHYSTLSTMLWIGVTARNIYKQVTKKAPLCLDTDQPPYPRQPLLRFYLVSGGVPFIICGVTAATNIRNYGTEDEDTAYCWMAWEPSLGAFYGPAAIITLVTCVYFLGTYVQLRRHPGRRYELRTQPEEQRRLATPEGGRGIRPGTPPAHDAPGASVLQNEHSFQAQLRAAAFTLFLFTATWAFGALAVSQGHFLDMVFSCLYGAFCVTLGLFVLIHHCAKREDVWQCWWACCPPRKDAHPALDANGAALGRAACLHSPGLGQPRGFAHPPGPCKMTNLQAAQGHASCLSPATPCCAKMHCEPLTADEAHVHLQEEGAFGHDPHLHGCLQGRTKPPYFSRHPAEEPEYAYHIPSSLDGSPRSSRTDSPPSSLDGPAGTHTLACCTQGDPFPMVTQPEGSDGSPALYSCPTQPGREAALGPGHLEMLRRTQSLPFGGPSQNGLPKGKLLEGLPFGTDGTGNIRTGPWKNETTV
468	O60241	>sp|O60241|AGRB2_HUMAN Adhesion G protein-coupled receptor B2 GN=ADGRB2 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MENTGWMGKGHRMTPACPLLLSVILSLRLATAFDPAPSACSALASGVLYGAFSLQDLFPTIASGCSWTLENPDPTKYSLYLRFNRQEQVCAHFAPRLLPLDHYLVNFTCLRPSPEEAVAQAESEVGRPEEEEAEAAAGLELCSGSGPFTFLHFDKNFVQLCLSAEPSEAPRLLAPAALAFRFVEVLLINNNNSSQFTCGVLCRWSEECGRAAGRACGFAQPGCSCPGEAGAGSTTTTSPGPPAAHTLSNALVPGGPAPPAEADLHSGSSNDLFTTEMRYGEEPEEEPKVKTQWPRSADEPGLYMAQTGDPAAEEWSPWSVCSLTCGQGLQVRTRSCVSSPYGTLCSGPLRETRPCNNSATCPVHGVWEEWGSWSLCSRSCGRGSRSRMRTCVPPQHGGKACEGPELQTKLCSMAACPVEGQWLEWGPWGPCSTSCANGTQQRSRKCSVAGPAWATCTGALTDTRECSNLECPATDSKWGPWNAWSLCSKTCDTGWQRRFRMCQATGTQGYPCEGTGEEVKPCSEKRCPAFHEMCRDEYVMLMTWKKAAAGEIIYNKCPPNASGSASRRCLLSAQGVAYWGLPSFARCISHEYRYLYLSLREHLAKGQRMLAGEGMSQVVRSLQELLARRTYYSGDLLFSVDILRNVTDTFKRATYVPSADDVQRFFQVVSFMVDAENKEKWDDAQQVSPGSVHLLRVVEDFIHLVGDALKAFQSSLIVTDNLVISIQREPVSAVSSDITFPMRGRRGMKDWVRHSEDRLFLPKEVLSLSSPGKPATSGAAGSPGRGRGPGTVPPGPGHSHQRLLPADPDESSYFVIGAVLYRTLGLILPPPRPPLAVTSRVMTVTVRPPTQPPAEPLITVELSYIINGTTDPHCASWDYSRADASSGDWDTENCQTLETQAAHTRCQCQHLSTFAVLAQPPKDLTLELAGSPSVPLVIGCAVSCMALLTLLAIYAAFWRFIKSERSIILLNFCLSILASNILILVGQSRVLSKGVCTMTAAFLHFFFLSSFCWVLTEAWQSYLAVIGRMRTRLVRKRFLCLGWGLPALVVAVSVGFTRTKGYGTSSYCWLSLEGGLLYAFVGPAAVIVLVNMLIGIIVFNKLMARDGISDKSKKQRAGSERCPWASLLLPCSACGAVPSPLLSSASARNAMASLWSSCVVLPLLALTWMSAVLAMTDRRSVLFQALFAVFNSAQGFVITAVHCFLRREVQDVVKCQMGVCRADESEDSPDSCKNGQLQILSDFEKDVDLACQTVLFKEVNTCNPSTITGTLSRLSLDEDEEPKSCLVGPEGSLSFSPLPGNILVPMAASPGLGEPPPPQEANPVYMCGEGGLRQLDLTWLRPTEPGSEGDYMVLPRRTLSLQPGGGGGGGEDAPRARPEGTPRRAAKTVAHTEGYPSFLSVDHSGLGLGPAYGSLQNPYGMTFQPPPPTPSARQVPEPGERSRTMPRTVPGSTMKMGSLERKKLRYSDLDFEKVMHTRKRHSELYHELNQKFHTFDRYRSQSTAKREKRWSVSSGGAAERSVCTDKPSPGERPSLSQHRRHQSWSTFKSMTLGSLPPKPRERLTLHRAAAWEPTEPPDGDFQTEV
469	P50052	>sp|P50052|AGTR2_HUMAN Type-2 angiotensin II receptor GN=AGTR2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MKGNSTLATTSKNITSGLHFGLVNISGNNESTLNCSQKPSDKHLDAIPILYYIIFVIGFLVNIVVVTLFCCQKGPKKVSSIYIFNLAVADLLLLATLPLWATYYSYRYDWLFGPVMCKVFGSFLTLNMFASIFFITCMSVDRYQSVIYPFLSQRRNPWQASYIVPLVWCMACLSSLPTFYFRDVRTIEYLGVNACIMAFPPEKYAQWSAGIALMKNILGFIIPLIFIATCYFGIRKHLLKTNSYGKNRITRDQVLKMAAAVVLAFIICWLPFHVLTFLDALAWMGVINSCEVIAVIDLALPFAILLGFTNSCVNPFLYCFVGNRFQQKLRSVFRVPITWLQGKRESMSCRKSSSLREMETFVS
470	P35869	>sp|P35869|AHR_HUMAN Aryl hydrocarbon receptor GN=AHR PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MNSSSANITYASRKRRKPVQKTVKPIPAEGIKSNPSKRHRDRLNTELDRLASLLPFPQDVINKLDKLSVLRLSVSYLRAKSFFDVALKSSPTERNGGQDNCRAANFREGLNLQEGEFLLQALNGFVLVVTTDALVFYASSTIQDYLGFQQSDVIHQSVYELIHTEDRAEFQRQLHWALNPSQCTESGQGIEEATGLPQTVVCYNPDQIPPENSPLMERCFICRLRCLLDNSSGFLAMNFQGKLKYLHGQKKKGKDGSILPPQLALFAIATPLQPPSILEIRTKNFIFRTKHKLDFTPIGCDAKGRIVLGYTEAELCTRGSGYQFIHAADMLYCAESHIRMIKTGESGMIVFRLLTKNNRWTWVQSNARLLYKNGRPDYIIVTQRPLTDEEGTEHLRKRNTKLPFMFTTGEAVLYEATNPFPAIMDPLPLRTKNGTSGKDSATTSTLSKDSLNPSSLLAAMMQQDESIYLYPASSTSSTAPFENNFFNESMNECRNWQDNTAPMGNDTILKHEQIDQPQDVNSFAGGHPGLFQDSKNSDLYSIMKNLGIDFEDIRHMQNEKFFRNDFSGEVDFRDIDLTDEILTYVQDSLSKSPFIPSDYQQQQSLALNSSCMVQEHLHLEQQQQHHQKQVVVEPQQQLCQKMKHMQVNGMFENWNSNQFVPFNCPQQDPQQYNVFTDLHGISQEFPYKSEMDSMPYTQNFISCNQPVLPQHSKCTELDYPMGSFEPSPYPTTSSLEDFVTCLQLPENQKHGLNPQSAIITPQTCYAGAVSMYQCQPEPQHTHVGQMQYNPVLPGQQAFLNKFQNGVLNETYPAELNNINNTQTTTHLQPLHHPSEARPFPDLTSSGFL
471	Q86UN6	>sp|Q86UN6|AKA28_HUMAN A-kinase anchor protein 14 GN=AKAP14 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MSETQNSTSQKAMDEDNKAASQTMPNTQDKNYEDELTQVALALVEDVINYAVKIVEEERNPLKNIKWMTHGEFTVEKGLKQIDEYFSKCVSKKCWAHGVEFVERKDLIHSFLYIYYVHWSISTADLPVARISAGTYFTMKVSKTKPPDAPIVVSYVGDHQALVHRPGMVRFRENWQKNLTDAKYSFMESFPFLFNRV
472	Q9P0M2	>sp|Q9P0M2|AKA7G_HUMAN A-kinase anchor protein 7 isoform gamma GN=AKAP7 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MERPEAGGINSNECENVSRKKKMSEEFEANTMDSLVDMPFATVDIQDDCGITDEPQINLKRSQENEWVKSDQVKKRKKKRKDYQPNYFLSIPITNKEIIKGIKILQNAIIQQDERLAKAMVSDGSFHITLLVMQLLNEDEVNIGIDALLELKPFIEELLQGKHLTLPFQGIGTFGNQVGFVKLAEGDHVNSLLEIAETANRTFQEKGILVGESRSFKPHLTFMKLSKSPWLRKNGVKKIDPDLYEKFISHRFGEEILYRIDLCSMLKKKQSNGYYHCESSIVIGEKNGGEPDDAELVRLSKRLVENAVLKAVQQYLEETQNKNKPGEGSSVKTEAADQNGNDNENNRK
473	Q92667	>sp|Q92667|AKAP1_HUMAN A-kinase anchor protein 1, mitochondrial GN=AKAP1 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MAIQFRSLFPLALPGMLALLGWWWFFSRKKGHVSSHDEQQVEAGAVQLRADPAIKEPLPVEDVCPKVVSTPPSVTEPPEKELSTVSKLPAEPPALLQTHPPCRRSESSGILPNTTDMRLRPGTRRDDSTKLELALTGGEAKSIPLECPLSSPKGVLFSSKSAEVCKQDSPFSRVPRKVQPGYPVVPAEKRSSGERARETGGAEGTGDAVLGEKVLEEALLSREHVLELENSKGPSLASLEGEEDKGKSSSSQVVGPVQEEEYVAEKLPSRFIESAHTELAKDDAAPAPPVADAKAQDRGVEGELGNEESLDRNEEGLDRNEEGLDRNEESLDRNEEGLDRNEEIKRAAFQIISQVISEATEQVLATTVGKVAGRVCQASQLQGQKEESCVPVHQKTVLGPDTAEPATAEAAVAPPDAGLPLPGLPAEGSPPPKTYVSCLKSLLSSPTKDSKPNISAHHISLASCLALTTPSEELPDRAGILVEDATCVTCMSDSSQSVPLVASPGHCSDSFSTSGLEDSCTETSSSPRDKAITPPLPESTVPFSNGVLKGELSDLGAEDGWTMDAEADHSGGSDRNSMDSVDSCCSLKKTESFQNAQAGSNPKKVDLIIWEIEVPKHLVGRLIGKQGRYVSFLKQTSGAKIYISTLPYTQSVQICHIEGSQHHVDKALNLIGKKFKELNLTNIYAPPLPSLALPSLPMTSWLMLPDGITVEVIVVNQVNAGHLFVQQHTHPTFHALRSLDQQMYLCYSQPGIPTLPTPVEITVICAAPGADGAWWRAQVVASYEETNEVEIRYVDYGGYKRVKVDVLRQIRSDFVTLPFQGAEVLLDSVMPLSDDDQFSPEADAAMSEMTGNTALLAQVTSYSPTGLPLIQLWSVVGDEVVLINRSLVERGLAQWVDSYYTSL
474	A6NHY2	>sp|A6NHY2|AKD1B_HUMAN Ankyrin repeat and death domain-containing protein 1B GN=ANKDD1B PE=3 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MDPAGRARGQGATAGGLLLRAAAAAKGLREDLWGAAALPWRSLSRIPKREGLGEEDTAVAGHELLLPNERSFQNAAKSNNLDLMEKLFEKKVNINVVNNMNRTALHFAVGRNHLSAVDFLLKHKARVDVADKHGLTVIHLAAWSGSLEVMLMLVKAGADQRAKNQDGMSALHFATQSNHVRIVEYLIQDLHLKDLNQPDEKGRKPFLLAAERGHVEMIEKLTFLNLHTSEKDKGGNTALHLAAKHGHSPAVQVLLAQWQDINEMNELNISSLQIATRNGHASLVNFLLSENVDLHQKVEPKESPLHLVVINNHITVVNSLLSAQHDIDILNQKQQTPLHVAADRGNVELVETLLKAGCDLKAVDKQGKTALAVASRSNHSLVVGMLIKAERYYAWREEHHESIRDPSTGFTLTFKQDHSLETRHIRTLLWDLAYHQLKANEWQRLARSWNFTDDQIRAIEEQWSGNESFREHGHRALLIWLHGTLMTQGDPAKQLYEELVHAGFPKLAEKTRHFKSKTDSNSKKCVVS
475	Q53H80	>sp|Q53H80|AKIR2_HUMAN Akirin-2 GN=AKIRIN2 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MACGATLKRTLDFDPLLSPASPKRRRCAPLSAPTSAAASPLSAAAATAASFSAAAASPQKYLRMEPSPFGDVSSRLTTEQILYNIKQEYKRMQKRRHLETSFQQTDPCCTSDAQPHAFLLSGPASPGTSSAASSPLKKEQPLFTLRQVGMICERLLKEREEKVREEYEEILNTKLAEQYDAFVKFTHDQIMRRYGEQPASYVS
476	Q5T1N1	>sp|Q5T1N1|AKND1_HUMAN Protein AKNAD1 GN=AKNAD1 PE=2 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MDEADFSEHTTYKQEDLPYDGDLSQIKIGNDYSFTSKKDGLEVLNQIIFIADDPQEKAMHSETCGNTAVTIPLGKITENAANKKDEKEKQCTAALHIPANEGDASKSSISDILLHHLSKEPFLRGQGIDCETLPEISNADSFEEEAIIKSIISCYNKNSWPKEQTPELTDQLNPKRDGENSNKPGSATTTEENTSDLEGPVAAGDSSHQENVNVLTKTKGPGDKQKSYQGQSPQKQQTEKANSGNTFKYGQGQVHYQLPDFSKIAPKVKIPKNKIINKPLAIAKQASFSSKSRDKPTLVQDSLETTPESNCVEKQHQEQKGKITEPSQQIQMEPIVHIHQELLTGIESEASLSKLSPTSQKGTSSSSSYIFQKISQGKQMCQKLKEQTDQLKTKVQEFSKRIKQDSPYHLQDKKLVLEKLQGHLELLEQNFLATKDKHLTLQQQVHKHESTIVGDFDPERKVEGEIFKLEMLLEDVKEKMDESKYTSAPSLPVSSPVTLDDLASTFSSLSNEIPKEHPGHPSGPRGSGGSEVTGTPQGGPQEAPNEELCELAPQTYLNGHYGDAAAQNKPDQVAMRLSSNSGEDPNGTPRRQDCAEMTAPSPSCAFCRRLLEWKQNVEKKGHGRINCGRFSIVLHEKAPHSDSTPNSDTGHSFCSDSGTEMQSNKCQDCGTKIPTSRRACRKEPTKEFHYRYNTPGQNYSNHSKRGAFVQPHSLDESKNSSPSFLKPKRICSQRVNSKSFKGEHEPTPGKKKLQAFMTYSSDPATPSPHFYSCRISGSKSLCDFDSTEEIKSEILNSALDHALRTATILKETTDQMIKTIAEDLAKAQRWRNRLKY
477	P00352	>sp|P00352|AL1A1_HUMAN Retinal dehydrogenase 1 GN=ALDH1A1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MSSSGTPDLPVLLTDLKIQYTKIFINNEWHDSVSGKKFPVFNPATEEELCQVEEGDKEDVDKAVKAARQAFQIGSPWRTMDASERGRLLYKLADLIERDRLLLATMESMNGGKLYSNAYLNDLAGCIKTLRYCAGWADKIQGRTIPIDGNFFTYTRHEPIGVCGQIIPWNFPLVMLIWKIGPALSCGNTVVVKPAEQTPLTALHVASLIKEAGFPPGVVNIVPGYGPTAGAAISSHMDIDKVAFTGSTEVGKLIKEAAGKSNLKRVTLELGGKSPCIVLADADLDNAVEFAHHGVFYHQGQCCIAASRIFVEESIYDEFVRRSVERAKKYILGNPLTPGVTQGPQIDKEQYDKILDLIESGKKEGAKLECGGGPWGNKGYFVQPTVFSNVTDEMRIAKEEIFGPVQQIMKFKSLDDVIKRANNTFYGLSAGVFTKDIDKAITISSALQAGTVWVNCYGVVSAQCPFGGFKMSGNGRELGEYGFHEYTEVKTVTVKISQKNS
478	P36544	>sp|P36544|ACHA7_HUMAN Neuronal acetylcholine receptor subunit alpha-7 GN=CHRNA7 PE=1 SV=5 Homo sapiens OS=Human NCBI_TaxID=9606	MRCSPGGVWLALAASLLHVSLQGEFQRKLYKELVKNYNPLERPVANDSQPLTVYFSLSLLQIMDVDEKNQVLTTNIWLQMSWTDHYLQWNVSEYPGVKTVRFPDGQIWKPDILLYNSADERFDATFHTNVLVNSSGHCQYLPPGIFKSSCYIDVRWFPFDVQHCKLKFGSWSYGGWSLDLQMQEADISGYIPNGEWDLVGIPGKRSERFYECCKEPYPDVTFTVTMRRRTLYYGLNLLIPCVLISALALLVFLLPADSGEKISLGITVLLSLTVFMLLVAEIMPATSDSVPLIAQYFASTMIIVGLSVVVTVIVLQYHHHDPDGGKMPKWTRVILLNWCAWFLRMKRPGEDKVRPACQHKQRRCSLASVEMSAVAPPPASNGNLLYIGFRGLDGVHCVPTPDSGVVCGRMACSPTHDEHLLHGGQPPEGDPDLAKILEEVRYIANRFRCQDESEAVCSEWKFAACVVDRLCLMAFSVFTIICTIGILMSAPNFVEAVSKDFA
479	P17787	>sp|P17787|ACHB2_HUMAN Neuronal acetylcholine receptor subunit beta-2 GN=CHRNB2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MARRCGPVALLLGFGLLRLCSGVWGTDTEERLVEHLLDPSRYNKLIRPATNGSELVTVQLMVSLAQLISVHEREQIMTTNVWLTQEWEDYRLTWKPEEFDNMKKVRLPSKHIWLPDVVLYNNADGMYEVSFYSNAVVSYDGSIFWLPPAIYKSACKIEVKHFPFDQQNCTMKFRSWTYDRTEIDLVLKSEVASLDDFTPSGEWDIVALPGRRNENPDDSTYVDITYDFIIRRKPLFYTINLIIPCVLITSLAILVFYLPSDCGEKMTLCISVLLALTVFLLLISKIVPPTSLDVPLVGKYLMFTMVLVTFSIVTSVCVLNVHHRSPTTHTMAPWVKVVFLEKLPALLFMQQPRHHCARQRLRLRRRQREREGAGALFFREAPGADSCTCFVNRASVQGLAGAFGAEPAPVAGPGRSGEPCGCGLREAVDGVRFIADHMRSEDDDQSVSEDWKYVAMVIDRLFLWIFVFVCVFGTIGMFLQPLFQNYTTTTFLHSDHSAPSSK
480	Q04844	>sp|Q04844|ACHE_HUMAN Acetylcholine receptor subunit epsilon GN=CHRNE PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MARAPLGVLLLLGLLGRGVGKNEELRLYHHLFNNYDPGSRPVREPEDTVTISLKVTLTNLISLNEKEETLTTSVWIGIDWQDYRLNYSKDDFGGIETLRVPSELVWLPEIVLENNIDGQFGVAYDANVLVYEGGSVTWLPPAIYRSVCAVEVTYFPFDWQNCSLIFRSQTYNAEEVEFTFAVDNDGKTINKIDIDTEAYTENGEWAIDFCPGVIRRHHGGATDGPGETDVIYSLIIRRKPLFYVINIIVPCVLISGLVLLAYFLPAQAGGQKCTVSINVLLAQTVFLFLIAQKIPETSLSVPLLGRFLIFVMVVATLIVMNCVIVLNVSQRTPTTHAMSPRLRHVLLELLPRLLGSPPPPEAPRAASPPRRASSVGLLLRAEELILKKPRSELVFEGQRHRQGTWTAAFCQSLGAAAPEVRCCVDAVNFVAESTRDQEATGEEVSDWVRMGNALDNICFWAALVLFSVGSSLIFLGAYFNRVPDLPYAPCIQP
481	Q5JWF8	>sp|Q5JWF8|ACL10_HUMAN Actin-like protein 10 GN=ACTL10 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MASTALLALCSTGAFSGLAVEAGAGVCHATPIYAGHSWHQATFRLNVAGSTLSRYLRDLLVAANPDLLQQALPRKAITHLKKRSCYVSLDFEGDLRDPARHHPASFSVGNGCCVCLSSERFRCPEPIFQPGLLGQAEQGLPALAFRALQKMPKTLRTRLADTVVLAGGSTLFPGFAERLDKELEAQCRRHGYAALRPHLVAKHGRGMAVWTGGSMVASLHSFQRRWITRAMYQECGSRLLYDVFN
482	P08912	>sp|P08912|ACM5_HUMAN Muscarinic acetylcholine receptor M5 GN=CHRM5 PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MEGDSYHNATTVNGTPVNHQPLERHRLWEVITIAAVTAVVSLITIVGNVLVMISFKVNSQLKTVNNYYLLSLACADLIIGIFSMNLYTTYILMGRWALGSLACDLWLALDYVASNASVMNLLVISFDRYFSITRPLTYRAKRTPKRAGIMIGLAWLISFILWAPAILCWQYLVGKRTVPLDECQIQFLSEPTITFGTAIAAFYIPVSVMTILYCRIYRETEKRTKDLADLQGSDSVTKAEKRKPAHRALFRSCLRCPRPTLAQRERNQASWSSSRRSTSTTGKPSQATGPSANWAKAEQLTTCSSYPSSEDEDKPATDPVLQVVYKSQGKESPGEEFSAEETEETFVKAETEKSDYDTPNYLLSPAAAHRPKSQKCVAYKFRLVVKADGNQETNNGCHKVKIMPCPFPVAKEPSTKGLNPNPSHQMTKRKRVVLVKERKAAQTLSAILLAFIITWTPYNIMVLVSTFCDKCVPVTLWHLGYWLCYVNSTVNPICYALCNRTFRKTFKMLLLCRWKKKKVEEKLYWQGNSKLP
483	P49753	>sp|P49753|ACOT2_HUMAN Acyl-coenzyme A thioesterase 2, mitochondrial GN=ACOT2 PE=1 SV=6 Homo sapiens OS=Human NCBI_TaxID=9606	MSNKLLSPHPHSVVLRSEFKMASSPAVLRASRLYQWSLKSSAQFLGSPQLRQVGQIIRVPARMAATLILEPAGRCCWDEPVRIAVRGLAPEQPVTLRASLRDEKGALFQAHARYRADTLGELDLERAPALGGSFAGLEPMGLLWALEPEKPLVRLVKRDVRTPLAVELEVLDGHDPDPGRLLCQTRHERYFLPPGVRREPVRVGRVRGTLFLPPEPGPFPGIVDMFGTGGGLLEYRASLLAGKGFAVMALAYYNYEDLPKTMETLHLEYFEEAMNYLLSHPEVKGPGVGLLGISKGGELCLSMASFLKGITAAVVINGSVANVGGTLHYKGETLPPVGVNRNRIKVTKDGYADIVDVLNSPLEGPDQKSFIPVERAESTFLFLVGQDDHNWKSEFYANEACKRLQAHGRRKPQIICYPETGHYIEPPYFPLCRASLHALVGSPIIWGGEPRAHAMAQVDAWKQLQTFFHKHLGGHEGTIPSKV
484	O14734	>sp|O14734|ACOT8_HUMAN Acyl-coenzyme A thioesterase 8 GN=ACOT8 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MSSPQAPEDGQGCGDRGDPPGDLRSVLVTTVLNLEPLDEDLFRGRHYWVPAKRLFGGQIVGQALVAAAKSVSEDVHVHSLHCYFVRAGDPKLPVLYQVERTRTGSSFSVRSVKAVQHGKPIFICQASFQQAQPSPMQHQFSMPTVPPPEELLDCETLIDQYLRDPNLQKRYPLALNRIAAQEVPIEIKPVNPSPLSQLQRMEPKQMFWVRARGYIGEGDMKMHCCVAAYISDYAFLGTALLPHQWQHKVHFMVSLDHSMWFHAPFRADHWMLYECESPWAGGSRGLVHGRLWRQDGVLAVTCAQEGVIRVKPQVSESKL
485	Q6ZNF0	>sp|Q6ZNF0|ACP7_HUMAN Acid phosphatase type 7 GN=ACP7 PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MHPLPGYWSCYCLLLLFSLGVQGSLGAPSAAPEQVHLSYPGEPGSMTVTWTTWVPTRSEVQFGLQPSGPLPLRAQGTFVPFVDGGILRRKLYIHRVTLRKLLPGVQYVYRCGSAQGWSRRFRFRALKNGAHWSPRLAVFGDLGADNPKAVPRLRRDTQQGMYDAVLHVGDFAYNLDQDNARVGDRFMRLIEPVAASLPYMTCPGNHEERYNFSNYKARFSMPGDNEGLWYSWDLGPAHIISFSTEVYFFLHYGRHLVQRQFRWLESDLQKANKNRAARPWIITMGHRPMYCSNADLDDCTRHESKVRKGLQGKLYGLEDLFYKYGVDLQLWAHEHSYERLWPIYNYQVFNGSREMPYTNPRGPVHIITGSAGCEERLTPFAVFPRPWSAVRVKEYGYTRLHILNGTHIHIQQVSDDQDGKIVDDVWVVRPLFGRRMYL
486	Q08AH3	>sp|Q08AH3|ACS2A_HUMAN Acyl-coenzyme A synthetase ACSM2A, mitochondrial GN=ACSM2A PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MHWLRKVQGLCTLWGTQMSSRTLYINSRQLVSLQWGHQEVPAKFNFASDVLDHWADMEKAGKRLPSPALWWVNGKGKELMWNFRELSENSQQAANVLSGACGLQRGDRVAVVLPRVPEWWLVILGCIRAGLIFMPGTIQMKSTDILYRLQMSKAKAIVAGDEVIQEVDTVASECPSLRIKLLVSEKSCDGWLNFKKLLNEASTTHHCVETGSQEASAIYFTSGTSGLPKMAEHSYSSLGLKAKMDAGWTGLQASDIMWTISDTGWILNILCSLMEPWALGACTFVHLLPKFDPLVILKTLSSYPIKSMMGAPIVYRMLLQQDLSSYKFPHLQNCVTVGESLLPETLENWRAQTGLDIRESYGQTETGLTCMVSKTMKIKPGYMGTAASCYDVQIIDDKGNVLPPGTEGDIGIRVKPIRPIGIFSGYVDNPDKTAANIRGDFWLLGDRGIKDEDGYFQFMGRANDIINSSGYRIGPSEVENALMEHPAVVETAVISSPDPVRGEVVKAFVVLASQFLSHDPEQLTKELQQHVKSVTAPYKYPRKIEFVLNLPKTVTGKIQRAKLRDKEWKMSGKARAQ
487	Q4G176	>sp|Q4G176|ACSF3_HUMAN Acyl-CoA synthetase family member 3, mitochondrial GN=ACSF3 PE=1 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MLPHVVLTFRRLGCALASCRLAPARHRGSGLLHTAPVARSDRSAPVFTRALAFGDRIALVDQHGRHTYRELYSRSLRLSQEICRLCGCVGGDLREERVSFLCANDASYVVAQWASWMSGGVAVPLYRKHPAAQLEYVICDSQSSVVLASQEYLELLSPVVRKLGVPLLPLTPAIYTGAVEEPAEVPVPEQGWRNKGAMIIYTSGTTGRPKGVLSTHQNIRAVVTGLVHKWAWTKDDVILHVLPLHHVHGVVNALLCPLWVGATCVMMPEFSPQQVWEKFLSSETPRINVFMAVPTIYTKLMEYYDRHFTQPHAQDFLRAVCEEKIRLMVSGSAALPLPVLEKWKNITGHTLLERYGMTEIGMALSGPLTTAVRLPGSVGTPLPGVQVRIVSENPQREACSYTIHAEGDERGTKVTPGFEEKEGELLVRGPSVFREYWNKPEETKSAFTLDGWFKTGDTVVFKDGQYWIRGRTSVDIIKTGGYKVSALEVEWHLLAHPSITDVAVIGVPDMTWGQRVTAVVTLREGHSLSHRELKEWARNVLAPYAVPSELVLVEEIPRNQMGKIDKKALIRHFHPS
488	Q9ULC5	>sp|Q9ULC5|ACSL5_HUMAN Long-chain-fatty-acid--CoA ligase 5 GN=ACSL5 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MLFIFNFLFSPLPTPALICILTFGAAIFLWLITRPQPVLPLLDLNNQSVGIEGGARKGVSQKNNDLTSCCFSDAKTMYEVFQRGLAVSDNGPCLGYRKPNQPYRWLSYKQVSDRAEYLGSCLLHKGYKSSPDQFVGIFAQNRPEWIISELACYTYSMVAVPLYDTLGPEAIVHIVNKADIAMVICDTPQKALVLIGNVEKGFTPSLKVIILMDPFDDDLKQRGEKSGIEILSLYDAENLGKEHFRKPVPPSPEDLSVICFTSGTTGDPKGAMITHQNIVSNAAAFLKCVEHAYEPTPDDVAISYLPLAHMFERIVQAVVYSCGARVGFFQGDIRLLADDMKTLKPTLFPAVPRLLNRIYDKVQNEAKTPLKKFLLKLAVSSKFKELQKGIIRHDSFWDKLIFAKIQDSLGGRVRVIVTGAAPMSTSVMTFFRAAMGCQVYEAYGQTECTGGCTFTLPGDWTSGHVGVPLACNYVKLEDVADMNYFTVNNEGEVCIKGTNVFKGYLKDPEKTQEALDSDGWLHTGDIGRWLPNGTLKIIDRKKNIFKLAQGEYIAPEKIENIYNRSQPVLQIFVHGESLRSSLVGVVVPDTDVLPSFAAKLGVKGSFEELCQNQVVREAILEDLQKIGKESGLKTFEQVKAIFLHPEPFSIENGLLTPTLKAKRGELSKYFRTQIDSLYEHIQD
489	Q6P461	>sp|Q6P461|ACSM6_HUMAN Acyl-coenzyme A synthetase ACSM6, mitochondrial GN=ACSM6 PE=2 SV=3 Homo sapiens OS=Human NCBI_TaxID=9606	MLGRFQPFSLVRSFRLGFEACCYPNQKCATQTIRPPDSRCLVQAVSQNFNFAKDVLDQWSQLEKDGLRGPYPALWKVSAKGEEDKWSFERMTQLSKKAASILSDTCALSHGDRLMIILPPTPEAYWICLACVRLGITFVPGSPQLTAKKIRYQLRMSKAQCIVANEAMAPVVNSAVSDCPTLKTKLLVSDKSYDGWLDFKKLIQVAPPKQTYMRTKSQDPMAIFFTKGTTGAPKMVEYSQYGLGMGFSQASRRWMDLQPTDVLWSLGDAFGGSLSLSAVLGTWFQGACVFLCHMPTFCPETVLNVLSRFPITTLSANPEMYQELLQHKCFTSYRFKSLKQCVAAGGPISPGVIEDWKRITKLDIYEGYGQTETGLLCATSKTIKLKPSSLGKPLPPYIVQIVDENSNLLPPGEEGNIAIRIKLNQPASLYCPHMVSWEEYASARGHMLYLTGDRGIMDEDGYFWWSGRVDDVANALGQRL
490	P35609	>sp|P35609|ACTN2_HUMAN Alpha-actinin-2 GN=ACTN2 PE=1 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MNQIEPGVQYNYVYDEDEYMIQEEEWDRDLLLDPAWEKQQRKTFTAWCNSHLRKAGTQIENIEEDFRNGLKLMLLLEVISGERLPKPDRGKMRFHKIANVNKALDYIASKGVKLVSIGAEEIVDGNVKMTLGMIWTIILRFAIQDISVEETSAKEGLLLWCQRKTAPYRNVNIQNFHTSWKDGLGLCALIHRHRPDLIDYSKLNKDDPIGNINLAMEIAEKHLDIPKMLDAEDIVNTPKPDERAIMTYVSCFYHAFAGAEQAETAANRICKVLAVNQENERLMEEYERLASELLEWIRRTIPWLENRTPEKTMQAMQKKLEDFRDYRRKHKPPKVQEKCQLEINFNTLQTKLRISNRPAFMPSEGKMVSDIAGAWQRLEQAEKGYEEWLLNEIRRLERLEHLAEKFRQKASTHETWAYGKEQILLQKDYESASLTEVRALLRKHEAFESDLAAHQDRVEQIAAIAQELNELDYHDAVNVNDRCQKICDQWDRLGTLTQKRREALERMEKLLETIDQLHLEFAKRAAPFNNWMEGAMEDLQDMFIVHSIEEIQSLITAHEQFKATLPEADGERQSIMAIQNEVEKVIQSYNIRISSSNPYSTVTMDELRTKWDKVKQLVPIRDQSLQEELARQHANERLRRQFAAQANAIGPWIQNKMEEIARSSIQITGALEDQMNQLKQYEHNIINYKNNIDKLEGDHQLIQEALVFDNKHTNYTMEHIRVGWELLLTTIARTINEVETQILTRDAKGITQEQMNEFRASFNHFDRRKNGLMDHEDFRACLISMGYDLGEAEFARIMTLVDPNGQGTVTFQSFIDFMTRETADTDTAEQVIASFRILASDKPYILAEELRRELPPDQAQYCIKRMPAYSGPGSVPGALDYAAFSSALYGESDL
491	Q08043	>sp|Q08043|ACTN3_HUMAN Alpha-actinin-3 GN=ACTN3 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MMMVMQPEGLGAGEGRFAGGGGGGEYMEQEEDWDRDLLLDPAWEKQQRKTFTAWCNSHLRKAGTQIENIEEDFRNGLKLMLLLEVISGERLPRPDKGKMRFHKIANVNKALDFIASKGVKLVSIGAEEIVDGNLKMTLGMIWTIILRFAIQDISVEETSAKEGLLLWCQRKTAPYRNVNVQNFHTSWKDGLALCALIHRHRPDLIDYAKLRKDDPIGNLNTAFEVAEKYLDIPKMLDAEDIVNTPKPDEKAIMTYVSCFYHAFAGAEQAETAANRICKVLAVNQENEKLMEEYEKLASELLEWIRRTVPWLENRVGEPSMSAMQRKLEDFRDYRRLHKPPRIQEKCQLEINFNTLQTKLRLSHRPAFMPSEGKLVSDIANAWRGLEQVEKGYEDWLLSEIRRLQRLQHLAEKFRQKASLHEAWTRGKEEMLSQRDYDSALLQEVRALLRRHEAFESDLAAHQDRVEHIAALAQELNELDYHEAASVNSRCQAICDQWDNLGTLTQKRRDALERMEKLLETIDRLQLEFARRAAPFNNWLDGAVEDLQDVWLVHSVEETQSLLTAHDQFKATLPEADRERGAIMGIQGEIQKICQTYGLRPCSTNPYITLSPQDINTKWDMVRKLVPSCDQTLQEELARQQVNERLRRQFAAQANAIGPWIQAKVEEVGRLAAGLAGSLEEQMAGLRQQEQNIINYKTNIDRLEGDHQLLQESLVFDNKHTVYSMEHIRVGWEQLLTSIARTINEVENQVLTRDAKGLSQEQLNEFRASFNHFDRKQNGMMEPDDFRACLISMGYDLGEVEFARIMTMVDPNAAGVVTFQAFIDFMTRETAETDTTEQVVASFKILAGDKNYITPEELRRELPAKQAEYCIRRMVPYKGSGAPAGALDYVAFSSALYGESDL
492	O43707	>sp|O43707|ACTN4_HUMAN Alpha-actinin-4 GN=ACTN4 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MVDYHAANQSYQYGPSSAGNGAGGGGSMGDYMAQEDDWDRDLLLDPAWEKQQRKTFTAWCNSHLRKAGTQIENIDEDFRDGLKLMLLLEVISGERLPKPERGKMRVHKINNVNKALDFIASKGVKLVSIGAEEIVDGNAKMTLGMIWTIILRFAIQDISVEETSAKEGLLLWCQRKTAPYKNVNVQNFHISWKDGLAFNALIHRHRPELIEYDKLRKDDPVTNLNNAFEVAEKYLDIPKMLDAEDIVNTARPDEKAIMTYVSSFYHAFSGAQKAETAANRICKVLAVNQENEHLMEDYEKLASDLLEWIRRTIPWLEDRVPQKTIQEMQQKLEDFRDYRRVHKPPKVQEKCQLEINFNTLQTKLRLSNRPAFMPSEGKMVSDINNGWQHLEQAEKGYEEWLLNEIRRLERLDHLAEKFRQKASIHEAWTDGKEAMLKHRDYETATLSDIKALIRKHEAFESDLAAHQDRVEQIAAIAQELNELDYYDSHNVNTRCQKICDQWDALGSLTHSRREALEKTEKQLEAIDQLHLEYAKRAAPFNNWMESAMEDLQDMFIVHTIEEIEGLISAHDQFKSTLPDADREREAILAIHKEAQRIAESNHIKLSGSNPYTTVTPQIINSKWEKVQQLVPKRDHALLEEQSKQQSNEHLRRQFASQANVVGPWIQTKMEEIGRISIEMNGTLEDQLSHLKQYERSIVDYKPNLDLLEQQHQLIQEALIFDNKHTNYTMEHIRVGWEQLLTTIARTINEVENQILTRDAKGISQEQMQEFRASFNHFDKDHGGALGPEEFKACLISLGYDVENDRQGEAEFNRIMSLVDPNHSGLVTFQAFIDFMSRETTDTDTADQVIASFKVLAGDKNFITAEELRRELPPDQAEYCIARMAPYQGPDAVPGALDYKSFSTALYGESDL
493	P07311	>sp|P07311|ACYP1_HUMAN Acylphosphatase-1 GN=ACYP1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAEGNTLISVDYEIFGKVQGVFFRKHTQAEGKKLGLVGWVQNTDRGTVQGQLQGPISKVRHMQEWLETRGSPKSHIDKANFNNEKVILKLDYSDFQIVK
494	Q13444	>sp|Q13444|ADA15_HUMAN Disintegrin and metalloproteinase domain-containing protein 15 GN=ADAM15 PE=1 SV=4 Homo sapiens OS=Human NCBI_TaxID=9606	MRLALLWALGLLGAGSPLPSWPLPNIGGTEEQQAESEKAPREPLEPQVLQDDLPISLKKVLQTSLPEPLRIKLELDGDSHILELLQNRELVPGRPTLVWYQPDGTRVVSEGHTLENCCYQGRVRGYAGSWVSICTCSGLRGLVVLTPERSYTLEQGPGDLQGPPIISRIQDLHLPGHTCALSWRESVHTQKPPEHPLGQRHIRRRRDVVTETKTVELVIVADHSEAQKYRDFQHLLNRTLEVALLLDTFFRPLNVRVALVGLEAWTQRDLVEISPNPAVTLENFLHWRRAHLLPRLPHDSAQLVTGTSFSGPTVGMAIQNSICSPDFSGGVNMDHSTSILGVASSIAHELGHSLGLDHDLPGNSCPCPGPAPAKTCIMEASTDFLPGLNFSNCSRRALEKALLDGMGSCLFERLPSLPPMAAFCGNMFVEPGEQCDCGFLDDCVDPCCDSLTCQLRPGAQCASDGPCCQNCQLRPSGWQCRPTRGDCDLPEFCPGDSSQCPPDVSLGDGEPCAGGQAVCMHGRCASYAQQCQSLWGPGAQPAAPLCLQTANTRGNAFGSCGRNPSGSYVSCTPRDAICGQLQCQTGRTQPLLGSIRDLLWETIDVNGTELNCSWVHLDLGSDVAQPLLTLPGTACGPGLVCIDHRCQRVDLLGAQECRSKCHGHGVCDSNRHCYCEEGWAPPDCTTQLKATSSLTTGLLLSLLVLLVLVMLGASYWYRARLHQRLCQLKGPTCQYRAAQSGPSERPGPPQRALLARGTKQASALSFPAPPSRPLPPDPVSKRLQAELADRPNPPTRPLPADPVVRSPKSQGPAKPPPPRKPLPADPQGRCPSGDLPGPGAGIPPLVVPSRPAPPPPTVSSLYL
495	P35348	>sp|P35348|ADA1A_HUMAN Alpha-1A adrenergic receptor GN=ADRA1A PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MVFLSGNASDSSNCTQPPAPVNISKAILLGVILGGLILFGVLGNILVILSVACHRHLHSVTHYYIVNLAVADLLLTSTVLPFSAIFEVLGYWAFGRVFCNIWAAVDVLCCTASIMGLCIISIDRYIGVSYPLRYPTIVTQRRGLMALLCVWALSLVISIGPLFGWRQPAPEDETICQINEEPGYVLFSALGSFYLPLAIILVMYCRVYVVAKRESRGLKSGLKTDKSDSEQVTLRIHRKNAPAGGSGMASAKTKTHFSVRLLKFSREKKAAKTLGIVVGCFVLCWLPFFLVMPIGSFFPDFKPSETVFKIVFWLGYLNSCINPIIYPCSSQEFKKAFQNVLRIQCLCRKQSSKHALGYTLHPPSQAVEGQHKDMVRIPVGSRETFYRISKTDGVCEWKFFSSMPRGSARITVSKDQSSCTTARVRSKSFLQVCCCVGPSTPSLDKNHQVPTIKVHTISLSENGEEV
496	P25100	>sp|P25100|ADA1D_HUMAN Alpha-1D adrenergic receptor GN=ADRA1D PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MTFRDLLSVSFEGPRPDSSAGGSSAGGGGGSAGGAAPSEGPAVGGVPGGAGGGGGVVGAGSGEDNRSSAGEPGSAGAGGDVNGTAAVGGLVVSAQGVGVGVFLAAFILMAVAGNLLVILSVACNRHLQTVTNYFIVNLAVADLLLSATVLPFSATMEVLGFWAFGRAFCDVWAAVDVLCCTASILSLCTISVDRYVGVRHSLKYPAIMTERKAAAILALLWVVALVVSVGPLLGWKEPVPPDERFCGITEEAGYAVFSSVCSFYLPMAVIVVMYCRVYVVARSTTRSLEAGVKRERGKASEVVLRIHCRGAATGADGAHGMRSAKGHTFRSSLSVRLLKFSREKKAAKTLAIVVGVFVLCWFPFFFVLPLGSLFPQLKPSEGVFKVIFWLGYFNSCVNPLIYPCSSREFKRAFLRLLRCQCRRRRRRRPLWRVYGHHWRASTSGLRQDCAPSSGDAPPGAPLALTALPDPDPEPPGTPEMQAPVASRRKPPSAFREWRLLGPFRRPTTQLRAKVSSLSHKIRAGGAQRAEAACAQRSEVEAVSLGVPHEVAEGATCQAYELADYSNLRETDI
497	Q9UKJ8	>sp|Q9UKJ8|ADA21_HUMAN Disintegrin and metalloproteinase domain-containing protein 21 GN=ADAM21 PE=2 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAVDGTLVYIRVTLLLLWLGVFLSISGYCQAGPSQHFTSPEVVIPLKVISRGRSAKAPGWLSYSLRFGGQKHVVHMRVKKLLVSRHLPVFTYTDDRALLEDQLFIPDDCYYHGYVEAAPESLVVFSACFGGFRGVLKISGLTYEIEPIRHSATFEHLVYKINSNETQFPAMRCGLTEKEVARQQLEFEEAENSALEPKSAGDWWTHAWFLELVVVVNHDFFIYSQSNISKVQEDVFLVVNIVDSMYKQLGTYIILIGIEIWNQGNVFPMTSIEQVLNDFSQWKQISLSQLQHDAAHMFIKNSLISILGLAYVAGICRPPIDCGVDNFQGDTWSLFANTVAHELGHTLGMQHDEEFCFCGERGCIMNTFRVPAEKFTNCSYADFMKTTLNQGSCLHNPPRLGEIFMLKRCGNGVVEREEQCDCGSVQQCEQDACCLLNCTLRPGAACAFGLCCKDCKFMPSGELCRQEVNECDLPEWCNGTSHQCPEDRYVQDGIPCSDSAYCYQKRCNNHDQHCREIFGKDAKSASQNCYKEINSQGNRFGHCGINGTTYLKCHISDVFCGRVQCENVRDIPLLQDHFTLQHTHINGVTCWGIDYHLRMNISDIGEVKDGTVCGPGKICIHKKCVSLSVLSHVCLPETCNMKGICNNKHHCHCGYGWSPPYCQHRGYGGSIDSGPASAKRGVFLPLIVIPSLSVLTFLFTVGLLMYLRQCSGPKETKAHSSG
498	Q8TC27	>sp|Q8TC27|ADA32_HUMAN Disintegrin and metalloproteinase domain-containing protein 32 GN=ADAM32 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MFRLWLLLAGLCGLLASRPGFQNSLLQIVIPEKIQTNTNDSSEIEYEQISYIIPIDEKLYTVHLKQRYFLADNFMIYLYNQGSMNTYSSDIQTQCYYQGNIEGYPDSMVTLSTCSGLRGILQFENVSYGIEPLESAVEFQHVLYKLKNEDNDIAIFIDRSLKEQPMDDNIFISEKSEPAVPDLFPLYLEMHIVVDKTLYDYWGSDSMIVTNKVIEIVGLANSMFTQFKVTIVLSSLELWSDENKISTVGEADELLQKFLEWKQSYLNLRPHDIAYLLIYMDYPRYLGAVFPGTMCITRYSAGVALYPKEITLEAFAVIVTQMLALSLGISYDDPKKCQCSESTCIMNPEVVQSNGVKTFSSCSLRSFQNFISNVGVKCLQNKPQMQKKSPKPVCGNGRLEGNEICDCGTEAQCGPASCCDFRTCVLKDGAKCYKGLCCKDCQILQSGVECRPKAHPECDIAENCNGTSPECGPDITLINGLSCKNNKFICYDGDCHDLDARCESVFGKGSRNAPFACYEEIQSQSDRFGNCGRDRNNKYVFCGWRNLICGRLVCTYPTRKPFHQENGDVIYAFVRDSVCITVDYKLPRTVPDPLAVKNGSQCDIGRVCVNRECVESRIIKASAHVCSQQCSGHGVCDSRNKCHCSPGYKPPNCQIRSKGFSIFPEEDMGSIMERASGKTENTWLLGFLIALPILIVTTAIVLARKQLKKWFAKEEEFPSSESKSEGSTQTYASQSSSEGSTQTYASQTRSESSSQADTSKSKSEDSAEAYTSRSKSQDSTQTQSSSN
499	Q8NCV1	>sp|Q8NCV1|ADAD2_HUMAN Adenosine deaminase domain-containing protein 2 GN=ADAD2 PE=2 SV=1 Homo sapiens OS=Human NCBI_TaxID=9606	MASASQGADDDGSRRKPRLAASLQISPQPRPWRPLPAQAQSAWGPAPAPATYRAEGGWPQVSVLRDSGPGAGAGVGELGAARAWENLGEQMGKAPRVPVPPAGLSLPLKDPPASQAVSLLTEYAASLGIFLLFREDQPPGPCFPFSVSAELDGVVCPAGTANSKTEAKQQAALSALCYIRSQLENPESPQTSSRPPLAPLSVENILTHEQRCAALVSAGFDLLLDERSPYWACKGTVAGVILEREIPRARGHVKEIYKLVALGTGSSCCAGWLEFSGQQLHDCHGLVIARRALLRFLFRQLLLATQGGPKGKEQSVLAPQPGPGPPFTLKPRVFLHLYISNTPKGAARDIYLPPTSEGGLPHSPPMRLQAHVLGQLKPVCYVAPSLCDTHVGCLSASDKLARWAVLGLGGALLAHLVSPLYSTSLILADSCHDPPTLSRAIHTRPCLDSVLGPCLPPPYVRTALHLFAGPPVAPSEPTPDTCRGLSLNWSLGDPGIEVVDVATGRVKANAALGPPSRLCKASFLRAFHQAARAVGKPYLLALKTYEAAKAGPYQEARRQLSLLLDQQGLGAWPSKPLVGKFRN
500	O75689	>sp|O75689|ADAP1_HUMAN Arf-GAP with dual PH domain-containing protein 1 GN=ADAP1 PE=1 SV=2 Homo sapiens OS=Human NCBI_TaxID=9606	MAKERRRAVLELLQRPGNARCADCGAPDPDWASYTLGVFICLSCSGIHRNIPQVSKVKSVRLDAWEEAQVEFMASHGNDAARARFESKVPSFYYRPTPSDCQLLREQWIRAKYERQEFIYPEKQEPYSAGYREGFLWKRGRDNGQFLSRKFVLTEREGALKYFNRNDAKEPKAVMKIEHLNATFQPAKIGHPHGLQVTYLKDNSTRNIFIYHEDGKEIVDWFNALRAARFHYLQVAFPGAGDADLVPKLSRNYLKEGYMEKTGPKQTEGFRKRWFTMDDRRLMYFKDPLDAFARGEVFIGSKESGYTVLHGFPPSTQGHHWPHGITIVTPDRKFLFACETESDQREWVAAFQKAVDRPMLPQEYAVEAHFKHKP
\.


--
-- Name: proteins_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dblyon
--

SELECT pg_catalog.setval('proteins_id_seq', 1, false);


--
-- Data for Name: taxa; Type: TABLE DATA; Schema: public; Owner: dblyon
--

COPY taxa (id, taxid, taxname, scientific) FROM stdin;
1	1185564	Diolcogaster spreta	1
2	34607	Amblyomma cajennense	1
3	163260	uncultured Thermodesulfobacterium sp.	1
4	1649861	Cladosporium sp. 4 SDM-2014	1
5	1445646	Limnometra matsudai (Miyamoto, 1967)	0
6	103392	Podoscypha elegans	1
7	632155	Aconitum geniculatum	1
8	680116	SPbeta-like viruses	0
9	1396863	Curimata cyprinoides (Linnaeus, 1766)	0
10	1580483	Pseudomonas sp. DP-1	1
11	322186	Helcon sp. AZR-2005	1
12	1580490	Pseudomonas sp. DP-3	1
13	323194	Trianthema sheilae	1
14	1456524	uncultured marine group II/III euryarchaeote KM3_84_G11	1
15	101843	Naucoria rheophylla	1
16	1064309	Hymenoptera sp. BOLD:AAU9571	1
17	1064310	Hymenoptera sp. BOLD:AAU9572	1
18	1064311	Hymenoptera sp. BOLD:AAU9573	1
19	1064312	Hymenoptera sp. BOLD:AAU9574	1
20	1064313	Hymenoptera sp. BOLD:AAU9575	1
21	393663	Pseudoruegeria aquimaris	1
22	1064315	Hymenoptera sp. BOLD:AAU9577	1
23	6452	Haliotis	1
24	1832683	Gonatocerus sp. CNROJ695-13	1
25	1186966	Cololejeunea kulenensis Tixier	0
26	326523	Neisseria zoodegmatis Vandamme et al. 2006	0
27	213263	Lysimachia engleri	1
28	1400720	Influenza A virus (A/Singapore/394T/2009(H1N1))	1
29	1088	strain DSI	0
30	1863053	Idiocerus obispanus Ball & Parker, 1946	0
31	966632	Hymenoptera sp. BOLD:AAN3642	1
32	966631	Hymenoptera sp. BOLD:AAN3641	1
33	516663	Austroniscus sp. 1 MR-2008	1
34	263010	Rexia erectus CAT 1M	0
35	687523	Parornix sp. DRD01	1
36	1183075	Ptychozoon horsfieldii (Gray, 1827)	0
37	1605449	Alicyclobacillus acidocaldarius subsp. acidocaldarius DSM 454	0
38	1097053	Homolobus sp. BJS-2011	1
39	1296189	Xylariaceae sp. SLM6	1
40	714823	Poliopastea laciades	1
41	712210	Campylobacter sp. oral taxon H15	1
42	551213	Influenza A virus (A/chicken/Phichit/NIAH600674/2008(H5N1))	1
43	235932	strain DS1	0
44	403962	strain DS2	0
45	182983	Stereum damaecorne	0
46	1198673	Pseudomonas syringae pv. theae ICMP 3923	1
47	1757931	Bacillus sp. X24-1	1
48	1423418	Burkholderia contaminans FFH2050	1
49	506622	Buchnera aphidicola (Cinara pilicornis)	1
50	826748	Hymenoptera sp. BOLD:AAG3930	1
51	1192508	Kradibia sp. ex Ficus gul	1
52	1345035	Cosmodela juxtata	0
53	238777	Phaeodaria	0
54	241174	Trachycardium alternatum	1
55	163849	Cape canary	0
56	856321	Hammondia sp. SSD-2010	0
57	1576704	Micromonospora sp. R10-29	1
58	755731	Clostridium sp. BNL1100	1
59	1647127	Enneapterygius cf. hemimelas BOLD:AAC0704	1
60	88318	Paruroctonus	1
61	674979	Bacilladnavirus	1
62	1217836	Gluconacetobacter sp. Wu 4	1
63	586703	Amphiacusta sp. 2 Viequez, Puerto Rico	0
64	518651	Bacillus sp. GK2	1
65	1423689	Glossogobius sp. AB-2013	1
66	1202010	Crematogaster grevei	1
67	50589	Podura aquatica	1
68	1535985	Culama sp. ANIC1	1
69	166257	Crenidens leoninus	0
70	1372492	Culama sp. ANIC3	1
71	75224	Philosycus	1
72	1235950	Xylariaceae sp. 5341	1
73	1235931	Xylariaceae sp. 5340	0
74	1437491	Hydrolithon boergesenii	1
75	99861	Urocitellus townsendi Bachman, 1839	0
76	1792847	Triplophysa tenuis	1
77	156880	Ollotis luetkeni	0
78	1475156	Eusparassus mesopotamicus Moradmand & Jager, 2012	0
79	354290	Acropyga	1
80	855194	Trichoptera sp. BOLD:AAB2410	1
81	1209805	Ascomycota sp. R3DOM3	0
82	1744986	Acritopappus confertus	1
83	240506	Cyclotelus sp. NCSU-0300010	1
84	498882	Bacillus sp. 50LAx-1	1
85	1247613	Pseudooceanicola antarcticus (Huo et al. 2014) Lai et al. 2015	0
86	1150209	Parapimelodus nigribarbus	0
87	134387	Vibrio sp. GIT-70	1
88	906717	Anacithara lita (Melvill & Standen, 1896)	0
89	1792380	Brevibacterium sp. CMT37	1
90	1844516	Aleiodes cantherius	1
91	1105414	Amaxia cf. pandama BOLD:AAB3082	1
92	1575888	Influenza A virus (A/chicken/Sichuan/P142/2013(H9))	1
93	3852	Laburnum alpinum	1
94	94289	Sterkiella histriomuscorum	1
95	366441	Parasagitta setosa	1
96	1166655	Influenza A virus (A/pintail/Alberta/22/1997(H2N9))	1
97	257368	Alathyria jacksoni	1
98	304456	Channa punctatus	0
99	470057	Vibrio sp. NC81	1
100	1514134	Fusarium sp. 2 MMH-2014	1
101	1147880	cyanobacterium enrichment culture clone 3_10_3.5.4_H12-T7	1
102	301852	Lygodactylus tuberosus	1
103	12480	Lymphotropic polyomavirus	0
104	1589212	Inocybe sp. AU76	1
105	1589207	Inocybe sp. AU71	1
106	1589206	Inocybe sp. AU70	1
107	1589209	Inocybe sp. AU73	1
108	233858	Mycobacterium sacrum	1
109	1768045	Fusarium sp. D59Fs	1
110	887144	Rhizobium sp. CCNWSX 0457	0
111	1174689	Acacia acinacea	1
112	1583306	Inocybe sp. AU79	1
113	1233958	Dryas grandis Juz.	0
114	822458	Entomobryomorpha sp. BOLD:AAC4133	1
115	822457	Entomobryomorpha sp. BOLD:AAC4132	1
116	241512	Asplenium polyodon	1
117	311194	JCM 12929	0
118	253519	Rickettsia sp. COOPERI	1
119	304413	JCM 12927	0
120	304417	JCM 12926	0
121	246191	JCM 12925	0
122	340956	JCM 12924	0
123	341036	JCM 12923	0
124	225894	JCM 12921	0
125	272239	JCM 12920	0
126	574911	Hercostomus vivax (Loew, 1857)	0
127	980329	Arctic staghorn sculpin	0
128	30917	threadfins	0
129	634884	Pontibacter niistensis	1
130	323071	Croton montevidensis Spreng.	0
131	269369	Poa sibirica Roshev.	0
132	49765	Megaceros sp.	1
133	1399844	Streptomyces sp. O22	1
134	264294	Salinospora sp. CNR107	1
135	1740913	Limonia halterata	0
136	495947	sooty falcon	0
137	1357690	Basidiobolus heterosporus B8920	1
138	1227979	Festuca pseudo-eskia	0
139	446963	Andrachne asperula	1
140	1579087	Paratrichosoma sp. FW11 C5	1
141	1193723	Lythrypnus sp. 1 JMM-2012	1
142	221312	Vandenboschia capillacea (L.) Copel.	0
143	1494739	Avena sp. aga6AB	1
144	765488	Influenza A virus (A/California/VRDL229/2009(H1N1))	1
145	601441	Nomada conjungens Herrich-Schaffer,1839	0
146	117448	uncultured sludge bacterium A6b	1
147	404194	Influenza A virus (A/swine/Shandong/nc/2005(H9N2))	1
148	1565864	Mycobacterium sp. INBio_4511F	1
149	196656	Desmanthus pubescens	1
150	855399	Trichoptera sp. BOLD:AAD1026	1
151	1857805	Fusarium sp. 3 IDEA_FITOPAT_D019	1
152	381446	ZJUF0986	0
153	651312	Lacerta danfordi	0
154	676447	Onychiuridae sp. DPCOL90633	1
155	213679	Libellula rubicunda	0
156	1569066	Prionocyphon sp. Springbrook	1
157	795536	marine bacterium HB-34	1
158	795537	marine bacterium HB-35	1
159	795538	marine bacterium HB-36	1
160	1541150	Influenza A virus (A/Quebec/26-100605/2005(H3N2))	1
161	795532	marine bacterium HB-30	1
162	795533	marine bacterium HB-31	1
163	795534	marine bacterium HB-32	1
164	795535	marine bacterium HB-33	1
165	29095	Akodon azarae	1
166	647080	Oxyrrhynchium sp. 2 (Buck 23824)	1
167	1621888	Influenza A virus (A/Alberta/35/2014(H1N1))	1
168	1316237	Influenza A virus (A/Tehran/895/2012(H3N2))	1
169	391231	saccharomycete sp. 3AD23	1
170	211707	Clusia melchiorii	1
171	1204306	Meconopsis oliveriana Franch. & Prain ex Prain	0
172	1512045	Influenza A virus (A/swine/Hong Kong/NS3817/2010(H1N1))	1
173	1534848	Bradyrhizobium sp. ARR204	1
174	1213190	TN-22-W4A	0
175	1427781	Influenza A virus (A/Illinois/YGA_04048/2012(H3N2))	0
176	227533	Anthocharis cardamines isshikii	1
177	1082517	Influenza A virus (A/chicken/Qianzhou/12/2010(H9N2))	1
178	1150807	Taygetis laura	1
179	754975	Exiguobacterium sp. MJ536	1
180	398235	strain TAN 31504	0
181	534751	Leucoagaricus sp. JJS020520-04	1
182	4768	Achlya ambisexualis	1
183	120451	Rhabdus	1
184	1516431	Arthropoda sp. JGP0389	0
185	1826223	Lachenalia margaretae W.F.Barker	0
186	1049154	Influenza A virus (A/Quebec/QC152717/2009(H1N1))	1
187	1647734	Zimmermannella sp. S413	0
188	386713	Norovirus Hu/GII/HK/CU041213/2004/CHN	1
189	1603719	Embelia laeta (L.) Mez	0
190	327689	Acheilognathus longibarbatus	1
191	1679551	Bacillus sp. MRSA111B15_13_2E	1
192	207300	Pterostylis allantoidea	1
193	358915	Ceratobasidium sp. CBS 223.51	1
194	2382	Acetitomaculum ruminis	1
195	1007864	Gladiolus woodii	1
196	1398945	Acinetobacter baumannii UH0807	1
197	368518	Sporosarcina sp. K2-4-037	1
198	1824123	Influenza B virus (B/California/05/2015)	1
199	1346573	Ziziphus cf. fungii MR-2013	1
200	1196288	Tamaulipas crow	0
201	67301	Streptomyces fragilis	1
202	179722	Bennettiodendron Merr., 1927	0
203	1576847	Aspergillus sp. AM_L5	1
204	362730	Sideroxylon repens	1
205	1032661	Aspergillus costiformis	1
206	247589	Hypenetes critesi	1
207	701042	strain 5356591	0
208	1773583	Chironomidae sp. BOLD:ACL4016	1
209	277992	Takifugu exascurus	1
210	70400	Libellula lydia	0
211	485	Micrococcus der gonorrhoe	0
212	1397933	Mycobacterium tuberculosis TKK_04_0044	1
213	254216	Laccaria sp. NC-8336	1
214	1397936	Mycobacterium tuberculosis TKK_04_0042	1
215	1286411	Salmonella enterica subsp. enterica serovar Cerro str. FSL R8-2827	1
216	1397932	Mycobacterium tuberculosis TKK_04_0040	1
217	76442	Fimbristylis	1
218	881525	Apateticus	1
219	559647	Hydrotaea cyrtoneurina	1
220	697011	Coluber petola	0
221	591859	Oigolaimella sp. RGD844	1
222	586809	Cryptocentrus cyanotaenia	1
223	145445	Euglandina rosea	1
224	1385098	Tenthredo dahlii Klug, 1817	0
225	549724	Oligogonotylus manteri Watson, 1976	0
226	1051983	Scutellospora sp. S1	1
227	1605823	Lancetes waterhousei Griffini, 1895	0
228	1391057	Radiella	1
229	292777	Linospadix palmerianus (F.M.Bailey) Burret	0
230	798411	Locris pullata Stal, 1866	0
231	996366	Tinopsis tamatavensis Capuron	0
232	1605449	Alicyclobacillus acidocaldarius subsp. acidocaldarius DSM 453	0
233	1824977	Poecilolycia vittata (Walker, 1849)	0
234	383037	Influenza A virus (A/New York/696/1994(H3N2))	1
235	1096428	Influenza A virus (A/chicken/Viet Nam/TMU015/2008(H5N1))	1
236	1133545	Xanthomonadaceae bacterium MS54b	1
237	167683	Halimolobos minutiflorus	1
238	1129505	Funchalia villosa (Bouvier, 1905b)	0
239	491687	Alteromonadales bacterium HD-OI-02-5	1
240	1778758	Hohenbuehelia longipes	1
241	491688	Alteromonadales bacterium HD-OI-02-6	1
242	408803	Mycobacterium sp. Ri506	1
243	1203686	Influenza A virus (A/Singapore/GP394/2011(H1N1))	1
244	1760237	Scheloribatidae sp. BOLD:ACM9934	1
245	72949	Lagenophora panamensis	1
246	229132	Pomacentrus grammorhynchus	1
247	56641	Fusarium crookwellense	0
248	155906	Pestivirus sp. Reindeer-1	0
249	510450	Calohypsibius sp. Calo_07_116	1
250	508772	Escalera's bat	0
251	1592097	Sewage-associated circular DNA virus-30	1
252	1452831	Pseudomezira kashmirensis	1
253	1317720	Caenohalictus galletue Rojas & Toro, 2000	0
254	1714555	Cyclocephala inca Endrodi, 1966	0
255	1388779	KUN F73639	0
256	491686	Alteromonadales bacterium HD-OI-02-3	1
257	426854	Sirhookera lanceolata	1
258	1202445	Mycoplasma sp. 7320	1
259	1516319	Arthropoda sp. JGP0271	0
260	1199180	Cortinarius ursus Soop 2001	0
261	1492108	Phialocephala sp. CM16m2	1
262	869813	Laricobius osakensis Montgomery & Shiyake, 2011	0
263	1734633	Rhizobium sp. NSB1_5	1
264	702521	Influenza A virus (A/gadwall/Minnesota/Sg-00044/2007(mixed))	1
265	3570	Dianthus caryophyllus L.	0
266	827	Campylobacter ureolyticus	1
267	1553786	Tachyporus pulchellus	1
268	1201539	bacterium NLAE-zl-H228	1
269	39666	Methanihalophilus sp. strain SF-1	0
270	186960	Ligulariopsis shichuana	1
271	1123533	Microsporomyces pini (Pohl, M.S. Smit & Albertyn) Q.M. Wang, F.Y. Bai, M. Groenew. & Boekhout, 2015	0
272	1201531	bacterium NLAE-zl-H220	1
273	1201532	bacterium NLAE-zl-H221	1
274	1201533	bacterium NLAE-zl-H222	1
275	1201534	bacterium NLAE-zl-H223	1
276	1201535	bacterium NLAE-zl-H224	1
277	1201536	bacterium NLAE-zl-H225	1
278	1201537	bacterium NLAE-zl-H226	1
279	1201538	bacterium NLAE-zl-H227	1
280	1865273	Influenza A virus (A/Missouri/09/2016(H1N1))	1
281	30211	Vespula flavopilosa	1
282	1616323	Saxifraga parnassifolia	1
283	1336929	Iophon nigricans	1
284	395766	Hylaeus cyaneomicans	1
285	350200	Maxillaria curtipes	1
286	1028809	Streptomyces mutabilis str. 13676F	0
287	1482154	Orpha flavicornis Pascoe, 1870	0
288	1544083	Bacillus sp. H319	1
289	1544082	Bacillus sp. H318	1
290	37453	ATCC 700399	0
291	531	ATCC 700398	0
292	1714344	Curvibacter sp. PAE-UM	1
293	1534768	Sobralia mucronata Ames & C.Schweinf.	0
294	66219	ATCC 700394	0
295	53483	ATCC 700397	0
296	1544078	Bacillus sp. H310	1
297	1544081	Bacillus sp. H316	1
298	1542325	Anastraphia D.Don, 1830	0
299	70541	Distoechodon tumirostris	1
300	1896	ISP 5581	0
301	371361	Ferula sp. Schiptschinsky 104	0
302	1602090	Streptomyces sp. 0312TES10J4	1
303	1844666	Loktanella sp. ZJ0205B95	1
304	42238	ISP 5588	0
305	329769	Solanum comptum	1
306	1605116	Influenza A virus (A/Quebec/50/2014(H3N2))	1
307	1056645	Cochliobolus heteropogonis Alcorn 1990	0
308	670173	uncultured Sufflavibacter sp.	1
309	1636092	Beltraniella sp. 111.3.3	1
310	486125	Boechera lasiocarpa	1
311	485495	Streptomyces sp. A403Ydz-QZ	1
312	49728	Milligania stylosa (F.Muell. ex Hook.f.) F.Muell. ex Benth.	0
313	167112	Ctenoblepharys adspersa	1
314	328294	Cosmarium subprotumidum var. gregorii	1
315	1811068	Heteronemertea sp. NemBar0904	1
316	1834208	Peniophora munda	0
317	1086296	Enyo latipennis	1
318	29261	Ntaya virus group	1
319	240304	Rhodocybe aureicystidiata	0
320	36017	Cyberlindnera bimundalis	1
321	933250	Orcynia calcarata	1
322	1227066	Dioscorea sp. KMXK	1
323	1555196	Influenza A virus (A/crow/India/01TR01/2012(H5N1))	1
324	262511	Ochlochaete hystrix	1
325	1433548	Allium cf. globosum NF-2013a	0
326	1433549	Allium cf. globosum NF-2013b	0
327	1434318	Allium cf. globosum NF-2013c	0
328	689121	Enargia decolor (Walker, 1858)	0
329	1342524	Aciculites sp. USNM 1204870	1
330	722470	Hylophylax poecilonotus lepidonota	0
331	1831604	Cryptinae sp. BOLD:AAF2903	1
332	1030264	Stenotrophomonas sp. Vi3	1
333	1209936	Pardosa timidula	1
334	335148	Silene viridiflora L.	0
335	243077	Rossia bipillata	1
336	1392938	Dictyophora sp. 1 LL-2013	0
337	1320337	Schizophyllum sp. 38a	1
338	350419	Xylobium subpulchrum Dressler	0
339	307540	gamma proteobacterium II-01	1
340	515321	Protoachlya sp. Argentina 3.1	1
341	118861	Andinomys edax	1
342	307541	gamma proteobacterium II-02	1
343	1580940	Pheidole sp. EPEM100	1
344	414627	Notholaena affinis (Mett.) Moore	0
345	316683	Adenocline violaefolia	0
346	310573	Acinetobacter sp. PC19	1
347	1658131	Thrassis pandorae	1
348	1391654	Sorangiineae bacterium B00002	0
349	1622162	Onychiurus flavescens	1
350	1173525	Archinome storchi	1
351	1381274	Influenza A virus (A/guinea fowl/Italy/1766/2000(H7N1))	1
352	192945	Acinetobacter sp. PC11	1
353	490386	Colwellia sp. MN1-44	1
354	1654929	Heliophobius argenteocinereus kapiti Heller, 1909	0
355	1369298	Hyposada	1
356	1447708	Oenothera riparia Nutt.	0
357	84524	horse bot flies	0
358	307544	gamma proteobacterium II-06	1
359	70956	Trigonella arcuata	0
360	1572084	Busseola nairobica	1
361	943538	Hypocreales sp. r443	1
362	1266872	twohorn sculpin	0
363	1271778	Influenza A virus (A/swine/Finland/si4171/2010(H1N1))	1
364	307545	gamma proteobacterium II-08	1
365	469510	Liodessus sp. NHM-IR527	1
366	294181	Chalcura samoana	1
367	138992	uncultured organism HB1-23	0
368	37264	Dissoteira	0
369	54892	Poecilanthe falcata (Vell.) Heringer	0
370	537132	Erysimum siliculosum	1
371	1803967	Epiplatys esekanus	1
372	1082134	Somatochlora sp. ECODB518-09	1
373	117259	Tylocephalum sp. DTJL-2000	1
374	587739	JSM 070026	0
375	1286126	Hypoclinemus sp. GO328	1
376	1529128	Bacillus sp. 80	1
377	890055	Pontibacter sp. HYL7-15	0
378	756231	Oxytropis hailarensis subsp. chankaensis (Jurtzev) Kitag.	0
379	257293	Calochilus sp. Chase O-488	1
380	1287	Staphylococcus simulans staphylolyticus	0
381	1306990	Streptomyces sp. R1-NS-10	0
382	332788	Lycosa clara	1
383	30549	Mustela sp.	1
384	62504	Influenza A virus (A/Paris/688/93(H3N2))	1
385	670404	Nomopyle Roalson & Boggan	0
386	651689	Zasmidium anthuriicola	1
387	1182201	Dules flaviventris	0
388	1550819	Brickellia frutescens	1
389	754875	Ebenus longipes	1
390	1469870	Influenza A virus (A/Headington/INS3_651/2011(H1N1))	1
391	1562553	Trypethelium neogalbineum	1
392	982717	Influenza A virus (A/swine/Minnesota/02345/2008(H1N1))	1
393	944221	Pterodroma sandwichensis	1
394	368405	Glaciecola chathamense	0
395	3660	pumpkins	0
396	1516	Thermoanaerobacter thermohydrosulfuricus (Klaushofer and Parkkinen 1965) Lee et al. 1993	0
397	1139738	Symmachia BioLep01	0
398	46680	Pseudomonas nitroreductans	0
399	304898	Catenulispora sp. Neo15	1
400	162063	Chaetomorpha antennina	1
401	1527031	Chimarra australica Ulmer, 1916	0
402	708459	Favartia mactanensis	1
403	60069	Retiniphyllum pilosum	1
404	31525	Epstein-Barr virus (strain CAO)	0
405	1007477	Rhinebothrium copianullum Reyda, 2008	0
406	109598	forkleaf toothwort	0
407	403206	Marinobacter sp. SB12	1
408	556890	DSM 25990	0
409	101199	uncultured bacterium SH5	1
410	237530	Paenibacillus cineris	1
411	1007394	Adeixis griseata	1
412	1169191	Salinispora pacifica CNT584	1
413	101194	uncultured bacterium SH1	1
414	206625	Cymopterus corrugatus M.E.Jones	0
415	1577556	Streptomyces sp. MSSRFDF17	1
416	1229247	Bauhinia erythrantha	0
417	1747087	Amphora sp. HN09	1
418	101200	uncultured bacterium SH9	1
419	475974	Ceratomyxa oxycheilinae Heiniger, Gunter & Adlard, 2008	0
420	717517	Dioszegia sp. RS092	0
421	717517	Dioszegia sp. RS090	0
422	86087	Carnibacterium sp. Y6	0
423	1809511	Somethus tasmani Jeekel, 2006	0
424	236905	Cylapini	1
425	71656	Brenneria alni (Surico et al. 1996) Hauben et al. 1999	0
426	517062	Norovirus Han River/GII/Dukpoong/Jan03/2006/KOR	1
427	64104	NRRL B-617	0
428	1721676	Cecidomyiidae sp. BOLD:ACL9909	1
429	252670	Clytia viridicans	1
430	43404	Cryptodacus	1
431	1312353	Influenza A virus (A/Shiraz/11/2013(H1N1))	1
432	8258	Limanda ferruginea	1
433	855310	Trichoptera sp. BOLD:AAC4426	1
434	855311	Trichoptera sp. BOLD:AAC4427	1
435	522461	Marinobacterium sp. PY97E	1
436	1118594	Eupelmus falcatus	1
437	598501	Alcaligenes sp. MH146	1
438	522460	Marinobacterium sp. PY97A	1
439	70258	strain SK03	0
440	441231	Mecopoda	1
441	1270275	Microbacteriaceae bacterium ISO538_OTU14462	1
442	314782	Vibrio sp. 1D08	1
443	314783	Vibrio sp. 1D09	1
444	865523	Bacillus sp. SGE185(2010)	1
445	388818	HIV-1 N_YBF30	1
446	1002675	Phytophthora sp. SWKA	1
447	314777	Vibrio sp. 1D02	1
448	314778	Vibrio sp. 1D03	1
449	53893	sericea lespedeza	0
450	314776	Vibrio sp. 1D01	1
451	314780	Vibrio sp. 1D06	1
452	314781	Vibrio sp. 1D07	1
453	314779	Vibrio sp. 1D04	1
454	186963	Parasenecio latipes (Franch.) Y.L.Chen	0
455	682621	Syagrus coronata	1
456	1194950	Boletus sp. 12 ZLY-2012	1
457	175015	Thamnophilus nigrocinereus	1
458	908351	Volvopluteus michiganensis	1
459	1334842	Atherinichthys sallei Regan, 1903	0
460	992179	Yersinia pestis PY-98	1
461	992180	Yersinia pestis PY-99	1
462	1311425	Caulolatilus intermedius	1
463	992176	Yersinia pestis PY-94	1
464	992177	Yersinia pestis PY-95	1
465	992178	Yersinia pestis PY-96	1
466	1384739	Allantus laticinctus	1
467	992172	Yersinia pestis PY-90	1
468	992173	Yersinia pestis PY-91	1
469	992174	Yersinia pestis PY-92	1
470	992175	Yersinia pestis PY-93	1
471	1433830	Schefflera polybotrya	1
472	1600443	Influenza B virus (B/Fukuoka/1/2009)	1
473	590732	Rhynchostegium holstii	0
474	1354285	Begonia gueritziana Gibbs	0
475	1713922	Empis sp. 4 BKC-2015	1
476	749585	Transposon vector EPICENTRE EZ-Tn5 <oriV/KAN-2>	1
477	1778834	Unclassified Paraplatyarthridae	1
478	350172	Maxillaria burgeri J.T.Atwood	0
479	865920	Conotrochus	1
480	36374	Visna/maedi virus EV1 KV1772	1
481	1588171	Sciarosoma	1
482	1590101	Frontonia ocularis Bullington, 1939	0
483	675436	Moina brachiata (Jurine, 1820)	0
484	1446219	Platypalpus stabilis (Collin, 1961)	0
485	1471876	Miconia krugiana	1
486	210794	Cloeosiphon japonicum	0
487	1470755	Episopus politus	1
488	514321	Influenza A virus (A/HANNOVER/8/2002(H3N2))	1
489	1449264	Oceanospirillales bacterium SCGC AD-308-L02	1
490	759953	Rhinotyphlops lalandei Schlegel, 1839	0
491	361892	Trifolium berytheum Boiss. & Blanche	0
492	1155141	Epicoccum sp. CPO 10.006	1
493	1155142	Epicoccum sp. CPO 10.007	1
494	504605	IFM 54738	0
495	670650	Sarconesia	1
496	860400	Schistidium cf. papillosum Hedenaes s.n.	1
497	1013601	bacterium enrichment culture clone ALO1_GLFRUDD03G7FGJ	1
498	652513	Conotrachelus sp. CTS-162	1
499	1096299	Fossombronia incurva Lindb.	0
500	29831	Saccharomyces cidri	0
\.


--
-- Name: taxa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dblyon
--

SELECT pg_catalog.setval('taxa_id_seq', 1, false);


--
-- Data for Name: taxid_2_rank; Type: TABLE DATA; Schema: public; Owner: dblyon
--

COPY taxid_2_rank (id, taxid, rank) FROM stdin;
1	1185564	species
2	34607	species
3	163260	species
4	1649861	species
5	1445646	species
6	103392	species
7	632155	species
8	680116	genus
9	1396863	species
10	1580483	species
11	322186	species
12	1580490	species
13	323194	species
14	1456524	species
15	101843	species
16	1064309	species
17	1064310	species
18	1064311	species
19	1064312	species
20	1064313	species
21	393663	species
22	1064315	species
23	6452	genus
24	1832683	species
25	1186966	species
26	326523	species
27	213263	species
28	1400720	no rank
29	1088	species
30	1863053	species
31	966632	species
32	966631	species
33	516663	species
34	263010	no rank
35	687523	species
36	1183075	species
37	1605449	species
38	1097053	species
39	1296189	species
40	714823	species
41	712210	species
42	551213	no rank
43	235932	species
44	403962	species
45	182983	species
46	1198673	no rank
47	1757931	species
48	1423418	no rank
49	506622	no rank
50	826748	species
51	1192508	species
52	1345035	subspecies
53	238777	no rank
54	241174	species
55	163849	species
56	856321	species
57	1576704	species
58	755731	species
59	1647127	species
60	88318	genus
61	674979	genus
62	1217836	species
63	586703	species
64	518651	species
65	1423689	species
66	1202010	species
67	50589	species
68	1535985	species
69	166257	species
70	1372492	species
71	75224	genus
72	1235950	species
73	1235931	species
74	1437491	species
75	99861	species
76	1792847	species
77	156880	species
78	1475156	species
79	354290	genus
80	855194	species
81	1209805	species
82	1744986	species
83	240506	species
84	498882	species
85	1247613	species
86	1150209	species
87	134387	species
88	906717	species
89	1792380	species
90	1844516	species
91	1105414	species
92	1575888	no rank
93	3852	species
94	94289	species
95	366441	species
96	1166655	no rank
97	257368	species
98	304456	species
99	470057	species
100	1514134	species
101	1147880	species
102	301852	species
103	12480	species
104	1589212	species
105	1589207	species
106	1589206	species
107	1589209	species
108	233858	species
109	1768045	species
110	887144	species
111	1174689	species
112	1583306	species
113	1233958	species
114	822458	species
115	822457	species
116	241512	species
117	311194	species
118	253519	species
119	304413	species
120	304417	species
121	246191	species
122	340956	species
123	341036	species
124	225894	species
125	272239	species
126	574911	species
127	980329	species
128	30917	family
129	634884	species
130	323071	species
131	269369	species
132	49765	species
133	1399844	species
134	264294	species
135	1740913	species
136	495947	species
137	1357690	no rank
138	1227979	species
139	446963	species
140	1579087	species
141	1193723	species
142	221312	species
143	1494739	species
144	765488	no rank
145	601441	species
146	117448	species
147	404194	no rank
148	1565864	species
149	196656	species
150	855399	species
151	1857805	species
152	381446	species
153	651312	species
154	676447	species
155	213679	species
156	1569066	species
157	795536	species
158	795537	species
159	795538	species
160	1541150	no rank
161	795532	species
162	795533	species
163	795534	species
164	795535	species
165	29095	species
166	647080	species
167	1621888	no rank
168	1316237	no rank
169	391231	species
170	211707	species
171	1204306	species
172	1512045	no rank
173	1534848	species
174	1213190	species
175	1427781	no rank
176	227533	subspecies
177	1082517	no rank
178	1150807	species
179	754975	species
180	398235	subspecies
181	534751	species
182	4768	species
183	120451	genus
184	1516431	species
185	1826223	species
186	1049154	no rank
187	1647734	species
188	386713	no rank
189	1603719	species
190	327689	species
191	1679551	species
192	207300	species
193	358915	species
194	2382	species
195	1007864	species
196	1398945	no rank
197	368518	species
198	1824123	no rank
199	1346573	species
200	1196288	species
201	67301	species
202	179722	genus
203	1576847	species
204	362730	species
205	1032661	species
206	247589	species
207	701042	species
208	1773583	species
209	277992	species
210	70400	species
211	485	species
212	1397933	no rank
213	254216	species
214	1397936	no rank
215	1286411	no rank
216	1397932	no rank
217	76442	genus
218	881525	genus
219	559647	species
220	697011	species
221	591859	species
222	586809	species
223	145445	species
224	1385098	species
225	549724	species
226	1051983	species
227	1605823	species
228	1391057	genus
229	292777	species
230	798411	species
231	996366	species
232	1605449	species
233	1824977	species
234	383037	no rank
235	1096428	no rank
236	1133545	species
237	167683	species
238	1129505	species
239	491687	species
240	1778758	species
241	491688	species
242	408803	species
243	1203686	no rank
244	1760237	species
245	72949	species
246	229132	species
247	56641	species
248	155906	no rank
249	510450	species
250	508772	species
251	1592097	species
252	1452831	species
253	1317720	species
254	1714555	species
255	1388779	species
256	491686	species
257	426854	species
258	1202445	species
259	1516319	species
260	1199180	species
261	1492108	species
262	869813	species
263	1734633	species
264	702521	no rank
265	3570	species
266	827	species
267	1553786	species
268	1201539	species
269	39666	species
270	186960	species
271	1123533	species
272	1201531	species
273	1201532	species
274	1201533	species
275	1201534	species
276	1201535	species
277	1201536	species
278	1201537	species
279	1201538	species
280	1865273	no rank
281	30211	species
282	1616323	species
283	1336929	species
284	395766	species
285	350200	species
286	1028809	no rank
287	1482154	species
288	1544083	species
289	1544082	species
290	37453	species
291	531	species
292	1714344	species
293	1534768	species
294	66219	species
295	53483	species
296	1544078	species
297	1544081	species
298	1542325	genus
299	70541	species
300	1896	species
301	371361	species
302	1602090	species
303	1844666	species
304	42238	species
305	329769	species
306	1605116	no rank
307	1056645	species
308	670173	species
309	1636092	species
310	486125	species
311	485495	species
312	49728	species
313	167112	species
314	328294	varietas
315	1811068	species
316	1834208	species
317	1086296	species
318	29261	subgenus
319	240304	species
320	36017	species
321	933250	species
322	1227066	species
323	1555196	no rank
324	262511	species
325	1433548	species
326	1433549	species
327	1434318	species
328	689121	species
329	1342524	species
330	722470	subspecies
331	1831604	species
332	1030264	species
333	1209936	species
334	335148	species
335	243077	species
336	1392938	species
337	1320337	species
338	350419	species
339	307540	species
340	515321	species
341	118861	species
342	307541	species
343	1580940	species
344	414627	species
345	316683	species
346	310573	species
347	1658131	species
348	1391654	species
349	1622162	species
350	1173525	species
351	1381274	no rank
352	192945	species
353	490386	species
354	1654929	subspecies
355	1369298	genus
356	1447708	species
357	84524	genus
358	307544	species
359	70956	species
360	1572084	species
361	943538	species
362	1266872	species
363	1271778	no rank
364	307545	species
365	469510	species
366	294181	species
367	138992	species
368	37264	genus
369	54892	species
370	537132	species
371	1803967	species
372	1082134	species
373	117259	species
374	587739	species
375	1286126	species
376	1529128	species
377	890055	species
378	756231	species
379	257293	species
380	1287	no rank
381	1306990	species
382	332788	species
383	30549	species
384	62504	no rank
385	670404	genus
386	651689	species
387	1182201	species
388	1550819	species
389	754875	species
390	1469870	no rank
391	1562553	species
392	982717	no rank
393	944221	species
394	368405	species
395	3660	genus
396	1516	species
397	1139738	species
398	46680	species
399	304898	species
400	162063	species
401	1527031	species
402	708459	species
403	60069	species
404	31525	no rank
405	1007477	species
406	109598	species
407	403206	species
408	556890	species
409	101199	species
410	237530	species
411	1007394	species
412	1169191	no rank
413	101194	species
414	206625	species
415	1577556	species
416	1229247	species
417	1747087	species
418	101200	species
419	475974	species
420	717517	species
421	717517	species
422	86087	species
423	1809511	species
424	236905	tribe
425	71656	species
426	517062	no rank
427	64104	species
428	1721676	species
429	252670	species
430	43404	genus
431	1312353	no rank
432	8258	species
433	855310	species
434	855311	species
435	522461	species
436	1118594	species
437	598501	species
438	522460	species
439	70258	species
440	441231	genus
441	1270275	species
442	314782	species
443	314783	species
444	865523	species
445	388818	no rank
446	1002675	species
447	314777	species
448	314778	species
449	53893	species
450	314776	species
451	314780	species
452	314781	species
453	314779	species
454	186963	species
455	682621	species
456	1194950	species
457	175015	species
458	908351	species
459	1334842	species
460	992179	no rank
461	992180	no rank
462	1311425	species
463	992176	no rank
464	992177	no rank
465	992178	no rank
466	1384739	species
467	992172	no rank
468	992173	no rank
469	992174	no rank
470	992175	no rank
471	1433830	species
472	1600443	no rank
473	590732	species
474	1354285	species
475	1713922	species
476	749585	species
477	1778834	no rank
478	350172	species
479	865920	genus
480	36374	no rank
481	1588171	genus
482	1590101	species
483	675436	species
484	1446219	species
485	1471876	species
486	210794	species
487	1470755	species
488	514321	no rank
489	1449264	species
490	759953	species
491	361892	species
492	1155141	species
493	1155142	species
494	504605	species
495	670650	genus
496	860400	species
497	1013601	species
498	652513	species
499	1096299	species
500	29831	species
\.


--
-- Name: taxid_2_rank_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dblyon
--

SELECT pg_catalog.setval('taxid_2_rank_id_seq', 1, false);


--
-- Name: function_2_definition_pkey; Type: CONSTRAINT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY function_2_definition
    ADD CONSTRAINT function_2_definition_pkey PRIMARY KEY (id);


--
-- Name: functions_pkey; Type: CONSTRAINT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY functions
    ADD CONSTRAINT functions_pkey PRIMARY KEY (id);


--
-- Name: go_2_slim_pkey; Type: CONSTRAINT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY go_2_slim
    ADD CONSTRAINT go_2_slim_pkey PRIMARY KEY (id);


--
-- Name: og_2_function_pkey; Type: CONSTRAINT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY og_2_function
    ADD CONSTRAINT og_2_function_pkey PRIMARY KEY (id);


--
-- Name: ogs_pkey; Type: CONSTRAINT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY ogs
    ADD CONSTRAINT ogs_pkey PRIMARY KEY (id);


--
-- Name: ontologies_pkey; Type: CONSTRAINT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY ontologies
    ADD CONSTRAINT ontologies_pkey PRIMARY KEY (id);


--
-- Name: peptides_pkey; Type: CONSTRAINT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY peptides
    ADD CONSTRAINT peptides_pkey PRIMARY KEY (id);


--
-- Name: protein_2_function_pkey; Type: CONSTRAINT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY protein_2_function
    ADD CONSTRAINT protein_2_function_pkey PRIMARY KEY (id);


--
-- Name: protein_2_og_pkey; Type: CONSTRAINT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY protein_2_og
    ADD CONSTRAINT protein_2_og_pkey PRIMARY KEY (id);


--
-- Name: protein_2_taxid_pkey; Type: CONSTRAINT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY protein_2_taxid
    ADD CONSTRAINT protein_2_taxid_pkey PRIMARY KEY (id);


--
-- Name: protein_2_version_pkey; Type: CONSTRAINT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY protein_2_version
    ADD CONSTRAINT protein_2_version_pkey PRIMARY KEY (id);


--
-- Name: proteins_pkey; Type: CONSTRAINT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY proteins
    ADD CONSTRAINT proteins_pkey PRIMARY KEY (id);


--
-- Name: taxa_pkey; Type: CONSTRAINT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY taxa
    ADD CONSTRAINT taxa_pkey PRIMARY KEY (id);


--
-- Name: taxid_2_rank_pkey; Type: CONSTRAINT; Schema: public; Owner: dblyon
--

ALTER TABLE ONLY taxid_2_rank
    ADD CONSTRAINT taxid_2_rank_pkey PRIMARY KEY (id);


--
-- Name: function_2_definition_an_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX function_2_definition_an_idx ON function_2_definition USING btree (an);


--
-- Name: functions_an_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX functions_an_idx ON functions USING btree (an);


--
-- Name: functions_type_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX functions_type_idx ON functions USING btree (type);


--
-- Name: go_2_slim_an_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX go_2_slim_an_idx ON go_2_slim USING btree (an);


--
-- Name: og_2_function_function_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX og_2_function_function_idx ON og_2_function USING btree (function);


--
-- Name: og_2_function_og_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX og_2_function_og_idx ON og_2_function USING btree (og);


--
-- Name: ogs_og_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX ogs_og_idx ON ogs USING btree (og);


--
-- Name: ontologies_child_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX ontologies_child_idx ON ontologies USING btree (child);


--
-- Name: ontologies_direct_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX ontologies_direct_idx ON ontologies USING btree (direct);


--
-- Name: ontologies_parent_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX ontologies_parent_idx ON ontologies USING btree (parent);


--
-- Name: peptides_aaseq_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX peptides_aaseq_idx ON peptides USING btree (aaseq);


--
-- Name: peptides_an_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX peptides_an_idx ON peptides USING btree (an);


--
-- Name: peptides_missedcleavages_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX peptides_missedcleavages_idx ON peptides USING btree (missedcleavages);


--
-- Name: protein_2_function_an_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX protein_2_function_an_idx ON protein_2_function USING btree (an);


--
-- Name: protein_2_function_function_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX protein_2_function_function_idx ON protein_2_function USING btree (function);


--
-- Name: protein_2_og_an_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX protein_2_og_an_idx ON protein_2_og USING btree (an);


--
-- Name: protein_2_og_og_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX protein_2_og_og_idx ON protein_2_og USING btree (og);


--
-- Name: protein_2_taxid_an_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX protein_2_taxid_an_idx ON protein_2_taxid USING btree (an);


--
-- Name: protein_2_taxid_taxid_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX protein_2_taxid_taxid_idx ON protein_2_taxid USING btree (taxid);


--
-- Name: protein_2_version_an_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX protein_2_version_an_idx ON protein_2_version USING btree (an);


--
-- Name: protein_2_version_version_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX protein_2_version_version_idx ON protein_2_version USING btree (version);


--
-- Name: proteins_an_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX proteins_an_idx ON proteins USING btree (an);


--
-- Name: taxa_scientific_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX taxa_scientific_idx ON taxa USING btree (scientific);


--
-- Name: taxa_taxid_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX taxa_taxid_idx ON taxa USING btree (taxid);


--
-- Name: taxa_taxname_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX taxa_taxname_idx ON taxa USING btree (taxname);


--
-- Name: taxid_2_rank_rank_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX taxid_2_rank_rank_idx ON taxid_2_rank USING btree (rank);


--
-- Name: taxid_2_rank_taxid_idx; Type: INDEX; Schema: public; Owner: dblyon
--

CREATE INDEX taxid_2_rank_taxid_idx ON taxid_2_rank USING btree (taxid);


--
-- Name: public; Type: ACL; Schema: -; Owner: dblyon
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM dblyon;
GRANT ALL ON SCHEMA public TO dblyon;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

