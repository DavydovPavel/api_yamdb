from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title


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
