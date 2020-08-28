from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .serializers import UsersSerializer

User = get_user_model()


class UsersViewSet(viewsets.ViewSetMixin, generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
