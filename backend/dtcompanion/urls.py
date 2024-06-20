"""
URL configuration for dtcompanion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

from django.urls import path  
from chat import views as chat_views
from knowledge_manager import views as knowledge_manager_views

urlpatterns = [  
    path('api/knowledge_manager/', knowledge_manager_views.upload_docx , name='upload_docx'),
    path('api/health_check/', chat_views.health_check, name='health_check'),
    path('api/chat/get_source_file/<str:source_id>/', chat_views.get_source_file, name='get_source_file')
]

