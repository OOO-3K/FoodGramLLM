"""
URL configuration for llm_server project.

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
from gemini_call.views import gemini_questions_en_index, gemini_description_en_index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("gemini/questions/en/", gemini_questions_en_index),
    path("gemini/description/en/", gemini_description_en_index),
]
