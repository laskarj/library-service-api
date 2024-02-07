from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from books.models import Book
from books.serializers import BookListSerializer, BookDetailSerializer


BOOKS_BASE_URL = reverse("books:book-list")


def sample_book(**params):
    defaults = {
        "title": "Test Book",
        "author": "John Dou",
        "cover": "HARD",
        "inventory": 10,
        "daily_fee": 1.99,
    }
    defaults.update(params)
    return Book.objects.create(**defaults)


def detail_url(book_id: int):
    return reverse("books:book-detail", args=[book_id])


class UnauthorizedBooksApiTests(TestCase):
    """
    Test cases for unauthorized access to Books API endpoints.
    """

    def setUp(self):
        self.client = APIClient()

    def test_list_movie(self):
        sample_book()
        sample_book()

        response = self.client.get(BOOKS_BASE_URL)

        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book_forbidden(self):
        payload = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "SOFT",
            "inventory": 3,
            "daily_fee": 1.99,
        }
        response = self.client.post(BOOKS_BASE_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_book_detail(self):
        book = sample_book()

        url = detail_url(book.id)
        response = self.client.get(url)

        serializer = BookDetailSerializer(book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_book_detail_not_allowed(self):
        book = sample_book()
        url = detail_url(book.id)

        response = self.client.patch(url, {"title": "New title"})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        book.refresh_from_db()
        self.assertEqual(book.title, "Test Book")

    def test_delete_book_not_allowed(self):
        book = sample_book()
        url = detail_url(book.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
