from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserResistViewSet

router = DefaultRouter()
router.register('', UserResistViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls))
]
