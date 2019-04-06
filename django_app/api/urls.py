from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views


router = DefaultRouter()
router.register('book', views.BookViewset)
router.register('author', views.AuthorViewset)

app_patterns = [
    *router.urls
]

urlpatterns = [
    path('001/', include(app_patterns))
]
