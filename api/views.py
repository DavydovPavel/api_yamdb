from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, filters
from rest_framework.response import Response
from .models import Title, Genre, Category, User
from .serializers import TitleSerializer, GenreSerializer, CategorySerializer
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend


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