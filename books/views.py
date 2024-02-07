from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.serializers import ModelSerializer

from books.models import Book
from books.serializers import (
    BookSerializer,
    InventorySerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self) -> ModelSerializer:
        if self.action in ("put", "patch"):
            return InventorySerializer
        return BookSerializer
