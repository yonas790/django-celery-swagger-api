from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('send-email/', views.send_email, name='send-email'),
    path('process-data/', views.process_data, name='process-data'),
]
