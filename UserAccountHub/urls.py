from django.contrib import admin
from django.urls import path 

from UserAccountHub import views

urlpatterns = [
    path('users/', views.user_list),
    path('users/<str:username_or_email>/', views.user_detail_view_by_username_or_email),

]