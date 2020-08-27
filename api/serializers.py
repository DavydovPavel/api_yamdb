from rest_framework import serializers
from .models import Title, Genre, Category


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
