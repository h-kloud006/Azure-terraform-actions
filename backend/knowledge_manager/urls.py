from django.urls import path  
import views  
  


urlpatterns = [
    path('api/knowledge_manager/', views.upload_docx, name='upload_docx'),
]