import unittest
import json
from utils.all_utils import read_config
from rag.generation import data_generation
from langchain.schema.runnable import RunnablePassthrough
import logging
import os

logger = logging.getLogger(__name__)

class TestGeneration(unittest.TestCase):
    def test_generation(self, context:str, question:str):
        print('\n Unit test for generation started')
        config_path = "./config/config.yaml"
        config = read_config(config_path)
        
        generation_obj = data_generation(config_path)
        chain = generation_obj.rag_chain()
        
        rag_chain = (
                {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
                | chain
                )
        
        
        print(f"\n- context:{context}")
        print(f"\n- question:{question}")
        answer = rag_chain.invoke({'context':context,'question':question})
        print('\n- answer :',answer)
        
        print('\n -- Unittest for generation passed -- ')
            

if __name__ == '__main__':
    obj = TestGeneration()
    context = """DT-Companion is a internal chatbot that helps Daimler Truck Employees in answering their queries.
                The frontend and backend of the chatbot is developed by the dedicated DT-Companion team.
                The Pareto distribution is a continuous power law distribution that is based on the observations that Pareto made."""
    query = 'What is the DT-Companion?'
    obj.test_generation(context, query)