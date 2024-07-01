import os
import logging
from utils.all_utils import read_config
from chromadb import Settings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(r'.env')

logger = logging.getLogger(__name__)

class FileStorage:

    def storeFile(self, file_name, content):
        pass
    
    def loadFile(self, file_id):
        pass

class FilesystemFileStorage (FileStorage):
    def __init__(self, file_storage_path):
        self.file_storage_path = file_storage_path

    def storeFile(self, file_name, content):
        file_path = os.path.join(self.file_storage_path, file_name)
        with open(file_path, 'wb') as f:
            f.write(content)
        return file_name

    def loadFile(self, file_id):
        file_path = os.path.join(self.file_storage_path, file_id)
        with open(file_path, 'rb') as f:
            return f.read()