from django.shortcuts import render
from channels.generic.websocket import AsyncWebsocketConsumer
import base64
import io
import logging
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app_data_ingestion import data_pipeline
from utils.all_utils import read_config
from django.conf import settings

logger = logging.getLogger(__name__)

import json
from django.conf import settings

class config_file:
    def __init__(self, 
                 config_path = "./config/config.yaml"):
        self.config_path = config_path
        self.config = read_config(config_path)
        self.partition_config = self.config["partitioning"]

async def upload_docx(request):
    if request.method == 'POST':
        # iterate over all uploaded files
        uploaded_files = request.FILES.getlist('files')
        categories = json.loads(request.POST.get('categories'))

        for index, file in enumerate(uploaded_files):
            file_name = str(file)
            # From the front end 
            topic = 'House of Policies'
            category = categories[index]
            category_id = topic + ':' + category
            # Check if the file is a .docx or .doc file
            if not file_name.endswith(('.docx', '.doc')):
                error_message = 'Unsupported file format. Only .docx and .doc files are supported.'
                logger.error(error_message)
                return JsonResponse({'error': error_message}, status=400)
           
            # Check if the file size is less than or equal to 10 MB
            if file.size > 10 * 1024 * 1024:
                error_message = 'File size exceeds the limit of 10 MB.'
                logger.error(error_message)
                return JsonResponse({'error': error_message}, status=400)     
                 
            logger.info("\nfile :%s", file)
            logger.info("\nfile type :%s", type(file))
            
            file_bytes = file.read()
            logger.info("\ntype -> file_bytes :%s", type(file_bytes))
            
            file_id = settings.file_storage.storeFile(file_name, file_bytes)
            print('file id', file_id)
            vector_store = data_pipeline().process(file_id=file_id, file=io.BytesIO(file_bytes),category_id=category_id) # file_io = io.BytesIO(file_bytes) # file=file_io
        return JsonResponse({'message': 'Files received and processed.'})
    else:
        logger.error("Error in upload_docx: Invalid request type")
        return JsonResponse({'error': 'Invalid request.'}, status=400)

