from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import AzureOpenAIEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever
from utils.all_utils import read_config
import os
import chromadb
import logging
from chromadb import Settings
from langchain.storage import InMemoryStore
from django.conf import settings

logger = logging.getLogger(__name__)

class data_retriever:
    def __init__(self, 
                 config_path = "./config/config.yaml"):
        self.config_path = config_path
        self.config = read_config(config_path)
            
    def chroma_vector_store(self,):
        """
        Retrieves a Chroma vector store from a server or from local storage.

        This function retrieves a Chroma vector store from a server if the CHROMA_HOST environment variable is set; 
        otherwise, it retrieves the vector store from local storage. 
        The embedding function used is AzureOpenAIEmbeddings.

        Returns:
            db: The retrieved Chroma vector store.

        Environment Variables:
            CHROMA_HOST (str): The host address of the Chroma server. If not set, the vector store is retrieved from local storage.
            EMBEDDING_MODEL (str): The Azure deployment for the AzureOpenAIEmbeddings.
            CHROMA_COLLECTION_NAME (str): The name of the collection to retrieve from the Chroma server or local storage.
            CHROMA_PORT (str): The port number of the Chroma server.
        """



        if settings.DTC_CHROMA_HOST != '':
            try:
                logger.info("Retrieving from server chroma db")
                emb_fn=AzureOpenAIEmbeddings(azure_deployment=settings.DTC_EMBEDDING_MODEL,
                                                        openai_api_version="2023-05-15")
                collection_name = settings.DTC_CHROMA_COLLECTION_NAME 
                client = chromadb.HttpClient(host=settings.DTC_CHROMA_HOST, port=settings.DTC_CHROMA_PORT, settings=Settings(allow_reset=True, anonymized_telemetry=False))
                logger.info("client.heartbeat:%s",client.heartbeat())
                db = Chroma(client=client, collection_name=collection_name, embedding_function=emb_fn)
            except Exception as e:
                logger.error(f'\n Error in connecting to chroma db server {settings.DTC_CHROMA_HOST} : {e}')
        else:
            try:
                logger.info("Retrieving from local chroma db")
                self.chormaDB_local_config = self.config["chorma_db_local"]
                client = None
                emb_fn=AzureOpenAIEmbeddings(azure_deployment=self.chormaDB_local_config['embedding_model'],
                                                        openai_api_version="2023-05-15")
                collection_name = self.chormaDB_local_config["collection_name"]
                db = Chroma(persist_directory=self.chormaDB_local_config["persist_directory"], 
                            collection_name=collection_name, 
                            embedding_function=emb_fn)
            except Exception as e:
                logger.error(f'\n Error in connecting to local chroma db : {e}')
        return db, client

    def multivectorretrieval(self,):
        '''
        Retrieve similar elements using multivector retriever
        '''
        store = InMemoryStore()
        vectorstore = self.chroma_vector_store()
        retriever = MultiVectorRetriever(
                                vectorstore=vectorstore,
                                docstore=store,
                                # id_key=id_key,
                            )
        
        return retriever