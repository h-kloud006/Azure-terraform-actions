import os
from django.apps import AppConfig
from retry import retry
import logging
from .config import data_retriever_instance
from django.conf import settings

class CommonAppConfig(AppConfig):
    name = 'config'

    @retry(tries=3, delay=1, logger=logging)
    def initialize_db_instance(self):
        
        # Attempt to initialize the database instance
        db_instance = data_retriever_instance.chroma_vector_store()
        
        # Set the db_instance in settings for later access if needed
        setattr(settings, 'dt_companion_db_instance', db_instance)
        
    def initialize_file_storage(self):
        from .fileStorage import FilesystemFileStorage
        from django.conf import settings

        file_storage_path = os.getenv('FILE_STORAGE_PATH')
        file_storage = FilesystemFileStorage(file_storage_path=file_storage_path)

        setattr(settings, 'file_storage', file_storage)

    def ready(self):
        try:
            self.initialize_db_instance()
        except Exception as e:
            logging.error(f"Failed to connect to database after multiple retries: {e}")
        
        self.initialize_file_storage()
