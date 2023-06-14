import json
import requests
import os
import time
import argparse
import pandas as pd
from tqdm import tqdm

def call_llm(input_str, api_url="http://localhost:5000/api/generate"):
    body = {'doc': input_str}
    x = requests.post(api_url, json = body)
    return x.json()

def batch_process(args):
    
    df = pd.read_csv(args.input_file, dtype=str)
    if args.input_column not in df.columns:
        raise ValueError("Input csv must have an 'input' column")
    
    # Create a column if it doesn't exist already
    df[args.output_column] = df.get(args.output_column, None) 
    with tqdm(df.itertuples(), total = df.shape[0], ascii=True, desc=f"processing {args.input_file}", unit="rows") as pbar:
        for row in pbar:
            #Skip rows which already have an output
            if not pd.isnull(df.loc[row.Index, args.output_column]): 
                pbar.update()
                continue 
            input_str = row.__getattribute__(args.input_column)
            df.loc[row.Index, args.output_column] = call_llm(input_str, args.api)['response']
            df.to_csv(args.output_file, index=False)
            # time.sleep(1)
            pbar.update()


    timer = pbar.format_dict["elapsed"]
    print(f"Processed {df.shape[0]} documents in {timer:.4} seconds. ({df.shape[0]/timer:.4} documents/second)")
    print(f"Saved results into {args.output_file}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(prog="batch_processor",
                                 description="Process a csv data in api")
    
    ap.add_argument("--api", type=str, default="http://localhost:5000/api/generate", help= "API URL")
    ap.add_argument("-i", "--input_file", default="input.csv", type=str, help = "input file path")
    ap.add_argument("-o", "--output_file", default="output.csv", type=str, help = "output file path")
    ap.add_argument("-ic", "--input_column", default="input", type=str, help = "name of the input data column")
    ap.add_argument("-oc", "--output_column", default="output", type=str, help = "name of the output data column")

    args = ap.parse_args()

    try:
        batch_process(args)
    except KeyboardInterrupt:
        pass