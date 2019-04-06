from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer
from rest_framework import viewsets

# (setq-local python-shell-interpreter (rel-path "../venv/bin/python"))
# Create your views here.


class BookViewset(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
