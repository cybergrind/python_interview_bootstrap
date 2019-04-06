from api.models import Author, Book
from rest_framework_dyn_serializer import DynModelSerializer


class AuthorSerializer(DynModelSerializer):
    class Meta:
        model = Author
        fields_param = 'author_fields'
        limit_fields = True


class BookSerializer(DynModelSerializer):
    author = AuthorSerializer(nested=True, limit_fields=True)

    class Meta:
        model = Book
        limit_fields = True
        fields_param = 'book_fields'
