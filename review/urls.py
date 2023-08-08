from django.urls import path
from .views import serve_create_review_for_order, serve_get_reviews_of_outlet


urlpatterns = [
    path('create/', serve_create_review_for_order),
    path('outlet/', serve_get_reviews_of_outlet),
]
