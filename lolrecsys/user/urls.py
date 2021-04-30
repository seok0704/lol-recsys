from django.urls import path,include
from . import views

app_name = 'user'

urlpatterns = [
    path('recommend/', views.user_rec, name='user_rec'),
]
