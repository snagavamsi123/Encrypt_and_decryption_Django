from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('decrypt',views.decrypt,name='decrypt'),
    path('encrypt',views.encrypt,name='encrypt'),
]