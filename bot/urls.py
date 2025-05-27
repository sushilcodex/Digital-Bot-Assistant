from django.urls import path
from .views import chatbot_page, chat_api

urlpatterns = [
    path('', chatbot_page, name='chatbot_page'),
    path('api/', chat_api, name='chat_api'),
]
