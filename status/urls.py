from django.urls import path
from .views import (
    serve_get_laundry_progress_statuses,
    serve_update_laundry_progress_status,
)


urlpatterns = [
    path('all/', serve_get_laundry_progress_statuses),
    path('update/', serve_update_laundry_progress_status),
]
