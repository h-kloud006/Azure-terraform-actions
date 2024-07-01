from django.urls import re_path  
from . import views  

websocket_urlpatterns = [  
    re_path(r'/knowledge_manager/$', views.upload_docx),  
]
