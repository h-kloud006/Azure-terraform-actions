import os
from dotenv import load_dotenv
from django.conf import settings

# Load environment variables from .env file
load_dotenv()

# Define constants
DTC_OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DTC_AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
DTC_CHROMA_HOST = os.getenv('CHROMA_HOST')
DTC_CHROMA_PORT = os.getenv('CHROMA_PORT')
DTC_EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL')
DTC_CHROMA_COLLECTION_NAME = os.getenv('CHROMA_COLLECTION_NAME')
DTC_STORAGE_PATH = os.getenv('STORAGE_PATH')
DTC_ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS')

# Set the attributes in settings for later access if needed
setattr(settings, 'DTC_OPENAI_API_KEY', DTC_OPENAI_API_KEY)
setattr(settings, 'DTC_AZURE_OPENAI_ENDPOINT', DTC_AZURE_OPENAI_ENDPOINT)
setattr(settings, 'DTC_CHROMA_HOST', DTC_CHROMA_HOST)
setattr(settings, 'DTC_CHROMA_PORT', DTC_CHROMA_PORT)
setattr(settings, 'DTC_EMBEDDING_MODEL', DTC_EMBEDDING_MODEL)
setattr(settings, 'DTC_CHROMA_COLLECTION_NAME', DTC_CHROMA_COLLECTION_NAME)
setattr(settings, 'DTC_STORAGE_PATH', DTC_STORAGE_PATH)
setattr(settings, 'DTC_ALLOWED_HOSTS', DTC_ALLOWED_HOSTS)


