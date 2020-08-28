from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = (
            'first_name', 'last_name', 'username',
            'bio', 'email', 'role'
        )