class PromptTemplate:

    def __init__(self, template : str):
        self.template = template

    def create_prompt(self, input):
        prompt = self.template.replace("__INPUT__", input)
        return prompt