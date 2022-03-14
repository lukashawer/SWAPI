from swc import views
from django.urls import path

app_name = "swc"
urlpatterns = [
    path('collections', views.collections, name='collections'),
    path('refres_collection', views.refres_collection, name='refres_collection'),
    path('collection/<int:id>/<int:rows>', views.collection, name='collection'),
    path('grouping_stat/<int:doc_id>/<str:new_q>/<str:curent_q>', views.grouping_stat, name='grouping_stat'),
]