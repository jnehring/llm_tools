import requests

def call_llm(input_str, api_url="http://localhost:5000/api/generate"):
    body = {'doc': input_str}
    x = requests.post(api_url, json = body)
    return x.json()

if __name__ == "__main__":

    template_str = '''Assign labels to text document. Here are some examples:

Label #greeting: Hello, Hi, How are you doing?
Label #bye: Goodbye, adios, it was nice to meet you.

What is the label of this text?

__INPUT__'''
    
    prompt = template_str.replace("__INPUT__", "Good morning")
    response = call_llm(prompt)
    response_str = response["response"]
    print(response_str)
