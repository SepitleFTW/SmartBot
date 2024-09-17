from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), #this is the main chatbot page
    path('chat/', views.chatbot_view, name='chatbot'),
    path('conversation_logs/', views.conversation_logs, name='conversation_logs'),
    path('user-data/', views.user_data, name='user_data'),

]
