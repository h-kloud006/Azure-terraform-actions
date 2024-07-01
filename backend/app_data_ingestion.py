from utils.all_utils import read_config
from data_ingestion.partition import data_partition
from data_ingestion.chunking import data_chunking
from data_ingestion.vectordb import VectorDB
import os
from django.conf import settings

class data_pipeline:
    def __init__(self,
                 config_path = "./config/config.yaml"):
        self.config_path = config_path
        self.config = read_config(self.config_path)
        self.partition_config = self.config["partitioning"]
        
    def process(self, file_id=None, file=None,category_id=None):
        """
        Processes a file or a directory of files and stores the resulting vector store either locally or on a Chroma server.

        This function partitions the data from the given file or the files in the given directory, chunks the partitioned data, and then creates a vector store from the chunks. 
        If the CHROMA_HOST environment variable is set, the vector store is pushed to a Chroma server; otherwise, it is saved to disk.

        Args:
            file (str, optional): The path to the file to process. If None, the function processes the files in the directory specified in the partition_config. Default is None.

        Returns:
            vectorstore: The created vector store.

        Environment Variables:
            CHROMA_HOST (str): The host address of the Chroma server. If not set, the vector store is saved to disk.
        """
        print('\nfilepath in Data Ingestion :',file_id)
        elements = data_partition().process(file_id=file_id,file=file,category_id=category_id)
        chunks =  data_chunking().partition_default_chunks(elements)
        if settings.DTC_CHROMA_HOST != '':
            vectorstore = VectorDB().chormaDB_server(chunks, save_to_disk=True)
            print('\n vectorstore pushed to chroma server sucessfully')
        else:
            vectorstore = VectorDB().chormaDB_local(chunks, save_to_disk=True)
            print('\n vectorstore saved to disk sucessfully')
        
        return vectorstore
    
if __name__ == '__main__':
    obj = data_pipeline()
    obj.process(data_path=None)
