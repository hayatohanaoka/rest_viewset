from rest_framework import serializers

from .models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'quantity', 'recipe')
        read_only_fields = ('id',)


class RecipesSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'instruction', 'author', 'updated_at', 'ingredients')
        read_only_fields = ('id', 'author', 'updated_at')
