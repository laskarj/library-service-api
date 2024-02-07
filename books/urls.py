from django.urls import path
from rest_framework.routers import DefaultRouter

from views import BookViewSet

app_name = "books"

router = DefaultRouter()

router.register("books", BookViewSet, basename="books")

urlpatterns = [path("", include(router.urls))]
