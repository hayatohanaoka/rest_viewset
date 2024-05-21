from django.urls import path, include
from .views import FacilityViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# facility の URL を自動生成して router に登録
router.register(
    'facility', FacilityViewSet, basename='facility'
)

urlpatterns = [
    path('', include(router.urls))
]
