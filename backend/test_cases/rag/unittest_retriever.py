import unittest
import json
from utils.all_utils import read_config
from rag.retriever import data_retriever

import os

class TestRetriever(unittest.TestCase):
    def test_retriever(self, query:str):
        print('\n Unit test for retriever started')
        config_path = "./config/config.yaml"
        config = read_config(config_path)
        partition_config = config["partitioning"]
        
        retriever_obj = data_retriever(config_path)
        db, client = retriever_obj.chroma_vector_store()
        
        if len(str(client.heartbeat()))>0:
            print('\n- Unittest for chroma connection passed')
            try:
                retriever = db.as_retriever(search_kwargs={'k': 1})
                print('\n- query :',query)
                chunks = retriever.invoke(query)
                print('\n- chunks :',chunks)
                print('\n -- Unittest for retriever passed -- ')
            except Exception as e:
                print('Exception : ',e)

        else:
            print('\n- Unittest for chroma connection failed')
            

if __name__ == '__main__':
    obj = TestRetriever()
    query = 'What is the DT-Companion?'
    obj.test_retriever(query)