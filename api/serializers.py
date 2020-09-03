from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import Field, empty
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('email',)


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


class MeInfoUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = (
            'first_name', 'last_name', 'username',
            'bio', 'email', 'role'
        )
        read_only_fields = ('email', 'role')


class MyTokenObtainSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD

    default_error_messages = {
        'no_active_account': _(
            'No active account found with the given credentials'
        )
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, attrs):
        self.user = User.objects.filter(
            email__iexact=attrs[self.username_field]
        ).first()

        if not self.user:
            raise ValidationError('The email is not valid.')

        if self.user:
            if not self.user.check_token(attrs['confirmation_code']):
                raise ValidationError('The confirmation_code is not valid.')

        if self.user is None or not self.user.is_active:
            raise ValidationError(
                'No active account found with the given credentials')

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError(
            'Must implement "get_token" method for "MyTokenObtain" subclasses')


class MyTokenObtainPairSerializer(MyTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ['name', 'slug']
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreField(
        slug_field="slug",
        required=False,
        many=True,
        queryset=Genre.objects.all()
    )
    category = CategoryField(
        slug_field="slug",
        required=False,
        queryset=Category.objects.all() 
    )
    #rating = serializers.FloatField()
        
    class Meta:
        fields = ("id", "name","year", "description", "genre", "category",)
        model = Title


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
