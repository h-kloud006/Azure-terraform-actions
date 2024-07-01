from langchain_openai import AzureChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from utils.all_utils import read_config
from rag.retriever import data_retriever
from rag.augmentation import template
from dotenv import load_dotenv
load_dotenv(r'.env')


class data_generation:
    def __init__(self, 
                 config_path = "./config/config.yaml"):
        self.config_path = config_path
        self.config = read_config(config_path)
        self.generation_model = self.config["generation_model"]
        
    def rag_chain(self):
        
        """
        Creates a RAG (Retrieval-Augmented Generation) pipeline.

        This function creates a RAG pipeline with a chat prompt, an AzureChatOpenAI model, and a StrOutputParser. 
        The chat prompt is generated from a template, and the AzureChatOpenAI model and StrOutputParser are configured with specific run names.

        Returns:
            chain: The created RAG pipeline.
        """
        prompt = template().prompt()
        model = AzureChatOpenAI(temperature=self.generation_model['temperature'],
                                azure_deployment=self.generation_model['azure_deployment'],
                                openai_api_version=self.generation_model['openai_api_version'])

        # RAG pipeline
        chain = (prompt
                | model.with_config({"run_name": "model"})
                | StrOutputParser().with_config({"run_name": "Assistant"})
            )
        return chain
        
        
        
if __name__ == '__main__':
    input = 'What is the percentage difference between the share for Window-Eyes between May 2012 and September 2010?'
    chain = data_generation().rag_chain()