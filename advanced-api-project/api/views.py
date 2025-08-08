from django.shortcuts import render
from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from .models import Book, Author
from .serializers import BookSerializer

# Create your views here.
#ListViews: Katseft kulshy 1 books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    
    # Add filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Fields for filtering (exact match)
    filterset_fields = ['title', 'author__name', 'publication_year']

    # Fields for searching (text search)
    search_fields = ['title', 'author__name']

    # Fields for ordering
    ordering_fields = ['title', 'publication_year']

    # Optional: default ordering
    ordering = ['title']

#DetailView: katseft book whd b id
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

 # CreateView : create the book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

 #UpdateView : update the book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
 # delete the book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]      


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass')

        # Create author and book for tests
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

    def test_permissions_for_unauthenticated(self):
        self.client.logout()
        url_create = reverse('book-create')
        response = self.client.post(url_create, {'title': 'No Auth Book', 'publication_year': 2023, 'author': self.author.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # or 401 depending on settings

        url_list = reverse('book-list')
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # allowed for unauthenticated

   
