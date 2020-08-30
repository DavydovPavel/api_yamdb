from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import Field, empty

from .models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CurrentUserField(Field): 
    """
    CurrentUserField заполняет поле пользователем
    из sel.context['request'].
    """
    def to_representation(self, value):
        return str(value)
    
    def get_value(self, dictionary):
        return self.context.get('request').user

    def to_internal_value(self, data):
        return data


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


class ReviewSerializer(serializers.ModelSerializer):
    author = CurrentUserField()

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = CurrentUserField()

    class Meta:
        fields = '__all__'
        model = Comment
