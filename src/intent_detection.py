from llm.openai import OpenAIDavinci
from prompts.prompt_template import PromptTemplate

if __name__ == "__main__":

    template_str = '''Assign labels to text document. Here are some examples:

Label #greeting: Hello, Hi, How are you doing?
Label #bye: Goodbye, adios, it was nice to meet you.

What is the label of this text?

__INPUT__'''
    template = PromptTemplate(template_str)
    prompt = template.create_prompt("Good morning")

    llm = OpenAIDavinci()
    response = llm.generate_response(prompt)
    print(response)