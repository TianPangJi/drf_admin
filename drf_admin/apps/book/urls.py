from django.urls import path

from chatbot.views import centre

# from drf_admin.apps.chatbot import views

urlpatterns = [
    # path('save-message/', views.index, name='index'), 
    path('save-message/', centre.ChatMessageUpdateAPIView.as_view()), 
    # path('save-message/', centre.SaveMessageAPIView.as_view()), 
    path('get-message/', centre.GetMessageAPIView.as_view()), 
]