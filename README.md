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

**HTTP API interaction with OpenAI Davinci**

```
export OPENAI_API_KEY=...
python3 -m llm.run --llm openai_davinci --mode http_api
```

**Adding a new LLM to llm_tools**

```
Inside llm_registry.py file, add a new entry to the llm_registry dictionary, mapping a unique name for your LLM to a lambda function that creates an instance of your LLM class.
Inside my_llm.py, define a class that inherits from the LLMWrapper abstract class. This class will represent your LLM implementation.
You have successfully added a new LLM to the llm_tools.
```

**llm_tools web user interface**

```
There is a Web user interface available to interact with llm.
Start the HTTP API with any desired llm. This will also start the service of web interface.
You can open web UI through your browser using local IP (127.0.0.1:5000).
The web UI looks like this.
![WebUI](https://github.com/jnehring/llm_tools/assets/94236355/05a6badd-4d8f-4f8d-b6fc-b3313b6742dc)
You can type in any text in the textbox that you want to sent to llm and press send. 
The result will be displayed in the lower white box.
```
