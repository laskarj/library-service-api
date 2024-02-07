from rest_framework import viewsets
from rest_framework.serializers import ModelSerializer

from books.permissions import IsAdminUserOrReadOnly
from books.models import Book
from books.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminUserOrReadOnly, )
