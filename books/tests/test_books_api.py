from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from books.models import Book
from books.serializers import BookSerializer


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
        serializer = BookSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book_unauthorized(self):
        payload = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "SOFT",
            "inventory": 3,
            "daily_fee": Decimal("1.99"),
        }
        response = self.client.post(BOOKS_BASE_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_book_detail(self):
        book = sample_book()

        url = detail_url(book.id)
        response = self.client.get(url)

        serializer = BookSerializer(book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_book_detail_unauthorized(self):
        book = sample_book()
        url = detail_url(book.id)

        response = self.client.patch(url, {"title": "New title"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        book.refresh_from_db()
        self.assertEqual(book.title, "Test Book")

    def test_delete_book_unauthorized(self):
        book = sample_book()
        url = detail_url(book.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AdminUserBooksApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_user(
            email="test@admin.com", password="testpass123", is_staff=True
        )
        self.client.force_authenticate(self.admin_user)

    def test_create_book(self):
        payload = {
            "title": "Test Admin",
            "author": "Test Author",
            "cover": "SOFT",
            "inventory": 3,
            "daily_fee": Decimal("1.99"),
        }
        response = self.client.post(BOOKS_BASE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        book = Book.objects.get(id=response.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(book, key))


