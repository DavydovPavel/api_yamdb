from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Category, Comment, Genre, Review, Title
import datetime
User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('email',)


class UsersSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = (
            'first_name', 'last_name', 'username',
            'bio', 'email', 'role'
        )


class MyTokenObtainSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD

    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, attrs):
        # self.user = authenticate(**{
        #     self.username_field: attrs[self.username_field],
        #     'token': attrs['confirmation_code'],
        # })
        self.user = User.objects.filter(
            email__iexact=attrs[self.username_field]
            # , token=attrs[self.confirmation_code]
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
            'Must implement "get_token" method for "MyTokenObtainSerializer" subclasses')


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
