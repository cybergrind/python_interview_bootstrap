import django_filters
from django_filters import rest_framework as filters
from django.contrib.postgres.search import TrigramDistance
from django.db.models import F, Value
from tipsi_tools.django.db.pgfields import WordSimilarity
from tipsi_tools.django.db.utils import set_word_similarity_threshold


class TrigramFilterDistance(django_filters.CharFilter):
    def __init__(self, *args, **kwargs):
        self.distance_threshold = kwargs.pop('distance_threshold', 0.9)
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        if value:
            qs = (qs.annotate(distance=TrigramDistance(self.field_name, value))
                  .order_by('-distance', 'pk')
                  .filter(distance__lte=self.distance_threshold))
            print(qs.explain())
            for i in qs:
                print(i.distance)
        return qs


class TrigramFilterField(django_filters.CharFilter):
    def __init__(self, *args, **kwargs):
        self.similarity_threshold = kwargs.pop('similarity_threshold', 0.6)
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        if value:
            if self.similarity_threshold:
                set_word_similarity_threshold(1 - self.similarity_threshold)
            similarity = WordSimilarity(Value(value), F(self.field_name))
            qs = (
                qs.annotate(similarity=similarity)
                .order_by('similarity', 'pk')
                .filter(**{f'{self.field_name}__similar': value})
            )
            print(qs.explain())
            for i in qs:
                print(f'{i.similarity} => {value}/{i}')
        return qs


class BookFilter(filters.FilterSet):
    title_similarity = TrigramFilterField(field_name='title')
    title_distance = TrigramFilterDistance(field_name='title')
