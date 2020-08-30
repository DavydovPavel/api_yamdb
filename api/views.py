from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.generics import get_object_or_404

from .models import Category, Comment, Genre, Review, Title
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        self.title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return self.title.reviews

    def perform_create(self, serializer):
        serializer.save(title=self.title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        self.review = get_object_or_404(title.reviews, pk=self.kwargs.get('review_id'))
        return self.review.comments

    def perform_create(self, serializer):
        serializer.save(review=self.review)
