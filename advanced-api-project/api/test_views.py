from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create a test user and login
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass')

        # Create an author and a book instance
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author
        )

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_book(self):
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2021,
            'author': self.author.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Book')

    def test_update_book(self):
        url = reverse('book-update', args=[self.book.id])
        data = {
            'title': 'Updated Book',
            'publication_year': 2022,
            'author': self.author.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')

    def test_delete_book(self):
        url = reverse('book-delete', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_filter_books_by_publication_year(self):
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 2020})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(book['publication_year'] == 2020 for book in response.data))

    def test_search_books_by_title(self):
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any('Test' in book['title'] for book in response.data))

    def test_unauthenticated_cannot_create(self):
        self.client.logout()
        url = reverse('book-create')
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(url, data)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_unauthenticated_can_list(self):
        self.client.logout()
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
