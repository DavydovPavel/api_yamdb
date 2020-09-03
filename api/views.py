from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status, viewsets, filters, mixins
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

from .models import Category, Comment, Genre, Review, Title
from .permissions import IsAdminOrUserOrReadOnly, IsAdminUser, ReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          CreateUserSerializer, GenreSerializer,
                          MeInfoUserSerializer, MyTokenObtainPairSerializer,
                          ReviewSerializer, TitleSerializer, UsersSerializer)

User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    """
     Takes a set of user credentials and returns an access and refresh JSON web
     token pair to prove the authentication of those credentials.
    """
    serializer_class = MyTokenObtainPairSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeInfoUserSet(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = MeInfoUserSerializer

    def get_object(self):
        return self.request.user


class CreateUserSet(viewsets.ViewSetMixin, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        new_user_email = self.request.data.get('email')
        new_user_token = str(uuid4())

        if serializer.is_valid():
            serializer.save(username=new_user_email,
                            email=new_user_email, token=new_user_token)
            send_mail(
                'Тема письма',
                new_user_token,
                'from@example.com',  # Это поле "От кого"
                # Это поле "Кому" (можно указать список адресов)
                [new_user_email],
                # Сообщать об ошибках («молчать ли об ошибках?»)
                fail_silently=False,
            )

            return Response(status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminUser | ReadOnly,]
    """ filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'genre', 'name', 'year'] """
    filter_backends = [filters.SearchFilter]
    search_fields = ['=category', '=genre', '=name', '=year']
    
class GenreViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser | ReadOnly,]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    

class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin, 
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser | ReadOnly,]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminUser | ReadOnly,]#(IsAdminOrUserOrReadOnly,)

    def get_queryset(self):
        self.title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return self.title.reviews

    def perform_create(self, serializer):
        serializer.save(title=self.title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrUserOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        self.review = get_object_or_404(
            title.reviews, pk=self.kwargs.get('review_id'))
        return self.review.comments

    def perform_create(self, serializer):
        serializer.save(review=self.review)
