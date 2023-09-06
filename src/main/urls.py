from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('create/', views.create_view, name='create'),
    path('view/<str:graph_id>/', views.result_view, name='view'),
]
