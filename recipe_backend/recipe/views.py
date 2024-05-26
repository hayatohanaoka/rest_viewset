from rest_framework import viewsets, mixins, permissions, decorators
from rest_framework.response import Response

from .models import Recipe, Ingredient
from .serializers import RecipesSerializer, IngredientSerializer

# Create your views here.
class RequestViewSet(viewsets.ModelViewSet):

    def get_serializer_context(self):
        """
        serializer にデータを追加して渡すためのメソッド
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class RecipeViewSet(RequestViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    model = Recipe


class IngredientViewSet(RequestViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    model = Recipe
