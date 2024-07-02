from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/date/', views.data_view, name='date'),
    path('dashboard/chat/', views.chat_view, name='chat'),
    path('api/chatbot/', views.ChatbotAPIView.as_view(), name="chat_bot"),
    path('api/welcome-message/', views.WelcomeMessageAPIView.as_view(), name="welcome_message"),
    path('api/device-data/', views.DeviceDataAPIView.as_view(), name="welcome_message"),
    path('api/temperatures/', views.TemperatureListAPIView.as_view(), name='temperature-list'),
    path('api/temperatures/recent/', views.RecentTemperatureListAPIView.as_view(), name='temperature-list'),
]
