from swc import views
from django.urls import path

app_name = "swc"
urlpatterns = [
    path('collections', views.collections, name='collections'),
]