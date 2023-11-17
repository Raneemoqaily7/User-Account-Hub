from django.contrib import admin
from django.urls import path 

from rest_framework.authtoken.views import obtain_auth_token
from UserAccountHub import views

urlpatterns = [
    
    path('register/', views.registeration_view ),
    path('login/', obtain_auth_token ),

    path('users/', views.user_list),
    path('users/<str:username_or_email>/', views.user_detail_view_by_username_or_email),
    path('deleteuser/', views.delete_users),
    path('adduser/', views.add_user),
    path('updateuser/<int:id>', views.update_user),
    path('accounts/', views.accounts_list),
    path('accountdetail/<str:search_query>/', views.account_by_id),
    path('deleteaccounts/', views.delete_accounts),
    path('updateaccount/<int:id>', views.update_account),
   

] 