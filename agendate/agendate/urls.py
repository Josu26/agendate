from django.urls import path
from authentication import views as auth_views  # Import the views from your authentication app

urlpatterns = [
    path('login/', auth_views.login, name='login'),
    path('register/', auth_views.register, name='register'),
    path('logout/', auth_views.logout, name='logout'),
    path('forgotpassword/', auth_views.forgotpassword, name='forgotpassword'),
    path('dashboard/', auth_views.dashboard, name='dashboard'),
    path('appointments/', auth_views.appointments, name='appointments'),
    path('business_info/', auth_views.business_info, name='business_info'),
    path('calendar_popup/', auth_views.calendar_popup, name='calendar_popup'),
    path('change_password/', auth_views.change_password, name='change_password'),
    path('profile/', auth_views.profile, name='profile'),
    path('profile/update/', auth_views.update_profile, name='update_profile'),
    path('clients/', auth_views.clients, name='clients'),
    path('communications/', auth_views.communications, name='communications'),
    path('chatbot/', auth_views.chatbot, name='chatbot'),
    path('reports/', auth_views.reports, name='reports'),
    path('settings/', auth_views.settings, name='settings'),
    path('help/', auth_views.help, name='help'),
    path('', auth_views.index, name='index'),
    path('chat/', auth_views.chat_view, name='chat_view'),  # Adjust the path for the chat
]
