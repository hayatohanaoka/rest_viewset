from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserResistViewSet, UserLoginViewSet

router = DefaultRouter()
router.register('', UserResistViewSet, basename='user')
router.register('', UserLoginViewSet, basename='login')

urlpatterns = [
    path('', include(router.urls))
]
