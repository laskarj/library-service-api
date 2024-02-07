from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from books.models import Book
from books.serializers import (
    BookSerializer,
    InventorySerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self):
        if self.action in ("put", "patch"):
            return InventorySerializer
        return BookSerializer
