import json
import requests
import os
import time

def call_llm(input_str, api_url="http://localhost:5000/api/generate"):
    body = {'doc': input_str}
    x = requests.post(api_url, json = body)
    return x.json()

def batch_process():
    infile = "util/batch_processor/example_data/input_data.json"
    outfile = "util/batch_processor/example_data/output_data.json"

    input_data = json.load(open(infile, "r"))

    api_url = "http://192.168.33.209:5000"

    docs = []
    start_time = time.time()
    for doc in input_data:

        response = call_llm(doc, api_url=api_url)
        doc["response"] = response
        docs.append(doc)

        f = open(outfile, "w")
        json.dump(docs, f, indent=4)
        f.close()

    t = time.time()/1000
    print(f"processed {len(input_data)} documents in {t} seconds.")

if __name__ == "__main__":
    batch_process()