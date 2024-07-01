from channels.generic.websocket import AsyncWebsocketConsumer
from rag.retriever import data_retriever
from rag.generation import data_generation
import json
import logging
from django.http import JsonResponse
from utils.all_utils import read_config
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from django.conf import settings
from django.http import FileResponse, Http404
from io import BytesIO

logger = logging.getLogger(__name__)

tempCategories = [
    {
    "category_id": "policies:cat1",
    "description": "ndjkendejk djend jd ej"},
    {
    "category_id": "policies:cat3",
    "description": "ndjkendejk djend jd ej"},
    {
    "category_id": "supply:cat136",
    "description": "fr djend jd ej"}
]

class ChatConsumer(AsyncWebsocketConsumer):
    """
    Represents a WebSocket consumer for handling chat messages.

    This consumer handles the connection, disconnection, and message receiving
    events for the chat functionality.

    Attributes:
        None

    Methods:
        connect: Called when a WebSocket connection is established.
        disconnect: Called when a WebSocket connection is closed.
        receive: Called when a message is received from the WebSocket connection.
    """

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # db, client = data_retriever().chroma_vector_store()
        db = settings.dt_companion_db_instance
        retriever = db.as_retriever(search_kwargs={'k': 5})
        
        chain = data_generation().rag_chain()
        text_data_json = json.loads(text_data)
        if text_data_json.get('request_type') == 'category_selection':
            print("category_selection called\n\n", text_data_json.get('category_id'), text_data_json.get('previous_query'))
            message = text_data_json["previous_query"]
            retriever.search_kwargs = {"filter":{"category_id":text_data_json.get('category_id')},"k":5}
            chunks = retriever.get_relevant_documents(message)
        elif text_data_json.get('request_type') == 'query':
            message = text_data_json["message"]
            chunks = retriever.get_relevant_documents(message)
        number_of_category = [category.metadata['category_id'] for category in chunks]

        print('\nnumber_of_category :',number_of_category)
        is_all_same = all(x == number_of_category[0] for x in number_of_category)
        unique_categories = list(set(number_of_category))
        unique_categories = [{'category_id': item} for item in unique_categories]
        print('\nunique_categories :',unique_categories)
        if is_all_same or len(unique_categories) == 0:
            try:
                sources = []
                for doc in chunks:
                    source = {
                        "filename": doc.metadata.get('file_id', None), #['filename'], #.get('filename'),
                        "page": doc.metadata.get('page_number', None) #.get('page'),
                    }
                    sources.append(source)
                    response_sources = {
                        "event_type": "answer_init",
                        "answer_id": None,
                        "sources": sources,
                    }
            # Stream the response
                async for chunk in chain.astream_events({'context': chunks,'question': message}, version="v1", include_names=["Assistant"]):
                    if chunk["event"] == "on_parser_start":
                        response = {
                            "event_type": chunk.get('event'),
                            "answer_id": chunk.get('run_id'),
                            "answer_part": chunk['data'].get('chunk'),
                        }
                        await self.send(text_data=json.dumps(response))
                        
                        response_sources["answer_id"] = chunk.get('run_id')
                        await self.send(text_data=json.dumps(response_sources))
                                       
                    elif chunk["event"] == "on_parser_stream":
                        response = {
                            "event_type": chunk.get('event'),
                            "answer_id": chunk.get('run_id'),
                            "answer_part": chunk['data'].get('chunk'),
                        }
                        await self.send(text_data=json.dumps(response))
                    
                    elif chunk["event"] == "on_parser_end":
                        await self.send(text_data=json.dumps({'event_type': 'on_parser_end',"answer_id": chunk.get('run_id')}))

            except Exception as e:
                logger.error("\nError in receiving socket data: %s", e)
        else:
            await self.send(text_data=json.dumps({
            'event_type': 'categories_list',
            'categories': unique_categories
        }))

def health_check(request):
    config_path = "./config/config.yaml"
    config = read_config(config_path)
    generation_model = config["generation_model"]
    db, client = data_retriever().chroma_vector_store()
    try:

        llm = AzureChatOpenAI(temperature=generation_model['temperature'],
                                azure_deployment=generation_model['azure_deployment'],
                                openai_api_version=generation_model['openai_api_version'])
        response = llm.invoke(
            [
                HumanMessage(
                    content="Translate this sentence from English to French: I love programming."
                )
            ]
        )
        logger.info("\nResponse: %s", response)
        if len(response.content)>0 and len(str(client.heartbeat()))>0:
            logger.info("\nThe llm in Azure OpenAI and Chroma DB is working")
            return JsonResponse({"status": "OK"}, status=200)
        else:
            logger.error("There was an error with the llm in Azure OpenAI or Chroma DB")
            return JsonResponse({"status": "failed"}, status=500)

    except Exception as e:

        # If any service is not available, return a HTTP 500 response with the message "failed"
        logger.error("There was an error with the llm in Azure OpenAI or Chroma DB: %s", e)
        return JsonResponse({"status": e}, status=500)
    
def get_source_file(request, source_id):
    file_data = settings.file_storage.loadFile(source_id)
    
    print("\nfile_data:", file_data)
    if file_data is not None:
        return FileResponse(BytesIO(file_data), content_type='application/pdf')
    else:
        raise Http404("File not found.")

