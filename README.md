## Table of contents
- [LLM Tools](#llm-tools)
  - [Installation](#installation)
  - [Usage](#usage)
- [llm\_tools web user interface](#llm_tools-web-user-interface)
- [batch\_processor](#batch_processor)
  - [Usage](#usage-1)
# LLM Tools

## Starting an LLM on the DFKI Cluster

Clone the repository. Use an example slurm starter skript from the [llm models table](https://docs.google.com/spreadsheets/d/1F6T_ZPiEomYrfvpy64GUmuO0CiSQ4LrZrgM4BjSLmKA/edit#gid=0). Then make the starter skript executable and execute it (replace __PATH__ with your installation directory)

```
chmod +x __PATH__/src/slurm/run_llm.sh
./usrun.sh -p A100-40GB --gpus=1 --time 08:00:00 --mem 100GB __PATH__/src/slurm/run_llm.sh vicuna7b
```

## Installation

1. Create a virtual environment, e.g. with Conda. We recommend Python 3.9.6.
2. Install the requirements: `pip3 install -r requirements.txt`

## Usage

You can start the command line tool to do a oneshot interaction with the LLM. Or you can start an HTTP API. Here are some examples:

**Get help**

```
$ python3 -m llm.run --help
usage: LLM Tools [-h] --llm LLM [--input_str INPUT_STR] [--mode {http_api,oneshot}]

optional arguments:
  -h, --help            show this help message and exit
  --llm LLM             Specify which LLM you want to load.
  --input_str INPUT_STR
                        Specify input document. For mode=oneshot.
  --mode {http_api,oneshot}
```

**One shot interaction with the Dummy LLM**

```
python3 -m llm.run --llm dummy_llm --mode oneshot --input_str="hallo"
```

**Start the HTTP API with the Dummy LLM** 

```
python3 -m llm.run --mode http_api --llm dummy_llm
```

Send a post request to the Dummy LLM:

```
curl -X POST -d '{"doc": "hello world"}'  -H "Content-Type: application/json" http://localhost:5000/api/generate
```

Call the dummy LLM from a remote LLM:

```
python3 -m llm.run --llm http --mode oneshot --input_str="hallo" --api_url "http://localhost:5000/api/generate"
```

**HTTP API interaction with OpenAI Davinci**

```
export OPENAI_API_KEY=...
python3 -m llm.run --llm openai_davinci --mode http_api
```

**Adding a new LLM to llm_tools**

```
Inside llm_registry.py file, add a new entry to the llm_registry dictionary, 
mapping a unique name for your LLM to a lambda function that creates an instance of your LLM class.
Inside my_llm.py, define a class that inherits from the LLMWrapper abstract class. 
This class will represent your LLM implementation.
You have successfully added a new LLM to the llm_tools.
```

# llm_tools web user interface

```
There is a Web user interface available to interact with llm.
Start the HTTP API with any desired llm using the --http_api parameter. This will also start the service of web interface.
You can open web UI through your browser using local IP (127.0.0.1:5000).
You can type in any text in the textbox that you want to sent to llm and press send. 
The result will be displayed in the lower white box.
```
![WebUI](https://github.com/jnehring/llm_tools/assets/94236355/05a6badd-4d8f-4f8d-b6fc-b3313b6742dc)

# batch_processor
Tool for processing CSV files with llm. 
## Usage
Help:
```
$ python batch_processor.py -h
usage: batch_processor [-h] [--api API] [-i INPUT_FILE] [-o OUTPUT_FILE] [-ic INPUT_COLUMN] [-oc OUTPUT_COLUMN] [--max_new_tokens MAX_NEW_TOKENS] [--temperature TEMPERATURE]

Process a csv data in api

options:
  -h, --help            show this help message and exit
  --api API             API URL; defaults to 'http://localhost:5000/api/generate'
  -i INPUT_FILE, --input_file INPUT_FILE
                        input file path; defaults to 'input.csv'
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        output file path; defaults to 'output.csv'
  -ic INPUT_COLUMN, --input_column INPUT_COLUMN
                        name of the input data column; defaults to 'input'
  -oc OUTPUT_COLUMN, --output_column OUTPUT_COLUMN
                        name of the output data column; defaults to 'output'
  --max_new_tokens MAX_NEW_TOKENS
                        maximum model return size in tokens; defaults to 10
  --temperature TEMPERATURE
                        model output temperature between 0 and 2, defines how random is output; defaults to 1
```
Each entry in an INPUT_COLUMN of INPUT_FILE will be sent to API.

OUTPUT_FILE is a copy of an input file with a new column OUTPUT_COLUMN (default = 'output') which contains API responses. 

If input file already has an 'output' column - only rows with empty output will be processed. Processing may be interrupted(via CTRL+C in UNIX) at any point and continued later by using an output file as an input. 

Example usage
```
$ python3.11 batch_processor.py -i output.csv
processing output.csv: 100%|########################################| 60/60 [00:00<00:00, 673.91rows/s]
Processed 60 rows in 0.08912 seconds. (673.3 rows/second)
Saved results into output.csv
```
