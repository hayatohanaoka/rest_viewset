from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'quantity', 'recipe')
        read_only_fields = ('id',)

    def validate(self, data):
        recipe = get_object_or_404(Recipe, id=data['recipe'].id)
        user = self.context['request'].user
        if recipe.author != user:
            raise serializers.ValidationError('このレシピは更新できません')
        return data


class RecipesSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'instruction', 'author', 'updated_at', 'ingredients')
        read_only_fields = ('id', 'author', 'updated_at')
    
    
    def create(self, validated_data):
        """
        author にログインユーザーを自動でセットする
        """
        user = self.context['request'].user
        return Recipe.objects.create(author=user, **validated_data)
