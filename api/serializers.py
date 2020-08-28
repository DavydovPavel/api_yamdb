from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title

User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = (
            'first_name', 'last_name', 'username',
            'bio', 'email', 'role'
        )


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category
