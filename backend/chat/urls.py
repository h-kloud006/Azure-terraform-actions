from django.urls import path  
import views  
  
  
urlpatterns = [
    path('ws/chat/', views.ChatConsumer.as_asgi()),
    path('api/chat/get_source_file/<str:source_id>/', views.get_source_file, name='get_source_file')
]
