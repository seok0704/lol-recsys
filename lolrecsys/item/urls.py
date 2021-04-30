from django.urls import path,include
from . import views

app_name = 'item'

urlpatterns = [
    path('recommend/', views.item_rec, name='item_rec'),
]
