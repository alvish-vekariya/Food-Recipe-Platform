from django.contrib import admin
from django.urls import path,include
from vege import views

urlpatterns = [
    path('',views.receipes,name='receipes'),
    path('delete/<id>/',views.delete, name='delete'),
    path('update/<id>/',views.update, name='update'),
    path('login_page',views.login_page, name='login_page'),
    path('logout_page',views.logout_page, name='logout_page'),
    path('register',views.register, name='register')
]