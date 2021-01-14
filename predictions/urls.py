import django.contrib.auth.views as auth_views
from django.urls import path
from predictions import views

urlpatterns = [
    path('predictions/', views.predictions_view, name='predictions'),
    path('volume/', views.volume_view, name='volume'),
    path('results/', views.results_view, name='results'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login_form.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='users/logout_form.html'), name='logout'), 
    path('', views.guest_view, name='guest_page'),
    path('bet/', views.make_bet_view, name='make_bet'),
    path('history/', views.my_bets_history_view, name='history'),
    path('pending/', views.my_pending_bets_view, name='pending'),
]