# import requests
# from io import StringIO
# import pandas as pd
# call api_help for help and argument defaults

# response = requests.get(r"https://agotool.org/api_help")
# print(response.json())

from io import StringIO
import pandas as pd
import requests
url_ = r"https://agotool.org/api"
ENSPs = ["9606.ENSP00000266970"]
fg = "%0d".join(ENSPs)
result = requests.post(url_,
                   params={"output_format": "tsv",
                           "filter_foreground_count_one": False,
                           "enrichment_method": "characterize_foreground"},
                   data={"foreground": fg})
df = pd.read_csv(StringIO(result.text), sep='\t')
print(df.head())