from langchain.prompts import ChatPromptTemplate

class template:
    def __init__(self):
        self.template = """Answer the question based only on the following context, 
                        which can include text and tables:
                        {context}
                        Question: {question}
                        """
    
    def prompt(self):
        
        """
        Generates a chat prompt from a template.

        Returns:
            prompt: The generated chat prompt.
        """

        prompt = ChatPromptTemplate.from_template(self.template)
        return prompt