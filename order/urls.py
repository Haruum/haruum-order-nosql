from django.urls import path
from .views import serve_create_order


urlpatterns = [
    path('create/', serve_create_order),
]
