import pandas as pd
import json

infile = "~/Downloads/tweets.csv"
df = pd.read_csv(infile)

out = [{"input_doc": x} for x in list(df.Text)][0:10]
outfile = "util/batch_processor/example_data/input_data.json"
f = open(outfile, "w")
json.dump(out, f, indent=4)
f.close()
print("wrote " + outfile)