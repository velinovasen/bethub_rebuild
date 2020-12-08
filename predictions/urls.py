from django.urls import path
from predictions import views

urlpatterns = [
    path('predictions/', views.predictions_view, name='predictions'),
    path('volume/', views.volume_view, name='volume'),

]