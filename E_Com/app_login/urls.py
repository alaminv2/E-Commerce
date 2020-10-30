from django.urls import path
from app_login import views

app_name = 'app_login'


urlpatterns = [
    path('sign_up/', views.signUpView, name="sign_up"),
    path('login/', views.loginView, name="login"),
    path('logout/', views.logoutView, name="logout"),
    path('profile/', views.profileView, name="profile"),
]
