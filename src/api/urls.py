from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    EquipmentViewSet,
    FacilityViewSet,
    FacilityTypeViewSet,
    UserViewSet,
    UserPictureViewSet
)

router = DefaultRouter()
# facility の URL を自動生成して router に登録
router.register(
    'facility', FacilityViewSet, basename='facility'
)
router.register(
    'equipment', EquipmentViewSet, basename='equipment'
)
router.register(
    'facility_type', FacilityTypeViewSet, basename='facility_type'
)
# パターンマッチの順番関係で、これを先にする必要性がある
router.register(
    'user', UserPictureViewSet, basename='user_picture'
)
router.register(
    'user', UserViewSet, basename='user'
)

urlpatterns = [
    path('', include(router.urls))
]
