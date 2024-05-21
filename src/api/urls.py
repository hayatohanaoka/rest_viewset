from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EquipmentViewSet, FacilityViewSet

router = DefaultRouter()
# facility の URL を自動生成して router に登録
router.register(
    'facility', FacilityViewSet, basename='facility'
)
router.register(
    'equipment', EquipmentViewSet, basename='equipment'
)

urlpatterns = [
    path('', include(router.urls))
]
