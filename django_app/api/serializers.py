from api.models import Author, Book
from rest_framework import serializers
from rest_framework_dyn_serializer import DynModelSerializer


class LimitedBook(DynModelSerializer):
    class Meta:
        model = Book
        limit_fields = True
        fields_param = 'book_fields'
        fields = ['id', 'title']


class AuthorSerializer(DynModelSerializer):
    books = LimitedBook(nested=True, read_only=True, many=True)

    class Meta:
        model = Author
        fields_param = 'author_fields'
        limit_fields = True


class BookSerializer(DynModelSerializer):
    author = AuthorSerializer(nested=True, fields=['id', 'name'])

    def validate_title(self, value):
        if value.lower().startswith('math'):
            raise serializers.ValidationError('Book about math is not allowed')
        return value

    class Meta:
        model = Book
        limit_fields = True
        fields_param = 'book_fields'
