from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import RecipeViewSet, IngredientViewSet

router = SimpleRouter()
router.register('recipe', RecipeViewSet, basename='recipe')
router.register('ingredient', IngredientViewSet, basename='ingredient')

urlpatterns = [
    path('', include(router.urls))
]