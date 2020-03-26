import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
import pytest
import variables, ratio, query, run





def get_random_human_ENSP(num_ENSPs=2000, max_index=19566, joined_for_web=False, contiguous=False, UniProt_ID=False):
    if UniProt_ID:
        IDs_2_sample = UniProt_IDs_human
    else:
        IDs_2_sample = ENSPs_homo
    max_index = len(IDs_2_sample)
    if not contiguous:
        if not joined_for_web:
            return random.sample(IDs_2_sample, num_ENSPs)
        else:
            return "%0d".join(random.sample(IDs_2_sample, num_ENSPs))
    else:
        start_pos = np.random.randint(0, max_index)
        if start_pos + num_ENSPs > max_index:
            start_pos = max_index - num_ENSPs
        stop_pos = start_pos + num_ENSPs
        if not joined_for_web:
            return list(islice(IDs_2_sample, start_pos, stop_pos))
        else:
            return "%0d".join(list(islice(IDs_2_sample, start_pos, stop_pos)))



url_local = ""



fg = "%0d".join(ENSPs)
response = requests.post(url_,
                  params={"output_format": "json",
                          "foreground": fg_10000,
                          "enrichment_method": "genome",
                          "taxid": 9606})
df = pd.read_csv(StringIO(response.text), sep='\t')