from django.urls import path
from .views import registration_view, home_view, login_view, profile_view, logout_view, forgot_password_view, reset_password_view

urlpatterns = [
    path('', home_view, name='home_view'),
    path('home/', home_view, name='home_view'),
    path('register/', registration_view, name='registration_view'),
    path('login/', login_view, name='login_view'),
    path('profile/', profile_view, name='profile_view'),
    path('logout/', logout_view, name='logout_view'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('reset-password/<str:pk>/<str:token>/', reset_password_view, name='reset_password'),
]