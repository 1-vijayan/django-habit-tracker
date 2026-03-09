from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.home, name="home"),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('register/', views.register, name="register"),

    path('complete/<int:habit_id>/', views.complete_habit, name="complete"),

    path('delete/<int:habit_id>/', views.delete_habit, name="delete"),

    path("profile/", views.profile, name="profile"),
]