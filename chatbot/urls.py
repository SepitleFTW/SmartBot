from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), #this is the main chatbot page
    path('chat/', views.chatbot_view, name='chatbot'),
]
