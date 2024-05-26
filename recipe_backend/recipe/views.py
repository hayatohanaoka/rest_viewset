from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

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
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('title',)
    ordering_fields = ('id', 'title', 'created_at', 'updated_at')


class IngredientViewSet(RequestViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    model = Recipe
