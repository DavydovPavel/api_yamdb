from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets

from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Genre, Title
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          UsersSerializer)

User = get_user_model()


class UsersViewSet(viewsets.ViewSetMixin, generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'genre', 'name', 'year']


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
