from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),

    path("register/", views.register, name="register"),

    path("profile/", views.profile, name="profile"),

    path("complete/<int:habit_id>/", views.complete_habit, name="complete"),

    path("delete/<int:habit_id>/", views.delete_habit, name="delete"),
]