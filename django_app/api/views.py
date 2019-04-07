from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer
from rest_framework import viewsets, decorators, fields
from rest_framework.response import Response
from api.filters import BookFilter
from django_filters import rest_framework as filters

# (setq-local python-shell-interpreter (rel-path "../venv/bin/python"))
# Create your views here.


class BookViewset(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = BookFilter

    @decorators.action(methods=['POST'], detail=False)
    def batch(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def validate_title(self, value):
        assert value, 'Value is exapected'


class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    @decorators.action(methods=['POST'], detail=False)
    def batch(self, request, *args, **kwargs):
        serializer = AuthorSerializer(data=request.data, many=True)
        assert serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
