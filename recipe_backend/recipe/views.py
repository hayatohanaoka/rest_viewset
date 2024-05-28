from rest_framework import viewsets, serializers
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.filters import OrderingFilter

from .models import Recipe, Ingredient
from .serializers import RecipesSerializer, IngredientSerializer
from user.models import CustomUser
from query.reader import Reader


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    model = Recipe
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('title',)
    ordering_fields = ('id', 'title', 'created_at', 'updated_at')

    def _get_user_related_token(self):
        token = self.request.headers["Authorization"].replace('Token ', '')
        query = Reader.get_by_file('get_user.sql').replace('Authorization', token)
        user = CustomUser.objects.raw(query)[0]
        return user
    
    def perform_create(self, serializer):
        user = self._get_user_related_token()
        # self.request.user がAnonymsUserになってしまう
        # serializer.save(author=self.request.user)  
        serializer.save(author=user)
    
    def perform_update(self, serializer):
        # /recipe/recipe/<pk>
        user = self._get_user_related_token()
        recipe_id = self.kwargs['pk']
        author_id = get_object_or_404(Recipe, id=recipe_id).author.id
        
        # self.request.user がAnonymsUserになってしまう
        # if author != self.request.user: 
        if author_id != user.id:
            raise serializers.ValidationError('レシピ更新失敗')

        serializer.save()
    
    def perform_destroy(self, instance):
        user = self._get_user_related_token()
        
        # self.request.user がAnonymsUserになってしまう
        # if instance.author != self.request.user: 
        if instance.author != user:
            raise serializers.ValidationError('レシピ削除失敗')
        
        instance.delete()


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    model = Recipe

    def perform_create(self, serializer):
        recipe = serializer.validated_data['recipe']
        if recipe.user != self.request.user:
            raise serializers.ValidationError('材料追加不可')
        serializer.save(recipe=recipe)
    
    def perform_update(self, serializer):
        pk = self.kwargs['ok']
        ingredient = get_object_or_404(Ingredient, pk=pk)
        recipe = ingredient.recipe
        if recipe.user != self.request.user:
            raise serializers.ValidationError('材料更新不可')
        serializer.save(recipe=recipe)

    def perform_destroy(self, instance):
        if instance.recipe.author != self.request.user:
            raise serializers.ValidationError('材料削除失敗')
        
        instance.delete()
