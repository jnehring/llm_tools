# LLM Tools

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
python3 -m llm.run --llm dummy_llm --mode http_api
```

Send a post request to the Dummy LLM:

```
curl -X POST -d '{"doc": "hello world"}'  -H "Content-Type: application/json" http://localhost:5000/api/generate
```

Call the dummy LLM from a remote LLM:

```
python3 -m llm.run --llm http --mode oneshot --input_str="hallo" --api_url "http://localhost:5000/api/generate"
```

**Run oneshot interaction with OpenAI Davinci**

```
export OPENAI_API_KEY=...
python3 -m llm.run --llm openai_davinci --mode http_api
```