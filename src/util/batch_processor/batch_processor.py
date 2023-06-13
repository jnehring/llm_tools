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

def batch_process(api, file_in, file_out):
    
    df = pd.read_csv(file_in, dtype=str)
    if "input" not in df.columns:
        raise ValueError("Input csv must have an 'input' column")
    
    # Create a column if it doesn't exist already
    df['output'] = df.get('output', None) 
    with tqdm(df.itertuples(), total = df.shape[0], ascii=True, desc=f"processing {file_in}", unit="rows") as pbar:
        for row in pbar:
            #Skip rows which already have an output
            if not pd.isnull(df.loc[row.Index, 'output']): 
                pbar.update()
                continue 
            df.loc[row.Index, 'output'] = call_llm(row.input, api)['response']
            df.to_csv(file_out, index=False)
            # time.sleep(1)
            pbar.update()


    timer = pbar.format_dict["elapsed"]
    print(f"Processed {df.shape[0]} rows in {timer:.4} seconds. ({df.shape[0]/timer:.4} rows/second)")
    print(f"Saved results into {file_out}")

    
if __name__ == "__main__":
    ap = argparse.ArgumentParser(prog="batch_processor",
                                 description="Process a csv data in api")
    
    ap.add_argument("--api", type=str, help= "API URL")
    ap.add_argument("-i", "--input", type=str, help = "input file path")
    ap.add_argument("-o", "--output", type=str, help = "output file path")

    args = ap.parse_args()
    api = "http://localhost:5000/api/generate" if args.api is None else args.api
    file_in = "input.csv" if args.input is None else args.input
    file_out = "output.csv" if args.output is None else args.output
    batch_process(api, file_in, file_out)